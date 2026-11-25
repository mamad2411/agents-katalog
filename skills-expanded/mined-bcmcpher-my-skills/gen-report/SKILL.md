---
name: gen-report
description: User has completed or planned a statistical analysis and wants to scaffold
  a jupytext report notebook with standard sections, QC diagnostic plots, model summary
  tables, and result figures. Use this skill whenever the user wants to start writing
  up results, needs a notebook template for a statistical analysis, or wants to turn
  plan-analysis model hierarchy output into a reportable format. Also invoke when the
  user asks for an analysis notebook, report script, or structured write-up.
argument-hint: [analysis type or title]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Skill: gen-report

Scaffold a jupytext-compatible report file with standard analysis sections, method-
appropriate QC diagnostic plot cells, and a model sequence stub. The output is a
plain-text script (`.py` percent format by default) that converts to a runnable
Jupyter notebook with `jupytext --to notebook <file>`.

Reference files (load as directed):
- `${CLAUDE_PLUGIN_ROOT}/references/jupytext-config.md` — pairing formats, header
  block, conversion commands, editor setup
- `${CLAUDE_PLUGIN_ROOT}/references/report-sections.md` — section templates and
  cell content guidance
- `${CLAUDE_PLUGIN_ROOT}/../../references/qc-metrics.md` — must-run
  diagnostic plots per method family (load in Phase 2)

---

## Phase 0: Intake

Parse from `$ARGUMENTS` where possible. Ask only for what is missing.

1. **Analysis title** — a short descriptive name for the report file.

2. **Method family** — what kind of analysis is being reported?
   - If the user ran `/plan-analysis` and has a model hierarchy, ask them to paste
     it or point to the output file — you will pre-fill the model stubs from it.
   - If not, ask which method family: ANOVA/regression/mixed effects/logistic/
     CCA/EFA — one of the families from `test-selection.md`.

3. **Language** — Python (default), R, or Julia.

4. **Output path** — where to write the report script. Default: same directory as
   `merged.tsv` (if known), named `report_<title_snake_case>.py`.

---

## Phase 1: Load context

Load `${CLAUDE_PLUGIN_ROOT}/references/jupytext-config.md` to confirm the correct
header format for the chosen language.

Load `${CLAUDE_PLUGIN_ROOT}/references/report-sections.md` to get the section
templates and cell content guidance.

If the user provided a plan-analysis output or model hierarchy, read it to extract:
- The model formula at each level (null → covariates → main effects → interaction)
- The comparison test (F-test, LRT, etc.)
- The statistical family (used to select QC plots in Phase 2)

---

## Phase 2: Select method-appropriate QC cells

Load `${CLAUDE_PLUGIN_ROOT}/../../references/qc-metrics.md`.

Locate the row for the user's method family in the "Diagnostic plots quick-reference"
table at the bottom of the file. Then pull the full code blocks for each listed plot
from the body of `qc-metrics.md`. These become the Section 2 cells in the output.

If the user chose Python, use the Python code blocks. If R, use R blocks. If Julia,
note that Julia diagnostic coverage is limited and fall back to Python or R.

---

## Phase 3: Write the report file

Assemble and write a single report file using:
- The jupytext header from `jupytext-config.md`
- Section templates from `report-sections.md`
- QC cells from Phase 2
- Model stubs from Phase 0 (user-provided hierarchy or method-labelled placeholders)

### Section 3 (Models) stub population

If the user provided a plan-analysis hierarchy, fill in the actual model formulas:
```python
# %% 3a — Null model
m0 = smf.ols("fa_l_af ~ 1", data=df).fit()
# %% 3b — Covariates
m1 = smf.ols("fa_l_af ~ age + C(site)", data=df).fit()
# etc.
```

If no hierarchy was provided, use clearly-labelled placeholders:
```python
# %% 3a — Null model     [replace with your formula]
m0 = smf.ols("outcome ~ 1", data=df).fit()
```

### Output filename convention
`report_<title_snake_case>.<ext>` where ext is `.py`, `.R`, or `.jl`.

After writing, tell the user:
1. The path to the written file
2. The conversion command to get a notebook:
   `jupytext --to notebook <file>` then `jupyter lab <file>.ipynb`
3. Which QC sections were pre-populated vs left as placeholders
4. A reminder: "Fill in the OUTPUT_DIR path and data column names in Section 0
   before running."

---

## Constraints

- **Never modify input data files.** The report file is the only thing written.
- **Always include all six sections**, even if some are mostly placeholder. A
  partial template with clear TODO comments is more useful than a short file that
  omits the results section.
- **QC cells should be specific to the method**, not generic. The reader should
  understand immediately which assumption is being checked and what a red flag
  looks like.
- **Prefer method-specific figure types** in Section 5 rather than a generic
  scatter plot. The `report-sections.md` table lists the recommended figure type
  per method family.
- **If the user's language is Julia** and a required QC plot has no Julia template
  in `qc-metrics.md`, add a comment in the cell: `# No Julia template available
  for this plot — see the R or Python cell in qc-metrics.md` and include a prose
  description of what to look for.
