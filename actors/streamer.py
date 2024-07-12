"""Module containing the *Streamer* class.

**NOTE**:
- *Typically* this will be *asyncio" functionality
    calling a 3rd party Websockets server.
- For more detail, see: [AsyncIO / Concurrency for Actors](https://docs.ray.io/en/latest/ray-core/actors/async_api.html#asyncio-for-actors)
- For this example, we are *faking* that part.
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
        - The *_request_number* attribute would not be required.
        """

        self._request_number = 0

    def get_latest_data(self) -> None:
        """Get the latest data.

        Raises:
            ConnectionError: If no more data is available.
        """

        try:
            latest_ohlcv_data = FAKE_DATA[self._request_number]
        except KeyError:
            raise ConnectionError('No more data available from API.')
        else:
            self._request_number += 1
            return latest_ohlcv_data
