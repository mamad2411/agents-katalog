---
name: suggest-python-fix
description: Suggests a concrete, actionable Python fix for an exception given the file, line number, variable name, and error type. Generates both a human-readable explanation and a corrected code snippet.
goal: "Produce a clear root-cause explanation and a working Python code fix for the reported exception location."
version: 1.0.0
category: python/debugging
level: atomic
tags: [python, fix, attributeerror, patch, refactoring]

# ── Specification ───────────────────────────────────────────────────
input:
  type: object
  required: [file, line, variable, error_type]
  properties:
    file:
      type: string
      description: Python source filename with the error
    line:
      type: integer
      description: Line number where the exception occurs
    variable:
      type: string
      description: The variable or expression that is None or invalid
    error_type:
      type: string
      description: The Python exception class (e.g. AttributeError, TypeError)
    code_context:
      type: string
      description: The actual source code around the error line

output:
  type: object
  properties:
    fix_suggestion:
      type: string
      description: Human-readable root cause and recommended fix strategy (2-4 sentences)
    code_snippet:
      type: string
      description: Python code snippet (10-20 lines) demonstrating the fix

constraints:
  host:
    os: [linux, darwin, windows]
  resources:
    memory: "256MB"
    timeout: "30s"
  safety:
    fs_access: read-only
    requires_approval: false

acceptance_criteria:
  - "len(output.fix_suggestion) >= 30"
  - "any(kw in output.code_snippet for kw in ['def ', 'if ', 'return', 'self.', 'None', 'assert', 'raise', 'try'])"
  - "input.error_type.lower() in output.fix_suggestion.lower() or input.variable.lower() in output.fix_suggestion.lower()"
  - "len(output.code_snippet) > 0"

metrics:
  pass_rate:
    target: "≥ 80%"
    unit: "%"
  accuracy:
    target: "≥ 80%"
    unit: "%"
  latency_p95:
    target: "< 6000"
    unit: "ms"
  token_usage:
    target: "< 1000"
    unit: "tokens/call"

# ── Design ──────────────────────────────────────────────────────────

examples:
  - input:
      file: "service.py"
      line: 42
      variable: "self.db"
      error_type: "AttributeError"
    expected_output:
      fix_suggestion: "The variable self.db is None because it was not initialized before use..."
      code_snippet: "def __init__(self):\n    self.db = DatabaseConnection()  # Initialize properly\n"

# ──  Evaluation — Test Cases ────────────────────────────────────────
test_cases:
  - id: TC-001
    name: "Fix for AttributeError on None"
    input:
      file: "buggy_code.py"
      line: 19
      variable: "self.current_user"
      error_type: "AttributeError"
    expected_output:
      fix_suggestion: "placeholder"   # validated by acceptance criteria, not exact match
      code_snippet: "placeholder"
    acceptance:
      - "len(output.fix_suggestion) >= 30"
      - "any(kw in output.code_snippet for kw in ['def ', 'if ', 'self.', 'return', 'None', 'assert', 'raise', 'try'])"
      - "'None' in output.fix_suggestion or 'none' in output.fix_suggestion.lower() or 'attribute' in output.fix_suggestion.lower() or 'current_user' in output.fix_suggestion"
      - "len(output.code_snippet) >= 20"
    tags: [happy_path, attributeerror]

  - id: TC-002
    name: "Fix for KeyError on dict access"
    input:
      file: "routes.py"
      line: 33
      variable: "request_data"
      error_type: "KeyError"
    expected_output:
      fix_suggestion: "placeholder"
      code_snippet: "placeholder"
    acceptance:
      - "len(output.fix_suggestion) >= 30"
      - "len(output.code_snippet) >= 10"
      - "any(kw in output.code_snippet for kw in ['.get(', 'if ', 'KeyError', 'try', 'in '])"
    tags: [happy_path, keyerror]

  - id: TC-003
    name: "Fix for TypeError in arithmetic"
    input:
      file: "calculator.py"
      line: 8
      variable: "factor"
      error_type: "TypeError"
    expected_output:
      fix_suggestion: "placeholder"
      code_snippet: "placeholder"
    acceptance:
      - "len(output.fix_suggestion) >= 30"
      - "len(output.code_snippet) >= 10"
      - "any(kw in output.code_snippet for kw in ['isinstance', 'if ', 'int(', 'float(', 'None', 'raise'])"
    tags: [happy_path, typeerror]
---

## Goal
Generate a clear, actionable fix for a Python exception — explaining the root cause in plain language and providing corrected code.

## 🚀 Instructions

1. Based on the `file`, `line`, `variable`, and `error_type`, reason about the root cause:
2. **For `AttributeError: 'NoneType' object has no attribute ...`**:
   - The variable was never initialized or set to `None` before use.
   - Fix options (choose most appropriate):
     - Guard: `if variable is not None:` before access
     - Early raise: `if variable is None: raise ValueError("message")`
     - Initialize in `__init__` with a valid default
     - Use dependency injection or factory pattern
3. **For `TypeError`** (wrong operand types):
   - Add `isinstance()` check or explicit type conversion
4. **For `KeyError` / `IndexError`**:
   - Use `.get(key, default)` for dicts, or `if key in dict` guard
5. Write `fix_suggestion` (2-4 sentences): what went wrong, why, and recommended fix.
6. Write `code_snippet` (10-20 lines): corrected Python code for the relevant method/block.
7. Return **ONLY** a JSON object with `fix_suggestion` and `code_snippet`.

## Examples

See `examples:` in the YAML frontmatter above.

## ⚠️ Common Mistakes

- Being too generic — always reference the specific `variable` in the explanation.
- Providing a code snippet that doesn't compile valid Python.
- Forgetting to handle the case where None is a valid intentional value.

## 🔗 Related Skills

- `analyze-python-error` — produces the input for this skill.
- `debug-python-error` — composite skill that chains both.
