---
name: sensor-coverage-matrix
description: >-
  Score the sensor classes an estate already owns — EDR, DLP, CSPM, CNAPP —
  against what an agent actually does, and name the actions no sensor sees. Use
  before buying detection tooling for an agent estate, or when someone claims
  the estate is already covered.
allowed-tools: Read, Grep, Glob
---

# Coverage is a column, not a percentage

Every estate that runs agents already owns four classes of sensor, bought for
people and hosts. The question is not whether they work — they do, at what they
were built for — but which parts of an agent's working day are inside their
field of view at all.

Answer it as a matrix and one number falls out that no product page will give
you: the actions seen by **nothing**.

## When to use this

Before a detection roadmap, before a tooling purchase, and any time "we already
have visibility" is offered as an answer about an agent estate.

## Procedure

**1 — List the sensor classes you own, with the product behind each.** Naming
the product keeps the conversation checkable. The open-source references are
Wazuh for EDR, regex plus file integrity monitoring for the DLP that most teams
actually have, Prowler or ScoutSuite for CSPM, and Falco plus Trivy for CNAPP.

**2 — List what the agents do, not what you fear.** An ordinary day: files
written, an outbound session to a model API, a customer record read through an
internal API, tokens placed in a prompt, a vendor tool called, money moved, a
role assumed, a child process spawned.

**3 — Score each cell as full, partial or none — on visibility, not alerting.**
"Would this sensor alert" is a tuning question and comes later. "Is this sensor
in the path" is a fact about architecture, and it is the one that decides
whether tuning is even possible.

**4 — Read the uncovered rows, and read what they have in common.** If the
uncovered set is arbitrary, tune. If it is coherent — every action inside the
reasoning loop, or behind an API the host never observes — then a fifth product
of the same four kinds will not move it, and the answer is a new source rather
than a better rule.

## Example

```
per-sensor coverage of the agent's day
  EDR     3.0 / 9   33%
  DLP     0.5 / 9   6%
  CSPM    0.5 / 9   6%
  CNAPP   3.0 / 9   33%

  best single sensor   EDR
  all four combined    3.5 / 9   39%
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
  "sensors": [{"name": "str", "product": "str", "sees": "str"}],
  "actions": [{"action": "str", "coverage": {"EDR": "full|partial|none"}}],
  "per_sensor": [{"name": "str", "score": 0.0, "of": 0}],
  "combined": {"score": 0.0, "of": 0},
  "uncovered": ["str"]
}
```

## Failure modes

- **Scoring alerting rather than visibility.** A sensor that is not in the path
  cannot be tuned into one that is.
- **Summing the columns.** Four sensors covering the same three actions is
  still three actions; take the union per row, which is what the script does.
- **Reporting the combined percentage alone.** 39% sounds like a tuning problem.
  The four named rows are the finding.
- **Treating a partial as a full.** Seeing a TLS session open is not seeing what
  crossed it.
