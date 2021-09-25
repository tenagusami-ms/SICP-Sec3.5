"""
stream module
"""
from __future__ import annotations

import sys
from itertools import count, takewhile, repeat, accumulate, chain
from typing import Iterable, TypeVar, Any, Generator, Iterator, Callable

T = TypeVar("T")
sys.setrecursionlimit(1000)


def integers_starting_from(n: int) -> Iterator[int]:
    """
    infinite stream of numbers from
    Args:
        n(int): starting number
    Returns:
        infinite stream(Generator[int, None, Any])
    """
    return count(n)


def integers() -> Iterator[int]:
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
        """
        index predicate
        Args:
            indexed_element(tuple[int, Any]): indexed
        Returns:

        """
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


def multiply_streams(s1: Iterable[T], s2: Iterable[T]) -> Iterator[T]:
    """
    exercise 3.54-1
    """
    yield next(iter(s1)) * next(iter(s2))
    yield from multiply_streams(s1, s2)


def add_2streams(s1: Iterable[T], s2: Iterable[T]) -> Iterator[T]:
    """
    exercise 3.54-1
    """
    yield next(iter(s1)) + next(iter(s2))
    yield from add_2streams(s1, s2)


def add_streams(*streams) -> Iterator[T]:
    """
    multiple addition
    """
    if len(streams) < 2:
        yield from streams[0]
    yield from add_2streams(streams[0], add_streams(*streams[1:]))


def factorial() -> Generator[int, None, Any]:
    """
    exercise 3.54-2
    """
    yield 1
    yield from multiply_streams(integers_starting_from(2), factorial())


def partial_sums(s: Iterator[int]) -> Iterator[int]:
    """
    exercise 3.55
    """
    return accumulate(s)


def scale_streams(s: Iterator[T], factor: T) -> Iterator[T]:
    """
    scale streams
    """
    yield next(iter(s)) * factor
    yield from scale_streams(s, factor)


def merge(s1: Iterator[int], s2: Iterator[int]) -> Iterator[int]:
    """
    exercise 3.56-1
    """
    # try:
    #     v1: int = next(iter(s1))
    # except StopIteration:
    #     yield from s2
    #
    # try:
    #     v2: int = next(iter(s2))
    # except StopIteration:
    #     yield from s1
    v1: int = next(iter(s1))
    v2: int = next(iter(s2))

    if v1 < v2:
        yield v1
        yield from merge(s1, chain([v2], s2))
    elif v1 > v2:
        yield v2
        yield from merge(chain([v1], s1), s2)
    else:
        yield v1
        yield from merge(s1, s2)


def humming_stream() -> Iterator[int]:
    """
    exercise 3.56-2
    """
    yield 1
    yield from merge(scale_streams(humming_stream(), 2),
                     merge(scale_streams(humming_stream(), 3), scale_streams(humming_stream(), 5)))


def expand(numerator: int, denominator: int, radix: int) -> Iterator[int]:
    """
    exercise 3.58
    """
    yield (numerator * radix) // denominator
    yield from expand((numerator * radix) % denominator, denominator, radix)


def integrate_series(integration_constant: float, s: Iterator[float]) -> Iterator[float]:
    """
    exercise 3.59a
    """
    yield integration_constant
    coefficient_inverse: float = 0.0
    while True:
        coefficient_inverse += 1.0
        yield next(iter(s)) / coefficient_inverse


def negate_series(s: Iterator[float]) -> Iterator[float]:
    """
    negate
    """
    yield from multiply_streams(s, repeat(-1.0))


def exponential() -> Iterator[float]:
    """
    exercise 3.59b-1
    """
    yield from integrate_series(1.0, exponential())


def sine() -> Iterator[float]:
    """
    exercise 3.59b-2
    """
    yield from integrate_series(0.0, (integrate_series(1.0, negate_series(sine()))))


def cosine() -> Iterator[float]:
    """
    exercise 3.59b-2
    """
    yield from integrate_series(1.0, (integrate_series(0.0, negate_series(cosine()))))


add_series: Callable[[Iterator[T], ...], Iterator[T]] = add_streams


def multiply_series(s0: Iterator[float], s1: Iterator[float]) -> Iterator[float]:
    """
    exercise 3.60
    """
    v0: float = next(iter(s0))
    v1: float = next(iter(s1))
    yield v0 * v1
    yield from add_2streams(add_2streams(scale_streams(s1, v0), scale_streams(s0, v1)), multiply_series(s0, s1))


def inverted_unit_series(s: Iterator[float]) -> Iterator[float]:
    """
    exercise 3.61-1
    """
    first: float = next(iter(s))
    yield first
    yield from multiply_series(negate_series(s), inverted_unit_series(chain([first], s)))


def divide_series(numerator: Iterator[float], denominator: Iterator[float]) -> Iterator[float]:
    """
    exercise 3.61-2
    """
    denominator_first_coefficient: float = next(iter(denominator))
    if denominator_first_coefficient == 0.0:
        raise ValueError("division must be done by the series with non-zero 0th-order term.")
    yield from multiply_series(
        scale_streams(numerator, 1.0 / denominator_first_coefficient),
        inverted_unit_series(chain([1.0], scale_streams(denominator, 1.0 / denominator_first_coefficient))))


def tangent() -> Iterator[float]:
    """
    exercise 3.61-3
    """
    yield from divide_series(sine(), cosine())
