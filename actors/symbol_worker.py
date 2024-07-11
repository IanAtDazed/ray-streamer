"""Module containing the *SymbolWorker* class."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ray.util.queue import Queue

import ray

from helpers.datetime_helpers import convert_unix_timestamp_to_new_york_datetime
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

        self._put_result(symbol_latest_period)

    def _put_result(self, symbol_latest_period: dict) -> None:
        """Put the result on the *_result_queue*.
        
        Args:
            symbol_latest_period: The latest period to put on the queue.
        
        **NOTE:** This method handles *None* values, gracefully, but IRL, a *None*
        for any of these intraday stock price attributes would likely indicate issues
        with the API's data, that should not be ignored.
        """

        unix_ts = symbol_latest_period.get('datetime')

        self._result_queue.put(
            ResultInstance(
                self._symbol,
                symbol_latest_period.get('open'),
                symbol_latest_period.get('high'),
                symbol_latest_period.get('low'),
                symbol_latest_period.get('close'),
                symbol_latest_period.get('volume'),
                unix_ts,
                convert_unix_timestamp_to_new_york_datetime(unix_ts) if unix_ts else None
            )
        )