from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from src.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(String, primary_key=True)
    road_name = Column(String, nullable=True)
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4326), nullable=False)

    speed_records = relationship("SpeedRecord", back_populates="link")


class SpeedRecord(Base):
    __tablename__ = "speed_records"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    speed = Column(Float, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)

    link_id = Column(String, ForeignKey("links.id"), index=True)

    link = relationship("Link", back_populates="speed_records")
    
    __table_args__ = (
        UniqueConstraint("timestamp", "link_id", name="uq_speedrecord_ts_link"),
    )

