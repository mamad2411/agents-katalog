---
name: merge-data
description: User has a folder of tabular data files (.csv/.tsv/.xlsx/etc.) and wants to inspect, merge, and combine them into a single analysis-ready dataframe with a runnable script. Use this skill whenever the user mentions merging, joining, or combining data files, wants to produce an analysis-ready dataset from multiple spreadsheets or data exports, or asks how to load and integrate a collection of tabular files.
argument-hint: [path/to/data/folder]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: merge-data

Discover, inspect, and merge a collection of tabular files into a single
analysis-ready dataframe. Produce a runnable Python (or R/Julia) script.
Source files are read-only — this skill never modifies them.

Once you are satisfied with the merged output, run `/gen-data-dict` to annotate
the variables and produce a BIDS data dictionary. Keeping these steps separate
means the dictionary is built from the final, stable column layout.

Reference files (load on demand):
- `${CLAUDE_PLUGIN_ROOT}/references/input-formats.md` — supported formats, read
  commands, delimiter/encoding detection heuristics
- `${CLAUDE_PLUGIN_ROOT}/references/merge-strategies.md` — join types, key-name
  patterns, wide/long detection, duplicate handling, validation checklist
- `${CLAUDE_PLUGIN_ROOT}/../../references/data-qc.md` — column profiling, missing-
  value normalization, type validation, duplicate detection, outlier flagging,
  cross-field consistency checks, and fuzzy key matching (Python/R/Julia)

---

## Phase 0: Discover and inventory files

1. Determine the target folder.
   - If `$ARGUMENTS` contains a path, use it.
   - Otherwise ask: "What folder contains your data files?"

2. Enumerate all files (including subdirectories):
   ```
   Bash: find <folder> -type f | sort
   ```

3. Filter to recognized tabular formats. Consult `input-formats.md` for the full
   extension list (`.csv`, `.tsv`, `.txt`, `.xlsx`, `.xls`, `.xlsm`, `.parquet`,
   `.feather`, `.h5`, `.hdf5`, `.json`, `.jsonl`). Note any unrecognized files.

4. Report the inventory to the user before doing anything else:
   - Total recognized file count grouped by extension
   - Full list of recognized files (relative path + extension)
   - Any skipped files and the reason (unrecognized extension, empty, etc.)

   Stop and report clearly if the folder is empty or contains no recognized files.
   Do not proceed.

---

## Phase 1: Inspect each recognized file

Load `${CLAUDE_PLUGIN_ROOT}/../../references/data-qc.md` for the full profiling and
QC patterns. Run the following for each file without modifying it:

1. **Row count** — `wc -l` for text formats; programmatic count for binary formats.
2. **Column headers** — read the first row only.
3. **Sample rows** — read 3–5 data rows to understand actual values.
4. **Column profile** — apply the profiling pattern from `data-qc.md §1` to get
   dtype, null fraction, cardinality, and sample values per column.
5. **Missing-value normalization** — apply `data-qc.md §2` to ensure blank strings,
   coded NAs ("-9", "Unknown", etc.), and sentinels are replaced with true nulls
   before inspecting further.
6. **Type validation** — apply `data-qc.md §3` to catch numeric data stored as
   strings or dates in inconsistent formats.
7. **Encoding and delimiter** — for text formats, apply the detection rules in
   `input-formats.md`.

Flag key-candidate columns immediately. A column is likely a merge key if its name
matches patterns from `merge-strategies.md` (subject ID, session, run, participant,
etc.) and it has low or zero nulls with cardinality close to the number of rows.
If a key candidate has < 100% coverage across files after an exact match, check
`data-qc.md §7` (fuzzy key matching) before concluding the keys are incompatible.

Produce a compact summary table for the user:

| File | Rows | Columns | Key candidate columns | QC flags |
|------|------|---------|----------------------|----------|

---

## Phase 2: Identify candidate merge keys and file structure

1. Find columns that appear in more than one file with the same or similar name.
   Cross-reference the key-name pattern list in `merge-strategies.md`.

