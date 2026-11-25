---
name: policy-change-proposal
description: >-
  Turn a root cause record into a reviewable policy diff with the incident
  attached as evidence, and name what the diff does not fix. Use at the end of an
  incident, when a postmortem's lessons never reach the policy, or when a
  proposed control change needs to be argued on evidence rather than opinion.
allowed-tools: Read, Grep, Glob
---

# The last step of an incident is a change to what is allowed

Most incidents end with a change to what is *deployed*. The policy that
permitted the incident is usually untouched, so the next system built under it
reproduces the conditions.

Stated as a diff — clause, old value, new value, and the incident as the reason
— the change can be argued with. Stated as a postmortem paragraph, it cannot.

## When to use this

After `root-cause-record` and `kci-fix-validation`, with both in hand. Before
the incident is closed, because the appetite for a policy change decays fast.

## Step-by-step

**1 — Quote the clause as it stands.** A proposal that paraphrases the current
policy is arguing with something nobody wrote.

**2 — Write the new value as text that could be adopted.** Not a direction of
travel — the words.

**3 — Put the measured number in the "why".** "41% of calls carried provenance
during the incident" ends an argument that "we should tighten provenance"
starts.

**4 — Name what the diff does NOT address.** A KCI that no policy change fixes
is an engineering item, and saying so stops it falling between the two.

**5 — Expect the expensive clause to be refused, and say so.** A proposal whose
every line is easy did not come from a real incident.

## Example

**Input** — a root cause record and four policy clauses, in
[`scripts/policy_change_proposal.py`](scripts/policy_change_proposal.py).

**Output** — one change from a real run:

```
  tool.call.provenance
  - recorded when present
  + required; a call without it is refused
    why: 41% of calls carried provenance during the incident, so it was optional
```

## Output contract

```json
{
  "incident": "str",
  "changes": [{"clause": "str", "from": "str", "to": "str", "why": "str"}],
  "unaddressed": ["str"]
}
```

## Common edge cases

- **The policy already required it.** Then the gap is engineering, not policy —
  and that is the finding.
- **The change breaks integrations.** State it in the diff. That review is the
  one that should happen before it ships.
- **No clause covers the behaviour.** A new clause is a bigger ask than an
  amendment; say which you are making.

## Failure modes

- **Proposals with an opinion in the "why" column.** They get argued on
  opinions, and the loudest person wins.
- **Silence on what is not fixed.** The unaddressed KCI is the one that recurs.
- **Deferring to "the next policy review".** By then the evidence is cold.
