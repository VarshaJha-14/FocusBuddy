"""
ai/downscale.py — Step downscaling via LLM.

When a user clicks "Too Hard / Stuck" on a step, this module
takes the exact failed step text and asks the LLM to break it
into 2-3 even smaller micro-steps.
"""

import asyncio
import json
import os
import logging
from typing import Optional

from groq import AsyncGroq

from db.models import DownscaleResponse

logger = logging.getLogger(__name__)

# ---------- Fallback Micro-Steps ----------
FALLBACK_DOWNSCALE = DownscaleResponse(
    micro_steps=[
        "Just walk over and sit down at your desk. Don't do anything else yet.",
        "Put your hands on the keyboard or pick up your pen. That's it.",
        "Take one breath and look at the thing you need to work on. Just look.",
    ],
    encouragement="Sometimes the smallest step is the bravest one. You're doing great.",
)

DOWNSCALE_SYSTEM_PROMPT = """You are FocusBuddy's micro-step assistant. The user found a step too difficult or overwhelming. Your job is to break that ONE step into 2-3 even tinier micro-steps.

RULES:
1. Each micro-step should be a single physical action that takes under 30 seconds.
2. The first micro-step should be absurdly easy — just moving, sitting, or looking.
3. Don't repeat the original step — break it into smaller pieces.
4. Be warm and non-judgmental. This is about making progress possible, not about failure.
5. DO NOT provide therapy or medical advice.

You MUST respond with valid JSON in exactly this format:
{
  "micro_steps": [
    "Micro-step 1 — absurdly tiny",
    "Micro-step 2 — still very small",
    "Micro-step 3 — slightly bigger but still tiny"
  ],
  "encouragement": "A brief, warm encouragement sentence."
}

Respond with ONLY the JSON object."""


def _get_client() -> Optional[AsyncGroq]:
    """Create an AsyncGroq client if API key is available."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return None
    return AsyncGroq(api_key=api_key)


async def downscale_step(
    step_text: str,
    cognitive_state: str | None = None,
) -> DownscaleResponse:
    """
    Break a difficult step into 2-3 micro-steps using the LLM.

    Args:
        step_text: The exact text of the step the user found too hard.
        cognitive_state: The user's current cognitive state (for tone matching).

    Returns:
        Validated DownscaleResponse with micro_steps and encouragement.
        Falls back to generic micro-steps on any failure.
    """
    client = _get_client()
    if client is None:
        logger.warning("No Groq API key configured — using fallback micro-steps.")
        return FALLBACK_DOWNSCALE

    user_message = f'The user found this step too hard: "{step_text}"'
    if cognitive_state:
        user_message += f"\nTheir current emotional state: {cognitive_state}"
    user_message += "\n\nBreak this into 2-3 micro-steps."

    try:
        completion = await asyncio.wait_for(
            client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": DOWNSCALE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=512,
                response_format={"type": "json_object"},
            ),
            timeout=5.0,
        )

        content = completion.choices[0].message.content
        if not content:
            logger.error("Empty response from Groq API (downscale)")
            return FALLBACK_DOWNSCALE

        response = DownscaleResponse.model_validate_json(content)

        if not response.micro_steps:
            logger.error("LLM returned empty micro_steps array")
            return FALLBACK_DOWNSCALE

        return response

    except asyncio.TimeoutError:
        logger.error("Groq API downscale call timed out after 5 seconds")
        return FALLBACK_DOWNSCALE
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse downscale JSON response: {e}")
        return FALLBACK_DOWNSCALE
    except Exception as e:
        logger.error(f"Groq API downscale call failed: {type(e).__name__}: {e}")
        return FALLBACK_DOWNSCALE
