---
name: r-methodology-narrator
description: >
  Translates R scripts into plain-language methodology narratives readable by
  domain experts who are not R programmers. Use this skill whenever a user
  pastes or uploads an R script and asks for a methodology description, plain
  language summary, expert review document, or non-technical explanation of what
  the code does. Also trigger when a user says things like "explain this script
  for a reviewer", "write up what this code does", "translate this R code into
  steps", or "my colleague needs to review this but can't read R". The output
  is a numbered methodology narrative formatted for use in Quarto or Word
  documents.
---

# R Methodology Narrator

Produces a plain-language, numbered methodology narrative from an R script,
suitable for review by a scientific domain expert who cannot read R code.

---

## Guiding Principles

- **Audience**: A domain expert (scientist, analyst, or subject matter expert)
  who understands the field but not R syntax. Never explain R functions by
  name. Instead, describe *what* they accomplish in plain language.
- **Tone**: Clear, precise, and professional — appropriate for a methods
  section of a technical report or scientific document.
- **Granularity**: Capture meaningful methodological steps, not individual
  lines of code. Group related lines into logical operations. Omit purely
  mechanical steps (loading libraries, setting file paths) unless they have
  methodological significance (e.g., a specific version dependency or a
  deliberate file structure choice).
- **Fidelity**: Do not infer intent beyond what the code supports. If
  something is ambiguous, note it explicitly as a point for the reviewer
  to confirm.
- **Calculation detail**: In sections that perform calculations, describe
  each operation in plain algebraic terms. Express formulas using plain
  language variables and standard symbols (×, ÷, +, −) rather than R
  syntax. For example: *"Estimated emissions = consumption × emission
  factor"*. Each distinct calculation should appear as its own sub-step
  or inline formula so a reviewer could reconstruct the arithmetic
  independently. For non-calculation sections (data loading, reshaping,
  filtering), maintain the higher-level grouping style.

---

## Process

### Step 1 — Parse the Script

Read the full script before writing anything. Identify:

- **Inputs**: What data sources, files, or parameters does the script consume?
- **Outputs**: What does the script produce — tables, files, model objects,
  plots?
- **Major phases**: Mentally segment the script into logical blocks (e.g.,
  data ingestion, cleaning/validation, calculation, aggregation, output).
  These will become the top-level numbered steps.
- **Key assumptions**: Hard-coded values, filter criteria, thresholds, or
  lookup tables embedded in the code that a reviewer should be aware of.
- **Ambiguities**: Places where intent is unclear or where multiple
  interpretations are possible.

### Step 2 — Draft the Narrative

Write a numbered list of methodology steps. Follow these rules:

1. **Number sequentially** from 1. Use sub-numbers (e.g., 2.1, 2.2) only
   when a major phase has distinct sub-steps worth calling out separately.
2. **Lead each step with a plain-language verb**: "Load", "Filter", "Calculate",
   "Join", "Apply", "Aggregate", "Export" — not R function names.
3. **Name the objects being acted on** in domain terms, not R variable names.
   E.g., "the equipment inventory table" not "`df_equip`".
4. **Call out parameters and assumptions explicitly**. If a filter threshold,
   emission factor, or reference year is hard-coded, state the value and flag
   it for reviewer confirmation.
