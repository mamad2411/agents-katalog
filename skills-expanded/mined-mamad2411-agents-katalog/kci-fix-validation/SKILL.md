---
name: kci-fix-validation
description: >-
  Re-measure the key control indicators an incident moved and report which the
  fix actually restored. Use when closing a remediation, when a ticket is marked
  done without evidence, or when a control was rebuilt and nobody has checked
  whether it now meets its target.
allowed-tools: Read, Grep, Glob
---

# Closing a ticket is not evidence that a control came back

A fix is a claim. The KCIs are how the claim is checked: re-measure the
indicators the incident moved and see which returned to target.

Doing it automatically is the point. Done by hand, it happens for the incidents
somebody remembers, which are not the ones where it matters.

## When to use this

On every remediation that claims to restore a control, before the incident is
closed — and again at the next measurement cycle, because a fix that holds for a
week and then regresses is common.

## Step-by-step

**1 — Take the KCIs from the root cause record.** Not all of them; the ones the
incident actually moved.

**2 — Read the healthy baseline, not just the target.** A control that was
never at target before the incident did not regress.

**3 — Re-measure after the fix, the same way.** A different measurement is a
different indicator.

**4 — Report restored, not restored, and untouched separately.** Untouched
indicators are noise in the report and belong out of it.

**5 — Attach before/during/after to the incident record.** That is the artefact
an auditor asks for, and it is worth more than the postmortem.

## Example

**Input** — six indicators with three readings each, in
[`scripts/kci_fix_validation.py`](scripts/kci_fix_validation.py).

**Output** — the part that changes the outcome:

```
   KCI-03  refunds with a matching approval
          target >= 0.99, measured 0.94 — the fix did not reach this one
   KCI-04  mean minutes to detect a scope breach
          target <= 15, measured 118.0 — the fix did not reach this one
```

Detection improved from 194 minutes to 118 and is still eight times target.
Without the re-measurement, that reads as done.

## Output contract

```json
{
  "restored": ["str"],
  "not_restored": ["str"],
  "regressed": ["str"]
}
```

## Common edge cases

- **Partially restored.** Improvement is not restoration; the target is the
  test, not the direction of travel.
- **The indicator was already failing before the incident.** Then it is a
  standing gap, not incident damage.
- **The measurement changed with the fix.** A new instrument reading better is
  not a control reading better.

## Failure modes

- **Marking remediated on ticket closure.** The most common way a control gap
  survives its own incident.
- **Reporting an average across indicators.** Two restored and two not is not
  "50% recovered", it is two open gaps.
- **Measuring once.** Regression at the next cycle is the normal case.
