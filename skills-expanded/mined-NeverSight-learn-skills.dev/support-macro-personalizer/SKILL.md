---
name: support-macro-personalizer
description: Vendor-neutral skill to render customer support macros with variables, validate placeholders, and output ready-to-send drafts.
---

## When to invoke
- You use templated support responses (“macros”) and want consistent personalization.
- You want to ensure all required placeholders are filled before sending.

## Inputs needed
- `--macros_json`: JSON file with macros.
- `--context_json`: JSON file with variables (customer + ticket context).
- `--out_dir`: Output directory for rendered drafts.

Macro JSON format (reference implementation)
- `macros[]`:
  - `id` (string)
  - `subject_template` (string)
  - `body_template` (string)
  - `required_variables[]` (optional)

Context JSON format
- `variables`: object of string keys to string/number values.

## Workflow
1. Load macros and context variables.
2. For each macro:
   - Extract `{placeholders}` from subject/body.
   - Validate required variables:
     - `required_variables` must exist.
     - All placeholders must be resolvable (or be listed as optional via `--allow_missing`).
3. Render templates via safe substitution.
4. Emit one JSON draft per macro and a summary report.

## Output format
- For each macro: `<out_dir>/<id>.json` with:
  - `id`, `subject`, `body`, `missing_variables`.
- Summary printed to stdout.

## Guardrails
- Never execute code from templates.
- Treat unfilled placeholders as errors unless explicitly allowed.

## Reference code
- `support_macro_personalizer.py`
