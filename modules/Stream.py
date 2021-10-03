"""
stream module
"""
from __future__ import annotations

import dataclasses
from itertools import count, accumulate, chain, islice
from typing import TypeVar, Iterator, Generic

T = TypeVar("T")


@dataclasses.dataclass
class MemoizedInfiniteSequence(Generic[T]):
    """
    メモ化された無限リスト
    """
    _iterator: Iterator[T]
    __memo: list[T] = dataclasses.field(default_factory=list)

    def __getitem__(self, item):
        return self.value(item)

    def value(self, index: int) -> T:
        """
        インデックスに対する値
        """
        if index < len(self.__memo):
            return self.__memo[index]
        self.__memo += list(islice(self._iterator, index - len(self.__memo) + 1))
        return self.value(index)


@dataclasses.dataclass
class Stream(Generic[T]):
    """
    ストリーム
    """
    values: MemoizedInfiniteSequence[T]  # メモ化された値リストとイテレータの組
    _current_index: int = 0  # 現在のカーソル位置

    def __iter__(self):
        return self

    def __next__(self):
        current_value: T = self.values.value(self._current_index)
        self._current_index += 1
        return current_value

    def __mul__(self, other) -> Stream[T]:
        if isinstance(other, self.__class__):
            return multiply_2streams(self, other)
        return scale_streams(self, other)

    def __add__(self, other) -> Stream[T]:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return add_2streams(self, other)

    def __neg__(self) -> Stream[T]:
        return make_stream((-v for v in self.values), initial_index=self._current_index)

    def __sub__(self, other) -> Stream[T]:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return self + (-other)

    @property
    def current_index(self):
        """
        現在のカーソル位置のゲッタ
        """
        return self._current_index

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

    @property
    def second_latest(self) -> T:
        """
        2nd latest value
        """
        if self._current_index == 0:
            return self.values[0]
        return self.nth(self._current_index - 1)


def make_stream(iterator: Iterator[T], initial_index=0) -> Stream[T]:
    """
    generate stream
    """
    if isinstance(iterator, Stream):
        return iterator
    return Stream(values=MemoizedInfiniteSequence(_iterator=iterator),
                  _current_index=initial_index)


def copy_stream(s: Stream) -> Stream:
    """
    copy a stream
    """
    return Stream(values=s.values, _current_index=s.current_index)


def stream_reference(stream: Stream[T], n: int) -> T:
    """
    nth element of stream
    """
    return stream.nth(n)


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


def partial_sums(s: Stream[T]) -> Stream[T]:
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
        infinite stream of integers starting from 0
    """
    return integers_starting_from(0)
