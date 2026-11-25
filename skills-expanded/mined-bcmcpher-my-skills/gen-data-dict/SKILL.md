---
name: gen-data-dict
description: User has a merged or analysis-ready tabular file and wants to generate a BIDS-style JSON data dictionary that annotates every variable. Use this skill whenever the user asks to document, annotate, or describe the variables in a dataframe or TSV/CSV file, wants to create a data dictionary or codebook, or needs BIDS-compliant variable metadata for a merged dataset.
argument-hint: [path/to/merged.tsv]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Skill: gen-data-dict

Inspect a tabular file (typically the output of `/merge-data`), annotate each
variable with a BIDS-style description, and write a JSON data dictionary. The
input file is read-only. Run this skill after you are satisfied with the merged
dataframe — not before, since column names and types may still change.

---

## Phase 0: Locate the input file

1. If `$ARGUMENTS` contains a path, use it.
2. Otherwise, look for a `merged.tsv` in the current directory or ask:
   "What file should I build the dictionary for? (Usually `merged.tsv` from `/merge-data`)"

3. Confirm the file exists and is a supported tabular format (`.tsv`, `.csv`,
   `.parquet`, `.feather`, `.xlsx`). If not, report the issue clearly.

---

## Phase 1: Inspect all columns

Read the file and collect the following for each column:

1. **Name** (exact, case-sensitive)
2. **Dtype** as stored (object, int64, Int64, float64, bool, category, datetime)
3. **Cardinality** — unique value count and ratio to total rows
4. **Sample values** — up to 5 distinct values
5. **Null fraction** — fraction of rows with missing values

For text formats, detect delimiter and encoding before reading. For binary formats,
read the schema first, then a sample.

---

## Phase 2: Propose annotations for each column

For each column, draft a proposed annotation using these rules:

**Description:**
- Write a concise human-readable label.
- Expand recognizable domain acronyms:
  - Neuroimaging: `fa` → fractional anisotropy, `md` → mean diffusivity,
    `ad` → axial diffusivity, `rd` → radial diffusivity, `gm` → grey matter,
    `wm` → white matter, `csf` → cerebrospinal fluid, `roi` → region of interest
  - Psychiatry / cognition: `bprs` → Brief Psychiatric Rating Scale,
    `panss` → Positive and Negative Syndrome Scale, `iq` → intelligence quotient,
    `rt` → reaction time, `hit` → hit rate, `fa` (in cognition context) → false alarm
  - Demographics: `dob` → date of birth, `ses` → socioeconomic status (verify context)
- For opaque coded names (e.g., `x7b_v2`), leave Description as `""` and flag
  it to ask the user.

**Units:**
- Fill in when unambiguous: `"years"`, `"mm³"`, `"ms"`, `"z-score"`,
  `"unitless (0–1)"`, `"mm"`, `"Hz"`.
- Use `"n/a"` for identifiers, categoricals, booleans, and free-text columns.

**Levels** (for categorical / boolean columns only):
- Keys: the string representation of each unique value as it appears in the data.
- Values: human-readable labels. Propose labels based on context:
  - `M` / `F` → `"Male"` / `"Female"`
  - `HC` / `SZ` / `BD` → `"Healthy control"` / `"Schizophrenia spectrum"` / `"Bipolar disorder"`
  - `0` / `1` for a `passed_qc` column → `"Failed QC"` / `"Passed QC"`
  - Unknown codes → leave as `""` and flag for the user.

**LongName** (optional):
- Add when the column name is a short abbreviation and the full name is
  well-established (e.g., `bprs_total` → `"Brief Psychiatric Rating Scale, total score"`).

---

## Phase 3: Present proposed annotations and ask for confirmation

Show the user the proposed dictionary as a readable summary — not raw JSON.
Use a compact table format:

| Column | Dtype | Proposed Description | Units | Levels / Notes |
|--------|-------|----------------------|-------|----------------|
| subject_id | object | Participant identifier | n/a | — |
| age | Int64 | Age at time of assessment | years | — |
| diagnosis | category | Clinical diagnosis group | n/a | HC, SZ, BD |
| passed_qc | bool | Whether scan passed QC | n/a | true/false |
| fa_l_af | float64 | *(flagged — see below)* | — | — |

List flagged columns separately:
- Columns where Description is `""` (opaque names you couldn't decode)
- Columns where Levels values are `""` (coded values whose meaning is unclear)
- Any column where you are genuinely uncertain about units or interpretation

For each flagged column, ask a targeted question. Examples:
- "What does `fa_l_af` measure? Is it fractional anisotropy of the left arcuate
  fasciculus, or something else?"
- "For the `site` column, what do the codes `A`, `B`, `C` stand for?"
- "Is `age` measured in years at scan, years at consent, or something else?"

Incorporate the user's answers before writing the file.

---

## Phase 4: Write the data dictionary

Write a JSON file with one top-level key per column. Use this structure:

```json
{
  "subject_id": {
    "Description": "Participant identifier",
    "Units": "n/a"
  },
  "age": {
    "Description": "Age at time of assessment",
    "Units": "years"
  },
  "diagnosis": {
    "LongName": "Clinical diagnosis group",
    "Description": "Diagnostic category assigned at study intake",
    "Levels": {
      "HC": "Healthy control",
      "SZ": "Schizophrenia spectrum disorder",
      "BD": "Bipolar disorder"
    }
  },
  "passed_qc": {
    "Description": "Whether the scan passed quality control review",
    "Units": "n/a",
    "Levels": {
      "true":  "Passed QC",
      "false": "Failed QC or manually excluded"
    }
  },
  "fa_l_af": {
    "LongName": "Fractional anisotropy, left arcuate fasciculus",
    "Description": "Mean FA along the left arcuate fasciculus tract, derived from probabilistic tractography",
    "Units": "unitless (0–1)"
  }
}
```

Name the file `<input_stem>_data_dictionary.json` and place it in the same
directory as the input file. For example, `merged.tsv` → `merged_data_dictionary.json`.

---

## Phase 5: Report

After writing the file, tell the user:

1. Path to the written dictionary
2. Total number of variables annotated
3. Any Description or Levels fields still left as `""` that the user should
   fill in manually before submitting or sharing the dataset
4. A reminder: "Re-run `/gen-data-dict` if you modify the merged file and column
   names or types change."

---

## Constraints

- **Never modify the input data file.** Read-only.
- **Never leave a flagged column silent.** If you cannot interpret a column name
  or code, ask the user — do not guess and do not silently write `""`.
- **Always write the dictionary even if some fields remain blank.** A partial
  dictionary with clear TODOs is more useful than nothing.
- **Levels keys must match the actual data values exactly** — same case, same
  whitespace. A mismatch means the dictionary silently misrepresents the data.
