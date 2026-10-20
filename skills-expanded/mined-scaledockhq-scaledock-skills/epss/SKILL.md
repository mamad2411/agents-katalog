---
name: epss
description: >-
  EPSS: estimate the probability that a vulnerability will be exploited with the Exploit Prediction Scoring System. Covers EPSS. Use when estimating exploit probability. Triggers: EPSS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# EPSS

The Exploit Prediction Scoring System (EPSS) from the FIRST EPSS Special Interest Group: what the score and percentile mean, how the model is calibrated and measured, how to combine EPSS with local context and the CISA KEV catalog, and how to get the data. Read from the FIRST EPSS pages for the current model, EPSS v5 (v2026.06.15).

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Vulnerability management owner, or a tool that ingests EPSS scores and uses them for prioritization.
- Target version: EPSS (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **What EPSS measures.** "The EPSS score is a calibrated probability: the estimated likelihood that exploitation activity for a given vulnerability will be observed across EPSS data partners in the next 30 days."
2. **Combining EPSS with other signals.** "As a general rule of thumb: when a vulnerability appears on CISA KEV, treat it as actively exploited and prioritize accordingly, regardless of EPSS score."
3. **Common misuses.** "Do not multiply an EPSS score by an ordinal (such as CVSS) and think that produces a combined "risk score.""
4. **Known limitations.** "The score should be read as a probability and used as a prioritization input, not as a pass/fail threshold."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Stored EPSS values keep the score, the percentile, the score date and the model version, and no workflow multiplies EPSS by CVSS.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `cvss`, `ssvc`, `cisa-kev`, `cve-json`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [How EPSS Works](https://www.first.org/epss/how-it-works): FIRST EPSS SIG documentation, EPSS v5 (v2026.06.15), page read 2026-10-06, checked 2026-10-06.
- [Using EPSS](https://www.first.org/epss/using-epss): FIRST EPSS SIG documentation, EPSS v5 (v2026.06.15), page read 2026-10-06, checked 2026-10-06.
- [Get the Data](https://www.first.org/epss/data): FIRST EPSS SIG documentation, EPSS v5 (v2026.06.15), page read 2026-10-06, checked 2026-10-06.
