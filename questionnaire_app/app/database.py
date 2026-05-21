from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Database:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    participant_id INTEGER UNIQUE,
                    group_name TEXT NOT NULL,
                    current_task INTEGER NOT NULL,
                    pretest_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    pretest_submitted_at TEXT NOT NULL,
                    posttest_json TEXT,
                    posttest_submitted_at TEXT,
                    completed_at TEXT,
                    abandoned_at TEXT,
                    timeout_at TEXT
                );

                CREATE TABLE IF NOT EXISTS task_starts (
                    session_id TEXT NOT NULL,
                    task_id INTEGER NOT NULL,
                    started_at TEXT NOT NULL,
                    PRIMARY KEY (session_id, task_id)
                );

                CREATE TABLE IF NOT EXISTS task_responses (
                    session_id TEXT NOT NULL,
                    task_id INTEGER NOT NULL,
                    answers_json TEXT NOT NULL,
                    supervision_json TEXT NOT NULL,
                    submitted_at TEXT NOT NULL,
                    PRIMARY KEY (session_id, task_id)
                );
                """
            )
            columns = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(sessions)").fetchall()
            }
            if "participant_id" not in columns:
                conn.execute("ALTER TABLE sessions ADD COLUMN participant_id INTEGER")
                conn.execute("UPDATE sessions SET participant_id = rowid WHERE participant_id IS NULL")
            if "posttest_json" not in columns:
                conn.execute("ALTER TABLE sessions ADD COLUMN posttest_json TEXT")
            if "posttest_submitted_at" not in columns:
                conn.execute("ALTER TABLE sessions ADD COLUMN posttest_submitted_at TEXT")
            if "abandoned_at" not in columns:
                conn.execute("ALTER TABLE sessions ADD COLUMN abandoned_at TEXT")
            if "timeout_at" not in columns:
                conn.execute("ALTER TABLE sessions ADD COLUMN timeout_at TEXT")

    def choose_group(self) -> str:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT group_name, COUNT(*) AS c FROM sessions WHERE abandoned_at IS NULL GROUP BY group_name"
            ).fetchall()
        counts = {"A": 0, "B": 0}
        for row in rows:
            counts[row["group_name"]] = row["c"]
        return "A" if counts["A"] <= counts["B"] else "B"

    def create_session(self, pretest: dict[str, Any]) -> dict[str, Any]:
        session_id = uuid.uuid4().hex
        group = self.choose_group()
        now = utc_now()
        with self.connect() as conn:
            participant_id = (
                conn.execute("SELECT COALESCE(MAX(participant_id), 0) + 1 AS next_id FROM sessions").fetchone()[
                    "next_id"
                ]
            )
            conn.execute(
                """
                INSERT INTO sessions
                (id, participant_id, group_name, current_task, pretest_json, created_at, pretest_submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (session_id, participant_id, group, 1, json.dumps(pretest, ensure_ascii=False), now, now),
            )
        return {"session_id": session_id, "participant_id": participant_id, "group": group, "next_task": 1}

    def start_session(self, agreement: str) -> dict[str, Any]:
        session_id = uuid.uuid4().hex
        group = self.choose_group()
        now = utc_now()
        pretest = {"research_notice_agreement": agreement}
        with self.connect() as conn:
            participant_id = (
                conn.execute("SELECT COALESCE(MAX(participant_id), 0) + 1 AS next_id FROM sessions").fetchone()[
                    "next_id"
                ]
            )
            conn.execute(
                """
                INSERT INTO sessions
                (id, participant_id, group_name, current_task, pretest_json, created_at, pretest_submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (session_id, participant_id, group, 0, json.dumps(pretest, ensure_ascii=False), now, now),
            )
        return {"session_id": session_id, "participant_id": participant_id, "group": group}

    def get_session(self, session_id: str) -> sqlite3.Row | None:
        with self.connect() as conn:
            return conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()

    def abandon_incomplete_session(self, session_id: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE sessions SET abandoned_at = ? WHERE id = ? AND completed_at IS NULL",
                (utc_now(), session_id),
            )

    def mark_timeout(self, session_id: str, timeout_at: str) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE sessions
                SET timeout_at = ?
                WHERE id = ? AND completed_at IS NULL AND abandoned_at IS NULL AND timeout_at IS NULL
                """,
                (timeout_at, session_id),
            )

    def save_pretest(self, session_id: str, pretest: dict[str, Any]) -> dict[str, Any]:
        submitted_at = utc_now()
        with self.connect() as conn:
            session = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if not session:
                raise LookupError("Session not found")
            if session["current_task"] != 0:
                raise ValueError("Pretest already submitted")
            if session["abandoned_at"] or session["timeout_at"]:
                raise ValueError("Session is not active")
            conn.execute(
                """
                UPDATE sessions
                SET pretest_json = ?, pretest_submitted_at = ?, current_task = 1
                WHERE id = ?
                """,
                (json.dumps(pretest, ensure_ascii=False), submitted_at, session_id),
            )
        return {"next_task": 1, "next_stage": "task"}

    def mark_task_started(self, session_id: str, task_id: int) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO task_starts (session_id, task_id, started_at) VALUES (?, ?, ?)",
                (session_id, task_id, utc_now()),
            )

    def save_task_response(
        self,
        session_id: str,
        task_id: int,
        answers: dict[str, str],
        supervision_answers: dict[str, str],
    ) -> dict[str, Any]:
        submitted_at = utc_now()
        next_task = task_id + 1
        with self.connect() as conn:
            existing = conn.execute(
                "SELECT 1 FROM task_responses WHERE session_id = ? AND task_id = ?",
                (session_id, task_id),
            ).fetchone()
            if existing:
                raise ValueError("Task already submitted")
            conn.execute(
                """
                INSERT INTO task_responses
                (session_id, task_id, answers_json, supervision_json, submitted_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    task_id,
                    json.dumps(answers, ensure_ascii=False),
                    json.dumps(supervision_answers, ensure_ascii=False),
                    submitted_at,
                ),
            )
            conn.execute(
                "UPDATE sessions SET current_task = ? WHERE id = ?",
                (next_task, session_id),
            )
        return {"next_task": next_task, "posttest_required": next_task > 6, "complete": False}

    def save_posttest(self, session_id: str, posttest: dict[str, Any]) -> dict[str, Any]:
        submitted_at = utc_now()
        with self.connect() as conn:
            session = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if not session:
                raise LookupError("Session not found")
            if session["current_task"] <= 6:
                raise ValueError("Posttest is not available")
            if session["posttest_submitted_at"]:
                raise ValueError("Posttest already submitted")
            conn.execute(
                """
                UPDATE sessions
                SET posttest_json = ?, posttest_submitted_at = ?, completed_at = ?
                WHERE id = ?
                """,
                (json.dumps(posttest, ensure_ascii=False), submitted_at, submitted_at, session_id),
            )
        return {"complete": True}

    def admin_list_sessions(self, include_abandoned: bool = False) -> list[dict[str, Any]]:
        where = "" if include_abandoned else "WHERE abandoned_at IS NULL"
        with self.connect() as conn:
            rows = conn.execute(f"SELECT * FROM sessions {where} ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]

    def admin_get_session(self, session_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            session = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if not session:
                return None
            starts = conn.execute("SELECT * FROM task_starts WHERE session_id = ?", (session_id,)).fetchall()
            responses = conn.execute(
                "SELECT * FROM task_responses WHERE session_id = ? ORDER BY task_id", (session_id,)
            ).fetchall()
        return {
            "session": dict(session),
            "starts": {row["task_id"]: dict(row) for row in starts},
            "responses": [dict(r) for r in responses],
        }

    def admin_delete_session(self, session_id: str) -> bool:
        with self.connect() as conn:
            result = conn.execute(
                "UPDATE sessions SET abandoned_at = ? WHERE id = ? AND abandoned_at IS NULL",
                (utc_now(), session_id),
            )
        return result.rowcount > 0

    def admin_update_session(self, session_id: str, updates: dict[str, Any]) -> bool:
        allowed = {"group_name", "current_task"}
        fields = {k: v for k, v in updates.items() if k in allowed}
        if not fields:
            return False
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        with self.connect() as conn:
            result = conn.execute(
                f"UPDATE sessions SET {set_clause} WHERE id = ?",
                (*fields.values(), session_id),
            )
        return result.rowcount > 0

    def admin_restore_session(self, session_id: str) -> bool:
        with self.connect() as conn:
            result = conn.execute(
                "UPDATE sessions SET abandoned_at = NULL WHERE id = ?", (session_id,)
            )
        return result.rowcount > 0

    def all_rows(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            sessions = conn.execute(
                "SELECT * FROM sessions WHERE abandoned_at IS NULL ORDER BY created_at"
            ).fetchall()
            starts = conn.execute("SELECT * FROM task_starts").fetchall()
            responses = conn.execute("SELECT * FROM task_responses ORDER BY task_id").fetchall()
        starts_by_session = {(row["session_id"], row["task_id"]): row for row in starts}
        responses_by_session: dict[str, list[sqlite3.Row]] = {}
        for row in responses:
            responses_by_session.setdefault(row["session_id"], []).append(row)
        result = []
        for session in sessions:
            result.append(
                {
                    "session": session,
                    "starts": {task_id: starts_by_session.get((session["id"], task_id)) for task_id in range(1, 7)},
                    "responses": responses_by_session.get(session["id"], []),
                }
            )
        return result


def decode_json(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    return json.loads(value)


def seconds_between(start: str | None, end: str | None) -> int | None:
    if not start or not end:
        return None
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    return max(0, int((end_dt - start_dt).total_seconds()))


def seconds_to_hms(seconds: int | None) -> str | None:
    if seconds is None:
        return None
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
