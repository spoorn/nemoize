from src.memoize import memoize


def test_memoize_cached_object():
    @memoize
    class Test:
        def __init__(self, value):
            pass

    t1 = Test(0)
    t2 = Test(0)
    assert t1 == t2
    assert id(t1) == id(t2)

    t3 = Test(1)
    assert t1 != t3
    assert id(t1) != id(t3)


def test_memoize_no_init_args():
    @memoize
    class Test:
        def __init__(self):
            pass

    t1 = Test()
    t2 = Test()
    assert t1 == t2
    assert id(t1) == id(t2)


def test_memoize_simple():
    @memoize
    class Test:
        values = []

        def __init__(self, value):
            Test.values.append(value)

    _assert_counter_and_values(Test, 0, [0])
    _assert_counter_and_values(Test, 1, [0, 1])
    _assert_counter_and_values(Test, 0, [0, 1])
    _assert_counter_and_values(Test, 1, [0, 1])


def test_memoize_max_size_eviction():
    @memoize(max_size=3)
    class Test:
        values = []

        def __init__(self, value):
            Test.values.append(value)

    _assert_counter_and_values(Test, 0, [0])
    _assert_counter_and_values(Test, 1, [0, 1])
    _assert_counter_and_values(Test, 2, [0, 1, 2])
    _assert_counter_and_values(Test, 2, [0, 1, 2])
    # Adding 0, 1, and 2 should fetch cached versions and have no change to Test
    _assert_counter_and_values(Test, 0, [0, 1, 2])
    _assert_counter_and_values(Test, 1, [0, 1, 2])
    _assert_counter_and_values(Test, 2, [0, 1, 2])
    # Adding 3 should create a new Test and evict 0, the LRU Test object, so adding 0 should re-add it
    _assert_counter_and_values(Test, 3, [0, 1, 2, 3])
    _assert_counter_and_values(Test, 0, [0, 1, 2, 3, 0])
    # Then adding a 2 should NOT change anything as the cache now has [2, 3, 0]
    _assert_counter_and_values(Test, 2, [0, 1, 2, 3, 0])
    # Then adding a 1 should evict the 3 which is now the LRU, so subsequently adding 3 will create a new Object
    _assert_counter_and_values(Test, 1, [0, 1, 2, 3, 0, 1])
    _assert_counter_and_values(Test, 3, [0, 1, 2, 3, 0, 1, 3])


def test_memoize_cache_exceptions_true():
    @memoize(cache_exceptions=True)
    class Test:
        values = []

        def __init__(self, value):
            raise Exception("Test")

    try:
        Test(0)
    except Exception as e1:
        try:
            Test(0)
        except Exception as e2:
            assert e1 == e2
            assert id(e1) == id(e2)


def test_memoize_cache_exceptions_false():
    @memoize(cache_exceptions=False)
    class Test:
        values = []

        def __init__(self, value):
            raise Exception("Test")

    try:
        Test(0)
    except Exception as e1:
        try:
            Test(0)
        except Exception as e2:
            assert e1 != e2
            assert str(e1) == str(e2)
            assert id(e1) != id(e2)


def test_memoize_cache_exceptions_true_with_max_size():
    @memoize(max_size=2, cache_exceptions=True)
    class Test:
        values = []

        def __init__(self, value):
            raise Exception("Test")

    try:
        Test(0)
    except Exception as e1:
        try:
            Test(0)
        except Exception as e2:
            # Exception should have been cached
            assert e1 == e2
            assert id(e1) == id(e2)

            try:
                Test(1)
            except Exception as e3:
                # New exception, not cached
                assert e1 != e3
                assert id(e1) != id(e3)

                try:
                    Test(2)
                except Exception as e4:
                    # New exception again, not cached, but evicts Test(0)
                    assert e3 != e4
                    assert str(e3) == str(e4)
                    assert id(e3) != id(e4)

                    try:
                        Test(0)
                    except Exception as e5:
                        # Validate Test(0) creats a new object since it was evicted
                        assert e1 != e5
                        assert str(e1) == str(e5)
                        assert id(e1) != id(e5)


def test_memoize_isinstance():
    @memoize
    class Test:
        def __init__(self):
            pass

    t1 = Test()
    assert isinstance(t1, Test)


def test_memoize___name__attribute_preserved():
    @memoize
    class Test:
        def __init__(self):
            pass

    assert Test.__name__ == "Test"


def test_static_method_preserved():
    @memoize
    class Test:
        def __init__(self):
            pass

        @staticmethod
        def echo():
            return "echo"

    assert Test.echo() == "echo"
    assert Test().echo() == "echo"


def test_memoize_function():
    counter = 0

    @memoize
    def test_func():
        nonlocal counter
        counter += 1

    test_func()
    assert counter == 1
    test_func()
    assert counter == 1


def test_memoize_method():
    class Test:
        def __init__(self):
            self.counter = 0
            pass

        @memoize(max_size=5)
        def test_method(self):
            self.counter += 1

    t1 = Test()
    t1.test_method()
    assert t1.counter == 1
    t1.test_method()
    assert t1.counter == 1


def _assert_counter_and_values(cls, arg, values):
    cls(arg)
    assert cls.values == values