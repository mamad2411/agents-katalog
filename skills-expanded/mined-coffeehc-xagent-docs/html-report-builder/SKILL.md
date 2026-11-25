---
name: html-report-builder
description: Use when the user explicitly asks for an HTML report/document, printable or PDF-ready HTML, static visual report page, dashboard-like report page, HTML report package, or when an upstream Skill has produced structured report content that needs HTML packaging. Do not use for research, data analysis, formal drafting, factual conclusion generation, software UI prototypes, frontend app projects, deployment, or external publishing flows.
meta:
  version: 4
  display_name: HTML 报告生成器
---

# HTML Report Builder

## Purpose

Create a static HTML report or HTML document package with one primary HTML entry file and optional local CSS, JavaScript, image, data, or asset files under the same report root. The user should be able to open, share, print, archive, preview, and pass the report to an HTML-to-PDF worker without a build step. The report may include already-prepared narrative content, KPI cards, native SVG charts, tables, timelines, comparison matrices, appendices, visual packaging, and lightweight in-page interactions.

This Skill integrates report-generation patterns from reviewed open-source HTML Skills. It intentionally excludes their publishing systems, callback receivers, package managers, CDN libraries, MCP flows, app templates, and software UI prototype workflows. Its core responsibility is report content structure, evidence-visible presentation, and static report packaging, not enforcing that every byte lives in a single HTML file.

## Trigger

Use only when:

- The user explicitly asks for an HTML report, HTML document, visual static report, printable HTML, PDF-ready HTML, static HTML report package, single-file HTML artifact, or shareable offline HTML file.
- The user asks for a dashboard-like report page, KPI page, visual comparison page, timeline page, or static data report page as an HTML deliverable.
- An upstream domain Skill has already produced structured report content and the remaining task is HTML packaging, visual layout, chart rendering, print styling, or PDF conversion compatibility.
- The user asks to convert already-provided Markdown, JSON, report notes, tables, chart specs, or a report-spec into a polished HTML report.

Do not trigger merely because the user asks for a report, analysis, evaluation, comparison, plan, design document, retrospective, briefing, decision memo, executive summary, research synthesis, data analysis, or formal document. Those tasks belong to upstream domain Skills unless the requested deliverable is explicitly HTML or PDF-ready HTML.

Prefer this Skill over frontend app/UI Skills when the artifact is a document-like HTML report, not a product interface.

When paired with a domain or method Skill, this Skill owns final HTML packaging, visual presentation, chart rendering, print styling, and PDF conversion compatibility. The upstream Skill owns evidence gathering, analysis method, domain reasoning, formal drafting, and factual conclusions.

## Non-goals

Do not use this Skill for:

- Research, data analysis, formal drafting, policy reasoning, market analysis, business recommendations, or final factual conclusion generation.
- App pages, login pages, CRM/SaaS/admin console prototypes, component libraries, or product UI mockups.
- React, Vue, Next.js, Vite, Tailwind, package-manager, or frontend app projects that require a build step.
- Interactive editors, local servers, listeners, web apps, iframes, deployment, or public hosting.
- GitHub Pages, Vercel, Netlify, Figma, Google Stitch, MCP servers, plugin marketplace, or slash-command ecosystems.
- Remote CDN libraries, remote fonts, remote images, analytics scripts, embeds, or unapproved external runtime dependencies.
- Slide decks as the primary output unless the user explicitly asks for a report-like HTML presentation; even then, keep it a static report package with a clear primary entry.

## Inputs

Before writing the report, identify:

- Audience, purpose, report title, output path, language, and expected reading context.
- Source material: pasted text, Markdown, CSV/TSV/JSON, database/query output, screenshots, attachments, URLs already fetched, code snippets, logs, or prior notes.
- Provided claims, metrics, time range, entities, comparison candidates, chart intent, table fields, and source/citation needs.
- Confidentiality constraints and whether any provided data contains secrets, private keys, tokens, credentials, or regulated data.

If core content or evidence is missing, produce a partial report with `待确认` / `Not verified` sections or ask for the smallest missing material. Do not invent data, sources, dates, owners, benchmarks, or conclusions.

## Report Spec Input

