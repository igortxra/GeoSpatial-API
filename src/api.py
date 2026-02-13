import os
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from typing import Annotated, List

from sqlalchemy import cast
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func
from sqlalchemy.dialects.postgresql import JSONB
from src.db import Link, SpeedRecord, init_db, get_session
from src.types import Period, Weekday


SessionDep = Annotated[Session , Depends(get_session)]


class SpatialFilterRequest(BaseModel):
    day: str
    period: str
    bbox: List[float]


def create_app() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    def on_startup():
        init_db(os.getenv("DATABASE_URL", "")) # TODO: Improve

    @app.get("/")
    def index():
        return {"message": "up and running..."}

    @app.get("/aggregates/")
    def get_aggregates(day: str, period: str, session: SessionDep):
        period_code = Period.from_string(period)
        weekday_code = Weekday.from_string(day)

        stmt = (
            select(
                Link.id.label("road_name"),
                func.avg(SpeedRecord.speed).label("average_speed"),
                cast(func.ST_AsGeoJSON(func.ST_LineMerge(Link.geom)), JSONB).label("geometry"),
            )
            .join(SpeedRecord, Link.id == SpeedRecord.link_id)
            .where(
                SpeedRecord.day_of_week == weekday_code, 
                SpeedRecord.period == period_code)
            .group_by(Link.id)
        )

        result = session.execute(stmt).mappings().all()

        return result


    @app.get("/aggregates/{link_id}")
    def get_aggregate_by_link(link_id: str, day: str, period: str):
        pass

    @app.get("/patterns/slow_links/")
    def get_slow_links(period: str, threshold: float, min_days: int):
        pass

    @app.post("/aggregates/spatial_filter/")
    def spatial_filter(payload: SpatialFilterRequest):
        pass

    return app
