---
name: martix-markdown
description: 'Markdownlint guidance for Markdown lint triage and durable fixes while keeping upstream defaults separate from repo-local overlays. Use when users mention markdownlint, markdownlint-cli2, MD rule IDs, suppressions, custom rules, Prettier conflicts, link or alt-text quality, or whether a Markdown issue belongs in content, config, or repo-overlay guidance.'
license: Complete terms in LICENSE.txt
---

## MartiX Markdown router

- Route tight: assess scope first, open one nearest rule file, and add a
  reference only when the question widens.
- Start with the nearest grouped rule file in `rules/`.
- Keep upstream markdownlint defaults separate from repo-local policy overlays.
- Use [AGENTS.md](./AGENTS.md) for cross-family routes or maintainer-level context.

## In scope

- markdownlint and `markdownlint-cli2` triage by MD rule IDs.
- Content vs config vs suppression vs custom-rule decisions.
- Prettier/tooling coexistence for Markdown linting.
- Link and image quality checks that overlap with accessibility review.
- Upstream-default vs repo-overlay comparison using the bridge layer.

## Out of scope

- Generic writing coaching not tied to markdownlint behavior.
- Domain-specific technical guidance owned by another skill package.
- Repository publishing workflows that do not affect Markdown lint decisions.

## Route by problem type

| Problem type | Start here | Add when needed |
| --- | --- | --- |
| Config, aliases/tags, install, validation, MD013/MD044 | [rules/foundation-configuration.md](./rules/foundation-configuration.md) | [references/config-and-validation-map.md](./references/config-and-validation-map.md) |
| Headings, title/front matter, MD001/MD022/MD024/MD025/MD041/MD043 | [rules/headings-front-matter-structure.md](./rules/headings-front-matter-structure.md) | [references/instruction-bridge.md](./references/instruction-bridge.md) |
| Lists, spacing, tabs, trailing whitespace, MD004/MD007/MD009/MD010/MD029/MD030/MD032 | [rules/lists-whitespace-block-spacing.md](./rules/lists-whitespace-block-spacing.md) | [references/prettier-and-tooling-notes.md](./references/prettier-and-tooling-notes.md) |
| Code fences, inline HTML, emphasis, MD014/MD031/MD033/MD036/MD040/MD046/MD048/MD049/MD050 | [rules/code-html-emphasis.md](./rules/code-html-emphasis.md) | [references/rule-family-map.md](./references/rule-family-map.md) |
| Links, images, fragments, MD011/MD034/MD045/MD051-MD054/MD059 | [rules/links-images-accessibility.md](./rules/links-images-accessibility.md) | [references/accessibility-review-map.md](./references/accessibility-review-map.md) |
| Tables/layout edges, MD035/MD055/MD056/MD058/MD060 | [rules/tables-layout-edges.md](./rules/tables-layout-edges.md) | [references/default-rule-profile.md](./references/default-rule-profile.md) |
| Custom rules, suppressions, formatter conflicts | [rules/custom-rules-suppressions-toolchain.md](./rules/custom-rules-suppressions-toolchain.md) | [references/config-and-validation-map.md](./references/config-and-validation-map.md) |

## High-value references

- [references/rule-family-map.md](./references/rule-family-map.md)
- [references/config-and-validation-map.md](./references/config-and-validation-map.md)
- [references/instruction-bridge.md](./references/instruction-bridge.md)
- [references/accessibility-review-map.md](./references/accessibility-review-map.md)
- [references/install-and-validation.md](./references/install-and-validation.md)

## Package conventions

- Grouped rule files follow [rules/_sections.md](./rules/_sections.md).
- Keep durable detail in `rules/` and `references/`; keep this file as a router.
- Keep package inventory aligned across [metadata.json](./metadata.json),
  [assets/taxonomy.json](./assets/taxonomy.json), and
  [assets/section-order.json](./assets/section-order.json).
