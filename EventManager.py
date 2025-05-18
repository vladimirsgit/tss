from datetime import datetime
from typing import List

class EventManager:
    def __init__(self):
        self.events: List = []

    def add_event(self, event_name: str, start_datetime: datetime, end_datetime: datetime) -> bool:
        if not (isinstance(start_datetime, datetime) and
                isinstance(end_datetime, datetime) and
                isinstance(event_name, str) and
                event_name and
                start_datetime < end_datetime):
            return False

        if start_datetime < datetime.now():
            return False

        self.events.append({
            'name': event_name,
            'start': start_datetime,
            'end': end_datetime
        })
        return True

    def get_events_in_range(self, range_start: datetime, range_end: datetime) -> List:
        if not (isinstance(range_start, datetime) and
                isinstance(range_end, datetime) and
                range_start < range_end):
            return []

        events_in_range = []
        for event in self.events:
            if event['start'] < range_end and event['end'] > range_start:
                events_in_range.append(event)

        return events_in_range

    def has_conflict(self, start_datetime: datetime, end_datetime: datetime) -> bool:
        if not (isinstance(start_datetime, datetime) and
                isinstance(end_datetime, datetime) and
                start_datetime < end_datetime):
            return False

        for event in self.events:
            if event['start'] < end_datetime and event['end'] > start_datetime:
                return True
        return False