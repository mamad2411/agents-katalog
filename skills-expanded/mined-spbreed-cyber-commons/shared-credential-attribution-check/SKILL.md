---
name: shared-credential-attribution-check
description: >-
  Find credentials held by more than one agent and show what sharing does to
  attribution and to containment — who the downstream records, and what
  revoking it stops. Use when several agents call the same API, or when asked
  which agent did something and the record cannot say.
allowed-tools: Read, Grep, Glob
---

# One credential, three agents, one line in the log

A shared credential is usually adopted for convenience and paid for during an
incident. It costs two things at once: the downstream cannot attribute an
action to an agent, and the only containment available stops **every** holder.

## When to use this

Whenever more than one agent, job or replica authenticates downstream. Also
before an incident: this is the check whose absence turns a contained problem
into an outage.

## Procedure

**1 — Enumerate holders per credential.** Group by the secret, not by the
service. Environment variables, mounted files, a shared secrets-manager path
and a baked-in image layer are all the same credential when the value matches.

**2 — Read a downstream record.** Whatever the caller is identified by — an API
key id, a client id, a service account — record what the downstream can print.
If three agents map to one identifier, attribution ends there.

**3 — Simulate the destructive call.** Have one holder perform something
irreversible. Ask, from the downstream record alone, which holder did it. Write
down the answer even when it is "cannot be determined"; that sentence is the
finding.

**4 — Cost the containment.** Revoke the credential on paper and list what
stops. The count of unrelated things that stop is the number to report.

**5 — Propose per-workload identity,** and say what it costs: one credential
per agent, issued by the platform rather than pasted, so revocation is
per-agent and attribution is free.

## Example

**Input** — the fixture committed at the top of [`scripts/shared_credential_attribution_check.py`](scripts/shared_credential_attribution_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
what the downstream service recorded:
   caller=svc-agent-7f3a1c  read    reports
   caller=svc-agent-7f3a1c  read    reports
   caller=svc-agent-7f3a1c  read    reports
   caller=svc-agent-7f3a1c  delete  prod.customers

incident: delete on prod.customers
which agent did it? candidates: ['deploy-agent', 'patch-agent', 'triage-agent']
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
  "credentials": [{"id": "str", "holders": ["str"], "source": "env|file|manager|image"}],
  "downstream_identifier": {"field": "str", "distinguishes_holders": false},
  "destructive_probe": {"actor": "str", "recoverable_from_record": false},
  "containment": {"revoking_stops": ["str"], "collateral": 0}
}
```

## Failure modes

- **Grouping by service instead of by secret value.** Two names, one key, is
  still one credential.
- **Assuming the log will disambiguate.** Read an actual row before assuming a
  field exists.
- **Reporting only attribution.** The containment cost is what makes it urgent.
