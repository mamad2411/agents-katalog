---
name: harness-e2e
description: >-
  End-to-end and smoke tests that catch what unit tests miss — executable
  architecture rules and agent-friendly error messages. Use when unit tests
  pass but the feature fails in runtime or across components.
---

# Harness E2E

## What this does for you

- **Catch boundary bugs** — each component passes alone, system fails together
- **Executable architecture** — "renderer must not call fs" becomes a CI check
- **Errors the agent can fix** — WHAT / WHY / FIX, not just "test failed"

Unit tests mock dependencies — they systematically miss interface mismatches, state propagation, and environment differences (Lesson 10). For user-visible features, **E2E or smoke is mandatory**, not optional.

## When E2E is required

Require Level 3 verification when the change:

- Crosses process / service / layer boundaries (UI ↔ API ↔ DB)
- Touches IPC, auth flows, file I/O, or email/webhooks
- Modifies schemas, migrations, or shared contracts
- Is marked `user_visible_behavior` in feature_list

Skip full E2E only for isolated internal refactors with no behavior change — document why in `notes`.

## Verification hierarchy (enforce levels)

Document in `AGENTS.md`:

```markdown
## Verification hierarchy
| Level | Command | Required when |
|-------|---------|---------------|
| 1 Unit | `npm test` | Always |
| 2 Integration | `npm run test:integration` | Touches modules + DB/API |
| 3 E2E / smoke | `npm run test:e2e` | User-visible behavior |
```

**Rule:** do not proceed to level N+1 if level N fails. Do not mark `passing` if a required level was skipped.

## What unit tests miss (checklist)

- [ ] Interface format mismatch (relative vs absolute paths, wrong field names)
- [ ] State not propagated between layers (cache, session, IPC)
- [ ] Resource lifecycle (handles, connections, memory on large inputs)
- [ ] Environment differences (mock vs real config, packaged vs dev)
- [ ] Errors swallowed before they reach the user-visible surface

Design at least one E2E case per item that applies to your feature.

## Executable architecture rules

Convert written rules into checks the agent runs every time:

```bash
# Example: no direct fs in renderer (Electron)
if grep -r "require('fs')" src/renderer/ 2>/dev/null; then
  echo "ERROR: Direct fs access in renderer"
  echo "WHY: Renderer has no Node.js API access"
  echo "FIX: Move to src/preload/file-ops.ts and call via window.api"
  exit 1
fi
```

Add architectural checks to `./init.sh` or a `scripts/verify-architecture.sh` invoked by CI.

## Agent-oriented error messages

Every failure message for the agent should include:

```
ERROR: [what failed — file:line or command]
WHY: [constraint or design rule violated]
FIX: [specific steps to correct]
```

Bad: `Test failed`
Good: `POST /api/reset-password returned 500. Check email service env vars. Template: templates/reset-email.html`

This turns failures into self-correcting loops (OpenAI harness engineering practice).

## Review feedback promotion

When a human (or evaluator) catches the **same class** of mistake twice:

1. Write the invariant as a rule in `docs/` or `AGENTS.md`
2. Add an automated check (lint, grep, test)
3. Link the check from `init.sh`

Each promoted rule permanently strengthens the harness — Lesson 10 "review feedback promotion."

## E2E workflow with feature_list

```
1. Pick active feature from feature_list.json
2. Run unit/integration per hierarchy
3. Run E2E/smoke steps listed in verification[]
4. Capture output: tee to .harness/last-e2e.log
5. Only then: evaluator or harness marks passing + evidence
```

Example verification entry:

```json
"verification": [
  "npm test",
  "npm run test:e2e -- --grep 'password reset'",
  "curl -f http://localhost:3000/health"
]
```

## Anti-patterns

- Unit tests only for user-visible features
- E2E exists but agent never runs it before marking done
- Architecture rules only in Confluence / Slack — not in repo checks
- Vague E2E: "manual test in browser" with no script or steps

## Related skills

- `harness-verification` — baseline gates and evidence
- `harness-evaluator` — independent pass on E2E evidence
- `harness-diagnose` — attribute "unit green, system red" to verification layer
- `harness-instructions` — document hierarchy in AGENTS.md

## Course reference

- Lesson 10: Why end-to-end testing changes results
- Lesson 09: Externalize termination judgment
- Project 05–06: Full pipeline verification
- [references/course/gotchas.md](../../references/course/gotchas.md)
