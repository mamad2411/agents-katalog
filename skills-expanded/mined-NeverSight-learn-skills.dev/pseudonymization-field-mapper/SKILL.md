---
name: pseudonymization-field-mapper
description: Vendor-neutral skill to generate a consistent pseudonymization field map and implementation plan for datasets.
---

## When to invoke
- You need to share or analyze datasets while reducing re-identification risk.
- You need a clear, reviewable mapping from original fields to pseudonymized outputs.
- You are preparing a de-identified extract for analytics, QA, or vendor handoff.

## Inputs needed
- A JSON dataset schema describing fields (name, type, examples, sensitivity tags).
- Optional policy settings:
  - Whether mapping must be reversible (tokenization) or irreversible (hashing).
  - Join requirements (which identifiers must remain linkable across tables).
  - Environment (dev/test/prod) and key management constraints.

## Workflow
1. Parse schema and classify fields into categories: direct identifiers, quasi-identifiers, sensitive attributes, operational metadata.
2. For each field, choose a transformation:
   - drop, redact, generalize, hash, tokenize, mask, shift, bucket.
3. Ensure consistency constraints:
   - Stable linkage for join keys.
   - No derived direct identifiers (e.g., full name from first+last).
   - Date shifting coherence across related date fields.
4. Emit a pseudonymization plan with:
   - Per-field mapping (input -> output name, transformation, parameters).
   - Keying strategy notes (salt/pepper guidance; tokenization vault requirement).
   - Residual risk notes and review checklist.

## Output format
- JSON report containing:
  - `summary` with counts by category.
  - `field_map[]` list with transformation decisions.
  - `notes[]` for key management and joinability.

## Guardrails
- Do not output real secrets, salts, keys, or reversible mapping tables.
- Treat free-text fields as high risk; default to drop/redact unless explicitly allowed.
- Prefer irreversible approaches unless reversibility is explicitly required.

## Reference code
- `pseudonymization_field_mapper.py` reads a schema JSON and outputs a mapping plan JSON.
