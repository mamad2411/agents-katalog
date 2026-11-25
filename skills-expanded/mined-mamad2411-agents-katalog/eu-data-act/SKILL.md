---
name: eu-data-act
description: >-
  Data Act: Regulation (EU) 2023/2854 sets rules on fair access to and use of data. Covers Regulation (EU) 2023/2854. Use when applying the Data Act. Triggers: Data Act, 2023/2854.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Data Act

Regulation (EU) 2023/2854 of 13 December 2023 on harmonised rules on fair access to and use of data (Data Act).

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when applying the Data Act to access and use of data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a data holder, user or recipient.
- Target version: Regulation (EU) 2023/2854 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **text.** "In order to allow for the emergence of liquid, fair and efficient markets for non-personal data in the Union, the party that has the right to offer such data on a market must be clarified."
2. **Article 13.** "Unless otherwise provided for in Union law, including Article 4(6) and Article 5(9) of this Regulation, or by national legislation adopted in accordance with Union law, an obligation to make data available to a data recipient shall not oblige the disclosure of trade secrets."
3. **Article 15.** "The obligation to demonstrate that the public sector body was unable to obtain non-personal data by purchasing them on the market shall not apply where the specific task carried out in the public interest is the production of official statistics and where the purchase of such data is not allowed by national law."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

- `gdpr`, when the data includes personal data: `npx skills add ScaleDockHQ/scaledock-skills --skill gdpr`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Regulation (EU) 2023/2854](http://publications.europa.eu/resource/oj/L_202302854.ENG): Official Journal, Official Journal, 13 December 2023 act, checked 2026-10-06.
