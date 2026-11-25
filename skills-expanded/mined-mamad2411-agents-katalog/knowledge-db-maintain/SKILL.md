---
name: knowledge-db-maintain
description: Use when creating or maintaining a kb-core@2 local Markdown knowledge base with canonical info and knowledge entry templates, package-defined metadata, self-contained validation, generic filters, provenance tracing, or metadata-aware search.
---

# Knowledge DB Maintain

Use this skill to change a local knowledge base that contains `source/`, `info/`, `knowledge/`, `kb-package.json`, and `kb-package-schema.json`. Keep its grounding chain strict: `knowledge -> info -> source`.

## Three-Layer Meaning

Keep the three layers semantically distinct, not merely linked by frontmatter:

| Layer | Store | Do not store |
| --- | --- | --- |
| `source/` | Original, attributable material: web pages, papers, API references, source-file excerpts, logs, transcripts, datasets, or other primary evidence. Preserve enough context to re-check it. | Extracted conclusions or implementation advice. |
| `info/` | Objective facts extracted from one or more source entries: what an API does, signature and parameters, preconditions, return values, side effects, limits, and version-specific observations. Cite every supporting source. | Raw source dumps, recommendations, workflows, or unsupported generalizations. |
| `knowledge/` | Reusable guidance derived from info entries: how to combine APIs to implement a feature, recommended execution routes, decision criteria, tradeoffs, and operational constraints. Declare every dependency with `depends_on`. | New facts without info support, raw evidence, or a restatement of API reference material. |

Write in this order: add or update `source` first, extract only supported facts into `info`, then create or revise `knowledge` only when the info supports a reusable conclusion. Do not create knowledge merely because a source or info entry changed. Keep unresolved questions and planned experiments out of knowledge until evidence supports a conclusion.

## Entry Body Contract

Use exactly one H1 equal to the frontmatter `title`. Keep the required H2 headings in the shown order; add detail only with H3 or lower headings. Heading-like text inside fenced code blocks does not count.

Write every `info` body as:

```markdown
# <title>

## Scope
<!-- Coverage, applicability, and explicit exclusions. -->

## Facts
<!-- Objective facts supported by source. -->

## Notes
<!-- Source positioning, extraction method, conflicts, uncertainty, and limits. -->
```

Write every `knowledge` body as:

```markdown
# <title>

## Problem and Context
<!-- Reusable problem, applicability, and prerequisites. -->

## Conclusion
<!-- Derived guidance, recommendation, or decision rule. -->

## Limits
<!-- Non-applicability, risks, version constraints, and unknowns. -->

## Reasoning
<!-- How depends_on info supports the conclusion. -->
```

Do not introduce new facts in `knowledge`; put supporting facts in `info` first. The generated package checker rejects missing, duplicated, additional, or reordered H1/H2 headings.

## Package and Entry Contract

Every package must declare its human-facing identity in root `kb-package.json`. `name` and
`description` are required non-empty strings and are what a catalog consumer shows to users;
the repository/package identifier remains the stable technical `package_name`.

```json
{
  "schema": "kb-package@1",
  "name": "SAP BTP Knowledge Base",
  "description": "Implementation guidance and verified facts for SAP BTP."
}
```

Every package extends `kb-core@2` in its root `kb-package-schema.json`. Core frontmatter fields are `schema`, `kind`, `title`, `status`, and `updated`; `info` also requires `source`, while `knowledge` requires `depends_on`. Package-specific values may appear only under the nested `metadata` mapping.

```json
{
  "schema": "kb-package-schema@2",
  "extends": "kb-core@2",
  "fields": {
    "country": {
      "type": "string",
      "multiple": true,
      "description": "Countries where this entry applies.",
      "filterable": true,
      "normalization": "upper-case-code",
      "search": { "enabled": true, "weight": 700 },
      "aliases": { "JP": ["Japan", "日本"] }
    }
  }
}
```

Package fields use `string`, `integer`, `number`, `boolean`, or `date`. Every definition
explicitly declares its type, `multiple`, a non-empty `description`, `filterable`, compatible
`normalization`, and `search.enabled`. Searchable fields use an integer `search.weight` from
`1..1000`; disabled search fields omit `weight`. `multiple` selects an array versus single
value. Aliases are allowed only for searchable string fields. Do not put business fields such
as country or capability in directories or top-level frontmatter.

```yaml
---
schema: kb-entry@2
kind: info
title: Intercompany Processing
status: active
updated: '2026-07-10'
source:
  - source/sap/"16T".md
metadata:
  country:
    - JP
    - DE
  capability:
    - "16T"
---
```

## Commands

Run `kb schema` before constructing a query; `kb schema --json` returns the complete merged core-plus-package contract. Use generic filters, never a field-specific switch:

```text
kb scan
kb new info sap/api.md --title "API behavior" --source source/sap/api.md
kb new knowledge sap/api-guidance.md --title "API guidance" --depends-on info/sap/api.md
kb search "intercompany" --filter country=JP
kb search --filter country=JP --filter country=DE --filter capability=16T
kb list info --filter country=BR
kb read info/sap/16T.md --meta-only
kb trace knowledge/sap/intercompany.md
```

Repeated values of one `--filter` key are OR; different keys are AND. Filters are normalized exact values. Aliases increase keyword recall only, never exact-filter matches. An empty search is permitted only with at least one filter. Search ranks declared metadata fields using their package-owned weights; paths and folder names do not supply metadata semantics.

Use `scan` or `validate` after all changes. It rejects a missing/invalid schema, undeclared fields, bad cardinality or types, missing required package fields, missing `source`/`depends_on`, and invalid provenance references.

`scan` and `validate` delegate to the package-owned `scripts/check_package.py --kb <root>`
created by `kb init`; that generated checker is the authority for package validation and
version-directory layout. It returns the checker exit code and diagnostics unchanged. Keep
directories for maintenance organization only: queries, filters, aliases, scoring, and
validation semantics come from frontmatter and `kb-package-schema.json`, never a path.

## Initialize a Package

Run `kb init` in an empty package root to materialize the generic schema, empty
`source/`, `info/`, and `knowledge/` roots, package checker, catalog helpers, and artifact
workflow. It also creates `templates/info.md` and `templates/knowledge.md`; use `kb new` to
render them with core frontmatter and the canonical body structure. It is safe to rerun only
while generated assets remain byte-identical; it refuses
to overwrite changed files or directory collisions. The generated Python producer validates
the package and builds `kb-catalog@3` SQLite locally; its CI needs only package-local scripts,
PyYAML, and the repository's MinIO publication secrets. It never checks out or imports a
query service. The v3 catalog stores the package identity plus `field_value_facets`, computed
from declared `filterable` metadata values while the catalog is built. Consumers can therefore
enumerate legal filter values without a second Markdown scan. A service consumes only the
published v3 artifact and validates its generic v3 contract.
