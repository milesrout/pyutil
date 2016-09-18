# pyutil
A collection of very useful utilities for Python 3.

## pyaccumulate

I think we can all agree that generators are nice to write in Python, much nicer than explicitly collecting into a data structure (like a list, a set or a dictionary). But sometimes you want those strict semantics, and sometimes you want to manipulate the return values of a function in one place. So you can either do it manually:

```python
def foo(a, b, c):
  result = []
  for x in a:
    if pred(x):
      result.append(baz(x))
      return result
    ...
    ...
    result.append(bar(x))
  return result
```

or write a generator and a wrapper function for that generator:

```python

def foo(*args, **kwds):
  return list(foo_impl(*args, **kwds))
  
def foo_impl(a, b, c):
  for x in a:
    if pred(x):
      return (yield baz(x))
    ...
    ...
    yield bar(x)
```

I don't find that very aesthetically pleasing. So I wrote this:

```python
@accumulate(list)
def foo(a, b, c):
  for x in a:
    if pred(x):
      return (yield baz(x))
    ...
    ...
    yield bar(x)
```

Easy.

## pytrace

A **simple** tracing decorator for Python.

```python
@trace()
def foo(a, b, c):
    return "hello, world!"
foo(1, 'a', True)
```

```
$ python3 pytrace.py
foo(1, 'a', True) -> "hello, world!"
```

**pytrace** supports showing argument types.

```python
@trace(show_types=True)
def foo(a, b, c):
    return "hello, world!"
foo(1, 'a', True)
```

```
$ python3 pytrace.py
foo(1: int, 'a': str, True: bool) -> "hello, world!"
```

**pytrace** also supports a per-definition call counter.

```python
@trace(show_counter=True)
def test_counter(n):
    return n
test_counter(1)
test_counter(10)
test_counter(20)
```

```
$ python3 pytrace.py
1 test_counter(1) -> 1
2 test_counter(10) -> 10
3 test_counter(20) -> 20
```
