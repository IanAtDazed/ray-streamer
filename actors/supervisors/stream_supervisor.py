"""Module containing the *StreamSupervisor* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

import ray.exceptions
from ray.util.queue import Queue

if TYPE_CHECKING:
    from ray.util.queue import Queue

import ray

from actors.supervisors.base_supervisor import _BaseSupervisor
from actors.streamer import Streamer
from actors.helpers.named_tuples import ErrorInstance


@ray.remote
class StreamSupervisor(_BaseSupervisor):
    """Class responsible for *fetching* the streamed data."""

    def __init__(self, processing_queue: Queue, result_queue: Queue, stream_symbols: tuple) -> None:
        """Initialize the class.

        Args:
            processing_queue: The queue to add streamed data to for processing.
            result_queue: The queue to to put result data on.
            stream_symbols: The symbols to stream.
        """

        super().__init__(processing_queue, result_queue)

        self._streamer = Streamer.remote(stream_symbols)

        self._stream()

    def _stream(self) -> None:
        """Start the streaming process."""

        while self._is_processing:
            self._fetch_from_api()

    def _fetch_from_api(self) -> None:
        """Fetch the data from the API.

        - Typically, puts the latest streamed data on the *_processing_queue*.
        - If there is an error (such as the API connection closing),
          it stops the streaming process and puts an *ErrorInstance* on the *_result_queue*.
        """

        try:
            latest_period_ohlcv = ray.get(
                self._streamer.get_latest_period_data.remote())

        except ray.exceptions.RayTaskError as e:
            self._is_processing = False
            error = e.args[0]

            self._result_queue.put(ErrorInstance(type(error), str(error)))

        else:
            self._processing_queue.put(latest_period_ohlcv)
