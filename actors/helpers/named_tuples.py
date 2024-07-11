"""Module containing NamedTuple classes for the *actors* module."""

from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from datetime import datetime


class ErrorInstance(NamedTuple):
    """NamedTuple class for returning *error* details."""

    error: Exception
    message: str


class ResultInstance(NamedTuple):
    """NamedTuple class for returning *result* details."""

    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    unix_ts: int
    new_york_datetime: datetime
