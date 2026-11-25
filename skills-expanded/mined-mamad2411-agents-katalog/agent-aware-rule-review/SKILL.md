---
name: agent-aware-rule-review
description: >-
  Run existing detection rules against an agent doing its job to find which fire
  on legitimate work, and measure behavioural drift from a signed-off baseline
  week by week. Use when agents enter an estate whose detection content predates
  them.
allowed-tools: Read, Grep, Glob
---

# Every classic rule fires on an agent working normally

Detection content written for humans classifies agent behaviour as an incident:
the volume rule, the off-hours rule, the breadth-of-access rule. Turning them
off loses coverage; leaving them on trains the analyst to ignore them. The
answer is a per-population baseline and a drift measure against it.

## When to use this

Whenever agents are introduced into an estate with existing detection content,
and at each model or manifest upgrade afterwards.

## Procedure

**1 — Run each classic rule against a clean agent run** and against a human's
day. Record which fire on which. Rules that fire on the agent and not the human
are the ones needing a population.

**2 — Sign off a baseline for each agent.** Tools used, resources touched, rate,
hours. Signed off means somebody agreed it — a baseline nobody approved is a
measurement, not a control.

**3 — Compare each subsequent week against the baseline.** Report a drift figure
and, more usefully, the *new* items: a tool that was not in the baseline is the
signal, and it is legible in a way a distance number is not.

**4 — Set a tolerance and say what crossing it does.** Drift within tolerance is
noise; beyond it is a review, and the review is of the change that caused it —
usually a model upgrade or a manifest edit.

**5 — Write the alert text for a human.** "patch-agent drift 0.35, new tools:
run_shell" is actionable. A distance metric on its own gets closed.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_aware_rule_review.py`](scripts/agent_aware_rule_review.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
classic rule                      fires on agent  fires on human
------------------------------------------------------------------
rate > 30 actions/min             True            False
activity outside 09:00-18:00      True            True
same action > 100 times           True            False

All three fire on an agent doing exactly its job. Deployed as-is, they
produce continuous noise and are disabled within a week.
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
  "classic_rules": [{"name": "str", "fires_on_agent": true, "fires_on_human": false}],
  "baseline": {"agent": "str", "tools": ["str"], "resources": ["str"], "signed_off": true},
  "weeks": [{"week": 0, "drift": 0.0, "new_tools": ["str"], "within_tolerance": true}],
  "tolerance": 0.0,
  "alert_text": "str"
}
```

## Failure modes

- **Muting the classic rules.** You lose them for humans too.
- **A baseline nobody signed off.** Nothing to appeal to when it drifts.
- **Alerting on the distance only.** Name the new tool.
