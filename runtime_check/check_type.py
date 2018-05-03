from collections import Iterable

import numpy as np

class _TypeCheckerMeta(type):
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

class TypeChecker(object, metaclass=_TypeCheckerMeta): 
    """
    TypeChecker[int](0)
    TypeChecker.array(numpy.arange(10))

    you may use list of types to allow multiple types
    """
    @classmethod
    def scalar(cls, a):
        cls._validater([int, float])(a)

    @classmethod
    def numpy_array(cls, a):
        cls._validater(np.ndarray)(a)

    @classmethod
    def array(cls, a):
        cls._validater([np.ndarray, Iterable])(a)