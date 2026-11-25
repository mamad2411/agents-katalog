---
name: run-tests
description: Runs the project's test suite (pytest or npm test) and summarises failures. Use when asked to run or fix tests.
allowed-tools: Bash(pytest *) Bash(npm test *) Read Grep
argument-hint: "[test path]"
---

# Run tests

Run `scripts/run_tests.sh $ARGUMENTS` and read the summary it prints. For a single file pass its path.

| Tool | Command |
|---|---|
| `pytest` | `pytest -q` |
| `npm` | `npm test --silent` |

If a test needs network access, say so instead of retrying.
