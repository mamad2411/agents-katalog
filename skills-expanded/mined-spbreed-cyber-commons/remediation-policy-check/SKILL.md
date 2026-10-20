---
name: remediation-policy-check
description: >-
  Classify remediation actions on reversibility and blast radius so each
  runbook's automation tier is derived rather than chosen. Use before writing
  response automation, when a runbook's tier is set by its author's confidence,
  or when the blast radius of a response is unknown until it fires.
allowed-tools: Read, Grep, Glob
---

# Decide once what may be done without asking, and let every runbook inherit it

If each runbook picks its own automation tier, the blast radius of your response
is unknown until the response happens. Two properties of the *action* decide it,
and neither is a property of the person writing the runbook.

**Reversibility** — can this be undone without a human decision?
**Blast radius** — one agent, one tenant, or the estate?

Reversibility outranks radius. An irreversible action on one agent is manual; a
reversible one across the estate is human-in-the-loop.

## When to use this

Before the first runbook is written, and whenever a new remediation action is
added to the catalogue. Re-run it when an action's reversibility changes —
"revoke token" becomes irreversible the moment there is no re-issue path.

## Step-by-step

**1 — List the actions, not the incidents.** The policy is about what can be
done, not about when.

**2 — Ask whether each is reversible without a human.** An undo that needs an
approval is not reversible for this purpose.

**3 — Set the radius honestly.** "One agent" means one, not one class.

**4 — Derive the tier; do not assign it.** If you find yourself arguing for an
exception, the two properties are wrong, not the policy.

**5 — Publish the table.** Every runbook cites a row rather than restating it.

## Example

**Input** — nine actions, in
[`scripts/remediation_policy_check.py`](scripts/remediation_policy_check.py).

**Output** — the rows that make the ordering visible:

```
force HITL on every agent            True   estate   human-in-the-loop
delete the agent's workdir          False    agent   manual
```

Estate-wide and reversible is a lower tier than single-agent and irreversible.

## Output contract

```json
{
  "actions": [{"action": "str", "reversible": true,
               "radius": "agent|tenant|estate", "tier": "automated|human-in-the-loop|manual"}],
  "by_tier": {"automated": 0, "human-in-the-loop": 0, "manual": 0}
}
```

## Common edge cases

- **Reversible in theory.** If restoring takes six hours of manual work, it is
  not reversible for an incident that lasts twenty minutes.
- **Radius depends on the target.** Then it is two actions, not one.
- **An action nobody has ever taken.** It still needs a tier, before somebody
  needs it at 3am.

## Failure modes

- **Tier by confidence.** The most automated runbooks end up written by whoever
  was most sure.
- **Radius over reversibility.** Produces automated deletes because they only
  touch one agent.
- **A policy with no published table.** Then every runbook re-derives it and
  they disagree.
