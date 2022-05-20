"""Quick benchmarking to validate the usability of @memoize"""

import functools
import time

from src.memoize import memoize


def simplified_memoize(f=None):
    """Simplified Memoizer for benchmarking comparison"""

    class SimplifiedMemoized(object):
        cache = {}

        def __init__(self, func):
            self.func = func
            self.key = (func.__module__, func.__name__)
            self.cache[self.key] = {}

        def __call__(self, *args):
            try:
                return SimplifiedMemoized.cache[self.key][args]
            except KeyError:
                value = self.func(*args)
                SimplifiedMemoized.cache[self.key][args] = value
                return value
            except TypeError:
                # uncachable -- for instance, passing a list as an argument.
                # Better to not cache than to blow up entirely.
                return self.func(*args)

        def __get__(self, obj, objtype):
            """Support instance methods."""
            return functools.partial(self.__call__, obj)

        @staticmethod
        def reset():
            SimplifiedMemoized.cache = {}

    if f:
        return SimplifiedMemoized(f)
    else:
        def wrapper(func):
            return SimplifiedMemoized(func)
        return wrapper


def benchmark_memoized_class_simple(num_iters=1000000, init_computations=1000):
    print(f"Benchmark test for Memoized vs Non-memoized classes with [{init_computations}] computations in their"
          f"__init__() methods for [{num_iters}] iterations")

    @memoize(arg_hash_function=str)
    class MemoizedTest:
        def __init__(self, p1, p2, p3, p4):
            self._p1 = p1
            self._p2 = p2
            self._p3 = p3
            self._p4 = p4
            # Some computations
            for _ in range(init_computations):
                if p1 is None:
                    raise Exception("should not happen")

        def echo(self):
            """Call this after creating the object to prevent any under the hood optimizations"""
            return self._p1, self._p2, self._p3, self._p4

    class NonMemoizedTest:
        def __init__(self, p1, p2, p3, p4):
            self._p1 = p1
            self._p2 = p2
            self._p3 = p3
            self._p4 = p4
            # Some computations
            for _ in range(init_computations):
                if p1 is None:
                    raise Exception("should not happen")

        def echo(self):
            """Call this after creating the object to prevent any under the hood optimizations"""
            return self._p1, self._p2, self._p3, self._p4

    p1s = ["static string"] * num_iters
    p2s = []
    for i in range(num_iters):
        p2s.append("hello")
    p3s = [""] * num_iters
    p4s = [[1, 2, 3, 4]] * num_iters

    # NonMemoized
    start_time = time.time()
    for i in range(num_iters):
        a = NonMemoizedTest(p1s[i], p2s[i], p3s[i], p4s[i])
        a.echo()
    duration = time.time() - start_time
    print(f"Non-memoized class creation + empty method call average time (ms): {duration/num_iters * 1000}")

    # Memoized
    start_time = time.time()
    for i in range(num_iters):
        a = MemoizedTest(p1s[i], p2s[i], p3s[i], p4s[i])
        a.echo()
    duration = time.time() - start_time
    print(f"Memoized class creation + empty method call average time (ms): {duration/num_iters * 1000}")


def benchmark_fib(num_iters=10000000, fib_num=100):
    print(f"Benchmark test for @memoize, non-memoized, a @simplified_memoize, and @functools.lru_cache comparison using"
          f"function calculating fibonacci sum for [{fib_num}] fib numbers, for [{num_iters}] iterations")

    @simplified_memoize
    def simp_memo_fib(n):
        if n in (0, 1):
            return n
        return simp_memo_fib(n - 1) + simp_memo_fib(n - 2)

    @functools.lru_cache(maxsize=None)
    def lru_cache_fib(n):
        if n in (0, 1):
            return n
        return lru_cache_fib(n - 1) + lru_cache_fib(n - 2)

    @memoize
    def memo_fib(n):
        if n in (0, 1):
            return n
        return memo_fib(n - 1) + memo_fib(n - 2)

    @memoize(cache_exceptions=True)
    def memo_fib_non_lru(n):
        if n in (0, 1):
            return n
        return memo_fib_non_lru(n - 1) + memo_fib_non_lru(n - 2)

    def non_memo_fib(n):
        if n in (0, 1):
            return n
        return non_memo_fib(n - 1) + non_memo_fib(n - 2)

    # This takes a really long time!
    # start_time = time.time()
    # for _ in range(num_iters):
    #     non_memo_fib(fib_num)
    # end_time = time.time() - start_time
    # print(f"Non-memoized fib average time (ms): {end_time/num_iters * 1000}")

    start_time = time.time()
    for _ in range(num_iters):
        simp_memo_fib(fib_num)
    end_time = time.time() - start_time
    print(f"@simplified_memoize fib average time (ms): {end_time/num_iters * 1000}")

    start_time = time.time()
    for _ in range(num_iters):
        memo_fib(fib_num)
    end_time = time.time() - start_time
    print(f"@memoize fib average time (ms): {end_time / num_iters * 1000}")

    start_time = time.time()
    for _ in range(num_iters):
        memo_fib_non_lru(fib_num)
    end_time = time.time() - start_time
    print(f"@memoize(cache_exceptions=True) (to avoid delegation to functools.lru_cache) fib average time (ms): "
          f"{end_time / num_iters * 1000}")

    start_time = time.time()
    for _ in range(num_iters):
        lru_cache_fib(fib_num)
    end_time = time.time() - start_time
    print(f"@functools.lru_cache fib average time (ms): {end_time/num_iters * 1000}")


if __name__ == "__main__":
    benchmark_memoized_class_simple()
    benchmark_fib()
