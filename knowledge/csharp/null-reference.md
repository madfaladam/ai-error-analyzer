# C# NullReferenceException

## Symptoms

`NullReferenceException` occurs when code accesses an instance member through a reference whose value is `null`.

Example:

```csharp
Player player = null;
player.transform.position = target;
```

## Likely Causes

- Object was never instantiated.
- Component lookup returned `null`.
- Initialization order is incorrect.
- An object was destroyed before access.

## Recommended Debugging

1. Inspect the reference on the failing line.
2. Verify the object/component lookup succeeded.
3. Check lifecycle and initialization order.
4. Guard nullable references where appropriate.
