"""
main module
"""
from __future__ import annotations

from itertools import takewhile, islice, repeat, chain
from typing import Sequence, Generator, Any

from modules.Math import is_prime
from modules.Stream import integers_starting_from, integers, is_divisible, stream_reference, fibonacci_generator, \
    eratosthenes_sieve, integers_from_ones, fibonacci_adding, double, factorial, partial_sums, humming_stream, expand, \
    exponential, sine, cosine, multiply_series, add_series, tangent, inverted_unit_series, make_stream, Stream


def main() -> None:
    """
    メインプログラム
    """
    precision: int = 4
    max_number: int = 100
    primes: Sequence[int] = [m for m in range(max_number) if is_prime(m, precision)]
    print(primes)

    print(list(takewhile(lambda x: x < 30, integers_starting_from(10))))

    print(stream_reference(make_stream((n for n in integers() if not is_divisible(n, 7))), 100))

    print(list(takewhile(lambda x: x < 100, fibonacci_generator(0, 1))))

    primes: Sequence[int] = list(islice(eratosthenes_sieve(integers_starting_from(2)), 50))
    print(primes[-1])

    integers2: Generator[int, None, Any] = integers_from_ones()
    print(list(takewhile(lambda x: x < 20, integers2)))

    fibonacci2: Generator[int, None, Any] = fibonacci_adding()
    print(list(takewhile(lambda x: x < 100, fibonacci2)))

    doubles: Generator[int, None, Any] = double()
    print(list(takewhile(lambda x: x < 100, doubles)))

    print(f"exercise 3.54: factorial = {list(takewhile(lambda x: x < 1000, factorial()))}")

    print(f"exercise 3.55: triangular = {list(takewhile(lambda x: x < 100, partial_sums(integers_starting_from(1))))}")

    print(f"exercise 3.56: Humming = {list(takewhile(lambda x: x < 100, humming_stream()))}")

    print(f"exercise 3.58: (expand 1 7 10) = {list(islice(expand(1, 7, 10), 10))}")
    print(f"exercise 3.58: (expand 3 8 10) = {list(islice(expand(3, 8, 10), 10))}")

    print(f"exercise 3.59b: (exp-series) = {list(islice(exponential(), 10))}")
    print(f"exercise 3.59b: (sine-series) = {list(islice(sine(), 10))}")
    print(f"exercise 3.59b: (cosine-series) = {list(islice(cosine(), 10))}")
    print(f"exercise 3.60: (cos^2) ="
          f" {list(islice(multiply_series(cosine(), cosine()), 3))}")
    print(f"exercise 3.60: (sin^2 + cos^2) ="
          f" {list(islice(add_series(multiply_series(cosine(), cosine()), multiply_series(sine(), sine())), 10))}")

    # print(f"exercise 3.61: 1/(1-x) = {list(islice(inverted_unit_series(chain([1.0, -1.0], repeat(0.0))), 5))}")
    # print(f"exercise 3.61: (secant-series) = {list(islice(inverted_unit_series(cosine()), 5))}")
    # print(f"exercise 3.61: (tangent-series) = {list(islice(tangent(), 2))}")


if __name__ == '__main__':
    main()
