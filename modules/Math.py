"""
math module
"""
from __future__ import annotations

import random


def power(x, y, p):
    """
    Utility function to do
    modular exponentiation.
    It returns (x^y) % p
    Args:
        x:
        y:
        p:

    Returns:

    """

    # Initialize result
    res = 1

    # Update x if it is more than or
    # equal to p
    x = x % p
    while y > 0:

        # If y is odd, multiply
        # x with result
        if y & 1:
            res = (res * x) % p

        # y must be even now
        y >>= 1  # y = y/2
        x = (x * x) % p

    return res


def miller_test(d, n):
    """
    This function is call
    for all k trials. It
    false if n is composite
    returns false if n is
    probably prime. d is
    number such that d*2<
    for some r >= 1
    Args:
        d:
        n:

    Returns:

    """
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, n - 4)

    # Compute a^d % n
    x = power(a, d, n)

    if x == 1 or x == n - 1:
        return True

    # Keep squaring x while one
    # of the following doesn't
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while d != n - 1:
        x = (x * x) % n
        d *= 2

        if x == 1:
            return False
        if x == n - 1:
            return True

    # Return composite
    return False


def is_prime(n, k):
    """
    It returns false if n is
    composite and returns true if n
    is probably prime. k is an
    input parameter that determines
    accuracy level. Higher value of
    k indicates more accuracy.
    """

    # Corner cases
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    # Find r such that n =
    # 2^d * r + 1 for some r >= 1
    d = n - 1
    while d % 2 == 0:
        d //= 2

    # Iterate given number of 'k' times
    for i in range(k):
        if not miller_test(d, n):
            return False

    return True
