"""
stream module
"""
from __future__ import annotations

import copy
import dataclasses
import sys
from itertools import count, takewhile, repeat, accumulate, chain, islice
from typing import Iterable, TypeVar, Any, Generator, Iterator, Callable, Generic

T = TypeVar("T")
sys.setrecursionlimit(1000)


@dataclasses.dataclass
class MemoizedInfiniteSequence(Generic[T]):
    """
    メモ化された無限リスト
    """
    iterator: Iterator[T]
    memo: list[T] = dataclasses.field(default_factory=list)

    def __getitem__(self, item):
        return self.value(item)

    def value(self, index: int) -> T:
        """
        インデックスに対する値
        Args:
            index:

        Returns:

        """
        if index < len(self.memo):
            return self.memo[index]
        self.memo += list(islice(self.iterator, index - len(self.memo) + 1))
        return self.value(index)


@dataclasses.dataclass
class Stream(Generic[T]):
    """
    ストリーム
    """
    values: MemoizedInfiniteSequence[T]  # メモ化された値リストとイテレータの組
    current_index: int = 0  # 現在のカーソル位置

    def __iter__(self):
        return self

    def __next__(self):
        current_value: T = self.values.value(self.current_index)
        self.current_index += 1
        return current_value

    def nth(self, n: int) -> T:
        """
        nth value
        """
        return self.values.value(n)


def make_stream(iterator: Iterator[T]) -> Stream[T]:
    """
    generate stream
    """
    if isinstance(iterator, Stream):
        return iterator
    return Stream(values=MemoizedInfiniteSequence(iterator=iterator))


def copy_stream(s: Stream) -> Stream:
    """
    copy a stream
    """
    return copy.copy(s)


def integers_starting_from(n: int) -> Stream[int]:
    """
    infinite stream of numbers from
    Args:
        n(int): starting number
    Returns:
        infinite stream(Generator[int, None, Any])
    """
    return make_stream(count(n))


def integers() -> Stream[int]:
    """
    integers
    Returns:
        infinite stream of integers
    """
    return make_stream(count())


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


def stream_reference(stream: Stream[T], n: int) -> T:
    """
    nth element of stream
    """
    return stream.nth(n)


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


def eratosthenes_sieve(stream: Iterator[int]) -> Stream[int]:
    """
    Eratosthenes' sieve
    Returns:

    """
    p: int = next(iter(stream))
    yield p
    yield from eratosthenes_sieve(make_stream(s for s in stream if not is_divisible(s, p)))


def ones() -> Stream[int]:
    """
    repeat 1s
    """
    return make_stream(repeat(1))


def integers_from_ones() -> Stream[int]:
    """
    integers from ones
    """
    yield 1
    yield from make_stream(one + i for one, i in zip(ones(), integers_from_ones()))


def fibonacci_adding() -> Generator[int, None, Any]:
    """
    Fibonacci numbers
    Returns:

    """
    yield 0
    yield 1
    fib1 = fibonacci_adding()
    next(iter(fib1))
    yield from make_stream(f2 + f1 for f2, f1 in zip(fibonacci_adding(), fib1))


def double() -> Generator[int, None, Any]:
    """
    power of 2
    Returns:

    """
    yield 1
    yield from make_stream(2 * i for i in double())


def multiply_streams(s1: Iterator[T], s2: Iterator[T]) -> Iterator[T]:
    """
    exercise 3.54-1
    """
    yield next(iter(s1)) * next(iter(s2))
    yield from multiply_streams(make_stream(s1), make_stream(s2))


def add_2streams(s1: Iterator[T], s2: Iterator[T]) -> Iterator[T]:
    """
    exercise 3.54-1
    """
    yield next(iter(s1)) + next(iter(s2))
    yield from add_2streams(make_stream(s1), make_stream(s2))


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
    yield from scale_streams(make_stream(s), factor)


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
    yield from add_2streams(add_2streams(scale_streams(make_stream(s1), v0),
                                         scale_streams(make_stream(s0), v1)),
                            multiply_series(make_stream(s0), make_stream(s1)))


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
