# slice_generator

## WHEN TO USE

Use when more bounded markdown slice specs are needed.

## INPUTS

- `templates/COMPACT_SLICE_TEMPLATE.md`
- `docs/00_PERSONAL_TOOL_DOCTRINE.md`
- `docs/03_DRIFT_BOUNDARIES.md`
- `reference/PROJECT_CONTEXT_SUMMARY.md`
- short user goal

## ALLOWED WORK

- Generate small markdown slice files.
- Include objective, allowed files, forbidden work, validation, final report, and stop condition.

## FORBIDDEN WORK

- Do not implement the slice.
- Do not create broad tasks.
- Do not generate runtime/orchestration slices for the current phase.
- Do not ask for unnecessary reviews.

## OUTPUT FORMAT

One compact `slices/SLICE_*.md` file per small task.

## STOP CONDITION

Stop after generating the requested slice specs.
