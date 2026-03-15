from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_aaa():
    # Arrange
    expected_key = "Chess Club"

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert expected_key in data
    assert isinstance(data[expected_key]["participants"], list)


def test_signup_for_activity_aaa():
    # Arrange
    activity = "Chess Club"
    email = "aaa_tester@example.com"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate_aaa():
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up"


def test_delete_participant_aaa():
    # Arrange
    activity = "Programming Class"
    email = "delete_tester@example.com"
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_delete_unknown_participant_aaa():
    # Arrange
    activity = "Programming Class"
    email = "not_a_participant@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found"
