---
name: mj-plan
description: "Majordomus plan: Reserve the next issue, case or ADR number; How far each issue's work has travelled; Where the plan's stamps contradict the delivered work; Where the work is now; The issues, filtered by what the graph derived; The whole derived plan; The one issue to take now; One milestone or…"
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:plan; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `plan`

The capabilities the Majordomus registry declares in its module `plan`. Choose the one that answers the request below — or, without one, the person's last request about `plan` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `plan.allocate` | Reserve the next issue, case or ADR number | `majordomus_plan_allocate` | — | changes |
| `plan.delivery` | How far each issue's work has travelled | `majordomus_plan_delivery` | `majordomus plan delivery` | reads |
| `plan.drift` | Where the plan's stamps contradict the delivered work | `majordomus_plan_drift` | `majordomus plan drift` | reads |
| `plan.flight` | Where the work is now | `majordomus_plan_flight` | — | reads |
| `plan.issues` | The issues, filtered by what the graph derived | `majordomus_plan_issues` | — | reads |
| `plan.model` | The whole derived plan | `majordomus_plan` | — | reads |
| `plan.next` | The one issue to take now | `majordomus_plan_next` | — | reads |
| `plan.record` | One milestone or issue, with everything derived about it | `majordomus_plan_record` | — | reads |
| `plan.roadmap` | The milestones in derived order | `majordomus_plan_roadmap` | — | reads |
| `plan.status` | Where the plan stands | `majordomus_plan_status` | — | reads |
| `plan.transition` | Move one issue through the lifecycle | `majordomus_plan_transition` | — | changes |
| `plan.validate` | What the model refuses | `majordomus_plan_validate` | — | reads |
| `plan.waves` | What may run at the same time | `majordomus_plan_waves` | — | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
