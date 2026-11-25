---
name: figure-table-studio
description: Use when the user needs top-journal-quality social-science statistical figures and tables: regression tables, descriptive tables, coefficient plots, event-study plots, predicted probabilities, marginal effects, robustness figures, text-analysis summary charts, network metrics charts, publication-ready captions, or figure/table consistency review. Not for conceptual mechanism diagrams or image2-first scientific illustrations; use research-figure-studio for those.
---

# Figure Table Studio

This skill is for empirical figures and tables in social-science manuscripts.

## Required References

Before producing formal empirical figures, read:
- `<VELA_RUNTIME_ROOT>/skills/catalog/scientific_figure_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/figure_style_presets.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/publication_style_rules.json`

## Division of Labor

- Use `figure-table-studio` for real-data charts, model-output figures, regression tables, descriptive tables, coefficient plots, event-study plots, marginal effects, predicted probabilities, robustness displays, and figure/table consistency checks.
- Use `research-figure-studio` for mechanism diagrams, conceptual frameworks, research-design diagrams, workflow diagrams, visual abstracts, non-numeric scientific illustrations, and image2-first academic figures.

If the task includes both, start with `research-figure-studio` for the figure brief and use this skill for the empirical panels.

## Non-Negotiable Standard

Every empirical figure or table must state:
- what is shown;
- unit of analysis;
- sample and time window;
- variable or construct definition;
- model or statistic;
- uncertainty meaning;
- data source;
- script or output source when available.

Do not make a visually polished chart that hides weak measurement, unsupported causal wording, or missing uncertainty.

## Scientific Figure Built-in Standards

For Excel/CSV/table-driven figures, use the `scientific_figure_workflow.json` contract as the default production standard.

Before plotting:
- Put a configuration block at the top of the analysis script: input paths, output directory, font fallback, output formats, significance thresholds, error-bar type, numeric precision, figure sizes, and DPI.
- Use a separate project output folder, normally `<project_root>/outputs/figures/<run_slug>/`, with `figures/` and `process_data/` subfolders.
- Generate a data-health report before formal plotting. At minimum check shape, dtypes, missingness, duplicate rows, descriptive statistics, outliers, and, for modeling tasks, correlation or VIF risk.
- Save process data: raw-loaded table, cleaned table, figure-specific data sidecars, and statistical-test outputs when tests are used.

Typography defaults:
- Font family: serif.
- Chinese fallback: `SimSun`, `Songti SC`, `Source Han Serif SC`, `Noto Serif CJK SC`, `serif`.
- English fallback: `Times New Roman`, `Liberation Serif`, `DejaVu Serif`, `serif`.
- Base font: 10 pt.
- Axis labels: 10 pt.
- Tick labels: 9 pt.
- Legends: 9 pt.
- Captions/figure notes: 9 pt.
- Panel labels: 10 pt.
- Annotation text: 9 pt.
- Significance marks: 10 pt.
- Single-column figure default: about 3.5 x 2.6 inches.
- Double-column figure default: about 7.2 x 4.0 inches.
- Preview raster exports: at least 300 DPI.

These are defaults, not journal law. If the target journal, Word template, or manuscript layout requires different sizing, preserve readability and state the change in the figure note or delivery summary.

Style preset defaults:
- Use `nature_empirical_red_blue_rainbow` as the default formal empirical figure style.
- Use `minimal_review_ready_red_blue` for submission, reviewer-response, robustness and final-package figures.
- Use `presentation_premium_red_blue_rainbow` only for research presentations or defense visuals, not as the default manuscript plot style.
- Do not describe a target only as "Nature style" or "top-journal style"; record the preset id in the script config, figure brief, or delivery note.
- Default aesthetics are red-blue anchored Nature-style rainbow colors, white or very light gray background, high whitespace, light gridlines, consistent labels, and no internal formal title or long caption.

