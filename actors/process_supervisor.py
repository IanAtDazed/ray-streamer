"""Module containing the *ProcessSupervisor* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

from ray.util.queue import Queue

if TYPE_CHECKING:
    from ray.util.queue import Queue

import ray

from actors.base_supervisor import _BaseSupervisor
from actors.symbol_worker import SymbolWorker


@ray.remote
class ProcessSupervisor(_BaseSupervisor):
    """Class responsible for *processing* the streamed data."""

    def __init__(self, stream_queue: Queue, result_queue: Queue, stream_symbols: tuple) -> None:
        """Initialize the class.

        Args:
            stream_queue: The queue to stream data from.
            result_queue: The queue to store the processed data.
            stream_symbols: The symbols to stream.
        """

        super().__init__(stream_queue, result_queue)

        self._assign_symbol_workers(stream_symbols)
        self._is_processing = True
        self._process_streamed_data()

    def _assign_symbol_workers(self, stream_symbols: tuple) -> None:
        """Assign the symbol workers.

        Args:
            stream_symbols: The symbols to assign.
        """

        self._symbol_workers = {
            symbol: SymbolWorker.remote(symbol, self._result_queue)
            for symbol in stream_symbols
        }

    def _process_streamed_data(self) -> None:
        """Process the streamed data."""

        while self._is_processing:
            data = self._stream_queue.get()

            ray.get([symbol_worker.process_latest_period.remote(data)
                     for symbol_worker in self._symbol_workers.values()])
