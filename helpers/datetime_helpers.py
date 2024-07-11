"""Module containing datetime helpers."""

from datetime import datetime
from zoneinfo import ZoneInfo

NY_TIMEZONE = ZoneInfo('America/New_York')

def convert_unix_timestamp_to_new_york_datetime(milliseconds_unix_timestamp: int) -> datetime:
    """Convert a milliseconds UNIX timestamp to a datetime object in the New York timezone.

    Args:
        milliseconds_unix_timestamp: The unix timestamp, in milliseconds, to convert.
    
    Returns:
        The datetime object in New York timezone.
    """

    unix_datetime = datetime.fromtimestamp(milliseconds_unix_timestamp/1000)

    return unix_datetime.astimezone(NY_TIMEZONE)
