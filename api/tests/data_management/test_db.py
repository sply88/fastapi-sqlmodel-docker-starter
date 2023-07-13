from sqlmodel import select, Session

from api.data_management import Database, Message


def test_database_setup(db_uri):
    Database.setup(db_uri)
    # Confirm creation of engine
    with Session(Database.engine) as session:
        # Confirm creation of table by executing a query
        session.exec(select(Message))