This Skill may receive a structured `report-spec` from an upstream Skill. Treat it as the preferred input contract when available.

A report-spec may include:

- `title`, `subtitle`, `audience`, `purpose`, `language`, `date_scope`, and `source_scope`;
- `summary`, `key_findings`, `sections`, `kpis`, `metrics`, and `actions`;
- `chart_specs`, `tables`, `timeline`, `comparison_matrix`, `scorecards`, and `figures`;
- `source_log`, `claim_evidence`, `evidence_refs`, `source_refs`, `workspace_refs`, `tool_refs`, `raw_refs`, `caveats`, `assumptions`, `unverified_items`, `data_needed`, `validation_notes`, and `appendix`;
- print or PDF preferences such as page size, orientation, margin, page headers, page footers, or sections that should avoid page breaks.

When a report-spec is provided:

- Preserve its factual content, terminology, numbers, dates, sources, caveats, and conclusions.
- Preserve claim-to-source mapping, confidence labels, unresolved conflicts, unverified items, and source freshness notes.
- You may reorganize, compress, label, group, visualize, or format the provided content for readability.
- Do not add unverified facts, data, sources, dates, benchmarks, owners, recommendations, or conclusions.
- If a chart, KPI, or table cannot be rendered from the provided data, show the limitation near the affected block instead of filling gaps.
- If the report-spec is missing evidence mapping for source-backed claims, create a visible `Needs evidence mapping` section or ask for the smallest missing evidence bundle before writing final HTML.

## Template Selection

Always select a report preset before writing HTML.

- If no style is specified, use `official-clean`.
- If the report is data-heavy, KPI-heavy, or chart-heavy, use `data-dashboard`.
- Use `executive-brief` for management summaries, one-pagers, and decision memos.
- Use `research-editorial` for long-form research briefs and evidence-heavy reports.
- Use `comparison-matrix` for option, vendor, product, or policy comparisons.

Available local templates:

- `templates/base-report.html`: minimal shared skeleton.
- `templates/official-clean.html`: default formal report.
- `templates/executive-brief.html`: conclusion-first executive brief.
- `templates/research-editorial.html`: long-form evidence report.
- `templates/data-dashboard.html`: KPI and chart-heavy report.
- `templates/comparison-matrix.html`: scored comparison report.

Do not design the report from scratch. Select a preset and compose from approved report components. Only adjust tokens when the user gives explicit brand or style constraints.

## Mandatory Execution Protocol

When this Skill owns the final HTML deliverable:

1. Start from an upstream `report-spec` when available. If no report-spec exists, create a compact content inventory first: title, audience, sections, claims, metrics, chart/table inputs, evidence refs, caveats, and missing items.
2. Select exactly one preset before writing HTML: `official-clean`, `data-dashboard`, `executive-brief`, `research-editorial`, or `comparison-matrix`.
3. If `skills_load_resource` is visible, load the selected preset by passing one exact file path from the resource index. For chart-heavy, table-heavy, or PDF-ready reports, also load the exact reference file paths listed in `Resources`.
4. Compose the report with approved component classes: `report-shell`, `report-paper`, `report-header`, `report-meta`, `executive-summary`, `report-section`, `kpi-grid`, `kpi-card`, `figure-card`, `data-table`, `evidence-box`, `caveat-box`, and `report-footer` as applicable.
5. The root report element must be auditable with `data-skill="html-report-builder"` and `data-report-preset="<preset>"`, for example: `<main class="report-shell" data-skill="html-report-builder" data-report-preset="official-clean">`.
6. Include visible verification status in the report metadata or footer. If PDF conversion was not actually run and visually checked, show `PDF: Not verified` or `PDF conversion: Not verified`.
7. Before writing the primary HTML entry, verify that the selected preset, audit attributes, approved classes, `@page`, `@media print`, print color preservation, evidence/caveat blocks, and PDF verification marker are present. If CSS/JS/assets are split into local files, verify they live under the same report root and are referenced with workspace-preview-safe relative paths unless the task explicitly requires root-relative URLs.
8. For research, evaluation, landscape, comparison, or recommendation reports, verify that each major claim or recommendation has a nearby evidence marker, source appendix entry, or explicit `Not verified` label.

