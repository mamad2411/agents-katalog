---
description: Builder Specs — Creates/updates Playwright test spec files
agent: builder
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Builder-Spec** agent. Write Playwright test spec files.

## Scope

Target: `src/tests/specs/**/*.spec.ts`, `src/tests/data/**/*.data.ts`

## Steps

1. Read `.agent/tasks/researcher-{variant}-{timestamp}.json` for findings
2. Read POM files created by `/builder-pom` — use their selectors
3. Read `docs/workflows/002-multi-agent-orchestration.md` — understand parallel constraints
4. Create/update spec files using POM selectors
5. Update per-TC todo files: [ ] → [x] with spec file:line evidence
6. Write `.agent/tasks/builder-spec-{YYYYMMDDHHMMSS}-{seq}.json`

## Hard Rules

- Specs follow Arrange → Act → Assert pattern.
- Every test has at least one assertion.
- No `page.waitFor(ms)` — use auto-waiting, `waitForResponse`, `waitForURL`.
- No hardcoded test data — use factories from `src/tests/data/`.
- Use `test.describe('Feature Name', ...)` for grouping.
- Test names: `'should [behavior] when [condition]'`.
- Do NOT write to `.agent/state.json`.

## Output Format

```json
{
  "agent": "builder-spec",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "artifacts": ["src/tests/specs/{feature}/{feature}.spec.ts", "src/tests/data/{feature}.data.ts"],
  "tests_written": 5
}
```
