"""Module containing the *SymbolWorker* class."""

class SymbolWorker:
    """Class responsible for *processing* a specific streamed data symbol.
    
    **NOTE:** Typically, you would persist the data, here, but since this
    is a toy example, we are going allow it to be discarded, once it is processed.
    """

    def __init__(self, symbol: str) -> None:
        """Initialize the class.
        
        Args:
            symbol: The symbol this worker is responsible for.
        """

        self._symbol = symbol
    
    def process_latest_period(self, latest_period: dict) -> None:
        """Process the latest streamed period data.

        Args:
            latest_period: The latest period to process.
        """

        symbol_latest_period = latest_period.get(self._symbol)

        if not symbol_latest_period:
            return

        print(self._symbol)
        print(symbol_latest_period)
        print()
