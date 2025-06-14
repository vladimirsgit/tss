import pytest
from datetime import datetime, timedelta
from EventManager import EventManager

@pytest.fixture
def manager():
    return EventManager()

def test_add_event_success(manager):
    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(hours=2)
    assert manager.add_event("Meeting", start, end) is True

def test_add_event_invalid_dates(manager):
    now = datetime.now()
    assert manager.add_event("Meeting", now, now) is False
    assert manager.add_event("Meeting", now + timedelta(hours=2), now + timedelta(hours=1)) is False

def test_add_event_in_past(manager):
    past = datetime.now() - timedelta(days=1)
    assert manager.add_event("Past Event", past, past + timedelta(hours=1)) is False

def test_get_events_in_range(manager):
    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(hours=2)
    manager.add_event("Event1", start, end)
    results = manager.get_events_in_range(start - timedelta(minutes=30), end + timedelta(minutes=30))
    assert len(results) == 1

def test_get_events_in_range_invalid(manager):
    now = datetime.now()
    assert manager.get_events_in_range(now, now - timedelta(hours=1)) == []

def test_has_conflict_true(manager):
    start = datetime.now() + timedelta(hours=2)
    end = start + timedelta(hours=1)
    manager.add_event("Event1", start, end)
    assert manager.has_conflict(start + timedelta(minutes=15), end + timedelta(minutes=15)) is True

def test_has_conflict_false(manager):
    start = datetime.now() + timedelta(hours=2)
    end = start + timedelta(hours=1)
    manager.add_event("Event1", start, end)
    assert manager.has_conflict(end + timedelta(minutes=1), end + timedelta(hours=1)) is False

def test_get_event_detailed(manager):
    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(hours=2)
    manager.add_event("Event1", start, end)
    result = manager.get_event("Event1", detailed=True)
    assert result['name'] == "Event1"

def test_get_event_non_detailed(manager):
    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(hours=2)
    manager.add_event("Event1", start, end)
    assert manager.get_event("Event1", detailed=False) is True

def test_get_event_invalid(manager):
    assert manager.get_event(123, "yes") is False
