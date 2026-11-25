---
name: root-cause-record
description: >-
  Turn a reconstructed incident into a root cause record that names the control
  that failed, and reject statements that name a person or an intention. Use when
  closing an incident, when a postmortem produces a narrative instead of a
  change, or when the same incident class keeps recurring.
allowed-tools: Read, Grep, Glob
---

# A root cause is a control, not a story and not a person

"The on-call engineer missed the alert" is true and useless: it will happen
again next quarter to a different engineer. "We should have been more careful"
names no control and no change.

A usable root cause names **the control that should have caught this and did
not**, in a form the next change can act on and `kci-fix-validation` can later
measure.

## When to use this

At incident close, before the postmortem is written, and in review of any
incident whose remediation was "increased awareness" or "additional training".

## Step-by-step

**1 — List every control in the chain, not just the one that failed last.**
Detection, prevention, authority to stop.

**2 — Mark each present, absent, or present-but-wrong.** The third category is
the one that gets missed.

**3 — The first absent control in the chain is the root cause candidate.**
Later absences are contributing.

**4 — Test the statement: does it name a control?** If it names a person, a
team, or a state of mind, it is rejected. This is mechanical and should be.

**5 — Carry the named control forward as a KCI.** That is the handover to
E5.4 and to the policy change proposal.

## Example

**Input** — a five-control chain and three candidate statements, in
[`scripts/root_cause_record.py`](scripts/root_cause_record.py).

**Output** — a real run:

```
   REJECT  the on-call engineer missed the alert
           -> names no control
   ACCEPT  no control compared the vendor tool description against the version approved at onboarding
```

## Output contract

```json
{
  "incident": "str",
  "root_control": "str",
  "contributing": ["str"],
  "statements": [{"text": "str", "accepted": true}]
}
```

## Common edge cases

- **The control existed and was never reached.** That is evidence about the
  detection in front of it, not a mitigating factor.
- **Several controls absent at once.** The first in the chain is root; naming
  all of them as root produces a list nobody actions.
- **A genuine human error with no control behind it.** Then the finding is that
  no control existed — which is a control statement.

## Failure modes

- **Narrative postmortems.** Readable, and they change nothing.
- **Blame, however gently worded.** It ends the analysis one step early.
- **A root cause with no KCI.** Nothing will ever check that the fix worked.
