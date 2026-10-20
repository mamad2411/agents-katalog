---
name: eu-product-liability
description: >-
  Product liability: Directive (EU) 2024/2853 covers liability for defective products. Covers Directive (EU) 2024/2853. Use when applying the revised product liability rules. Triggers: 2024/2853, product liability.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Product Liability Directive

Directive (EU) 2024/2853 of 23 October 2024 on liability for defective products and repealing Council Directive 85/374/EEC, published in Official Journal L series 2024/2853 on 18 November 2024.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when assessing liability for a defective product.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a manufacturer, importer or injured person.
- Target version: Directive (EU) 2024/2853 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Article 2.** "This Directive shall apply to products placed on the market or put into service after 9 December 2026."
2. **Article 7.** "A product shall be considered defective where it does not provide the safety that a person is entitled to expect or that is required under Union or national law."
3. **Article 9.** "Member States shall ensure that, when determining whether the disclosure of evidence requested by a party is necessary and proportionate, national courts consider the legitimate interests of all parties concerned, including third parties, in particular in relation to the protection of confidential information and trade secrets."

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

- `eu-digital-product-passport`, when the product is also a sustainable product under Regulation (EU) 2024/1781: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-digital-product-passport`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Directive (EU) 2024/2853](https://publications.europa.eu/resource/celex/32024L2853.ENG): Official Journal, OJ L 2024/2853, 18 November 2024, checked 2026-10-06.
