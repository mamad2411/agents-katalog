---
name: verify
description: "Verify a completed plan phase against the plan in a fresh session; produce a PASS/WARN/FAIL report and commit on pass."
disable-model-invocation: true
---

# Verify a Phase

You are reviewing a completed phase against the implementation plan. You should be running in a **fresh session** — not the same one that wrote the code.

## 1. Find the Plan

Look for `plan.md` in the current directory, then `../plan.md`. If not found, ask the user where it is.

## 2. Identify the Phase

If the user specified a phase number, use that. Otherwise, look at recent git history to determine which phase was just implemented, and confirm with the user.

## 3. Review Against the Plan

Read the phase's objective and tasks, then systematically check:

1. **Does it work?** Run the test suite. Report pass/fail counts.
2. **Does it match the plan?** Compare each task's acceptance criteria against what was implemented.
3. **Is it safe?** Check auth, validation, input sanitization, no data leaks.
4. **Is it maintainable?** Readable code, tests present for key paths, no dead code left behind.
5. **Is it scoped correctly?** No work that belongs in other phases, no missing pieces.

## 4. Check Cross-Repo Contracts (if applicable)

If the phase produced or modified API endpoints:
- Verify the integration summary exists and matches the actual serializers/views
- Check that request/response shapes in the summary match the code

## 5. Check Context Health

Perform a lightweight check on the project's context scaffold. This is not a full drift analysis — just surface-level health.

1. Check if `.claude/context/` exists
   - **No:** Note "Context scaffold not present" and suggest `/intel` to generate it. Skip the rest of this step.
   - **Yes:** Continue.

2. List each file in `.claude/context/` (including `patterns/*.md`):
   - Read the `Last updated` date from the header comment
   - If the date is still the literal `YYYY-MM-DD` placeholder, the file is an unfilled template — report it as "Template (run /intel)" rather than stale
   - Note the line count
   - Flag files not updated in 30+ days as stale

3. Check ROUTER.md cross-references: verify each listed file actually exists

4. Summarize findings for the report's Context Health section

If context is stale or missing, suggest running `/intel` to refresh or `/remember` to add missing entries.

## 6. Produce the Report

Write the report to the **project root's** `docs/verification/` folder — one level above the sub-project you're working in. For example, if you're verifying work in `~/prj/my-app/api/`, the report goes in `~/prj/my-app/docs/verification/phase-N-[name].md`. Create the directory if it doesn't exist. All verification reports go here regardless of which sub-project the phase belongs to.

```markdown
# Verification Report: Phase N — [Name]

## Summary
[One paragraph: overall assessment]

## Results

| Check | Status | Notes |
|-------|--------|-------|
| Tests pass | PASS/FAIL | [details] |
| Matches plan | PASS/FAIL | [details] |
| Security | PASS/WARN/FAIL | [details] |
| Code quality | PASS/WARN | [details] |
| Scope | PASS/WARN | [details] |
| Integration summary | PASS/FAIL/N/A | [details] |

## Context Health

| File | Last Updated | Lines | Status |
|------|-------------|-------|--------|
| context/architecture.md | YYYY-MM-DD | NN | OK / Stale / Missing |
| context/decisions.md | YYYY-MM-DD | NN | OK / Stale / Missing |
| context/conventions.md | YYYY-MM-DD | NN | OK / Stale / Missing |
| context/ROUTER.md | YYYY-MM-DD | NN | OK / Stale / Missing |

[Any broken cross-references or suggestions]

## Issues

### FAIL (must fix)
- [file:line] Description and suggested fix

### WARN (should review)
- [file:line] Description and concern

## Verdict
PASS / PASS WITH WARNINGS / FAIL
```

## 7. Commit (on PASS only)

This step applies when you own the phase's work — a top-level manual review session. If a `/autopilot` or `/orchestrator` lead spawned you as the reviewer, do **not** commit: report your verdict and let the lead commit. The session that owns the loop is the one that commits.

If the verdict is **PASS** or **PASS WITH WARNINGS** (and the user approves), commit all changes for the phase:

- Stage all relevant files
- Write a clear commit message following commit-conventions (e.g., `feat(auth): implement phase 1 — user model and API`)
- Include the verification report in the commit

**Do not commit if the verdict is FAIL.** Fixes must happen first.

## 8. Next Steps

Based on the verdict:
- **PASS:** Changes committed. "Ready for the next phase. Start a new session and run `/execute`."
- **PASS WITH WARNINGS:** Ask the user whether to commit now or address warnings first.
- **FAIL:** List what must be fixed. Suggest fixing in this session, then re-running `/verify`.
