
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database.models import Base
from src.settings import settings

engine = create_engine(settings.database_url)

def create_db_and_tables():
    Base.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
