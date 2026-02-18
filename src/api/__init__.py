from functools import lru_cache
from typing import Annotated, List

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import Date, cast
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from src.database import get_session, init_db
from src.database.models import Link, SpeedRecord
from src.domain import Period, Weekday
from src.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()

SessionDep = Annotated[Session, Depends(get_session)]

class SpatialFilterRequest(BaseModel):
    day: str
    period: str
    bbox: List[float]


def create_app() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    def on_startup():
        settings = get_settings()
        init_db(settings.database_url)

    @app.get("/")
    def index():
        return {"message": "up and running..."}

    @app.get("/aggregates/")
    def get_aggregates(day: str, period: str, session: SessionDep):
        period_code = Period.from_string(period)
        weekday_code = Weekday.from_string(day)

        stmt = (
            select(
                Link.id,
                func.min(Link.road_name).label("road_name"),
                func.avg(SpeedRecord.speed).label("average_speed"),
                cast(func.ST_AsGeoJSON(func.ST_LineMerge(Link.geom)), JSONB).label(
                    "geometry"
                ),
            )
            .join(SpeedRecord, Link.id == SpeedRecord.link_id)
            .where(
                SpeedRecord.day_of_week == weekday_code,
                SpeedRecord.period == period_code,
            )
            .group_by(Link.id)
        )

        result = session.execute(stmt).mappings().all()

        return result

    @app.post("/aggregates/spatial_filter/")
    def spatial_filter(payload: SpatialFilterRequest, session: SessionDep):
        xmin, ymin, xmax, ymax = payload.bbox
        period_code = Period.from_string(payload.period)
        weekday_code = Weekday.from_string(payload.day)

        stmt = (
            select(
                func.distinct(Link.id),
                func.min(Link.road_name).label("road_name"),
                cast(func.ST_AsGeoJSON(Link.geom), JSONB).label("geometry"),
            )
            .join(SpeedRecord, SpeedRecord.link_id == Link.id)
            .where(
                func.ST_Intersects(
                    Link.geom, func.ST_MakeEnvelope(xmin, ymin, xmax, ymax, 4326)
                ),
                SpeedRecord.period == period_code,
                SpeedRecord.day_of_week == weekday_code,
            )
        )

        result = session.execute(stmt).mappings().all()
        return result

    @app.get("/aggregates/{link_id}")
    def get_aggregate_by_link(link_id: str, day: str, period: str, session: SessionDep):
        period_code = Period.from_string(period)
        weekday_code = Weekday.from_string(day)

        stmt = (
            select(
                Link.id,
                func.min(Link.road_name).label("road_name"),
                func.avg(SpeedRecord.speed).label("average_speed"),
                cast(func.ST_AsGeoJSON(func.ST_LineMerge(Link.geom)), JSONB).label(
                    "geometry"
                ),
            )
            .join(SpeedRecord, Link.id == SpeedRecord.link_id)
            .where(
                Link.id == link_id,
                SpeedRecord.day_of_week == weekday_code,
                SpeedRecord.period == period_code,
            )
            .group_by(Link.id)
        )

        result = session.execute(stmt).mappings().first()

        return result

    @app.get("/patterns/slow_links/")
    def get_slow_links(
        period: str, threshold: float, min_days: int, session: SessionDep
    ):
        """Return links with average speeds below a threshold for at least min_days in a week."""

        period_code = Period.from_string(period)

        stmt = (
            select(
                Link.id,
                func.min(Link.road_name).label("road_name"),
                cast(func.ST_AsGeoJSON(Link.geom), JSONB).label("geometry"),
            )
            .join(SpeedRecord, SpeedRecord.link_id == Link.id)
            .where(
                SpeedRecord.period == period_code,
            )
            .group_by(
                Link.id,
                func.date_part("year", SpeedRecord.timestamp),
                func.date_part("week", SpeedRecord.timestamp),
            )
            .having(
                func.count(func.distinct(cast(SpeedRecord.timestamp, Date)))
                >= min_days,
                func.avg(SpeedRecord.speed) <= threshold,
            )
        )

        result = session.execute(stmt).mappings().all()
        return result

    return app
