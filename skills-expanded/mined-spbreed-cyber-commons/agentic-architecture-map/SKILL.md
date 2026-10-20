---
name: agentic-architecture-map
description: >-
  Draw a vendor-neutral map of an agentic system — ingress, orchestrator, agent
  runtime, model, tools and MCP, memory and knowledge, messaging, egress — and
  mark the edges where trust changes. Use before naming any risk, because a risk
  with no component is an argument.
allowed-tools: Read, Grep, Glob
---

# Draw it before you argue about it

Every disagreement about agentic security is really a disagreement about which
system is being discussed. The map fixes that: nine components and the edges
between them, drawn the same way every time, so a risk can be pinned to a box
and a control can be pinned to an edge.

## When to use this

First. Before threat modelling, before writing a risk register, and before any
conversation that contains the phrase "secure the agent".

## Procedure

**1 — Place the nine components.** Ingress, orchestrator, agent runtime, model,
tools, MCP servers, memory and knowledge, agent-to-agent messaging, egress. Draw
every one even if a system has only a stub of it — an absent box is a decision,
not a gap in the diagram.

**2 — Draw the edges as data flow, not as call direction.** Where text goes is
what matters; who initiated the call is an implementation detail that hides
whether untrusted content reaches the model.

**3 — Mark the trust level of each component.** Which ones receive content from
outside the boundary, and which ones hold authority. The edge from a lower trust
level to a higher one is a boundary crossing, and there are always more of them
than expected.

**4 — Annotate each edge with what crosses it.** User text, retrieved documents,
tool results, peer messages, credentials. This is what turns the picture into
something a threat model can walk.

**5 — Name the components that do not exist yet.** A system with no gateway and
no messaging is a smaller map, and saying that explicitly stops a later
conversation about controls for components nobody has.

## Example

**Input** — the fixture committed at the top of [`scripts/agentic_architecture_map.py`](scripts/agentic_architecture_map.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

```
9 components, 8 present at CyberTravels
   component        trust  authority  present
   agent runtime        2        yes  yes
   egress               3        yes  NO
   ingress              0          -  yes
   knowledge            0          -  yes
   mcp servers          1        yes  yes
   messaging            2          -  yes
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "components": [{"name": "str", "present": true, "trust": 0, "holds_authority": false}],
  "edges": [{"from": "str", "to": "str", "carries": ["str"], "boundary_crossing": false}],
  "crossings": 0,
  "absent": ["str"]
}
```

## Failure modes

- **Drawing call direction.** It hides where untrusted content arrives.
- **Omitting components a system does not have.** Their absence is information.
- **A map with no trust levels.** Then no edge is a boundary and the diagram is
  decoration.
