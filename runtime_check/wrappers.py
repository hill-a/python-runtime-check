from inspect import signature
from collections import Iterable
from functools import wraps

from runtime_check.check_bounds import BoundChecker
from runtime_check.check_type import TypeChecker


def enforce_annotations(func):
    """
    @enforce_annotations
    def hello(a: [BoundChecker[(0,1)], TypeChecker[int,float]]):
        pass

    @enforce_annotations
    def hello(a: [BoundChecker[(0,1)], TypeChecker[int,float]]) -> [BoundChecker[(0,1,(False, True))], TypeChecker[float]]:
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
                    for t in ann[name]:
                        t(val)
                else:
                    ann[name](val)

        return_val = func(*args, **kwargs)
        if 'return' in ann:
            if isinstance(ann['return'], Iterable):
                for t in ann['return']:
                    t(return_val)
            else:
                ann['return'](return_val)
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
            return b * 100
        else:
            return min(a, 100)

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
                if isinstance(ann[name], list):
                    valid = any([BoundChecker._in_bounds(val, key) for key in ann[name]])
                else:
                    valid = BoundChecker._in_bounds(val, ann[name])
                if not valid:
                    raise ValueError("Number out of bounds {}, expected bounds {}".format(val, ann[name]))

        return_val = func(*args, **kwargs)
        if 'return' in ann:
            if isinstance(ann['return'], list):
                valid = any([BoundChecker._in_bounds(return_val, key) for key in ann['return']])
            else:
                valid = BoundChecker._in_bounds(return_val, ann['return'])
            if not valid:
                raise ValueError("Number out of bounds {}, expected bounds {}".format(return_val, ann['return']))
        return return_val

    return wrapper


def check_type_at_run(func):
    """
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
    sig = signature(func)
    ann = func.__annotations__

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            if name in ann:
                if not TypeChecker._check_type(ann[name], val):
                    raise TypeError('Expected {} for argument {}, got {}'.format(ann[name], name, val.__class__))

        return_val = func(*args, **kwargs)
        if 'return' in ann:
            if not TypeChecker._check_type(ann['return'], return_val):
                raise TypeError('Expected {} for return, got {}'.format(ann['return'], return_val.__class__))
        return return_val

    return wrapper
