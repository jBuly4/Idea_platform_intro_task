import json
from datetime import datetime, timedelta


class JSONParser:
    """Parser for JSON-objects."""

    def __init__(self, data: bytes, key: str, timezone_departure: int, timezone_arrival: int):
        """
        Instantiate data object.
        :param key: key to access array with data
        :param data: bytes of data from file
        """
        self.data = json.loads(data)
        self.timezones_diff = timedelta(hours=timezone_departure) - timedelta(hours=timezone_arrival)
        self.key = key

    def get_date(self, position: int, depart: bool) -> datetime:
        """
        Get date as DD.MM.YY HH:MM.
        :param position: position inside array of flights
        :param  depart: True - departure, False - arrival
        :return: date as datetime object
        """
        if depart:
            return datetime.strptime(
                    self.data[self.key][position]["departure_date"] + ' ' \
                    + self.data[self.key][position]["departure_time"], '%d.%m.%y %H:%M'
            )
        return datetime.strptime(
                self.data[self.key][position]["arrival_date"] + ' ' \
                + self.data[self.key][position]["arrival_time"], '%d.%m.%y %H:%M'
        )

    def get_duration(self, position: int) -> timedelta:
        """Get duration of flight in seconds."""
        return (self.get_date(position, False) - self.get_date(position, True) + self.timezones_diff).total_seconds()

    def get_num_of_flights(self) -> int:
        """Get size of array of flights."""
        return len(self.data[self.key])
