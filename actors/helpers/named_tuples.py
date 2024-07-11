"""Module containing NamedTuple classes for the *actors* module."""

from typing import NamedTuple

class ErrorInstance(NamedTuple):
    """NamedTuple class for returning *error* details."""

    error: Exception

class ResultInstance(NamedTuple):
    """NamedTuple class for returning *result* details."""

    pass # TODO