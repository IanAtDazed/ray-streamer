"""Module containing the *ProcessSupervisor* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

import ray.actor

if TYPE_CHECKING:
    from ray.util.queue import Queue

import ray

from actors.symbol_worker import SymbolWorker

# TODO: Inherit from base class
@ray.remote
class ProcessSupervisor:
    """Class responsible for *processing* the streamed data."""

    def __init__(
            self,
            stream_queue: Queue,
            result_queue: Queue,
            stream_symbols: tuple
        ) -> None:
        
        self._stream_queue = stream_queue
        self._result_queue = result_queue
        self._assign_symbol_workers(stream_symbols)
        self._is_processing = True
        self._process_streamed_data()
    
    def _assign_symbol_workers(self, stream_symbols: tuple) -> None:
        """Assign the symbol workers.

        Args:
            stream_symbols: The symbols to assign.
        """

        self._symbol_workers = {
            symbol: SymbolWorker(symbol)
            for symbol in stream_symbols
        }
    
    def _process_streamed_data(self) -> None:
        """Process the streamed data."""

        while self._is_processing:
            data = self._stream_queue.get()

            for symbol_worker in self._symbol_workers.values():
                symbol_worker.process_latest_period(data)