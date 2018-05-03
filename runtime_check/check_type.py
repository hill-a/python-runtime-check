from collections import Iterable

import numpy as np

class _Type_checker_meta(type):
    @classmethod
    def _validater(cls, key):
        def check(a):
            if isinstance(key, Iterable):
                valid = any([isinstance(a, t) for t in key])
            else:
                valid = isinstance(a, key)
            assert valid, "Expected {}, got {}".format(key, a.__class__)
        return check

    def __getitem__(cls, key):
        return cls._validater(key)

class Type_checker(object, metaclass=_Type_checker_meta): 
    """
    Type_checker[int](0)
    Type_checker.array(numpy.arange(10))

    you may use list of types to allow multiple types
    """
    @classmethod
    def scalar(self, a):
        self._validater([int, float])(a)

    @classmethod
    def numpy_array(self, a):
        self._validater(np.ndarray)(a)

    @classmethod
    def array(self, a):
        self._validater([np.ndarray, Iterable])(a)