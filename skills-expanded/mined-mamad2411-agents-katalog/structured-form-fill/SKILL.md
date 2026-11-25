# Structured Form Fill

## When To Use

Use this skill when the task requires filling multiple related form fields before a final submit action.

Use it for structured data-entry tasks where the fields can be mapped before submission.

Do not use it for:

- open-ended text drafting or rich editing
- continuation-style revisions to an existing artifact
- tasks where submission is not part of the goal

## Procedure

1. Identify the relevant fields before typing.
2. Map each requested value to a specific input, select, or checkbox.
3. Fill fields one by one without submitting early.
4. Re-check required fields and validation messages before submission.
5. Submit only when all requested values are present and no obvious validation blocker remains.

## Required Evidence

- The field mapping for requested values
- Visible form state before submission
- Post-submit success or validation state

## Common Failures

- Pressing Enter too early in a multi-field form
- Filling the right value into the wrong field
- Submitting before required selections are made

## Verification

- Prefer deterministic verification through visible field values, selected options, and submit outcomes.

## Relevance

This is one of the most broadly reusable skills because multi-field forms are common across real sites.

Current strongest E2E targets:

- `tests/e2e/multi-step-form.test.ts`
- `tests/e2e/continuation-abandon-restart.test.ts`

Additional candidate targets:

- `tests/e2e/support-ticket.test.ts`
- `tests/e2e/login.test.ts`
