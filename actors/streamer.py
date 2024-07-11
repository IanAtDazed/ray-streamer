"""Module containing the *Streamer* class.

**NOTE:**
- # TODO
"""

import ray

from data.fake_api_data import FAKE_DATA

@ray.remote
class Streamer:
    """Class responsible for streaming data."""

    def __init__(self, stream_symbols: tuple) -> None:
        """Initialize the class.

        Args:
            stream_symbols: The symbols to stream.
        
        **NOTE:**
        - Because this is a fake API, the symbols' data it returns
          is predefined.
        - Typically, you would subscribe to the symbols in *stream_symbols*.
        """

        self._period_number = 0

    def get_latest_period_data(self) -> None:
        """Get the latest period data.
        
        Raises:
            ConnectionError: If no more data is available.
        """

        try:
            latest_ohlcv_data = FAKE_DATA[self._period_number]
        except KeyError:
            raise ConnectionError('No more data available from API.')
        else:
            self._period_number += 1
            return latest_ohlcv_data

