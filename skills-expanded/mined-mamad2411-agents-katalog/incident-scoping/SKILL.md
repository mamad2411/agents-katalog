---
name: incident-scoping
description: >-
  Scope an incident in which an agent was the actor — what it touched, what it
  changed, what it may have exfiltrated, and where containment must cut. Use
  when responding to an agent-involved incident, reconstructing what an
  autonomous system did, deciding what to revoke, or sizing notification
  obligations.
allowed-tools: Read, Grep, Bash
---

# Scoping an agentic incident

Scoping a human incident asks where someone logged in. Scoping an agentic one
asks what the agent **decided**, because a compromised agent's actions are all
individually authorised. Nothing looks anomalous at the authentication layer;
the anomaly is in the sequence.

## When to use this

Any incident where an agent, an automated pipeline, or an AI-driven tool
performed actions under investigation.

## Procedure

**1 — Fix the window.** Establish the first suspicious decision, not the first
alert. Work backwards from the earliest action you cannot explain; the trigger
is usually earlier than the detection by the length of one task loop.

**2 — Reconstruct the decision chain.** For the window, list every action with
the input that motivated it. The critical question is which input entered the
context from **outside the trust boundary** — a fetched page, an issue comment,
a dependency's README, a tool description. That input is the likely root cause,
and it is invisible if you only log tool calls and not their justification.

**3 — Separate authority from behaviour.** For each action ask: was it within
the agent's granted authority? Actions that were authorised but wrong tell you
the grant was too broad. Actions that exceeded authority tell you a control
failed. These lead to different fixes and must not be pooled.

**4 — Establish data reach.** What did the agent read, and where could it have
sent it? Reach is bounded by the agent's egress, not by what it appears to have
sent — a request body you cannot see is still reach. State reach and confirmed
exfiltration as separate numbers, and never let the smaller one stand in for
the larger in a notification decision.

**5 — Decide the containment cut.** Options, in increasing cost: revoke the
agent's credential, disable the trigger, quarantine the workload, disable the
whole class of agents. Choose by blast radius, not by convenience, and record
what the cut does **not** stop — sibling agents on the same shared service
account almost always survive a credential revocation aimed at one of them.

**6 — Preserve evidence the agent could alter.** If the agent can write to the
log store, the logs are not evidence. Snapshot first, then contain.

## Example

**Input** — the fixture committed at the top of [`scripts/incident_scoping.py`](scripts/incident_scoping.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
chain                     dana@corp → orchestrator → patch-agent → deploy-agent
scoped_last_actor_only    ['cluster-prod']
scoped_whole_chain        ['cluster-prod', 'queue-tasks', 'repo-core', 'repo-infra', 'repo-payments', 'vault-dev']
missed_by_naive_scoping   ['queue-tasks', 'repo-core', 'repo-infra', 'repo-payments', 'vault-dev']
undercount_factor         6.0

Scoping the last actor finds one cluster. The chain reached six
resources, including a payments repository and a dev vault.
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
  "window": {"first_suspicious_action": "str", "detected_at": "str", "gap_seconds": 0},
  "chain": [{"action": "str", "motivating_input": "str",
             "input_origin": "operator|internal|external_untrusted",
             "within_authority": true}],
  "root_cause": {"input": "str", "origin": "str", "why_trusted": "str"},
  "authority": {"authorised_but_wrong": 0, "exceeded_authority": 0},
  "data": {"reach": ["str"], "confirmed_exfiltration": ["str"], "egress_bounded_by": "str"},
  "containment": {"cut": "credential|trigger|workload|class",
                  "does_not_stop": ["str"], "evidence_snapshotted_first": true},
  "clock": {"regulatory_trigger": false, "basis": "str"}
}
```

## Failure modes

- **Scoping by authentication.** Every action was authenticated; that is the
  point.
- **Logging tool calls without their motivating input.** Root cause then cannot
  be established at all.
- **Reporting confirmed exfiltration as the scope.** Reach is the scope until
  proven otherwise.
- **Revoking one agent's token** when the identity is shared, and calling it
  contained.
- **Containing before snapshotting** a log store the agent can write to.
