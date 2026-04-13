"""FastAPI application factory."""

import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from jrebel import __version__
from jrebel.api import api_router
from jrebel.config import get_settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001  # noqa: ARG001
    """Application lifespan context manager."""
    settings = get_settings()
    logger.info(
        "Starting JRebel License Server",
        version=__version__,
        host=settings.host,
        port=settings.port,
    )
    yield
    logger.info("Shutting down JRebel License Server")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()

    app = FastAPI(
        title="JRebel License Server",
        description="A modern JRebel License Server built with FastAPI",
        version=__version__,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router)

    # Setup templates
    import importlib.resources as resources

    templates_path = resources.files("jrebel") / "templates"
    templates = Jinja2Templates(directory=str(templates_path))

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> HTMLResponse:
        """Render the main index page with usage instructions."""
        base_url = str(request.base_url).rstrip("/")
        example_guid = str(uuid.uuid4())

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "base_url": base_url,
                "example_guid": example_guid,
                "server_version": settings.server_version,
                "version": __version__,
            },
        )

    return app


# Application instance
app = create_app()
