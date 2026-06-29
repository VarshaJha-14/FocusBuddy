"""
routes/steps.py — Step execution page and reward page.

GET /step/{session_id}          → Outer shell (safe for direct navigation)
GET /step-content/{session_id}  → Protected: inner step workspace partial
GET /reward/{session_id}        → Outer shell
GET /reward-content/{session_id} → Protected: reward partial with ownership check
"""

import logging

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from tech.db.session import get_session
from tech.auth.dependencies import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/step/{session_id}", response_class=HTMLResponse)
async def step_page(request: Request, session_id: str):
    """
    Outer shell for the step page — safe for direct navigation/refresh.
    Loads Clerk JS; HTMX then fetches /step-content/{session_id}.
    """
    return templates.TemplateResponse(
        request,
        "step.html",
        {"session_id": session_id},
    )


@router.get("/step-content/{session_id}", response_class=HTMLResponse)
async def step_content(
    request: Request,
    session_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Protected: verify ownership and return the inner step workspace partial."""
    session = await get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if user_id and session.user_id and session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your session")

    if session.current_index >= len(session.steps):
        return templates.TemplateResponse(
            request,
            "reward.html",
            {
                "session_id": session_id,
                "task": session.task,
                "steps": session.steps,
                "total_steps": len(session.steps),
            },
        )

    total_steps = len(session.steps)
    current_step = session.steps[session.current_index]
    progress_pct = (session.current_index / total_steps) * 100

    return templates.TemplateResponse(
        request,
        "partials/step_card.html",
        {
            "session_id": session_id,
            "task": session.task,
            "steps": session.steps,
            "current_index": session.current_index,
            "total_steps": total_steps,
            "current_step": current_step,
            "progress_pct": progress_pct,
            "micro_mode": False,
            "micro_steps": [],
            "encouragement": "",
        },
    )


@router.get("/reward/{session_id}", response_class=HTMLResponse)
async def reward_page(request: Request, session_id: str):
    """Outer shell for the reward page — safe for direct navigation."""
    return templates.TemplateResponse(
        request,
        "reward.html",
        {"session_id": session_id},
    )


@router.get("/reward-content/{session_id}", response_class=HTMLResponse)
async def reward_content(
    request: Request,
    session_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Protected: verify ownership and return the reward partial."""
    session = await get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if user_id and session.user_id and session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your session")

    return templates.TemplateResponse(
        request,
        "partials/reward_content.html",
        {
            "session_id": session_id,
            "task": session.task,
            "steps": session.steps,
            "total_steps": len(session.steps),
        },
    )