# find the number of permutations from set of k unique primes
#
# for example:
# given 3 primes: p1,p2,p3
# there can be 5 different permutations:
#           1. p1, p2, p3
#           2. p1*p2, p3
#           3. p1*p3, p2
#           4. p1, p2*p3
#           5. p1*p2*p3
#
# using memorization with temporary data types to set the time complexity down to polynomial

import sys
import timeit


def binomial_table(buckets: int, items: int) -> []:
    b = [[0 for _ in range(buckets + 1)] for _ in range(items + 1)]

    for n in range(buckets + 1):
        for k in range(n + 1):
            b[n][k] = 1 if k == 0 or k == n else n if k == 1 or k == n-1 \
                else b[n-1][k-1] + b[n-1][k]

    return b


def PrimePermutations(k_primes: int) -> int:
    binom = binomial_table(k_primes, k_primes)
    f = [[0 for _ in range(k_primes + 1)] for _ in range(k_primes + 1)]

    # f[i][k] - how many permutations k primes can fit in i slots
    for i in range(1, k_primes + 1):
        for k in range(i, k_primes + 1):
            f[i][k] = 1 if i == 1 or i == k else sum(
                binom[k-1][j] * f[i-1][k-1-j] for j in range(0, k-i + 1))

    # debug:
    # for l in f: print(l)

    # sum all solutions of specified k primes
    return sum(f[i][k] for i in range(k_primes + 1))


if __name__ == "__main__":

    MAX_ITERATIONS = 1000
    MIN_ITERATIONS = 1

    if len(sys.argv) > 1:
        primes = int(sys.argv[1])
        iterations = MIN_ITERATIONS if len(sys.argv) < 3 else int(sys.argv[2])

        start = timeit.default_timer()
        for _ in range(iterations):
            result = PrimePermutations(primes)
        end = timeit.default_timer()

        print(f"\nFor {primes} unique primes there are {result} permutations.\n{iterations} iterations of PrimePermutations({primes}) took {1000 * (end - start):.3f} ms\n")

    else:
        print(
            f"Number of permutations from a given number of unique primes\nUsage: {sys.argv[0]} <num of primes> <iterations>")