5. **Note any iterative or recursive logic** in plain terms (e.g., "This step
   is repeated for each year in the study period").
6. **For calculation steps, express each operation algebraically** using plain
   variable names and standard symbols. Present as sub-steps when multiple
   distinct calculations occur in sequence. Example:
   - 6.1. Sector-partitioned imports = total imports × sector share
   - 6.2. Sector-partitioned exports = total exports × sector share
   - 6.3. Sector-partitioned production = total production × sector share
7. **Flag ambiguities** inline with a note: *[Reviewer note: please confirm
   whether X is intended here]*.

### Step 3 — Add a Preamble and Closing Summary

**Preamble** (before the numbered list): 2–4 sentences describing the overall
purpose of the script, its primary input(s), and its primary output(s).

**Closing summary** (after the numbered list): 2–3 sentences summarizing any
assumptions, limitations, or open questions the reviewer should pay particular
attention to.

### Step 4 — Format for Quarto / Word

Structure the output as clean markdown suitable for pasting into a `.qmd` file
or converting to Word via `pandoc` / `knitr`. Use:

- `##` for the document title (e.g., `## Methodology: [Script Name or Purpose]`)
- `###` for major phase headings if the script has clearly distinct phases
- Plain numbered list for steps (no markdown nesting beyond sub-numbers)
- `> Reviewer note:` blockquote style for flagged ambiguities or assumptions
  needing confirmation
- A horizontal rule (`---`) before the closing summary

Do **not** include R code blocks in the output. This document is for
non-coders.

---

## Output Template

```
## Methodology: [Brief description of script purpose]

[Preamble: 2–4 sentences on overall purpose, inputs, and outputs.]

### [Phase 1 Name, if applicable]

1. [Step description.]
2. [Step description.]
   2.1. [Sub-step if needed.]
   2.2. [Sub-step if needed.]

### [Phase 2 Name, if applicable]

3. [Step description.]

> **Reviewer note:** [Flag any assumption or ambiguity here.]

4. [Step description.]

---

**Summary and open questions:** [2–3 sentences on key assumptions,
limitations, or items requiring reviewer confirmation.]
```

---

## Handling Unknown Custom Functions

R scripts frequently call custom functions defined elsewhere — in a separate sourced file, an internal package, or earlier in the same script. When the narrative encounters a call to a custom function whose source code is not available in the provided script, apply the following rules:

### Tier 1 — Semantically transparent name
If the function name clearly implies its purpose (e.g., `calculate_emissions`, `apply_emission_factor`, `process_component`), a plain-language inference is acceptable. State what the function appears to do based on its name and its inputs/outputs, but flag it explicitly:

> **Reviewer note:** The function `[name]` is defined externally and was not available for review. The description above is inferred from its name and calling context. Please confirm this interpretation against the source definition.

### Tier 2 — Opaque name
If the function name does not imply its purpose (e.g., `run_step2`, `helper_fn`, `do_calc`), do not attempt a description. Instead, note only that a custom sub-routine is called, identify its inputs and outputs as visible from the calling script, and direct the reviewer to the source:

> **Reviewer note:** A custom function (`[name]`) is called here. Its internal logic was not available in this script. Please review its source definition separately before approving this methodology step.

### Tier 3 — Source file referenced
If the script contains a `source()` call that loads an external file, name that dependency explicitly in the preamble or in the relevant step:

*"This step calls a custom routine loaded from `[filename]`, which was not included in the materials reviewed."*

### General principle
Never silently absorb an unknown custom function into the narrative as if its behavior were confirmed. The goal is a methodology document a reviewer can trust — unverified inferences must always be visible as such.

---

## Notes on Common R Patterns

Translate these patterns into plain language without mentioning R:

| R pattern | Plain language |
|---|---|
| `left_join` / `merge` | "matched to" / "combined with [table] using [key]" |
| `filter` / `subset` | "restricted to records where [condition]" |
| `group_by` + `summarise` | "aggregated by [group variable], calculating [metric]" |
| `mutate` | "a new field was calculated as [description]" |
| `purrr::map` / `lapply` | "this process was repeated for each [element]" |
| `accumulate` | "applied cumulatively across [sequence], carrying forward prior values" |
| `pivot_wider` / `pivot_longer` | "restructured from [wide/long] to [long/wide] format" |
| `readxl::read_excel` / `read_csv` | "imported from [file type]" |
| `write_csv` / `openxlsx::write.xlsx` | "exported as [file type]" |
| `targets` pipeline | "each calculation step was run in sequence, with results cached for reproducibility" |
