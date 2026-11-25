---
name: code-write
description: Use when you must generate predictable code that follows the patterns of an existing file (tests, config, type stubs, boilerplate). A cheap model writes it from your spec plus a reference file and saves it straight to disk, so you never read the reference or the output.
---

# code-write

Run it from Bash. A spec, one or more reference files, and a target path:

```bash
~/.claude/bin/code-write --spec "Write pytest tests for UserService covering create, update and delete" --reference tests/test_order_service.py --target tests/test_user_service.py
```

Rules:
- The reference is required. Without a file to match, the output fits nothing in the project.
- Put every constraint in the spec: names, cases to cover, imports to reuse.
- Without `--target` the code is printed to stdout instead of written.
- Verify the result with a compiler, linter or test run, not by reading the whole file back.
