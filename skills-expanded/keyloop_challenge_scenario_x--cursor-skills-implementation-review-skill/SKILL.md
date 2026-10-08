---
name: implementation-review
description: >-
  Self-audits Unified Service Scheduler implementation against the approved
  feature plan, PRD/Design invariants, and .cursor/rules. Use after coding
  (PIV Validate), before marking a plan done, when the user asks for an
  implementation review / audit, or when re-auditing after a manual-test bug.
---

# Implementation Review Skill

## When

After [I] Implementation for a feature plan, on demand (“audit this against the plan”), or after fixing a bug found in **manual testing**.

## Inputs

- Approved `plans/[feature]-plan.md`
- Diff / files changed in this feature
- Relevant `.cursor/rules/*.mdc`

## Audit checklist

Copy and mark each item:

```text
Review Progress:
- [ ] Plan AC all satisfied (or explicitly deferred with reason)
- [ ] Tasks completed; no silent scope creep
- [ ] Architecture boundaries respected (no Prisma in controllers)
- [ ] If booking path touched: FOR UPDATE on VEHICLE + candidate BAYS + TECHS; lock order OK
- [ ] Half-open overlap; CONFIRMED-only occupancy
- [ ] Timezone/hours: Asia/Ho_Chi_Minh at app layer; entire interval fits
- [ ] Error codes/HTTP match Design §3.4
- [ ] Validation Strategy commands run (or blocked with clear reason)
- [ ] Tests added/updated per plan (esp. concurrency if in scope)
- [ ] No PRD non-goals introduced (cancel/Redis/auth/VIN create)
```

## Output format

```markdown
## Verdict: PASS | FAIL

### Findings
- 🔴 Critical: ...
- 🟡 Suggestion: ...
- 🟢 Note: ...

### Evolution actions (if FAIL)
- Bug fix: ...
- Rule update: create/update `.cursor/rules/<name>.mdc` → ...
- ai-log.md entry: yes/no
- Re-audit required: yes
```

## On PASS — Mandatory handoffs

1. **Manual testing checklist** — numbered steps the human can run (plan Validation Strategy + AC; PowerShell-friendly where env/copy differs). Cover install/compose/generate/build/test/start, health/Swagger/API demos in scope, and connectivity notes.
2. **Stop and wait** — ask the human to confirm manual checks passed. Do **not** emit commit commands yet.
3. **After human approval** — follow `git-commit-standards.mdc`: analyze tree, chunk atomically, output **PowerShell** `git add` / `git commit -m "..."` only (never execute commit).

## Evolution loop

Applies on Review Skill FAIL **and** when the human reports a bug during manual testing:

```text
Bug Found (AI audit OR human manual check)
   → Fix Bug (minimal correct change)
   → Update existing .mdc OR create a new focused .mdc
   → Log entry in ai-log.md
   → AI Audit again (re-run this skill + failed tests)
   → On PASS: new manual checklist → wait for approval → commit commands
```

Do not treat manual-test bugs as “notes only”; they enter the same evolution loop as audit failures.
