from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .database import Database, decode_json, seconds_between, seconds_to_hms
from .export import build_export_workbook
from .questionnaire import POSTTEST_FIELDS, PRETEST_FIELDS, localized_task, posttest_schema, task_question_ids
from .scoring import check_response_pattern, check_timing, score_answers, score_supervision

SESSION_COOKIE_NAME = "questionnaire_session"
SESSION_COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 7
QUESTIONNAIRE_TIME_LIMIT_SECONDS = 40 * 60


class PretestPayload(BaseModel):
    consent: str
    age: int
    gender: str
    grade_year: str
    major: str
    programming_experience_years: str
    python_familiarity: str
    file_io_familiarity: str
    numpy_familiarity: str
    ai_tool_use_frequency: str
    ai_code_review_experience: str


class AgreementPayload(BaseModel):
    agreement: str


class TaskPayload(BaseModel):
    answers: dict[str, str]
    supervision_answers: dict[str, str] = {}


class PosttestPayload(BaseModel):
    post_attitude_useful: str
    post_attitude_confident: str
    post_attitude_learning_value: str
    post_attitude_cognitive_load: str
    post_attitude_future_use: str
    post_strategy_requirements_first: str
    post_strategy_trace_code: str
    post_strategy_predict_output: str
    post_strategy_test_cases: str
    post_strategy_delivery_risk: str
    post_trust_ai_correctness: str
    post_trust_ai_boundary_cases: str
    post_trust_ai_direct_submit: str
    post_trust_ai_with_review: str
    post_trust_ai_overall: str


