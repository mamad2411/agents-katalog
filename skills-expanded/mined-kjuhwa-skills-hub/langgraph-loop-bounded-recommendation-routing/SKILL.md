---
name: langgraph-loop-bounded-recommendation-routing
description: Bound an agent loop in LangGraph by inspecting recommendations + a loop counter + an availability flag in a single conditional, defaulting to "publish" so a routing exception never traps the agent in an infinite loop.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [langgraph, loop-control, safety, routing]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/pipeline/routing.py
imported_at: 2026-04-18T00:00:00Z
---

# Bounded Recommendation Loop in LangGraph

## When to use
Your agent has a "decide whether to loop again" step that depends on (a) the model still proposing follow-ups, (b) a hard iteration cap, and (c) the existence of any tools/actions left to run. You want a single function that handles all three plus failure-mode default to "publish" so a routing bug never causes spinning.

## How it works
The conditional reads three pieces of state — `investigation_recommendations`, `investigation_loop_count`, `available_action_names` — and picks `"investigate"` only when all gates pass. Any exception in the predicate is logged and resolves to `"publish"`, terminating the loop safely.

## Example
```python
MAX_INVESTIGATION_LOOPS = 4

def should_continue_investigation(state) -> str:
    try:
        recs = state.get("investigation_recommendations", [])
        loop_count = state.get("investigation_loop_count", 0)
        available = state.get("available_action_names", [])

        if not available:
            return "publish"               # no tools left -> stop
        if loop_count > MAX_INVESTIGATION_LOOPS:
            return "publish"               # hard cap
        if recs:
            return "investigate"           # model wants more evidence
        return "publish"
    except Exception as e:
        logger.exception("routing failed: %s", e)
        return "publish"                   # safety: never loop on error
```

## Gotchas
- `loop_count` must be incremented inside the diagnose node; the routing function only reads it.
- Always default to the "exit" branch in the exception handler — never re-enter the loop on uncertainty.
- The "no available actions" check is a safety net for runs where integrations were dropped mid-flight; without it the planner may keep returning empty plans.
