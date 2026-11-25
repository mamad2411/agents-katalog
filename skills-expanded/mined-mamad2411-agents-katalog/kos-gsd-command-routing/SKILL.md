---
name: kos-gsd-command-routing
description: Route an incoming @claude request to the correct GSD command (quick/debug/ship/capture/progress/execute/etc.) so the ad-hoc claude workflow does the right amount of process for the task.
user-invocable: true
when_to_use: "When responding to an @claude mention on an issue/PR/review and deciding which GSD skill or command handles it."
category: utilities
argument-hint: "[user request]"
keywords: [gsd, routing, claude, mention, quick, debug, ship, capture, progress]
related: [kos-claude-turn-budget, kos-zai-run-failure-prevention, kos-trigger-policy-trust-gate]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from claude.yml prompt routing rules + run behavior
  license: repo
  version: "1.0"
---

# Idea

The `claude` workflow answers `@claude` mentions with a fixed instruction: route to the right GSD command. Misdistribution is the core waste — a small fix run through full planning, or a bug run through quick-mode without diagnosis. This skill is the routing table: match the request to the lightest sufficient command, then stay inside the turn budget.

## When to invoke this skill directly

- An `@claude` request arrived and you are choosing the command.
- A request spans two intents and you must pick the primary.

## References

- `claude.yml` prompt (the routing instruction this operationalizes).
- GSD commands: `/gsd:quick` (small/ad-hoc), `/gsd:debug` (investigation/bugs), `/gsd:ship` (PR pipeline), `/gsd:capture` (ideas/notes), `/gsd:progress` (status), `/gsd:execute-phase` (planned phase), `/gsd:plan-phase` (planning).
- Repo coding standards (the prompt also enforces tests + TypeScript for new files).

## Communication Style

One line: request class → command + why. Then act.

## Core Principles

YAGNI / KISS / DRY. Pick the **lightest** command that covers the task. Do not invoke planning for a one-line fix; do not use quick for a multi-file feature.

## Routing table

| Request shape | Route to |
|---|---|
| "fix X", "X is broken", small concrete change | `/gsd:quick` (or `/gsd:debug` if root cause unknown) |
| Bug needing investigation | `/gsd:debug` |
| "ship this", "merge", "open PR" | `/gsd:ship` |
| "remember …", "note …", idea | `/gsd:capture` |
| "status", "where are we", "what's left" | `/gsd:progress` |
| Work scoped to an existing phase | `/gsd:execute-phase` |
| New feature needing design | `/gsd:plan-phase` (via discuss/spec first) |

## Your Approach

1. Classify the request (fix / investigate / ship / capture / status / phase / new).
2. Pick the lightest matching command.
3. State the choice, then execute within the turn budget ([[kos-claude-turn-budget]]).

## Process Flow (Authoritative)

1. Read the mention + surrounding issue/PR context.
2. Map to one routing-table row.
3. If two intents: primary command acts, note the secondary.
4. Execute; follow repo standards (tests, TS for new files).

## Output Format

```text
REQUEST CLASS: <class>  =>  COMMAND: /gsd:<x>  REASON: <short>
```

## Critical Constraints

- Never run full planning for a trivial fix; never quick-mode a deep bug.
- Respect the workflow `allowed-tools` — if a needed tool is missing, say so rather than improvising.
- If the request is ambiguous between two commands, state both and pick the lighter, don't ask unless high-reversibility risk.
