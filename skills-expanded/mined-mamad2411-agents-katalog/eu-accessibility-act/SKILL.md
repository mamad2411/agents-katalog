---
name: eu-accessibility-act
description: >-
  European Accessibility Act: Directive (EU) 2019/882 sets accessibility requirements for products and services. Covers Directive (EU) 2019/882. Use when applying the European Accessibility Act. Triggers: 2019/882, EAA.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# European Accessibility Act

Directive (EU) 2019/882 of 17 April 2019 on the accessibility requirements for products and services, published in Official Journal L 151 of 7 June 2019.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when applying the accessibility requirements for products and services.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a provider or public body placing a product or service in scope on the Union market.
- Target version: Directive (EU) 2019/882 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Article 32.** "this shall, with regard to information screens, be limited to interactive screens located within the territory of the Union;"
2. **Article 9.** "Before placing a product on the market, importers shall ensure that the conformity assessment procedure set out in Annex IV has been carried out by the manufacturer."
3. **Article 4.** "Upon a request from the market surveillance authorities or from the authorities responsible for checking compliance of services, as applicable, the economic operators shall provide the authorities with a copy of the assessment referred to in paragraph 2."

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

- `en-301-549`, when a product or service also has to meet the harmonised ICT standard: `npx skills add ScaleDockHQ/scaledock-skills --skill en-301-549`
- `wcag`, when the work is web content under a later presumption of conformity: `npx skills add ScaleDockHQ/scaledock-skills --skill wcag`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Directive (EU) 2019/882](https://publications.europa.eu/resource/celex/32019L0882.ENG): Official Journal, OJ L 151, 7 June 2019, checked 2026-10-06.
