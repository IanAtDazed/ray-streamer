"""Module containing the *Administrator* class.

This class manages the *Supervisor* classes.
"""

from ray.util.queue import Queue

from actors.stream_supervisor import StreamSupervisor
from actors.process_supervisor import ProcessSupervisor

class Administrator:
    """Class for managing the *Supervisor* classes."""

    # TODO
    def __init__(self, stream_symbols: tuple) -> None:
        """Initialize the *Supervisor* classes.
        
        Args:
            stream_symbols: The symbols to stream.
        """

        self._stream_queue = Queue()
        self._result_queue = Queue()

        self._process_supervisor = ProcessSupervisor.remote(self._stream_queue, self._result_queue, stream_symbols)
        self._stream_supervisor = StreamSupervisor.remote(self._stream_queue, self._result_queue)
