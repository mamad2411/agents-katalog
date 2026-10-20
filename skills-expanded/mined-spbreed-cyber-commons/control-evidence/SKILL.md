---
name: control-evidence
description: >-
  Turn evaluation and monitoring output into audit evidence that survives
  challenge, and say plainly what it does not prove. Use when asked to evidence
  a control, prepare for an audit, map evals to a control framework, justify
  continuous control verification, or interpret a passing test as assurance.
allowed-tools: Read, Bash
---

# Evaluation output as audit evidence

An evaluation result is not evidence until three things are true: it tested the
control that is claimed, it ran on the system that is deployed, and its failure
mode is stated. Most "evidence" fails the second.

Point-in-time control testing fails for AI systems specifically because the
thing under test changes between tests — the model, the prompt, the tool set,
and the data all move independently of any release.

## When to use this

Preparing audit evidence, mapping evals to controls, or reviewing whether a
green dashboard supports the assurance being claimed from it.

## Procedure

**1 — State the control claim precisely.** "The agent cannot exfiltrate
customer data" is not testable. "Egress from the agent workload is denied to
all destinations outside the allowlist, enforced at the gateway" is. Evidence
is only as good as the sentence it supports.

**2 — Bind evidence to the deployed artefact.** Record the model version, the
prompt/config hash, the tool allowlist, and the commit — for the system **as
deployed**, not as tested in a branch. Evidence that cannot be bound to a
deployed artefact proves something about a different system.

**3 — State the population and the sample.** How many cases exist, how many
were tested, how they were chosen. A sample chosen by the team that built the
control is not independent, and that has to be written down rather than
implied.

**4 — Separate operating effectiveness from outcome.** "The gate ran on every
request" (operating) is different from "no harmful action got through"
(outcome). Auditors ask for the first; incidents are caused by the second. Give
both, labelled.

**5 — Report accuracy, never conformance.** A pipeline whose output is
schema-valid 100% of the time has demonstrated that its serialiser works.
Conformance is near-free by construction; accuracy is the expensive,
interesting number. Any evidence pack leading with a conformance percentage is
overstating itself, and an auditor who notices will discount everything else in
it.

**6 — State the blind spots.** What the eval cannot see: cases not in the
corpus, failure modes not modelled, drift since the run. A control with stated
limits is stronger evidence than one claiming none.

**7 — Set the re-verification interval from the change rate.** If the model can
be updated weekly, annual testing evidences a system that no longer exists. Tie
re-verification to the artefact's change events, not the calendar.

## Example

**Input** — the fixture committed at the top of [`scripts/control_evidence.py`](scripts/control_evidence.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
n                24
conformance      1.0000   ← structural. NOT a quality claim.
expert accuracy  0.8750   ← the number that evidences EV-2
EV-2  PASS
      expert accuracy 0.8750 over 24 held-out questions; conformance 1.0000 reported separately; key never exposed to the harness
      at +10d → PASS
      at +45d → STALE
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
  "control": {"id": "str", "claim": "str", "testable": true},
  "binding": {"model": "str", "config_hash": "str", "tools": ["str"],
              "commit": "str", "matches_deployed": true},
  "sample": {"population": 0, "tested": 0, "selection": "random|risk_based|convenience",
             "independent": false},
  "results": {"operating_effectiveness": 0.0, "outcome_effectiveness": 0.0,
              "accuracy": 0.0, "conformance_reported": false},
  "blind_spots": ["str"],
  "reverification": {"trigger": "on_model_change|on_config_change|periodic",
                     "interval_days": 0},
  "conclusion": {"supports_claim": true, "limits": "str"}
}
```

`conformance_reported: true` should be treated as a defect in the evidence
pack, not a feature of it.

## Failure modes

- **Evidence from a branch.** Bind to what is deployed or say you cannot.
- **A green dashboard as assurance.** Ask what turns it red, and test that.
- **Convenience sampling presented as coverage.**
- **Annual re-verification of a weekly-changing artefact.**
- **Leading with conformance.** The single most common overstatement in
  automated assurance.
