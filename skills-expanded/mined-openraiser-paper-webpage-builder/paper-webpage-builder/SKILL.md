---
name: paper-webpage-builder
description: Build a polished single-page academic project webpage from a paper directory or paper source, including content extraction, figure selection/conversion, module planning, visual design, tables, assets, and validation. Use when asked to create or update webpages for papers, benchmarks, arXiv-style projects, OpenRaiser project pages, or paths containing paper.tex/PDF/images/assets.
---

# Paper Webpage Builder

Use this skill to turn a paper project folder into a web-ready project page. It is optimized for repos with `paper.tex`, `*.pdf`, `images/`, and `assets/`, but also works from a PDF plus image assets.

## Core Rule

Do not mechanically clone an existing webpage. Use prior pages only as references for interaction patterns and content completeness. The final design must follow the target paper's topic, figures, color palette, density, and audience.

Two failure modes to actively avoid:

- Do not reuse a background system from another paper page by default. Grids, coordinate paper, dark sections, gradients, or canvas textures are allowed only when they are supported by the target paper's own figures, domain, or visual language.
- Do not default to a split hero with oversized title text on the left and a paper figure/card on the right. This generic composition is allowed only when the paper has a product-like teaser image that clearly belongs in the first viewport and the whole composition is justified by the paper's evidence hierarchy.
- Do not summarize away central evidence. If the paper's main claim depends on a main experiment table, benchmark comparison table, dataset statistics table, or ablation table, the webpage must include that table in full or provide a clearly equivalent full presentation.
- Do not show partial or horizontally scrolling tables. Table rows, headers, and cell text must be statically visible; they must not be clipped by smaller white/card containers, fixed-height panels, masks, fades, `overflow:hidden`, or `overflow-x:auto/scroll`. Wide tables should use grouped columns, multiple full sub-tables, readable density reduction, or a larger responsive container while preserving values.

## Workflow

1. Inspect inputs before editing.
   - Locate paper source, PDF, figures, logos, existing `template.html`, and target `index.html`.
   - Run `scripts/scan_paper.py <paper.tex>` when a TeX source exists. Multi-file projects are followed via `\input`/`\include` automatically. This gives the skeleton (title, authors, captions, table/figure metadata, links) — not the argument.
   - Run `scripts/extract_sections.py <paper.tex>` to read the body prose of every section. The skeleton is not enough: designing from `scan_paper.py` alone is the main cause of shallow pages with abstract-paraphrased copy and invented headings. Read this output in full (use `--full` for truncated sections).
   - Run `scripts/scan_pdf.py <paper.pdf>` when only a PDF is available; it produces the same shape of inventory (title, authors, abstract, sections, figure/table captions, links).
   - Run `scripts/extract_tables.py <paper.tex>` to dump every table (caption, label, header rows, data rows) as JSON. Use this to seed the table ledger instead of eyeballing the .tex.
   - Build a table ledger before designing: caption, label, section, whether it is main evidence, and whether it must appear fully on the page.
   - Identify important tables as well as figures; main results, benchmark comparisons, dataset statistics, and ablations usually belong on the page.

2. Read deeply and build a Paper Brief.
   - This step is mandatory and comes before any visual or copy decision. Follow `references/paper_reading.md`.
   - From the section prose, write an explicit eight-part Brief in working notes: thesis (as a claim), problem, core idea/name, how it works (2-4 stages), evidence map (what each central table/figure proves), headline numbers (each with its comparison), honest limits, and audience/tone.
   - Do not invent any part. If a part cannot be filled from the extracted text, read more rather than guessing.
   - All later page copy (hero subtitle, TL;DR, section headings, result framing) must derive from this Brief, not from the abstract directly. Section headings must be claims, not academic labels; never use "the paper argues/proposes/presents" phrasing; never show a number without its comparison or a central table without a one-line "why this matters" framing.

3. Build a content map.
   - Extract title, authors, affiliations, abstract claim, contributions, links, dataset stats, method description, main results, case studies, citation.
   - Map every central table to a page module. If a central table is too large, plan grouped columns, multiple full sub-tables, or a larger static table module rather than dropping rows or adding horizontal scroll.
   - Decide modules before writing. Typical modules: Hero, Motivation, Method, Dataset/Benchmark, Results, Case Study, Citation.
   - Read `references/module_patterns.md` when choosing sections or table placement.

