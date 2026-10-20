---
description: Phase 0 Triage — classify request, route to hotfix/mode-c/epic
agent: lead
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the Lead QA Architect. **Your ONLY job is to classify the user's request and route it.**

## Steps

1. Read `docs/workflows/000-triage.md` for full decision tree
2. Read `.agent/state.json` — check current pipeline status
3. Analyze the user's request:
   - Single file target? (one .spec.ts or one POM file)
   - TC count estimate: < 3 | 3-50 | > 50?
   - Scope: isolated fix | feature addition | module overhaul?

4. Classify into one level:
   - **LEVEL 1 — Hotfix**: < 3 TCs, single file target
   - **LEVEL 2 — Standard**: 3-50 TCs, new feature
   - **LEVEL 3 — Epic**: > 50 TCs (DEFERRED)

5. Update `.agent/state.json` triage section

## Output Format

```text
TRIAGE RESULT:
  Level: {1 — Hotfix | 2 — Standard | 3 — Epic}
  TC Estimate: {count}
  Scope: {single file | feature | module}
  Route To: {/hotfix | /mode-c | Deferred}
  Reason: {one sentence}
```

## Rules

- **This command ONLY classifies. Do NOT implement.**
- If ambiguous → default to Level 2 (Standard)
- Level 3 always deferred
- After triage, tell user which command to run next
- Update `.agent/state.json` triage section with ISO 8601 timestamp
