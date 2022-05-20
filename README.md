# nemoize
Simple Python Memoizer decorator for classes, functions, and methods.

# Installation
nemoize is available on PyPi

```commandline
python3 -m pip install nemoize
```

Or you can install manually via the built distribution (wheel)/source dist from [PyPi](pypi.org/project/nemoize) or [github](https://github.com/spoorn/nemoize).


# How to Use

Import

```python
from nemoize import memoize
```

Then use the `@memoize` decorator on various entities as seen below

### Using on a Class

```python
@memoize
class Test:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
```

### Using on a function

```python
@memoize
def test_func():
    return "hoot"
```

### Using on an instance method

```python
class Owl:
    def __init__(self):
        self.food = 1337
        pass

    @memoize(max_size)
    def eat(self, num):
        self.food -= num
```

## Configuration

There are also various configuration parameters to `memoize()`:

- `@memoize(max_size=13)` : Max number of entries to keep in the cache: 
- `@memoize(cache_exceptions=True)` : Also cache exceptions, so any raised Exceptions will be the exact same Exception instance: 
- `@memoize(max_size=13, cache_exceptions=True)` : Together
- `@memoize(arg_hash_function=str)` : Changes the hash function on arg and each keyword-arg to use the str() function, which can make lists "hashable"

# Testing
The unit tests in `test/unit/test_memoize.py` run through various use cases of using the @memoize annotation on classes, functions, and instance methods.

# Benchmarking
There is a benchmarking utility under [`benchmark/`](https://github.com/spoorn/nemoize/tree/main/benchmark) that is used for benchmarking nemoize performance against other options and non-memoized scenarios.

Example numbers:

```commandline
Benchmark test for Memoized vs Non-memoized classes with [1000] computations in their__init__() methods for [1000000] iterations
Non-memoized class creation + empty method call average time (ms): 0.01550699806213379
Memoized class creation + empty method call average time (ms): 0.0012589995861053468

Benchmark test for @memoize, non-memoized, a @simplified_memoize, and @functools.lru_cache comparison usingfunction calculating fibonacci sum for [100] fib numbers, for [10000000] iterations
@simplified_memoize fib average time (ms): 0.0001555999994277954
@memoize fib average time (ms): 4.4699978828430175e-05
@memoize(cache_exceptions=True) (to avoid delegation to functools.lru_cache) fib average time (ms): 0.00034309999942779544
@functools.lru_cache fib average time (ms): 4.440000057220459e-05
```