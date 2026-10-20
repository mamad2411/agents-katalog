---
name: context-window-sizing
description: >-
  Find the smallest slice of a file in which a defect is actually decidable, and
  measure what larger windows add in unrelated code. Use when tuning what a
  model is shown per finding, when analysis costs too much, or when a model
  keeps missing a bug that is on the line you gave it.
allowed-tools: Read, Grep, Glob
---

# Decidable, then small — in that order

Context engineering for an analysis pipeline is not "send less". It is finding
the slice in which the question can be answered at all, and only then making it
smaller. A ±2-line window around the bug is cheap and **not decidable**: it
lacks the signature, so nothing in it says where the value came from.

## When to use this

When designing what a pipeline sends per finding, and whenever cost per finding
is the constraint.

## Procedure

**1 — Define decidability for the defect class.** For injection: the sink, the
value's origin, and any sanitiser between them. Write it down before slicing, or
you will judge slices by how they look.

**2 — Build the candidate slices.** The whole file, a fixed window around the
line, a wider window, and a **path slice** — the enclosing function plus the
definitions it depends on. Measure each in characters.

**3 — Mark each slice decidable or not,** against step 1. Cheap and undecidable
is the trap: it looks like a saving and it produces confident answers about
information that is not there.

**4 — Count unrelated content in the decidable ones.** Functions, constants and
imports the defect does not depend on. This is what a bigger window costs, in
tokens and in the model's attention.

**5 — Pick the smallest decidable slice, and say what it excluded.** The
exclusion list is what somebody re-reads when the pipeline misses something.

## Example

**Input** — the fixture committed at the top of [`scripts/context_window_sizing.py`](scripts/context_window_sizing.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
the bug is on line 22
whole file             839 chars   29 lines
±2 line window         207 chars    5 lines
±6 line window         432 chars   13 lines
strategy            sink   concat  source  intent  decidable
----------------------------------------------------------------
whole file          True   True    True    True    True
±2 line window      True   True    False   False   False
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
  "decidability": {"requires": ["str"]},
  "slices": [{"name": "str", "chars": 0, "decidable": false, "unrelated_units": 0}],
  "chosen": {"name": "str", "chars": 0, "unrelated_units": 0},
  "excluded": ["str"]
}
```

## Failure modes

- **Optimising size first.** An undecidable slice is not cheap; it is wrong at a
  lower price.
- **Judging slices by eye.** Write the decidability requirement down first.
- **Ignoring unrelated content** in a decidable slice. It is the cost you can
  actually remove.
