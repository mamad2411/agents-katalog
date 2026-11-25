---
name: figure-design
description: Use when creating, updating, or reviewing a research figure (plot, chart, brain map, heatmap, schematic) — guides chart-type selection, typography, colorblind-safe palette, layout, and journal-specific export specs. Dispatches a figure-reviewer subagent after rendering. Complements claims-audit (which checks figure integrity) by checking figure design.
---

# Figure Design

## Overview

Guide the creation of a research figure with the same discipline Eureka applies to everything else: gates before rendering, iron laws that do not bend, a hard prohibition on chart junk, and a fresh-eyes subagent review after every figure. A figure is an argument — every pixel either advances it or distracts from it.

**Core principle:** A peer reviewer spends 3 seconds on a figure before forming an opinion. Those 3 seconds decide whether they read the caption, the text, or the paper at all.

## The Iron Law

```
NO FIGURE WITHOUT A GENERATING SCRIPT.
NO SUBMISSION WITHOUT COLORBLIND-SAFE PALETTE.
NO DEFAULT MATPLOTLIB STYLE IN A TOP-JOURNAL SUBMISSION.
```

Writing a figure means writing a script that produces it deterministically. Picking a palette means picking one that 8% of male readers can still decode. Setting a style means setting it once at the top of the script and never editing the output manually.

## When to Use

**Use this skill when:**
- The user says "make a figure", "draw fig X", "plot the results", "update the brain map", "the figure looks wrong"
- A Results section is being written and a figure is needed
- An existing figure failed reviewer feedback or journal submission
- A multi-panel composite figure is being assembled

**Do NOT use when:**
- The user is doing pure data analysis with no figure output (no skill needed)
- The user wants to verify figure integrity post-hoc (use `eureka:claims-audit` Part B)
- The user is writing a manuscript section (use `eureka:manuscript-writing`)

## Checklist

You MUST create a task for each of these and complete them in order:

1. **Determine figure purpose** — ask the user: what argument does this figure advance? One sentence.
2. **Identify target journal** — ask the user, or check `CLAUDE.md` / the manuscript. Different journals have different column widths, fonts, formats.
3. **Select chart type** — match the purpose to a chart type (see Chart Type Selection Gate below)
4. **Set global style ONCE** — `apply_paper_style()`-equivalent at the top of the script (font family, TrueType embedding, DPI, spine style)
5. **Render the figure** — write the script; run it; inspect the output
6. **Apply iron laws** — typography, color, layout, export format (see Iron Laws below)
7. **Inline self-check** — run through the Red Flags list
8. **Dispatch `figure-reviewer` subagent** — per figure, after the inline check passes
9. **Act on feedback** — fix issues; re-render; re-dispatch until approved
10. **Commit script + output** — both the `.py`/`.R` and the `.pdf`/`.svg` go to git

## Chart Type Selection Gate

<HARD-GATE>
Before writing any plotting code, state the figure's purpose in one sentence and select the chart type from this table. If your purpose doesn't match any row, stop and ask the user to clarify.
</HARD-GATE>

| Purpose | First choice | Acceptable alternative | Avoid |
|---|---|---|---|
| Compare ≤5 groups on one metric | Horizontal bar chart | Grouped vertical bar | Pie chart, 3D bar |
| Compare >5 groups on one metric | Dot plot, lollipop chart | Heatmap (if >10) | Stacked bar, spaghetti line |
| Show distribution of a single variable | Violin plot, histogram | Box plot with raw points overlaid | Bar of mean only (hides spread) |
| Show distribution across groups | Violin + strip, raincloud plot | Box + swarm | Bar chart of means |
| Show trend over time (continuous) | Line plot with CI band | Scatter + LOESS | Bar chart with time on x-axis |
| Show relationship between 2 continuous variables | Scatter + regression line | Hexbin (if N is large) | 3D scatter |
| Show rank ordering | Dot plot, horizontal bar | Slope chart (if 2 timepoints) | Pie chart |
| Part-to-whole (few categories, one total) | Stacked horizontal bar | Tree map | Pie chart with >3 slices, donut chart |
| Show flow / transition | Sankey diagram, alluvial plot | Chord diagram | Network diagram with arbitrary arrows |
| Show spatial pattern (brain, map, chip) | Heatmap on native coordinates | Glass-brain projection (neuroscience) | Volume rendering for 2D questions |
| Show matrix of pairwise relationships | Heatmap with clustering | Correlation matrix with dendrogram | Separate scatter plots per pair |
| Show two metrics simultaneously | Scatter with size encoding | Dual-axis line (only if scales compatible) | Dual-axis with unrelated scales |

