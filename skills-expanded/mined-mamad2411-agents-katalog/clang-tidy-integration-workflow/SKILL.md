---
name: clang-tidy-integration-workflow
description: Automated static analysis pipeline using clang-tidy with project-specific checks and suppression strategies for large multi-file C++ codebases.
category: devops
version: 1.0.0
tags: [cpp, static-analysis, clang-tidy, ci, linting]
source_type: extracted-from-git
source_url: https://github.com/bitcoin/bitcoin
source_ref: refs/remotes/origin/master
source_commit: edcf84c73abcad31346388a4b8712b38742801ce
source_project: bitcoin
version_origin: extracted
confidence: high
---

# Clang-tidy Integration for C++ Code Quality

## When to use

Any non-trivial C++ project that wants deterministic linting enforcement across CI and local dev, with inline suppression that doesn't rot.

## Procedure

1. Configure the build with `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` so clang-tidy can resolve includes/flags per translation unit.
2. Either run clang-tidy on the whole tree in CI, or only on changed lines in pre-commit via a `clang-format-diff.py`-style wrapper that reads `git diff -U0`.
3. Suppress individual checks inline with `// NOLINTNEXTLINE(<check-name>): <one-line justification>`. Require the justification in code review — bare `NOLINT` rots.
4. Pair with a checked-in `.clang-format` so format and semantic checks share the same style source of truth.
5. Treat new warnings as errors in CI; whitelist existing ones by directory during adoption, burn down over time.

## Notes

- Use `-header-filter='^<project>/'` to avoid third-party header noise.
- `.clang-tidy` at repo root can set baseline checks; per-directory overrides live in nested `.clang-tidy` files.

## Evidence

- `doc/developer-notes.md` (section "Running clang-tidy")
- `src/.clang-format`
- `contrib/devtools/clang-format-diff.py`
