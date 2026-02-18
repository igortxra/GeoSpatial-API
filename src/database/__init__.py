from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import (Column, DateTime, Engine, Float, ForeignKey, Integer,
                        String, UniqueConstraint, create_engine)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def init_db(database_url: str):
    global _engine, _SessionLocal

    if _engine is None:
        _engine = create_engine(database_url, pool_pre_ping=True)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)

    Base.metadata.create_all(_engine)


def get_engine() -> Engine:
    if _engine is None:
        raise RuntimeError("DB not initialized. Call init_db() first.")
    return _engine


def get_session():
    if _SessionLocal is None:
        raise RuntimeError("DB not initialized. Call init_db() first.")
    return _SessionLocal()