4. Prepare assets.
   - Prefer paper-provided figures over generic visuals.
   - Convert figures to web assets with `scripts/convert_figures.py <source_images_dir> <target_figures_dir>` (the legacy `convert_figures.sh` is now a shim around it). The script handles multi-page PDFs, `.eps`, `.svg` passthrough, raster passthrough, and writes a `figures.manifest.json` that records source→output mapping plus an empty `alt` field per asset for the LLM to fill.
   - Copy logos and paper PDF into the webpage output folder when useful.
   - Filenames coming out of the manifest are already slug+hash safe; do not rename them again.
   - Keep project branding assets separate:
     - `web-logo.*` / favicon is a project icon, not the teaser figure and not an institution logo.
     - teaser/overview figures belong in the hero or method/results modules.
     - institution or partner logos belong in the footer logo strip only.
   - If the paper has no suitable project icon, create or request a simple flat project mark before finalizing the page. It must remain readable at favicon size and should not reuse a dense paper figure.

5. Generate the citation block.
   - Run `scripts/extract_citation.py <paper.tex> [--pdf paper.pdf]` and embed the produced BibTeX as the page's citation default.
   - Preserve the leading `% NOTE:` comments verbatim; they document fields that were inferred or guessed (year, venue, authors).
   - When notes indicate missing venue/year, add a SINGLE small inline hint (e.g., a muted footnote or tooltip "Citation fields pending verification") rather than a full warning banner. Never add a red/yellow `.warn` div or multi-line warning block for draft citations — it reads as broken, not cautious.
   - Use `@article` with a best-guess year (e.g., `2025`) rather than `@unpublished` when the paper has a clear title and authors but no venue yet. The `@unpublished` type confuses citation tools and looks unprofessional on the page.
   - Strip `% NOTE:` comment lines from the BibTeX shown on the page; they are for the builder's internal tracking, not for end users to see.
   - The Citation module must only contain the section title, BibTeX/code block, copy affordance when useful, and a short citation-status/license note if the source verifies it. It must not become a project-resources card.
   - Do not duplicate header resource buttons in Citation. If Code/Dataset/Project links already appear in the hero/header, do not repeat them in Citation.
   - Do not invent a license statement. Only show a license sentence when a LICENSE file, paper source, or user-provided link verifies it.
   - Institution, lab, and partner logos must be rendered below the page content in a compact footer/partners strip, not inside the Citation module.

6. Design the page around the paper.
   - Derive colors, background, spacing, figure framing, and motifs from the paper's key figures and domain.
   - First list the paper-specific visual cues, then choose the background. A plain surface, soft paper tone, lab-notebook grid, dark canvas, figure-derived gradient, or no visible texture are all valid; none is the default.
   - Choose a paper-specific hero strategy before writing CSS. The hero is a narrative decision, not a default two-column layout. Valid strategies include:
     - thesis-first hero: concise title/claim with evidence modules beginning immediately below the fold;
     - figure-led hero: one full-width teaser/overview figure with compact title/caption treatment;
     - benchmark-dashboard hero: compact metrics and primary result evidence, with paper figures deferred to the benchmark/results sections;
     - system-workflow hero: a short title block followed by a full-width pipeline/workflow band;
     - brand-led hero: project mark or mascot as identity, with technical figures moved to method/results.
   - Do not place title, authors, resource buttons, metrics, and a key paper figure into one hero unless the first viewport remains balanced and the figure is truly the paper's lead evidence. Move secondary evidence into Motivation, Method, Benchmark, or Results.
   - Plan figure layout from the actual converted image ratios in `figures.manifest.json`. Wide pipeline/heatmap/table figures, tall case figures, and compact charts should not be forced into one equal-height grid.
   - Avoid fixed-height or fixed-aspect figure cards with `object-fit: contain` for paper figures. Use natural image height (`width: 100%; height: auto`) by default; reserve fixed boxes for icons, logos, thumbnails, or zoom modals.
   - Put figures side-by-side only when their aspect ratios are compatible, or when one side is balanced by text/table content instead of another image. If max/min ratio is above about 1.25, stack them or use a main-figure-plus-notes composition.
   - Do not use fixed-height figure boxes to fake alignment for primary paper figures. If two figures have mismatched heights, change the composition instead of stretching/cropping/containing the images.
   - Keep background transitions coherent across sections. Avoid abrupt dark-to-light jumps unless the entire page system intentionally supports that contrast.
   - Read `references/design_principles.md` when deciding visual style or revising design feedback. The "Measurable Criteria" section there names the thresholds the design-drift check enforces.

