"""
This module is used for type checking
"""

from typing import List, Union, Dict, Tuple, Any, Set, TypeVar, Callable, Mapping, Iterator, Iterable

import numpy as np

DEEP = False

class _TypeCheckerMeta(type):
    """
    Meta class used for the TypeChecker[] notation, also contains the checking code.
    """

    @classmethod
    def _check_type(mcs, key, val): #TODO: add the remainding typing objects (generator, ...)
        """
        Checks whether a value is of a specific type.

        :param val: (Any)
        :param key: (Type or Typing object)
        :return: (bool) is of type
        """
        if key == Any:
            return True
        elif type(key) == type(Union):
            return any([mcs._check_type(k, val) for k in key.__args__])
        elif isinstance(key, TypeVar):
            return any([mcs._check_type(k, val) for k in key.__constraints__])
        elif issubclass(key, List):
            valid = isinstance(val, List)
            if DEEP and valid and key.__args__ is not None:
                return all([mcs._check_type(key.__args__[0], v) for v in val])
            else:
                return valid
        elif issubclass(key, Set):
            valid = isinstance(val, Set)
            if DEEP and valid and key.__args__ is not None:
                return all([mcs._check_type(key.__args__[0], v) for v in val])
            else:
                return valid
        elif issubclass(key, Dict):
            valid = isinstance(val, Dict)
            if DEEP and valid and key.__args__ is not None:
                return all([mcs._check_type(key.__args__[0], k) and
                            mcs._check_type(key.__args__[1], v) for (k, v) in val.items()])
            else:
                return valid
        elif issubclass(key, Tuple):
            valid = isinstance(val, Tuple) and (key.__args__ is None or len(key.__args__) == len(val))
            if DEEP and valid and  key.__args__ is not None:
                return all([mcs._check_type(k, v) for k, v in zip(key.__args__, val)])
            else:
                return valid
        elif type(key) == type(Callable): # will not do in depth checking, only shallow.
            return callable(val)
        elif issubclass(key, Mapping): # will not do in depth checking, only shallow.
            return isinstance(val, map)
        elif issubclass(key, Iterator): # will not do in depth checking, only shallow.
            return isinstance(val, Iterator)
        elif key == type(None) or key == None:
            return val is None
        elif val is None:
            return False
        else:
            try:
                return isinstance(val, key)
            except Exception as ex: # pragma: no cover
                print("Error: occured when comparing {} to class {}".format(val, key))
                raise ex

    @classmethod
    def _validater(mcs, key):
        """
        Returns a checking function that checks that a value in allowed by key.

        :param key: (Type or Typing object)
        :retrun: (callable) function that takes value and will raise an error if not valid
        """
        def check(val):
            """
            Checks that val is valid, will raise an error if not valid.

            :param val: (Any)
            """
            if not cls._check_type(key, val):
                raise TypeError("Expected {}, got {}".format(key, val.__class__))
        return check

    def __getitem__(mcs, key):
        if isinstance(key, (Tuple, List, Set)):
            return cls._validater(Union[tuple(key)])
        else:
            return cls._validater(key)


class TypeChecker(object, metaclass=_TypeCheckerMeta):
    """
    Class used to check whether a value is of a specific type.

    ex:
        TypeChecker[int, float](0)
        TypeChecker.array(numpy.arange(10))

    you may use typing.Union[int, float] for mutliple valid types
    or List[int], Dict[str, int], Optional[int].
    """

    @classmethod
    def scalar(cls, val):
        """
        Checks whether val is a number.
        """
        cls._validater(Union[int, float])(val)

    @classmethod
    def numpy_array(cls, val):
        """
        Checks whether val is a numpy array.
        """
        cls._validater(np.ndarray)(val)

    @classmethod
    def iterable(cls, val):
        """
        Checks whether val is an Iterable.
        """
        cls._validater(Union[np.ndarray, Iterable])(val)
