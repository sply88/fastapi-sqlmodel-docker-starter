import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.data_management import Database, Message
from api.routers import messages


@pytest.fixture
def app(engine):
    app = FastAPI()
    app.include_router(messages.router)

    def get_session_overwrite():
        yield Session(engine)

    app.dependency_overrides[Database.get_session] = get_session_overwrite

    yield app


@pytest.fixture
def client(app):
    yield TestClient(app)


@pytest.fixture
def message_data():
    return {"text": "This is a test.", "label": "informative"}


def test_list_messages(client, engine, message_data):
    message = Message(**message_data)
    session = Session(engine)
    session.add(message)
    session.commit()

    expected_response_data = message_data
    expected_response_data["id"] = message.id
    expected_response_data = [expected_response_data]

    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() == expected_response_data


def test_list_messages_no_data(client):
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() == []


def test_add_message(client, engine, message_data):
    response = client.post("/messages", json=message_data)
    assert response.status_code == 201

    message_id = response.json()["id"]

    with Session(engine) as session:
        message_db = session.get(Message, message_id)

    assert message_db.dict() == response.json()


def test_get_message(client, engine, message_data):
    with Session(engine) as session:
        message = Message(**message_data)
        session.add(message)
        session.commit()
        message_id = message.id

    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200
    assert response.json() == message.dict()


def test_get_message_not_found(client):
    response = client.get("/messages/1")
    assert response.status_code == 404


def test_update_message(client, engine, message_data):
    with Session(engine) as session:
        message = Message(**message_data)
        session.add(message)
        session.commit()
        message_id = message.id

    new_label = "funny"
    assert new_label != message.label

    response = client.patch(
        f"/messages/{message_id}", json={"label": new_label}
    )
    assert response.status_code == 200
    assert response.json()["label"] == new_label

    with Session(engine) as session:
        message_db = session.get(Message, message_id)

    assert message_db == response.json()


def test_update_message_not_found(client):
    response = client.patch("/messages/1", json={"label": "funny"})
    assert response.status_code == 404


def test_delete_message(client, engine, message_data):
    with Session(engine) as session:
        message = Message(**message_data)
        session.add(message)
        session.commit()
        message_id = message.id

    response = client.delete(f"/messages/{message_id}")
    assert response.status_code == 204
    assert response.text == ""

    with Session(engine) as session:
        message_db = session.get(Message, message_id)
    assert message_db is None


def test_delete_message_not_found(client):
    response = client.delete("/messages/1")
    assert response.status_code == 404
