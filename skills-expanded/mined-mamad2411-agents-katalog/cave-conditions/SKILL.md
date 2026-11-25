---
name: cave-conditions
description: Program WHEN each agent may be messaged — conditions on messages, the GUARDRAILS of a leader-driven team run. Use to gate agents on runtime state: after these two respond, only when a flag holds, any predicate over the message log. THIS is what makes cave-teams programmable where Claude Code Teams' flow is fixed.
---

# Conditions — program WHEN each agent runs (the guardrails on messages)

Teams run **LEADER-DRIVEN**: a leader agent proposes each message; cave-teams CHECKS the proposal
against the conditions (the guardrails) before delivery. An invalid message is never delivered —
the leader is re-prompted with the error string and self-fixes. Conditions are predicates over the
team's MESSAGE LOG: `Condition = Callable[[List[TeamMessage]], bool]`.

## Native API (how you program)

```python
from cave_teams import (responded, after, when_flag, when_message, all_of, any_of, always,
                        Edge, register_condition, compile_to_edges, run_team, check_proposal)

edges = compile_to_edges(seq(a, par(b, c), d))      # the algebra compiles to the guardrails
# or hand-build an edge:
edges += [Edge(to="publisher", conditions=[when_flag("approved")])]     # only after approval
edges += [Edge(to="merge", conditions=[after("frontend", "backend")])]  # join — wait for BOTH
edges += [Edge(to="worker", conditions=[when_message(lambda m: m.kind == "flag")])]  # any rule

register_condition("qa_passed", after("qa"))         # name a condition for team configs
```

`run_team(team, task, leader, runtimes, team_dir)` enforces them: `check_proposal` blocks a message
to a non-member or an out-of-turn agent and re-prompts the leader with `{e}`. Re-dispatch to an
agent that already responded IS allowed (revision loops are the leader's call) — conditions
enforce ORDER, the leader decides.

**Not a `cave()` build-op** — conditions are the message state machine (a separate runtime axis),
not a composition Link. Two tiers: these CLOSED-WORLD checks (enforced mechanically) + OPEN-WORLD
`open_rules={agent: [str]}` (surfaced to the leader, assumed true when it proceeds).

## See also
`cave-branch` · `cave-gate` · `cave-teams`

Part of the **cave-teams** plugin — the language + full DSL is the **cave-teams** skill; drive any pattern from data with the **cave** skill.
