---
name: tdd-bugfix
description: "Reproduce → root-cause → failing test → minimal fix → verify. Trigger: 'fix this bug', 'reproduce and fix', 'TDD fix'. Requires a local test path."
when_to_use: "Activate when fixing a bug WITH a cheap local test path. Do NOT use for design tasks, features, or bugs requiring manual browser reproduction."
argument-hint: "[bug description or failing test path]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: development
  ck_mcp_tools: [ck_validate, ck_finding, ck_git_diff, ck_git_commit, ck_memory_record]
  related_skills: [deep-code-quality-review]
---

# TDD Bugfix

Test-first bug fix. Failing test proves the bug, fix makes it pass, runtime evidence confirms.

## Do NOT use when
- No local test path exists (manual browser testing, production-only bugs)
- Building features (use `architect-first` then `plan-slice`)
- Refactoring (use `deep-code-quality-review`)

## Workflow

1. **Reproduce**: Trace the code path to the defect. Write a minimal test that fails. Run it to confirm failure.
2. **Root-cause**: Follow [root-cause checklist](references/root-cause-checklist.md). Record root cause via `ck_memory_record` (type: `finding`).
3. **Failing test**: Write a test that demonstrates the bug. Must be: minimal, deterministic, clearly named. Confirm it fails.
4. **Validate test**: Run `ck_validate` on the test code. Fix findings.
5. **Minimal fix**: Smallest change to make the test pass. No refactoring, no improvements. Record improvement ideas via `ck_memory_record` for later.
6. **Verify**: Failing test passes. Full suite passes (`mix test`). Zero new failures.
7. **Validate fix**: Run `ck_validate` on the diff. Record findings.
8. **Commit**: `ck_git_commit` with message referencing the bug and test.

## Rules

- Test first, fix second — no exceptions
- Minimal fix only — refactoring is a separate commit
- No `Process.sleep/1` in tests — use monitors or `:sys.get_state/1`
- Root-cause, not symptom — fix the cause or record deeper issue as `ck_finding`

## Output

- Failing test proving the bug
- Minimal fix making test pass
- Full suite passing
- Root cause recorded in memory