2. Classify the file collection into one of two structures:

   **Case A — Multi-variable (join horizontally):** Files cover different
   measurement domains and share an index column. They should be joined.
   Evidence: different column names per file, similar row counts, a common key.

   **Case B — Subject-split (stack vertically first):** One file per subject
   (or subject × session), all with the same column layout. They should be
   concatenated, then optionally joined to a wide summary file.
   Evidence: repeating filename pattern (`sub-01_*.csv`), identical column sets,
   small row count per file.

3. If both structures are present (e.g., subject-split files that need stacking
   before joining to a demographics file), identify the two-step plan: stack → join.

4. Flag any file that has no detectable connection to the others. Do not guess how
   to include it.

---

## Phase 3: Confirm with the user before generating any code

Present a structured summary and **wait for explicit confirmation** before
delegating to merge-agent. The summary must address every item below.

A missing confirmation on any point means you do not proceed.

Present:

1. **Proposed merge keys** — which column(s) will be used to join the files, and
   which files share each key. If a key needs format normalization (e.g., BIDS
   prefix stripping), say so.

2. **Proposed join strategy** — inner / left / outer. Explain the trade-off in
   plain language:
   - Inner: only subjects present in every file are kept; rows may be silently dropped.
   - Left: all subjects in the base file are preserved; gaps in other files become NaN.
   - Outer: all subjects from any file are kept; maximizes data but maximizes NaN too.
   Ask the user which they prefer.

3. **Subject-split files** — if Case B was detected, list which files will be
   stacked and confirm the user agrees with that interpretation. Never assume
   subject-split without evidence.

4. **Ambiguous files** — if any file has no detectable join path, list it and ask:
   "I can't find a common key between [file] and the rest. Should I include it,
   and if so, on what column?"

5. **Language preference** — confirm Python (default), R, or Julia.

6. **Output path** — confirm where to write the script, or accept the default
   (same folder as the input data, named `merge_data.py`).

---

## Phase 4: Delegate to merge-agent

Once the user has confirmed all items in Phase 3, delegate to `merge-agent` with
the following context explicitly in the delegation message:

- Absolute paths to all input files
- Confirmed merge keys (column name + which files it appears in)
- Confirmed join strategy (inner / left / outer)
- Files to stack first (if Case B or mixed), in order
- Language (Python / R / Julia)
- Absolute path for the output script
- Any user corrections or overrides from Phase 3

merge-agent will re-inspect the files, apply variable typing, and generate the
runnable script with `--interactive` support. It returns the script path and a
summary.

---

## Phase 5: Verify and report output

After merge-agent returns:

1. Confirm the output script file was created at the expected path.
2. Run the script in non-interactive mode to verify it executes without error:
   ```
   Bash: python <script_path>      # or Rscript / julia
   ```
   Check that it prints a merge summary with shape and missing-value counts.
3. Report to the user:
   - Final dataframe shape (rows × columns)
   - Merge keys and join type applied
   - Rows lost (if inner join) or NaN columns introduced (if outer/left)
   - Path to the script
4. Suggest next steps: "When you're happy with the merged output, run
   `/gen-data-dict <path/to/merged.tsv>` to annotate variables and produce a
   BIDS data dictionary."

If the script fails to run, diagnose the error and either fix it directly or ask
merge-agent to revise. Do not ask the user to debug generated code themselves.

---

## Constraints

- **Never modify input files.** All reads are read-only. The only file written is
  the output script.
- **Never assume a merge key.** If the key is not confirmed in Phase 3, do not
  delegate. One wrong key silently corrupts the entire analysis.
- **Never assume subject-split structure.** Look for evidence (filename pattern,
  identical column sets) before treating files as a stack rather than a join.
- **Never silently drop files.** Every file in the inventory must be accounted for:
  merged, stacked, or explicitly excluded with a stated reason.
- **Always confirm language before generating code.** Python is the default but
  must be stated to the user.
- **Fix failures before reporting done.** If the generated script fails to run or
  produces malformed JSON, fix it or re-delegate — never deliver broken output.
