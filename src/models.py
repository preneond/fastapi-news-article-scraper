from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Article(Base):  # type: ignore
    __tablename__ = "article"

    id: int = Column(Integer, primary_key=True)
    header: str = Column(String, nullable=False, index=True)
    url: str = Column(String, nullable=False, index=True)
    timestamp: datetime = Column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now(), index=True
    )

    def __str__(self) -> str:
        """
        @return: object representation as string
        """
        return f"Article(id={self.id}, header={self.header}, url={self.url})"
