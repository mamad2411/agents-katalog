---
name: compile-central-alignment
description: Generate a central alignment/index.html table of contents for all alignment pages in the current repo
type: ops
version: v0.2
---

# Compile Central Alignment

Invoke as `$compile-central-alignment`.

Generate a browsable `alignment/index.html` linking to every alignment page in the current repository. Works in any repo with an `alignment/` directory.

## Process

1. Locate `alignment/` at the project root; stop if absent.
2. Scan `alignment/*.html` (exclude `index.html`), extract per-file: `<title>`, first `<h1>`, first `<p class="meta">`, `data-alignment-category` from `<html>` element, modification date.
3. Group and sort:
   - Assign category per page: `data-alignment-category` attribute first; else match filename against prefix lists:
     - `research`: `devtool-positioning`, `devtool-adoption`, `devtool-monetization`, `devtool-user-map`, `devtool-workflow`, `devtool-dx-journey`, `devtool-integration-map`, `deep-research`, `repo-glossary`
     - `product-design`: `idea-scope-brief`, `fork-idea-branch`, `animation-design-planner`, `skills-showcase`, `skills-inventory`
     - `utility`: `investigate`, `session-triage`, `prompt-history-backfill`
     - `qa-meta`: `expert-review`, `benchmark`, `targeted-skill-builder`, `devtool-docs-audit`
     - `ops-analysis`: `analyze-sessions`, `canonical-workflow`, `run-batch`
     - Default: `research`
   - Group by category in fixed order: research → product-design → utility → qa-meta → ops-analysis
   - Within each category, sort by modification date descending
4. Generate `alignment/index.html` — self-contained HTML with:
   - Visual style matching existing alignment pages (same CSS variables, fonts, layout)
   - Category sections: each non-empty category gets an `<h2>` with display name and count (e.g., "Research (7)"), followed by its card grid
   - Display names: Research, Product Design & Spec, Utility & Maintenance, QA & Meta-Skill Improvement, Ops & Session Analysis
   - Card grid with linked titles, descriptions, dates
   - Text filter input searching across all categories, hiding empty category headings
   - Total page count and generation timestamp
   - All relative links, no external dependencies
   - Skip categories with zero pages
5. Verify `alignment/index.html` was written and still works as a direct `file://` page.
6. Open or focus the generated index with:
   - `node scripts/open-html-page.mjs alignment/index.html --browser auto`
7. Report the opener script status exactly as one of `focused`, `opened`, `fallback-opened`, `blocked`, or `failed`.
   - `blocked` means the browser-open attempt was unavailable or blocked; it does not fail this skill when `alignment/index.html` was generated and verified.

## Constraints

- Do not modify existing alignment pages — only create or overwrite `alignment/index.html`.
- Do not commit or push `alignment/index.html` by default — it is a local convenience artifact, regenerated fresh each time.
- Empty-state page if no `.html` files found (besides `index.html`).
- Must work as `file://` URL — no server required.
- Do not open individual alignment pages from this skill; individual alignment-producing skills handle their own review pages, and this skill opens or focuses only the central index.

## Default Shipping Contract

- **No commit/push.** Local convenience file, regenerated on demand. Do not commit `alignment/index.html` unless the user explicitly asks.
- **Default next-step routing:** After generating the index, suggest contextual next steps based on what was found:
  - If any pages have old modification dates or the scan revealed outdated content: `Recommended next command: $upgrade-alignment-pages`
  - If the index is freshly built with all pages current: confirm completion with no further routing
  - Do not default to `$skills` as a generic fallback