Never generate final HTML directly from raw research notes when a domain Skill has not produced structured content, evidence mapping, or a report-spec. Produce the missing report-spec or ask for the smallest missing evidence bundle instead.

Do not create one-off .container/header/section/kpi-card systems that bypass the approved report template and component contract.

If `skills_load_resource` is not visible, continue from the rules embedded in this SKILL.md, but do not treat the local templates/references as loaded. In that case, the final response should not imply template-resource validation was performed.

## Resources

This Skill has local resources. They are not automatically injected into the prompt body. Use `skills_load_resource` to read the needed resource before writing final HTML.

`resource_path` must be one exact file path from the resource index below. Do not pass directories, globs, placeholders, `resources/...`, or natural-language aliases. Invalid examples: `resources/templates/`, `templates/`, `templates/<preset>.html`.

Load order:

1. Always load the selected preset template by exact path.
2. Load `references/report-style-core.md` for any substantial visual report, PDF-ready report, or report with KPI cards, charts, tables, timelines, matrices, evidence boxes, or caveats.
3. Load `references/chart-style-system.md` when rendering native SVG charts, KPI strips, legends, chart captions, or chart-plus-table pairings.
4. Load `references/table-style-system.md` when rendering data tables, comparison tables, appendix tables, or long text/URL/code cells.
5. Load `references/visual-quality-gate.md` before delivery for visual/PDF checks.
6. Use `examples/kpi-chart-report.html` only as an example pattern, not as a source of facts.

Preset path map:

- `official-clean` -> `templates/official-clean.html`
- `data-dashboard` -> `templates/data-dashboard.html`
- `executive-brief` -> `templates/executive-brief.html`
- `research-editorial` -> `templates/research-editorial.html`
- `comparison-matrix` -> `templates/comparison-matrix.html`
- `base-report` -> `templates/base-report.html`

Available resource paths:

- `templates/base-report.html`
- `templates/official-clean.html`
- `templates/executive-brief.html`
- `templates/research-editorial.html`
- `templates/data-dashboard.html`
- `templates/comparison-matrix.html`
- `references/report-style-core.md`
- `references/chart-style-system.md`
- `references/table-style-system.md`
- `references/visual-quality-gate.md`
- `examples/kpi-chart-report.html`

## Report Style Core

Use `references/report-style-core.md` when creating or modifying the visual structure of a report, especially when it includes KPI cards, charts, tables, timelines, matrices, evidence boxes, caveats, or print/PDF output.

Hard rules:

- Use the shared design tokens for colors, spacing, typography, radius, shadows, and chart colors.
- Do not invent random palettes, shadows, gradients, card styles, or chart colors.
- Keep the report document-like. Do not make landing pages, hero marketing pages, glassmorphism layouts, decorative blobs, or generic purple gradients.
- Keep core content readable without JavaScript.
- Keep evidence and caveats visually close to the claims they qualify.

## Approved Components

Use these component classes unless the user explicitly requests a custom brand system:

- `report-shell`, `report-header`, `report-meta`, `executive-summary`, `report-section`, `section-header`;
- `kpi-grid`, `kpi-card`, `metric-delta`, `insight-card`, `action-list`;
- `figure-card`, `chart-header`, `chart-body`, `svg-chart`, `chart-caption`, `chart-legend`;
- `data-table`, `comparison-matrix`, `timeline`;
- `evidence-box`, `caveat-box`, `risk-box`, `appendix`, `report-footer`, `print-footer`.

Do not create parallel component systems for the same report. Extend with one-off classes only when the approved components cannot express the content.

## Chart Style System

Use `references/chart-style-system.md` for KPI cards, bar charts, line charts, donut charts, heatmap-like tables, comparison matrices, timelines, legends, captions, and chart-plus-table pairings.

Charts must use native SVG and the approved chart tokens. Do not use 3D charts, rainbow palettes, random colors, decorative gradients, decorative animation, or unsupported precision. If labels overflow on small screens, switch to numbered marks plus a legend or a nearby table.

## Table Style System

Use `references/table-style-system.md` for normal data tables, compact tables, comparison tables, score tables, appendix tables, numeric alignment, zebra stripes, long text wrapping, long URL/code wrapping, and print-mode table behavior.

