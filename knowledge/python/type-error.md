# Python TypeError

## Symptoms

`TypeError` occurs when an operation or function is used with an incompatible type.

Example:

```python
count = "10"
result = count + 5
```

## Likely Causes

- Mixing strings and numbers.
- Passing the wrong argument type.
- Calling a value that is not callable.
- Incorrect assumptions about a function's return type.

## Recommended Debugging

1. Inspect the runtime types of the values involved.
2. Check the function signature and caller.
3. Validate external input before performing operations.
4. Convert values explicitly when conversion is intended.
