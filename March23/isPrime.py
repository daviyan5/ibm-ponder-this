import random

def is_prime_rabin_miller(n, k=10):
    if n <= 1:
        return False
    elif n == 2 or n == 3:
        return True
    elif n % 2 == 0:
        return False

    # write n-1 as 2^r*d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # repeat k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

n = int(input())

while n > 0:
    ans = is_prime_rabin_miller(n)

    if ans:
        print(n, " is prime")
    else:
        print(n, " is composite")

    n //= 10