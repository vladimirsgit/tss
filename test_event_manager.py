import pytest
from datetime import datetime, timedelta

from EventManager import EventManager

@pytest.fixture
def event_manager_empty():
    return EventManager()

@pytest.fixture
def event_manager_one_event():
    event_manager = EventManager()
    event_manager.add_event('name', datetime.now() + timedelta(minutes=1), datetime.now() + timedelta(minutes=2))
    return event_manager

"""
    Partitionarea in clase de echivalenta
"""

"""
    add_event
"""
def test_add_event_valid(event_manager_empty):
    event_to_add = {
        'name': 'name',
        'start': datetime.now() + timedelta(days=1),
        'end': datetime.now() + timedelta(days=2)
    }
    res = event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert res == True


def test_add_event_valid_event_is_added(event_manager_empty):
    event_to_add = {
        'name': 'name',
        'start': datetime.now() + timedelta(days=1),
        'end': datetime.now() + timedelta(days=2)
    }
    assert len(event_manager_empty.events) == 0

    event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert len(event_manager_empty.events) == 1

def test_add_event_invalid_event_name_type_is_int(event_manager_empty):
    event_to_add = {
        'name': 1,
        'start': datetime.now() + timedelta(days=1),
        'end': datetime.now() + timedelta(days=2)
    }

    res = event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert res == False


def test_add_event_invalid_start_date_type_is_str(event_manager_empty):
    event_to_add = {
        'name': 'name',
        'start': str(datetime.now() + timedelta(days=1)),
        'end': datetime.now() + timedelta(days=2)
    }

    res = event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert res == False


def test_add_event_invalid_start_date_after_end_date(event_manager_empty):
    event_to_add = {
        'name': 'name',
        'start': datetime.now() + timedelta(days=2),
        'end': datetime.now() + timedelta(days=1)
    }

    res = event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert res == False

def test_add_event_invalid_start_date_before_current_date(event_manager_empty):
    event_to_add = {
        'name': 'name',
        'start': datetime.now() - timedelta(days=1),
        'end': datetime.now() + timedelta(days=1)
    }

    res = event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert res == False

"""
    get_events_in_range
"""
def test_get_events_in_range_valid_found_one(event_manager_one_event):
    range_start = datetime.now()
    range_end = datetime.now() + timedelta(minutes=3)

    res = event_manager_one_event.get_events_in_range(range_start, range_end)

    assert len(res) == 1


def test_get_events_in_range_valid_found_zero(event_manager_one_event):
    range_start = datetime.now()
    range_end = datetime.now() + timedelta(seconds=30)

    res = event_manager_one_event.get_events_in_range(range_start, range_end)

    assert not res


def test_get_events_in_range_invalid_range_start_is_str(event_manager_one_event):
    range_start = '2027-01-01'
    range_end = datetime.now() + timedelta(minutes=3)
    res = event_manager_one_event.get_events_in_range(range_start, range_end)

    assert not res

def test_get_events_in_range_invalid_range_end_is_str(event_manager_one_event):
    range_start = datetime.now() + timedelta(minutes=3)
    range_end = '2027-01-01'
    res = event_manager_one_event.get_events_in_range(range_start, range_end)

    assert not res


def test_get_events_in_range_invalid_range_start_after_range_end(event_manager_one_event):
    range_start = datetime.now() + timedelta(minutes=3)
    range_end = datetime.now() + timedelta(minutes=2)
    res = event_manager_one_event.get_events_in_range(range_start, range_end)

    assert not res


def test_get_events_in_range_no_events_saved(event_manager_empty):
    range_start = datetime.now() + timedelta(minutes=1)
    range_end = datetime.now() + timedelta(minutes=3)
    res = event_manager_empty.get_events_in_range(range_start, range_end)

    assert not res

"""
    has_conflict
"""
def test_has_conflict_valid_conflict_found(event_manager_one_event):
    start_datetime = datetime.now() + timedelta(minutes=1)
    end_datetime = datetime.now() + timedelta(minutes=3)

    res = event_manager_one_event.has_conflict(start_datetime, end_datetime)

    assert res

