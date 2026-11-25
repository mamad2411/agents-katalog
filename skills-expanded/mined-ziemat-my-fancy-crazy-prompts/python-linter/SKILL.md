---
name: python-linter
description: "Skill for linting Python code using Astral tools: ruff for code checks and ty for type checks. Use when user requests linting or type validation for Python."
---

# Python Lint & Type Check (Astral)

Lint Python code with `ruff` and validate types with `ty`.

## When to Use

- After modifying `.py` files
- Before committing or opening a PR
- When user requests lint or type checks

## Verification Procedure

1. **Run ruff lint:**
```bash
   ruff check <path/to/file_or_dir> --config pyproject.toml
```

2. **Run ty type check:**
```bash
   ty check <path/to/file_or_dir> --config pyproject.toml
```

3. **Interpret results:**
   - No output = no issues found
   - Output with messages = lint or type errors detected
   - If errors found:
     - Identify the reported line and issue
     - Suggest or apply fixes
     - Re-run the checks after fix

4. **Error Handling:**
   - If ruff or ty is unavailable, inform user
   - If the target path does not exist, verify path first
   - If issues persist after fixes, provide detailed explanation

## Example Output

Ruff (issues found):

```bash
ruff check app.py --config pyproject.toml
# F401 `os` imported but unused
```

Ty (issues found):

```bash
ty check app.py --config pyproject.toml
# error: Incompatible return value type (got "int", expected "str")
```

## Important considerations
Usage of `--config` for Ruff and Ty is important to make sure the linters follow the rules declared in the project.
