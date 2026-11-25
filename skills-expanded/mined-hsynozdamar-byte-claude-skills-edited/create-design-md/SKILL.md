---
name: create-design-md
description: "Create or update a DESIGN.md from an existing repo or public site. Use to document a design language, extract tokens, or give agents persistent UI context. Never modifies product source."
---

# Create DESIGN.md

Write a `DESIGN.md` for one product or coherent website: the design language that governs it, not every value that exists. Only `DESIGN.md` changes; product source, dependencies, configuration and generated files stay as they are. The format is the DESIGN.md contract below, with no competing schema. Repetition, local styling and visual preference are not product intent.

## 1. Choose the mode

- **Repository mode** (a local repo is available, always preferred): write `DESIGN.md` at the root of the selected product. With several deployable products, use the one the user named; if ownership is unclear, ask before writing. Repository evidence can establish normative values, token names, component ownership and documented rationale.
- **URL mode** (public URL, no source): write a reconstructed draft in the current workspace. Evidence can establish only observable patterns and computed values, never token names, ownership, rationale or canonical intent. A supplied URL can verify rendered presentation in repository mode but does not replace source. Procedure, evidence ledger and output rules: [references/url-mode.md](references/url-mode.md), loaded for any URL run.

Both modes share one pipeline: `role -> value -> source -> scope -> recurrence -> confidence`.

1. Collect evidence in the chosen mode.
2. Record source, scope and recurrence per candidate.
3. Normalize into the DESIGN.md schema.
4. Omit candidates that are uncertain, local without a contract, or irrelevant to implementation.
5. Validate frontmatter shape and export compatibility.
6. Write Markdown only after the normalized frontmatter passes.

The draft stays private until lint and export succeed: show or summarize nothing before that. On an invalid shape or missing export category, rewrite the frontmatter and rerun; a category that cannot be repaired is removed and reported as omitted.

## 2. Trace the evidence (repository mode)

Inspect in order: existing `DESIGN.md` and explicit repo guidance; tokens, themes, variables, global styles; shared primitives and variants; representative routes and rendered consumers; surface-local implementations. A source counts only when the selected product imports, references, inherits or renders it. Proposals, migrations, examples, generated outputs, legacy code and similarly named packages are out unless the product uses them.

## 3. Decide what belongs

- Find explicit product intent or a design reference before describing product character; absent that, the Overview states purpose and evidenced direction only.
- YAML comes from named shared tokens and roles in governing sources. Utility classes, repeated literals and component values do not become token scales.
- The frontmatter shape is a hard gate: mappings, flat valid names, canonical typography fields, `rounded.base` for a lone `--radius`. Shape rules, export target selection (`css-tailwind` / `json-tailwind` / `dtcg`), theme-mode encoding and examples: [references/schema.md](references/schema.md). Read it before writing any frontmatter.
- Every prose rule rests on explicit guidance, a named shared token or variant, or a shared owner used by at least two audited surfaces. Otherwise omit it.
- Outside the Overview, every sentence changes an implementation choice. Component inventories, generic advice and restatements of the YAML are deleted.
- Keep the scope and direction of each rule. When implementation conflicts with explicit guidance, document the guidance and report the conflict outside `DESIGN.md`.

## 4. Write the document

Frontmatter first (`version: alpha`, `name`, `description`; more categories per schema.md), then `## Overview` (purpose and evidenced design direction only), then only supported sections in this order: Colors, Themes, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts. No reordering or duplicates; an unknown section only when supported guidance fits no standard one.

- Exact normative values live in YAML (alternate-theme values may sit in the fallback `## Themes` table). Rationale and application guidance live in Markdown.
- A Don't appears only for an explicit prohibition in a governing source.
- An existing `DESIGN.md`'s accepted decisions stay unless the user or current governing evidence replaces them.
- Citations, audit notes, rejected candidates, conflicts and open questions stay out of the file.

Before saving, delete: YAML tokens no governing source names; page-local behavior presented as product-wide; patterns that conflict with explicit guidance; prohibitions not explicitly stated; exact values outside frontmatter or the Themes table; component configuration or documentation methodology in Markdown; any sentence that does not change the result.

## 5. Validate

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md export --format <format> DESIGN.md   # target from schema.md
```

Inspect the export. Every populated frontmatter category the target supports must emit its token category; a missing one is a schema failure even with exit code 0. Rewrite and rerun until it emits (unless the target genuinely cannot represent it, then report the limitation and keep the design information). The `css-tailwind` output families to check are in schema.md. Return nothing while lint or export fails, and leave no exported files behind.

When updating, keep the previous file aside and run `npx @google/design.md diff <previous-file> DESIGN.md`; restore any removed accepted decision unless evidence or the user replaces it.

## 6. Report

Mode and audited product or URL; created or updated `DESIGN.md`; governing sources used; conflicts or unsupported areas omitted; final lint and export results. URL mode labels the output a reconstructed draft.
