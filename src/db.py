"""
DB definitions.
"""

from typing import Union

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from src.config.settings import get_settings
from src.models import Base

settings = get_settings()
engine = create_engine(settings.db_connection.postgres_uri)
session_factory = sessionmaker(bind=engine)
session: Union[Session, scoped_session] = scoped_session(session_factory)


def create_empty_db() -> None:
    """
    Creates empty database
    """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_db_session(request: Request) -> Session:
    """
    Returns a DB session from app state - works in REST API only
    :param request: Request
    :return: DB session
    """
    return request.app.state.db_session