**Anti-patterns (never use these):**
- **3D bar / 3D pie charts** — the 3D projection distorts comparison
- **Rainbow / `jet` colormap for sequential data** — not perceptually uniform, not colorblind-safe
- **Gradient fills for categorical colors** — implies ordering where none exists
- **Dual y-axes with unrelated scales** — invites misleading visual correlation
- **Pie charts with >3 slices** — angle comparison is harder than length comparison
- **Dynamite plot (bar of mean + error whisker with no raw data overlay)** — reviewer-flagged top-10 mistake per eLife (Ten common statistical mistakes). Hides distribution, misrepresents spread, biases the eye to means. Overlay raw points or switch to violin/box when N per group ≤ 50

## Iron Laws

These apply regardless of tool, field, or journal:

### 1. Typography: sans-serif, 5-7pt, one family per paper

- **Font family**: Arial or Helvetica (Nature, Cell, most STEM). Helvetica specifically for Science family. Never Comic Sans, Times, Courier, or decorative fonts.
- **Size range**: 5pt minimum, 7pt typical for axis labels/tick labels, 8-9pt for panel labels. Anything below 5pt is unreadable in print.
- **Consistency**: same font family across ALL figures in a single paper. Mixing Arial and Helvetica across figures is a reviewer's cheap hit.
- **TrueType embedding (matplotlib)**: set `plt.rcParams['pdf.fonttype'] = 42` and `plt.rcParams['ps.fonttype'] = 42`. Default Type 3 fonts are rejected by most journals.

### 2. DPI / resolution: 300 minimum raster, vector preferred

- **Vector formats (PDF, SVG, EPS)** are preferred for anything with lines, text, or geometric shapes (scatter plots, bar charts, line plots).
- **Raster formats (PNG, TIFF)** only for pixel-based content (microscopy, photographs, brain volume renderings). Minimum 300 DPI at final print size. 600 DPI in the save command gives headroom.
- **Never JPEG** for scientific figures — compression artifacts around text and edges.

### 3. Color: colorblind-safe, semantic, minimal

