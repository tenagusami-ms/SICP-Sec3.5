"""
sec 3.5.2 sequence
"""
from __future__ import annotations

from itertools import repeat
from typing import TypeVar, Iterator

from modules.Math import is_divisible
from modules.Stream import Stream, make_stream, integers_starting_from, merge

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
