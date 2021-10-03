"""
stream module
"""
from __future__ import annotations

from itertools import repeat, chain
from typing import TypeVar, Iterator, Callable

from modules.Math import is_divisible
from modules.Stream import Stream, make_stream, integers_starting_from, merge, partial_sums

T = TypeVar("T")


def fibonacci_generator(a: int, b: int) -> Iterator[int]:
    """
    Fibonacci numbers
    Args:
        a:
        b:
    Returns:

    """
    yield a
    yield from fibonacci_generator(b, a + b)


def eratosthenes_sieve() -> Stream[int]:
    """
    Eratosthenes' sieve
    Returns:

    """
    def sieve_generator(stream: Iterator[int]) -> Iterator[int]:
        """
        sieve
        """
        p: int = next(iter(stream))
        yield p
        yield from sieve_generator(s for s in stream if not is_divisible(s, p))

    return make_stream(sieve_generator(integers_starting_from(2)))


def ones() -> Stream[int]:
    """
    repeat 1s
    """
    return make_stream(repeat(1))


def integers_from_ones() -> Stream[int]:
    """
    integers from ones
    """
    def integer_generator() -> Iterator[int]:
        """
        integers
        """
        yield 1
        yield from make_stream(one + i for one, i in zip(ones(), integers_from_ones()))

    return make_stream(integer_generator())


def fibonacci_adding() -> Stream:
    """
    Fibonacci numbers
    Returns:

    """
    def fibonacci_inner_generator() -> Iterator[int]:
        """
        generator of Fibonacci numbers
        """
        yield 0
        yield 1
        fib1 = fibonacci_inner_generator()
        next(iter(fib1))
        yield from (f2 + f1 for f2, f1 in zip(fibonacci_inner_generator(), fib1))

    return make_stream(fibonacci_inner_generator())


def double() -> Stream[int]:
    """
    power of 2
    """
    def double_generator() -> Iterator[int]:
        """
        double generator
        """
        yield 1
        yield from make_stream(2 * i for i in double())
    return make_stream(double_generator())


def factorial() -> Stream[int]:
    """
    exercise 3.54-2
    """
    def factorial_generator() -> Iterator[int]:
        """
        factorial
        """
        yield 1
        yield from factorial() * integers_starting_from(2)
    return make_stream(factorial_generator())


def humming_stream() -> Stream[int]:
    """
    exercise 3.56-2
    """
    def humming_generator() -> Iterator[int]:
        """
        humming generator
        """
        yield 1
        yield from merge(humming_stream() * 2, humming_stream() * 3, humming_stream() * 5)
    return make_stream(humming_generator())


def expand(numerator: int, denominator: int, radix: int) -> Iterator[int]:
    """
    exercise 3.58
    """
    yield (numerator * radix) // denominator
    yield from expand((numerator * radix) % denominator, denominator, radix)


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
