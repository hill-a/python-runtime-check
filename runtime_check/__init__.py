# inspired blackmagic https://www.youtube.com/watch?v=Je8TcRQcUgA
# python 3 only type and bound checking

from runtime_check.check_type import TypeChecker
from runtime_check.check_bounds import BoundChecker
from runtime_check.wrappers import check_bound_at_run, check_type_at_run, enforce_annotations
