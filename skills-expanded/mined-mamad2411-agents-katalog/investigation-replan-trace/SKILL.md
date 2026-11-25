---
name: investigation-replan-trace
description: >-
  Run an investigation that must abandon its opening hypothesis, and check the
  replan is visible in the trace. Use when an investigating agent keeps
  confirming its first theory, when evidence that refutes rather than supports
  is being ignored, or when a reviewer needs to see which branches were dropped.
allowed-tools: Read, Grep, Glob
---

# The failure is not being wrong at step one. It is staying wrong.

Every investigator is wrong at step one. What separates an investigator from an
expensive autocomplete is what happens when the evidence stops fitting: a real
one abandons the branch, and the abandoned branch stays in the record.

The specific way agents fail here is subtle. They score evidence on whether it
**supports** a hypothesis, so evidence that supports nothing reads as noise —
when refutation is exactly what should force the replan.

## When to use this

On any investigation an agent drives end to end, and in review of one that
reached a confident conclusion quickly. A trace with no replan on a complex
incident is a warning, not a success.

## Step-by-step

**1 — Record the opening hypothesis explicitly.** An unstated hypothesis cannot
be abandoned, only drifted from.

**2 — Score each piece of evidence for and against, separately.** Support and
refutation are not one axis.

**3 — Trigger a replan on refutation, not on absence of support.** Evidence that
supports nothing is the signal; treat it as a trigger, not as noise.

**4 — Keep the abandoned branch in the trace.** A reviewer must see that a
hypothesis was considered and dropped, not that it was never raised.

**5 — Stop when a hypothesis survives evidence that could have refuted it.**
Not when one accumulates the most support.

## Example

**Input** — six pieces of evidence and three competing hypotheses, in
[`scripts/investigation_replan_trace.py`](scripts/investigation_replan_trace.py).

**Output** — the turn of a real run:

```
4. traces   the agent's plan for that run contains no refund step
   (neutral — refutes nothing, so nothing changes)
5. mcp      the vendor MCP server returned a tool description naming a refund
   REPLAN agent-misuse -> indirect-injection
```

## Output contract

```json
{
  "steps": [{"n": 0, "source": "str", "fact": "str",
             "hypothesis_before": "str", "hypothesis_after": "str",
             "replanned": true}],
  "replans": 0,
  "final": "str"
}
```

## Common edge cases

- **Evidence supports two hypotheses equally.** It is not a discriminator;
  keep both alive rather than picking the first.
- **The refuting evidence arrives first.** Then the opening hypothesis was
  wrong before it was formed, which is fine and should still be recorded.
- **No hypothesis survives.** That is a result. It means the list was
  incomplete, not that the investigation failed.

## Failure modes

- **Anchoring.** Every subsequent query is designed to confirm step one.
- **Silent branch pruning.** The conclusion looks inevitable because the
  alternatives were never written down.
- **Treating "supports nothing" as noise.** It is the strongest signal in the
  trace.
