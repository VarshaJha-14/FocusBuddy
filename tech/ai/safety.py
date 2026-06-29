"""
ai/safety.py — PII scrubbing and crisis keyword detection.

Runs BOTH client-side (via JS regex patterns) and server-side (this module).
Crisis keywords are intercepted BEFORE any LLM call.
"""

import re
from typing import Tuple


# ---------- PII Patterns ----------
# Each tuple: (compiled regex, replacement label)
PII_PATTERNS = [
    # Email addresses
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '[EMAIL]'),
    # Phone numbers — Indian formats (10-digit, with optional +91/0 prefix)
    (re.compile(r'(?:\+91[\s-]?|0)?[6-9]\d{4}[\s-]?\d{5}\b'), '[PHONE]'),
    # Phone numbers — international (generic)
    (re.compile(r'\+?\d{1,3}[\s-]?\(?\d{1,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}'), '[PHONE]'),
    # Aadhaar numbers (12 digits, often space/dash separated in groups of 4)
    (re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'), '[AADHAAR]'),
    # PAN numbers (ABCDE1234F pattern)
    (re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b'), '[PAN]'),
    # Credit card numbers (13-19 digits, possibly space/dash separated)
    (re.compile(r'\b(?:\d{4}[\s-]?){3,4}\d{1,4}\b'), '[CARD]'),
    # IP addresses
    (re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'), '[IP]'),
    # SSN-like (US format)
    (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), '[SSN]'),
]


# ---------- Crisis Keywords ----------
# Word-boundary matching to avoid false positives (e.g., "therapist" won't match "the rapist")
CRISIS_KEYWORDS = [
    # Suicidal ideation
    r'\bsuicid(?:e|al)\b',
    r'\bkill\s+my\s*self\b',
    r'\bend\s+(?:my\s+)?life\b',
    r'\bwant\s+to\s+die\b',
    r'\bdon\'?t\s+want\s+to\s+(?:live|be\s+alive|exist)\b',
    r'\bbetter\s+off\s+dead\b',
    r'\bno\s+reason\s+to\s+live\b',
    r'\bhopeless\b',
    # Self-harm
    r'\bself[\s-]?harm\b',
    r'\bcut(?:ting)?\s+my\s*self\b',
    r'\bhurt(?:ing)?\s+my\s*self\b',
    # Domestic violence
    r'\b(?:he|she|they|partner|spouse)\s+(?:hit|hits|beat|beats|hurt|hurts)\s+me\b',
    r'\bdomestic\s+(?:violence|abuse)\b',
    r'\babused?\b',
]

CRISIS_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in CRISIS_KEYWORDS]


def scrub_pii(text: str) -> str:
    """
    Remove personally identifiable information from text using regex patterns.
    Applied server-side as a safety net (client-side JS also scrubs before POST).
    """
    scrubbed = text
    for pattern, replacement in PII_PATTERNS:
        scrubbed = pattern.sub(replacement, scrubbed)
    return scrubbed


def check_crisis(text: str) -> bool:
    """
    Check if text contains crisis-related keywords.
    Returns True if crisis is detected — caller should return crisis modal
    and skip ALL LLM processing.
    """
    for pattern in CRISIS_PATTERNS:
        if pattern.search(text):
            return True
    return False


def get_pii_patterns_js() -> list[dict]:
    """
    Return PII patterns in a format suitable for client-side JavaScript.
    Used to generate the client-side scrubbing script.
    """
    return [
        {"pattern": r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", "replacement": "[EMAIL]"},
        {"pattern": r"(?:\+91[\s-]?|0)?[6-9]\d{4}[\s-]?\d{5}", "replacement": "[PHONE]"},
        {"pattern": r"\+?\d{1,3}[\s-]?\(?\d{1,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}", "replacement": "[PHONE]"},
        {"pattern": r"\d{4}[\s-]?\d{4}[\s-]?\d{4}", "replacement": "[AADHAAR]"},
        {"pattern": r"[A-Z]{5}\d{4}[A-Z]", "replacement": "[PAN]"},
        {"pattern": r"\b\d{3}-\d{2}-\d{4}\b", "replacement": "[SSN]"},
    ]
