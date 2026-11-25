---
name: kci-control-measurement
description: >-
  Measure key control indicators against a real repository and report each gap
  with the lesson that closes it. Use when turning framework controls into
  something measurable, when a control is asserted but never verified, or when a
  governance report needs an artefact other than a score.
allowed-tools: Read, Grep, Glob
---

# A control indicator is only an indicator if something measures it

Otherwise it is a sentence in a policy. The test is mechanical: can you compute
this number from the estate, today, without asking anyone?

So these are computed from `cybertravels/` — the same tree C2.3 scans and B1.1
draws — and the output is a list of gaps each naming the lesson that closes it,
not a maturity score. A governance report whose only artefact is a number
changes nothing.

## When to use this

After control mapping (F1.4) and before any assurance claim. Re-run it after
every change to the estate: an indicator measured once is a snapshot, and the
whole argument for KCIs is that point-in-time testing fails for systems that
change weekly.

## Step-by-step

**1 — Write the indicator as a computation, not a question.** "Object handlers
that compare an owner" is measurable; "is authorisation adequate" is not.

**2 — State the target beside it.** An indicator with no target cannot be met
or missed.

**3 — Compute it from source, not from a register.** A register records what
somebody believed at the time.

**4 — Include at least one indicator the estate passes.** A set that always
reports GAP cannot be shown to discriminate.

**5 — Attach a mitigation to every gap, naming where the fix is taught.** A gap
with no next step is a complaint.

## Example

**Input** — the `cybertravels/` tree, read at run time.

**Output** — a real run:

```
KCI-01  object handlers that compare an owner       == 1.00      0.29  GAP
KCI-05  egress control present                         == 1      0.00  GAP
KCI-06  no credential literal in the source            == 0      0.00  ok
```

KCI-05 measures a component that does not exist. That is the backlog, stated in
the same units as everything else.

## Output contract

```json
{
  "kcis": [{"id": "str", "indicator": "str", "target": "str",
            "measured": 0.0, "met": true}],
  "gaps": [{"id": "str", "gap": "str", "mitigation": "str"}]
}
```

## Common edge cases

- **The indicator measures a control you have not built.** It reads zero and
  always will. That is a backlog item, not an estate failure.
- **A denominator of zero.** No object handlers means the indicator is
  undefined, not perfect.
- **The measurement is gameable.** If renaming a function moves the number, it
  measures naming.

## Failure modes

- **Scoring instead of listing gaps.** "72% compliant" is not actionable by
  anyone.
- **Measuring from the register.** It records intent, not state.
- **Indicators that all fail.** Nothing shows the instrument works.