def test_has_conflict_valid_no_conflict_found(event_manager_one_event):
    start_datetime = datetime.now() + timedelta(minutes=5)
    end_datetime = datetime.now() + timedelta(minutes=10)

    res = event_manager_one_event.has_conflict(start_datetime, end_datetime)

    assert not res

def test_has_conflict_valid_no_conflict_found_no_events_saved(event_manager_empty):
    start_datetime = datetime.now() + timedelta(minutes=5)
    end_datetime = datetime.now() + timedelta(minutes=10)

    res = event_manager_empty.has_conflict(start_datetime, end_datetime)

    assert not res


def test_has_conflict_invalid_start_datetime_is_str(event_manager_one_event):
    start_datetime = '2017-01-01'
    end_datetime = datetime.now() + timedelta(minutes=10)

    res = event_manager_one_event.has_conflict(start_datetime, end_datetime)

    assert not res

def test_has_conflict_invalid_end_datetime_is_str(event_manager_one_event):
    start_datetime = datetime.now() + timedelta(minutes=1)
    end_datetime = '2017-01-01'

    res = event_manager_one_event.has_conflict(start_datetime, end_datetime)

    assert not res

def test_has_conflict_invalid_start_datetime_after_end_datetime(event_manager_one_event):
    start_datetime = datetime.now() + timedelta(minutes=6)
    end_datetime = datetime.now() + timedelta(minutes=4)

    res = event_manager_one_event.has_conflict(start_datetime, end_datetime)

    assert not res

"""
    Analiza valorilor de frontiera
"""

"""
    add_events
"""
def test_add_event_event_name_empty(event_manager_empty):
    event_to_add = {
        'name': '',
        'start': datetime.now() + timedelta(days=1),
        'end': datetime.now() + timedelta(days=2)
    }

    res = event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert res == False

def test_add_event_start_date_equals_end_date(event_manager_empty):
    same_date = datetime.now() + timedelta(days=1)
    event_to_add = {
        'name': 'name',
        'start': same_date,
        'end': same_date
    }

    res = event_manager_empty.add_event(event_to_add['name'], event_to_add['start'], event_to_add['end'])

    assert res == False


"""
    get_events_in_range
"""
def test_get_events_range_start_equals_range_end(event_manager_one_event):
    same_date = datetime.now() + timedelta(minutes=3)

    res = event_manager_one_event.get_events_in_range(same_date, same_date)

    assert not res


def test_get_events_range_start_at_event_end(event_manager_one_event):
    event_end = event_manager_one_event.events[0]['end']
    range_start = event_end
    range_end = datetime.now() + timedelta(minutes=3)

    res = event_manager_one_event.get_events_in_range(range_start, range_end)

    assert not res


def test_get_events_range_end_at_event_start(event_manager_one_event):
    event_start = event_manager_one_event.events[0]['start']
    range_start = datetime.now() + timedelta(minutes=0)
    range_end = event_start

    res = event_manager_one_event.get_events_in_range(range_start, range_end)

    assert not res

"""
    has_conflict
"""

def test_has_conflict_start_datetime_equals_end_datetime(event_manager_empty):
    same_date = datetime.now()

    res = event_manager_empty.has_conflict(same_date, same_date)

    assert not res


def test_has_conflict_start_datetime_equals_event_end_datetime(event_manager_one_event):
    existing_event = event_manager_one_event.events[0]
    start_datetime = existing_event['start']
    end_datetime = datetime.now() + timedelta(minutes=3)


    res = event_manager_one_event.has_conflict(start_datetime, end_datetime)

    assert res


def test_has_conflict_end_datetime_equals_event_start_datetime(event_manager_one_event):
    existing_event = event_manager_one_event.events[0]
    start_datetime = datetime.now() + timedelta(minutes=0)
    end_datetime = existing_event['end']

    res = event_manager_one_event.has_conflict(start_datetime, end_datetime)

    assert res