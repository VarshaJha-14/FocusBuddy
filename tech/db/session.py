"""
db/session.py — Async SQLite CRUD operations via aiosqlite.

All session state is persisted in SQLite only — no localStorage, no cookies.
"""

import json
import aiosqlite
import logging
from datetime import datetime
from typing import Optional

from tech.db.models import (
    CREATE_SESSIONS_TABLE,
    CREATE_FEEDBACK_TABLE,
    SessionData,
)

logger = logging.getLogger(__name__)

DATABASE_PATH = "focusbuddy.db"


async def init_db(db_path: str | None = None) -> None:
    """Create tables if they don't exist. Migrates user_id column if missing."""
    path = db_path or DATABASE_PATH
    async with aiosqlite.connect(path) as db:
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute(CREATE_SESSIONS_TABLE)
        await db.execute(CREATE_FEEDBACK_TABLE)

        # Migration: add user_id column if it doesn't exist yet
        async with db.execute("PRAGMA table_info(sessions)") as cursor:
            columns = [row[1] async for row in cursor]
        if "user_id" not in columns:
            await db.execute("ALTER TABLE sessions ADD COLUMN user_id TEXT")
            logger.info("Migrated sessions table: added user_id column")

        await db.commit()
    logger.info(f"Database initialized at {path}")


def _get_db_path() -> str:
    return DATABASE_PATH


async def create_session(session: SessionData) -> None:
    """Insert a new session into the database."""
    async with aiosqlite.connect(_get_db_path()) as db:
        await db.execute(
            """INSERT INTO sessions (id, task, steps, current_index, cognitive_state, tone, user_id, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session.id,
                session.task,
                json.dumps(session.steps),
                session.current_index,
                session.cognitive_state,
                session.tone,
                session.user_id,
                datetime.utcnow().isoformat(),
            ),
        )
        await db.commit()
    logger.info(f"Created session {session.id} for task: {session.task}")


async def get_session(session_id: str) -> Optional[SessionData]:
    """Fetch a session by ID. Returns None if not found."""
    async with aiosqlite.connect(_get_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return SessionData(
                id=row["id"],
                task=row["task"],
                steps=json.loads(row["steps"]),
                current_index=row["current_index"],
                cognitive_state=row["cognitive_state"],
                tone=row["tone"],
                user_id=row["user_id"],
                created_at=row["created_at"],
                completed_at=row["completed_at"],
            )


async def get_completed_sessions(user_id: str) -> list[SessionData]:
    """Fetch all completed sessions for a user, sorted by completion date descending."""
    async with aiosqlite.connect(_get_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT * FROM sessions
               WHERE user_id = ? AND completed_at IS NOT NULL
               ORDER BY completed_at DESC""",
            (user_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [
                SessionData(
                    id=row["id"],
                    task=row["task"],
                    steps=json.loads(row["steps"]),
                    current_index=row["current_index"],
                    cognitive_state=row["cognitive_state"],
                    tone=row["tone"],
                    user_id=row["user_id"],
                    created_at=row["created_at"],
                    completed_at=row["completed_at"],
                )
                for row in rows
            ]


async def advance_step(session_id: str) -> Optional[SessionData]:
    """
    Increment current_index by 1. If all steps are done, set completed_at.
    Returns updated session data.
    """
    async with aiosqlite.connect(_get_db_path()) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None

        steps = json.loads(row["steps"])
        new_index = row["current_index"] + 1

        if new_index >= len(steps):
            await db.execute(
                "UPDATE sessions SET current_index = ?, completed_at = ? WHERE id = ?",
                (new_index, datetime.utcnow().isoformat(), session_id),
            )
        else:
            await db.execute(
                "UPDATE sessions SET current_index = ? WHERE id = ?",
                (new_index, session_id),
            )
        await db.commit()

    return await get_session(session_id)


async def log_feedback(
    session_id: str,
    step_index: int,
    step_text: str,
    action: str,
) -> None:
    """Log a feedback entry (done, too_hard, strategy_change)."""
    async with aiosqlite.connect(_get_db_path()) as db:
        await db.execute(
            """INSERT INTO feedback_log (session_id, step_index, step_text, action, timestamp)
               VALUES (?, ?, ?, ?, ?)""",
            (
                session_id,
                step_index,
                step_text,
                action,
                datetime.utcnow().isoformat(),
            ),
        )
        await db.commit()
    logger.debug(f"Logged feedback: session={session_id}, step={step_index}, action={action}")


async def delete_session(session_id: str) -> None:
    """Delete a session and its feedback logs."""
    async with aiosqlite.connect(_get_db_path()) as db:
        await db.execute("DELETE FROM feedback_log WHERE session_id = ?", (session_id,))
        await db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        await db.commit()
    logger.info(f"Deleted session {session_id}")