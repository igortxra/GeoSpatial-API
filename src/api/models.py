
from typing import Any, List, Tuple

from pydantic import BaseModel

from src.domain import PeriodOption, WeekdayOption


class SpatialFilterRequest(BaseModel):
    day: WeekdayOption
    period: PeriodOption
    bbox: Tuple[float, float, float, float]

class Geometry(BaseModel):
    type: str
    coordinates: List[Any]

class RoadAggregatedResponse(BaseModel):
    id: int
    road_name: str | None
    average_speed: float | None
    geometry: Geometry

