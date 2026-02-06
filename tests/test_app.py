import sys
import pathlib
import uuid

# Ensure src is on path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Basketball"
    email = f"test+{uuid.uuid4().hex[:8]}@example.com"

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    # Participant should appear in activity
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # Unregister
    r2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r2.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
