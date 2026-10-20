---
name: agent-tempo-baseline
description: >-
  Measure the behavioural signals that separate an agent's tempo from a
  person's — action rate, inter-action variance, session length, tool breadth,
  night-hours share — and check what a volume rule tuned for human tempo does
  when an agent runs. Use before writing any detection that will see agents.
allowed-tools: Read, Grep, Glob
---

# The rule fires 154 seconds into a sixty-minute run

Detection content is calibrated on human tempo. An agent performs in an hour
what a person performs in a month, so a volume rule does fire — immediately, and
then not again for the rest of the run, which is the part that matters. The
baseline has to be measured before any rule is written against it.

## When to use this

Before authoring or tuning detections in an estate where agents act, and when
an existing rule is either silent or permanently firing.

## Procedure

**1 — Pick one human and one agent doing comparable work.** Same task class,
same hour. Comparability is what makes the ratio meaningful.

**2 — Measure five signals for each.** Actions per hour, variance between
actions, session length, distinct tools touched, and share of activity outside
working hours. Report the ratio per signal — most will be in the hundreds.

**3 — Run the existing volume rule against the agent's hour.** Record when it
first fires, in seconds. This is usually early enough that the rest of the run
is unmonitored, which is the finding.

**4 — Say what the rule now means.** After the first firing it is silent for the
remainder — so it is an *onset* detector, not a volume detector, and anyone
relying on it for volume is relying on something else.

**5 — Derive per-population thresholds.** Humans and agents need different
baselines, and an agent's baseline needs a per-agent one: a patch agent and a
triage agent do not share a tempo.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_tempo_baseline.py`](scripts/agent_tempo_baseline.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   Alex                12 actions/hour -> silent
   workflow agent    1400 actions/hour -> ALERT

the agent crosses the threshold after 154 seconds
and keeps going for the remaining 3446.

So the rule fires, about two and a half minutes into a sixty-minute run -
by which point most of what the actor was going to do is done. If those
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
  "subjects": [{"name": "str", "kind": "human|agent",
                "actions_per_hour": 0, "variance": 0.0, "session_minutes": 0,
                "distinct_tools": 0, "night_share": 0.0}],
  "ratios": {"str": 0.0},
  "existing_rule": {"threshold": 0, "first_fires_after_seconds": 0, "silent_after": true},
  "recommendation": {"per_population_thresholds": true, "populations": ["str"]}
}
```

## Failure modes

- **Comparing an agent to an average human.** Compare like work.
- **Reading an early firing as coverage.** It is one alert and then silence.
- **One agent baseline for every agent.** Their tempos differ as much as their
  jobs do.
