from inspect import signature
from collections import Iterable
from functools import wraps

from runtime_check.check_type import Type_checker
from runtime_check.check_bounds import Bound_checker

def enforce_annotations(func):
    """
    @enforce_annotations
    def hello(a: [Bound_checker[(0,1)], Type_checker[[int,float]]]):
        pass

    @enforce_annotations
    def hello(a: [Bound_checker[(0,1)], Type_checker[[int,float]]]) -> [Bound_checker[(0,1,(False, True))], Type_checker[float]]:
        return 0.2
    """
    sig = signature(func)
    ann = func.__annotations__
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            if name in ann:
                if isinstance(ann[name], Iterable):
                    valid = all([t(val) for t in ann[name]])
                else:
                    valid = ann[name](val)

        return_val = func(*args, **kwargs)
        if 'return' in ann:
            if isinstance(ann['return'], Iterable):
                valid = all([t(return_val) for t in ann['return']])
            else:
                valid = ann['return'](return_val)
        return return_val
    return wrapper

def check_bound_at_run(func): 
    """
    @check_bound_at_run
    def hello(a: [(float('-inf'), -1), (0, 1),(2, float('+inf'))]):
        pass

    @check_bound_at_run
    def hello(a: (0, 1)):
        pass

    @check_bound_at_run
    def hello(a: (0, float('+inf'),(False, True)), b: (0, 1)) -> (0,100):
        if a < (b * 100):
            b * 100
        else:
            min(a, 100)

    the tuple defining the bounds are (Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))
        or (Lower_bound, Upper_bound)
    You may use lists of bounds to define discontinuous bounds
    """
    sig = signature(func)
    ann = func.__annotations__
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            if name in ann:
                if isinstance(ann[name], Iterable):
                    valid = any([Bound_checker._in_bounds(val, key) for key in ann[name]])
                else:
                    valid = Bound_checker._in_bounds(val, ann[name])
                assert valid, "Number out of bounds {}, expected bounds {}".format(val, ann[name])

        return_val = func(*args, **kwargs)
        if 'return' in ann:
            if isinstance(ann['return'], Iterable):
                valid = any([Bound_checker._in_bounds(return_val, key) for key in ann['return']])
            else:
                valid = Bound_checker(return_val, ann['return'])
            assert valid, "Number out of bounds {}, expected bounds {}".format(return_val, ann['return'])
        return return_val
    return wrapper

def check_type_at_run(func):
    """
    @check_type_at_run
    def hello(a: [int,float]):
        pass

    @check_type_at_run
    def hello(a: int):
        pass

    @check_type_at_run
    def hello(a: int, b: str, c: [list, type(None)] = []) -> [int, str]:
        if c is None:
            return b
        else: 
            return a

    you may use list of types to allow multiple types
    """
    sig = signature(func)
    ann = func.__annotations__
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            if name in ann:
                if isinstance(ann[name], Iterable):
                    valid = any([isinstance(val, t) for t in ann[name]])
                else:
                    valid = isinstance(val, ann[name])
                assert valid, 'Expected {} for argument {}, got {}'.format(ann[name], name, val.__class__)

        return_val = func(*args, **kwargs)
        if 'return' in ann:
            if isinstance(ann['return'], Iterable):
                valid = any([isinstance(return_val, t) for t in ann['return']])
            else:
                valid = isinstance(return_val, ann['return'])
            assert valid, 'Expected {} for return, got {}'.format(ann['return'], return_val.__class__)
        return return_val
    return wrapper