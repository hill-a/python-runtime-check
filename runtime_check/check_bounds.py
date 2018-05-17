import operator

import numpy as np

from runtime_check.check_type import TypeChecker


class _BoundCheckerMeta(type):
    @classmethod
    def _in_bounds(mcs, a, key):
        TypeChecker.scalar(a)
        if len(key) == 2:
            TypeChecker.scalar(key[0])
            TypeChecker.scalar(key[1])
            return key[0] <= a <= key[1]
        elif len(key) == 3 and len(key[2]) == 2:
            TypeChecker.scalar(key[0])
            TypeChecker.scalar(key[1])
            TypeChecker[bool](key[2][0])
            TypeChecker[bool](key[2][1])
            return (operator.le if key[2][0] else operator.lt)(key[0], a) and \
                   (operator.le if key[2][1] else operator.lt)(a, key[1])
        else:
            raise ValueError("The bound tuple can be of structure: (Lower_bound, Upper_bound, (Include_lower_bound, " +
                          "Include_upper_bound)) or (Lower_bound, Upper_bound)")

    @classmethod
    def _validater(mcs, key):
        def check(a):
            if isinstance(key, list) or isinstance(key, tuple) and all([isinstance(k, tuple) for k in key]):
                valid = any([mcs._in_bounds(a, k) for k in key])
            else:
                valid = mcs._in_bounds(a, key)
            if not valid:
                raise ValueError("Number out of bounds {}, expected bounds {}".format(a, key))

        return check

    def __getitem__(cls, key):
        return cls._validater(key)


class BoundChecker(object, metaclass=_BoundCheckerMeta):
    """
    BoundChecker[(0,1)](0.5)
    BoundChecker.positive(100)

    the tuple defining the bounds are (Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))
        or (Lower_bound, Upper_bound)
    You may use lists of bounds to define discontinuous bounds
    """

    @classmethod
    def positive(cls, a):
        cls._validater((0, np.inf))(a)

    @classmethod
    def negative(cls, a):
        cls._validater((-np.inf, 0))(a)

    @classmethod
    def positive_not_zero(cls, a):
        cls._validater((0, np.inf, (False, True)))(a)

    @classmethod
    def negative_not_zero(cls, a):
        cls._validater((-np.inf, 0, (True, False)))(a)

    @classmethod
    def probability(cls, a):
        cls._validater((0, 1))(a)
