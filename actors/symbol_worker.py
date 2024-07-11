"""Module containing the *SymbolWorker* class."""

class SymbolWorker:
    """Class responsible for *processing* a specific streamed data symbol.
    
    **NOTE:** Typically, you would persist the data, here, but since this
    is a toy example, we are going to discard it, once it is processed.
    """

    def __init__(self, symbol: str) -> None:
        """Initialize the class.
        
        Args:
            symbol: The symbol this worker is responsible for.
        """

        self._symbol = symbol
    
    def process_latest_period(self, msg: dict) -> None:
        """Process the latest streamed period data.

        Args:
            msg: The message to process.
        """

        pass # TODO
