"""
routes/ingest.py — Landing page and vent ingestion.

GET  /          → Outer shell (loads Clerk, handles auth redirect)
GET  /landing   → Public landing page partial
GET  /workspace → Protected workspace partial (vent form + completed tasks)
POST /vent      → Protected: process vent, create session, return step shell
"""

import uuid
import logging

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ai.safety import scrub_pii, check_crisis
from ai.prompt import build_prompt
from ai.engine import generate_steps
from db.models import SessionData
from db.session import create_session, get_completed_sessions
from auth.dependencies import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Outer shell page — loads Clerk JS and lets the frontend decide
    whether to show /landing or /workspace based on auth state.
    """
    from main import CLERK_PUBLISHABLE_KEY
    return templates.TemplateResponse(
        request,
        "ingest.html",
        {"clerk_publishable_key": CLERK_PUBLISHABLE_KEY or ""},
    )


@router.get("/landing", response_class=HTMLResponse)
async def landing_partial(request: Request):
    """Public landing page partial — hero text and Get Started button."""
    return templates.TemplateResponse(request, "partials/landing.html")


@router.get("/workspace", response_class=HTMLResponse)
async def workspace_partial(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """
    Protected workspace partial.
    Returns the vent form + completed tasks history for the authenticated user.
    """
    completed = await get_completed_sessions(user_id) if user_id else []
    return templates.TemplateResponse(
        request,
        "partials/workspace.html",
        {"completed_sessions": completed},
    )


@router.post("/vent", response_class=HTMLResponse)
async def process_vent(
    request: Request,
    vent_text: str = Form(...),
    cognitive_state: str = Form(default=""),
    custom_mood: str = Form(default=""),
    user_id: str = Depends(get_current_user_id),
):
    """
    Process the user's vent text:
    1. Server-side PII scrub
    2. Crisis keyword check → return modal if detected
    3. Build LLM prompt
    4. Async LLM call with fallback
    5. Validate response
    6. Persist session with user_id
    7. Return step.html shell
    """
    # Clean up cognitive state
    custom_mood = custom_mood.strip() if custom_mood else ""
    cognitive_state = custom_mood if custom_mood else (cognitive_state.strip() if cognitive_state else None)

    # Step 1: PII scrub
    scrubbed_text = scrub_pii(vent_text)
    logger.info(f"Processing vent (length={len(scrubbed_text)}, state={cognitive_state}, user={user_id})")

    # Step 2: Crisis check
    if check_crisis(scrubbed_text):
        logger.warning("Crisis keywords detected — returning crisis modal")
        return templates.TemplateResponse(
            request,
            "partials/crisis_modal.html",
            {"show_full_page": True},
        )

    # Step 3: Build prompt
    messages = build_prompt(scrubbed_text, cognitive_state)

    # Step 4: LLM call
    llm_response = await generate_steps(messages)

    # Step 5: Already validated by Pydantic in engine.py

    # Step 6: Create session with user_id
    session_id = str(uuid.uuid4())
    session = SessionData(
        id=session_id,
        task=llm_response.task,
        steps=llm_response.steps,
        current_index=0,
        cognitive_state=cognitive_state,
        tone=llm_response.tone,
        user_id=user_id,
    )
    await create_session(session)
    logger.info(f"Session created: {session_id} with {len(llm_response.steps)} steps, user={user_id}")

    # Step 7: Return step shell
    total_steps = len(session.steps)
    current_step = session.steps[0]
    progress_pct = (0 / total_steps) * 100

    return templates.TemplateResponse(
        request,
        "step.html",
        {
            "session_id": session_id,
            "task": session.task,
            "steps": session.steps,
            "current_index": 0,
            "total_steps": total_steps,
            "current_step": current_step,
            "progress_pct": progress_pct,
            "micro_mode": False,
            "micro_steps": [],
            "encouragement": "",
        },
    )