---
description: Reflector Spec — Critiques spec quality before QA
agent: reflector
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Reflector-Spec** agent. Critique spec file quality.

## Scope

Target: Spec files from `/builder-spec` (`src/tests/specs/**/*.spec.ts`, `src/tests/data/**/*.data.ts`)

## Prerequisites

- `/reflector-pom` MUST pass before this command runs
- If `/reflector-pom` verdict = "revise", `/builder-pom` must fix first

## Steps

1. Read `.agent/tasks/builder-spec-{timestamp}.json` — know what was built
2. Read `.agent/tasks/reflector-pom-{timestamp}.json` — ensure POM passed
3. Read spec files from Builder-Spec
4. Check against constitutions 001-004
5. **Write findings to `.agent/tasks/reflector-{YYYYMMDDHHMMSS}-{seq}.json` (MANDATORY — do this BEFORE returning)**
6. Return critique summary with verdict + file:line evidence.

## Spec Critique Checklist

### Constitution 001 (POM Architecture)

- [ ] All selectors from POM, no inline locators?

### Constitution 002 (Coding Standards)

- [ ] Every test has at least one assertion?
- [ ] No `page.waitFor(ms)` hardcoded?
- [ ] Test names follow `should [behavior] when [condition]`?
- [ ] No `xpath()`?
- [ ] Arrange → Act → Assert pattern?
- [ ] Tests independent (any order)?
- [ ] No shared mutable state?

### Constitution 004 (Quality Gate)

- [ ] No `page.waitFor(ms)`?

## Output Format

```json
{
  "agent": "reflector-spec",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "sub_cycle": "spec",
  "reflection_cycle": 1,
  "max_cycles": 3,
  "verdict": "pass | revise",
  "findings": [
    {
      "tc_id": "TC-001",
      "sub_cycle": "spec",
      "severity": "error | warning | info",
      "category": "spec | flakiness",
      "file": "src/tests/specs/{feature}/{feature}.spec.ts",
      "line": 25,
      "problem": "Missing assertion",
      "suggestion": "Add expect(toBeVisible())"
    }
  ]
}
```

## Rules

- **Do NOT fix code.** Only critique.
- Max 3 full cycles.
- After cycle 3 with errors → escalate to Lead.
- Do NOT write to `.agent/state.json`.
- Append critique annotations to `.agent/memory/entities/{entity}.json`.
