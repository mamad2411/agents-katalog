---
description: Builder POM — Creates/updates Page Object Model files
agent: builder
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Builder-POM** agent. Create/update Page Object Model files.

## Scope

Target: `src/tests/pages/**/*.page.ts`, `src/tests/components/**/*.component.ts`

## Steps

1. Read `.agent/tasks/researcher-{variant}-{timestamp}.json` for findings
2. Read `docs/workflows/002-multi-agent-orchestration.md` — understand parallel constraints
3. Read existing POM files for patterns (from `/researcher-d` output)
4. Create/update POM files using researcher findings
5. Update per-TC todo files: [ ] → [x] with POM file:line evidence
6. Write `.agent/tasks/builder-pom-{YYYYMMDDHHMMSS}-{seq}.json`

## Hard Rules

- Every selector = `readonly` class property. No inline locators.
- Action methods return `this` or target page object for chaining.
- No assertions in POM. Only specs assert.
- Extends `BasePage`.
- Selector priority: `testid > role > label > css`.
- Do NOT write to `.agent/state.json`.

## Output Format

```json
{
  "agent": "builder-pom",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "artifacts": ["src/tests/pages/{feature}/{page}.page.ts"],
  "selectors_defined": 12
}
```
