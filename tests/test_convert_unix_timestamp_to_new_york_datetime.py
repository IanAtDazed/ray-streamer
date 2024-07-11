"""pytest module containing tests for *convert_unix_timestamp_to_new_york_datetime*"""

from helpers.datetime_helpers import convert_unix_timestamp_to_new_york_datetime


def test_convert_unix_timestamp_to_new_york_datetime() -> None:
    """Test the *convert_unix_timestamp_to_new_york_datetime* function."""

    # Arrange
    UNIX_TIMESTAMP = 1720522920000
    EXPECTED_DATETIME_STR = '2024-07-09 07:02:00-04:00'

    # Act
    new_york_datetime = convert_unix_timestamp_to_new_york_datetime(UNIX_TIMESTAMP)

    # Assert
    assert str(new_york_datetime) == EXPECTED_DATETIME_STR