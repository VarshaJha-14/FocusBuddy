"""
main.py — FastAPI application entry point.

Mounts static files, includes route routers, and initializes the database on startup.
"""

from dotenv import load_dotenv
load_dotenv(override=True)

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.session import init_db
from auth.dependencies import CLERK_PUBLISHABLE_KEY
from routes.ingest import router as ingest_router
from routes.steps import router as steps_router
from routes.feedback import router as feedback_router
from routes.transcribe import router as transcribe_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    db_path = os.environ.get("DATABASE_PATH", "focusbuddy.db")
    import db.session as db_session
    db_session.DATABASE_PATH = db_path
    await init_db(db_path)
    logger.info("FocusBuddy is ready! 🚀")
    yield
    logger.info("FocusBuddy shutting down.")


# Create FastAPI app
app = FastAPI(
    title="FocusBuddy",
    description="AI-powered behavioral assistant for task paralysis",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates (shared across routes)
templates = Jinja2Templates(directory="templates")

# Include route routers
app.include_router(ingest_router)
app.include_router(steps_router)
app.include_router(feedback_router)
app.include_router(transcribe_router)