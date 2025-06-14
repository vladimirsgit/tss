import pytest
from datetime import datetime, timedelta
from EventManager import EventManager

class TestAddEvent:
    def setup_method(self):
        self.em = EventManager()
        self.now = datetime.now()
        self.future_start = self.now + timedelta(hours=1)
        self.future_end = self.now + timedelta(hours=2)

    def test_valid_event(self):
        assert self.em.add_event("Meeting", self.future_start, self.future_end) is True
        assert len(self.em.events) == 1

    def test_start_after_end(self):
        assert self.em.add_event("Invalid", self.future_end, self.future_start) is False

    def test_start_in_past(self):
        past = self.now - timedelta(days=1)
        future = self.now + timedelta(days=1)
        assert self.em.add_event("Past Event", past, future) is False

    def test_empty_event_name(self):
        assert self.em.add_event("", self.future_start, self.future_end) is False

    def test_invalid_types(self):
        assert self.em.add_event(123, "start", "end") is False


class TestGetEventsInRange:
    def setup_method(self):
        self.em = EventManager()
        now = datetime.now()
        self.em.add_event("E1", now + timedelta(hours=1), now + timedelta(hours=2))
        self.em.add_event("E2", now + timedelta(hours=3), now + timedelta(hours=4))

    def test_valid_range_includes_events(self):
        range_start = datetime.now()
        range_end = datetime.now() + timedelta(hours=5)
        events = self.em.get_events_in_range(range_start, range_end)
        assert len(events) == 2

    def test_range_excludes_all(self):
        range_start = datetime.now() + timedelta(days=1)
        range_end = datetime.now() + timedelta(days=2)
        assert self.em.get_events_in_range(range_start, range_end) == []

    def test_invalid_range(self):
        now = datetime.now()
        assert self.em.get_events_in_range(now + timedelta(hours=1), now) == []

    def test_partial_overlap(self):
        now = datetime.now()
        start = now + timedelta(hours=1, minutes=30)
        end = now + timedelta(hours=3, minutes=30)
        events = self.em.get_events_in_range(start, end)
        assert len(events) == 2


class TestHasConflict:
    def setup_method(self):
        self.em = EventManager()
        now = datetime.now()
        self.em.add_event("E1", now + timedelta(hours=1), now + timedelta(hours=2))

    def test_conflict_exists(self):
        start = datetime.now() + timedelta(hours=1, minutes=30)
        end = datetime.now() + timedelta(hours=2, minutes=30)
        assert self.em.has_conflict(start, end) is True

    def test_no_conflict(self):
        start = datetime.now() + timedelta(hours=3)
        end = datetime.now() + timedelta(hours=4)
        assert self.em.has_conflict(start, end) is False

    def test_invalid_times(self):
        end = datetime.now() + timedelta(hours=1)
        start = datetime.now() + timedelta(hours=2)
        assert self.em.has_conflict(start, end) is False


class TestGetEvent:
    def setup_method(self):
        self.em = EventManager()
        now = datetime.now()
        self.em.add_event("E1", now + timedelta(hours=1), now + timedelta(hours=2))

    def test_get_event_detailed(self):
        result = self.em.get_event("E1", True)
        assert isinstance(result, dict)
        assert result['name'] == "E1"

    def test_get_event_non_detailed(self):
        assert self.em.get_event("E1", False) is True

    def test_event_not_found(self):
        assert self.em.get_event("Unknown", False) is False

    def test_invalid_input_types(self):
        assert self.em.get_event(123, "yes") is False
