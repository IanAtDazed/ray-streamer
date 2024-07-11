"""Module for base supervisor."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ray.util.queue import Queue

from abc import ABC


class _BaseSupervisor(ABC):
    """Base supervisor class."""

    def __init__(
        self,
        stream_queue: Queue,
        result_queue: Queue
    ) -> None:
        """Initialize the class.

        Args:
            stream_queue: The queue to stream data from.
            result_queue: The queue to store the processed data.
            stream_symbols: The symbols to stream.
        """

        self._stream_queue = stream_queue
        self._result_queue = result_queue
        self._is_processing = True
