from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .database import Database, decode_json, is_test_pretest, seconds_between, seconds_to_hms
from .export import build_export_workbook
from .questionnaire import (
    POSTTEST_FIELDS,
    PRETEST_FIELDS,
    PRETEST_IDENTITY_FIELDS,
    localized_task,
    normalize_questionnaire_version,
    posttest_schema,
    task_question_ids,
)
from .scoring import check_timing, score_answers, score_posttest, score_supervision
from .settings import QuestionnaireSettings

SESSION_COOKIE_NAME = "questionnaire_session"
VERSION_COOKIE_NAME = "questionnaire_version"
SESSION_COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 7
QUESTIONNAIRE_TIME_LIMIT_SECONDS = 40 * 60


class PretestPayload(BaseModel):
    consent: str
    questionnaire_version: str = "python"
    class_name: str
    student_name: str
    student_id: str
    grade_year: str
    major: str
    programming_experience_years: str
    python_familiarity: str
    file_io_familiarity: str
    numpy_familiarity: str | None = None
    ai_tool_use_frequency: str
    ai_code_review_experience: str


class AgreementPayload(BaseModel):
    agreement: str
    test_group: str | None = None


class TaskPayload(BaseModel):
    answers: dict[str, str]
    supervision_answers: dict[str, str] = {}


class PosttestPayload(BaseModel):
    post_supervisor_role: str
    post_requirements_first: str
    post_missing_conditions: str
    post_code_logic_tracing: str
    post_output_prediction: str
    post_test_design: str
    post_human_intervention: str
    post_responsible_submission: str


