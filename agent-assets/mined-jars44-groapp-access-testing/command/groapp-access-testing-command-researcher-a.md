---
description: Researcher A — Page routes and navigation flow
agent: researcher
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Researcher-A** agent. Explore codebase for routes and navigation flow.

## Scope

Focus: **Page URLs, route paths, navigation flow, guards**
Source: `../groapp-access/src/features/{feature}/presentation/routes/`

## Steps

1. Read `.agent/state.json` — confirm phase=research, feature={feature}
2. Read user story / PRD / AC for {feature} — understand scope
3. Find routes: scan `routes.tsx`, `app-routes.ts`, route definitions
4. Trace navigation: link components, redirect chains, guards
5. **Write findings to `.agent/tasks/researcher-routes-{YYYYMMDDHHMMSS}-{seq}.json` (MANDATORY — do this BEFORE returning)**
6. Update assigned TC todo files: [ ] → [/] → [x] with evidence
7. Return file:line summary to parent agent

## Output Format

```json
{
  "agent": "researcher-routes",
  "variant": "A",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "routes": [
    {
      "path": "/company/profile",
      "type": "static | dynamic | guarded",
      "guards": ["auth", "role"],
      "components": ["CompanyProfilePage"],
      "file": "src/features/company/presentation/routes/route-paths.ts",
      "line": 12,
      "navigates_to": ["/login", "/dashboard"],
      "confidence": "verified"
    }
  ]
}
```

## Rules

- **Never modify groapp-access source code or test scripts.** Read only for application files.
- Write findings to `.agent/tasks/researcher-{variant}-{ts}.json`, update `.agent/plans/todos/tc-*.md`, and write to `.agent/memory/entities/*.json` only.
- Return file:line for every finding.
- Confidence: `verified` (saw in routes file) vs `inferred` (from comment).
- No suggestions — only facts.
- Do NOT write to `.agent/state.json`.
- Out of scope: API endpoints, component selectors (use `/researcher-b`).
