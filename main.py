"""
main module
"""
from __future__ import annotations

from itertools import takewhile
from typing import Sequence, Generator, Any

from modules.Math import is_prime
from modules.Stream import integers_starting_from, integers, is_divisible, stream_reference, fibonacci_generator, \
    eratosthenes_sieve, integers_from_ones, fibonacci_adding, double


def main() -> None:
    """
    メインプログラム
    """
    precision: int = 4
    max_number: int = 100
    primes: Sequence[int] = [m for m in range(max_number) if is_prime(m, precision)]
    print(primes)

    print(list(takewhile(lambda x: x < 30, integers_starting_from(10))))

    print(stream_reference((n for n in integers() if not is_divisible(n, 7)), 100))

    print(list(takewhile(lambda x: x < 100, fibonacci_generator(0, 1))))

    primes: Generator[int, None, Any] = eratosthenes_sieve(integers_starting_from(2))
    print(stream_reference(primes, 50))

    integers2: Generator[int, None, Any] = integers_from_ones()
    print(list(takewhile(lambda x: x < 20, integers2)))

    fibonacci2: Generator[int, None, Any] = fibonacci_adding()
    print(list(takewhile(lambda x: x < 100, fibonacci2)))

    doubles: Generator[int, None, Any] = double()
    print(list(takewhile(lambda x: x < 100, doubles)))


if __name__ == '__main__':
    main()
