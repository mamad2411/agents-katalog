---
name: context-sentinel
description: Check whether the current session is approaching context limits. Routes to compact or handoff.
---

@markdownai v1.0

# Context Sentinel

Check session context health and apply the cascading relief protocol before quality degrades.

## Run

```bash
SCRIPTS="${WILLOW_FYLGJA_ROOT:-${WILLOW_ROOT:-~/github/willow-2.0}/willow/fylgja}/skills/scripts"
bash "$SCRIPTS/check_context.sh"
```

## Interpret and act

| Output         | Meaning                              | Action                                        |
| -------------- | ------------------------------------ | --------------------------------------------- |
| STATUS_OK      | prompt_count < 15                    | Continue normally                             |
| COMPACT_NOW    | prompt_count 15–25                   | Invoke the `strategic-compact` or `/compact` skill |
| HANDOFF_NOW    | prompt_count > 25                    | Write handoff, submit next task to queue, end session |
| POSTGRES_DOWN  | session_anchor reports postgres down | Fix infra before resuming KB-dependent work   |

## Cascade

```
Session start
    │
    ├─ STATUS_OK       → continue
    ├─ COMPACT_NOW     → `/compact` → re-check
    └─ HANDOFF_NOW     → /shutdown (context-critical mode) → end
```

## When to run

- Start of every session
- Every ~10 prompts during long sessions
- Before any large batch operation
- If responses feel slower or less coherent
