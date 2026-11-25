---
name: report-website
description: Convert one Markdown report or a collection of documented Markdown outputs into clean JSX routes for a polished, readable frontend website
type: execution
version: v0.2
required_conventions: [alignment-page]
argument-hint: "<report.md|directory|--all-output-docs> [base route]"
---

# Report Website

Invoke as `$report-website`.

Use this skill when the user wants one report, a directory of reports, or all documented Markdown outputs turned into a frontend website whose content is represented as clean JSX components instead of a raw Markdown render. The goal is a readable publication surface: strong hierarchy, responsive layout, accessible content, source-faithful report sections, and stable routes for each document.

## Modes

- **Single report**: `$report-website path/to/report.md [route]` converts one Markdown report into one JSX-backed route.
- **Directory**: `$report-website path/to/reports/ [base route]` converts Markdown files under a directory into an index route plus one route per document.
- **All documented outputs**: `$report-website --all-output-docs [base route]` discovers documented output Markdown files across the repo and converts them into a route-based report collection.

## Process

1. **Resolve source and target**
   - Read the requested Markdown report path, directory, or `--all-output-docs` mode. If no path was provided, locate likely report files under `reports/`, `docs/`, `research/`, `benchmark/`, or the project root and ask only when there is no clear source.
   - For `--all-output-docs`, discover tracked Markdown files that are documented outputs rather than operational instructions. Prefer `reports/`, `docs/reports/`, `research/**/reports/`, `benchmark/test-*.md`, `benchmark/review-*.md`, `benchmark/triage-*.md`, `specs/*.md`, and project-specific output folders. Exclude `README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `PACK.md`, changelog/history/task planning files, dependency docs, and generated assets unless the user explicitly includes them.
   - For directory mode, include Markdown descendants by default, but apply the same exclusions for instruction/config docs unless the directory itself is clearly a report archive.
   - Identify the frontend stack from existing files before creating anything: framework, route conventions, component directories, styling system, icon library, image handling, deployment config, and test commands.
   - Decide the frontend target before writing code:
     - Integrate into an existing frontend app by default when exactly one obvious public/docs/showcase app exists, when an app already owns report-like content, or when an existing app has clear routing, styling, and deploy conventions for documentation pages.
     - In a monorepo, prefer likely documentation/public surfaces by name and evidence: `apps/docs`, `apps/showcase`, `apps/web`, `apps/site`, a separate public report/showcase repository, or routes/components that already render docs, reports, changelogs, or benchmark evidence.
     - Create a separate frontend subdirectory or standalone site only when no frontend app exists, when the user explicitly asks for a standalone site, when the report site needs a separate brand/domain/audience/access policy, or when existing apps cannot cleanly support static report routes.
     - Ask one narrow question before choosing only when multiple plausible frontend apps exist with no clear owner, integrating would change public navigation or deployment in a non-obvious way, the desired base route conflicts with existing routes, or the audience/access level cannot be inferred.
     - When asking, name the concrete candidates and default recommendation, for example: `I found apps/docs and apps/marketing. Should report routes live under apps/docs at /reports, or should I create a standalone report site?`
   - Choose a base route for multi-document mode, such as `/reports`, `/research`, `/benchmarks`, or the user-provided route.
   - Check existing routes before finalizing the base route. If the requested route conflicts, either nest under a non-conflicting route or ask the user to choose between the concrete options.
   - Inspect `AGENTS.md`, `CLAUDE.md`, `README.md`, `DESIGN.md`, package scripts, and relevant neighboring pages before editing.

2. **Build the route plan**
   - For single-report mode, create or update one route for the report.
   - For multi-document mode, create:
     - An index route at the base route with searchable or scannable links to every generated document route.
     - One stable route per Markdown file, split by document rather than putting every report on one page.
   - Derive slugs from repo-relative file paths, not just titles, so routes are stable and collisions are rare. Example: `benchmark/test-roadmap-2026-05-17.md` can become `/reports/benchmark/test-roadmap-2026-05-17`.
   - Preserve directory hierarchy when it helps users browse the collection. Flatten only when the target app's route conventions require it.
   - Detect duplicate slugs before writing. Resolve collisions deterministically by adding the nearest parent directory or a short content hash.
   - Generate route metadata for each document: title, source path, last known date if present, category, summary excerpt, and table-of-contents anchors.

3. **Parse reports into structure**
   - Convert each Markdown file into an explicit content model before writing JSX: title, subtitle, metadata, summary, sections, subsections, tables, lists, callouts, citations, figures, links, code blocks, footnotes, and appendices.
   - Preserve source meaning and ordering. Do not summarize, omit, or rewrite findings unless the user explicitly asks for editorial compression.
   - Normalize links, anchors, heading IDs, dates, numbers, and table columns. Keep citations and source references visible and clickable when present.
   - Convert links between included Markdown files into links to their generated routes when possible.
   - Flag unsupported Markdown features or missing assets early, then implement the closest source-faithful rendering.

4. **Build clean JSX**
   - Represent each report with typed data, small presentational components, or a straightforward JSX section tree, following the existing framework's conventions.
   - Keep JSX readable: semantic elements, named section components, stable keys, and clear component boundaries. Avoid a single monolithic blob when the report has meaningful structure.
   - Reuse the same report layout and content components across routes. Do not duplicate large component definitions inside every generated page.
   - For route-based frameworks, use native dynamic/static route generation where appropriate, such as `generateStaticParams`, file-based route segments, or route data loaders.
   - Use framework-native routing, metadata, bundling, and asset APIs. Do not add dependencies unless the existing stack cannot reasonably handle the conversion.
   - Escape or encode content safely. Never inject raw HTML from Markdown unless the project already has a trusted sanitizer and the source requires it.
   - Preserve code blocks, tables, quotes, and footnotes with accessible markup and responsive overflow behavior.

5. **Design the reading experience**
   - Build the actual report as the first screen; do not create a marketing landing page for the report.
   - In multi-document mode, make the base route a useful collection index: group by folder/category/date when available, show source paths or labels, and provide enough context to choose a report.
   - Provide a publication-quality layout with readable measure, strong heading hierarchy, scan-friendly section spacing, and mobile-first responsiveness.
   - Add expected report navigation when the document is long: table of contents, anchor links, sticky or collapsible section nav, progress affordance, or back-to-top controls as appropriate to the existing app.
   - Use the project's design system and UI primitives. If none exist, keep the palette restrained, text-forward, accessible, and not dominated by a single hue family.
   - For report assets, use real supplied images/charts/tables when available. Do not replace report evidence with decorative stock imagery.

6. **Verify behavior and fidelity**
   - Run the repo's relevant lint, typecheck, unit, or build commands.
   - Start the local dev server when needed and inspect the page in a browser at desktop and mobile widths.
   - In multi-document mode, verify the index route and a representative sample of generated document routes across short reports, long reports, tables, code blocks, and nested headings.
   - Check that all sections render, long tables and code blocks do not overflow incoherently, anchors work, generated route links are valid, and text does not overlap.
   - Compare rendered pages against the Markdown sources for missing headings, tables, figures, links, and appendix content. For large batches, run a scripted parity check for document count, heading count, route count, and broken route links.
   - Capture screenshots or describe browser verification evidence in the final response.

7. **Document and ship**
   - Record the source Markdown path or discovery query, generated base route, per-document route strategy, document count, verification commands, and any fidelity exceptions.
   - If tracked files changed, commit and push intended changes on the repository primary branch unless the user explicitly asked not to.
   - Leave unrelated dirty files untouched.

## Output

- **Source:** Markdown report path, directory, or `--all-output-docs` discovery scope used.
- **Website:** base route, index route, and document routes created or updated.
- **Implementation:** key components/data files created or changed.
- **Route Plan:** slug strategy, route count, and collision handling.
- **Fidelity:** any report content intentionally transformed, deferred, or unsupported.
- **Validation:** commands and browser checks run.
- **Git:** commit hash and pushed branch when tracked files changed.
- **Next Work:** exact follow-up, or `none` only when there is no useful follow-up.

## Constraints

- Do not use raw Markdown rendering as the final implementation when the user asked for clean JSX. Markdown may be an intermediate parsing source only.
- Do not collapse multiple documented outputs into one giant page when route-based output is expected. Use an index route plus one route per document.
- Do not create a separate frontend app just because reports are numerous. Prefer integrating into the existing documentation/public site unless the target-selection rules justify separation.
- Do not invent report findings, citations, images, charts, or metrics.
- Do not hide dense report content behind decorative cards, carousels, or marketing sections.
- Do not introduce a new frontend framework inside an existing app unless the user explicitly requests a separate standalone site.
- Do not add broad dependencies for Markdown parsing or UI when the existing project or standard toolchain is sufficient.
- Keep generated JSX maintainable enough for a human to edit the report after conversion.
- Do not skip visual verification for a frontend website.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/report-website-{topic}.html`.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>`.
- After building the report website, recommend `$uat` when the report is intended for stakeholder review, or `$ship` when implementation is complete but not yet packaged.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping.
