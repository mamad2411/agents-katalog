---
name: whats-new-in-python
description: Consult version-specific Python syntax, built-in type, and typing updates when writing or reviewing Python code or discussing new Python features.
metadata:
  homepage: "https://docs.python.org/3/whatsnew/"
  version: "Python 3.14, 3.15"
  last-updated: "2026-09-20"
  generated-by: "gpt-6"
---

# What's New in Python

## How to load references

1. Before reading any reference, determine the project's required Python version and supported range from its configuration, such as `requires-python` in `pyproject.toml`. Do not infer compatibility from the installed interpreter alone. If no project requirement is available, use the explicitly requested target version or ask for it.
2. Load references cumulatively: read every reference in the table whose version is less than or equal to the target version, in ascending version order. For example, a Python 3.15 target requires both the 3.14 and 3.15 references. For upgrade discussions, use the proposed target version. When applying features to code, preserve compatibility with the project's minimum supported Python version.
3. Read each reference only once per context. Reuse its contents when already available; do not reload it on subsequent skill invocations.

| Python version | Reference |
| --- | --- |
| 3.14 | [Python 3.14 summary](references/python-3.14-summary.md) |
| 3.15 | [Python 3.15 summary](references/python-3.15-summary.md) |

## Further reference

The [Python What's New documentation](https://docs.python.org/3/whatsnew/) covers details intentionally omitted here, including uncommon restrictions and migration considerations. Consult it or the linked PEPs only when the task needs information absent from the loaded reference. Do not fetch external documentation for information already covered here or in that reference.