7. Implement the webpage.
   - Start from `assets/single-page-template.html`. It includes semantic landmarks (`header`/`nav`/`main`/`footer`), a skip-link, a `prefers-reduced-motion` fallback, a CJK-friendly font stack, and the `{{LANG}} {{TITLE}} {{DESCRIPTION}} {{CANONICAL_URL}} {{OG_IMAGE}} {{JSONLD}}` placeholders. Fill them with `scripts/render_template.py` (or `scripts/inject_metadata.py --inplace` if you only need to refresh the head block of an existing page).
   - Set `<html lang="...">` to the paper's language (BCP-47: `en`, `zh-CN`, `ja`, `ko`, etc.); the scan scripts do not auto-detect this. For CJK papers keep the bundled font stack and add `lang` attributes around any embedded English titles so browsers pick the right glyphs.
   - Generate the head metadata once via `scripts/inject_metadata.py --title ... --description ... --canonical ... --og-image ... --author ...` and pipe its `render-values` JSON into `render_template.py`. Use `--arxiv` / `--doi` when known so the ScholarlyArticle JSON-LD includes a stable identifier.
   - Produce a self-contained single-page `index.html` unless the repo already has a framework.
   - Include responsive navigation, resource buttons, figure zoom/modal behavior, and readable tables.
   - For primary paper figures, do not use equal-ratio card grids unless all figures in that grid share a close aspect ratio. If a layout needs equal rhythm, align captions/text, not the image boxes.
   - Use compact/narrow table treatments for two- or three-column tables. Do not stretch low-density tables across the full page just because wide result tables need more space, and do not leave narrow tables isolated with a large blank area to the right; pair them with related notes, metrics, or figures.
   - Size tables by content, not by a global default. Before assigning `compact-table`, inspect column count, header length, and cell density:
     - 2-3 low-density columns: compact/narrow wrapper is appropriate.
     - 4-6 explanatory columns with long headers: use full module width and explicit `colgroup` widths when needed.
     - many-column result tables: use full-width responsive/static table treatment with grouped columns or row-card mobile fallback.
   - Avoid header wrapping for short semantic headers such as `Active stages`, `Family`, `Tier`, `Rank`, `Metric`, and `Scenario`. Give those columns enough width and use `white-space: nowrap` when values are short.
   - Center short categorical/ordinal columns such as `Family`, `Active stages`, `Tier`, `Rank`, `Best config.`, and compact stage/objective codes. Keep long mechanism/explanation columns left-aligned.
   - Include full central tables as static readable content, with sticky headers when useful, grouped rows/columns when needed, and highlights for the proposed method or best values. Tag each rendered `<table>` (or its wrapping `<section>`) with `data-tex-label="<label>"` so step 8 can reconcile it.
   - Keep each table visually contained by its white/card/table wrapper. If a table is wider than the module, redesign the module: allocate more width, split/group columns into complete sub-tables, or reduce density while staying readable. Do not use `overflow-x:auto/scroll`, `overflow:hidden`, fixed heights, clipped cards, text fades, or partial table previews.
   - Use charts only when they clarify a key result beyond the paper figures.
   - Avoid hidden dependency on the source paper directory; generated page should work from the webpage folder.
   - CSS custom properties must use semantic names (`--primary`, `--accent`, `--surface`) not hue-literal names (`--green`, `--blue`). See `references/design_principles.md` "CSS Variable Naming" section.
   - After defining CSS variables, ensure ALL theme-significant colors (table headers, card backgrounds, tag pills, group rows, borders, footer accents) reference those variables. Do a final pass to replace orphan hardcoded hex values with the appropriate `var(--...)` reference.
   - Footer logo strips must use uniform `height: 48px; object-fit: contain` for consistent visual weight across logos of different native sizes.
   - Grids with >4 columns must include a `@media (max-width: 960px)` breakpoint that reduces to max 3 columns. Verify no grid item is narrower than 180px at any viewport 360-1440px.
   - Paired primary paper figures should use natural image height. Use `align-items: start` or baseline-aligned captions when aspect ratios are compatible; if aspect ratios differ substantially, stack the figures or redesign the row. Reserve `object-fit: contain` for logos, icons, thumbnails, and footer marks, not for primary paper figures.

