"""Module containing the *Streamer* class.

**NOTE:**
- # TODO
"""

import ray

from data.fake_api_data import FAKE_DATA

@ray.remote
class Streamer:
    """Class responsible for streaming data."""

    def __init__(self) -> None:

        self._period_number = 0

    def get_latest_period_data(self) -> None:
        """Get the latest period data."""

        try:
            latest_ohlcv_data = FAKE_DATA[self._period_number]
        except IndexError:
            return ConnectionError('No more data available.')
        else:
            self._period_number += 1
            return latest_ohlcv_data # TODO: Serialize

