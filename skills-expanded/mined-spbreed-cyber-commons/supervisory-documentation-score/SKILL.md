---
name: supervisory-documentation-score
description: >-
  Score written documentation on how many of its sentences are checkable — each
  naming a control, an artefact and a date — and test it against the follow-up
  questions a supervisor actually asks. Use before submitting anything to an
  assessor.
allowed-tools: Read, Grep, Glob
---

# Count the checkable sentences

Documentation that survives supervision is not better written; it is
differently written. Each load-bearing sentence names a control, the artefact
that evidences it, and a date. A paragraph with none of those reads well, passes
internal review, and produces four follow-ups you cannot answer.

## When to use this

Before submitting documentation to a regulator, an auditor or a customer's
assurance team.

## Procedure

**1 — Split the text into sentences and score each.** Does it name a control
identifier, an artefact, and a date? Three marks per sentence, and the count of
sentences scoring all three is the headline.

**2 — Report the weak version's score.** Usually zero. Showing it beside the
strong version is what changes how the next document gets written.

**3 — Rewrite so the load-bearing claims carry all three.** Not every sentence —
the ones an assessor would test. The rest can be prose.

**4 — Generate the follow-up questions and try to answer them from the text
alone.** "Which control", "show me the artefact", "when was it last tested",
"who owns it". A question you cannot answer from the document is a question you
will answer live, badly.

**5 — Attach the artefacts.** A checkable sentence with an unattached artefact
is one email away from being unevidenced.

## Example

**Input** — the fixture committed at the top of [`scripts/supervisory_documentation_score.py`](scripts/supervisory_documentation_score.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
=== WEAK — 0/3 sentences checkable ===
   [---] Our AI systems are subject to appropriate oversight and 
   [---] Access is
granted on a least-privilege basis and reviewe
   [---] Agents are
monitored for anomalous behaviour and we main

=== STRONG — 0/6 sentences checkable ===
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
  "sentences": [{"text": "str", "names_control": false, "names_artefact": false, "has_date": false}],
  "score": {"checkable": 0, "total": 0},
  "comparison": {"weak_checkable": 0, "strong_checkable": 0},
  "followups": [{"question": "str", "answerable_from_text": false}],
  "artefacts_attached": ["str"]
}
```

## Failure modes

- **Editing for tone.** The problem is not the prose.
- **Making every sentence checkable.** Only the load-bearing ones need it.
- **Naming an artefact you did not attach.** The follow-up arrives immediately.
