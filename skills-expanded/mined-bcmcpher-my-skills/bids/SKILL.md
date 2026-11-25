---
name: bids
description: >
  Load BIDS (Brain Imaging Data Structure) conventions into context. Auto-invoke
  when the user is working with neuroimaging files, asks about BIDS naming or
  structure, mentions entities like sub/ses/task/run, asks about JSON sidecars
  for MRI/fMRI/DWI/EEG/MEG/PET, or references a bids/ dataset directory.
  Use when validating filenames, suggesting sidecar fields, or organizing data.
argument-hint: [datatype, path, or question]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash
---

# Skill: bids

Load and apply Brain Imaging Data Structure (BIDS) conventions when working
with neuroimaging datasets. Use the reference files below to answer questions,
validate filenames, suggest sidecar metadata, and guide dataset organization.

## References

- Entity ordering and filename patterns: `${CLAUDE_PLUGIN_ROOT}/references/entities.md`
- Datatype directories, suffixes, and dataset-level files: `${CLAUDE_PLUGIN_ROOT}/references/datatypes.md`
- JSON sidecar required and recommended fields per modality: `${CLAUDE_PLUGIN_ROOT}/references/sidecars.md`

Load the relevant reference(s) before answering. Load all three when the question
spans multiple aspects of the spec.

## Steps

1. Read the relevant reference file(s) to ground your answer in the spec.
2. Identify the datatype involved (anat, func, dwi, fmap, perf, eeg, ieeg, meg, pet, beh, micr).
3. If the user asks to validate a dataset or check compliance:
   a. Determine the dataset root path. If $ARGUMENTS contains a path use it;
      otherwise ask the user.
   b. Run: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh <dataset-path>`
      To override the BIDS schema version (2.x only):
      `BIDS_SCHEMA=/path/to/schema.json bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh <dataset-path>`
      or: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh <dataset-path> --schema <path-or-url>`
   c. Interpret the output — explain each error/warning using the references,
      state which spec rule was violated, and suggest the corrected filename or
      sidecar field.
   d. If the script reports "bids-validator not found", inform the user of the
      installation steps from the README. Note that the fallback structural check
      ran instead; it checks for required dataset files and entity/suffix validity
      but does not validate sidecar JSON content. The recommended install is
      `pip install bids-validator-deno` (2.x, Deno bundled).
4. If validating or constructing a filename without running the validator:
   - Confirm required entities are present (`sub` always; `task` for func/beh/eeg/meg).
   - Confirm entities appear in canonical order from the entity table.
   - Confirm label values are alphanumeric only (no hyphens, no underscores).
   - Confirm the suffix is valid for the datatype.
5. If advising on sidecar JSON:
   - Note that sidecars inherit from higher to lower levels: dataset-level → subject-level →
     session-level → run-level. Only recommend fields not already covered by a parent sidecar
     to avoid redundancy.
   - List REQUIRED fields first; note which are missing.
   - Then list STRONGLY RECOMMENDED fields for that modality.
   - For field maps, always check that `IntendedFor` is present and paths are
     relative to the subject directory.
6. If the user asks about dataset structure, confirm dataset-level required files
   (`dataset_description.json`, `README`, `participants.tsv`) exist or should exist.
   Note that `scans.tsv` (per-subject scan log) is recommended for flagging bad scans.
6b. If a `func` datatype is present or described, check for corresponding `_events.tsv`
   files (one per task run). These are required for all functional task data and follow
   the same entity pattern as the BOLD file but with the `_events.tsv` suffix.
7. When working with derivatives, remind the user that derivatives live under
   `derivatives/<pipeline>/` outside the raw BIDS root, and use `desc` and
   `space` entities to distinguish processed variants.
8. If $ARGUMENTS is provided, treat it as the dataset path, datatype, filename,
   or question to focus on.

## Constraints

- Always cite entity order by position number from the entity table, not from memory.
- Never invent suffixes or entities not listed in the references.
- Always distinguish REQUIRED vs RECOMMENDED vs OPTIONAL fields in sidecars.
- Never assume a label value is valid if it contains hyphens or underscores —
  flag it as a violation.
- When a filename violates the spec, explain the specific rule broken and provide
  a corrected example.
- For ambiguous modality questions, ask which datatype/suffix the user is working
  with before advising.