- **Qualitative (discrete categories, ≤8 items)**: Okabe-Ito palette, tol-bright palette, matplotlib `tab10`. All colorblind-safe.
- **Sequential (ordered magnitude)**: `viridis`, `cividis`, `plasma`, `inferno`. All perceptually uniform and colorblind-safe.
- **Diverging (zero-centered)**: `RdBu_r`, `coolwarm`, `PuOr`. Colorblind-safe if tested.
- **Never**:
  - Red AND green for categorical contrast (8% of men cannot distinguish)
  - Rainbow / `jet` for sequential data (not perceptually uniform)
  - More than 8 qualitative colors in one figure (saturates the reader's discrimination)
- **Semantic consistency**: if blue = model A in Figure 2, blue = model A in Figure 3. Pick a palette dictionary at the project level; reuse it everywhere. See `docs/references/figure-guide.md` for copy-paste hex codes.

### 4. No chart junk (Tufte)

- No 3D effects, drop shadows, gradient fills on bars, textures, or ornamental gridlines
- No frame around the plot area unless the journal explicitly requires it (most don't)
- Remove top and right spines (`axes.spines.top: False`, `axes.spines.right: False`) — they add ink without information
- Gridlines only when they aid reading specific values; if used, thin and light gray

### 5. Axes: label with units, human-readable ticks

- Every axis has a label. Every label includes units (except when units are counts or dimensionless ratios, in which case say so: "Accuracy" not "Accuracy (unitless)").
- Tick values are round numbers humans read quickly: 0, 0.25, 0.50, 0.75, 1.00 — not 0, 0.17, 0.33, 0.50, 0.67, 0.83.
- Avoid scientific notation unless the magnitude demands it; prefer log scale with integer decade ticks.

### 6. Legend: readable, non-overlapping

- Legend text at the same size as tick labels (or 1pt smaller, never smaller than 5pt)
- Position outside the data region when possible; if inside, never overlapping data points or error bars
- No legend frame unless the legend overlaps gridlines or other elements; prefer `frameon=False`
- If the categories are obvious (e.g., labeled directly on the lines), omit the legend entirely

### 7. Panel labels: lowercase, bold, top-left

- Multi-panel figures use (a), (b), (c), ... — lowercase, bold, sans-serif, in the top-left corner of each panel
- Consistent size across all panels (typically 8-10pt, larger than tick labels)
- Panel label does NOT overlap the plot content — place it in the figure margin, not on top of axes

### 8. Export format matches journal requirements

See the Journal Export Gate below for the table.

### 9. Legend self-containment (reviewer-grade)

Figure + legend alone must be interpretable **without reading the main text**. Reviewers often evaluate figures independently of the Methods section and the Results prose. If a reader can't understand the figure from the legend, the figure fails peer review regardless of how pretty it is.

### 10. Statistical reporting in legend (mandatory whenever statistical inference is shown)

Every figure with a statistical test, error bars, or group comparison must state in the legend:

- **`n = X` per group/condition** — exact number, not a range
- **`n` definition** — what `n` represents and sample independence where applicable. Examples by field: biology — "3 biological replicates (animals), 5 technical replicates each"; ML/physics — "10 independent random seeds"; psychology/HCI — "24 subjects, 40 trials each"; clinical — "50 patients, 1 scan each"
- **Statistical test name** — e.g., "one-way ANOVA with Tukey HSD post-hoc correction", "paired t-test", "Wilcoxon signed-rank"
- **Error bar type** — SEM, SD, or 95% CI. "Error bars" alone is not enough
- **Center value** — mean, median, or geometric mean
- **p-value convention** — prefer exact values (`p = 0.003`); if using asterisks, the legend must define them (`*p < 0.05, **p < 0.01, ***p < 0.001`)

Missing any one of these is the single most common figure-related reviewer flag at top-tier journals.

### 11. Raw data visibility — no dynamite plots

For distributions or group comparisons, **show individual data points overlaid on summary statistics** whenever sample size permits (violin + strip, box + jitter, raincloud, strip plot with mean line). Bar chart of mean + error whisker alone ("dynamite plot") is the #1 flagged visualization anti-pattern in top-journal review (eLife: Ten common statistical mistakes). The rule of thumb: overlay raw points when N per group ≤ 50; above that overlay becomes illegible and summary statistics are acceptable.

## Journal Export Gate

<HARD-GATE>
Before calling `savefig()` (or equivalent), confirm the target journal's requirements from `docs/references/figure-guide.md`. If unknown, ask the user.
</HARD-GATE>

Inline summary (full table in `docs/references/figure-guide.md`):

| Journal family | 1-col width | 2-col width | Font | Font size | DPI (raster) | Preferred format |
|---|---|---|---|---|---|---|
| Nature family | 89mm | 183mm | Arial/Helvetica | 5-7pt | 300+ | PDF/AI/EPS for vector; TIFF/PNG for raster |
| Science family | 55mm | 115/180mm | Helvetica | 6-12pt | 300+ | PDF/EPS preferred |
| Cell family | 85mm | 174mm (full); 114mm (1.5-col) | Arial/Helvetica | 6-8pt | 300+ | PDF preferred; EPS/TIFF accepted |
| JAMA / NEJM | 3.375" | 6.75" | Arial | 7-9pt | 300+ | EPS/PDF; TIFF for raster |
| IEEE Transactions | 3.5" (88.9mm) | 7.16" (182mm) | Times/Helvetica | 8pt min | 300+ | PDF/EPS |

## Per-Figure Workflow

For each figure, follow these steps in order:

### Step 1: State the purpose

"This figure shows [what] for [what purpose], to support [what claim]."

If you can't finish that sentence, you're not ready to plot. Ask the user.

### Step 2: Select the chart type

Use the Chart Type Selection Gate table. Write the choice in a comment at the top of the script: `# Chart type: horizontal bar (compare 5 models on r²)`.

### Step 3: Set the global style

At the top of the plotting script, call a style function that sets:
- Font family (sans-serif, Arial or Helvetica)
- TrueType embedding (`pdf.fonttype = 42`)
- Base font size (7pt for axis/ticks, 8pt for titles)
- Savefig DPI (600)
- Spine style (top and right off)
- Default palette (qualitative: Okabe-Ito; sequential: viridis)

See `docs/references/figure-guide.md` for a copy-paste-ready `apply_paper_style()` recipe.

### Step 4: Render

Write the plotting code. Use named color variables, not hex strings inline. Keep one figure per script (or one composite function per script).

### Step 5: Export

Call `savefig('figures/fig_name.pdf', bbox_inches='tight', pad_inches=0.02)`. If a raster version is needed, also save `.png` at 600 DPI.

### Step 6: Inline self-check

Before dispatching the reviewer, run through:
- [ ] Font is sans-serif (Arial/Helvetica) and embedded (TrueType)?
- [ ] All text ≥5pt?
- [ ] Palette is colorblind-safe (Okabe-Ito, viridis, or equivalent)?
- [ ] Every axis has a label with units?
- [ ] Every legend entry is readable without zooming?
- [ ] No 3D effects, gradients, or rainbow cmap?
- [ ] Top and right spines removed?
- [ ] Panel labels (if multi-panel) are lowercase bold top-left?
- [ ] Output is PDF or SVG (not JPEG)?
- [ ] Figure legend names `n`, statistical test, error bar type, and center value?
- [ ] Legend is interpretable without reading the main text?
- [ ] Sample independence clarified where applicable (biological vs technical replicates; independent vs repeated measures; subjects vs trials)?
- [ ] No dynamite plots when sample size permits raw overlay (N ≤ 50 per group)?
- [ ] Representative images labeled as such; quantified images state N?

### Step 7: Dispatch `figure-reviewer` subagent

Locate the reviewer prompt at `skills/figure-design/figure-reviewer-prompt.md`. Fill the placeholders:

- `{FIGURE_PATH}` — path to the output file (e.g., `figures/fig3.pdf`)
- `{SCRIPT_PATH}` — path to the generating script
- `{FIGURE_PURPOSE}` — one-sentence purpose from Step 1
- `{TARGET_JOURNAL}` — e.g., "Nature Communications"
- `{CAPTION_TEXT}` — the draft caption (if written), else "N/A"

Dispatch via Task tool (`general-purpose` subagent). Wait for `Status: Approved` or `Status: Issues Found`.

### Step 8: Act on feedback

- **`Status: Approved`** → move to the next figure or back to `manuscript-writing`
- **`Status: Issues Found`** → fix each issue in the script, re-render, re-dispatch the reviewer. Repeat until approved.

If the reviewer flags the same issue twice, escalate to the user.

### Step 9: Commit

Both the script (`.py`/`.R`/`.jl`) AND the output file (`.pdf`/`.svg`) go to git. The output file is a build artifact, but committing it protects against environment drift — the paper reader can see what the authors saw even if their TeX/matplotlib environment differs.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Default matplotlib style is fine for now" | Default is 100 DPI, bitmap fonts, blue axis labels. Journals silently reject; reviewers assume carelessness. Set the style upfront, not later. |
| "Viridis is overused, let me pick a prettier palette" | Viridis is perceptually uniform AND colorblind-safe. Pretty is irrelevant; the reader's job is to decode, not admire. |
| "I'll fix the typography later in Illustrator" | Manual edits break reproducibility (claims-audit fails). Anyone running the script should get the submitted figure byte-for-byte. Fix in the script. |
| "Pie chart is fine, it's only 3 categories" | Horizontal bar beats pie at any N. Humans compare lengths faster and more accurately than angles. |
| "The legend fits if I shrink it" | Sub-5pt text is unreadable in print. Move the legend outside the axes, split panels, or drop it entirely — never shrink below 5pt. |
| "Red vs green is intuitive for error/success" | 8% of men see them as the same color. Use blue/orange, add shape coding, or annotate directly. |
| "The figure looks fine on my screen" | Screens are 100-200 DPI RGB. Print is 300+ DPI CMYK. Always export to PDF and inspect at 100% zoom before declaring done. |
| "Journal guidelines are for final submission — draft can be loose" | Drafts become submissions through editorial inertia. Fixing typography at submission time is 10x the cost of setting a global style once. |
| "I'll just screenshot the Jupyter notebook output" | Screenshots are raster at screen DPI, no vector, no TrueType. Always save via `savefig('.pdf')`. |
| "The figure has to look exactly like a specific paper's visualization" | Mimicking an exemplar is fine; copying the exact palette, colorbar, and layout is not. Derive from principles, not from a specific paper's stylistic choices. |
| "n is in Methods — don't need it in the legend" | Reviewers read figure legends independently of Methods. Put `n` in BOTH. |
| "Bar chart of mean is standard practice" | It is — and it's the single most-flagged visualization anti-pattern in top-journal review (eLife top-10). Show the raw points. |
| "Asterisks for p-values are fine, everyone uses them" | Only if the legend defines them. `*p<0.05` alone is not enough; prefer exact values (`p = 0.003`). |
| "This is a representative image, obviously" | Not obvious to reviewers. Label it "representative of N independent experiments" or state the quantification N. |

## Red Flags — STOP

- Generating a figure inside a notebook cell with no saved script file
- Editing the output PDF manually in Illustrator or Inkscape
- Using `jet` / `rainbow` cmap for a sequential quantity
- Any text below 5pt in the figure
- 3D bar chart, 3D pie, gradient-filled categorical bars
- Red + green as the only two colors distinguishing categories
- Axis without a label
- Legend overlapping data points or error bars
- Panel labels in a different font from the tick labels
- Saving as `.jpg` or a screenshot-based format
- "I'll clean it up before submission" (no — clean it up now)
- Legend missing `n`, statistical test, or error bar definition
- Bar chart of mean values with no raw data overlay (dynamite plot) when N per group ≤ 50
- Image panel without "representative of N" label or quantification N stated

## Orthogonality with `claims-audit`

`figure-design` and `claims-audit` Part B (Figure Integrity) are orthogonal and both run:

| Concern | Owned by |
|---|---|
| Does the generating script exist? | `claims-audit` |
| Is the output reproducible from the script? | `claims-audit` |
| Are the plotted numbers traceable to a results file? | `claims-audit` |
| Is the chart type appropriate for the data and purpose? | `figure-design` |
| Is the typography readable and embedded correctly? | `figure-design` |
| Is the palette colorblind-safe? | `figure-design` |
| Does the figure match journal export specs? | `figure-design` |

A figure can pass one and fail the other. Both must pass for submission-readiness.

## Integration

- **Called by:** `eureka:using-eureka` when figure creation intent is detected; `eureka:manuscript-writing` when Results section cites a figure
- **Prerequisite:** data exists + analysis complete (a figure has nothing to show otherwise)
- **Invokes:** `figure-reviewer` subagent (per figure, after rendering)
- **Pairs with:** `eureka:claims-audit` (integrity) — orthogonal, both run before submission
- **Reference:** `docs/references/figure-guide.md` (for journal-specific specs, palette hex codes, matplotlib style recipe, accessibility tools, chart-type flowchart)

## Skill Type

**FLEXIBLE** — Chart type, palette choice, and journal target adapt to the user's field, data, and venue. The iron laws (colorblind-safe palette, 5pt font floor, TrueType embedding, no chart junk, vector export, script-generated only) are fixed.
