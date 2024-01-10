import logging

from sqlalchemy import JSON, BigInteger, Column, Integer
from sqlalchemy.sql.expression import text

from app.database.database import Base, engine


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    history = Column(JSON, server_default=text("'[]'"), nullable=False)
    frequency = Column(Integer, server_default='30', nullable=False)


async def create_all() -> None:
    """
    Create all tables if they do not already exist.
    """

    logging.info("Trying to create all tables")
    Base.metadata.create_all(bind=engine)