## Visual Quality Gate

Before delivery, apply `references/visual-quality-gate.md`. If a generated report violates the gate, revise the HTML instead of explaining the issue in the final response.

## Output Contract

The output must be:

- A primary `.html` file unless the user explicitly asks only for source text. Supporting local CSS, JavaScript, images, data, or asset files may be generated when they make the report easier to maintain, preview, or reuse.
- The primary final deliverable for explicit HTML report or PDF-ready HTML tasks. Markdown, JSON, CSV, or text files may be supporting materials, source ledgers, drafts, or appendices, but should not replace the visual report unless requested.
- Static and portable: inline assets are allowed, and workspace-local CSS/JavaScript/images/data/assets are allowed under the same report root. No package install, build step, hosted server, or network access should be required.
- Preview-friendly: prefer relative URLs for local assets so workspace static preview and direct browser open resolve the package consistently.
- Source-backed: claims, numbers, caveats, and assumptions appear near the relevant content.
- Evidence-visible for research, evaluation, comparison, market, industry, competitor, landscape, trend, case-analysis, recommendation, or decision reports: include inspected source URLs, workspace refs, tool/raw refs, provided-material refs, or explicitly labeled assumptions in the report body or evidence appendix.
- Claim-auditable: major claims and recommendations preserve the upstream `claim_evidence` mapping or show an explicit missing-evidence marker.
- Machine-auditable: the primary report root includes `data-skill="html-report-builder"` and `data-report-preset="<preset>"`.
- Responsive down to 390px width without page-level horizontal overflow.
- Printable with a usable `@media print` stylesheet.
- Accessible with semantic landmarks, keyboard-reachable controls, visible focus states, and sufficient contrast.

## Completion Gate

Before delivery, confirm:

- a primary `.html` entry file exists and is listed before any supporting assets;
- the selected preset and required resources were used when resource loading was visible;
- `data-skill`, `data-report-preset`, print CSS, and PDF verification status are present;
- evidence, caveats, assumptions, and unverified items are visible inside the HTML for source-backed reports;
- no claim, metric, citation, chart datum, recommendation, or source was invented during packaging.

Do not depend on:

- external SaaS or design platforms;
- MCP servers;
- custom local web servers;
- package managers or build tools;
- CDN, remote fonts, remote images, iframe embeds, analytics, tracking, or unapproved remote runtime dependencies;
- GitHub Pages, Vercel, Netlify, or other publishing systems.

## Report Structure

Adapt the structure to the material, but default to:

1. Header: title, one-sentence framing, date/source scope, and caveat if evidence is incomplete.
2. Executive summary: the answer, recommendation, or headline finding in the first screen.
3. KPI or fact strip: 3-6 verified headline metrics when available.
4. Main sections: research synthesis, analysis, comparison, timeline, findings, or narrative.
5. Visual modules: charts, tables, matrices, timelines, flow diagrams, or callouts where they clarify the report.
6. Evidence and caveats: sources, assumptions, limitations, conflicts, and unverified items.
7. Next steps or decisions needed when the report supports action.

Use section IDs and an in-page table of contents for reports longer than three major sections. Keep headings short; move long context into prose, captions, or notes.

For research or analysis reports, include visual structures that make the conclusion inspectable:

- scorecard or recommendation matrix;
- ranked options or industry/category comparison;
- evidence/source appendix with inspected source refs as clickable links when URLs or workspace refs are known;
- confidence, caveat, and unverified-item markers;
- timeline, funnel, workflow, or roadmap when sequence matters.

For source-backed reports, do not hide evidence in internal notes or final chat text only. The HTML report itself must show which claims are verified, assumed, disputed, or not yet verified.

## Fact Boundary

This Skill may:

- organize, compress, rewrite for clarity, label, format, and visually package already-provided content;
- choose visual modules for provided facts, such as KPI cards, tables, matrices, timelines, charts, callouts, and appendices;
- transform provided chart specs or tabular data into native SVG, semantic tables, captions, and legends;
- surface caveats, assumptions, confidence labels, and evidence refs closer to the claims they qualify.

This Skill must not:

