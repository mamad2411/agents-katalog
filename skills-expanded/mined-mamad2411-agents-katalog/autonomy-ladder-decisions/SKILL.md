---
name: autonomy-ladder-decisions
description: >-
  Approve or refuse an autonomy request against the rung its blast radius and
  gating actually support, rather than approving the tool it wants. Use when
  agents are being promoted to act unattended.
allowed-tools: Read, Grep, Glob
---

# Govern the rung, not the tool

Approving tools one at a time produces an agent nobody approved: each tool was
reasonable, and the combination acts unattended on production. Governing the
**rung** asks a different question — what does this agent's blast radius and
gating support — and the answer is computed rather than negotiated.

## When to use this

Every request to raise an agent's autonomy, and as a periodic re-check, because
tools accumulate.

## Procedure

**1 — Publish the ladder.** L1 suggests, L2 acts in a sandbox, L2.5 acts with
approval on irreversible actions, L3 acts unattended. With, for each rung, the
governance and the budget it requires.

**2 — Compute the request's blast radius.** Reachable resources weighted by
scope, with gated actions discounted. Ungated writers are what usually decide
the outcome.

**3 — Derive the supported rung from the radius and the gating,** not from the
requester's ask. Then compare. The gap is the conversation.

**4 — Refuse with the condition attached.** "Refused at L2 for ungated writers"
tells the requester what to change. A bare refusal produces an appeal; a
conditional one produces a pull request.

**5 — Re-evaluate on tool change.** A rung approved with three tools does not
carry over to five. Make the tool manifest the trigger for re-evaluation.

## Example

**Input** — the fixture committed at the top of [`scripts/autonomy_ladder_decisions.py`](scripts/autonomy_ladder_decisions.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
L1   self-service  budget   0  register it; no further review
                   Assist — model proposes, a human performs every action.
L2   lightweight   budget   0  named owner + approval gate on every writer
                   Act with approval — model calls tools, a human approves each call.
L2.5 governed      budget  20  risk tier + blast budget + drift monitoring + tested stop
                   Act within a blast radius — pre-approved tools, bounded scope, review after.
L3   board         budget  60  all of L2.5 + held-out eval per release + board sign-off
                   Autonomous — model acts and self-verifies; humans see aggregates.
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
  "ladder": [{"rung": "str", "governance": "str", "budget": "str"}],
  "requests": [{"name": "str", "asked": "str", "tools": ["str"], "gated": ["str"],
                "blast": 0, "supported": "str", "verdict": "approved|refused", "condition": "str|null"}],
  "reevaluate_on": ["tool added", "scope widened", "model changed"]
}
```

## Failure modes

- **Approving tools.** The combination is what acts.
- **A bare refusal.** Nobody knows what to fix.
- **No re-evaluation trigger.** The manifest grows and the rung does not move.
