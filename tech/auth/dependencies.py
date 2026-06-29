"""
auth/dependencies.py — Shared FastAPI dependencies, importable without circular refs.
"""

import os
from tech.auth.clerk import make_auth_dependency

CLERK_PUBLISHABLE_KEY = os.environ.get("CLERK_PUBLISHABLE_KEY")

get_current_user_id = make_auth_dependency(CLERK_PUBLISHABLE_KEY)