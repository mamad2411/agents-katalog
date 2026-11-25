---
name: coverage-gaps
description: Runs coverage, ranks the riskiest untested code by what breaks if it fails, and writes tests for the top items.
disable-model-invocation: true
---

Find and close coverage gaps. Scope: $ARGUMENTS (whole project if empty).

1. Run the project's coverage command (jest --coverage, vitest --coverage, pytest --cov, go test -cover, dotnet test with coverlet, cargo llvm-cov). If none is configured, suggest the smallest setup and ask before adding it.
2. Record the overall and per-file figures, including branch coverage if available.
3. Rank uncovered code by risk: money, auth, data writes and parsing first, then branching complexity, then recent change frequency (check `git log --since=3.months --name-only`). Ignore generated code, types and trivial getters.
4. Show the top 10 gaps with file, uncovered lines or branches, and why each is risky.
5. Write tests for the top 3, following the existing style. Assert behavior, not implementation details. Do not add tests whose only purpose is to touch lines.
6. Rerun coverage and compare.

Report before and after per file and list the remaining gaps. Ask before committing.
