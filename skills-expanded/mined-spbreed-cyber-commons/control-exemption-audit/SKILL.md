---
name: control-exemption-audit
description: >-
  Check that turning a control off is a recorded, bounded exemption the platform
  reads, and that risky launches are decided against the exemption class rather
  than one control at a time. Use when guardrails are disabled for a demo, a
  migration, or a load test.
allowed-tools: Read, Grep, Glob
---

# Turning a control off is defensible; not recording it is not

Every estate disables controls sometimes. The failure is not the disabling — it
is that nothing recorded it, nothing bounded it, and the next decision was made
by a system that believed the control was on. And decisions made one control at
a time approve launches that the same facts refuse when taken together.

## When to use this

Reviewing guardrail configuration, change management for agent platforms, or
any launch where "we turned that off for the demo" appears in a thread.

## Procedure

**1 — Compare intended state with actual state,** per control. The gap is the
set of undeclared exemptions, and each one is a finding regardless of whether
it was reasonable.

**2 — Require the exemption to be a record the platform reads.** Control,
requester, approver, reason, expiry. A record in a ticket the platform cannot
read is documentation; the orchestrator must refuse a disable with no matching
record.

**3 — Test both directions.** A named control with a valid exemption may be
disabled. A control with no approval must be refused. Both, or it is a logging
system.

**4 — Decide a launch one control at a time.** Take a large launch and evaluate
each control's own rule. It will be approved, and each answer will be correct in
isolation. Record that.

**5 — Re-decide against the exemption class.** Group the disabled controls —
detective, preventive, egress — and set caps per class: how many agents, for how
long, with what compensating control. The same launch is now refused, and a
smaller one on an allowlist is permitted. The disagreement between step 4 and
step 5 is the finding.

## Example

**Input** — the fixture committed at the top of [`scripts/control_exemption_audit.py`](scripts/control_exemption_audit.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
day  12  disable cyber-classifier    ALLOW via EX-118
day  44  disable cyber-classifier    REFUSE - no approved exemption
day  12  disable transcript-signing  REFUSE - no approved exemption

The record is the mechanism, not a wiki page describing one. An
exemption the platform cannot express is an exemption you cannot grant.
checked one decision at a time:
   exemption valid : True
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
  "controls": [{"name": "str", "intended": "on|off", "actual": "on|off", "exemption": "str|null"}],
  "exemptions": [{"control": "str", "approver": "str", "expires": "str", "platform_readable": true}],
  "probes": {"named_with_approval": "permitted", "unapproved": "refused"},
  "launch": {"request": {"agents": 0, "hours": 0}, "per_control_verdict": "approved",
             "by_exemption_class_verdict": "refused", "caps": {"class": "str", "agents": 0, "hours": 0}}
}
```

## Failure modes

- **An exemption the platform cannot read.** It cannot enforce an expiry it
  cannot see.
- **Deciding control by control.** Each answer is right and the composition is
  wrong.
- **No expiry.** A permanent exemption is a policy change made by whoever was
  on call.
