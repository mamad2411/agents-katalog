---
name: agent-registry-gap-check
description: >-
  Compare the agents actually present in an environment against the agents
  anybody registered, and establish what work and which tokens the unregistered
  ones are handed. Use when agents are created programmatically, when a
  discovery protocol is in play, or when asked how a worker joins a fleet.
allowed-tools: Read, Grep, Glob
---

# Discovery is not admission

A topology that discovers its workers will discover whatever answers. The
defect is not that an unknown agent exists — it is that the orchestrator hands
it the same delegated work, and the same narrowed user token, as a registered
one. The unregistered agent then acts **as the user** against anything
downstream that honours the token.

## When to use this

Any fleet where agents register themselves, are discovered over a network, or
are spawned by other agents. Also after adding a marketplace, a plugin
mechanism or an A2A-style protocol.

## Procedure

**1 — Enumerate what is present.** Ask the runtime, not the design document:
running workloads, connected clients, queue consumers, whatever the discovery
mechanism itself returns.

**2 — Enumerate what is registered.** The list somebody maintains, with owners.
Both lists in hand, the gap is arithmetic.

**3 — Follow a delegation.** For one task, record which agents received work
and what credential travelled with it. The question is whether registration is
consulted *before* delegation or only reported afterwards.

**4 — Establish what the token permits.** A narrowed on-behalf-of token in the
hands of an unregistered agent is a user session with no login. Name the
downstreams that would honour it.

**5 — Separate admission from identity.** Registration answers "should this
agent exist"; workload identity answers "is this the agent it claims to be".
Report which of the two is missing, because they are different projects.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_registry_gap_check.py`](scripts/agent_registry_gap_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
agent                 in registry?  approved?  received work?
pricing-agent         True          True       yes
billing-agent         True          True       yes
reporting-agent-v2    False         False      yes

agents that received delegated work : 3
of which unregistered               : 1
   reporting-agent-v2 now holds obo:dana@corp:reports:read,reports:write
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
  "present": ["str"],
  "registered": ["str"],
  "gap": ["str"],
  "delegations": [{"agent": "str", "registered": false, "credential": "str"}],
  "token": {"kind": "str", "acts_as_user": true, "honoured_by": ["str"]},
  "missing": {"admission": true, "workload_identity": true}
}
```

## Failure modes

- **Reading the registry as the inventory.** The registry is the claim; the
  runtime is the fact.
- **Treating discovery as authentication.** Answering is not proving.
- **Reporting the unregistered agent as the problem.** The problem is that
  delegation never consulted the registry.
