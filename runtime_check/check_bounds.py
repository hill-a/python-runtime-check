from collections import Iterable
import operator

import numpy as np

from runtime_check.check_type import TypeChecker

class _BoundCheckerMeta(type):
    @classmethod
    def _in_bounds(a, key):
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
                   (operator.le if key[2][1] else operator.lt)(key[1], a)
        else:
            assert False, "The bound tuple can be of structure: (Lower_bound, Upper_bound, (Include_lower_bound, " + \
                          "Include_upper_bound)) or (Lower_bound, Upper_bound)"

    @classmethod
    def _validater(cls, key):
        def check(a):
            TypeChecker.scalar(a)
            if isinstance(key, list):
                valid = any([_in_bounds(a, k) for k in key])
            else:
                valid = _in_bounds(a, key)
            assert valid, "Number out of bounds {}, expected bounds {}".format(a, key)
        return check

    def __getitem__(cls, key):
        return cls._validater(key)


class BoundChecker(object, metaclass=_BoundCheckerMeta): 
    """
    BoundChecker[(0,1)](0.5)
    BoundChecker.positif(100)

    the tuple defining the bounds are (Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))
        or (Lower_bound, Upper_bound)
    You may use lists of bounds to define discontinuous bounds
    """
    @classmethod
    def positif(self, a):
        self._validater((0,np.inf))(a)

    @classmethod
    def negatif(self, a):
        self._validater((-np.inf,0))(a)

    @classmethod
    def positif_not_zero(self, a):
        self._validater((0,np.inf,(False,True)))(a)

    @classmethod
    def negatif_not_zero(self, a):
        self._validater((-np.inf,0,(True, False)))(a)

    @classmethod
    def probability(self, a):
        self._validater((0,1))(a)
