---
name: build-standalone-html-report
description: Build or revise polished standalone single-file HTML research reports, incident reports, post-mortems, architecture comparisons, decision briefs, and evidence summaries with responsive tables, charts, diagrams, lightweight interaction, and iterative preview feedback. Use when Codex must turn research, raw measurements, repository evidence, or incident timelines into a self-contained HTML report; add architecture diagrams or data visualizations; improve an existing report from preview annotations; or validate and publish a standalone report.
---

# Build Standalone HTML Report

Produce a decision-ready artifact, not a decorated transcript. Keep the source evidence traceable while making the main conclusion understandable without repository knowledge.

## Start from the governing constraints

1. Read repository instructions before choosing the output path or link style. Treat local publishing rules as authoritative.
2. Identify the primary reader, the decision or incident question, and what action the report should enable.
3. Inspect the raw evidence, existing report, and any preview annotations. Preserve supported facts; do not infer certainty from visual polish.
4. Read [references/editorial-method.md](references/editorial-method.md) for research, comparison, incident, or decision reports.
5. Read [references/visual-system.md](references/visual-system.md) whenever the report needs charts, architecture diagrams, dense comparison tables, or interaction.
6. Read [references/quartz-publishing.md](references/quartz-publishing.md) only when the repository uses Quartz or declares the same standalone-report rules.

## Build the argument before the page

Write a compact content outline before styling:

- State the conclusion or incident impact first.
- Separate observed facts, inferences, unknowns, and limitations.
- Define unfamiliar terms in plain language at first use.
- Keep only details that change a decision, explain causality, or support verification.
- Remove internal reasoning, discarded alternatives, and unrelated repository inventory from the final artifact.
- Attach precise numbers to method, sample window, units, provenance, and raw evidence.
- Present resource footprint as one decision input; never imply it ranks total safety, operability, recovery, or product fit.

Choose a visual only when it reduces cognitive load:

- Use a table for exact repeated comparisons.
- Use a chart for magnitude, distribution, composition, or change.
- Use a timeline for event order and causal transitions.
- Use an architecture diagram for ownership, boundaries, routing, and failure paths.
- Use prose or a short list for a single fact or simple sequence.

## Create the single-file artifact

Copy [assets/report-template.html](assets/report-template.html) as a starting point when creating a new report. Replace its generic content; do not preserve placeholder sections that add no value.

Keep the deliverable self-contained:

- Default to a light theme. Provide optional dark mode only when useful.
- Embed CSS and JavaScript in the HTML.
- Draw charts and diagrams with inline SVG or HTML/CSS. Do not require external CSS or JavaScript at runtime.
- Use semantic landmarks, one clear `h1`, logical heading levels, accessible controls, keyboard-usable interaction, and text alternatives.
- Make layouts responsive, printable, and free of horizontal page overflow. Wrap or locally scroll only genuinely wide tables.
- Keep color meaningful but nonessential; label series and states directly.
- Draw directional arrows unambiguously. Label control plane, data plane, trust, ownership, and failure boundaries when they matter.
- Preserve raw data outside the HTML when required, and link it through a publishable stable location rather than a broken local path.

Use progressive disclosure for secondary evidence: concise findings first, details/tables afterward, and raw artifacts last. Keep essential conclusions visible without clicking tabs or expanding disclosures.

## Iterate through preview feedback

1. Open the actual HTML in the repository's supported preview browser.
2. Inspect desktop and mobile widths, not only the default viewport.
3. Treat each preview annotation as evidence of reader confusion. Rewrite the underlying explanation or visual hierarchy; do not merely patch the highlighted phrase.
4. Replace jargon with the reader's language. Explain domain terms on first occurrence.
5. Remove content identified as irrelevant instead of defending why it was included.
6. When feedback asks for a chart, confirm the relationship is chart-worthy and choose the smallest fitting visual.
7. Re-run the entire validation loop after structural changes.

## Validate before handoff

Run the bundled validator:

```bash
python3 scripts/validate_report.py path/to/report.html
```

Use `--strict-warnings` for new generic reports and templates. Use `--format json` when automation needs structured results. Exit code `0` means no errors; warnings remain non-fatal unless strict mode is enabled. Exit code `1` means report defects; exit code `2` means invalid invocation or unreadable input.

Also verify:

- Desktop and narrow/mobile rendering
- Browser console without errors
- No page-level horizontal overflow
- Tabs, filters, toggles, details, and tooltips by mouse and keyboard
- Print preview and readable monochrome output
- Every local link, fragment, and report-to-report link
- Method/raw/provenance links from every precise experimental result
- Publishing index and repository-required navigation

Do not claim completion from source inspection alone. Render, interact, validate, and inspect the final artifact.
