import pytest

from datetime import datetime, timedelta

from EventManager import EventManager

@pytest.fixture
def event_manager_empty():
    return EventManager()

@pytest.fixture
def event_manager_has_events():
    em = EventManager()
    em.add_event("event1", datetime(2080, 6, 12, 10), datetime(2080, 6, 12, 12))
    em.add_event("event2", datetime(2080, 6, 13, 14), datetime(2080, 6, 13, 16))
    return em

@pytest.fixture
def event_manager_one_event():
    em = EventManager()
    em.add_event("event1", datetime(2080, 6, 12, 10), datetime(2080, 6, 12, 12))
    return em


class TestEventManager:
    """
        TESTARE FUNCȚIONALĂ
            PARTITIONARE PE CLASE DE ECHIVALENȚĂ
    """
    """
        add_event
    """
    @pytest.mark.parametrize("event_name, start_datetime, end_datetime, expected", [
        ("Meeting", datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=2), True),  # valid N_1, S_1, E_1 -> C_1
        ("", datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=2), False),  # event name empty N_2 -> C_2
        (None, datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=2), False),  # event name not str N_3 -> C_2
        ("Test", "2024-01-01", datetime.now() + timedelta(days=2), False),  # start not datetime S_3 -> C_2
        ("Test", datetime.now() + timedelta(days=2), datetime.now() + timedelta(days=1), False),  # end before start E_2 -> C_2
        ("Test", datetime.now() - timedelta(days=1), datetime.now() + timedelta(days=1), False),  # start before present S_2 -> C_2
        ("Test", datetime.now() + timedelta(days=1), "2024-01-01", False), # end not datetime E_3 -> C_2
    ], ids=[
        "valid_event",
        "event_name_is_empty",
        "event_name_not_string",
        "start_not_datetime",
        "end_before_start",
        "start_before_nowtime",
        "end_not_datetime"
    ])
    def test_add_event_equivalence(self, event_name, start_datetime, end_datetime, expected, event_manager_empty):
        assert event_manager_empty.add_event(event_name, start_datetime, end_datetime) == expected

    """
        get_events_in_range
    """
    @pytest.mark.parametrize("range_start, range_end, expected_count", [
        (datetime(2080, 6, 12, 9), datetime(2080, 6, 12, 11), 1), # valid range - 1 event match
        (datetime(2080, 6, 12, 9), datetime(2080, 6, 13, 17), 2), # valid range - 2 events match
        (datetime(2080, 6, 14, 10), datetime(2080, 6, 14, 12), 0), # valid range - 0 events match
        ("2080-06-12", datetime(2080, 6, 12, 12), 0), # invalid start type
        (datetime(2080, 6, 12, 13), datetime(2080, 6, 12, 10), 0), # start > end
    ], ids=[
        "1_event_match",
        "2_events_match",
        "no_event_match",
        "start_not_datetime",
        "end_before_start"
    ])
    def test_get_events_in_range_equivalence(self, range_start, range_end, expected_count, event_manager_has_events):
        result = event_manager_has_events.get_events_in_range(range_start, range_end)
        assert isinstance(result, list)
        assert len(result) == expected_count

    """
        has_conflict
    """

    @pytest.mark.parametrize("start, end, expected", [
        (datetime(2080, 6, 12, 11), datetime(2080, 6, 12, 13), True), # valid interval, overlaps
        (datetime(2080, 6, 12, 13), datetime(2080, 6, 12, 14), False), # valid interval, no overlap
        ("2080-06-12", datetime(2080, 6, 12, 11), False),
        (datetime(2080, 6, 12, 12), datetime(2080, 6, 12, 10), False), # start > end
    ], ids=[
        "valid_interval_overlap",
        "valid_interval_no_overlap",
        "start_not_datetime",
        "end_before_start"
    ])
    def test_has_conflict_equivalence(self, start, end, expected, event_manager_one_event):
        assert event_manager_one_event.has_conflict(start, end) == expected

    """
        get_event
    """
    @pytest.mark.parametrize("event_name, detailed, expected", [
        ("event1", True, dict), # valid detailed event found
        ("event1", False, True), # valid simple event found
        ("missing", True, False), # valid detailed event not found
        ("", False, False), # invalid event name empty not detailed
        (123, True, False), # invalid event name not str detailed
        ("event1", "yes", False), # invalid detailed not str
    ], ids=[
        "found_detailed",
        "found_brief",
        "not_found",
        "empty_name",
        "non_string_name",
        "invalid_detailed"
    ])
    def test_get_event_equivalence(self, event_name, detailed, expected, event_manager_one_event):
        result = event_manager_one_event.get_event(event_name, detailed)
        if expected == dict:
            assert isinstance(result, dict)
        else:
            assert result == expected

    """
        TESTARE FUNCȚIONALĂ
            ANALIZA VALORILOR DE FRONTIERĂ
    """
    """
        add_event
    """

    @pytest.mark.parametrize("name, start_offset, end_offset, expected", [
        ("test", 1, 1, False), # start = end -> False
        ("test", 1, 1.001, True), # end - start = 1 sec -> True
        ("test", -1, 1, False), # start before present -> False
        ("test", 0.001, 1, True), # start - present = 1 sec -> True
        ("a", 1, 2, True), # len(event_name) = 1 -> True
    ], ids=[
        "start==end",
        "start_before_end_one_sec_valid",
        "start_in_past",
        "start_future_one_sec_valid",
        "one_char_name"
    ])
    def test_add_event_boundary_values(self, start_offset, end_offset, name, expected):
        em = EventManager()
        now = datetime.now()
        start = now + timedelta(seconds=start_offset)
        end = now + timedelta(seconds=end_offset)
        result = em.add_event(name, start, end)
        assert result == expected

    """
        get_events_in_range
    """
    @pytest.mark.parametrize("range_start, range_end, expected", [
        (datetime(2080, 6, 12, 10), datetime(2080, 6, 12, 10), 0), # invalid range_start == range_end
        (datetime(2080, 6, 12, 12, 0), datetime(2080, 6, 12, 11, 59), 0), # invalid start > end 1 minute diff
        (datetime(2080, 6, 12, 8, 0), datetime(2080, 6, 12, 10, 0), 0), # range end == event start no overlap
        (datetime(2080, 6, 12, 12, 0), datetime(2080, 6, 12, 13, 0), 0), # range start == event end no overlap
        (datetime(2080, 6, 12, 10, 0), datetime(2080, 6, 12, 12, 0), 1), #  range start end match event start end overlap
        (datetime(2080, 6, 12, 10, 0, 0, 1), datetime(2080, 6, 12, 10, 0, 0, 2), 1), # during event overlap start_range 1 microsec after event start
        (datetime(2080, 6, 12, 9, 59, 59, 999999), datetime(2080, 6, 12, 10, 0, 0, 1), 1), # partial overlap before
        (datetime(2080, 6, 12, 11, 59, 59, 999999), datetime(2080, 6, 12, 12, 0, 0, 1), 1),  # partial overlap after
    ], ids=[
        "equal_start_end_invalid",
        "start_after_end_invalid",
        "end_equals_event_start",
        "start_equals_event_end",
        "exact_match",
        "inside_event",
        "partial_overlap_before",
        "partial_overlap_after"
    ])
    def test_get_events_in_range_boundary(self, range_start, range_end, expected, event_manager_one_event):
        result = event_manager_one_event.get_events_in_range(range_start, range_end)
        assert len(result) == expected

    """
       TESTARE STRUCTURALĂ
           ACOPERIRE LA NIVEL DE DECIZII ȘI CONDIȚII
    """
    """
        get_event
    """

    # event_name nu e str, asa ca tot if-ul devine True
    def test_invalid_name_type(self, event_manager_one_event):
        result = event_manager_one_event.get_event(123, True)
        assert result is False

    # detailed nu e bool, asa ca tot if-ul devine True
    def test_invalid_detailed_type(self, event_manager_one_event):
        result = event_manager_one_event.get_event("event1", "yes")
        assert result is False

    # evenimentul nu exista, tot for-ul este executat
    def test_event_not_found(self, event_manager_one_event):
        result = event_manager_one_event.get_event("missing", False)
        assert result is False

    # eveniment gasit, detailed e false asa ca return True
    def test_event_found_brief(self, event_manager_one_event):
        result = event_manager_one_event.get_event("event1", False)
        assert result is True

    # eveniment gasit, detailed e True asa ca return event
    def test_event_found_detailed(self, event_manager_one_event):
        result = event_manager_one_event.get_event("event1", True)
        assert isinstance(result, dict)
        assert result["name"] == "event1"