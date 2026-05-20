from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .database import Database, decode_json
from .export import build_export_workbook
from .questionnaire import POSTTEST_FIELDS, PRETEST_FIELDS, localized_task, posttest_schema, task_question_ids
from .scoring import score_answers, score_supervision

SESSION_COOKIE_NAME = "questionnaire_session"
SESSION_COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 7


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
        return session_id

    def summarize_session(session_id: str) -> dict[str, Any]:
        rows = [row for row in db.all_rows() if row["session"]["id"] == session_id]
        if not rows:
            return {"status": "none"}
        row = rows[0]
        answers: dict[str, str] = {}
        supervision: dict[str, str] = {}
        for task_response in row["responses"]:
            answers.update(decode_json(task_response["answers_json"]))
            supervision.update(decode_json(task_response["supervision_json"]))
        formal = score_answers(answers)
        supervision_scores = score_supervision(supervision)
        posttest_ready = row["session"]["current_task"] > 6 and not row["session"]["posttest_submitted_at"]
        complete = bool(row["session"]["completed_at"])
        return {
            "status": "complete" if complete else "posttest" if posttest_ready else "in_progress",
            "participant_id": row["session"]["participant_id"],
            "next_task": None if row["session"]["current_task"] > 6 else row["session"]["current_task"],
            "next_stage": None if complete else "posttest" if posttest_ready else "task",
            "scores": {key: value for key, value in formal.items() if key != "per_question"},
            "supervision_scores": {key: value for key, value in supervision_scores.items() if key != "per_item"},
        }

    def read_task_for_session(session_id: str, task_id: int, lang: str) -> dict[str, Any]:
        session = db.get_session(session_id)
        if not session or session["abandoned_at"]:
            raise HTTPException(status_code=404, detail="Session not found")
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
        if session["current_task"] <= 6:
            raise HTTPException(status_code=409, detail="Posttest is not available")
        if session["posttest_submitted_at"]:
            raise HTTPException(status_code=409, detail="Posttest already submitted")
        return posttest_schema(lang)

    def submit_posttest_for_session(session_id: str, payload: PosttestPayload) -> dict[str, Any]:
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

    @app.post("/api/pretest")
    def submit_pretest(payload: PretestPayload, response: Response) -> dict[str, Any]:
        pretest = payload.model_dump()
        missing = [field for field in PRETEST_FIELDS if pretest.get(field) in ("", None)]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")
        if pretest["consent"] != "I agree":
            raise HTTPException(status_code=400, detail="Consent is required")
        created = db.create_session(pretest)
        set_session_cookie(response, created["session_id"])
        return {
            "participant_id": created["participant_id"],
            "next_task": created["next_task"],
            "next_stage": "task",
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

    @app.get("/api/admin/export")
    def export(password: str) -> Response:
        if password != password_value:
            raise HTTPException(status_code=401, detail="Invalid password")
        content = build_export_workbook(db.all_rows())
        return Response(
            content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": 'attachment; filename="questionnaire_export.xlsx"'},
        )

    password_value = password
    app.mount("/", StaticFiles(directory=base_dir / "static", html=True), name="static")
    return app


app = create_app()
