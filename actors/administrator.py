"""Module containing the *Administrator* class.

This class manages the *Supervisor* classes.
"""

import sys

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

        self._process_supervisor = ProcessSupervisor.remote(
            self._stream_queue, self._result_queue, stream_symbols)
        self._stream_supervisor = StreamSupervisor.remote(
            self._stream_queue, self._result_queue, stream_symbols)

        self._is_processing = True
        self._process_results()

    def _process_results(self) -> None:
        """Process the results.

        **NOTE:** 
        -*KeyboardInterrupt* is handled here, so that
          the application can be stopped gracefully from the command line.
        - However, if this class formed part of a larger application,
          you would want to achieve this by setting *self._is_processing*
          to *False* externally.
        - In that case, the *KeyboardInterrupt* handling could be removed.
        """

        while self._is_processing:

            try:
                result = self._result_queue.get()
            except KeyboardInterrupt:
                self._is_processing = False
                sys.exit()
            else:
                print(result)