- create new facts, data, sources, dates, owners, benchmarks, interpretations, recommendations, or conclusions;
- infer missing numbers or causal explanations from incomplete material;
- present model-memory claims as verified facts;
- upgrade assumptions into conclusions;
- hide missing evidence to make the report appear complete.

New conclusions must come from an upstream domain Skill or from verified material visible in the current task.

## Chart And Statistics Rules

Default chart rendering uses native SVG, semantic HTML tables, CSS, and vanilla JavaScript only. CSS and optional enhancement JavaScript may be inline or placed in local static files under the report root.

Use charts only when they explain a pattern better than text:

- KPI cards for headline counts, totals, rates, deltas, best/worst, pass/fail, cost/time, or sample size.
- Bar charts for ranked categories and comparisons.
- Line/area charts for time series with sorted dates and visible units.
- Scatter/bubble charts only when two numeric axes are both meaningful.
- Heatmaps for two-dimensional intensity matrices.
- Waterfall or funnel charts for stepwise change or conversion.
- Timelines/roadmaps for ordered events, milestones, dependencies, and status.
- Comparison matrices for candidates, criteria, weights, rationale, and disqualifying requirements.

Rules:

- Every chart must include title, units, data source/caveat, and exact values in a nearby table or caption.
- Sort data deterministically. Do not use randomness, animated transitions, or non-deterministic layout.
- Do not truncate data silently. State row limits, filters, sampled data, and omitted fields.
- Keep labels readable at 390px. If SVG labels may overflow, use numbered marks with a following legend/list or SVG `foreignObject` only when browser support is acceptable.
- Use stable IDs for SVG gradients, clip paths, and controls.
- Use `textContent`, `createElement`, and safe data serialization for user-provided text. Do not inject variable content through `innerHTML`.
- If a chart library seems necessary, it must be vendored locally, audited, and explicitly allowed by the project owner before use. Otherwise do not use it.

## HTML Implementation Rules

Use a compact static document architecture:

- `<!doctype html>`, `<html lang>`, `<meta charset>`, viewport, descriptive `<title>`, and one `<main>`.
- Inline CSS or local stylesheet files under the report root. Keep styling scoped to the report and avoid scattering report styles across unrelated directories.
- No inline `style=""` except SVG geometry or CSS custom properties that cannot be expressed cleanly elsewhere.
- CSS custom properties for colors, spacing, typography, borders, and chart tokens.
- A restrained palette chosen for the report domain. Avoid generic purple gradients, decorative blobs, glassmorphism, and stock landing-page composition.
- Semantic sections, tables, lists, figures, captions, details/summary for appendices, and buttons only for real actions such as filter, sort, copy, print, or toggle.
- Inlined data in JSON script blocks only when data size is reasonable and secret-free.
- Local data files are allowed when data is large enough that embedding it would make the primary HTML hard to review; the report must still show a visible summary and source/caveat context without relying on a hidden data file.
- Tables with more than 10 rows should have search, sorting, filter controls, pagination, or a clear summary plus appendix.
- Long paths, URLs, hashes, code, commands, and identifiers must wrap or scroll inside their own container.
- Use native SVG for charts and diagrams; keep hand-authored diagrams small and source-labeled.
- JavaScript must be optional enhancement for filtering, sorting, details, toggles, and copy/export. The report remains readable if JS fails.

## HTML To PDF Compatibility Rules

Assume the HTML may be converted to PDF by an `html_to_pdf` worker.

