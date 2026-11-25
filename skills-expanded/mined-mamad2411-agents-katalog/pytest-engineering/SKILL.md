---
name: pytest-engineering
description: Write and configure pytest suites. Use when working on Python test projects.
metadata:
  tags: pytest, engineering
---

# pytest Engineering

## Use this skill when
- Writing fixtures, parametrization, and markers
- Configuring conftest and plugins
- Speeding up and stabilizing the suite

## Do not use this skill when
- Non-Python projects
- Testing design (use unit-testing)

## Instructions
1. Use fixtures for setup/teardown and scope them (function/class/session).
2. Parametrize to cover cases compactly.
3. Use markers for slow/e2e/smoke; exclude by default.
4. Use monkeypatch and tmp_path; avoid monkeypatching internals broadly.
5. Freeze time with freezegun rather than sleeping.
6. Keep tests deterministic in ordering and isolation.
7. Configure coverage thresholds meaningfully.

## Checklist
- No sleeps or flaky ordering
- Slow tests excluded by default
- Fixtures scoped tightly

## Output Format
- Fixture map | markers | parametrization | perf notes

## Common Mistakes
- Shared mutable fixtures across tests
- Sleeps instead of waits
- Test order dependencies
