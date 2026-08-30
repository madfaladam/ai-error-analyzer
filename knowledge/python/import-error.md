# Python Import Errors

## Symptoms

Python can raise `ImportError` or `ModuleNotFoundError` when an import cannot be resolved.

## Likely Causes

- Package is not installed in the active environment.
- Module or package name is incorrect.
- Virtual environment is different from the one used to install dependencies.
- Local files shadow a package name.

## Recommended Debugging

1. Verify the exact import name.
2. Check the active Python interpreter.
3. Verify installed dependencies.
4. Check the project's package layout and working directory.
