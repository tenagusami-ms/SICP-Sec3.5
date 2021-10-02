"""
stream module
"""
from __future__ import annotations

import dataclasses
import sys
from itertools import count, repeat, accumulate, chain, islice
from typing import TypeVar, Iterator, Generic

from modules.Math import is_divisible

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

    def __mul__(self, other) -> Stream[T]:
        if isinstance(other, self.__class__):
            return make_stream(multiply_streams(self, other))
        return scale_streams(self, other)

    def __add__(self, other) -> Stream[T]:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return add_2streams(self, other)

    def nth(self, n: int) -> T:
        """
        nth value
        """
        return self.values[n]

    @property
    def rewound(self) -> Stream:
        """
        from start
        """
        return Stream(values=self.values)


def make_stream(iterator: Iterator[T], initial_index=0) -> Stream[T]:
    """
    generate stream
    """
    if isinstance(iterator, Stream):
        return iterator
    return Stream(values=MemoizedInfiniteSequence(iterator=iterator),
                  current_index=initial_index)


def copy_stream(s: Stream) -> Stream:
    """
    copy a stream
    """
    return Stream(values=s.values, current_index=s.current_index)


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


def stream_reference(stream: Stream[T], n: int) -> T:
    """
    nth element of stream
    """
    return stream.nth(n)


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


def multiply_2streams(s1: Stream[T], s2: Stream[T]) -> Stream[T]:
    """
    exercise 3.54-1
    """
    def multiply_generator() -> Iterator[T]:
        """
        multiply generators
        """
        yield next(iter(s1)) * next(iter(s2))
        yield from multiply_2streams(make_stream(s1), make_stream(s2))
    return make_stream(multiply_generator())


def multiply_streams(*streams) -> Stream[T]:
    """
    multiply
    """
    if len(streams) < 2:
        return streams[0]
    return multiply_2streams(streams[0], multiply_streams(*streams[1:]))


def add_2streams(s1: Stream[T], s2: Stream[T]) -> Stream[T]:
    """
    exercise 3.54-1
    """
    def add_generator() -> Iterator[T]:
        """
        add generator
        """
        yield next(iter(s1)) + next(iter(s2))
        yield from add_2streams(make_stream(s1), make_stream(s2))
    return make_stream(add_generator())


def add_streams(*streams) -> Stream[T]:
    """
    multiple addition
    """
    if len(streams) < 2:
        return streams[0]
    return add_streams(streams[0], add_streams(*streams[1:]))


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


def partial_sums(s: Stream[int]) -> Stream[int]:
    """
    exercise 3.55
    """
    return make_stream(accumulate(s))


def scale_streams(s: Stream[T], factor: T) -> Stream[T]:
    """
    scale streams
    """
    def scale_generator(g: Iterator[T]) -> Iterator[T]:
        """
        scale generator
        """
        yield next(iter(g)) * factor
        yield from scale_generator(g)

    return make_stream(scale_generator(s))


def merge_2streams(s1: Stream[T], s2: Stream[T]) -> Stream[T]:
    """
    exercise 3.56-1
    """
    def merge_generator(g1: Iterator[T], g2: Iterator[T]) -> Iterator[T]:
        """
        merge generators
        """
        v1: T = next(iter(g1))
        v2: T = next(iter(g2))

        if v1 < v2:
            yield v1
            yield from merge_generator(g1, chain([v2], g2))
        elif v1 > v2:
            yield v2
            yield from merge_generator(chain([v1], g1), g2)
        else:
            yield v1
            yield from merge_generator(g1, g2)
    return make_stream(merge_generator(s1, s2))


def merge(*streams) -> Stream[T]:
    """
    merge
    """
    if len(streams) < 2:
        return streams[0]
    return merge_2streams(streams[0], merge(*streams[1:]))


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
