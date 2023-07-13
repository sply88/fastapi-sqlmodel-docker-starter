import pytest

from sqlmodel import SQLModel, create_engine, Session, select

from api.data_management import Message


@pytest.fixture
def db_uri():
    # Expect a dedicated postgres instance for testing as defined in compose
    # file 'dev.yml'
    return "postgresql://test_user:test_user_pw@127.0.0.1:5555/test_db"


@pytest.fixture
def engine(db_uri):
    engine = create_engine(db_uri)
    SQLModel.metadata.create_all(engine)
    yield engine
    # Wipe all data, so each test starts with a fresh db
    models = [Message]
    with Session(engine) as session:
        for model in models:
            stmt = select(model)
            results = session.exec(stmt)
            for result in results:
                session.delete(result)
        session.commit()
