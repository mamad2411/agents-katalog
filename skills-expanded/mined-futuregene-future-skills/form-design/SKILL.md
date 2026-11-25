---
name: form-design
description: Design a form end to end — single-column layout, label and helper-text placement, input-type selection by data type, validation timing and error placement, multi-step structure and accessible labelling. Use when the artifact is a form, checkout, signup or data-entry flow.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Form Design

Reduce abandonment, prevent errors and keep data collection effortless — from one field to a long
multi-step flow. 中文触发：表单设计、字段校验时机、错误提示位置、多步流程。

## Layout
- **Single column** — almost always correct; two columns disrupt reading flow and blur field order
- **Field width reflects expected input length**: a postcode field is narrow, a bio field is wide
- **Top-aligned labels** — fastest to scan, resilient to long labels; never placeholder-only
- **Group related fields** by proximity and section headings; do not run a long form as one
  undifferentiated column

## Labels and instructions
- Every field has a persistent label (placeholders disappear on input and fail accessibility)
- Labels concise, sentence case, no ALL CAPS
- Helper text goes below the label, above the field: "Format: DD/MM/YYYY"
- Mark **optional**, not required, when most fields are required
- Show character counts whenever a limit exists, not only near the limit

## Input type by data type

| Data type | Input type |
|---|---|
| Short text | Text input |
| Long text | Textarea with visible resize |
| One from few options (≤5) | Radio buttons, all visible |
| One from many options (6+) | Select / combobox |
| Multiple from few options | Checkboxes |
| Date | Date picker or segmented inputs (day/month/year) — never freeform text |
| Phone / card numbers | Formatted input with masking |
| Password | Password input with show/hide toggle |

## Validation
- **Validate on blur**, not on every keystroke — real-time validation while typing is distracting
- **Error placement**: directly below the field, not at the top of the form
- **Error text**: say what is wrong and how to fix it — "Email address must include @" not "Invalid email"
- **Success indication**: subtle checkmark only where correctness is non-obvious (password strength,
  username availability)
- **Server-side errors**: inline to the field when possible; summarised at the top when several
  fields are affected

## Multi-step forms
- Show progress as a step indicator, not only "Step 2 of 5"
- Each step is completable as a unit — related questions together
- Back navigation must not lose data
- Auto-save or explicit "save and continue" for long forms
- Confirm before discarding partial input

## Accessibility
- Programmatic label for every field (`<label for>` or `aria-label`)
- Errors associated with their field (`aria-describedby`)
- Focus order matches visual order
- Error summary at top is keyboard-focusable and links to each field
- Never colour alone for required or error state

## Working rules
- Remove every optional field you can; fewer fields means higher completion
- Default to the most common answer where one exists; do not default to blank for binary choices
- Test with real users entering real data — synthetic data hides length and format edge cases
- Measure field-level abandonment; that is where optimisation pays
- High-stakes forms (payments, medical, legal) get a review step before submission
