"""
main module
"""
from __future__ import annotations

from typing import Sequence

from modules.Math import is_prime


def main() -> None:
    """
    メインプログラム
    """
    precision: int = 4
    max_number: int = 100

    primes: Sequence[int] = [m for m in range(max_number) if is_prime(m, precision)]
    print(primes)


if __name__ == '__main__':
    main()
