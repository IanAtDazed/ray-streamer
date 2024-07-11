"""Module containing the *StreamSupervisor* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

import ray.exceptions

if TYPE_CHECKING:
    from ray.util.queue import Queue

import ray

from actors.streamer import Streamer
from actors.helpers.named_tuples import ErrorInstance

# TODO: Inherit from base class


@ray.remote
class StreamSupervisor:
    """Class responsible for *fetching* the streamed data."""

    def __init__(
        self,
        stream_queue: Queue,
        result_queue: Queue
    ) -> None:

        self._stream_queue = stream_queue
        self._result_queue = result_queue

        self._streamer = Streamer.remote()
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
            error_type = type(e.args[0])

            self._result_queue.put(ErrorInstance(error_type))

        else:
            self._stream_queue.put(latest_period_ohlcv)
