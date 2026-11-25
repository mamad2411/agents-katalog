---
name: authorization-subject-check
description: >-
  Establish which principal a tool call is actually authorised against — the
  requesting human, or the agent's own service account — and what the resulting
  audit row can name. Use when a user reaches a scope they do not hold, or when
  every log line shows the same caller.
allowed-tools: Read, Grep, Glob
---

# Authorised as whom?

Privilege compromise in an agentic system is rarely a stolen credential. It is
authorisation evaluated against the **agent's** identity while the request came
from a user who does not hold the scope — and an audit trail that then names
the agent on every row, so the human cannot be recovered at all.

## When to use this

Any time an agent calls something on a user's behalf. Run it before designing
delegation, because the answer decides whether delegation is missing or merely
unenforced.

## Procedure

**1 — Find the authorisation decision point.** The single place where a scope
is compared against a holder. If there are several, list them all; they will
disagree.

**2 — Name the subject at that point.** Is the compared identity the requesting
user, or the process's own account? A service account with a union of every
scope any user might need is the shape to look for.

**3 — Run the asymmetric probe.** Have a user holding a narrow scope request an
action requiring a wider one. If it succeeds, authorisation is on the workload,
not the requester.

**4 — Read one audit row.** Does it name a human? A row naming `agent-svc` is
complete, well-formed and useless: it answers "what ran", never "who caused
it".

**5 — Separate the two fixes.** Authorising on the requester and *recording*
the requester are different changes with different owners; a report that merges
them gets half-implemented.

## Example

**Input** — the fixture committed at the top of [`scripts/authorization_subject_check.py`](scripts/authorization_subject_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
requestertheir scopes                                asked for       allowed?
dana    ['reports:read']                            db:admin        True
priya   ['db:admin', 'reports:read', 'reports:write']db:admin        True

AUDIT TRAIL
   actor=agent-svc  tool=drop_table   allowed=True
   actor=agent-svc  tool=drop_table   allowed=True
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
  "decision_points": [{"site": "str", "subject": "requester|workload|both"}],
  "probe": {"user_scopes": ["str"], "required": "str", "succeeded": true},
  "audit_row": {"names_human": false, "fields": ["str"]},
  "fixes": {"authorize_on_requester": true, "record_requester": true}
}
```

## Failure modes

- **Accepting that the user is "in the request".** Present in the payload is
  not the same as compared at the decision point.
- **Testing with an admin.** The probe needs a user who genuinely lacks the
  scope.
- **Reporting the audit gap as a logging bug.** It is the reason the incident
  cannot be scoped later.
