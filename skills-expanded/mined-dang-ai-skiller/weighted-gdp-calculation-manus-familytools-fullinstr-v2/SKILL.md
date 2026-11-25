---
name: weighted-gdp-calculation-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for weighted-gdp-calculation using latest full-instruction v2 family injection.
allowed-tools:
  - excel_formula_dump
  - excel_inspect_workbook
  - excel_read_range
  - excel_recalculate
  - excel_style_check
  - excel_write_formulas
  - list_dir
  - read_file
  - run_python
  - run_shell
  - weighted_gdp_calculate
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

# Skill: Weighted GDP Calculation

## 1. When to use this skill
Use this skill for tasks requiring the calculation of weighted means for economic indicators (e.g., net exports as a percentage of GDP or Trade Balance Coefficients) across countries like the GCC. The process involves reading source data from an Excel sheet, applying lookup functions based on multiple conditions, calculating derived metrics, and computing a final weighted mean using `SUMPRODUCT`. Strict preservation of original formatting and styles is required.

## 2. Visible input and artifact inventory
The primary input is an Excel workbook (e.g., `gdp.xlsx`) with "Task" and "Data" sheets. The `instruction.md` file details steps, cell ranges, and formatting requirements. The environment is defined by `task.toml` and `Dockerfile`. The expected artifact is the modified Excel workbook with required formulas in specified ranges, maintaining all original styles without added macros.

## 3. Execution procedure for the current task
First, inspect `instruction.md` for requirements like target ranges, functions (`VLOOKUP&MATCH`, `INDEX&MATCH`), and formatting (e.g., rounding to one decimal place). Use `excel_inspect_workbook` to analyze the Excel file structure. Employ `excel_read_range` to examine source data and target ranges.

Construct necessary formulas: lookups for data fetching, intermediate metrics, summary statistics, and the final `SUMPRODUCT` for the weighted mean. Apply these to the "Task" sheet using `excel_write_formulas`, preserving styles. Use `excel_recalculate` to evaluate formulas. Verify with `excel_formula_dump` and `excel_read_range`, and confirm style preservation with `excel_style_check`.

## 4. Family tool routing and useful placeholder snippets
- `excel_inspect_workbook`: Overview of sheets.
- `excel_read_range`: Read data ranges for verification.
- `excel_write_formulas`: Apply formulas. Example: `excel_write_formulas(workbook_path="gdp.xlsx", sheet_name="Task", updates={"H12": "=INDEX(Data!$A$21:$Z$40, MATCH($D12, Data!$D$21:$D$40, 0), MATCH(H$10, Data!$A$20:$Z$20, 0))"})`.
- `excel_recalculate`: Force recalculation.
- `excel_formula_dump`: Extract and verify formulas.
- `excel_style_check`: Ensure styles remain unchanged.
- `weighted_gdp_calculate`: Use if specifically provided, though standard tools are preferred.

## 5. Validation checks before final submission
Verify all required cells contain correct formulas (lookups, intermediate calculations, `SUMPRODUCT`). Check a sample of calculated values for expected logic and rounding (e.g., multiplying by 100 for percentage display). Confirm original formatting is unaltered and no unauthorized additions (macros, VBA) exist.

## 6. Common failure modes and repair actions
- **Incorrect Cell References:** Errors like `#N/A` or `#REF!`. Repair by adjusting absolute/relative references in formulas.
- **Style Alteration:** Ensure the formula writing tool preserves styles.
- **Rounding Issues:** Adjust formulas to include necessary multiplication and rounding functions if values don't match the required format.

## 7. Finalizer capsule
Perform a final review of the modified Excel workbook. Ensure all specified cell ranges in the "Task" sheet have correct formulas, the workbook is recalculated, and all original styles are intact. The final artifact must be the updated `gdp.xlsx` file at the original path.
