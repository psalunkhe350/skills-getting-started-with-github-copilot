from src.app import activities, signup_for_activity, unregister_participant, get_activities
from fastapi import HTTPException
import pytest


def test_get_activities_direct():
    data = get_activities()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_direct():
    activity = "Chess Club"
    email = "testuser+ci@example.com"

    # Ensure clean state (remove if present)
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up (call function directly)
    result = signup_for_activity(activity, email)
    assert "Signed up" in result.get("message", "")
    assert email in activities[activity]["participants"]

    # Unregister
    result = unregister_participant(activity, email)
    assert "Unregistered" in result.get("message", "")
    assert email not in activities[activity]["participants"]


def test_duplicate_signup_raises():
    activity = "Programming Class"
    email = "testdup@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # First signup should succeed
    signup_for_activity(activity, email)

    # Second signup should raise HTTPException with status 400
    with pytest.raises(HTTPException) as exc:
        signup_for_activity(activity, email)
    assert exc.value.status_code == 400

    # Cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
