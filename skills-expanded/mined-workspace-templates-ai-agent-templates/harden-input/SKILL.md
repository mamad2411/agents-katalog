---
name: harden-input
description: Adds validation and sanitization to the inputs of one named handler and writes tests that throw bad data at it.
disable-model-invocation: true
---

Harden the inputs of this handler: $ARGUMENTS

1. Find the handler and list every external input it reads: body fields, query string, path params, headers, cookies, uploaded files.
2. Use the validation library the project already has (zod, joi, pydantic, class-validator, Bean Validation, go-playground/validator). If none exists, ask before adding a dependency.
3. Define a strict schema: exact types, min and max lengths, numeric ranges, enums for fixed choices, regex for ids and emails, a size cap for bodies and files. Reject unknown fields.
4. Escape or encode on output, and use parameterized queries. Never strip characters as a substitute for validation.
5. Return a 400 with field-level messages that do not echo raw input.
6. Add tests next to the existing ones for: missing fields, wrong types, empty strings, 10 MB strings, null bytes, SQL and HTML payloads, and negative or huge numbers. Run them.

Show the diff and test results, list any input you left unchecked and why, and ask before committing.
