"""
db/models.py — Pydantic models for LLM response validation and SQL schema constants.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------- LLM Response Models ----------

class LLMResponse(BaseModel):
    """Validates the structured JSON response from the step-generation LLM call."""
    task: str = Field(..., min_length=1, max_length=200, description="Extracted core task name")
    tone: str = Field(..., description="Tone used: supportive_objective, permission_mode, or anchor_mode")
    steps: list[str] = Field(..., min_length=1, max_length=10, description="List of actionable step strings")


class DownscaleResponse(BaseModel):
    """Validates the structured JSON response from the downscale LLM call."""
    micro_steps: list[str] = Field(..., min_length=1, max_length=5, description="Broken-down micro-steps")
    encouragement: str = Field(default="You've got this. One tiny thing at a time.", description="Supportive message")


# ---------- Session Models ----------

class SessionData(BaseModel):
    """Represents a session record from the database."""
    id: str
    task: str
    steps: list[str]
    current_index: int = 0
    cognitive_state: Optional[str] = None
    tone: Optional[str] = None
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class FeedbackEntry(BaseModel):
    """Represents a feedback log entry."""
    id: Optional[int] = None
    session_id: str
    step_index: int
    step_text: str
    action: str  # done | too_hard | strategy_change
    timestamp: Optional[datetime] = None


# ---------- SQL Schema ----------

CREATE_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    task TEXT NOT NULL,
    steps TEXT NOT NULL,
    current_index INTEGER DEFAULT 0,
    cognitive_state TEXT,
    tone TEXT,
    user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
)
"""

CREATE_FEEDBACK_TABLE = """
CREATE TABLE IF NOT EXISTS feedback_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    step_text TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
)
"""
