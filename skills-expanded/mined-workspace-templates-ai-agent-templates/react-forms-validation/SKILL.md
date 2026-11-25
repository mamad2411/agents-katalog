---
name: react-forms-validation
description: Builds accessible React forms with schema validation, clear error messages and safe submit handling against double sends and server errors.
---

# React forms validation

One schema, real labels, honest errors, and a submit button that cannot be abused.

## Steps

1. Define the schema once with Zod or the project's validator, and export its inferred type. Use it on the client and in the server handler so the rules cannot drift.
2. Pick the form tool the project already uses (React Hook Form with a resolver, or Actions with `useActionState`). Use uncontrolled inputs by default for speed.
3. Markup rules for every field: a visible `<label for>`, the correct `type` and `autocomplete` (`email`, `new-password`, `one-time-code`), `inputmode` for numbers, and `required` only where the schema requires it.
4. Errors: validate on blur, then on change after the first error. Render the message under the field, connect it with `aria-describedby`, set `aria-invalid`, and on failed submit move focus to the first invalid field. Add a summary with a polite live region for long forms. Messages say what to do ("Use at least 12 characters"), not what failed ("Invalid").
5. Submit: disable the button while pending but keep it focusable-safe by showing a spinner label, guard against double submit, and send an idempotency key for payments.
6. Map server errors back to fields by name; show a form-level message for the rest. Never lose the user's input on error.
7. Test with Testing Library: user-event typing, error text found by role, submit with valid and invalid data.

## Rules

- Never trust client validation; the server validates again.
- Do not clear passwords or card fields on server errors without telling the user.
- No labels that exist only as hint text.

## Report

Fields, rules, accessibility attributes added and tests written.
