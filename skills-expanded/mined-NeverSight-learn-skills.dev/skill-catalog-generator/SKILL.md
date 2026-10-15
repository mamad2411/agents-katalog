---
name: skill-catalog-generator
description: Create, audit, and update searchable skill catalogs, marketplace groupings, registry metadata, quality scores, demo matrices, and install/discovery surfaces for AI-agent skill repositories. Use when turning a SKILL.md repository into a catalog, ranking skills, finding coverage gaps, or preparing public/private skill marketplace metadata.
---

# Skill Catalog Generator

Use this skill to turn a recurring product-operations problem into a concrete, reviewable artifact instead of generic advice.

## Workflow

1. Inventory every skill folder, frontmatter description, references, evals, examples, agents metadata, and install path.
2. Read `references/catalog-generation-patterns.md`.
3. Normalize skills by user job, lifecycle area, product type, and marketplace group instead of folder order alone.
4. Score quality with observable evidence: trigger clarity, reference depth, eval coverage, behavior demo, installability, and freshness.
5. Produce a catalog update, gap matrix, publish checklist, and automation hooks.

## Guardrails

- Do not fabricate quality signals; mark missing evidence as a gap.
- Separate generated registry facts from editorial marketplace claims.
- Keep private/internal skills and public catalog content separated.
- Prefer stable skill names, links, and install commands over marketing-heavy copy.

## Output format

```text
Catalog source:
Skill count / install source:

Grouping model:
- <group> -> <skills>

Quality score table:
| Skill | Trigger | Depth | Eval | Demo | Install | Gaps |
| --- | --- | --- | --- | --- | --- | --- |

Coverage gaps:
- <gap> -> <next skill or reference>

Publish actions:
- <registry/catalog/docs/verification step>
```
