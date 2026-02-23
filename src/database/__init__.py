from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database.models import Base
from src.settings import settings

engine = create_engine(settings.database_url)

def get_session():
    with Session(engine) as session:
        yield session
