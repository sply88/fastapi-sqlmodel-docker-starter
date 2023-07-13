from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session, create_engine


class Database:
    engine: Engine

    @classmethod
    def setup(cls, db_uri: str):
        cls.engine = create_engine(db_uri)
        SQLModel.metadata.create_all(cls.engine)

    @classmethod
    def get_session(cls):
        with Session(cls.engine) as session:
            yield session
