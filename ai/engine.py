"""
ai/engine.py — Async Groq LLM calls with timeout and fallback.

Uses the Groq Python SDK with AsyncGroq client.
Model: llama-3.3-70b-versatile
Timeout: 5 seconds
Fallback: hardcoded grounding steps when API is down.
"""

import asyncio
import json
import os
import logging
from typing import Optional

from groq import AsyncGroq

from db.models import LLMResponse

logger = logging.getLogger(__name__)

# ---------- Fallback Steps ----------
# Used when API is down, times out, or returns invalid response
FALLBACK_STEPS = [
    "Take one slow breath. In for 4 counts, out for 4 counts.",
    "Put both feet flat on the floor.",
    "Name one physical object you can see right now.",
    "Open the one file or tab related to your task. Just open it.",
    "Read only the first line of whatever is in front of you.",
]

FALLBACK_RESPONSE = LLMResponse(
    task="Getting Started",
    tone="anchor_mode",
    steps=FALLBACK_STEPS,
)


def _get_client() -> Optional[AsyncGroq]:
    """Create an AsyncGroq client if API key is available."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return None
    return AsyncGroq(api_key=api_key)


async def generate_steps(messages: list[dict]) -> LLMResponse:
    """
    Make an async LLM call to Groq for step generation.

    Args:
        messages: The assembled prompt messages (from prompt.build_prompt).

    Returns:
        Validated LLMResponse with task, tone, and steps.
        Falls back to FALLBACK_RESPONSE on any failure.
    """
    client = _get_client()
    if client is None:
        logger.warning("No Groq API key configured — using fallback steps.")
        return FALLBACK_RESPONSE

    try:
        # 5-second timeout for the entire LLM call
        completion = await asyncio.wait_for(
            client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                response_format={"type": "json_object"},
            ),
            timeout=5.0,
        )

        # Extract response content
        content = completion.choices[0].message.content
        if not content:
            logger.error("Empty response from Groq API")
            return FALLBACK_RESPONSE

        # Validate with Pydantic
        response = LLMResponse.model_validate_json(content)

        # Sanity check: ensure we have at least 1 step
        if not response.steps:
            logger.error("LLM returned empty steps array")
            return FALLBACK_RESPONSE

        return response

    except asyncio.TimeoutError:
        logger.error("Groq API call timed out after 5 seconds")
        return FALLBACK_RESPONSE
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON response: {e}")
        return FALLBACK_RESPONSE
    except Exception as e:
        logger.error(f"Groq API call failed: {type(e).__name__}: {e}")
        return FALLBACK_RESPONSE
