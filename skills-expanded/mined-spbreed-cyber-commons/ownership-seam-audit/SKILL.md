---
name: ownership-seam-audit
description: >-
  Find the decisions in an agentic programme that have no named owner and
  measure what they cost during a simulated incident. Use when org design is
  being discussed, or when an incident stalled waiting for a decision.
allowed-tools: Read, Grep, Glob
---

# Thirty-five of thirty-six hours were two unowned decisions

Org design failures are invisible until an incident, when they appear as hours.
The two decisions that typically have no owner — what autonomy rung an agent may
run at, and how long traces are retained — are the ones that stall response,
because nobody can make them and everybody can veto them.

## When to use this

Designing ownership for an agentic programme, and after any incident whose
timeline contains a wait.

## Procedure

**1 — Enumerate the decisions, not the functions.** Autonomy rung, trace
retention, stop authority, exemption approval, disclosure sign-off, vendor
acceptance. Decisions have owners; functions have opinions.

**2 — Ask who may decide each one alone.** Not who is consulted — who may
decide. Two or more names is the same as none, and it takes the same time to
resolve.

**3 — Simulate an incident that needs several of them.** Assign realistic hours,
with the unowned decisions taking as long as it takes to convene the people who
could make them.

**4 — Report the share of the incident that was decision latency.** It is
usually most of it, and the number is far more persuasive than the observation.

**5 — Assign each unowned decision a single accountable name, with an escalation
path.** Then re-run the simulation to show the difference. That is the business
case for the org change.

## Example

**Input** — the fixture committed at the top of [`scripts/ownership_seam_audit.py`](scripts/ownership_seam_audit.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
seam                        owner                           lesson
------------------------------------------------------------------------------
AppSec ↔ Platform           platform-security               B3.1
Identity ↔ SecOps           on-call SRE, pre-authorised     B3.6
GRC ↔ Engineering           ⚠ NOBODY                        F3.2
SOC ↔ Data                  ⚠ NOBODY                        E1.3
CISO office ↔ Legal         legal, on IR notification       F2.6
AppSec ↔ SOC                detection engineering           E2.2
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
  "decisions": [{"name": "str", "owner": "str|null", "consulted": ["str"], "may_decide_alone": 0}],
  "unowned": ["str"],
  "incident": [{"step": "str", "hours": 0.0, "blocked_on": "str|null"}],
  "totals": {"hours": 0.0, "decision_latency_hours": 0.0, "share": 0.0},
  "after_assignment": {"hours": 0.0}
}
```

## Failure modes

- **Mapping functions.** They all report coverage.
- **Two owners.** It resolves as slowly as none.
- **Reporting the seam without the hours.** It reads as a governance
  preference.
