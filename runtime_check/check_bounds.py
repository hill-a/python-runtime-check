"""
This module is used for bound checking on numbers
"""

import operator

import numpy as np

from runtime_check.check_type import TypeChecker


class _BoundCheckerMeta(type):
    """
    Meta class used for the BoundChecker[] notation, also contains the checking code.
    """

    @classmethod
    def _in_bounds(mcs, val, key):
        """
        Checks whether a value in within specific bounds.

        :param val: (int, float)
        :param key: (tuples) (Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))
                             or (Lower_bound, Upper_bound)
        :return: (bool) is in bounds
        """
        TypeChecker.scalar(val)
        if isinstance(key, tuple) and len(key) == 2:
            TypeChecker.scalar(key[0])
            TypeChecker.scalar(key[1])
            return key[0] <= val <= key[1]
        elif isinstance(key, tuple) and len(key) == 3 and isinstance(key[2], tuple) and len(key[2]) == 2:
            TypeChecker.scalar(key[0])
            TypeChecker.scalar(key[1])
            TypeChecker[bool](key[2][0])
            TypeChecker[bool](key[2][1])
            return (operator.le if key[2][0] else operator.lt)(key[0], val) and \
                   (operator.le if key[2][1] else operator.lt)(val, key[1])
        else:
            raise ValueError("The bound tuple can be of structure: (Lower_bound, Upper_bound, (Include_lower_bound, " +
                          "Include_upper_bound)) or (Lower_bound, Upper_bound)")

    @classmethod
    def _validater(mcs, key):
        """
        Returns a checking function that checks that a value in allowed by key.

        :param key: (tuples or [tuples]) (Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))
                                         or (Lower_bound, Upper_bound)
        :retrun: (callable) function that takes value and will raise an error if not valid
        """
        def check(val):
            """
            Checks that val is valid, will raise an error if not valid.

            :param val: (int, float)
            """
            if isinstance(key, list) or isinstance(key, tuple) and all([isinstance(k, tuple) for k in key]):
                valid = any([mcs._in_bounds(val, k) for k in key])
            else:
                valid = mcs._in_bounds(val, key)
            if not valid:
                raise ValueError("Number out of bounds {}, expected bounds {}".format(val, key))

        return check

    def __getitem__(mcs, key):
        return mcs._validater(key)


class BoundChecker(object, metaclass=_BoundCheckerMeta):
    """
    Class used to check whether a number is in given bounds.

    ex:
        BoundChecker[(0,1)](0.5)
        BoundChecker.positive(100)

    the tuple defining the bounds are (Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))
        or (Lower_bound, Upper_bound)
    You may use lists of bounds to define discontinuous bounds.
    """

    @classmethod
    def positive(cls, val):
        """
        Checks whether val is positive.
        """
        cls._validater((0, np.inf))(val)

    @classmethod
    def negative(cls, val):
        """
        Checks whether val is negative.
        """
        cls._validater((-np.inf, 0))(val)

    @classmethod
    def positive_not_zero(cls, val):
        """
        Checks whether val is positive and not zero.
        """
        cls._validater((0, np.inf, (False, True)))(val)

    @classmethod
    def negative_not_zero(cls, val):
        """
        Checks whether val is negative and not zero.
        """
        cls._validater((-np.inf, 0, (True, False)))(val)

    @classmethod
    def probability(cls, val):
        """
        Checks whether val is bound between 0 and 1 included.
        """
        cls._validater((0, 1))(val)
