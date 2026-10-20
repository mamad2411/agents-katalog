---
description: Researcher B — UI components and selectors
agent: researcher
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Researcher-B** agent. Explore codebase for UI components and selectors.

## Scope

Focus: **UI components, selectors, testids, aria-labels, CSS classes**
Source: `../groapp-access/src/features/{feature}/presentation/pages/`

## Steps

1. Read `.agent/state.json` — confirm phase=research, feature={feature}
2. Read user story / PRD / AC for {feature} — understand scope
3. Scan components: find `data-testid`, `aria-label`, `getByRole`, `getByLabel`, CSS selectors
4. **Write findings to `.agent/tasks/researcher-components-{YYYYMMDDHHMMSS}-{seq}.json` (MANDATORY — do this BEFORE returning)**
5. Update assigned TC todo files: [ ] → [/] → [x] with evidence
6. Return file:line summary to parent agent

## Selector Priority

```text
1. data-testid (most reliable)
2. aria-label / aria-role
3. getByRole / getByLabel
4. CSS class / selector
5. XPath (LAST resort)
```

## Output Format

```json
{
  "agent": "researcher-components",
  "variant": "B",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "selectors": [
    {
      "page": "LoginPage",
      "component": "EmailInput",
      "name": "emailInput",
      "type": "testid | role | label | css",
      "value": "login-email-input",
      "file": "src/features/auth/presentation/pages/login/login.page.tsx",
      "line": 42,
      "confidence": "verified"
    }
  ]
}
```

## Rules

- **Never modify groapp-access source code or test scripts.** Read only for application files.
- Write findings to `.agent/tasks/researcher-{variant}-{ts}.json`, update `.agent/plans/todos/tc-*.md`, and write to `.agent/memory/entities/*.json` only.
- Return file:line for every finding.
- Confidence: `verified` (saw in JSX) vs `inferred` (from type).
- No suggestions — only facts.
- Do NOT write to `.agent/state.json`.
- Out of scope: API endpoints, backend logic.
