from functools import lru_cache
from typing import Annotated, List

from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from sqlalchemy import Date, cast
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from src.api.models import RoadAggregatedResponse, SpatialFilterRequest
from src.api.routes import router
from src.database import get_session, init_db
from src.database.models import Link, SpeedRecord
from src.domain import Period, PeriodOption, Weekday, WeekdayOption
from src.settings import Settings


def create_app() -> FastAPI:

    app = FastAPI()

    @app.on_event("startup")
    def on_startup():
        settings = Settings.get()
        init_db(settings.database_url)

    app.include_router(router)

    # NOTE: Keep it after all routes
    app.openapi_schema = get_openapi(
        title="GeoSpatial API",
        version="1.0.0",
        summary="Provide spatial insights about traffic speed through an API",
        description="",
        routes=app.routes)

    return app
