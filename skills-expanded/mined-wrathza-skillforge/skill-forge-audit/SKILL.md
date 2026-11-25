---
name: skill-forge-audit
description: "Batch-evaluate all skills in the repo with skill-forge-judge and render a single consolidated grade report sorted by grade (worst first) so effort is directed correctly. Use when reviewing overall skill quality, finding where to invest improvement effort, or after bulk skill changes. Triggers: audit all skills, grade report, skill health check, where should I focus."
compatibility: Claude Code
---

# Skill Forge Audit

Batch-run skill-forge-judge across every skill in the repo. One consolidated report — grades, top issues, priority order. Read-only: no fixes applied.

Requires `skill-forge-judge` to be installed.

No `references/` — this skill is single-file by design; the whole workflow fits in the body, so the absent directory is intentional, not missing progressive disclosure.

---

## Workflow

### Phase 1 — Discover

Glob for all SKILL.md files, run from the repo root. Skills live one level deep under `skills/`:

```
pattern: skills/*/SKILL.md
```

Collect the directory name of each match — that's the skill name.

To detect skipped directories: also Glob `skills/*/` to list every skill directory. Any directory in the `skills/*/` result that is not in the `skills/*/SKILL.md` result has no SKILL.md — list it in the Skipped section of the report with reason "No SKILL.md found".

If zero SKILL.md files found: output "No skills found in this repo." and stop.

### Phase 2 — Evaluate

For each discovered skill, in order:

1. Read the SKILL.md file at its absolute path.
2. Invoke `/skill-forge-judge` on it.
3. From the judge output, extract and record:
   - Skill name
   - Grade (A/B/C/D/F)
   - Score (X/Y, Z%)
   - Numbered Improvements: up to 5 items (all if fewer than 5 exist)

Emit a one-line status per skill as each evaluation completes — do not wait until all are done:
```
✓ skill-forge-create   B  (98/120, 82%)
✓ skill-forge-hitl     C  (90/120, 75%)
```

If `/skill-forge-judge` is not installed: output "skill-forge-judge is required — install it before running skill-forge-audit." and stop.

If N > 10: output "About to run N skill-forge-judge evaluations — this may take several minutes. Proceed? (y/n)" and stop if denied.

If a skill's judge run errors: record `ERR` and the error message for that skill; continue to the next skill. Do not abort the audit.

### Phase 3 — Render Report

Before rendering, ask: does every layout decision put highest-priority work at the top? If the Needs Work section is empty, lead with a one-sentence "All skills passing" summary instead of an empty header.

Sort results by grade ascending: F → D → C → B → A. Worst grades appear first — the report is a priority queue, not an alphabetical list.

Split skills into two groups:
- **Needs Work**: grade below B (< 80%)
- **Passing**: grade B or above (≥ 80%)

For the `<YYYY-MM-DD>` report header, use the current date already present in the session context — do not shell out for it (`$(date)` and command substitution trigger a permission prompt under this repo's bash rules).

Output a single markdown report:

````markdown
# Skill Forge Audit
_<YYYY-MM-DD> — <N> skills evaluated_

## Grade Summary

| Skill | Grade | Score |
|-------|-------|-------|
| skill-forge-X | F | 55/120 (46%) |
| skill-forge-Y | C | 78/120 (65%) |
| skill-forge-Z | B | 98/120 (82%) |

## Needs Work

### skill-forge-X — F (55/120, 46%)

1. <improvement 1 from judge>
2. <improvement 2>
3. <improvement 3>

### skill-forge-Y — C (78/120, 65%)

1. <improvement 1>
2. <improvement 2>

## Passing (B+)

| Skill | Grade | Score |
|-------|-------|-------|
| skill-forge-Z | B | 98/120 (82%) |

## Skipped

| Directory | Reason |
|-----------|--------|
| some-dir  | No SKILL.md found |
````

If all skills pass: omit the "Needs Work" section entirely.
If no skills pass: omit the "Passing" section.
If nothing was skipped: omit the "Skipped" section.

---

## NEVER

- **NEVER display full judge reports inline for each skill**
  **Instead:** Extract only grade, score, and top 1–5 numbered improvements per skill.
  **Why:** Unfiltered judge output for 6+ skills floods the context window and buries the aggregate signal the report exists to surface.

- **NEVER apply any fixes during an audit run**
  **Instead:** Output the report only. Direct the user to `/skill-forge-hitl` or `/skill-forge-update` for remediation.
  **Why:** Mixing diagnosis with treatment makes it impossible to know what the baseline was — the audit's value is the before-state snapshot.

- **NEVER sort by skill name or alphabetically**
  **Instead:** Sort by grade ascending (F first, A last) within each section.
  **Why:** Alphabetical sort buries the worst skills; the report's job is to surface where effort is needed most.

- **NEVER read SKILL.md files via `~/.claude/skills/` paths**
  **Instead:** Use the absolute path to the skills project directory (the repo root where this audit runs).
  **Why:** `~/.claude/skills/` is a symlink back to the project; Claude Code's permission system fires on symlink traversal and interrupts the audit mid-run with a permission prompt.

- **NEVER abort the audit when a single skill errors**
  **Instead:** Record `ERR` for that skill and continue to the next one.
  **Why:** A failed judge run on one skill should not discard results already collected for the others — partial results are more useful than none.