def create_app(db_path: Path | None = None, admin_password: str | None = None) -> FastAPI:
    base_dir = Path(__file__).resolve().parents[1]
    db = Database(db_path or base_dir / "data" / "questionnaire.sqlite")
    password = admin_password or os.getenv("ADMIN_PASSWORD", "admin123")
    app = FastAPI(title="AI Supervision A/B Questionnaire")

    def set_session_cookie(response: Response, session_id: str) -> None:
        response.set_cookie(
            SESSION_COOKIE_NAME,
            session_id,
            max_age=SESSION_COOKIE_MAX_AGE_SECONDS,
            httponly=True,
            samesite="lax",
        )

    def clear_session_cookie(response: Response) -> None:
        response.delete_cookie(SESSION_COOKIE_NAME, samesite="lax")

    def cookie_session_id(request: Request) -> str | None:
        return request.cookies.get(SESSION_COOKIE_NAME)

    def require_cookie_session(request: Request) -> str:
        session_id = cookie_session_id(request)
        if not session_id:
            raise HTTPException(status_code=401, detail="No active session")
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=401, detail="No active session")
        if ensure_not_timed_out(session):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        return session_id

    def timeout_at_for_session(session: dict[str, Any]) -> str:
        from datetime import datetime

        started_at = datetime.fromisoformat(session["created_at"])
        return (started_at + timedelta(seconds=QUESTIONNAIRE_TIME_LIMIT_SECONDS)).isoformat()

    def has_submitted_pretest(session: dict[str, Any]) -> bool:
        pretest = decode_json(session["pretest_json"])
        return all(pretest.get(field) not in ("", None) for field in PRETEST_FIELDS)

    def elapsed_seconds_for_session(session: dict[str, Any]) -> int:
        from datetime import datetime, timezone

        if session["current_task"] == 0:
            return 0
        end_at = session["completed_at"] or session["abandoned_at"] or session["timeout_at"]
        if end_at:
            return seconds_between(session["created_at"], end_at) or 0
        started_at = datetime.fromisoformat(session["created_at"])
        return max(0, int((datetime.now(timezone.utc) - started_at).total_seconds()))

    def timing_metadata(session: dict[str, Any]) -> dict[str, int]:
        elapsed = elapsed_seconds_for_session(session)
        return {
            "time_limit_seconds": QUESTIONNAIRE_TIME_LIMIT_SECONDS,
            "elapsed_seconds": elapsed,
            "remaining_seconds": max(0, QUESTIONNAIRE_TIME_LIMIT_SECONDS - elapsed),
        }

    def ensure_not_timed_out(session: Any) -> bool:
        session_dict = dict(session)
        if session_dict["current_task"] == 0:
            return False
        if session_dict["completed_at"] or session_dict["abandoned_at"] or session_dict["timeout_at"]:
            return bool(session_dict["timeout_at"])
        elapsed = elapsed_seconds_for_session(session_dict)
        if elapsed <= QUESTIONNAIRE_TIME_LIMIT_SECONDS:
            return False
        db.mark_timeout(session_dict["id"], timeout_at_for_session(session_dict))
        return True

    def summarize_session(session_id: str) -> dict[str, Any]:
        rows = [row for row in db.all_rows() if row["session"]["id"] == session_id]
        if not rows:
            return {"status": "none"}
        row = rows[0]
        session_dict = dict(row["session"])
        if ensure_not_timed_out(session_dict):
            refreshed = db.admin_get_session(session_id)
            session_dict = dict(refreshed["session"])
            return {
                "status": "timeout",
                "participant_id": session_dict["participant_id"],
                "next_task": None,
                "next_stage": None,
                "valid": False,
                **timing_metadata(session_dict),
            }
        answers: dict[str, str] = {}
        supervision: dict[str, str] = {}
        for task_response in row["responses"]:
            answers.update(decode_json(task_response["answers_json"]))
            supervision.update(decode_json(task_response["supervision_json"]))
        formal = score_answers(answers)
        supervision_scores = score_supervision(supervision)
        posttest_ready = row["session"]["current_task"] > 6 and not row["session"]["posttest_submitted_at"]
        notice_ready = row["session"]["current_task"] == 0 and has_submitted_pretest(session_dict)
        pretest_ready = row["session"]["current_task"] == 0 and not notice_ready
        complete = bool(row["session"]["completed_at"])

        # Compute per-task durations and total duration for quality checks
        task_durations: dict[int, int | None] = {}
        for task_id in range(1, 7):
            start_row = row["starts"].get(task_id)
            resp = next((r for r in row["responses"] if r["task_id"] == task_id), None)
            task_durations[task_id] = seconds_between(
                start_row["started_at"] if start_row else None,
                resp["submitted_at"] if resp else None,
            )
        total_seconds = seconds_between(row["session"]["created_at"], row["session"]["completed_at"])
        timing_flags = check_timing(task_durations, total_seconds)
        pattern_flags = check_response_pattern(answers) if answers else []
        quality_flags = timing_flags + pattern_flags
        status = (
            "complete"
            if complete
            else "pretest"
            if pretest_ready
            else "notice"
            if notice_ready
            else "posttest"
            if posttest_ready
            else "in_progress"
        )
        next_stage = (
            None
            if complete
            else "pretest"
            if pretest_ready
            else "notice"
            if notice_ready
            else "posttest"
            if posttest_ready
            else "task"
        )

        return {
            "status": status,
            "participant_id": row["session"]["participant_id"],
            "next_task": None if row["session"]["current_task"] == 0 or row["session"]["current_task"] > 6 else row["session"]["current_task"],
            "next_stage": next_stage,
            "scores": {key: value for key, value in formal.items() if key != "per_question"},
            "supervision_scores": {key: value for key, value in supervision_scores.items() if key != "per_item"},
            "quality_flags": quality_flags,
            "valid": len(quality_flags) == 0,
            **timing_metadata(session_dict),
        }

    def quality_flags_for_row(row: dict[str, Any]) -> list[str]:
        answers: dict[str, str] = {}
        for response in row["responses"]:
            answers.update(decode_json(response["answers_json"]))
        task_durations = {}
        for task_id in range(1, 7):
            start_row = row["starts"].get(task_id)
            response = next((r for r in row["responses"] if r["task_id"] == task_id), None)
            task_durations[task_id] = seconds_between(
                start_row["started_at"] if start_row else None,
                response["submitted_at"] if response else None,
            )
        session = row["session"]
        total_seconds = seconds_between(session["created_at"], session["completed_at"])
        return check_timing(task_durations, total_seconds) + (check_response_pattern(answers) if answers else [])

    def completion_metadata(session: dict[str, Any], quality_flags: list[str]) -> dict[str, str | None]:
        if session["timeout_at"]:
            return {"completion_bucket": "incomplete", "incomplete_reason": "timeout"}
        if session["abandoned_at"]:
            return {"completion_bucket": "incomplete", "incomplete_reason": "abandoned"}
        if session["completed_at"] and not quality_flags:
            return {"completion_bucket": "normal_completed", "incomplete_reason": None}
        if session["completed_at"]:
            return {"completion_bucket": "incomplete", "incomplete_reason": "quality_failed"}
        if session["current_task"] > 6:
            return {"completion_bucket": "incomplete", "incomplete_reason": "pending_posttest"}
        return {"completion_bucket": "incomplete", "incomplete_reason": "in_progress"}

    def read_task_for_session(session_id: str, task_id: int, lang: str) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if task_id != session["current_task"] or task_id < 1 or task_id > 6:
            raise HTTPException(status_code=409, detail="This task is not available")
        db.mark_task_started(session_id, task_id)
        task = localized_task(task_id, lang)
        if session["group_name"] != "B" or task_id not in (1, 2):
            task["supervision_card"] = None
        return task

    def submit_task_for_session(session_id: str, task_id: int, payload: TaskPayload) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if task_id != session["current_task"] or task_id < 1 or task_id > 6:
            raise HTTPException(status_code=409, detail="This task is not available")
        required = set(task_question_ids(task_id))
        if set(payload.answers) != required:
            raise HTTPException(status_code=400, detail="All task questions must be answered")
        try:
            return db.save_task_response(session_id, task_id, payload.answers, payload.supervision_answers)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    def read_posttest_for_session(session_id: str, lang: str) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if session["current_task"] <= 6:
            raise HTTPException(status_code=409, detail="Posttest is not available")
        if session["posttest_submitted_at"]:
            raise HTTPException(status_code=409, detail="Posttest already submitted")
        return posttest_schema(lang)

    def submit_posttest_for_session(session_id: str, payload: PosttestPayload) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        data = payload.model_dump()
        missing = [field for field in POSTTEST_FIELDS if data.get(field) in ("", None)]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing posttest fields: {', '.join(missing)}")
        try:
            return db.save_posttest(session_id, data)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/session/start")
    def start_session_after_pretest(request: Request, payload: AgreementPayload, response: Response) -> dict[str, Any]:
        if payload.agreement != "I agree":
            raise HTTPException(status_code=400, detail="Research notice agreement is required")
        session_id = cookie_session_id(request)
        if not session_id:
            raise HTTPException(status_code=401, detail="Pretest is required before research notice agreement")
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=401, detail="No active session")
        if not has_submitted_pretest(dict(session)):
            raise HTTPException(status_code=409, detail="Pretest is required before research notice agreement")
        try:
            created = db.start_session(session_id, payload.agreement)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        refreshed = dict(db.get_session(session_id))
        set_session_cookie(response, created["session_id"])
        return {
            "participant_id": created["participant_id"],
            "next_task": created["next_task"],
            "next_stage": created["next_stage"],
            "time_limit_seconds": QUESTIONNAIRE_TIME_LIMIT_SECONDS,
            "remaining_seconds": timing_metadata(refreshed)["remaining_seconds"],
        }

    @app.post("/api/pretest")
    def submit_pretest(request: Request, payload: PretestPayload, response: Response) -> dict[str, Any]:
        session_id = cookie_session_id(request)
        pretest = payload.model_dump()
        missing = [field for field in PRETEST_FIELDS if pretest.get(field) in ("", None)]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")
        if pretest["consent"] != "I agree":
            raise HTTPException(status_code=400, detail="Consent is required")
        if not session_id:
            saved = db.create_session(pretest)
            set_session_cookie(response, saved["session_id"])
            return {
                "participant_id": saved["participant_id"],
                "next_task": saved["next_task"],
                "next_stage": saved["next_stage"],
            }
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            saved = db.create_session(pretest)
            set_session_cookie(response, saved["session_id"])
            return {
                "participant_id": saved["participant_id"],
                "next_task": saved["next_task"],
                "next_stage": saved["next_stage"],
            }
        if ensure_not_timed_out(session):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if session["current_task"] != 0:
            saved = db.create_session(pretest)
            set_session_cookie(response, saved["session_id"])
            return {
                "participant_id": saved["participant_id"],
                "next_task": saved["next_task"],
                "next_stage": saved["next_stage"],
            }
        try:
            saved = db.save_pretest(session_id, pretest)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {
            "participant_id": session["participant_id"],
            "next_task": saved["next_task"],
            "next_stage": saved["next_stage"],
        }

    @app.get("/api/session/current")
    def current_session(request: Request) -> dict[str, Any]:
        session_id = cookie_session_id(request)
        if not session_id:
            return {"status": "none"}
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            return {"status": "none"}
        return summarize_session(session_id)

    @app.post("/api/session/reset")
    def reset_session(request: Request, response: Response) -> dict[str, Any]:
        session_id = cookie_session_id(request)
        if session_id:
            db.abandon_incomplete_session(session_id)
        clear_session_cookie(response)
        return {"status": "none"}

    @app.get("/api/task/{task_id}")
    def read_current_task(request: Request, task_id: int, lang: str = "en") -> dict[str, Any]:
        return read_task_for_session(require_cookie_session(request), task_id, lang)

    @app.post("/api/task/{task_id}")
    def submit_current_task(request: Request, task_id: int, payload: TaskPayload) -> dict[str, Any]:
        return submit_task_for_session(require_cookie_session(request), task_id, payload)

    @app.get("/api/task/{session_id}/{task_id}")
    def read_task(session_id: str, task_id: int, lang: str = "en") -> dict[str, Any]:
        return read_task_for_session(session_id, task_id, lang)

    @app.post("/api/task/{session_id}/{task_id}")
    def submit_task(session_id: str, task_id: int, payload: TaskPayload) -> dict[str, Any]:
        return submit_task_for_session(session_id, task_id, payload)

    @app.get("/api/posttest")
    def read_current_posttest(request: Request, lang: str = "en") -> dict[str, Any]:
        return read_posttest_for_session(require_cookie_session(request), lang)

    @app.post("/api/posttest")
    def submit_current_posttest(request: Request, payload: PosttestPayload) -> dict[str, Any]:
        return submit_posttest_for_session(require_cookie_session(request), payload)

    @app.get("/api/posttest/{session_id}")
    def read_posttest(session_id: str, lang: str = "en") -> dict[str, Any]:
        return read_posttest_for_session(session_id, lang)

    @app.post("/api/posttest/{session_id}")
    def submit_posttest(session_id: str, payload: PosttestPayload) -> dict[str, Any]:
        return submit_posttest_for_session(session_id, payload)

    @app.get("/api/session/{session_id}/summary")
    def session_summary(session_id: str) -> dict[str, Any]:
        result = summarize_session(session_id)
        if result["status"] == "none":
            raise HTTPException(status_code=404, detail="Session not found")
        return result

    def require_admin(password: str) -> None:
        if password != password_value:
            raise HTTPException(status_code=401, detail="Invalid password")

    @app.get("/api/admin/export")
    def export(password: str) -> Response:
        require_admin(password)
        normal_completed_rows = [
            row
            for row in db.all_rows()
            if completion_metadata(dict(row["session"]), quality_flags_for_row(row))["completion_bucket"]
            == "normal_completed"
        ]
        content = build_export_workbook(normal_completed_rows)
        return Response(
            content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": 'attachment; filename="questionnaire_normal_completed_export.xlsx"'},
        )

    @app.get("/api/admin/sessions")
    def admin_list(password: str, include_abandoned: bool = False) -> list[dict[str, Any]]:
        require_admin(password)
        sessions = db.admin_list_sessions(include_abandoned)
        result = []
        for s in sessions:
            row = db.admin_get_session(s["id"])
            if row and not s["completed_at"] and not s["abandoned_at"] and not s["timeout_at"]:
                ensure_not_timed_out(s)
                row = db.admin_get_session(s["id"])
                s = row["session"]
            answers: dict[str, str] = {}
            for r in row["responses"]:
                answers.update(decode_json(r["answers_json"]))
            scores = score_answers(answers)
            flags = quality_flags_for_row(row)
            completion = completion_metadata(s, flags)
            result.append({
                "session_id": s["id"],
                "participant_id": s["participant_id"],
                "group": s["group_name"],
                "status": "abandoned" if s["abandoned_at"] else "timeout" if s["timeout_at"] else "complete" if s["completed_at"] else "in_progress",
                "current_task": s["current_task"],
                "created_at": s["created_at"],
                "completed_at": s["completed_at"],
                "abandoned_at": s["abandoned_at"],
                "total_score": scores["total_score"],
                "valid": len(flags) == 0,
                "quality_flags": flags,
                "total_duration_hms": seconds_to_hms(elapsed_seconds_for_session(s)),
                **completion,
            })
        return result

    @app.get("/api/admin/sessions/{session_id}")
    def admin_get(session_id: str, password: str) -> dict[str, Any]:
        require_admin(password)
        from .database import decode_json
        row = db.admin_get_session(session_id)
        if not row:
            raise HTTPException(status_code=404, detail="Session not found")
        s = row["session"]
        pretest = decode_json(s["pretest_json"])
        posttest = decode_json(s["posttest_json"])
        answers: dict[str, str] = {}
        supervision: dict[str, str] = {}
        for r in row["responses"]:
            answers.update(decode_json(r["answers_json"]))
            supervision.update(decode_json(r["supervision_json"]))
        scores = score_answers(answers)
        sup_scores = score_supervision(supervision)
        session = dict(s)
        session["total_duration_hms"] = seconds_to_hms(elapsed_seconds_for_session(session))
        return {
            "session": session,
            "pretest": pretest,
            "posttest": posttest,
            "answers": answers,
            "supervision": supervision,
            "scores": {k: v for k, v in scores.items() if k != "per_question"},
            "supervision_scores": {k: v for k, v in sup_scores.items() if k != "per_item"},
            "responses": row["responses"],
        }

    @app.delete("/api/admin/sessions/{session_id}")
    def admin_delete(session_id: str, password: str) -> dict[str, Any]:
        require_admin(password)
        if not db.admin_delete_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found or already abandoned")
        return {"ok": True}

    @app.patch("/api/admin/sessions/{session_id}")
    def admin_update(session_id: str, password: str, body: dict[str, Any]) -> dict[str, Any]:
        require_admin(password)
        if not db.admin_update_session(session_id, body):
            raise HTTPException(status_code=400, detail="No valid fields to update")
        return {"ok": True}

    @app.post("/api/admin/sessions/{session_id}/restore")
    def admin_restore(session_id: str, password: str) -> dict[str, Any]:
        require_admin(password)
        if not db.admin_restore_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        return {"ok": True}

    password_value = password
    app.mount("/", StaticFiles(directory=base_dir / "static", html=True), name="static")
    return app


app = create_app()
