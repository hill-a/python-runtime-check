# python-runtime-check

## Disclosure

inspired blackmagic from quite a fun talk https://www.youtube.com/watch?v=Je8TcRQcUgA

## what is it

It is a python 3 only, type and bound checking code. 

## Type checking

You can enforce python annotation types at call:
```python
@check_type_at_run
def hello(a: [int,float]):
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
Type_checker[int](0)
Type_checker.array(numpy.arange(10))
```

useful types:
- numpy.ndarray
- collections.Iterable
- type(None)

## Bounds checking

You can also check the bounds:
```python
@check_bound_at_run
def hello(a: [(float('-inf'), -1), (0, 1),(2, float('+inf'))]):
    pass

@check_bound_at_run
def hello(a: (0, 1)):
    pass

@check_bound_at_run
def hello(a: (0, float('+inf'),(False, True)), b: (0, 1)) -> (0,100):
    if a < (b * 100):
        b * 100
    else:
        min(a, 100)
```

Or check them during execution:
```
Bound_checker[(0,1)](0.5)
Bound_checker.positif(100)
```

the tuple defining the bounds are ```(Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))``` or ```(Lower_bound, Upper_bound)```
You may use lists of bounds to define discontinuous bounds

## Chainned checking

You may also combine the previous methods into the annotations:
```
@enforce_annotations
def hello(a: [Bound_checker[(0,1)], Type_checker[[int,float]]]):
    pass

@enforce_annotations
def hello(a: [Bound_checker[(0,1)], Type_checker[[int,float]]]) -> [Bound_checker[(0,1,(False, True))], Type_checker[float]]:
    return 0.2
```
