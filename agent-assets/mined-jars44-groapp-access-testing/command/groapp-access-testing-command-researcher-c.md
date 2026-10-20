---
description: Researcher C — Form validation and error states
agent: researcher
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Researcher-C** agent. Explore codebase for form validation and error states.

## Scope

Focus: **Form validation rules, error states, error messages, input constraints**
Source: `../groapp-access/src/features/{feature}/presentation/`

## Steps

1. Read `.agent/state.json` — confirm phase=research, feature={feature}
2. Read user story / PRD / AC for {feature} — understand scope
3. Find validators: scan forms for validation rules, error messages, input constraints
4. **Write findings to `.agent/tasks/researcher-validators-{YYYYMMDDHHMMSS}-{seq}.json` (MANDATORY — do this BEFORE returning)**
5. Update assigned TC todo files: [ ] → [/] → [x] with evidence
6. Return file:line summary to parent agent

## Output Format

```json
{
  "agent": "researcher-validators",
  "variant": "C",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "validators": [
    {
      "field": "email",
      "type": "input",
      "rules": ["required", "email: true", "maxLength: 255"],
      "error_message": "Email tidak valid",
      "error_locator": "email-error-message",
      "file": "src/features/auth/presentation/pages/login/login.page.tsx",
      "line": 55,
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
- Out of scope: API endpoints, route definitions, component selectors.
