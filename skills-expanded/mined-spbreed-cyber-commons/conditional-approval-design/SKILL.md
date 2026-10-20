---
name: conditional-approval-design
description: >-
  Tier a risky request, show what a flat refusal costs in visibility, and write
  the conditions that make a yes safe, testable and time-bound. Use when the
  answer is no and the capability will ship anyway.
allowed-tools: Read, Grep, Glob
---

# The flat no loses the visibility and the capability ships

A refusal without conditions has a predictable outcome: the capability appears
somewhere you cannot see, on somebody's personal account or inside a product
already bought. A conditional yes keeps it inside the estate, and the conditions
are the control — provided each one is testable and has a date.

## When to use this

Any request whose straightforward answer is no, and any exception that is about
to be granted informally.

## Procedure

**1 — Tier the request and compute its blast radius.** An irreversible
tenant-wide tool is what usually makes it critical, and naming that is more
useful than the tier.

**2 — Model the flat refusal.** Where the capability goes instead, and what
visibility you lose. Write it down — the point is not to argue against refusing
but to price it.

**3 — Write conditions that each remove a term of the risk.** Gate the
irreversible action, narrow the scope, cap the population, add the detection.
Vague conditions — "with appropriate oversight" — are a yes with extra words.

**4 — Make each condition testable.** A check that would fail if the condition
were not met, and who runs it. A condition nobody tests is a condition nobody
keeps.

**5 — Put an expiry on the approval.** Conditional approvals that do not expire
become permanent policy set by whoever asked first.

## Example

**Input** — the fixture committed at the top of [`scripts/conditional_approval_design.py`](scripts/conditional_approval_design.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
request        customer-refund-agent
asks for       issue refunds up to GBP 500 without human approval
business case  42% of refund tickets are mechanical; 3.5 FTE of manual work
claimed rung   L2.5
blast radius   18  (irreversible, tenant-wide)
risk tier      high (score 8)
decision            refused
what happens        the team ships it as a 'workflow automation' outside the AI register
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
  "request": {"name": "str", "tools": ["str"], "blast": 0, "tier": "str", "irreversible": ["str"]},
  "flat_refusal": {"capability_ships_anyway": true, "visibility_lost": ["str"]},
  "conditions": [{"condition": "str", "removes": "str", "test": "str", "owner": "str"}],
  "approval": {"granted": true, "expires": "str", "review_trigger": ["str"]}
}
```

## Failure modes

- **Refusing without pricing it.** The capability ships out of sight.
- **Untestable conditions.** They are a yes in a longer sentence.
- **No expiry.** The exception becomes the policy.
