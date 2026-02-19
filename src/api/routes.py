from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy import cast, func, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
from sqlalchemy.types import Date

from src.api.models import RoadAggregatedResponse, SpatialFilterRequest
from src.database import get_session
from src.database.models import Link, SpeedRecord
from src.domain.types import Period, PeriodOption, Weekday, WeekdayOption

SessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()


@router.get("/", tags=["Healthy Check"])
def index():
    return {"message": "up and running..."}


@router.get(
    "/aggregates/", response_model=List[RoadAggregatedResponse], tags=["Aggregations"]
)
def get_aggregates(day: WeekdayOption, period: PeriodOption, session: SessionDep):
    """Return aggregated average speed per link for the given day and time period."""

    period_code = Period.from_period_option(period).value
    weekday_code = Weekday.from_weekday_option(day).value

    stmt = (
        select(
            Link.id,
            Link.road_name,
            func.avg(SpeedRecord.speed).label("average_speed"),
            cast(func.ST_AsGeoJSON(Link.geom), JSONB).label(
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


@router.post(
    "/aggregates/spatial_filter/",
    response_model=List[RoadAggregatedResponse],
    tags=["Aggregations"],
)
def spatial_filter(payload: SpatialFilterRequest, session: SessionDep):
    """Return road segments intersecting the bounding box for the given day and period."""
    xmin, ymin, xmax, ymax = payload.bbox
    period_code = Period.from_period_option(payload.period).value
    weekday_code = Weekday.from_weekday_option(payload.day).value

    stmt = (
        select(
            func.distinct(Link.id).label("id"),
            Link.road_name,
            func.avg(SpeedRecord.speed).label("average_speed"),
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
        .group_by(Link.id)
    )

    result = session.execute(stmt).mappings().all()
    return result


@router.get(
    "/aggregates/{link_id}",
    response_model=RoadAggregatedResponse,
    tags=["Aggregations"],
)
def get_aggregate_by_link(
    link_id: str, day: WeekdayOption, period: PeriodOption, session: SessionDep
):
    """Return speed and metadata for a single road segment."""
    period_code = Period.from_period_option(period).value
    weekday_code = Weekday.from_weekday_option(day).value

    stmt = (
        select(
            Link.id,
            Link.road_name,
            func.avg(SpeedRecord.speed).label("average_speed"),
            cast(func.ST_AsGeoJSON(Link.geom), JSONB).label(
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


@router.get("/patterns/slow_links/", tags=["Patterns"])
def get_slow_links(
    period: PeriodOption, threshold: float, min_days: int, session: SessionDep
):
    """Return links with average speeds below a threshold for at least min_days in a week."""

    period_code = Period.from_period_option(period)

    stmt = (
        select(
            Link.id,
            Link.road_name,
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
            func.count(func.distinct(cast(SpeedRecord.timestamp, Date))) >= min_days,
            func.avg(SpeedRecord.speed) <= threshold,
        )
    )

    result = session.execute(stmt).mappings().all()
    return result
