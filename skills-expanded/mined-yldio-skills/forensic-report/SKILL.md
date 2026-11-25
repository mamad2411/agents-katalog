---
name: forensic-report
description: Use when writing, assembling or validating a forensic report or report package — after evidence has been collected, when the user asks to write up an investigation, produce findings, review a draft report, or check a package before release.
user-invocable: true
disable-model-invocation: true
---

# Forensic report — write and validate

Turn collected evidence into a report package a sceptical reader can challenge
and a second examiner can reproduce. Packages follow the layout of the
`forensic-investigation` skill's `assets/template/`; procedure context is
`references/RUNBOOK.md` steps 5–7 and conduct rules are `references/PROCESS.md`
Part 2, both in this skill's folder.

Two modes. Writing a package: follow "Write". Checking one (yours or
another's): follow "Validate". A package is not done until it passes Validate.

## Write

Order: REPORT.md findings first, then TIMELINE.md, METHODOLOGY.md,
POSTMORTEM.md, INDICATORS.md, RECOMMENDATIONS.md, README.md last (it
summarises the rest). Every template carries its own fill instructions.

Finding anatomy — every finding, no exceptions:

```text
### N. Finding F-0X — <one plain assertion>
Source: `evidence/<specific-file>` [, `analysis/<file>`]
<the data>
<the reasoning, arithmetic shown inline>
Alternatives considered: <each one, and what excludes it or keeps it open>
Consequence: <what it means operationally>
What would change this: <the observation that would overturn it>
Confidence: <established fact | assessment low/moderate/high | reported | unknown>
```

Phrasing rules:

- State how strongly the findings support one explanation over a named
  alternative. Never state the probability that the explanation is true —
  that inversion (the transposed conditional) is the classic forensic error.
- Confidence words come from the fixed vocabulary in METHODOLOGY §6. Grade by
  corroboration and tamper-resistance: one uncorroborated tamperable source
  is at most a weak assessment, whatever it shows.
- Facts and interpretation stay visibly separate. Opinions are labelled and
  carry their basis.
- No claims about guilt, intent or identity beyond what the records carry. A
  credential is not a person; a user agent is not an identity.
- Unknowns are written as unknown. Do not fill a gap with a plausible guess.
- A layperson must be able to follow the results; mechanism detail goes under
  the plain statement.
- Cite specific evidence files, not globs, wherever a specific file exists.

## Validate

Work through `references/validation.md`, gate by gate, and report failures
with file and line. Two rules for the validator:

1. **Blind first.** Re-derive the key figures from `analysis/` and `evidence/`
   before reading the report's conclusions, and write your numbers down.
   Then compare. Checking the report's arithmetic after reading its
   conclusions is how reviewers inherit the author's errors.
2. **Verify, don't trust.** Run the hash check. Re-run the transform script if
   it exists. Resolve every cross-reference (F/Q/R/C identifiers, § numbers).
   A checklist item passes on evidence, never on the document's say-so.

Report the outcome as: gates passed, gates failed (with locations), and a
verdict — release, fix first, or re-examine.

## Rationalisations to refuse

| Thought | Reality |
|---------|---------|
| "The finding is obvious, one source is enough" | Single-source findings are where corrections come from. Corroborate or downgrade the confidence label. |
| "I'll round the numbers for readability" | Show exact figures and the arithmetic; readability comes from structure. |
| "The reader will understand this means X is guilty" | The report states evidence strength against alternatives. Nothing more. |
| "Validation slows the release" | An uncaught material error costs a public correction and the package's credibility. |
| "I wrote it, so I know it's consistent" | Authors cannot see their own drift. Run the checklist or hand it to someone who will. |

## Handling

Report packages contain sensitive material. Keep them inside their declared
boundary and never paste their contents into external services. This skill
sends nothing to any external service; writing and validation are local file
work over the package.