Statistics and annotations:
- Add significance marks only when the figure is a justified group comparison, model estimate, or planned inferential display.
- Do not add p-values to time-series line charts, scatter plots, heatmaps, or single-distribution charts unless the design specifically requires it.
- If paired versus independent samples are ambiguous, ask before selecting the test.
- Never show `p = 0.0000`; use `p < 0.001`.
- Error bars must be named: SD, SEM, standard error, or confidence interval.

Captions:
- Use the what/how/so-what structure: what is shown, how it was summarized or tested, and what bounded conclusion the reader can take away.
- For social-science figures, also state unit of analysis, sample/time window, model/statistic, uncertainty meaning, data source, and script/output source when available.

Exports:
- Keep editable or vector sources whenever possible: script, PDF, SVG, or PPT.
- PNG is acceptable as a preview or submission support file.
- JPG is a compatibility output, not the only manuscript source.
- A final empirical figure without process data, caption, and source path should not pass `figure_table_consistency_checked`.

## Workbench Plot Adapters

The local workflow absorbs useful plotting patterns from `Jinze-Lee/codex-skills-workbench` as adapters, not as separate default skills.

Use them this way:

- Tool selection: choose R, Python, PowerPoint, vector tools, spreadsheets, or image2 from the final destination, data shape, modeling need, visible desktop requirement, reproducibility requirement, and collaboration constraints.
- R scatterplots: when making grouped scatterplots or regression plots, validate x/y variables, missingness, outliers, group sample sizes, model choice, and export the figure with statistics.
- Raincloud plots: use only when the manuscript needs distribution shape, raw observations, intervals, and summary markers together; do not use it as decoration.
- Weighted regression plots: first define what the weight means, check zero/negative/extreme weights, compare with unweighted results when useful, and state whether weighting changes the relationship.
- ggplot2 rich text: for superscripts, subscripts, formulas, Markdown/HTML labels, or special symbols, choose plotmath, Unicode, or `ggtext` deliberately and test the exported file, not only the preview.

Ecology-specific patterns such as hypervolume, trait-environment, or phylogeny workflows are not default social-science workflows. Use them only when the project genuinely has that substantive domain.

## Prompt Pattern Adapters

The local workflow also absorbs useful figure/table prompt constraints from `Leey21/awesome-ai-research-writing`.

Use them as local rules:

- Chart recommendation: before plotting, identify whether the evidence task is comparison, trend, classification assessment, matrix relationship, distribution, composition, tradeoff, or multi-panel evidence. Choose the simplest academic chart that answers that task.
- Scale handling: if values differ sharply, decide whether a broken axis, log scale, normalization, facet, or separate panel is justified. State the reason instead of hiding scale problems.
- Statistical elements: add error bars, confidence intervals, fitted lines, p values, or significance marks only when the design and data support them.
- Figure/table titles: write direct, plain titles. Remove empty openings such as "The figure shows"; do not put a stronger conclusion in the title than the figure or table proves.
- Result-analysis text: when turning a table or chart into manuscript prose, use only the supplied numbers or verified outputs. Do not infer missing robustness, sample size, or significance.

## Workflow

1. Identify the figure/table family:
   - descriptive table
   - regression table
   - coefficient plot
   - event-study plot
   - predicted probability or marginal effect
   - distribution or trend plot
   - mechanism/heterogeneity chart
   - robustness/sensitivity chart
   - text-analysis chart
   - network metric chart
2. Write the figure/table claim:
   - one sentence for the exact point the figure/table supports.
   - if there is no clear claim, ask for it or propose a conservative claim.
3. Lock the data contract:
   - input file or model output path
   - variables
   - sample restrictions
   - missing-data rule
   - weights, clusters, fixed effects, or model variants
4. Run data-health and traceability setup for structured data:
   - produce `00_data_health.md` or an equivalent data-health note;
   - create `figures/` and `process_data/`;
   - save cleaned data, analysis cuts, statistical outputs, and per-figure data sidecars.
