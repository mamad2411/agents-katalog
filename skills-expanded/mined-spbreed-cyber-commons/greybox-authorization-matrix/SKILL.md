---
name: greybox-authorization-matrix
description: >-
  With one credential per role and a schema but no source, fill a
  roles-by-objects-by-verbs matrix, flag design mismatches, and rank the cells
  nobody tested by blast radius. Use for a grey-box engagement, or when
  endpoint coverage is being reported as authorisation coverage.
allowed-tools: Read, Grep, Glob
---

# Authorisation lives in cells, not endpoints

Grey box is the mode that can actually find broken object-level authorisation,
because it has more than one identity. It is also the mode most often reported
wrong: the engagement touches every endpoint, calls itself complete, and never
notices that authorisation is a property of the *cell* — this role, this object,
this verb — not of the endpoint.

The matrix makes the untested cells visible, which is the whole point.

## When to use this

An engagement with low-privilege accounts and a schema, a BOLA/BFLA hunt, and
any report whose coverage claim is a count of endpoints.

## Procedure

**1 — List what you were handed.** One credential per role is the minimum and
the enabling fact; also the schema, a couple of ids you own and a couple you
must not, the matrix as designed, and the scope so the run is not an incident.

**2 — Build the full matrix.** Roles × objects × verbs. Write down what the
design *says* each cell should be, before touching anything.

**3 — Exercise cells and record what came back.** Every cell you do not exercise
stays untested — that is data, not a gap to hide.

**4 — Report three things.** Mismatches, where the estate disagrees with the
design. Untested cells, ranked by what a wrong answer would cost, not by schema
order. And the coverage fraction, so "we tested everything" cannot stand when
40% of the cells were never sent a request.

## Example

```
tested 12 of 30 cells (40%)
2 mismatch(es):
  ! traveller can read booking(other): designed deny, observed allow
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
  "data_sources": [{"source": "str", "gives": "str"}],
  "cells": [{"role": "str", "object": "str", "verb": "str",
             "design": "allow|deny", "observed": "allow|deny|null"}],
  "mismatches": [{"role": "str", "object": "str", "verb": "str",
                  "design": "str", "observed": "str"}],
  "untested": [{"role": "str", "object": "str", "verb": "str", "blast": 0}],
  "coverage": 0.0
}
```

## Failure modes

- **Reporting endpoint coverage as authorisation coverage.** Every endpoint
  touched, most cells untested.
- **Ranking untested cells by schema order.** The audit-log write matters more
  than the profile read; the order they appear in the spec is noise.
- **Testing only your own objects.** One id is a functionality test; the second
  id is the security test.
- **Trusting the design column.** It is what the team believes is enforced,
  which is the thing under test.
