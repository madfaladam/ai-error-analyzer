# Python Null Reference / None Access

## Symptoms

Python commonly raises `AttributeError` when code tries to access an attribute or method on `None`.

Example:

```python
player = None
player.transform.position
```

Typical message:

```text
AttributeError: 'NoneType' object has no attribute 'transform'
```

## Likely Causes

- A function returned `None` unexpectedly.
- An object lookup failed and returned `None`.
- Initialization did not happen before the object was used.
- A dependency was not injected or assigned.

## Recommended Debugging

1. Inspect the variable immediately before the failing line.
2. Find where the value is assigned or returned.
3. Add an explicit guard when `None` is a valid state.
4. Fix the initialization or lookup logic when `None` is not expected.

## Example Fix

```python
if player is None:
    raise ValueError("player must be initialized before update")

player.transform.position
```
