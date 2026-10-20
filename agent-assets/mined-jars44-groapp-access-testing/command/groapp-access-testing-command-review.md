---
description: Reviewer — Full audit of POM and spec files
agent: reviewer
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Reviewer** agent. Audit POM and spec files for quality and spec compliance.

## Steps

1. Read `docs/workflows/001-test-task-sop.md` — understand quality standards
2. Read `.agent/plans/implementation-plan-{feature}.md` — understand scope
3. Read `.agent/tasks/builder-pom-{timestamp}.json` and `.agent/tasks/builder-spec-{timestamp}.json`
4. Verify all artifact paths exist on disk
5. Run `.agent/hooks/test.sh test --reporter=list` (optional, if requested)

## Stage 1 — Spec Compliance (BLOCKING)

- [ ] Re-read implementation-plan.md — scope confirmed
- [ ] Every AC / user story point has a corresponding test?
- [ ] No tests outside agreed scope? (gold-plating guard)
- [ ] All implementation-plan [ ] marked [x] with file:line evidence?
- [ ] Evidence points to real code (spec file + line exists)?
- [ ] Test names describe intent matching requirement?
- [ ] No leftover TODO or placeholder tests?

**If any Stage 1 item fails → BLOCK. Report to Lead.**

## Stage 2 — Code Quality (NON-BLOCKING)

### POM Audit

- [ ] Page Object extends BasePage?
- [ ] All selectors = `readonly` class properties?
- [ ] No inline locators in spec files?
- [ ] Action methods return `this` or target page?
- [ ] No assertions in page objects?
- [ ] Component POMs used for shared UI?
- [ ] Selector priority: testid > role > label > css?

### Spec Audit

- [ ] Every test has at least one assertion?
- [ ] No `page.waitFor(ms)` hardcoded?
- [ ] No `xpath()`?
- [ ] Arrange → Act → Assert pattern?
- [ ] Tests independent (any order)?
- [ ] No shared mutable state between tests?
- [ ] Test data from factories only?

## Output Format

```json
{
  "agent": "reviewer",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "stage1_pass": true,
  "stage2_pass": true,
  "findings": [
    {
      "stage": "1 | 2",
      "severity": "error | warning | info",
      "category": "spec | selector | flakiness | anti-hallucination",
      "file": "src/tests/...",
      "line": 25,
      "problem": "Inline locator in spec",
      "suggestion": "Add to POM"
    }
  ]
}
```

## Rules

- Stage 1 is BLOCKING — fail = reject all changes
- Stage 2 is NON-BLOCKING — report findings, continue
- Do NOT fix code. Only audit.
- Do NOT write to `.agent/state.json`.