8. Validate.
   - Run `scripts/check_webpage_links.py <index.html> --full` for the broader lint: missing `src`/`href`/`data-figure`, CSS `url(...)`, `srcset`, `<source>`/`<video poster>`/`preload`, `og:image`/`twitter:image`, broken `#fragment` targets, duplicate ids, missing `alt`/`title` on `<img>`/`<iframe>`, and path-traversal hrefs that resolve outside the page directory. Use `--json` when you need a machine-readable report.
   - Reconcile the table ledger against the page with `scripts/reconcile_tables.py --ledger <ledger.json> --html <index.html>`. The ledger is the JSON produced by `extract_tables.py` in step 1; tag any HTML `<table>` (or its wrapping `<section>`) with `data-tex-label="<label>"` to enable strict matching. The script flags missing, abbreviated, and column-stripped tables; treat any "MISSING(central)" or "abbrev" line as a blocker.
   - Run `scripts/check_table_fit.py <index.html> --json` to verify rendered tables are not clipped, do not spill outside their visual containers, and do not require horizontal scrolling. Treat any error as a blocker; this means the first generated page design is wrong and must be repaired before delivery.
   - Run `scripts/check_html_sanity.py <index.html>` for HTML5-aware validation. It prefers `html5validator`, then `tidy`, then `html5lib`; without those installed it falls back to a stdlib structural check and says so explicitly. Do NOT use `xmllint --html` — it false-flags HTML5 elements like `<main>`, `<dialog>`, and `<picture>`.
   - Recheck the design with `scripts/check_design_drift.py --html <index.html> --manifest <figures.manifest.json> [--reports-dir reports]`. It computes palette overlap between the figure colors and the page's chosen colors, flags unsupported grid/dot/notebook backgrounds, warns about fixed figure containers that can create blank space, warns about mixed-ratio figures placed in the same row, warns about overstretched low-column tables, flags CSS variable names that contradict their hue, flags hardcoded hex colors not backed by a CSS variable, flags grids missing responsive breakpoints, and warns when class-token overlap with a sibling `reports/<other>/index.html` exceeds 70% (likely template clone). Treat any warning as a design review item, not silent acceptance.
   - Verify external links: run `scripts/check_webpage_links.py <index.html> --full --check-external` to HEAD-request all external URLs (with 5s timeout, max 20 requests). Any URL not provided by the user or extracted from the paper should be tagged with `data-unverified="true"` in the HTML so this check surfaces them clearly. Treat 4xx/5xx responses as blockers; treat timeouts and `data-unverified` links as warnings requiring user confirmation.
   - Capture responsive screenshots with `scripts/capture_screenshots.py <index.html> --out-dir reports/<slug>/screenshots`. The script tries Playwright, then Pyppeteer, then headless Chromium; if none are installed it skips cleanly with `meta.json.status == "skipped"` so the rest of validation can continue.
   - After capturing screenshots, perform a visual regression check: inspect the desktop screenshot for (a) color consistency across sections, (b) figure alignment and blank-space issues, (c) grid density and readability at each viewport, (d) table readability and overflow. Report findings even if HTML validation passed — visual issues are invisible to linters.
   - Perform module-level visual QA, not only full-page screenshot review. Capture or crop at least Hero, Framework/Method, Benchmark/Results, central Tables, Citation, and Footer/partners. For each module, explicitly check:
     - section composition matches the paper evidence hierarchy;
     - no large accidental blank areas;
     - paired figures are semantically and visually balanced;
     - table headers are readable and not awkwardly wrapped;
     - short categorical table columns are centered where appropriate;
     - Citation is not duplicating hero resources;
     - institution logos are in the footer/partners area and have balanced visual weight.
   - Treat design-drift warnings as action items. If a warning is intentionally acceptable (for example `object-fit: contain` on footer logos), record why it is acceptable rather than silently ignoring it.
   - Report any validation you could not run, including the `meta.json` skip reason when screenshots were not captured.

## Publishing Workflow

When asked to upload a generated webpage to GitHub Pages or a project repo:

- Confirm the exact target repository and branch mapping in the working notes before pushing.
- Default to `gh-pages` for the webpage branch unless the user names another branch.
- Do not push webpage assets to `main` unless explicitly requested.
- If the user wants an empty `main`, create a minimal README-only `main` branch and keep webpage content isolated on the page branch.
- Before every push, run `git ls-remote --heads <repo>` and report whether the target branches already exist.
- Never force-push or delete remote branches unless the user explicitly asks for that exact operation.
- After pushing, verify with `git ls-remote --heads <repo>` and report the branch names and commit hashes.

