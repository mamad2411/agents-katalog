---
name: assurance-conversation-prep
description: >-
  Prepare for a regulator or auditor conversation by reporting conformance and
  expert accuracy separately alongside control coverage, and rehearsing the
  three openings that actually get used. Use before an assurance meeting.
allowed-tools: Read, Grep, Glob
---

# Conformance 1.00, accuracy 0.50

The number that goes into an assurance conversation is usually conformance,
because it is the one that is high. Conformance says the output had the right
shape; accuracy says it was right. Reporting the first without the second is the
failure mode that ends a meeting badly, and reporting both is what makes the rest
of the conversation about controls instead of credibility.

## When to use this

Before any regulator, auditor or customer assurance conversation about an AI
system.

## Procedure

**1 — Compute conformance and accuracy separately, against a held-out key.**
Never the examples that were used for development. Report both to the same
number of decimals so neither can be read as the other.

**2 — Compute control coverage in three states.** Evidenced, stale, unevidenced.
A single percentage hides the stale bucket, which is the one you will be asked
about.

**3 — Rehearse the three openings.** "Show me the evidence for this control."
"What changed since the last test." "What would you not be able to detect."
These are the ones that get used.

**4 — Prepare the answer to the third one honestly.** A stated blind spot is a
programme that knows its own shape; a claim of full detection invites a search
for the counterexample, and there is one.

**5 — Bring the artefacts, dated.** The single most common failure is a correct
answer with the evidence three teams away.

## Example

**Input** — the fixture committed at the top of [`scripts/assurance_conversation_prep.py`](scripts/assurance_conversation_prep.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
n                20
conformance      1.0000
expert accuracy  0.7500
control  state         
------------------------
AC-1     PASS          
AC-2     PASS          
SB-1     STALE         
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
  "evaluation": {"conformance": 0.0, "accuracy": 0.0, "key": "held-out", "n": 0},
  "coverage": {"evidenced": 0, "stale": 0, "unevidenced": 0, "of": 0},
  "openings": [{"question": "str", "answer": "str", "artefact": "str|null"}],
  "known_blind_spots": ["str"],
  "artefacts": [{"control": "str", "artefact": "str", "as_of": "str"}]
}
```

## Failure modes

- **Leading with conformance.** It is the flattering half.
- **A single coverage percentage.** Stale is a state and it will be asked
  about.
- **Claiming complete detection.** The counterexample exists and they will find
  it.
