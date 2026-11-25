---
name: wsjf
description: The WSJF priority formula and its 1-2-3-5-8-13-20 scales, with who scores each component. Use when scoring or ranking a task or a queue ("WSJF", "prioritise", "business value vs job size"), and as the single source the product-owner and tech-lead roles and the feature-sanity-check skill refer to.
---

# WSJF — one scale, one place

`WSJF = (BV + TC + RR) / JS`, each component on the scale **1, 2, 3, 5, 8, 13, 20**.

| Component | Who scores it | Meaning |
|---|---|---|
| **BV** — business value | product owner | value for the user or the owner now |
| **TC** — time criticality | product owner | what is lost by postponing; does the value expire |
| **RR** — risk reduction / opportunity enablement | both; take the agreed value | does it reduce future risk, does it enable future features |
| **JS** — job size | tech lead | volume plus technical risk of the implementation (a risky small change is a large JS) |

Rules:

- A score without a one-sentence justification is invalid. Write each justification before computing the formula.
- A score disagreement of more than one step of the scale between two assessors: work out whose grounds are stronger,
  do not average.
- WSJF ranks "do now" and "do later" among themselves. It does not override "do not do": a high score with no real
  pain means the BV was scored on a hypothesis, so fix the BV, not the verdict.
- A score fitted to the wanted verdict is a red flag.

Severity of review findings (critical, major, minor) is a different scale; it lives in `docs/review-contract.md` of the
project and is referenced from there, not repeated.
