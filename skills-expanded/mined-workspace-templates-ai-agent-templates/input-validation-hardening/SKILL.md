---
name: input-validation-hardening
description: Adds allowlist validation where data enters your code and context-correct encoding where it leaves, closing injection paths at every trust boundary.
---

# Input validation hardening

Validate on the way in with allowlists. Encode on the way out for the exact context.

## Steps

1. List the trust boundaries: HTTP bodies, query strings, headers, cookies, uploaded files, webhooks, queue messages, environment and third-party API responses.
2. For each, check whether a schema runs before the data is used. Reuse the project's library (zod, joi, pydantic, class-validator, Bean Validation). Do not add a second one.
3. Write schemas that state: type, length range, character set or pattern, enum of allowed values, numeric bounds. Reject unknown fields. Prefer "must match" over "must not contain".
4. Validate on the server even when the client validates too.
5. Find sinks and match each to its defence:
   - SQL: parameters, never concatenation.
   - HTML: framework auto-escaping; no raw-HTML insertion without a sanitizer.
   - Shell: argument arrays, no shell string building.
   - File paths: resolve and confirm the result stays inside the base directory.
   - URLs for server-side fetches: allowlist hosts.
6. Return a generic 400 with field names, not internals.
7. Add tests with hostile inputs: empty, huge, wrong type, `'; --`, `<script>`, `../`, null bytes.

## Rules

- Never fix a vulnerability by blocklisting bad strings.
- Normalize before validating (trim, Unicode normalization), not after.
- Change one boundary at a time and keep the tests green.

## Report

Boundaries covered, schemas added, sinks fixed, tests added, and boundaries still open.
