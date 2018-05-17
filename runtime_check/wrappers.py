"""
This module containes the wrappers used in the library
"""

from inspect import signature
from collections import Iterable
from functools import wraps

from runtime_check.check_bounds import BoundChecker
from runtime_check.check_type import TypeChecker


def _checking_annotations(func, pre_check, post_check):
    """
    Takes a pre checker, a function and a post checker and runs them in order.

    :param func: (callable) the function you want to check
    :param pre_check: (callable) the check you want to run before execution
    :param post_check: (callable) the check you want to run after execution
    """
    sig = signature(func)
    ann = func.__annotations__

    @wraps(func)
    def _wrapper(*args, **kwargs):
        """
        A simple wrapper for the checking of a function
        """
        bound = sig.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            if name in ann:
                pre_check(ann[name], val, name)

        return_val = func(*args, **kwargs)
        if 'return' in ann:
            post_check(ann['return'], return_val)
        return return_val

    return _wrapper



def enforce_annotations(func):
    """
    An annotation used to enforce callable functions on the associated variable

    ex:
        @enforce_annotations
        def hello(a: [BoundChecker[(0,1)], TypeChecker[int,float]]):
            pass

        @enforce_annotations
        def hello(a: [BoundChecker[(0,1)], TypeChecker[int,float]]) -> [BoundChecker[(0,1,(False, True))]]:
            return 0.2
    """
    def _pre_check(annotated, val, name):
        if isinstance(annotated, Iterable):
            for ann in annotated:
                ann(val)
        else:
            annotated(val)

    def _post_check(annotated, val):
        if isinstance(annotated, Iterable):
            for ann in annotated:
                ann(val)
        else:
            annotated(val)

    return _checking_annotations(func, _pre_check, _post_check)


def check_bound_at_run(func):
    """
    Annotation used to enforce bounds on the associated variable

    ex:
        @check_bound_at_run
        def hello(a: [(float('-inf'), -1), (0, 1),(2, float('+inf'))]):
            pass

        @check_bound_at_run
        def hello(a: (0, 1)):
            pass

        @check_bound_at_run
        def hello(a: (0, float('+inf'),(False, True)), b: (0, 1)) -> (0,100):
            if a < (b * 100):
                return b * 100
            else:
                return min(a, 100)

    the tuple defining the bounds are (Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))
        or (Lower_bound, Upper_bound)
    You may use lists of bounds to define discontinuous bounds
    """

    def _pre_check(annotated, val, name):
        if isinstance(annotated, list):
            valid = any([BoundChecker._in_bounds(val, key) for key in annotated])
        else:
            valid = BoundChecker._in_bounds(val, annotated)
        if not valid:
            raise ValueError("Number out of bounds {} for argument {}, expected bounds {}".format(val, name, annotated))

    def _post_check(annotated, val):
        if isinstance(annotated, list):
            valid = any([BoundChecker._in_bounds(val, key) for key in annotated])
        else:
            valid = BoundChecker._in_bounds(val, annotated)
        if not valid:
            raise ValueError("Number out of bounds {} for return, expected bounds {}".format(val, annotated))

    return _checking_annotations(func, _pre_check, _post_check)


def check_type_at_run(func):
    """
    Annotation used to check the type of an associated variable

    ex:
        @check_type_at_run
        def hello(a: Union[int, float]):
            pass

        @check_type_at_run
        def hello(a: int):
            pass

        @check_type_at_run
        def hello(a: int, b: str, c: Optional[List[Any]] = []) -> Union[int, str]:
            if c is None:
                return b
            else:
                return a

    you may use typing.Union[int, float] for mutliple valid types
    or List[int], Dict[str, int], Optional[int].
    """
    def _pre_check(annotated, val, name):
        if not TypeChecker._check_type(annotated, val):
            raise TypeError('Expected {} for argument {}, got {}'.format(annotated, name, val.__class__))

    def _post_check(annotated, val):
        if not TypeChecker._check_type(annotated, val):
            raise TypeError('Expected {} for return, got {}'.format(annotated, val.__class__))

    return _checking_annotations(func, _pre_check, _post_check)

