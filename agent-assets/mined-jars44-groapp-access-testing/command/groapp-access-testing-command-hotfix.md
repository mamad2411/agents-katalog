---
description: Level 1 — Fast-track hotfix for single file fixes (< 3 TCs)
agent: lead
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the Lead Orchestrator. Execute a **fast-track hotfix** for micro-tasks.

## Steps

1. Confirm triage was run: `/triage` → level = hotfix
2. Read user's request — identify target file and fix scope
3. Dispatch **single Builder** agent with direct file path
4. Wait for Builder to complete
5. Run QA immediately: `.agent/hooks/test.sh test --grep "<target>" --reporter=list`
6. Output brief status message

## Output Format

```text
HOTFIX RESULT:
  File: {path/to/file}
  Fix: {one sentence}
  QA: {X/Y} tests passed
  Status: SUCCESS | FAILED
```

## Rules

- **Skip ALL planning docs** — no implementation-plan.md
- **Skip per-TC todos** — overhead not justified
- **Skip mandatory halt** — user requested direct fix
- **Skip full reflection cycle** — run QA immediately after Builder
- Still append errors to `.agent/state.json` if test fails
- Max 3 test files, max 3 TCs
- If scope exceeds hotfix limits → tell user to run `/triage` then `/mode-c` instead
