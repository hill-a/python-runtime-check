# python-runtime-check

## Disclosure

inspired blackmagic from quite a fun talk

<a href="http://www.youtube.com/watch?feature=player_embedded&v=Je8TcRQcUgA" target="_blank"><img src="http://img.youtube.com/vi/Je8TcRQcUgA/0.jpg" alt="The 'Fun' of Reinvention by David Beazley" width="240" height="180" border="10" /></a>


## What is it

This is a python 3 only, type and bound checking code enforced at runtime.

### Installation

You can install this using:
```bash
pip install -e .
```
in the root directory of the repository.

### Type checking

You can enforce python annotated types at call:
```python
@check_type_at_run
def hello(a: [int, float]):
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
```

Or check them during execution:
```python
TypeChecker[int, float](0)
TypeChecker.array(numpy.arange(10))
```

useful types:
- `numpy.ndarray`
- `collections.Iterable`
- `type(None)`

### Bounds checking

You can also check annotated bounds at call:
```python
@check_bound_at_run
def hello(a: [(float('-inf'), -1), (0, 1), (2, float('+inf'))]):
    pass

@check_bound_at_run
def hello(a: (0, 1)):
    pass

@check_bound_at_run
def hello(a: (0, float('+inf'), (False, True)), b: (0, 1)) -> (0, 100):
    if a < (b * 100):
        return b * 100
    else:
        return min(a, 100)
```

Or check them during execution:
```python
BoundChecker[(0, 1), (2, 4)](0.5)
BoundChecker.positive(100)
```

the tuple defining the bounds are:  
`(Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))`  
or:  
`(Lower_bound, Upper_bound)`  

You may use lists of bounds to define discontinuous bounds

### Chained checking

You may also combine the previous methods into the annotations:
```python
@enforce_annotations
def hello(a: [BoundChecker[(0, 1)], TypeChecker[int, float]]):
    pass

@enforce_annotations
def hello(a: [BoundChecker[(0, 1)], TypeChecker[int, float]]) -> [BoundChecker[(0, 1, (False, True))], TypeChecker[float]]:
    return 0.2
```