- Define `@page` with paper size and margins. Default to `size: A4 portrait` and explicit margins unless the user or report-spec requests otherwise.
- Use `@media print` for print/PDF layout, hiding only non-essential controls and expanding content that must appear in the PDF.
- Avoid `position: fixed`, `position: sticky`, full-viewport hero sections, `height: 100vh`, and viewport-height-dependent layouts because they can break pagination.
- Use `break-inside: avoid` / `page-break-inside: avoid` only on compact cards, figures, KPI blocks, short evidence/caveat boxes, table rows, chart-caption groups, comparison items, timeline items, and other small grouped blocks.
- Do not apply `break-inside: avoid` to long page-level containers such as `section`, `report-section`, or large highlight/content boxes. Long sections must be allowed to split across pages, otherwise PDF output can produce large blank areas.
- For tables, use semantic `<table>` markup, repeatable headers where possible, and avoid splitting short summary tables across pages. Large tables may split, but headers, captions, units, and caveats must remain clear.
- Keep charts and their captions, legends, source notes, and caveats together when practical.
- Do not rely on JavaScript to render core report content, charts, evidence, or conclusions. JavaScript may enhance sorting, filtering, copying, or toggles only after the core content is present in HTML/SVG.
- Preserve print colors explicitly: include `-webkit-print-color-adjust: exact` and `print-color-adjust: exact` on `html`, `body`, or all report elements, and repeat any color-critical header/card backgrounds inside `@media print` with `!important` when needed.
- Ensure printed backgrounds are compatible with PDF workers using `printBackground`; for manual browser "Save as PDF", the user may still need background graphics enabled. Do not depend on background colors alone for legibility or status.
- Prefer real text over background images or canvas for content that must appear in PDF.
- If the HTML has not actually been converted and visually checked as PDF, state that PDF conversion is `未验证` / `Not verified` in the completion note or visible validation notes when relevant.

## Accessibility And Print Rules

Minimum checks:

- Body text and chart labels meet WCAG AA contrast.
- Interactive controls are buttons or links with accessible labels and visible focus.
- Charts have textual captions or adjacent tables so the information is not color-only.
- Status uses text/shape plus color, not color alone.
- `prefers-reduced-motion: reduce` disables motion if any transitions exist.
- `@media print` removes controls, expands key hidden content, avoids clipped backgrounds, and preserves page breaks.
- Print CSS preserves intended report header, KPI, chart, table header, badge, and callout colors where those colors carry visual hierarchy.
- The report is usable at 390px width, standard desktop width, and print/PDF preview.
- Print/PDF output preserves claim text, evidence refs, captions, charts, table headers, caveats, and appendix content.

## Validation Checklist

Before delivery, verify:

- The primary entry opens in browser or workspace static preview without network requests, build step, custom server, or console errors.
- No remote `<script src>`, remote stylesheet, remote image, iframe, analytics, package-manager, or deployment instruction exists. Local CSS/JS/assets are allowed when they are under the report root and intentionally referenced.
- HTML has doctype, head, body, viewport, title, main, sections, and closing tags.
- Primary report root includes `data-skill="html-report-builder"` and `data-report-preset="<preset>"`.
- CSS and JS are inline or workspace-local static files, and scoped to the report.
- Claims, metrics, dates, and comparisons trace to provided or fetched sources.
- Research-like reports do not present model-memory claims as sourced facts. If no inspected source exists, the report title, caveat strip, and affected sections must label the work as assumption-only, draft, or evidence-blocked.
- The report includes a user-visible evidence/source section when any conclusion depends on external or provided material.
- Tables and charts have units, captions, and no silent truncation.
- Layout has no incoherent overlap or page-level horizontal overflow at 390px.
- Print stylesheet is present and usable, including `@page` and `@media print`.
- Print stylesheet includes `-webkit-print-color-adjust: exact` / `print-color-adjust: exact`, and color-critical backgrounds are not accidentally stripped in print mode.
- PDF conversion compatibility rules have been followed. If actual PDF conversion was not run, mark PDF conversion as `未验证` / `Not verified`.
- Secrets are not rendered. If suspected secrets are present, stop and warn instead of generating the report.
- The final response or completion report names the primary HTML file and links it with a Markdown link when a workspace ref is known.
- The primary HTML report is listed before supporting CSS/JS/assets, Markdown notes, source ledgers, drafts, JSON, CSV, or appendices.

## Failure / Escalation

- Missing evidence or missing upstream conclusions: produce a partial report with a clear `待确认` / `Not verified` list, or ask for the smallest missing source bundle.
- Conflicting sources: show the conflict, cite both sides, and avoid forcing a false conclusion.
- Oversized data: summarize, aggregate, or paginate; state the size and any sampling. Do not silently drop rows.
- Required external dependency: stop and ask for explicit approval to vendor and audit it, or switch to native SVG/HTML.
- User asks for app prototype or frontend project: hand off to the appropriate frontend/UI Skill instead of stretching this Skill.

