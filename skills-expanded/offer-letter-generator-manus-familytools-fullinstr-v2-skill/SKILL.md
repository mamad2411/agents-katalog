---
name: offer-letter-generator-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for offer-letter-generator using latest full-instruction v2 family injection.
allowed-tools:
  - docx_extract_placeholders
  - docx_fill_template
  - docx_metadata
  - docx_preview_text
  - list_dir
  - read_file
  - read_json
  - run_python
  - run_shell
  - write_file
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Offer Letter Generator

## When to use this skill
Use this skill for `offer-letter-generator` tasks to generate an offer letter by filling placeholders in a Word template (`.docx`) with data from a JSON file. It handles conditional sections like relocation packages.

## Visible input and artifact inventory
Visible files:
- `instruction.md`: Task instructions.
- `environment/offer_letter_template.docx`: Word template with placeholders (e.g., `{{CANDIDATE_FULL_NAME}}`) and conditional markers (e.g., `{{IF_RELOCATION}}...{{END_IF_RELOCATION}}`).
- `environment/employee_data.json`: JSON data for placeholders.
- `task.toml`: Task config.
- `environment/Dockerfile`: Environment setup.

Output artifact: A filled Word document, usually at `/root/offer_letter_filled.docx`.

## Execution procedure for the current task
1. **Inventory**: Read `instruction.md` for requirements and output path. Use `list_dir` to verify files.
2. **Extract Data**: Use `read_json` on `employee_data.json` to get candidate info, noting conditionals like `RELOCATION_PACKAGE`.
3. **Analyze Template**: Use `docx_extract_placeholders` on the template to find placeholders and conditional markers.
4. **Prepare Data**: Map placeholders to JSON values. Decide to keep or remove conditional sections based on data (e.g., if `RELOCATION_PACKAGE` is "Yes", keep content but remove markers).
5. **Fill Template**: Use `docx_fill_template` to generate the document. Use a custom Python script if the tool fails complex conditional removal.
6. **Verify**: Use `docx_preview_text` to ensure placeholders are replaced and conditionals handled.

## Family tool routing and useful placeholder snippets
- **`read_json`**: Extract data from `employee_data.json`.
- **`docx_extract_placeholders`**: List template placeholders.
- **`docx_fill_template`**: Generate the output document.
- **`docx_preview_text`**: Verify output without downloading.
- **`run_python`**: Use with `python-docx` if `docx_fill_template` cannot handle `{{IF_RELOCATION}}` logic.

## Validation checks before final submission
- **File Existence**: Ensure output exists at the specified path.
- **Placeholder Check**: No raw placeholders (e.g., `{{CANDIDATE_FULL_NAME}}`) remain.
- **Conditional Logic**: Markers (e.g., `{{IF_RELOCATION}}`) are removed. Content is present/absent correctly.
- **Data Accuracy**: Cross-check preview text against JSON data.

## Common failure modes and repair actions
- **Failure**: Output file not at correct path.
  - **Repair**: Check `instruction.md` and ensure the tool/script saves there.
- **Failure**: Placeholders remain.
  - **Repair**: Ensure mapping keys match extracted placeholders exactly.
- **Failure**: Conditional markers visible or wrong content.
  - **Repair**: Write a Python script using `python-docx` to manually process paragraphs and markers.

## A finalizer capsule for restoring the minimum required artifact or answer shape near max-step
If near max-step and conditional logic fails, use a basic Python script to perform simple string replacements for standard fields and save to the required path. This ensures an artifact is produced in the correct format and location.
