---
name: add-form-validation
description: Adds matching client and server validation to a form, with plain error messages that are announced to screen readers.
disable-model-invocation: true
---

Add validation to the form: $ARGUMENTS

1. Find the form, its submit handler and the endpoint that receives it. Detect the validation library already in use (zod, yup, valibot, Joi, class-validator, pydantic) and use it; add nothing new unless none exists.
2. List every field with its rule: required, type, length, format, range, and cross-field rules such as matching passwords. Show this list before coding.
3. Define one schema and use it on both sides. On the server, validate before any database write, return a 422 with `{ field, message }` pairs, and never trust client checks.
4. In the UI, validate on blur and on submit, show messages beside the field, link them with `aria-describedby`, set `aria-invalid`, and move focus to the first error. Do not clear user input on failure.
5. Messages say what to do ("Enter a date after today"), not what went wrong internally.
6. Add tests for one valid case and one failure per rule.

Run the tests. Report the rules added and any rule you were unsure about, and ask before changing database constraints.
