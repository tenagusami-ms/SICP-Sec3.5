"""
stream module
"""
from __future__ import annotations

import dataclasses
from itertools import chain, repeat
from typing import TypeVar, Iterator, Generic

from modules.Stream import make_stream, Stream

T = TypeVar("T")


@dataclasses.dataclass
class Series(Generic[T]):
    """
    ストリーム
    """
    coefficients: Stream[T]  # 係数の無限列

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.coefficients)
        except StopIteration:
            return 0.0

    def __mul__(self, other) -> Series[T]:
        if isinstance(other, self.__class__):
            return multiply_2series(self, other)
        return make_series(self.coefficients * other)

    def __add__(self, other) -> Series[T]:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return add_2series(self, other)

    def __neg__(self) -> Series[T]:
        return make_series(-self.coefficients)

    def __sub__(self, other) -> Series[T]:
        if not isinstance(other, self.__class__):
            raise NotImplementedError()
        return self + (-other)

    def __truediv__(self, other) -> Series[T]:
        if isinstance(other, self.__class__):
            return divide_series(self, other)
        return make_series(self.coefficients * (1.0 / other))

    def nth(self, n: int) -> T:
        """
        nth value
        """
        return self.coefficients.nth(n)

    @property
    def from_0th(self) -> Series[T]:
        """
        from 0th order term
        """
        return make_series(self.coefficients.rewound)


def make_series(coefficient_stream: Stream[T]) -> Series[T]:
    """
    constructor
    """
    return Series(coefficients=coefficient_stream)


def integrated_coefficients(integration_constant: float, s: Iterator[float]) -> Stream[float]:
    """
    exercise 3.59a
    """
    def integration_generator() -> Iterator[float]:
        """
        integration
        """
        yield integration_constant
        factor_inverse: float = 0.0
        while True:
            factor_inverse += 1.0
            yield next(iter(s)) / factor_inverse
    return make_stream(integration_generator())


def negate_series(s: Series[float]) -> Series[float]:
    """
    negate
    """
    return make_series(s.coefficients * (-1.0))


def exponential() -> Series[float]:
    """
    exercise 3.59b-1
    """
    def exp_generator() -> Iterator[float]:
        """
        exponential
        """
        yield from integrated_coefficients(integration_constant, exp_generator())

    integration_constant: float = 1.0
    return make_series(make_stream(exp_generator()))


def sine() -> Series[float]:
    """
    exercise 3.59b-2
    """
    def sine_generator() -> Iterator[float]:
        """
        sine
        """
        yield from integrated_coefficients(0.0, (integrated_coefficients(1.0, -sine())))
    return make_series(make_stream(sine_generator()))


def cosine() -> Series[float]:
    """
    exercise 3.59b-2
    """
    def cosine_generator() -> Iterator[float]:
        """
        cosine
        """
        yield from integrated_coefficients(1.0, (integrated_coefficients(0.0, -cosine())))
    return make_series(make_stream(cosine_generator()))


def add_2series(s1: Series[T], s2: Series[T]) -> Series[T]:
    """
    add 2 series
    """
    return make_series(s1.coefficients + s2.coefficients)


def add_series(*series) -> Stream[T]:
    """
    multiple addition
    """
    if len(series) < 2:
        return series[0]
    return add_series(series[0], add_series(*series[1:]))


def multiply_2series(s0: Series[float], s1: Series[float]) -> Series[float]:
    """
    exercise 3.60
    """
    def multiply_generator() -> Iterator[float]:
        """
        multiplication
        """
        v0: float = next(iter(s0))
        s1v0: Series[float] = s1 * v0
        yield next(iter(s1v0))
        yield from s1v0 + s0 * s1.from_0th

    return make_series(make_stream(multiply_generator()))


def multiply_series(*series) -> Series[T]:
    """
    multiple addition
    """
    if len(series) < 2:
        return series[0]
    return multiply_2series(series[0], multiply_series(*series[1:]))


def inverted_unit_series(s: Series[float]) -> Series[float]:
    """
    exercise 3.61-1
    """
    def inversion_generator() -> Iterator[float]:
        """
        inversion
        """
        _first: float = next(iter(s))  # = 1.0
        yield 1.0
        yield from -s * inverted_unit_series(s.from_0th)
    return make_series(make_stream(inversion_generator()))


def divide_series(numerator: Series[float], denominator: Series[float]) -> Series[float]:
    """
    exercise 3.61-2
    """
    denominator_first_coefficient: float = next(iter(denominator))
    if denominator_first_coefficient == 0.0:
        raise ValueError("division must be done by the series with non-zero 0th-order term.")
    return ((numerator / denominator_first_coefficient)
            * inverted_unit_series(denominator.from_0th / denominator_first_coefficient))


def constant_series(constant: float) -> Series[float]:
    """
    constant
    """
    return make_series(make_stream(chain([constant], repeat(0.0))))


def tangent() -> Series[float]:
    """
    exercise 3.61-3
    """
    return sine() / cosine()


def secant() -> Series[float]:
    """
    exercise 3.61-3
    """
    return inverted_unit_series(cosine())
