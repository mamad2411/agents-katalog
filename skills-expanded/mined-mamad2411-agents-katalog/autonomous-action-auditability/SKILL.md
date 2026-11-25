---
name: autonomous-action-auditability
description: >-
  Decide whether an audit record makes an autonomous action answerable, and
  demonstrate a record that is complete, internally consistent and false. Use
  when an audit trail is being accepted as evidence of what an agent did.
allowed-tools: Read, Grep, Glob
---

# Complete, consistent, and false

Auditability of autonomous action is not "is there a record". A record can name
the acting identity, the principal, the delegation chain and the scopes, be
internally consistent, and still be false — because the token it rests on was
impersonated rather than delegated. Answerable requires the record *and* a way
to tell those apart.

## When to use this

When designing audit records for agent actions, and when one is offered as
evidence in an investigation or to an assessor.

## Procedure

**1 — Define answerable as a set of fields.** Acting identity, principal,
delegation chain, scopes exercised, and whether the run is replayable. Fewer
than all of them and some question is unanswerable; say which.

**2 — Score a complete record against the definition.** This is the good case
and it should pass — establishing that the definition is achievable rather than
aspirational.

**3 — Construct the impersonation case.** A token where the actor equals the
subject rather than being nested under it. The record is complete and consistent
and the attribution is wrong. Show that it scores identically on completeness.

**4 — Add the check that separates them.** Delegation has a distinct actor claim
nested under the subject; impersonation does not. The record must carry that
distinction, or completeness is all you can ever measure.

**5 — Test the no-replay case.** A record whose run cannot be replayed answers
what happened and never why. Mark it partially answerable rather than
answerable.

## Example

**Input** — the fixture committed at the top of [`scripts/autonomous_action_auditability.py`](scripts/autonomous_action_auditability.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
action            merge_pr #8812
acting_identity   patch-agent
on_behalf_of      dana@corp
chain             dana@corp → orchestrator → patch-agent
scopes_held       ['repo:read', 'repo:write']
replayable        True
replay_gaps       []
answerable        True
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
  "definition": {"fields": ["str"], "replayable_required": true},
  "cases": [{"name": "complete|impersonated|no_replay", "fields_present": ["str"],
             "consistent": true, "answerable": false, "why": "str"}],
  "distinguisher": {"check": "str", "present": false}
}
```

## Failure modes

- **Measuring completeness.** The false record is complete.
- **Accepting a matching subject as delegation.** Impersonation matches too.
- **Calling a non-replayable record answerable.** It answers what, not why.
