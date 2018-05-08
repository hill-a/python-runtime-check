from typing import Union, Any, Optional, List, Dict, Tuple

import numpy
import runtime_check
from runtime_check import check_type_at_run, TypeChecker, check_bound_at_run, BoundChecker, enforce_annotations

runtime_check.check_type.DEEP = True


def test_type_decorator_union():
    @check_type_at_run
    def check_union(a: Union[int, float]):
        return a + 100

    for val in ["", [1,2,""], (1,"",[]), {"a":1, 2:'b'}]:
        # these should fail
        try:
            print(val)
            check_union(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [0.0, 0, 1e10, -100, -1.0, 10, 1.0]:
        print(val)
        check_union(val)


def test_type_decorator_simple():
    @check_type_at_run
    def check_int(a: int):
        return str(a + 10)

    for val in ["", 0.0, [1,2,""], (1,"",[]), {"a":1, 2:'b'}]:
        # these should fail
        try:
            print(val)
            check_int(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [0, int(1e10), -100, 10]:
        print(val)
        check_int(val)

def test_type_decorator_complex():
    @check_type_at_run
    def check_complex(a, b: str, c: Optional[List[Any]] = []) -> Union[int, str]:
        if c is None:
            return b
        else: 
            return a

    for val in [(0,0), (0,"",(1,)), (0,0,[]), ([], ""), (0.0, "")]:
        # these should fail
        try:
            print(val)
            check_complex(*val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [(0,""), (0,"",[1]), (0,"",[["a"], (1,)]), ([["a"], (1,)], "", None)]:
        print(val)
        check_complex(*val)



def test_type_union():
    for val in ["", [1,2,""], (1,"",[]), {"a":1, 2:'b'}]:
        # these should fail
        try:
            print(val)
            TypeChecker[int, float](val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
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
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [(0, 0.0, ""), (10, 100.0, "hello"), (-10, -1.0, "world")]:
        print(val)
        TypeChecker[Tuple[int, float, str]](val)

def test_type_dict():
    for val in [0, 0.0, [], "", (0,), {"hi":"bob"}, {"hi":0.0}, {0:0}, {"hi":0, 1:"world"}, {"hi":0, None:0}, {"hi":0, "world":None}]:
        # these should fail
        try:
            print(val)
            TypeChecker[Optional[Dict[str, int]]](val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [{}, {"str":0}, {"hello":0, "world":1}]:
        print(val)
        TypeChecker[Optional[Dict[str, int]]](val)

def test_type_array():
    for val in [0, 0.0, "", (0,), {}, float("nan")]:
        # these should fail
        try:
            print(val)
            TypeChecker.array(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [[], ["hello", 0, (1,), [], {}], list(range(1000)), numpy.arange(1000)]:
        print(val)
        TypeChecker.array(val)


def test_bounds_decorator_discontinuous():
     # a must be between ]-inf, 1] or [0, 1] or [2, +inf[
    @check_bound_at_run
    def check_discontinuous(a: [(float('-inf'), -1), (0, 1), (2, float('+inf'))]):
        return a + 0.1

    for val in [-0.5, 0.5, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            check_discontinuous(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [-1000, -100.0, -1, 0.0, 1.0, 2, 20000]:
        print(val)
        check_discontinuous(val)

def test_bounds_decorator_simple():
     # a must be between [0,1]
    @check_bound_at_run
    def check_simple(a: (0, 1)):
        return a + 0

    for val in [-10, 1000, -100.0, 1000.2, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            check_simple(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [0, 0.0, 0.5, 1, 1.0]:
        print(val)
        check_simple(val)


def test_bounds_decorator_return():
     # return must be between [0,1]
    @check_bound_at_run
    def check_return(a) -> (0,1):
        return a

    for val in [-10, 1000, -100.0, 1000.2, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            check_return(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [0, 0.0, 0.5, 1, 1.0]:
        print(val)
        check_return(val)

def test_bounds_decorator_complex():
     # a must be between ]0, +inf[
     # b must be between [0, 1]
     # return must be between [0, 100]
    @check_bound_at_run
    def check_complex(a: (0, float('+inf'), (False, True)), b: (0, 1)) -> (0, 100):
        if a < (b * 100):
            return b * 100
        else:
            return min(a, 100)

    for val in [(0.0, 0), (0,0), (-10,0), (100, 1.000001), (10, -0.0001), ("",""), ((1,),(1,)), (None, None), ([], []), ({},{})]:
        # these should fail
        try:
            print(val)
            check_complex(*val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [(0.00001, 0), (1000, 1), (0.5, 0.5)]:
        print(val)
        check_complex(*val)

def test_bounds_discontinuous():
     # [0, 1] or [2, 4]

    for val in [-10000, -1, -1.0, 1.5, 5, 5.4, 10000, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            BoundChecker[(0, 1), (2, 4)](val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
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
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
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
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [0, 0.0, 50, 50.0, 99.9999999, 1e10000, float("inf")]:
        print(val)
        BoundChecker.positive(val)


def test_enforced_dual():
    @enforce_annotations
    def check_dual(a: [BoundChecker[(0, 1)], TypeChecker[int, float]]):
        return a + 0

    for val in [-10000, -1, -1.0, 1.001, 10, 100000, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            check_dual(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [0, 0.0, 0.5, 1.0, 1]:
        print(val)
        check_dual(val)

def test_enforced_simple():
    @enforce_annotations
    def check_simple(a: TypeChecker[str]):
        return a + ""

    for val in [0, 0.0, (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            check_simple(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in ["hello", 'world']:
        print(val)
        check_simple(val)

def test_enforced_complex():
    @enforce_annotations
    def check_complex(a: [BoundChecker[(0, 1)], TypeChecker[int, float]]) -> [BoundChecker[(0, 1, (False, True))], TypeChecker[float]]:
        return 0.2 * a 

    for val in [-10000, -1, -1.0, 1.001, 10, 100000, 0, "", (1,), None, [], {}, float("nan")]:
        # these should fail
        try:
            print(val)
            check_complex(val)
            assert False, "Error: {} should not be valid".format(val)
        except AssertionError:
            pass

    print()
    for val in [0.000001, 0.5, 1.0, 1]:
        print(val)
        check_complex(val)