---
name: test-generator
description: Create focused tests for edge cases and regressions.
metadata:
    triggers:
        - write tests
        - add unit tests
        - cover edge cases
    tags:
        - coding
        - testing
    priority: 85
---

Generate tests that prove behavior.

Checklist:
- Cover success path, error path, and edge cases.
- Prefer deterministic, isolated tests.
- Add regression tests for known failures.
- Keep tests readable and fast.
