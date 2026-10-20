---
name: llm-empty-plan-controller-fallback
description: When a planning LLM returns an empty action list, force a deterministic verification action from a priority-ordered fallback list so the agent never spins on "no actions chosen".
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [planning, fallback, llm-defense, agent-loop]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/plan_actions/node.py
imported_at: 2026-04-18T00:00:00Z
---

# LLM Empty-Plan Controller Fallback

## When to use
Your planning LLM occasionally returns `actions: []` (e.g. for healthy or sparse alerts), which would route the agent into a no-op loop. You want the controller to seed at least one verification action so the agent makes progress and either gathers evidence or proves there's nothing to gather.

## How it works
- After parsing the LLM plan, if `planned_actions` is empty AND there are `available_action_names` (so we *can* do something), iterate a curated fallback list (most-broadly-useful queries first).
- Pick the first fallback that's available; record it with a clear rationale ("Controller fallback: LLM returned empty plan...").
- If none of the curated fallbacks are available, just take `available_action_names[0]`.

## Example
```python
if not planned_actions and available_action_names:
    fallback_candidates = [
        "query_grafana_metrics", "query_grafana_logs",
        "query_datadog_all", "query_datadog_logs",
        "query_honeycomb_traces", "query_coralogix_logs",
        "get_cloudwatch_logs", "get_host_metrics",
        "list_eks_pods", "get_eks_events",
    ]
    for candidate in fallback_candidates:
        if candidate in available_action_names:
            planned_actions = [candidate]
            plan_rationale = "Controller fallback: LLM returned empty plan. Forcing verification action."
            break
    if not planned_actions:
        planned_actions = [available_action_names[0]]
        plan_rationale = "Controller fallback: LLM returned empty plan. Forcing available verification action."
```

## Gotchas
- Pair this with a hard loop cap — if the fallback action returns no useful evidence and the LLM keeps returning empty, you still need an upper bound to terminate.
- The fallback list ordering matters: prefer high-signal/low-cost queries first.
- Always set `plan_rationale` to a string the user will see in traces; "controller fallback" is honest and easy to grep for in production.
