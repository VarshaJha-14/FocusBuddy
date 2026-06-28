"""
routes/feedback.py — Handles step feedback actions (Done, Too Hard, Back, Quit).

POST /feedback/{session_id} — Processes action and returns HTMX partials.

Actions:
  - done: Advance step, return next step card or reward screen
  - too_hard: Downscale step via LLM, return micro-mode step card
  - back_to_main: Exit micro mode, return original step card
  - quit: Return redirect to landing
"""

import logging

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ai.downscale import downscale_step
from db.session import get_session, advance_step, log_feedback
from auth.dependencies import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/feedback/{session_id}", response_class=HTMLResponse)
async def handle_feedback(
    request: Request,
    session_id: str,
    action: str = Form(...),
    user_id: str = Depends(get_current_user_id),
):
    session = await get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Ownership check — only enforce when both sides have a user_id
    if user_id and session.user_id and session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your session")

    if action == "done":
        return await _handle_done(request, session_id, session)
    elif action == "too_hard":
        return await _handle_too_hard(request, session_id, session)
    elif action == "back_to_main":
        return await _handle_back_to_main(request, session_id, session)
    elif action == "quit":
        return await _handle_quit(request)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")


async def _handle_done(request: Request, session_id: str, session):
    current_step_text = session.steps[session.current_index]
    step_index = session.current_index

    await log_feedback(session_id, step_index, current_step_text, "done")
    updated_session = await advance_step(session_id)
    if updated_session is None:
        raise HTTPException(status_code=500, detail="Failed to advance step")

    total_steps = len(updated_session.steps)
    new_index = updated_session.current_index

    if new_index >= total_steps:
        logger.info(f"Session {session_id} completed! All {total_steps} steps done.")
        return templates.TemplateResponse(
            request,
            "reward.html",
            {
                "session_id": session_id,
                "task": updated_session.task,
                "steps": updated_session.steps,
                "total_steps": total_steps,
                "htmx_request": True,
            },
        )

    current_step = updated_session.steps[new_index]
    progress_pct = (new_index / total_steps) * 100

    return templates.TemplateResponse(
        request,
        "partials/step_card.html",
        {
            "session_id": session_id,
            "current_index": new_index,
            "total_steps": total_steps,
            "current_step": current_step,
            "progress_pct": progress_pct,
            "micro_mode": False,
            "micro_steps": [],
            "encouragement": "",
            "task": updated_session.task,
        },
    )


async def _handle_too_hard(request: Request, session_id: str, session):
    current_step_text = session.steps[session.current_index]
    step_index = session.current_index

    await log_feedback(session_id, step_index, current_step_text, "too_hard")
    downscale_response = await downscale_step(
        step_text=current_step_text,
        cognitive_state=session.cognitive_state,
    )

    total_steps = len(session.steps)
    progress_pct = (session.current_index / total_steps) * 100

    return templates.TemplateResponse(
        request,
        "partials/step_card.html",
        {
            "session_id": session_id,
            "current_index": session.current_index,
            "total_steps": total_steps,
            "current_step": downscale_response.micro_steps[0] if downscale_response.micro_steps else current_step_text,
            "progress_pct": progress_pct,
            "micro_mode": True,
            "micro_steps": downscale_response.micro_steps,
            "encouragement": downscale_response.encouragement,
            "task": session.task,
        },
    )


async def _handle_back_to_main(request: Request, session_id: str, session):
    total_steps = len(session.steps)
    current_step = session.steps[session.current_index]
    progress_pct = (session.current_index / total_steps) * 100

    return templates.TemplateResponse(
        request,
        "partials/step_card.html",
        {
            "session_id": session_id,
            "current_index": session.current_index,
            "total_steps": total_steps,
            "current_step": current_step,
            "progress_pct": progress_pct,
            "micro_mode": False,
            "micro_steps": [],
            "encouragement": "",
            "task": session.task,
        },
    )


async def _handle_quit(request: Request):
    return HTMLResponse(
        content='<div hx-trigger="load" hx-get="/" hx-target="body" hx-push-url="true"></div>',
        headers={"HX-Redirect": "/"},
    )