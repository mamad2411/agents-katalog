---
name: review
description: Review recent changes against the project's harness rules — architecture, code quality, tests, security
---

Review the current uncommitted changes (or the most recent commits if specified) against the project's harness rules.

This skill is project-agnostic — every check below is parameterized by `.harness/project.md`. If that file does not exist, the review uses sensible defaults and tells the user that creating one would make reviews more accurate.

---

## Step 1: Load context

1. Read `.harness/project.md` if present.
2. Get the changed files:
   ```bash
   git diff --name-only HEAD
   git diff --name-only --cached
   ```
   (Combine staged + unstaged. If the user names a commit range, use that instead.)

## Step 2: Run the checklist

### A. Architecture Compliance
- [ ] Every changed file lives where `Source Layout` and `placement_rules` require.
- [ ] No import violates `layer_order`.
- [ ] Role-specific shape rules (e.g. tool function signatures, model placement) are respected if declared.
- [ ] No reverse imports introduced.

(Run the `arch-reviewer` agent for the heavy lifting if the diff is large.)

### B. Code Quality
- [ ] Project's `format_check`, `lint`, and `typecheck` (if any) all pass.
- [ ] Project's `Conventions` are respected: error handling, logging, secrets access.
- [ ] No hardcoded credentials, API keys, or tokens.
- [ ] No dead code, no obvious copy-paste duplication, no TODOs left without owners.

### C. Testing
- [ ] Every new public function/method/route has at least one test.
- [ ] Tests live in the project's `test_dirs`, mirroring the source structure.
- [ ] Tests assert real behavior — no tautological tests that mock everything and assert what was mocked.
- [ ] Edge cases (empty input, errors, timeouts) are covered, not only happy paths.

### D. Security
- [ ] No secrets committed.
- [ ] User input is validated before use in DB / shell / file / prompt / URL contexts.
- [ ] Authorization is checked on mutating operations.
- [ ] Errors don't leak internal details to users.

(Run `security-reviewer` for the heavy lifting if the diff touches input handling, auth, or external calls.)

### E. Spec / Change Alignment (if a harness change is active)
- [ ] Changes correspond to tasks in `<change-dir>/tasks.md`.
- [ ] Every spec scenario in `<change-dir>/specs/` has corresponding code and tests.
- [ ] No gold-plating — features added that the spec did not request.

---

## Step 3: Report

For each finding:

| Severity | File | Issue | Fix |
|---|---|---|---|
| CRITICAL / WARNING / INFO | `<project-relative path>:<line>` | <concise issue> | <specific suggested change> |

End with a one-line verdict:

- **APPROVE** — no findings, or only INFO items.
- **APPROVE WITH SUGGESTIONS** — only WARNING items.
- **REQUEST CHANGES** — at least one CRITICAL.

Always cite specific files and lines — never give vague feedback.