## References reviewed

| source | category | license | skill_md | fit_score | useful_patterns | dependencies_to_remove | risk | recommendation |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| `Sologa/codex-html-report-skill` | HTML report | MIT | yes | 5 | Report planning, sections, TOC, charts, searchable tables, print/mobile quality bar | publish script, hosting manifest, commit/push flow, remote library assumption | Publishing workflow and remote dependency conflict with XAgent offline contract | Absorb report structure and quality bar only |
| `careerhackeralex/visualize` | visual HTML | MIT | yes | 4 | Visual hierarchy, responsive checks, chart sizing, accessibility/print checklist | remote chart/runtime libraries, remote fonts, file auto-open requirement, broad UI/prototype scope | Too broad; encourages external libraries and visual app surfaces | Absorb sizing/accessibility/checklist ideas; exclude library and UI prototype defaults |
| `f-labs-io/agent-html-skills` | report modules | MIT | yes, multiple module Skills | 5 | Research reports, data explorer, comparison matrix, timeline/roadmap modules, source lists, semantic HTML | local submit receiver, submit server, clipboard bridge, plugin assets, external tool-hosting assumptions, remote font allowance | Strong module ideas but coupled to local server/plugin submission pipeline | Absorb report module taxonomy; remove runtime/submission protocol |
| `iharnoor/html-everything` | editorial HTML | MIT | yes | 4 | Single-file editorial conversion, input type detection, linkification, no package installs | remote font loading, shell open command, command-style invocation metadata | Good lightweight conversion recipe; weak data/chart coverage | Absorb content classification and editorial single-file discipline |
| `evalstate/birch-html` | visual report system | Apache-2.0 | yes | 4 | No network assets, source-grounded claims, mobile safety, strict component contracts, validation mindset | Birch CSS placeholder/resources, Python scripts, uv commands, benchmark/eval publishing scripts | Tied to Birch asset pipeline and scripts | Absorb no-network, grounding, mobile, table/SVG safety rules |
| `gooseworks-ai/goose-skills` | dashboard/slides ecosystem | not confirmed at repo root | yes, related dashboard/slides Skills | 2 | Data-first dashboard discipline and grid/layout thinking | React/Vite/Express template, package manager, fixed local port, hosted app tab, CLI/install flow | App/dashboard product workflow, not static report | Reference only; do not import workflow |
| `proyecto26/slides-ai-plugin/html-slides` | HTML presentation | MIT | yes | 3 | Single-file viewport discipline, print/PDF, reduced motion, slide density limits | remote animation/diagram/code libraries, PPTX extraction script, remote fonts, slide-first output | Presentation focus can distort report structure | Absorb viewport/print ideas only when report-like presentation is requested |
| `benchflow-ai/skillsbench/d3-visualization` | deterministic charts | Apache-2.0 | yes | 3 | Deterministic sorting, stable SVG, fixed dimensions, no CDN, pinned vendoring concept | D3 runtime, vendor bundle, JS helper scripts, dist layout | Requires third-party chart runtime if copied directly | Absorb determinism and SVG verification rules; default to native SVG |
| `matsonj/mviz` | chart/report spec | not confirmed at repo root | yes | 3 | KPI/chart/table taxonomy, 16-column layout, formatting/lint concepts | package-runner command, package-manager auto-download, CLI renderer, chart runtime, iframe/embed mode | License not confirmed in cloned repo; external CLI dependency | Reference chart taxonomy and lint ideas only |

## Boundary

Skill owns HTML report packaging, report structure mapping, visual module selection, native SVG chart presentation, static HTML constraints, accessibility checks, print styling, and HTML-to-PDF compatibility rules.

It does not own research, data analysis, formal drafting, domain reasoning, final factual conclusions, XAgent tool schemas, ToolResult fields, runtime path selection, file permissions, network access, external dependency approval, deployment, browser preview publishing, package installation, or final factual authority for unverified claims. It must not run shell, Python, Node, npm, curl, MCP, browser-open, publish, deploy, listener, or server commands by itself; those actions belong to XAgent tools visible in the current session and require the current task context.
