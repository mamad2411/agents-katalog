---
name: patch-validation-harness
description: >-
  Accept a proposed fix only when three things hold — behaviour unchanged, the
  exploit no longer works, and the fix proved against the build that was
  vulnerable. Use when an agent proposes a patch, or when a scanner going green
  is being read as a fix.
allowed-tools: Read, Grep, Glob, Bash
---

# A green scanner is not a fixed bug

Several candidate patches will make the scanner green. Some of them change
behaviour, some of them leave the bug exploitable, and one of them does neither.
Telling them apart needs three gates, and the third is the one that is usually
missing: proof against the **old** build, so "the exploit stops working" is a
statement about the patch rather than about the environment.

## When to use this

Every proposed remediation, whether authored by a person or an agent, and
especially when the evidence offered is that the scanner no longer fires.

## Procedure

**1 — Establish the baseline on the vulnerable build.** The behaviour cases must
pass and the exploit must work. If the exploit does not work here, you are about
to validate a patch against a bug you have not reproduced.

**2 — Gate one: behaviour unchanged.** Run every behaviour case against the
patched build. A patch that fixes the defect and changes an answer is a
regression with a security justification.

**3 — Gate two: the exploit no longer works.** Against the patched build,
directly. Not "the scanner is quiet" — the scanner was one of the tools that
missed the defect class in the first place.

**4 — Gate three: proof of fix.** Run the exploit against the old build again,
after the patch is written, in the same harness. It must still work. This is
what excludes the environment having changed underneath the test.

**5 — Report per candidate and per gate.** A candidate rejected at gate one and
one rejected at gate two need different conversations with whoever wrote them.

## Example

**Input** — the fixture committed at the top of [`scripts/patch_validation_harness.py`](scripts/patch_validation_harness.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
behaviour of the vulnerable build:
   get_user('dana'    ) → [(1, 'dana')]      ok
   get_user('sam'     ) → [(2, 'sam')]       ok
   get_user('nobody'  ) → []                 ok
   get_user("o'brien" ) → raised OperationalError FAILS

exploit works: True — probe returned 3 rows
scanner fires: False
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
  "baseline": {"behaviour_pass": true, "exploit_works": true},
  "candidates": [{"id": "str", "scanner_green": true,
                  "behaviour_unchanged": true, "exploit_blocked": true,
                  "proof_of_fix": true, "verdict": "accepted|rejected", "rejected_at": "str|null"}],
  "accepted": ["str"]
}
```

## Failure modes

- **Accepting a green scanner.** Several wrong patches produce one.
- **Skipping the behaviour cases.** The most reliable way to block an exploit is
  to break the feature.
- **Omitting proof of fix.** Without it you cannot distinguish a working patch
  from a broken exploit.
