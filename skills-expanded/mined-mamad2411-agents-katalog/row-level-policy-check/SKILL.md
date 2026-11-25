---
name: row-level-policy-check
description: >-
  Query an exposed data API as an anonymous caller with row-level security off
  and on, and count what a publishable key returns. Use when a client-side key
  reaches a database directly, or when a platform's default is open until
  somebody closes it.
allowed-tools: Read, Grep, Glob
---

# The anonymous key is meant to be public; the rows are not

Platforms that expose a database over HTTP hand out a key designed to ship in a
client. That is safe exactly when row-level policy is on, and the default on
several of them is off. The check is one query, run twice, and it is the
difference between a key that is public by design and a table that is.

## When to use this

Any deployment where a browser or an agent talks to a database service directly,
and any platform whose quickstart hands you an anonymous key.

## Procedure

**1 — Get the publishable key from where it actually is.** The client bundle,
the mobile app, the agent's configuration. It is not a secret and treating it as
one is what hides this defect.

**2 — Enumerate the tables.** Use the platform's catalogue rather than the
application's own queries — the application only touches the tables it needs,
which is not the set that exists.

**3 — Query each table anonymously with policy off.** Record the row count and,
specifically, whether any row contains a credential: provider keys stored
alongside agent configuration are the common and expensive case.

**4 — Enable policy and re-run.** Anonymous should return nothing; a signed-in
owner should return their own rows and no more. Both halves — a policy that
returns nothing to everyone is an outage.

**5 — Cost the exposure.** For every credential returned, name the provider and
who can revoke it. The revocation owner is usually not you, and that is the
sentence that gets the work scheduled.

## Example

**Input** — the fixture committed at the top of [`scripts/row_level_policy_check.py`](scripts/row_level_policy_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
RLS disabled (as shipped)   rows returned: 3
      @researchbot  dana@example    sk-REDACTED-openai
      @newsdigest   sam@example     sk-ant-REDACTED
      @dealfinder   kim@example     AKIA-REDACTED-aws
RLS enabled                 rows returned: 0

signed in as dana@example, RLS enabled: 1 row
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
  "key": {"kind": "publishable", "found_in": "str"},
  "tables": [{"name": "str", "sensitive": true,
              "anon_rows_policy_off": 0, "anon_rows_policy_on": 0, "owner_rows": 0}],
  "credentials_exposed": [{"provider": "str", "revocable_by": "str"}],
  "verdict": "open|closed"
}
```

## Failure modes

- **Testing with the service key.** It bypasses policy; that proves nothing.
- **Enumerating from the application.** It knows about its own tables only.
- **Reporting rows without the credentials.** The provider keys are the
  incident.