9. Use the agent workbench when the user wants an interactive UI, ongoing progress, preview, or region-level repair.
   - Start the local workbench with `python3 scripts/webpage_workbench.py --port 8765`.
   - The workbench is a chat interface over the real skill workflow. The user should be able to say "build a webpage for this paper" and the backend agent should perform this workflow, not generate a generic scaffold.
   - The backend runs an agent command in the background (default: local `codex exec` when available; override with `--agent-command` for Claude or another runner), tracks progress, logs output, and mounts the generated `index.html` in the preview pane.
   - Use the iframe overlay to mark a visual defect. The workbench saves `annotation.json`, `context.html`, and `repair_prompt.md` under `<paper-project>/.paper-webpage-builder/annotations/<timestamp>/`, then includes that context in the next chat turn when requested.
   - Treat saved DOM selectors, bounding boxes, computed styles, and user instruction as the repair scope. Make the smallest local HTML/CSS/JS change that resolves the selected defect, then rerun the checks in step 8.
   - Read `references/visual_workbench.md` for the exact closed-loop contract.

## Output Expectations

In the final response, include:
- The generated/updated `index.html` path.
- The major modules included.
- The important figures/tables included.
- The page metadata you set (`lang`, canonical URL, OG image; DOI/arXiv if known) — these populate the `metadata` block of the output schema.
- Suggested project keywords or tags for discovery (required, at least one).
- The quality checks performed for links, HTML sanity, responsive layout, asset independence, visual consistency, table reconciliation, and design drift (required; use `not_run` with a reason rather than omitting an entry).
- Validation performed and remaining risks.

The output is validated against `schemas/output.schema.json`; `keywords` and `quality_checks` are required.

## Reference Files

- `references/paper_reading.md`: deep-reading protocol and the Paper Brief that all page copy must derive from. Read this before designing.
- `references/module_patterns.md`: section patterns, paper-content extraction targets, and table handling.
- `references/design_principles.md`: visual design rules for paper webpages.
- `references/visual_workbench.md`: local UI loop for previewing generated pages, selecting visual defects, and handing region context to an agent.

## Scripts

- `scripts/scan_paper.py`: summarize TeX title/authors/abstract/sections/figures/tables/links; follows `\input`/`\include`. Emits an explicit warning when the file is not UTF-8 (with the fallback encoding it used). Produces the skeleton only — not section body prose.
- `scripts/extract_sections.py`: print the cleaned body prose of every section (drops float/equation noise, keeps citations as `[cite]` and contribution lists). Read this to understand the paper's argument before designing; pair it with `references/paper_reading.md`.
- `scripts/scan_pdf.py`: PDF-only inventory in the same shape as `scan_paper.py` (used for `kind: pdf_with_assets`).
- `scripts/extract_tables.py`: dump every LaTeX table (caption/label/header/data rows) as JSON for the table ledger.
- `scripts/extract_citation.py`: produce a best-effort BibTeX draft with explicit notes for unverified fields.
- `scripts/convert_figures.py` (and `convert_figures.sh` shim): convert paper figures to web assets and emit `figures.manifest.json`. Handles multi-page PDFs, `.eps`, `.svg`, raster passthrough, and CJK filenames.
- `scripts/render_template.py`: substitute `{{NAME}}` placeholders in `assets/single-page-template.html`; `--inplace` refreshes only the head metadata of an existing page.
- `scripts/inject_metadata.py`: build SEO + Schema.org `ScholarlyArticle` JSON-LD; outputs `render_template.py` values, a copy-paste meta block, or runs the in-place head refresh in one shot.
- `scripts/check_webpage_links.py`: link/lint check for local assets; `--full` adds CSS `url(...)`, `srcset`, `<source>`/`poster`, `preload`, `og:image`, `#fragment` targets, duplicate ids, missing `alt`/`title`, and path-traversal warnings. `--check-external` HEAD-requests external URLs (max 20, 5s timeout) and flags 4xx/5xx as errors, timeouts as warnings.
- `scripts/check_design_drift.py`: palette overlap between figures and page, plus figure-container, grid/dark/clone warnings, CSS variable name vs hue mismatch, hardcoded color orphans, grid responsive breakpoint checks, and paired-figure alignment checks against sibling `reports/`.
- `scripts/reconcile_tables.py`: cross-check the LaTeX table ledger against `<table>`/`data-tex-label` in the rendered HTML.
- `scripts/check_table_fit.py`: browser-level table fit check; flags clipped rows/cells, tables spilling outside white/card visual containers, and tables that require horizontal scrolling.
- `scripts/check_html_sanity.py`: HTML5-aware sanity check (html5validator → tidy → html5lib → stdlib fallback).
- `scripts/capture_screenshots.py`: desktop+mobile screenshots and `meta.json` (Playwright → Pyppeteer → headless Chromium; skips cleanly if none installed).
- `scripts/webpage_workbench.py`: dependency-light local chat UI/API for agent-backed paper webpage generation, progress/log streaming, preview mounting, iframe region marking, annotation capture, and local visual repair turns.
