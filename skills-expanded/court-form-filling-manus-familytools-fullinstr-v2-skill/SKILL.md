---
name: court-form-filling-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for court-form-filling using latest full-instruction v2 family injection.
allowed-tools:
  - date_normalize
  - list_dir
  - pdf_extract_text
  - pdf_field_value_dump
  - pdf_fill_form_fields
  - pdf_list_form_fields
  - pdf_render_pages
  - read_file
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

# Skill: Court Form Filling

## When to use this skill
Apply this skill for `court-form-filling` tasks in SkillLearnBench. The goal is to fill a legal PDF form (e.g., California Small Claims) based on a case description, mapping facts to fields and saving to a specific path.

## Visible input and artifact inventory
- **Inputs:** Task instruction (case facts, constraints like date formats), blank PDF form (e.g., `/root/sc100-blank.pdf`), and config files (`instruction.md`, `task.toml`).
- **Artifacts:** A filled PDF form saved to the exact path requested (e.g., `/root/sc100-filled.pdf`).

## Execution procedure for the current task
1. **Inventory:** Read the instruction and locate the blank PDF and required output path.
2. **Discovery:** Run `pdf_list_form_fields` on the blank PDF to get exact field names.
3. **Mapping:** Extract facts (names, addresses, amounts, dates) from the instruction. Map them to discovered fields. Leave unmentioned or court-only fields empty.
4. **Transformation:** Format dates as requested (e.g., `xxxx-xx-xx`) using `date_normalize`.
5. **Filling:** Use `pdf_fill_form_fields` to populate the PDF and save it to the target path.
6. **Verification:** Run `pdf_field_value_dump` on the output PDF to verify filled values.

## Family tool routing and useful placeholder snippets
Prefer family-specific tools over ad hoc shell scripts:
- `pdf_list_form_fields`: Discover field names.
- `pdf_fill_form_fields`: Generate the artifact.
- `pdf_field_value_dump`: Verify contents.
- `date_normalize`: Format dates.

*Snippet:*
```python
# Map extracted facts to discovered fields
fields = {"Plaintiff_Name": "Extracted Name", "Claim_Amount": "1500"}
# Use pdf_fill_form_fields(input_pdf, output_pdf, fields)
```

## Validation checks before final submission
- **Path:** Ensure the filled PDF exists at the exact requested output path.
- **Content:** Check `pdf_field_value_dump` output to confirm facts are correctly mapped.
- **Constraints:** Verify date formats and ensure unmentioned fields remain blank.

## Common failure modes and repair actions
- **Bad Field Names:** If filling fails, re-run `pdf_list_form_fields` to correct the mapping keys.
- **Format Mismatch:** If dates are wrong, review the instruction and reformat before filling.
- **Overfilling:** If court fields are filled, clear their mapping and regenerate the PDF.

## Finalizer capsule
If near the step limit without a perfect artifact:
1. Extract the most critical facts (Plaintiff, Defendant, Amount).
2. Map them to the most obvious fields found via `pdf_list_form_fields`.
3. Run `pdf_fill_form_fields` to create the file at the required path. A partially correct file at the right path is better than none.
