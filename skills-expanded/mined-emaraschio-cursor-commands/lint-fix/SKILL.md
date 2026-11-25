---
name: lint-fix
description: Fix lint issues in the current file
user-invocable: false
---
## Overview

Analyze the current file for linting issues and automatically fix them according to the project's coding standards, then apply the fixes directly to the code and explain what changes were made.

## Steps

1. **Identify linting issues**
    - Code formatting and style consistency
    - Unused imports and variables
    - Missing semicolons or proper indentation
    - Best practice violations
    - Type safety issues
2. **Apply fixes**
    - Fix formatting and style issues
    - Remove unused imports and variables
    - Add missing semicolons or correct indentation
    - Apply best practice corrections
    - Fix type safety issues
    - Explain what changes were made

## Lint and Fix Code Checklist

- [ ] Identified all code formatting and style issues
- [ ] Identified unused imports and variables
- [ ] Identified missing semicolons or indentation issues
- [ ] Identified best practice violations
- [ ] Identified type safety issues
- [ ] Applied all formatting and style fixes
- [ ] Removed unused imports and variables
- [ ] Fixed indentation and added missing semicolons
- [ ] Applied best practice corrections
- [ ] Fixed type safety issues
- [ ] Explained what changes were made

## Guardrails

- Limit edits to formatting and style; do not change behavior while fixing lint.
- Use the project linter config rather than personal or ad hoc rules.
- Scope is the current file; if asked to fix lint across the whole repo, point to the repo-wide lint workflow (`/lint-suite`) instead of silently linting one file.
- Do not commit, push, merge, or run production scripts without consent.