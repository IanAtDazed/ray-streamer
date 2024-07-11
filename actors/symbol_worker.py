"""Module containing the *SymbolWorker* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ray.util.queue import Queue

from actors.helpers.named_tuples import ResultInstance


class SymbolWorker:
    """Class responsible for *processing* a specific streamed data symbol.

    **NOTE:** Typically, you would persist the data, here, but since this
    is a toy example, we are going allow it to be discarded, once it is processed.
    """

    def __init__(self, symbol: str, result_queue: Queue) -> None:
        """Initialize the class.

        Args:
            symbol: The symbol this worker is responsible for.
        """

        self._symbol = symbol
        self._result_queue = result_queue

    def process_latest_period(self, latest_period: dict) -> None:
        """Process the latest streamed period data.

        Args:
            latest_period: The latest period to process.
        """

        symbol_latest_period = latest_period.get(self._symbol)

        if not symbol_latest_period:
            return

        # TODO: Process the latest period data

        self._result_queue.put(
            ResultInstance(
                self._symbol,
                symbol_latest_period.get('open'),
                symbol_latest_period.get('high'),
                symbol_latest_period.get('low'),
                symbol_latest_period.get('close'),
                symbol_latest_period.get('volume'),
                symbol_latest_period.get('datetime'),
                None # TODO
            )
        )

        # print(self._symbol)
        # print(symbol_latest_period)
        # print()
