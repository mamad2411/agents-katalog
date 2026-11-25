---
name: fix-compile-errors
description: Fix compilation/type errors with minimal diff
user-invocable: false
---
## Overview

Analyze the compilation errors in the current codebase and provide fixes for them, making the necessary changes to resolve all compilation errors.

## Steps

1. **Identify compilation errors**
    - Type mismatches and casting issues
    - Missing imports or dependencies
    - Syntax errors and malformed code
    - Undefined variables or functions
    - Configuration issues
2. **Fix each error**
    - Identify the root cause
    - Provide the corrected code
    - Explain why the fix resolves the issue

## Fix Compile Errors Checklist

- [ ] Identified all type mismatches and casting issues
- [ ] Fixed missing imports or dependencies
- [ ] Corrected syntax errors and malformed code
- [ ] Fixed undefined variables or functions
- [ ] Resolved configuration issues
- [ ] Provided corrected code for each error
- [ ] Explained why each fix resolves the issue
- [ ] Verified all compilation errors are resolved

## Guardrails

- Resolve the real type or compile error with the smallest correct change; do not disable checks or loosen types to force a green build.
- Make a minimal diff; do not refactor unrelated code while fixing compile errors.
- Do not commit, push, merge, or run destructive commands without explicit user consent.