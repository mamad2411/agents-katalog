---
name: plan-audit-entry-per-step
description: Emit a structured audit dict on every planning iteration (loop count, tool budget, planned action count, rerouted flag, rerouted reason) and stash it in state so post-mortem analysis can replay every planner decision.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [audit, planner, observability, langgraph]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/plan_actions/node.py
imported_at: 2026-04-18T00:00:00Z
---

# Plan Audit Entry per Loop Step

## When to use
Your agent has a planner that runs multiple times (one per loop iteration). When it misbehaves, you want to know exactly what was decided, with what budget, and whether the planner rerouted to a different source family. Logging via `print` makes this lossy; you want a typed dict in state.

## How it works
- A `PlanAudit` TypedDict declares the audit shape: `loop`, `tool_budget`, `planned_count`, `rerouted`, optional `reroute_reason`.
- Every planning node populates it before returning.
- Downstream nodes (e.g. `investigate`) read the audit so summaries can include "loop 2: planner re-routed from grafana to datadog because Grafana returned no logs".

## Example
```python
class PlanAudit(TypedDict, total=False):
    loop: int
    tool_budget: int
    planned_count: int
    rerouted: bool
    reroute_reason: str

def node_plan_actions(state):
    loop_count = state.get("investigation_loop_count", 0)
    plan, available_sources, available_action_names, _, rerouted, reroute_reason = build_plan_actions(...)
    audit_entry: PlanAudit = {
        "loop": loop_count,
        "tool_budget": input_data.tool_budget,
        "planned_count": len(plan.actions if plan else []),
        "rerouted": rerouted,
    }
    if rerouted:
        audit_entry["reroute_reason"] = reroute_reason
    return {
        "planned_actions": plan.actions if plan else [],
        "plan_rationale": plan.rationale if plan else "",
        "available_sources": available_sources,
        "available_action_names": available_action_names,
        "plan_audit": audit_entry,
    }
```

## Gotchas
- Use `TypedDict(total=False)` so you can omit optional fields without forcing a sentinel value.
- Don't accumulate the entire history in state — keep only the most recent `plan_audit`. The full history can be reconstructed from LangSmith traces or LangGraph's checkpoint table.
- Surface the audit in the final report so users can self-debug ("agent looped 3 times because Grafana returned no logs" is more actionable than "couldn't find root cause").
