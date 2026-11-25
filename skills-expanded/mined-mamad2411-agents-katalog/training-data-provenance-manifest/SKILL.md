---
name: training-data-provenance-manifest
description: >-
  Compute what fraction of a corpus an attacker needs to poison it, and build a
  hashed manifest that can answer where a record came from and whether it
  changed. Use when reviewing training or fine-tuning data, or a RAG corpus
  nobody can attest to.
allowed-tools: Read, Grep, Glob
---

# A list of records is not provenance

Data-layer attacks need a smaller share of a corpus than people expect, so the
useful question is not "could someone poison this" but "could we tell". A record
list answers none of the four questions that matter; a manifest of content
hashes with a root answers all four, and it is cheap.

## When to use this

Any corpus that trains, fine-tunes or grounds a model — including the RAG index
somebody built from a shared drive.

## Procedure

**1 — State the poisoning rates in absolute terms.** For the corpus size you
have, print what 0.01%, 0.1% and 1% mean as a record count. The number is
usually small enough to end the argument about whether it is feasible.

**2 — Write down the four questions.** Where did this record come from, has it
changed since ingestion, what is in the corpus now, and what was in it at
training time. These are the requirements.

**3 — Compare what each artefact can answer.** A record list, a row count, a
snapshot, a hashed manifest. Only the last answers all four, and showing the
table is more persuasive than asserting it.

**4 — Build the manifest.** Content hash per record plus its source, and a root
over the whole set. The root is what makes "the corpus changed" a one-comparison
question.

**5 — Demonstrate detection.** Append records, recompute, and show both that the
root moved and which records are new. A manifest that detects change without
localising it sends you back to diffing the corpus.

## Example

**Input** — the fixture committed at the top of [`scripts/training_data_provenance_manifest.py`](scripts/training_data_provenance_manifest.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   10 poisoned of 100,000 → 0.01000%
  100 poisoned of 100,000 → 0.10000%
 1000 poisoned of 100,000 → 1.00000%

Published attacks land in this range. 'We have more clean data' is not
a defence, because the attacker is not trying to outvote you.
setup                               Q1   Q2   Q3   Q4   
------------------------------------------------------------
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
  "corpus": {"records": 0, "poison_rates": [{"rate": 0.0, "records": 0}]},
  "questions": [{"question": "str", "answerable_by": ["str"]}],
  "manifest": {"records": 0, "root": "str", "per_record": [{"id": "str", "hash": "str", "source": "str"}]},
  "detection": {"appended": 0, "root_changed": true, "localised": ["str"]}
}
```

## Failure modes

- **Arguing about feasibility.** Print the record count and the argument ends.
- **A manifest with no source field.** It answers "changed", never "from where".
- **A root with no per-record hashes.** Detection without localisation.
