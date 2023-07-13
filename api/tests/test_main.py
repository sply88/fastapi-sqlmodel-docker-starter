import os

from fastapi.testclient import TestClient

from api.main import app


def test_app(db_uri):
    """
    Confirm that main app correctly integrates the different components
    (environment configuration, database, routers) and confirms expected
    behaviour via running a multi-request scenario.
    """

    # Configure db via env var
    os.environ["DB_URI"] = db_uri

    # Use 'with' statement to make sure that event handlers are executed
    with TestClient(app) as client:
        # Try the health router
        response = client.get("/health/ping")
        assert response.status_code == 200

        # Try the messages router and execute a multi-request scenario test
        response = client.get("/messages")
        assert response.status_code == 200

        # add message
        new_data = {"text": "We are testing the main app.", "label": "unknown"}
        response = client.post(
            "/messages",
            json=new_data
        )
        assert response.status_code == 201

        new_id = response.json()["id"]
        expected_data = {k: v for k, v in new_data.items()}
        expected_data["id"] = new_id

        # confirm message was saved
        response = client.get(f"/messages/{new_id}")
        assert response.status_code == 200
        assert response.json() == expected_data

        # update message
        new_label = "informative"
        response = client.patch(
            f"/messages/{new_id}", json={"label": new_label}
        )
        assert response.status_code == 200
        assert response.json()["label"] == new_label

        # confirm message was updated
        expected_data["label"] = new_label
        response = client.get(f"/messages/{new_id}")
        assert response.status_code == 200
        assert response.json() == expected_data

        # delete message
        response = client.delete(f"/messages/{new_id}")
        assert response.status_code == 204

        # confirm message was deleted
        response = client.get(f"/messages/{new_id}")
        assert response.status_code == 404
