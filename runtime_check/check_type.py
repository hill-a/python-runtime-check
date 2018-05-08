from typing import List, Union, Dict, Tuple, Any, Set, TypeVar, Callable, Mapping, Iterator, Iterable

import numpy as np

DEEP = False

class _TypeCheckerMeta(type):
    @classmethod
    def _check_type(mcs, key, a): #TODO: add the remainding typing objects (generator, ...)
        if key == Any:
            return True
        elif type(key) == type(Union):
            return any([mcs._check_type(k, a) for k in key.__args__])
        elif isinstance(key, TypeVar):
            return any([mcs._check_type(k, a) for k in key.__constraints__])
        elif issubclass(key, List):
            valid = isinstance(a, List)
            if DEEP and valid:
                return all([mcs._check_type(key.__args__[0], val) for val in a])
            else:
                return valid
        elif issubclass(key, Set):
            valid = isinstance(a, Set)
            if DEEP and valid:
                return all([mcs._check_type(key.__args__[0], val) for val in a])
            else:
                return valid
        elif issubclass(key, Dict):
            valid = isinstance(a, Dict)
            if DEEP and valid:
                return all([mcs._check_type(key.__args__[0], k) and 
                            mcs._check_type(key.__args__[1], val) for (k, val) in a.items()])
            else:
                return valid
        elif issubclass(key, Tuple):
            valid = isinstance(a, Tuple) and len(key.__args__) == len(a)
            if DEEP and valid:
                return all([mcs._check_type(k, val) for k, val in zip(key.__args__, a)])
            else:
                return valid
        elif type(key) == type(Callable): # will not do in depth checking, only shallow.
            return callable(a)
        elif issubclass(key, Mapping): # will not do in depth checking, only shallow.
            return isinstance(a, map)
        elif issubclass(key, Iterator): # will not do in depth checking, only shallow.
            return isinstance(a, Iterator)
        elif key == type(None) or key == None:
            return a is None
        elif a is None:
            return False
        else:
            try:
                return isinstance(a, key)
            except:
                print("Error: occured when comparing {} to class {}".format(a, key))

    @classmethod
    def _validater(cls, key):
        def check(a):
            assert cls._check_type(key, a), "Expected {}, got {}".format(key, a.__class__)
        return check

    def __getitem__(cls, key):
        if isinstance(key, (Tuple, List, Set)):
            return cls._validater(Union[tuple(key)])
        else:
            return cls._validater(key)


class TypeChecker(object, metaclass=_TypeCheckerMeta): 
    """
    TypeChecker[int, float](0)
    TypeChecker.array(numpy.arange(10))

    you may use typing.Union[int, float] for mutliple valid types
    or List[int], Dict[str, int], Optional[int].
    """
    @classmethod
    def scalar(cls, a):
        cls._validater(Union[int, float])(a)

    @classmethod
    def numpy_array(cls, a):
        cls._validater(np.ndarray)(a)

    @classmethod
    def array(cls, a):
        cls._validater(Union[np.ndarray, Iterable])(a)