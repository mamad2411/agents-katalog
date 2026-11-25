---
name: "dataweave-guidelines"
description: "DataWeave 2.0 transformation guidance for MuleSoft: modular mappings, typed inputs/outputs, null-safety, reuse via modules, and testing. Use when writing DataWeave transforms."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# DataWeave 2.0 Guidelines

- Put reusable functions/mappings in `*.dwl` modules under `src/main/resources/dw`; `import` them.
- Declare `%dw 2.0` + explicit `output application/json` (or target type); set `input` types where known.
- Null-safety: use `default`, `?`, and `if (x != null)`; avoid NPE on optional fields.
- Prefer pure functions; no side effects. Use `map`/`filter`/`reduce`/`groupBy` over imperative loops.
- Keep transforms small and composable; one transform per concern.
- Test transforms with MUnit (assert payload equality against fixtures).
- Preserve the legacy contract exactly when modernizing AS-IS (field names, formats, date patterns).
