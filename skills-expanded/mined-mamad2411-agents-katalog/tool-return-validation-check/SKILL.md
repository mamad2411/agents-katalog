---
name: tool-return-validation-check
description: >-
  Check what a tool's return value is validated against before the agent acts on
  it — schema, then an independent oracle — and confirm that an unverifiable
  claim stops rather than propagating. Use when a tool's output becomes an
  agent's belief, or when reviewing multi-hop reasoning.
allowed-tools: Read, Grep, Glob
---

# Well-formed is not true

A tool return is untrusted input that arrives wearing the tool's authority. Two
checks are needed and they catch different things: a **schema** catches
malformed, and an **oracle** catches confidently wrong. Systems usually have the
first and treat it as if it were the second.

## When to use this

Any agent that acts on what a tool told it, and any pipeline where one step's
output is the next step's premise.

## Procedure

**1 — Define the schema per tool return.** Types and required fields. This is
the cheap check and it should be automatic; a return that fails it never
reaches the model.

**2 — Identify the oracle for each claim type.** Something independent that can
say true or false: a CVE database, a build, a test run, a second source. Not
another model — a model checking a model measures agreement, not truth.

**3 — Run the four cases.** Schema-perfect and true; schema-perfect and false;
schema-perfect with **no oracle available**; malformed. All four have to be
distinguishable in the output.

**4 — Make "unverifiable" a terminal state.** The third case is the one that
matters. A claim with no oracle must stop as `unverifiable` rather than
defaulting to true — silent promotion is how a hedge becomes a fact three hops
later.

**5 — Confirm only verified claims propagate.** Follow each case for several
hops and record which survive. The unverified ones surviving is the finding.

## Example

**Input** — the fixture committed at the top of [`scripts/tool_return_validation_check.py`](scripts/tool_return_validation_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   schema_ok=True  -> {'stopped': 'refuted', 'claim': 'libfoo has no known CVEs', 'by': 'checked against the advisory database'}
   schema_ok=True  -> {'propagated': 'test_login passes', 'verified_by': 'checked against the advisory database', 'hops': 3}
   schema_ok=True  -> {'stopped': 'unverifiable', 'claim': 'the refund was approved', 'why': 'no oracle for this claim'}
   schema_ok=False -> {'stopped': 'malformed'}

The first message is schema-perfect and confident and false. Schema
validation passed it; the oracle refuted it.
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
  "tools": [{"name": "str", "schema": true, "oracle": "str|null"}],
  "cases": [{"claim": "str", "schema_ok": true, "oracle_verdict": "true|false|unavailable",
             "state": "verified|refuted|unverifiable|malformed", "propagated": false}],
  "unverifiable_is_terminal": true
}
```

## Failure modes

- **Treating schema conformance as verification.** It is a statement about the
  serialiser.
- **Using a model as the oracle.** Two models agreeing is not evidence.
- **Defaulting unverifiable to true** because the pipeline needs a value. That
  default is the defect.
