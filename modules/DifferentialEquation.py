"""
sec 3.5.3 differential equations
"""
from __future__ import annotations

from typing import TypeVar, Iterator

from modules.Stream import Stream, make_stream

T = TypeVar("T")


def integral(integrand: Stream[float], initial_value: float, dt: float) -> Stream[float]:
    """
    integration
    """
    def integration_generator() -> Iterator[float]:
        """
        integration generator
        """
        yield initial_value
        yield from integrand * dt + make_stream(integration_generator())
    return make_stream(integration_generator())