def create_app(db_path: Path | None = None, admin_password: str | None = None) -> FastAPI:
    base_dir = Path(__file__).resolve().parents[1]
    python_db_path = db_path or base_dir / "data" / "questionnaire.sqlite"
    c_db_path = (
        db_path.with_name(f"{db_path.stem}_c{db_path.suffix}")
        if db_path
        else base_dir / "data" / "questionnaire_c.sqlite"
    )
    agent_db_path = (
        db_path.with_name(f"{db_path.stem}_agent{db_path.suffix}")
        if db_path
        else base_dir / "data" / "questionnaire_agent.sqlite"
    )
    dbs = {
        "python": Database(python_db_path),
        "c": Database(c_db_path),
        "agent": Database(agent_db_path),
    }
    settings_path = (
        db_path.with_name(f"{db_path.stem}_settings.json")
        if db_path
        else base_dir / "data" / "questionnaire_settings.json"
    )
    questionnaire_settings = QuestionnaireSettings(settings_path)
    password = admin_password or os.getenv("ADMIN_PASSWORD", "admin123")
    app = FastAPI(title="AI Supervision A/B Questionnaire")

    def normalize_version_or_400(version: str | None) -> str:
        normalized = normalize_questionnaire_version(version)
        if version not in (None, "", normalized):
            raise HTTPException(status_code=400, detail="Unsupported questionnaire version")
        return normalized

    def db_for_version(version: str | None) -> Database:
        return dbs[normalize_version_or_400(version)]

    def require_enabled_version(version: str) -> None:
        if not questionnaire_settings.is_enabled(version):
            raise HTTPException(status_code=403, detail="This questionnaire version is currently closed")

    def request_version(request: Request) -> str:
        return normalize_questionnaire_version(request.cookies.get(VERSION_COOKIE_NAME))

    def request_db(request: Request) -> Database:
        return dbs[request_version(request)]

    def set_session_cookie(response: Response, session_id: str, version: str) -> None:
        response.set_cookie(
            SESSION_COOKIE_NAME,
            session_id,
            max_age=SESSION_COOKIE_MAX_AGE_SECONDS,
            httponly=True,
            samesite="lax",
        )
        response.set_cookie(
            VERSION_COOKIE_NAME,
            version,
            max_age=SESSION_COOKIE_MAX_AGE_SECONDS,
            httponly=True,
            samesite="lax",
        )

    def clear_session_cookie(response: Response) -> None:
        response.delete_cookie(SESSION_COOKIE_NAME, samesite="lax")
        response.delete_cookie(VERSION_COOKIE_NAME, samesite="lax")

    def cookie_session_id(request: Request) -> str | None:
        return request.cookies.get(SESSION_COOKIE_NAME)

    def require_cookie_session(request: Request) -> tuple[str, Database, str]:
        session_id = cookie_session_id(request)
        if not session_id:
            raise HTTPException(status_code=401, detail="No active session")
        version = request_version(request)
        require_enabled_version(version)
        db = dbs[version]
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=401, detail="No active session")
        if ensure_not_timed_out(session, db):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        return session_id, db, version

    def timeout_at_for_session(session: dict[str, Any]) -> str:
        from datetime import datetime

        started_at = datetime.fromisoformat(session["created_at"])
        return (started_at + timedelta(seconds=QUESTIONNAIRE_TIME_LIMIT_SECONDS)).isoformat()

    def pretest_fields_for_version(version: str) -> list[str]:
        return [
            field
            for field in PRETEST_FIELDS
            if version == "python" or field != "numpy_familiarity"
        ]

    def has_submitted_pretest(session: dict[str, Any]) -> bool:
        pretest = decode_json(session["pretest_json"])
        version = normalize_questionnaire_version(pretest.get("questionnaire_version"))
        return all(
            field == "questionnaire_version" or pretest.get(field) not in ("", None)
            for field in pretest_fields_for_version(version)
        )

    def is_test_session(session: dict[str, Any]) -> bool:
        return bool(session.get("is_test")) or is_test_pretest(decode_json(session.get("pretest_json")))

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

    def ensure_not_timed_out(session: Any, db: Database) -> bool:
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

    def summarize_session(session_id: str, db: Database) -> dict[str, Any]:
        rows = [row for row in db.all_rows() if row["session"]["id"] == session_id]
        if not rows:
            return {"status": "none"}
        row = rows[0]
        session_dict = dict(row["session"])
        if ensure_not_timed_out(session_dict, db):
            refreshed = db.admin_get_session(session_id)
            session_dict = dict(refreshed["session"])
            return {
                "status": "timeout",
                "participant_id": session_dict["participant_id"],
                "is_test": is_test_session(session_dict),
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
        posttest_scores = score_posttest(decode_json(row["session"]["posttest_json"]))
        posttest_ready = row["session"]["current_task"] > 6 and not row["session"]["posttest_submitted_at"]
        notice_ready = row["session"]["current_task"] == 0 and has_submitted_pretest(session_dict)
        pretest_ready = row["session"]["current_task"] == 0 and not notice_ready
        complete = bool(row["session"]["completed_at"])

        total_seconds = seconds_between(row["session"]["created_at"], row["session"]["completed_at"])
        timing_flags = check_timing({}, total_seconds)
        quality_flags = timing_flags
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
            "is_test": is_test_session(session_dict),
            "next_task": None if row["session"]["current_task"] == 0 or row["session"]["current_task"] > 6 else row["session"]["current_task"],
            "next_stage": next_stage,
            "scores": {key: value for key, value in formal.items() if key != "per_question"},
            "supervision_scores": {key: value for key, value in supervision_scores.items() if key != "per_item"},
            "posttest_scores": posttest_scores,
            "quality_flags": quality_flags,
            "valid": len(quality_flags) == 0,
            **timing_metadata(session_dict),
        }

    def quality_flags_for_row(row: dict[str, Any]) -> list[str]:
        session = row["session"]
        total_seconds = seconds_between(session["created_at"], session["completed_at"])
        return check_timing({}, total_seconds)

    def automatic_completion_metadata(session: dict[str, Any], quality_flags: list[str]) -> dict[str, str | None]:
        if session["abandoned_at"]:
            return {"completion_bucket": "incomplete", "incomplete_reason": "abandoned"}
        if session["timeout_at"]:
            return {"completion_bucket": "incomplete", "incomplete_reason": "timeout"}
        if session["completed_at"] and not quality_flags:
            return {"completion_bucket": "normal_completed", "incomplete_reason": None}
        if session["completed_at"]:
            return {"completion_bucket": "incomplete", "incomplete_reason": "quality_failed"}
        if session["current_task"] > 6:
            return {"completion_bucket": "incomplete", "incomplete_reason": "pending_posttest"}
        return {"completion_bucket": "incomplete", "incomplete_reason": "in_progress"}

    def completion_metadata(session: dict[str, Any], quality_flags: list[str]) -> dict[str, str | None]:
        automatic = automatic_completion_metadata(session, quality_flags)
        if automatic["incomplete_reason"] == "abandoned":
            return {**automatic, "completion_source": "auto"}
        override = session["completion_override"]
        if not override:
            return {**automatic, "completion_source": "auto"}
        if override == "normal_completed":
            return {
                "completion_bucket": "normal_completed",
                "incomplete_reason": None,
                "completion_source": "manual",
            }
        return {
            "completion_bucket": "incomplete",
            "incomplete_reason": override,
            "completion_source": "manual",
        }

    def average(values: list[float | int | None]) -> float | None:
        numeric = [value for value in values if value is not None]
        return round(sum(numeric) / len(numeric), 2) if numeric else None

    def scored_stats_row(row: dict[str, Any]) -> dict[str, Any]:
        answers: dict[str, str] = {}
        for response in row["responses"]:
            answers.update(decode_json(response["answers_json"]))
        scores = score_answers(answers)
        posttest_scores = score_posttest(decode_json(row["session"]["posttest_json"]))
        pretest = decode_json(row["session"]["pretest_json"])
        return {
            "session_id": row["session"]["id"],
            "participant_id": row["session"]["participant_id"],
            "is_test": is_test_session(dict(row["session"])),
            "group": row["session"]["group_name"],
            "class_name": pretest.get("class_name"),
            "student_name": pretest.get("student_name"),
            "student_id": pretest.get("student_id"),
            "total_score": scores["total_score"],
            "deliverability_score": scores["deliverability_score"],
            "reasoning_score": scores["reasoning_score"],
            "error_identification_score": scores["error_identification_score"],
            "post_agent_supervision_score": posttest_scores["post_agent_supervision_score"],
        }

    def stats_summary_for_version(version: str, db: Database) -> dict[str, Any]:
        rows = [row for row in db.all_rows() if not is_test_session(dict(row["session"]))]
        completed_rows = [row for row in rows if row["session"]["completed_at"]]
        normal_rows = [
            row
            for row in rows
            if completion_metadata(dict(row["session"]), quality_flags_for_row(row))["completion_bucket"]
            == "normal_completed"
        ]
        scored_rows = [scored_stats_row(row) for row in normal_rows]
        group_rows: list[dict[str, Any]] = []
        for group in ("A", "B"):
            group_scored = [row for row in scored_rows if row["group"] == group]
            group_rows.append({
                "version": version,
                "group": group,
                "sample_count": len(group_scored),
                "average_total_score": average([row["total_score"] for row in group_scored]),
                "average_deliverability_score": average([row["deliverability_score"] for row in group_scored]),
                "average_reasoning_score": average([row["reasoning_score"] for row in group_scored]),
                "average_error_identification_score": average([row["error_identification_score"] for row in group_scored]),
                "average_post_agent_supervision_score": average([row["post_agent_supervision_score"] for row in group_scored]),
            })
        return {
            "version": version,
            "sample_count": len(scored_rows),
            "completed_count": len(completed_rows),
            "normal_completed_count": len(scored_rows),
            "average_total_score": average([row["total_score"] for row in scored_rows]),
            "average_deliverability_score": average([row["deliverability_score"] for row in scored_rows]),
            "average_reasoning_score": average([row["reasoning_score"] for row in scored_rows]),
            "average_error_identification_score": average([row["error_identification_score"] for row in scored_rows]),
            "average_post_agent_supervision_score": average([row["post_agent_supervision_score"] for row in scored_rows]),
            "groups": group_rows,
            "samples": [
                {
                    "version": version,
                    **row,
                }
                for row in scored_rows
            ],
        }

    @app.get("/api/questionnaire-settings")
    def public_questionnaire_settings() -> dict[str, Any]:
        return questionnaire_settings.as_payload()

    def read_task_for_session(session_id: str, task_id: int, lang: str, db: Database, version: str) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session, db):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if task_id != session["current_task"] or task_id < 1 or task_id > 6:
            raise HTTPException(status_code=409, detail="This task is not available")
        db.mark_task_started(session_id, task_id)
        task = localized_task(task_id, lang, version)
        if session["group_name"] != "B" or (version != "agent" and task_id not in (1, 2)):
            task["supervision_card"] = None
        return task

    def submit_task_for_session(session_id: str, task_id: int, payload: TaskPayload, db: Database, version: str) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session, db):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if task_id != session["current_task"] or task_id < 1 or task_id > 6:
            raise HTTPException(status_code=409, detail="This task is not available")
        required = set(task_question_ids(task_id, version))
        if set(payload.answers) != required:
            raise HTTPException(status_code=400, detail="All task questions must be answered")
        try:
            return db.save_task_response(session_id, task_id, payload.answers, payload.supervision_answers)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    def read_posttest_for_session(session_id: str, lang: str, db: Database) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session, db):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if session["current_task"] <= 6:
            raise HTTPException(status_code=409, detail="Posttest is not available")
        if session["posttest_submitted_at"]:
            raise HTTPException(status_code=409, detail="Posttest already submitted")
        return posttest_schema(lang)

    def submit_posttest_for_session(session_id: str, payload: PosttestPayload, db: Database) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
        if ensure_not_timed_out(session, db):
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
        version = request_version(request)
        require_enabled_version(version)
        db = dbs[version]
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=401, detail="No active session")
        session_dict = dict(session)
        test_mode = is_test_session(session_dict)
        if payload.test_group is not None and payload.test_group not in ("A", "B"):
            raise HTTPException(status_code=400, detail="Test group must be A or B")
        if payload.test_group is not None and not test_mode:
            raise HTTPException(status_code=400, detail="Group choice is only available for test questionnaire")
        if test_mode and payload.test_group is None:
            raise HTTPException(status_code=400, detail="Test group must be A or B")
        if not has_submitted_pretest(session_dict):
            raise HTTPException(status_code=409, detail="Pretest is required before research notice agreement")
        try:
            created = db.start_session(session_id, payload.agreement, payload.test_group)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        refreshed = dict(db.get_session(session_id))
        set_session_cookie(response, created["session_id"], version)
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
        version = normalize_version_or_400(pretest.get("questionnaire_version"))
        require_enabled_version(version)
        pretest["questionnaire_version"] = version
        for field in PRETEST_IDENTITY_FIELDS:
            pretest[field] = pretest[field].strip()
        is_test = is_test_pretest(pretest)
        db = dbs[version]
        if version != "python":
            pretest.pop("numpy_familiarity", None)
        missing = [field for field in pretest_fields_for_version(version) if pretest.get(field) in ("", None)]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")
        if pretest["consent"] != "I agree":
            raise HTTPException(status_code=400, detail="Consent is required")
        if not session_id:
            saved = db.create_session(pretest, is_test)
            set_session_cookie(response, saved["session_id"], version)
            return {
                "participant_id": saved["participant_id"],
                "is_test": is_test,
                "next_task": saved["next_task"],
                "next_stage": saved["next_stage"],
            }
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            saved = db.create_session(pretest, is_test)
            set_session_cookie(response, saved["session_id"], version)
            return {
                "participant_id": saved["participant_id"],
                "is_test": is_test,
                "next_task": saved["next_task"],
                "next_stage": saved["next_stage"],
            }
        if ensure_not_timed_out(session, db):
            raise HTTPException(status_code=410, detail="Session timed out. Please restart the questionnaire.")
        if session["current_task"] != 0:
            saved = db.create_session(pretest, is_test)
            set_session_cookie(response, saved["session_id"], version)
            return {
                "participant_id": saved["participant_id"],
                "is_test": is_test,
                "next_task": saved["next_task"],
                "next_stage": saved["next_stage"],
            }
        try:
            saved = db.save_pretest(session_id, pretest, is_test)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {
            "participant_id": saved["participant_id"],
            "is_test": is_test,
            "next_task": saved["next_task"],
            "next_stage": saved["next_stage"],
        }

    @app.get("/api/session/current")
    def current_session(request: Request) -> dict[str, Any]:
        session_id = cookie_session_id(request)
        if not session_id:
            return {"status": "none"}
        version = request_version(request)
        if not questionnaire_settings.is_enabled(version):
            return {"status": "closed", "next_stage": None, "next_task": None}
        db = request_db(request)
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            return {"status": "none"}
        return summarize_session(session_id, db)

    @app.post("/api/session/reset")
    def reset_session(request: Request, response: Response) -> dict[str, Any]:
        session_id = cookie_session_id(request)
        if session_id:
            db = request_db(request)
            db.abandon_incomplete_session(session_id)
        clear_session_cookie(response)
        return {"status": "none"}

    @app.get("/api/task/{task_id}")
    def read_current_task(request: Request, task_id: int, lang: str = "en") -> dict[str, Any]:
        session_id, db, version = require_cookie_session(request)
        return read_task_for_session(session_id, task_id, lang, db, version)

    @app.post("/api/task/{task_id}")
    def submit_current_task(request: Request, task_id: int, payload: TaskPayload) -> dict[str, Any]:
        session_id, db, version = require_cookie_session(request)
        return submit_task_for_session(session_id, task_id, payload, db, version)

    @app.get("/api/task/{session_id}/{task_id}")
    def read_task(session_id: str, task_id: int, lang: str = "en", version: str = "python") -> dict[str, Any]:
        normalized = normalize_version_or_400(version)
        require_enabled_version(normalized)
        return read_task_for_session(session_id, task_id, lang, dbs[normalized], normalized)

    @app.post("/api/task/{session_id}/{task_id}")
    def submit_task(session_id: str, task_id: int, payload: TaskPayload, version: str = "python") -> dict[str, Any]:
        normalized = normalize_version_or_400(version)
        require_enabled_version(normalized)
        return submit_task_for_session(session_id, task_id, payload, dbs[normalized], normalized)

    @app.get("/api/posttest")
    def read_current_posttest(request: Request, lang: str = "en") -> dict[str, Any]:
        session_id, db, _version = require_cookie_session(request)
        return read_posttest_for_session(session_id, lang, db)

    @app.post("/api/posttest")
    def submit_current_posttest(request: Request, payload: PosttestPayload) -> dict[str, Any]:
        session_id, db, _version = require_cookie_session(request)
        return submit_posttest_for_session(session_id, payload, db)

    @app.get("/api/posttest/{session_id}")
    def read_posttest(session_id: str, lang: str = "en", version: str = "python") -> dict[str, Any]:
        normalized = normalize_version_or_400(version)
        require_enabled_version(normalized)
        return read_posttest_for_session(session_id, lang, dbs[normalized])

    @app.post("/api/posttest/{session_id}")
    def submit_posttest(session_id: str, payload: PosttestPayload, version: str = "python") -> dict[str, Any]:
        normalized = normalize_version_or_400(version)
        require_enabled_version(normalized)
        return submit_posttest_for_session(session_id, payload, dbs[normalized])

    @app.get("/api/session/{session_id}/summary")
    def session_summary(session_id: str, version: str = "python") -> dict[str, Any]:
        normalized = normalize_version_or_400(version)
        require_enabled_version(normalized)
        result = summarize_session(session_id, dbs[normalized])
        if result["status"] == "none":
            raise HTTPException(status_code=404, detail="Session not found")
        return result

    def require_admin(password: str) -> None:
        if password != password_value:
            raise HTTPException(status_code=401, detail="Invalid password")

    @app.get("/api/admin/questionnaire-settings")
    def admin_questionnaire_settings(password: str) -> dict[str, Any]:
        require_admin(password)
        return questionnaire_settings.as_payload()

    @app.put("/api/admin/questionnaire-settings")
    def admin_update_questionnaire_settings(password: str, body: dict[str, Any]) -> dict[str, Any]:
        require_admin(password)
        enabled_versions = body.get("enabled_versions")
        if not isinstance(enabled_versions, dict):
            raise HTTPException(status_code=400, detail="enabled_versions must be an object")
        questionnaire_settings.write(enabled_versions)
        return questionnaire_settings.as_payload()

    @app.get("/api/admin/export")
    def export(password: str, version: str = "python") -> Response:
        require_admin(password)
        db = db_for_version(version)
        normalized = normalize_questionnaire_version(version)
        normal_completed_rows = [
            row
            for row in db.all_rows()
            if not is_test_session(dict(row["session"]))
            and completion_metadata(dict(row["session"]), quality_flags_for_row(row))["completion_bucket"]
            == "normal_completed"
        ]
        content = build_export_workbook(normal_completed_rows, normalized)
        return Response(
            content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="questionnaire_{normalized}_normal_completed_export.xlsx"'},
        )

    @app.get("/api/admin/sessions")
    def admin_list(password: str, include_abandoned: bool = False, version: str = "python") -> list[dict[str, Any]]:
        require_admin(password)
        normalized = normalize_version_or_400(version)
        db = dbs[normalized]
        sessions = db.admin_list_sessions(include_abandoned)
        result = []
        for s in sessions:
            row = db.admin_get_session(s["id"])
            if row and not s["completed_at"] and not s["abandoned_at"] and not s["timeout_at"]:
                ensure_not_timed_out(s, db)
                row = db.admin_get_session(s["id"])
                s = row["session"]
            pretest = decode_json(s["pretest_json"])
            answers: dict[str, str] = {}
            for r in row["responses"]:
                answers.update(decode_json(r["answers_json"]))
            scores = score_answers(answers)
            posttest_scores = score_posttest(decode_json(s["posttest_json"]))
            flags = quality_flags_for_row(row)
            completion = completion_metadata(s, flags)
            automatic_completion = automatic_completion_metadata(s, flags)
            test_mode = is_test_session(s)
            result.append({
                "session_id": s["id"],
                "participant_id": s["participant_id"],
                "questionnaire_version": normalized,
                "is_test": test_mode,
                "class_name": pretest.get("class_name"),
                "student_name": pretest.get("student_name"),
                "student_id": pretest.get("student_id"),
                "group": s["group_name"],
                "status": "abandoned" if s["abandoned_at"] else "timeout" if s["timeout_at"] else "complete" if s["completed_at"] else "in_progress",
                "current_task": s["current_task"],
                "created_at": s["created_at"],
                "completed_at": s["completed_at"],
                "abandoned_at": s["abandoned_at"],
                "total_score": scores["total_score"],
                "post_agent_supervision_score": posttest_scores["post_agent_supervision_score"],
                "valid": completion["completion_bucket"] == "normal_completed" and not test_mode,
                "sample_included": completion["completion_bucket"] == "normal_completed" and not test_mode,
                "automatic_valid": automatic_completion["completion_bucket"] == "normal_completed",
                "quality_flags": flags,
                "completion_override": s["completion_override"],
                "completion_override_note": s["completion_override_note"],
                "completion_override_updated_at": s["completion_override_updated_at"],
                "automatic_completion_bucket": automatic_completion["completion_bucket"],
                "automatic_incomplete_reason": automatic_completion["incomplete_reason"],
                "total_duration_hms": seconds_to_hms(elapsed_seconds_for_session(s)),
                **completion,
            })
        return result

    @app.get("/api/admin/stats")
    def admin_stats(password: str) -> dict[str, Any]:
        require_admin(password)
        version_labels = {
            "python": "Python 版本",
            "c": "C 语言版本",
            "agent": "Agent 监督版本",
        }
        version_summaries = []
        group_summaries = []
        sample_rows = []
        for version, db in dbs.items():
            summary = stats_summary_for_version(version, db)
            summary["label"] = version_labels[version]
            version_summaries.append({key: value for key, value in summary.items() if key not in ("groups", "samples")})
            group_summaries.extend(
                {**group, "label": version_labels[version]}
                for group in summary["groups"]
            )
            sample_rows.extend(
                {**sample, "label": version_labels[version]}
                for sample in summary["samples"]
            )
        return {
            "score_max": 30,
            "posttest_score_max": 5,
            "sample_scope": "normal_completed",
            "versions": version_summaries,
            "groups": group_summaries,
            "samples": sample_rows,
        }

    @app.get("/api/admin/sessions/{session_id}")
    def admin_get(session_id: str, password: str, version: str = "python") -> dict[str, Any]:
        require_admin(password)
        from .database import decode_json
        normalized = normalize_version_or_400(version)
        db = dbs[normalized]
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
        posttest_scores = score_posttest(posttest)
        session = dict(s)
        session["is_test"] = is_test_session(session)
        session["total_duration_hms"] = seconds_to_hms(elapsed_seconds_for_session(session))
        flags = quality_flags_for_row(row)
        automatic_completion = automatic_completion_metadata(session, flags)
        completion = completion_metadata(session, flags)
        return {
            "session": session,
            "questionnaire_version": normalized,
            "pretest": pretest,
            "posttest": posttest,
            "answers": answers,
            "supervision": supervision,
            "scores": {k: v for k, v in scores.items() if k != "per_question"},
            "supervision_scores": {k: v for k, v in sup_scores.items() if k != "per_item"},
            "posttest_scores": posttest_scores,
            "quality_flags": flags,
            "automatic_completion": automatic_completion,
            "completion": completion,
            "responses": row["responses"],
        }

    @app.delete("/api/admin/sessions/{session_id}")
    def admin_delete(session_id: str, password: str, version: str = "python") -> dict[str, Any]:
        require_admin(password)
        if not db_for_version(version).admin_delete_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found or already abandoned")
        return {"ok": True}

    @app.post("/api/admin/sessions/bulk-delete")
    def admin_bulk_delete(password: str, body: dict[str, Any], version: str = "python") -> dict[str, Any]:
        require_admin(password)
        db = db_for_version(version)
        session_ids = body.get("session_ids")
        if not isinstance(session_ids, list) or not all(isinstance(item, str) for item in session_ids):
            raise HTTPException(status_code=400, detail="session_ids must be a list of session ids")
        deleted = 0
        for session_id in session_ids:
            if db.admin_delete_session(session_id):
                deleted += 1
        return {"ok": True, "deleted": deleted}

    @app.patch("/api/admin/sessions/{session_id}")
    def admin_update(session_id: str, password: str, body: dict[str, Any], version: str = "python") -> dict[str, Any]:
        require_admin(password)
        try:
            updated = db_for_version(version).admin_update_session(session_id, body)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not updated:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        return {"ok": True}

    @app.post("/api/admin/sessions/{session_id}/restore")
    def admin_restore(session_id: str, password: str, version: str = "python") -> dict[str, Any]:
        require_admin(password)
        if not db_for_version(version).admin_restore_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        return {"ok": True}

    password_value = password
    app.mount("/", StaticFiles(directory=base_dir / "static", html=True), name="static")
    return app


app = create_app()
