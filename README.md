# python-runtime-check

[![Build Status](https://travis-ci.org/hill-a/python-runtime-check.svg?branch=master)](https://travis-ci.org/hill-a/python-runtime-check) [![Build status](https://ci.appveyor.com/api/projects/status/bt3rj6k34vbwgn96?svg=true)](https://ci.appveyor.com/project/hill-a/python-runtime-check) [![CC-0 license](https://img.shields.io/badge/License-CC--0-blue.svg)](https://creativecommons.org/share-your-work/public-domain/cc0/) [![Python Version](https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg)](https://github.com/hill-a/python-runtime-check) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/ef2f1c7118934061ada23af105812b0c)](https://www.codacy.com/app/hill-a/python-runtime-check?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hill-a/python-runtime-check&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ef2f1c7118934061ada23af105812b0c)](https://www.codacy.com/app/hill-a/python-runtime-check?utm_source=github.com&utm_medium=referral&utm_content=hill-a/python-runtime-check&utm_campaign=Badge_Coverage)

## Information
### Disclosure

I did not directly come up with this. This 'blackmagic' is inspired from a talk by David Beazley. It's quite fun watch if you have an hour to spare :)  

Video:  
<a href="http://www.youtube.com/watch?feature=player_embedded&v=Je8TcRQcUgA" target="_blank"><img src="http://img.youtube.com/vi/Je8TcRQcUgA/0.jpg" alt="The 'Fun' of Reinvention by David Beazley" width="480" height="360" border="10" /></a>  

As such, all the code in this repository is Creative Commons 0 [(CC0)](https://creativecommons.org/share-your-work/public-domain/cc0/)  

### What is this?

This is a python 3 only library, used for type checking and bound checking, enforced at runtime.  

Now before I begin, yes I am aware of python's ducktyping. However some situations have arisen in the past, where I needed to garanty that my inputs where sanitized. For example, a list `a = []` that should contain only number, if `a.append('')` occure, it will lead to undesired side effects. 
Or even with `ParseArgument`, if you need a number between 0 and 1 for probabilistic usage.  

Also, I find it sad that the [annotations](https://www.python.org/dev/peps/pep-3107/) of types in methods `a: int` is not an enforced restriction at runtime (it is however very useful with [MyPy](http://mypy-lang.org/) or some IDEs).  

Hence this library, where annotations can be enforced if present, types checked, or bounds of numbers checked.  

### When should I use this?

Preferably, in situations where you REALLY need to. This is not designed to run on every function (you can't neglect the overhead cost), as such here are some (rather poor) examples of when to use this:  
<br/>
```python
def print_information(info):
    print("here is the information:" + info)
```
Here, we would prefere `info` to be of type string.  
<br/>  
```python
def print_informations(infos):
    for info in infos:
        print("here some of the information:" + info)
```
Here, we would prefere `infos` to be of type list of string.  
<br/>  
```python
def dice_roll(proba):
    roll = random.random()
    if roll <= proba:
        print("success!")
        return True
    else:
        print("failure!")
        return False
```
Here, we would prefere `proba` to be of type float, but also bound between [0, 1].  
  

## Installation

This library will require NumPy and python 3.5 or higher:
```bash
pip install numpy
```

You can install this using:
```bash
pip install git+https://github.com/hill-a/python-runtime-check
```

## Usage
### Type checking

You can enforce the python type annotations at call:
```python
 # a can either be a int, or a float
@check_type_at_run
def hello(a: Union[int, float]):
    pass

 # a has to be an int
@check_type_at_run
def hello(a: int):
    pass

 # c can be either None, or a list composed of anything
 # the return value can either be an int, or a string
@check_type_at_run
def hello(a: int, b: str, c: Optional[List[Any]] = []) -> Union[int, str]:
    if c is None:
        return b
    else: 
        return a
```  

Or check them during execution:
```python
TypeChecker[int, float](0) # here the comma seperated types are replaced with typing.Union internaly
TypeChecker[Tuple[int, float, str]]((0, 1.0, 'a'))
TypeChecker[Optional[Dict[str, int]]](None)
TypeChecker[Optional[Dict[str, int]]]({'a':1, 'b':2})
TypeChecker.iterable("hello")
TypeChecker.numpy_array(numpy.arange(10))
```  

Should you need to check all the elements of a list, dict, set, tuple or sequence when type checking, 
set this flag `runtime_check.check_type.DEEP = True`.  

Here are some useful types commonly used in python:
- `numpy.ndarray`
- `torch.FloatTensor`
- `torch.tensor._TensorBase`
- `collections.Iterable`
- `type(None)`
- `typing.Optional[int]`
- `typing.Union[int, float]`
- `typing.List, typing.Dict, typing.Set, typing.Tuple, typing.Iterable`
- `typing.Any, typing.TypeVar, typing.AnyStr`  

python typing annotations [here](https://docs.python.org/3/library/typing.html).

### Bounds checking

You can check annotated bounds at call (however the notation is not very readable):
```python
 # a must be between ]-inf, 1] or [0, 1] or [2, +inf[
@check_bound_at_run
def hello(a: [(float('-inf'), -1), (0, 1), (2, float('+inf'))]):
    pass

 # a must be between [0,1]
@check_bound_at_run
def hello(a: (0, 1)):
    pass

 # a must be between ]0, +inf[
 # b must be between [0, 1]
 # return must be between [0, 100]
@check_bound_at_run
def hello(a: (0, float('+inf'), (False, True)), b: (0, 1)) -> (0, 100):
    if a < (b * 100):
        return b * 100
    else:
        return min(a, 100)
```

Or check them during execution:
```python
BoundChecker[(0, 1), (2, 4)](0.5)         # [0, 1] or [2, 4]
BoundChecker[(0, 100, (True, False))](20) # [0, 100[
BoundChecker.positive(100)                # [0, +inf[
```

the tuple defining the bounds are:  
`(Lower_bound, Upper_bound, (Include_lower_bound, Include_upper_bound))`  
or:  
`(Lower_bound, Upper_bound)`  
The bounds must be numbers (`float` or `int`), if the `Include_lower_bound` and `Include_upper_bound` are not defined, 
they default to `True`. 

You may use lists of bounds to define discontinuous bounds

### Chained checking

You may also combine the previous execution checks, to validate a variable with annotations:
```python
@enforce_annotations
def hello(a: [BoundChecker[(0, 1)], TypeChecker[int, float]]):
    pass

@enforce_annotations
def hello(a: TypeChecker[str]):
    pass

@enforce_annotations
def hello(a: [BoundChecker[(0, 1)], TypeChecker[int, float]]) -> [BoundChecker[(0, 1, (False, True))], TypeChecker[float]]:
    return 0.2
```
