---
name: agentic-risk-tiering
description: >-
  Tier an AI use case by what it can do — autonomy, data reach and external
  effect — and compare the result against tiering by which model it uses. Use
  when writing or auditing a risk questionnaire, or when every large-model
  deployment is coming out high.
allowed-tools: Read, Grep, Glob
---

# Tier the authority, not the model

Tiering on model capability tracks vendor marketing: every frontier deployment
becomes high and every small model low. It gets the important case backwards — a
small local model with production deploy rights and regulated data — because the
model determines the likelihood of a bad output and the authority determines
what a bad output costs.

## When to use this

Writing an intake questionnaire, auditing an existing one, or re-tiering a
portfolio whose distribution looks like the vendor's price list.

## Procedure

**1 — Score three inputs, none of which is the model.** What the output can
trigger without a human, what data it can read, and whether it can act
externally. Each on a small ordinal scale, and write the scale down.

**2 — Set thresholds and apply them.** Publish the thresholds with the tiers, so
a disputed tier is a dispute about a number rather than about judgement.

**3 — Tier the same portfolio by model, as a comparison.** Run the
questionnaire that leads with the model question and record where the two
disagree. The disagreements are the argument.

**4 — Look hardest at the inversions.** An asset that is low by model and
critical by authority is the case that motivates the change, and there is
usually one.

**5 — Write the four questions the intake form should ask** and, explicitly, the
one it should not lead with. Reviewers copy questionnaires; make yours the one
worth copying.

## Example

**Input** — the fixture committed at the top of [`scripts/agentic_risk_tiering.py`](scripts/agentic_risk_tiering.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
asset                                         tier       score
------------------------------------------------------------------
frontier chatbot, public docs, read-only      low            0
small local model with prod deploy rights     critical      12
                                              autonomy L3 (+5)
                                              regulated data (+3)
                                              customer data (+2)
                                              can act externally (+2)
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
  "scale": {"autonomy": ["str"], "data": ["str"], "reach": ["str"]},
  "assets": [{"name": "str", "autonomy": 0, "data": 0, "reach": 0, "score": 0, "tier": "low|medium|high|critical"}],
  "by_model": [{"name": "str", "tier": "low|medium|high|critical"}],
  "disagreements": [{"name": "str", "by_authority": "str", "by_model": "str", "inversion": true}],
  "questions": ["str"]
}
```

## Failure modes

- **Leading with the model question.** Everything downstream inherits it.
- **Unpublished thresholds.** The tier becomes an opinion.
- **Ignoring the inversions.** They are the whole finding.
