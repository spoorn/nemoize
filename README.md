# nemoize
Simple Python Memoizer for classes, functions, and methods.

# How to Use
This isn't published to PyPi or anything, just a little fun coding.  You can try it out by pulling the code in locally to your project and adding the `@memoize` decorator to classes, functions, and instance methods.

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
