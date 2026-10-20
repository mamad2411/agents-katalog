---
name: post-incident-change-surface
description: >-
  Count the surfaces that change an agent's behaviour without passing change
  management, and check weeks later which post-incident actions are still
  verifiable rather than guidance. Use at post-incident review, or before
  closing actions from the last one.
allowed-tools: Read, Grep, Glob
---

# A prompt edit is guidance, and it closed an action item

Post-incident actions for agentic systems fail in a specific way: several of them
are changes to surfaces that generate no record, and one or two are prompt edits
recorded as controls. Six weeks later nobody can demonstrate that any of it is
still in place, and the review declares the incident closed.

## When to use this

At post-incident review, and again several weeks afterwards — the second pass is
the one that finds this.

## Procedure

**1 — Enumerate the change surfaces and mark which bypass change management.**
Code and infrastructure usually do not; model version, prompt, manifest and
approval settings usually do.

**2 — Classify every action from the review.** Control, detection, guidance, or
documentation. A prompt edit is guidance: it changes behaviour on average and
enforces nothing.

**3 — Test verifiability now.** For each action, is there a check that would fail
if it were reverted? If not, the action cannot be audited and will silently
regress.

**4 — Re-test weeks later.** Run the same check. The count that survives is the
honest measure of the review, and it is usually a third of what was agreed.

**5 — Measure the blast radius before and after.** The reduction is what the
incident actually bought. If it is unchanged, the actions were process rather
than containment, and that belongs in the report.

## Example

**Input** — the fixture committed at the top of [`scripts/post_incident_change_surface.py`](scripts/post_incident_change_surface.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
blast before 44  after 4
the manifest diff records the change even though no PR was raised.

OK   gate http_post behind approval            type=preventive  owner=platform-sec   verify_by=2026-09-30
OK   alert on credential-path reads            type=detective   owner=soc            verify_by=2026-09-15
WEAK update the prompt to warn the model       type=guidance    owner=—              verify_by=—

1 action(s) are guidance rather than controls: ['update the prompt to warn the model']
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
  "surfaces": [{"name": "str", "bypasses_change_management": true}],
  "actions": [{"action": "str", "kind": "control|detection|guidance|documentation",
               "verifiable": false, "check": "str|null"}],
  "recheck": {"weeks_later": 0, "still_verifiable": 0, "of": 0},
  "blast_radius": {"before": 0, "after": 0}
}
```

## Failure modes

- **Recording a prompt edit as a control.** It is guidance under a different
  name.
- **Closing actions at the review.** Re-check weeks later or the number is
  aspirational.
- **No before-and-after blast radius.** Nothing shows whether it helped.
