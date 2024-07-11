"""Module containing the *SymbolWorker* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ray.util.queue import Queue

import ray

from actors.helpers.named_tuples import ResultInstance


@ray.remote
class SymbolWorker:
    """Class responsible for *processing* a specific streamed data symbol.

    **NOTE:** IRL, _repsository will probably be something like a Polars
    dataframe or a database, etc., rather than a list.
    """

    def __init__(self, symbol: str, result_queue: Queue) -> None:
        """Initialize the class.

        Args:
            symbol: The symbol this worker is responsible for.
        """

        self._symbol = symbol
        self._result_queue = result_queue
        self._repository = []

    def process_latest_period(self, latest_period: dict) -> None:
        """Process the latest streamed period data.

        Args:
            latest_period: The latest period to process.

        **NOTE:**
        - Here, we are simply appending the latest data
          to our repository, and doing a little formatting, before
          putting it on *_result_queue*.
        - IRL, we would be doing something a little more interesting!
        """

        symbol_latest_period = latest_period.get(self._symbol)

        if not symbol_latest_period:
            return

        self._repository.append(symbol_latest_period)

        self._result_queue.put(
            ResultInstance(
                self._symbol,
                symbol_latest_period.get('open'),
                symbol_latest_period.get('high'),
                symbol_latest_period.get('low'),
                symbol_latest_period.get('close'),
                symbol_latest_period.get('volume'),
                symbol_latest_period.get('datetime'),
                None  # TODO
            )
        )
