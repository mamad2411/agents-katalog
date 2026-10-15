---
name: run-verification
description: Use when validating a change by running the smallest relevant checks first, then expanding verification only as needed.
---

# When to use
Use for:
- validating an implementation before presenting it
- verifying a bug fix or refactor
- checking whether a suspected issue is reproduced by tests or tooling

Do not use for:
- planning work before code changes
- code review without running any commands

# Goal
Verify changes efficiently without wasting time or tokens on unnecessary full-suite runs.

# Process
1. Start with the smallest relevant verification scope.
2. Run targeted tests closest to the changed behavior.
3. Run format, lint, typecheck, or build steps only if relevant.
4. Expand to broader verification if targeted checks fail to provide confidence.
5. Record what was run and what was not.

# Rules
- Prefer narrow verification first.
- Do not claim a check passed unless it was actually run.
- Report skipped checks explicitly.
- When a command fails, summarize the failure and likely cause.

# Output
Provide:
- commands run
- pass/fail result for each
- notable failures or warnings
- checks not run
