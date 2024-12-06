"""
Testing code for web app frontend. Run with 'python -m pytest test_app.py'
or to see with coverage run from root directory with
'python -m pytest web-app/test_app.py --cov=web-app'
"""

import pytest
from unittest.mock import MagicMock, patch
from flask import url_for

from app import app as flask_app
from user.user import User


@pytest.fixture
def mock_db(monkeypatch):
    """Mock MongoDB."""
    mock_db = MagicMock()
    mock_users = mock_db.users
    mock_users.find_one.side_effect = lambda query: (
        {
            "email": "testuser@example.com",
            "password": "hashedpassword",
            "firstname": "Test",
            "lastname": "User",
            "events": [
                {
                    "Amount": 50.75,
                    "Category": "Food",
                    "Date": "2024-12-06",
                    "Memo": "Dinner at a restaurant",
                },
                {
                    "Amount": 50.75,
                    "Category": "Transportation",
                    "Date": "2024-12-06",
                    "Memo": "Train",
                },
            ],
        }
        if query.get("email") == "testuser@example.com"
        else None
    )
    mock_db.users = mock_users
    monkeypatch.setattr("database.db", mock_db)
    return mock_db


@pytest.fixture
def mock_user(monkeypatch):
    """Mock a logged-in user."""
    mock_user = MagicMock(spec=User)
    mock_user.email = "testuser@example.com"
    mock_user.firstname = "Test"
    mock_user.lastname = "User"
    mock_user.get_id.return_value = "testuser@example.com"
    mock_user.is_authenticated = True
    mock_user.get_events.return_value = [
        {
            "Amount": 50.75,
            "Category": "Food",
            "Date": "2024-12-06",
            "Memo": "Dinner at a restaurant",
        },
        {
            "Amount": 50.75,
            "Category": "Transportation",
            "Date": "2024-12-06",
            "Memo": "Train",
        },
    ]
    monkeypatch.setattr("flask_login.utils._get_user", lambda: mock_user)
    return mock_user


@pytest.fixture
def client(mock_db):
    """Test client for Flask app."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


class Tests:
    """Test functions"""

    def test_sanity_check(self):
        """Test debugging sanity check."""
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True!"

    @patch("flask_login.utils._get_user")
    @patch("user.user.db")
    @patch("user.user.bcrypt.check_password_hash")
    def test_user_login(
        self, mock_check_password, mock_db, mock_get_user, client, mock_user
    ):
        """Test user login."""
        mock_get_user.return_value = mock_user
        mock_check_password.return_value = (
            True  # Make the password check always return True
        )

        mock_db.users.find_one.return_value = {
            "email": "testuser@example.com",
            "password": "doesn't_matter",
            "firstname": "Test",
            "lastname": "User",
        }

        response = client.post(
            "/user/login",
            data={"email": "testuser@example.com", "password": "password123"},
        )

        assert response.status_code == 302
        assert response.location.endswith(url_for("index"))

        response = client.post(
            "/user/login",
            data={"email": "testuser@example.com", "password": "password123"},
        )
        assert response.status_code == 302
        assert response.location.endswith(url_for("index"))

    def test_user_add_event(self, client, mock_user):
        """Test adding an event for a logged-in user."""
        response = client.post(
            "/user/add-event",
            json={
                "Amount": 100.0,
                "Category": "Entertainment",
                "Date": "2024-12-07",
                "Memo": "Movie night",
            },
        )
        assert response.status_code == 200
        assert response.json == {"message": "Event added successfully"}
        mock_user.add_event.assert_called_once()

    def test_get_events(self, client, mock_user):
        """Test retrieving user events."""
        response = client.get("/user/get-events")
        assert response.status_code == 200
        events = response.json
        assert len(events) == 2
        assert events[0]["Category"] == "Food"
        assert events[1]["Category"] == "Transportation"

    def test_analytics_data(self, client, mock_user):
        """Test analytics data."""
        response = client.get("/user/analytics-data")
        assert response.status_code == 200
        analytics = response.json
        assert "2024-12" in analytics
        assert analytics["2024-12"]["Food"] == 50.75
