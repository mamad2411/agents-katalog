---
name: stop-authority-readiness
description: >-
  Turn "we can stop it" into a named mechanism with an owner, a measured
  time-to-stop from a game day, and a stated cost of stopping. Use to answer how
  long it would actually take to stop a running agent, before granting autonomy,
  and whenever stop authority has never been exercised.
allowed-tools: Read, Grep, Glob
---

# Killing the process does not survive a restart

Stop authority is usually described rather than specified: somebody can stop it,
probably quickly, and nobody has tried. Three questions turn that into a control
— which mechanism, who may invoke it without asking, and how long it takes when
measured rather than estimated.

## When to use this

Before raising an agent's autonomy, at any authorisation to run unattended, and
once a year as a game day.

## Procedure

**1 — Write the vague answers down and then the concrete ones.** Side by side.
"Ops can kill it" against "the on-call SRE revokes the workload identity in the
identity console, and here is the runbook". The contrast is what gets the work
scheduled.

**2 — Enumerate mechanisms and what each survives.** Killing the process does not
survive a restart or a scheduler. Revoking the identity does. Blocking egress
stops the effect and not the run. Record what each actually stops.

**3 — Name who may invoke it without asking.** Stop authority that needs an
approval is not stop authority; it is an escalation. If nobody may act alone,
that is the finding.

**4 — Run a game day and measure.** From decision to the agent being unable to
act. Report seconds. An estimate is not a measurement and this is the number
that is always wrong in the optimistic direction.

**5 — Cost the stop.** What stopping costs per minute in halted legitimate work.
Somebody will ask, and having the number is what makes the decision fast during
an incident.

## Example

**Input** — the fixture committed at the top of [`scripts/stop_authority_readiness.py`](scripts/stop_authority_readiness.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
who         VAGUE    the security team
            CONCRETE on-call SRE, no approval required for non-human identities

mechanism   VAGUE    we can turn off the agents
            CONCRETE revoke the SPIFFE identity at the gateway (survives restart)

time        VAGUE    quickly
            CONCRETE measured 12s decision→first failed call, game day 2026-07-04
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
  "answers": [{"question": "str", "vague": "str", "concrete": "str"}],
  "mechanisms": [{"name": "str", "stops": ["str"], "survives_restart": false}],
  "authority": {"may_invoke_alone": ["str"], "approval_required": false},
  "game_day": {"measured_seconds": 0, "estimated_seconds": 0},
  "cost_per_minute": 0.0,
  "ready": false
}
```

## Failure modes

- **Process termination as the mechanism.** The scheduler restarts it.
- **An estimated time-to-stop.** Measure it once and the estimate is revealed.
- **Stop authority behind an approval.** That is escalation with a different
  name.
