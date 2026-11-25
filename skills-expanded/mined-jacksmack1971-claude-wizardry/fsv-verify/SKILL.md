---
name: fsv-verify
description: Project-local Full State Verification workflow. Use before and after every write, mutation, issue update, PR action, deployment action, or other external side effect.
disable-model-invocation: false
user-invocable: true
---

# FSV Verify

Use for every write, mutation, external side effect, GitHub issue update, PR creation, label edit, or deployment action.

## Protocol

1. PRE: read authoritative state.
2. ACT: perform exactly one intended operation.
3. POST: read authoritative state again.
4. DIFF: verify the exact expected delta.
5. HALT: stop on mismatch.

## Project Source-of-Truth Examples

- Files: read file contents from disk.
- Git: `git status --short`, `git diff`, `git rev-parse HEAD`.
- Tests: test output plus file-level evidence.
- GitHub: issue or PR state fetched after mutation.

Use `references/fsv-checklist.md` before reporting a multi-step task complete.
