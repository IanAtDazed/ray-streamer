"""Module containing the *StreamSupervisor* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

import ray.exceptions
from ray.util.queue import Queue

if TYPE_CHECKING:
    from ray.util.queue import Queue

import ray

from actors.base_supervisor import _BaseSupervisor
from actors.streamer import Streamer
from actors.helpers.named_tuples import ErrorInstance


@ray.remote
class StreamSupervisor(_BaseSupervisor):
    """Class responsible for *fetching* the streamed data."""

    def __init__(self, stream_queue: Queue, result_queue: Queue, stream_symbols: tuple) -> None:
        """Initialize the class.

        Args:
            stream_queue: The queue to stream data from.
            result_queue: The queue to store the processed data.
            stream_symbols: The symbols to stream.
        """

        super().__init__(stream_queue, result_queue)

        self._streamer = Streamer.remote(stream_symbols)
        self._is_streaming = True

        self._stream()

    def _stream(self) -> None:
        """Start the streaming process."""

        while self._is_streaming:
            self._fetch_from_api()

    def _fetch_from_api(self) -> None:
        """Fetch the data from the API.

        **NOTE**:
        - *Typically* this will be *asyncio" functionality
          calling a 3rd party Websockets server.
        - For more detail, see: [AsyncIO / Concurrency for Actors](https://docs.ray.io/en/latest/ray-core/actors/async_api.html#asyncio-for-actors)
        - For this example, we are faking that part.
        """

        try:
            latest_period_ohlcv = ray.get(
                self._streamer.get_latest_period_data.remote())

        except ray.exceptions.RayTaskError as e:
            self._is_streaming = False
            error = e.args[0]

            self._result_queue.put(ErrorInstance(type(error), str(error)))

        else:
            self._stream_queue.put(latest_period_ohlcv)
