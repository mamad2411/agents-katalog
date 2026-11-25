---
name: eu-digital-product-passport
description: >-
  Digital product passport: Regulation (EU) 2024/1781 establishes ecodesign requirements and the product passport. Covers Regulation (EU) 2024/1781. Use when applying the digital product passport. Triggers: DPP, ESPR, 2024/1781.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Digital product passport

Regulation (EU) 2024/1781 of 13 June 2024 establishing a framework for the setting of ecodesign requirements for sustainable products. The fetched text sets the digital product passport rules inside that framework.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when creating or reading a digital product passport.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a manufacturer or another economic operator.
- Target version: Regulation (EU) 2024/1781 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Article 3.** "Products shall only be placed on the market or put into service if they comply with the ecodesign requirements applicable to those products, set out in the delegated acts adopted pursuant to Article 4."
2. **text.** "By 19 July 2026, the Commission shall set up a digital registry (the ‘registry’) which stores in a secure manner at least the unique identifiers."
3. **text.** "When preparing a delegated act to be adopted pursuant to paragraph 3, point (a), the Commission shall: (a) assess the prevalence and environmental impacts of the destruction of certain unsold consumer products;"

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

- `eu-product-liability`, when a defect also raises liability under Directive (EU) 2024/2853: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-product-liability`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Regulation (EU) 2024/1781](http://publications.europa.eu/resource/oj/L_202401781.ENG): Official Journal, Official Journal, 13 June 2024 act, checked 2026-10-06.
