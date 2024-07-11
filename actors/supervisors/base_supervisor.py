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
        processing_queue: Queue,
        result_queue: Queue
    ) -> None:
        """Initialize the class.

        Args:
            processing_queue: The queue to add streamed data to for processing.
            result_queue: The queue to to put result data on.
            stream_symbols: The symbols to stream.
        """

        self._processing_queue = processing_queue
        self._result_queue = result_queue
        self._is_processing = True
