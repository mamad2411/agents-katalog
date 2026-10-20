---
name: debug-python-error
description: Full pipeline to debug any Python exception — analyzes the stacktrace to find the root cause, then generates an actionable fix suggestion with corrected code. Combines analyze-python-error and suggest-python-fix in sequence.
goal: "Deliver a complete debug report (error location + root cause + fix code) for any Python exception from a raw stacktrace."
version: 1.0.0
category: python/debugging
level: composite
tags: [python, debug, pipeline, composite, attributeerror]

# Execution order: analyze → fix (output of step 1 feeds into step 2)
sub_skills:
  - analyze-stacktrace      # step 1 → produces: file, line, variable, error_type
  - read-code-context       # step 2 → uses: file, line → produces: code_context
  - suggest-python-fix      # step 3 → uses: everything from above → produces: fix, snippet

# ── Layer 1: Specification ───────────────────────────────────────────────────
input:
  type: object
  required: [stacktrace, source_path]
  properties:
    stacktrace:
      type: string
      description: Full Python exception traceback
    source_path:
      type: string
      description: Path to the Python source file with the bug

output:
  type: object
  properties:
    file:          { type: string  }
    line:          { type: integer }
    variable:      { type: string  }
    error_type:    { type: string  }
    fix_suggestion:{ type: string  }
    code_snippet:  { type: string  }

constraints:
  host:
    os: [linux, darwin, windows]
  resources:
    memory: "256MB"
    timeout: "120s"
  safety:
    fs_access: read-only
    requires_approval: false

acceptance_criteria:
  - "output.file must be a .py filename"
  - "output.line must be a positive integer"
  - "output.error_type must be a non-empty string"
  - "output.fix_suggestion must have at least 30 characters"
  - "output.code_snippet must not be empty"
  - "All 6 output fields must be present"

metrics:
  pass_rate:
    target: "≥ 75%"
    unit: "%"
  latency_p95:
    target: "< 15000"
    unit: "ms"
  token_usage:
    target: "< 2000"
    unit: "tokens/call"
  retry_rate:
    target: "< 10%"
    unit: "%"

# ── Layer 2: Design ──────────────────────────────────────────────────────────

# ── Layer 5: Evaluation — Test Cases ────────────────────────────────────────
test_cases:
  - id: TC-001
    name: "Full pipeline on AttributeError (buggy_code.py)"
    input:
      stacktrace: |
        Handling order #42
        Traceback (most recent call last):
          File "/home/user/SWE-Agent-Skills/test_data/buggy_code.py", line 44, in <module>
            main()
          File "/home/user/SWE-Agent-Skills/test_data/buggy_code.py", line 40, in main
            controller.handle_order(order_id=42)
          File "/home/user/SWE-Agent-Skills/test_data/buggy_code.py", line 35, in handle_order
            self.user_service.process_user()
          File "/home/user/SWE-Agent-Skills/test_data/buggy_code.py", line 25, in process_user
            username = self.get_username()
          File "/home/user/SWE-Agent-Skills/test_data/buggy_code.py", line 19, in get_username
            return self.current_user.name
                   ^^^^^^^^^^^^^^^^^^^^^^
        AttributeError: 'NoneType' object has no attribute 'name'
      source_path: "test_data/buggy_code.py"
    expected_output:
      file: "buggy_code.py"
      line: 19
      error_type: "AttributeError"
    acceptance:
      - "output.file == expected.file"
      - "abs(output.line - expected.line) <= 2"
      - "output.error_type == expected.error_type"
      - "len(output.fix_suggestion) >= 30"
      - "len(output.code_snippet) >= 10"
      - "all(k in output for k in ['file', 'line', 'variable', 'error_type', 'fix_suggestion', 'code_snippet'])"
    tags: [happy_path, e2e, attributeerror]

  - id: TC-002
    name: "Full pipeline on KeyError"
    input:
      stacktrace: |
        Traceback (most recent call last):
          File "app/routes.py", line 33, in handle_request
            user_id = request_data['user_id']
        KeyError: 'user_id'
      source_path: "app/"
    expected_output:
      file: "routes.py"
      line: 33
      error_type: "KeyError"
    acceptance:
      - "output.file == expected.file"
      - "output.error_type == expected.error_type"
      - "len(output.fix_suggestion) >= 30"
      - "len(output.code_snippet) >= 10"
      - "all(k in output for k in ['file', 'line', 'variable', 'error_type', 'fix_suggestion', 'code_snippet'])"
    tags: [happy_path, e2e, keyerror]
---

## Goal
Orchestrate the full Python debugging pipeline: from raw stacktrace to a complete, actionable fix.

## 🚀 Instructions

Composite skill — SkillExecutor handles the pipeline automatically:
1. `analyze-stacktrace` receives `{stacktrace, source_path}` → outputs `{file, line, variable, error_type}`
2. `suggest-python-fix` receives `{file, line, variable, error_type}` → outputs `{fix_suggestion, code_snippet}`
3. All outputs are merged into the final response (6 fields total).

## ⚠️ Common Mistakes

- Using the composite skill for all cases — if only location is needed, use `analyze-python-error` directly to save tokens.

## 🔗 Related Skills

- `analyze-python-error` — atomic sub-skill for error location.
- `suggest-python-fix` — atomic sub-skill for fix generation.
