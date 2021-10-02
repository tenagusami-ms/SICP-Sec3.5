"""
main module
"""
from __future__ import annotations

from itertools import takewhile, islice

from modules.Series import exponential, sine, cosine, multiply_2series, add_series, multiply_series
from modules.Stream import integers_starting_from, integers, is_divisible, stream_reference, fibonacci_generator, \
    eratosthenes_sieve, integers_from_ones, fibonacci_adding, double, factorial, partial_sums, humming_stream, \
    make_stream, Stream, scale_streams, expand


def main() -> None:
    """
    メインプログラム
    """
    # precision: int = 4
    # max_number: int = 100
    # primes: Sequence[int] = [m for m in range(max_number) if is_prime(m, precision)]
    # print(f"(primes) = {primes}")

    print(f"(integers-starting-from 10) = {list(takewhile(lambda x: x < 30, integers_starting_from(10)))}")

    print(f"(stream-ref no-sevens 100) ="
          f" {stream_reference(make_stream(n for n in integers() if not is_divisible(n, 7)), 100)}")

    print(f"(fibs) = {list(takewhile(lambda x: x < 100, fibonacci_generator(0, 1)))}")
    primes: Stream[int] = eratosthenes_sieve()
    print(f"(primes) = {list(takewhile(lambda p: p < 100, primes))}")
    print(f"(stream-ref primes 50) = {stream_reference(primes, 50)}")

    integers2: Stream[int] = integers_from_ones()
    print(f"(integers-with-add) = {list(takewhile(lambda x: x < 20, integers2))}")

    fibonacci2: Stream[int] = fibonacci_adding()
    print(f"(fibonacci-with-add) = {list(takewhile(lambda x: x < 100, fibonacci2))}")

    doubles: Stream[int] = double()
    print(f"(double) = {list(takewhile(lambda x: x < 100, doubles))}")

    print(f"exercise 3.54: factorial = {list(takewhile(lambda x: x < 1000, factorial()))}")

    print(f"exercise 3.55: triangular = {list(takewhile(lambda x: x < 100, partial_sums(integers_starting_from(1))))}")

    print(f"exercise 3.56: Humming = {list(takewhile(lambda x: x < 100, humming_stream()))}")

    print(f"exercise 3.58: (expand 1 7 10) = {list(islice(expand(1, 7, 10), 10))}")
    print(f"exercise 3.58: (expand 3 8 10) = {list(islice(expand(3, 8, 10), 10))}")

    print(f"exercise 3.59b: (exp-series) = {list(islice(exponential(), 10))}")
    print(f"exercise 3.59b: (sine-series) = {list(islice(sine(), 10))}")
    print(f"exercise 3.59b: (cosine-series) = {list(islice(cosine(), 10))}")
    print(f"exercise 3.60: (cos^2) ="
          f" {list(islice(multiply_2series(cosine(), cosine()), 10))}")
    print(f"exercise 3.60: (sin^2 + cos^2) ="
          f" {list(islice(add_series(multiply_series(cosine(), cosine()), multiply_series(sine(), sine())), 10))}")

    # print(f"exercise 3.61: 1/(1-x) = {list(islice(inverted_unit_series(chain([1.0, -1.0], repeat(0.0))), 5))}")
    # print(f"exercise 3.61: (secant-series) = {list(islice(inverted_unit_series(cosine()), 5))}")
    # print(f"exercise 3.61: (tangent-series) = {list(islice(tangent(), 2))}")


if __name__ == '__main__':
    main()
