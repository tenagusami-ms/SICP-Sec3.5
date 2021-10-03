"""
sec 3.5.3
"""
from __future__ import annotations

from itertools import chain
from typing import TypeVar, Iterator, Callable

from modules.Stream import Stream, make_stream, partial_sums

T = TypeVar("T")


def sqrt_improve(guess: float, x: float) -> float:
    """
    Sec 3.5.3 sqrt-improve
    """
    return (guess + x / guess) / 2.0


def sqrt_stream(x: float) -> Stream[float]:
    """
    sec 3.5.3 sqrt-stream
    """
    def guess_generator() -> Iterator[float]:
        """
        guesses
        """
        yield 1.0
        yield from (sqrt_improve(guess, x) for guess in guess_generator())
    return make_stream(guess_generator())


def pi_summands(n: float) -> Stream[float]:
    """
    sec 3.5.3 pi-summands
    """
    def pi_generator() -> Iterator[float]:
        """
        pi
        """
        yield 1.0 / n
        yield from (-n_inverse for n_inverse in pi_summands(n + 2.0))
    return make_stream(pi_generator())


def pi_stream() -> Stream[float]:
    """
    sec 3.5.3 pi-stream
    """
    return partial_sums(pi_summands(1.0)) * 4.0


def euler_transform(s: Stream[T]) -> Stream[T]:
    """
    sec 3.5.3 Euler transformation
    """
    def euler_generator() -> Iterator[T]:
        """
        euler generator
        """
        s0: T = next(s)
        s1: T = next(s)
        s2: T = next(s)
        yield s2 - (s2 - s1) * (s2 - s1) / (s0 - 2.0 * s1 + s2)
        yield from euler_transform(make_stream(chain([s1, s2], s)))
    return make_stream(euler_generator())


def make_tableau(transform: Callable[[Stream[T]], Stream[T]], s: Stream[T]) -> Stream[T]:
    """
    sec 3.5.3 tableau
    """
    def tableau_generator() -> Iterator[Stream[T]]:
        """
        tableau generator
        """
        yield s
        yield from make_tableau(transform, transform(s))
    return make_stream(tableau_generator())


def accelerated_sequence(transform: Callable[[Stream[T]], Stream[T]], s: Stream[T]) -> Stream[T]:
    """
    sec 3.5.3 accelerated-sequence
    """
    def accelerated_generator() -> Iterator[T]:
        """
        generator
        """
        yield from (next(transformed) for transformed in make_tableau(transform, s))
    return make_stream(accelerated_generator())


def ln2_summands(n: float) -> Stream[float]:
    """
    exercise 3.65
    """
    def ln2_generator() -> Iterator[float]:
        """
        ln2
        """
        yield 1.0 / n
        yield from (-n_inverse for n_inverse in ln2_summands(n + 1.0))
    return make_stream(ln2_generator())


def ln2_stream() -> Stream[float]:
    """
    exercise 3.65
    """
    return partial_sums(ln2_summands(1.0))