5. Choose the rendering path:
   - deterministic code for numeric charts and tables;
   - editable SVG/PDF/PPT where possible;
   - PNG only as preview or user-requested export.
6. Produce the figure/table and note.
7. Run the audit before delivery.

## Style Defaults

- White background.
- No chart border unless the journal template requires it.
- Light or absent gridlines.
- Direct labels where they reduce legend load.
- Shared legend for multi-panel figures.
- Color-blind friendly palette, readable in grayscale.
- Consistent fonts, axis titles, tick labels, marker sizes, and line widths.
- Figure titles and long captions stay outside the image; use manuscript text, figure notes, or delivery notes.
- Legends must not overlap lines, points, confidence intervals, bars, labels, or dense plotted areas. If they do, move the legend outside, split the panel, or use direct labels.
- No 3D bars, heavy shadows, glossy gradients, decorative icons, or poster styling.
- Do not encode meaning by color alone; add line type, marker shape, facet, label, or pattern when useful.
- Do not treat the upstream four-sided boxed frame as a universal rule. Use it only when the user, target journal, or house style requires a full enclosed frame.

Recommended red-blue rainbow palette:
- charcoal `#2F3A45`
- deep blue `#1F4E79`
- teal `#2A9D8F`
- muted orange `#F4A261`
- light gray `#D9E2EC`

Nature empirical palette is preferred for formal outputs:
- estimate blue `#1F5AA6`
- comparison red `#C7363D`
- cyan `#18A6B8`
- amber `#F2B84B`
- orange `#E67E3A`
- deep indigo `#273E8E`
- confidence gray `#C9CDD0`
- light grid gray `#E7EBF0`

## Overlap And Caption Boundaries

Before final delivery, check:

- Legends do not cover lines, points, confidence bands, bars, annotations, or direct labels.
- Axis labels and tick labels do not collide or become unreadable.
- Panel labels do not overlap axes, plot marks, legends, or annotations.
- Error bars and confidence intervals remain visually distinguishable.
- Internal notes are minimal; formal titles, long captions, sources, samples, model notes, uncertainty explanations and script paths are delivered outside the image.

## Top-Journal Table Rules

- Table title is substantive but should not state the conclusion as if it were a result sentence.
- Column and row labels must be clear; abbreviations should be avoided or defined in notes.
- Numeric precision must be consistent.
- Standard errors belong directly under coefficients unless a target journal says otherwise.
- Align decimals.
- Keep probability-note symbols consistent.
- Avoid unnecessary vertical lines, heavy borders, and wide landscape tables.
- A table note must explain model, sample, controls, fixed effects, uncertainty, and source.

## Top-Journal Figure Rules

- Axes must name the quantity and unit.
- Uncertainty must be shown or explicitly explained as unavailable/not applicable.
- A multi-panel figure must use panels for distinct evidence, not repetitions.
- Panel labels should be short, meaningful, and visually consistent.
- Captions should not rely on color words alone because print or grayscale reading may remove color.
- Figure files should be named consistently with panel letters when exporting separate panels.

## Event-Study and Coefficient Plot Rules

- State the omitted/reference category.
- Show confidence intervals and the confidence level.
- Mark treatment/event time clearly.
- Avoid connecting estimates when a line would imply continuity that the model does not support.
- Keep axis ranges comparable across panels unless there is a stated reason not to.
- Do not overstate pre-trend or causal interpretation without the identification design.

## Audit Checklist

Before final delivery, verify:
- claim matches the plotted data/table;
- sample and unit are stated;
- labels and notes are readable;
- uncertainty is defined;
- no false precision;
- legends, annotations, labels, error bars, confidence intervals and plotted marks do not overlap;
- formal title and long caption are outside the image;
- color and grayscale both work;
- figure/table matches the manuscript text;
- source data or script path is recorded when available;
- output is editable or high-resolution enough for review.

If the audit fails, revise before calling the result finished.
