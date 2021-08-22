"""
stream module
"""
from __future__ import annotations

from itertools import count, takewhile, repeat
from typing import Iterable, TypeVar, Any, Generator

T = TypeVar("T")


def integers_starting_from(n: int) -> Iterable[int]:
    """
    infinite stream of numbers from
    Args:
        n(int): starting number
    Returns:
        infinite stream(Generator[int, None, Any])
    """
    return count(n)


def integers() -> Iterable[int]:
    """
    integers
    Returns:
        infinite stream of integers
    """
    return count()


def is_divisible(m: int, n: int) -> bool:
    """
    predicate to be divisible
    Args:
        m: dividend
        n: divisor
    Returns:
        True if divisible
    """
    return m % n == 0


def stream_reference(stream: Iterable[T], nth: int) -> T:
    """
    nth element of stream
    Args:
        stream:
        nth:

    Returns:
        element(T)
    """
    def index_predicate(indexed_element: tuple[int, Any]):
        index, _ = indexed_element
        return index < nth + 1

    return list(takewhile(index_predicate, enumerate(stream)))[-1][1]


def fibonacci_generator(a: int, b: int) -> Generator[int, None, Any]:
    """
    Fibonacci numbers
    Args:
        a:
        b:
    Returns:

    """
    yield a
    yield from fibonacci_generator(b, a + b)


def eratosthenes_sieve(stream: Iterable[int]) -> Generator[int, None, Any]:
    """
    Eratosthenes' sieve
    Returns:

    """
    p: int = next(iter(stream))
    yield p
    yield from eratosthenes_sieve(s for s in stream if not is_divisible(s, p))


def ones() -> Iterable[int]:
    """
    repeat 1s
    Returns:

    """
    return repeat(1)


def integers_from_ones() -> Generator[int, None, Any]:
    """
    integers from ones
    Returns:

    """
    yield 1
    yield from (one + i for one, i in zip(ones(), integers_from_ones()))


def fibonacci_adding() -> Generator[int, None, Any]:
    """
    Fibonacci numbers
    Returns:

    """
    yield 0
    yield 1
    fib1 = fibonacci_adding()
    next(iter(fib1))
    yield from (f2 + f1 for f2, f1 in zip(fibonacci_adding(), fib1))


def double() -> Generator[int, None, Any]:
    """
    power of 2
    Returns:

    """
    yield 1
    yield from (2 * i for i in double())
