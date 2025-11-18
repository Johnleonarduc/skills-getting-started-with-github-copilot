from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()

    # Ensure it returns a dict of activities
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure student is not already in list
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]


def test_signup_activity_not_found():
    response = client.post("/activities/Unknown Activity/signup", params={"email": "student@x.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_registered():
    activity = "Programming Class"
    email = "emma@mergington.edu"  # Already in participants

    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_success():
    activity = "Gym Class"
    email = "john@mergington.edu"

    # Ensure student is present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Unregistered" in response.json()["message"]


def test_unregister_not_found():
    response = client.delete("/activities/Unknown Activity/unregister", params={"email": "x@y.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered():
    activity = "Drama Club"
    email = "notregistered@mergington.edu"

    # Make sure they are not registered
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
