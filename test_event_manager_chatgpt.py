from datetime import datetime, timedelta
from EventManager import EventManager

def test_add_event_valid():
    em = EventManager()
    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(hours=1)
    assert em.add_event("Test", start, end)

def test_add_event_invalid_time_order():
    em = EventManager()
    start = datetime.now() + timedelta(hours=2)
    end = datetime.now() + timedelta(hours=1)
    assert not em.add_event("Test", start, end)

def test_add_event_past_start():
    em = EventManager()
    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=1)
    assert not em.add_event("Old Event", start, end)

def test_get_events_in_range_hit():
    em = EventManager()
    now = datetime.now()
    em.add_event("Event1", now + timedelta(hours=1), now + timedelta(hours=2))
    results = em.get_events_in_range(now, now + timedelta(hours=3))
    assert len(results) == 1

def test_get_events_in_range_miss():
    em = EventManager()
    now = datetime.now()
    em.add_event("Event1", now + timedelta(hours=5), now + timedelta(hours=6))
    results = em.get_events_in_range(now, now + timedelta(hours=2))
    assert results == []

def test_has_conflict_yes():
    em = EventManager()
    now = datetime.now()
    em.add_event("Conflicting", now + timedelta(hours=1), now + timedelta(hours=3))
    assert em.has_conflict(now + timedelta(hours=2), now + timedelta(hours=4))

def test_has_conflict_no():
    em = EventManager()
    now = datetime.now()
    em.add_event("NoConflict", now + timedelta(hours=1), now + timedelta(hours=2))
    assert not em.has_conflict(now + timedelta(hours=3), now + timedelta(hours=4))

def test_get_event_exists_detailed():
    em = EventManager()
    now = datetime.now()
    em.add_event("CheckMe", now + timedelta(hours=1), now + timedelta(hours=2))
    result = em.get_event("CheckMe", True)
    assert isinstance(result, dict)

def test_get_event_not_found():
    em = EventManager()
    assert em.get_event("Ghost", True) is False
