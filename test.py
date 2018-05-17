"""
Test code
"""
from typing import Union, Any, Optional, List, Dict, Tuple, TypeVar, Set, Callable, Iterator, Mapping

import numpy

import runtime_check
from runtime_check import check_type_at_run, TypeChecker, check_bound_at_run, BoundChecker, enforce_annotations

runtime_check.check_type.DEEP = True


def test_type_decorator_union():
    """
    test type decorator union
    """
    @check_type_at_run
    def _check_union(val_a: Union[int, float]):
        return val_a + 100

    for val in ["", [1, 2, ""], (1, "", []), {"a": 1, 2: 'b'}]:
        # these should fail
        try:
            print(val)
            _check_union(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in [0.0, 0, 1e10, -100, -1.0, 10, 1.0]:
        print(val)
        _check_union(val)


def test_type_decorator_simple():
    """
    test type decorator simple
    """
    @check_type_at_run
    def _check_int(val_a: int):
        return str(val_a + 10)

    for val in ["", 0.0, [1, 2, ""], (1, "", []), {"a": 1, 2: 'b'}]:
        # these should fail
        try:
            print(val)
            _check_int(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in [0, int(1e10), -100, 10]:
        print(val)
        _check_int(val)

def test_type_decorator_complex():
    """
    test type decorator complex
    """
    @check_type_at_run
    def _check_complex(val_a, val_b: str, val_c: Optional[List[Any]] = None) -> Union[int, str]:
        if val_c is not None:
            return val_b
        else:
            return val_a

    for val in [(0, 0), (0, "", (1,)), (0, 0, None), ([], ""), (0.0, "")]:
        # these should fail
        try:
            print(val)
            _check_complex(*val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in [(0, ""), (0, "", None), (0, "", None), ([["a"], (1,)], "", [["a"], (1,)])]:
        print(val)
        _check_complex(*val)



def test_type_union():
    for val in ["", [1, 2, ""], (1, "", []), {"a": 1, 2: 'b'}]:
        # these should fail
        try:
            print(val)
            TypeChecker[int, float](val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in [0.0, 0, 1e10, -100, -1.0, 10, 1.0]:
        print(val)
        TypeChecker[int, float](val)

def test_type_tuple():
    for val in [0, 0.0, [], None, "", {}, (0.0, 0.0, ""), (0, 0, ""), (0, 0.0, 0), (None, 0.0, ""), (0, None, ""), (0, 0.0, None), (1,), (1, 1.0), (1, 1.0, "", 0)]:
        # these should fail
        try:
            print(val)
            TypeChecker[Tuple[int, float, str]](val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in [(0, 0.0, ""), (10, 100.0, "hello"), (-10, -1.0, "world")]:
        print(val)
        TypeChecker[Tuple[int, float, str]](val)

def test_type_dict():
    for val in [0, 0.0, [], "", (0,), {"hi": "bob"}, {"hi": 0.0}, {0: 0}, {"hi": 0, 1: "world"}, {"hi": 0, None: 0}, {"hi": 0, "world": None}]:
        # these should fail
        try:
            print(val)
            TypeChecker[Optional[Dict[str, int]]](val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in [{}, {"str": 0}, {"hello": 0, "world": 1}]:
        print(val)
        TypeChecker[Optional[Dict[str, int]]](val)

def test_type_array():
    for val in [0, 0.0, float("nan")]:
        # these should fail
        try:
            print(val)
            TypeChecker.iterable(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in [[], ["hello", 0, (1,), [], {}], list(range(1000)), numpy.arange(1000)]:
        print(val)
        TypeChecker.iterable(val)


def test_bounds_decorator_discontinuous():
     # val_a must be between ]-inf, 1] or [0, 1] or [2, +inf[
    @check_bound_at_run
    def _check_discontinuous(val_a: [(float('-inf'), -1), (0, 1), (2, float('+inf'))]):
        return val_a + 0.1

    for val in [-0.5, 1.5, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            _check_discontinuous(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [-1000, -100.0, -1, 0.0, 0.5, 1.0, 2, 20000]:
        print(val)
        _check_discontinuous(val)

def test_bounds_decorator_simple():
     # val_a must be between [0,1]
    @check_bound_at_run
    def _check_simple(val_a: (0, 1)):
        return val_a + 0

    for val in [-10, 1000, -100.0, 1000.2, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            _check_simple(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [0, 0.0, 0.5, 1, 1.0]:
        print(val)
        _check_simple(val)


def test_bounds_decorator_return():
     # return must be between [0,1]
    @check_bound_at_run
    def _check_return(val_a) -> (0,1):
        return val_a

    for val in [-10, 1000, -100.0, 1000.2, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            _check_return(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [0, 0.0, 0.5, 1, 1.0]:
        print(val)
        _check_return(val)

def test_bounds_decorator_complex():
     # val_a must be between ]0, +inf[
     # val_b must be between [0, 1]
     # return must be between [0, 100]
    @check_bound_at_run
    def _check_complex(val_a: (0, float('+inf'), (False, True)), val_b: (0, 1)) -> (0, 100):
        if val_a < (val_b * 100):
            return val_b * 100
        else:
            return min(val_a, 100)

    for val in [(0.0, 0), (0, 0), (-10, 0), (100, 1.000001), (10, -0.0001), ("", ""), ((1,), (1,)), (None, None), ([], []), ({}, {})]:
        # these should fail
        try:
            print(val)
            _check_complex(*val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [(0.00001, 0), (1000, 1), (0.5, 0.5)]:
        print(val)
        _check_complex(*val)

def test_bounds_discontinuous():
     # [0, 1] or [2, 4]

    for val in [-10000, -1, -1.0, 1.5, 5, 5.4, 10000, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            BoundChecker[(0, 1), (2, 4)](val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [0, 0.0, 0.5, 1, 1.0, 2, 2.0, 3, 4, 4.0]:
        print(val)
        BoundChecker[(0, 1), (2, 4)](val)

def test_bounds_simple():
     # [0, 100[

    for val in [-10000, -1, -1.0, 100, 100.0, 10000, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            BoundChecker[(0, 100, (True, False))](val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [0, 0.0, 50, 50.0, 99.9999999]:
        print(val)
        BoundChecker[(0, 100, (True, False))](val)

def test_bounds_positive():
     # [0, +inf[

    for val in [-10000, -1, -1.0, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            BoundChecker.positive(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [0, 0.0, 50, 50.0, 99.9999999, 1e10000, float("inf")]:
        print(val)
        BoundChecker.positive(val)


def test_enforced_dual():
    @enforce_annotations
    def _check_dual(val_a: [BoundChecker[(0, 1)], TypeChecker[int, float]]):
        return val_a + 0

    for val in [-10000, -1, -1.0, 1.001, 10, 100000, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            _check_dual(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [0, 0.0, 0.5, 1.0, 1]:
        print(val)
        _check_dual(val)

def test_enforced_simple():
    @enforce_annotations
    def _check_simple(val_a: TypeChecker[str]):
        return val_a + ""

    for val in [0, 0.0, (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            _check_simple(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass

    print()
    for val in ["hello", 'world']:
        print(val)
        _check_simple(val)

def test_enforced_complex():
    @enforce_annotations
    def _check_complex(val_a: [BoundChecker[(0, 1)], TypeChecker[int, float]]) -> [BoundChecker[(0, 1, (False, True))], TypeChecker[float]]:
        return 0.2 * val_a

    for val in [-10000, -1, -1.0, 1.001, 10, 100000, 0, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            _check_complex(val)
            raise EnvironmentError("Error: {} should not be valid".format(val))
        except TypeError:
            pass
        except ValueError:
            pass

    print()
    for val in [0.000001, 0.5, 1.0, 1]:
        print(val)
        _check_complex(val)


def test_check_bounds_coverage():
    BoundChecker.positive(1)
    BoundChecker.negative(-1)
    BoundChecker.positive_not_zero(1)
    BoundChecker.negative_not_zero(-1)
    BoundChecker.probability(0.5)

    try:
        BoundChecker[(0, 1, 0)](0.5)
    except ValueError:
        pass


def test_check_type_coverage():
    TypeChecker[TypeVar('s', int, float)](1)
    TypeChecker[Set]({1})
    TypeChecker[Set[int]]({1})

    TypeChecker[Callable](lambda a : 1)
    TypeChecker[Mapping](map(lambda x: x+1, [1, 2, 3]))
    TypeChecker[Iterator]([1, 2, 3].__iter__())

    TypeChecker.numpy_array(numpy.ones(10))


def test_check_wrapper_coverage():
    @enforce_annotations
    def _enforce_simple_return(val_a) -> TypeChecker[str]:
        return val_a

    _enforce_simple_return("")

    @check_bound_at_run
    def _check_discontinuous_return(val_a: (0, float('+inf'), (False, True)), val_b: (0, 1)) -> [(0, 100), (200, 300)]:
        if val_a < (val_b * 100):
            return val_b * 100
        else:
            return min(val_a, 100)

    _check_discontinuous_return(100, 0.5)
