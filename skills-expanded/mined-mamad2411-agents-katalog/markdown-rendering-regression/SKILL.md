---
name: markdown-rendering-regression
description: Use when validating built HTML from Markdown or MDX content, especially Astro docs/wiki pages, for raw Markdown leaks, frontmatter leakage, placeholder copy, local filesystem paths, internal build labels, emoji UI icons, and artifact wording regressions.
cluster: quality-eval
version: 1.0.0
origin: folded from agent skills library (quality-eval overlap)
---

# Markdown Rendering Regression

## Purpose

Catch public documentation regressions that ordinary builds miss. Build success does not prove Markdown rendered correctly or that generated copy is safe for readers.

## What To Check

- Raw Markdown syntax visible in rendered pages: `**bold**`, `](link)`, fenced code markers, frontmatter delimiters.
- Placeholder copy: `_No source outputs were available_`, `_No structured content available_`, TODO/filler markers.
- Internal process language: wave labels, current run/build labels, raw output language, local machine paths.
- Artifact wording: use `Source artifact`, `Open artifact`, or `Download`; do not expose `Raw artifact path`.
- UI icon policy: verify rendered public HTML does not expose emoji icons where the design system bans them.
- Frontmatter descriptions: sidebar cards and document rails often expose frontmatter directly, so scan full visible text, not just Markdown bodies.

## Default Command

Use the helper script when available:

```bash
node ~/.agents/skills/markdown-rendering-regression/scripts/verify-public-html.mjs --dist dist
```

For repo-local copies:

```bash
node scripts/verify-public-html.mjs
```

## Implementation Notes

- Run after the static build has produced `dist/`.
- Strip `<script>` and `<style>` before visible-text checks.
- Scan all generated HTML, not only known docs pages.
- Report exact file and banned label for every failure.
- Keep the ban list configurable by editing the script constants or passing a JSON config in future repo-specific variants.

## Acceptance Examples

- A rendered page containing `_No source outputs were available_` must fail.
- A rendered page containing visible `**bold**` must fail.
- A rendered page containing `/Volumes/madara` or another local absolute path must fail.
- A rendered page containing `Raw artifact path` must fail.
