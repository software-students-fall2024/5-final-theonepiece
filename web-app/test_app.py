import pytest
from unittest.mock import MagicMock, patch
from flask_login import AnonymousUserMixin
from flask import url_for
from app import app as flask_app
from user.user import User


@pytest.fixture
def mock_db():
    """Return a mock db object."""
    mock_db = MagicMock()
    mock_collection = MagicMock()
    # Mock a test user in the database
    mock_collection.find_one.return_value = {
        "email": "testuser@example.com",
        "password": "hashed_password",
        "firstname": "Test",
        "lastname": "User",
        "events": [
            {"_id": "1", "Amount": 50, "Category": "Food", "Date": "2024-12-06", "Memo": "Dinner"},
            {"_id": "2", "Amount": 20, "Category": "Rent", "Date": "2024-12-07", "Memo": "Monthly"},
        ]
    }
    mock_db.users = mock_collection
    return mock_db


@pytest.fixture
def client(mock_db, monkeypatch):
    """Create a test client with mocked db."""
    # Patch db in both app and user modules
    monkeypatch.setattr("app.db", mock_db)
    monkeypatch.setattr("user.user.db", mock_db)
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def mock_user_logged_in():
    """Return a mock logged-in user object."""
    user = MagicMock(spec=User)
    user.email = "testuser@example.com"
    user.is_authenticated = True
    user.get_id.return_value = "testuser@example.com"
    # Return static events for analytics and get-events tests
    user.get_events.return_value = [
        {"_id": "1", "Amount": 50, "Category": "Food", "Date": "2024-12-06", "Memo": "Dinner"},
        {"_id": "2", "Amount": 20, "Category": "Rent", "Date": "2024-12-07", "Memo": "Monthly"}
    ]
    return user


def mock_user_logged_out():
    """Return an AnonymousUserMixin to simulate a logged-out user."""
    return AnonymousUserMixin()


class TestAppCoverage:
    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_out)
    def test_index_not_logged_in(self, _, client):
        # Not logged in should redirect to login
        response = client.get("/")
        assert response.status_code == 302
        assert "/user/login" in response.location

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_index_logged_in(self, _, client):
        # Logged in should see a page (Calendar)
        response = client.get("/")
        assert response.status_code == 200

    def test_signup_page(self, client):
        # Just check if we get 200 status code on signup page
        response = client.get("/signup")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_menu_logged_in(self, _, client):
        # Logged in can access menu
        response = client.get("/menu")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_calendar_logged_in(self, _, client):
        response = client.get("/calendar")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_analytics_page_logged_in(self, _, client):
        response = client.get("/analytics")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_search_page_logged_in(self, _, client):
        response = client.get("/search")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_info_get(self, _, client):
        response = client.get("/user-info")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_info_post(self, _, client):
        response = client.post("/user-info", data={"firstname": "New", "lastname": "Name"})
        # Expect redirect after post
        assert response.status_code == 302

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_delete_acct_get(self, _, client):
        response = client.get("/delete-acct")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_logout_route(self, _, client):
        response = client.get("/logout")
        assert response.status_code == 302


class TestUserBlueprintCoverage:
    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_out)
    def test_user_login_get(self, _, client):
        response = client.get("/user/login")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_out)
    @patch("user.user.bcrypt.check_password_hash", return_value=True)
    def test_user_login_post(self, mock_check, _, client):
        response = client.post("/user/login", data={"email": "testuser@example.com", "password": "pass"})
        # Should redirect to index on success
        assert response.status_code == 302

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_out)
    def test_user_signup_get(self, _, client):
        response = client.get("/user/signup")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_add_event(self, _, client):
        response = client.post("/user/add-event", json={
            "amount": 100,
            "category": "TestCategory",
            "date": "2024-12-08",
            "memo": "TestMemo"
        })
        assert response.status_code == 200
        assert response.json == {"message": "Event added successfully"}

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_delete_event(self, _, client):
        response = client.delete("/user/delete-event/2")
        assert response.status_code == 200
        assert response.json == {"message": "Event deleted successfully"}

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_edit_event(self, _, client):
        response = client.put("/user/edit-event/1", json={
            "amount": 200,
            "category": "NewCat",
            "date": "2024-12-09",
            "memo": "NewMemo"
        })
        assert response.status_code == 200
        assert response.json == {"message": "Event updated successfully"}

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_search_events(self, _, client):
        # With word
        response = client.get("/user/search-events/food")
        assert response.status_code == 200

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_search_events_no_word(self, _, client):
        # If empty word route is defined with defaults, it should return 200
        response = client.get("/user/search-events/")
        # Adjust according to your route logic. If you don't handle empty strings, remove this test.
        assert response.status_code in (200, 302, 404)

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    @patch("user.user.bcrypt.check_password_hash", return_value=True)
    def test_delete_account_post_success(self, mock_check, _, client):
        response = client.post("/user/delete-acct", data={
            "email": "testuser@example.com",
            "password": "pass"
        }, follow_redirects=False)
        # Should redirect or show success
        assert response.status_code in (302, 200)

    @patch("flask_login.utils._get_user", side_effect=mock_user_logged_in)
    def test_user_logout(self, _, client):
        response = client.get("/user/logout")
        assert response.status_code == 302


    # Add back the get-events and analytics tests with proper return values:
    @patch("flask_login.utils._get_user")
    def test_user_get_events(self, mock_get_user, client):
        mock_user = mock_user_logged_in()
        # Ensure get_events returns a simple list of dicts
        mock_user.get_events.return_value = [
            {"_id": "1", "Amount": 50, "Category": "Food", "Date": "2024-12-06", "Memo": "Dinner"},
            {"_id": "2", "Amount": 20, "Category": "Rent", "Date": "2024-12-07", "Memo": "Monthly"}
        ]
        mock_get_user.return_value = mock_user
        response = client.get("/user/get-events")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2

    @patch("flask_login.utils._get_user")
    def test_user_analytics_data(self, mock_get_user, client):
        mock_user = mock_user_logged_in()
        # Ensure events have a common month "2024-12"
        mock_user.get_events.return_value = [
            {"_id": "1", "Amount": 50, "Category": "Food", "Date": "2024-12-06", "Memo": "Dinner"},
            {"_id": "2", "Amount": 20, "Category": "Food", "Date": "2024-12-07", "Memo": "Monthly"}
        ]
        mock_get_user.return_value = mock_user
        response = client.get("/user/analytics-data")
        assert response.status_code == 200
        data = response.get_json()
        # Data should contain "2024-12" key
        assert "2024-12" in data
