# Documentation for LLM Consumption

## Purpose
Author and maintain Markdown documentation optimized for LLM retrieval and coding-assistant consumption: progressive disclosure layering, stable anchors, llms.txt index files, YAML frontmatter metadata, and chunk-size discipline so agents load the smallest sufficient context first.

## Use when
- Writing or restructuring docs that coding agents will read (AGENTS.md entries, skill pages, runbooks, API references, ADRs).
- Adding an llms.txt index at a documentation root following the llmstxt.org convention.
- Auditing existing Markdown for agent-hostile patterns: 4000-line pages, unstable headings, missing frontmatter, duplicated truth across copies.
- Defining heading, anchor, cross-link, and frontmatter conventions for a documentation corpus.

## Do not use when
- Building, theming, or deploying the published docs site itself (use `documentation-publishing`).
- Writing one-off chat answers with no durable documentation destination.
- Designing visual page layout, marketing copy, or brand voice guidelines.

## Required context
- Documentation corpus root and target audience (human developers, coding agents, or both).
- Canonical source map: which file is the single source of truth per topic.
- Token budget per page-load target (default: entry page under 1500 tokens, full topic path under 6000 tokens).
- Existing index and nav files (llms.txt, mkdocs.yml nav, astro.config.mjs) if present.

## Procedure
1. **Inventory the corpus**: list Markdown files under the docs root with word counts and heading depth (e.g. `wc -w docs/**/*.md`); flag pages over 2500 words or deeper than 4 heading levels for splitting.
2. **Establish frontmatter**: every page gets a title, a description under 160 characters, a last-reviewed date in ISO format such as 2026-09-10, and an audience tag of human, agent, or both; enforce presence in CI with markdownlint plus a frontmatter check script.
3. **Layer progressive disclosure**: the entry page states the outcome and links onward in under 1500 tokens; details move to linked sub-pages; each sub-page opens with a 3-line summary so an agent can stop early with enough understanding.
4. **Stabilize anchors**: keep heading wording that rarely changes, forbid duplicate headings within a page, and link with full relative paths plus fragments such as `../runtime/control-plane.md#control-plane-loop`.
5. **Write the llms.txt index**: a root file listing corpus sections with one-line descriptions and root-relative links; keep it under 300 lines and regenerate it whenever navigation changes.
6. **Right-size chunks**: keep retrievable sections between 150 and 600 tokens; convert tables wider than 5 columns into definition lists; put diffs, logs, and traces in fenced code blocks with language tags.
7. **Verify with lint and link gates**: run markdownlint with zero-error tolerance and lychee link checking over touched pages, then run `scripts/verify.sh`; fix broken anchors before merging.

## Decision rules
- **Single source of truth**: each fact lives in exactly one canonical page; all other pages link to it instead of restating it.
- **Frontmatter mandatory**: no new page merges without title, description, reviewed date, and audience tag.
- **Link, do not duplicate**: when two pages need the same paragraph, extract it to a shared page and link from both.
- **Stable headings**: never rename a heading that has inbound links without leaving a redirect note at the old anchor location for one release cycle.
- **Token ceiling enforced**: entry pages stay under 1500 tokens; any page over 6000 tokens is split before merge.

## Evidence required
- markdownlint run with zero errors on all touched pages.
- Link-check report (lychee or equivalent) with zero broken links or anchors.
- Passing execution log from `scripts/verify.sh`.
- Token counts before and after for every restructured page.

## Output contract
- Restructured Markdown pages with frontmatter, layered summaries, and stable anchors.
- llms.txt index updated or created at the corpus root.
- Lint and link-check logs proving zero defects.

## Stop conditions
- Corpus pages meet frontmatter, token-ceiling, and anchor-stability rules with evidence.
- llms.txt index regenerated and verified against current navigation.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the documentation owner if two claimed canonical sources contradict each other and no ADR resolves the conflict.
- Escalate to a human if link repair requires deleting public URLs that have external inbound links.
