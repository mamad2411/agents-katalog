---
description: Reflector POM — Critiques POM structure before QA
agent: reflector
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Reflector-POM** agent. Critique POM structure.

## Scope

Target: POM files from `/builder-pom` (`src/tests/pages/**/*.page.ts`, `src/tests/components/**/*.component.ts`)

## Steps

1. Read `.agent/tasks/builder-pom-{timestamp}.json` — know what was built
2. Read `.agent/plans/implementation-plan-{feature}.md` — know expected scope
3. Read POM files from Builder-POM
4. Check against constitutions 001-004
5. **Write findings to `.agent/tasks/reflector-{YYYYMMDDHHMMSS}-{seq}.json` (MANDATORY — do this BEFORE returning)**
6. Return critique summary with verdict + file:line evidence.

## POM Critique Checklist

### Constitution 001 (POM Architecture)

- [ ] Page Object extends BasePage?
- [ ] All selectors = `readonly` class properties?
- [ ] No inline locators in spec files?
- [ ] Action methods return `this` or target page?
- [ ] No assertions in POM?
- [ ] Component POMs used for shared UI?

### Constitution 002 (Coding Standards)

- [ ] Selector priority: testid > role > label > css?
- [ ] No `xpath()`?

### Constitution 003 (Anti-Hallucination)

- [ ] All selectors source-verified against actual component JSX?

## Output Format

```json
{
  "agent": "reflector-pom",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "sub_cycle": "pom",
  "reflection_cycle": 1,
  "max_cycles": 3,
  "verdict": "pass | revise",
  "findings": [
    {
      "tc_id": "TC-001",
      "sub_cycle": "pom",
      "severity": "error | warning | info",
      "category": "selector | architecture",
      "file": "src/tests/pages/{feature}/{page}.page.ts",
      "line": 25,
      "problem": "Missing readonly on selector",
      "suggestion": "Add readonly keyword"
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
