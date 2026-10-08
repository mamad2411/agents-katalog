# AGENTS.md

GitHub Action for HTTP requests powered by unjs/ofetch.

## Status

- Implemented: input parsing, body assembly (raw/multipart/octet-stream), request
  building (auth, query, retry, timeout), run orchestration (pass/fail, outputs),
  action entry + metadata, full unit + integration tests, CI (checks + self-test).
- Inputs use native ofetch naming. Outputs: `response`, `headers`, `status`, `requestError`.
- `requestError` is emitted only when the step actually fails.
- Resolves http-request-action issues #182 (JSON passthrough), #226 (octet-stream
  headers), #120 (array of files per field).

## Conventions

- Runtime deps (`ofetch`, `@actions/core`) live in `devDependencies` so obuild
  inlines them; `dist/` is committed and the action runs `dist/index.mjs`.
- Keep this file updated with project status.
- Tooling: obuild (rolldown), vitest, oxlint, oxfmt, tsgo. No CLI.
