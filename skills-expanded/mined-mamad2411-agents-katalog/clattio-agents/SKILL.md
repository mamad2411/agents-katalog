# AGENTS.md

## Purpose

This repository has a generated CLI surface and a hand-written agent skill.
Several files must be updated together to avoid drift.

## Edit-in-unison invariants

### 1. Attio API surface ↔ generated code ↔ CLI ↔ skill docs

These layers describe the same command surface and must stay aligned:

1. `scripts/generate.ts`
2. `src/codegen/normalize.ts`
3. `src/generated/manifest.gen.ts`
4. `src/generated/sdk.gen.ts` and the rest of `src/generated/`
5. `src/cli.ts`
6. `README.md`
7. `skills/clattio/SKILL.md`
8. `skills/clattio/references/api-surface.md`

If the Attio OpenAPI spec changes, or if you change normalization logic in
`src/codegen/normalize.ts`, then you must:

- run `bun run generate`
- run `bun run build`
- run `bun run test`
- inspect `node dist/attio.js --help`
- update the skill docs if command groups, command names, body shapes, or
  recommended workflows changed

### 2. `skills/clattio/SKILL.md` ↔ `skills/clattio/references/api-surface.md`

These two files are intentionally split into:

- a concise operational playbook in `SKILL.md`
- a detailed command reference in `references/api-surface.md`

Keep them synchronized:

- Resource vocabulary must match: object, attribute, record, list, entry,
  note, comment, thread, task, meeting, call recording, transcript, file,
  webhook, workspace member.
- If a command group is added, renamed, or removed, update both files.
- If command-selection guidance changes in `SKILL.md`, make sure the detailed
  reference still supports it.
- If `api-surface.md` gains or loses top-level sections, update its table of
  contents.
- `SKILL.md` should keep explicit links to `references/api-surface.md` wherever
  deeper lookup is expected.

### 3. Manifest shape ↔ CLI option handling

`src/manifest-types.ts`, `src/codegen/normalize.ts`, `src/io.ts`, and
`src/cli.ts` are tightly coupled.

Examples:

- If you add a new parameter type in `manifest-types.ts`, update parsing and
  option wiring in `src/cli.ts` and any input-building logic in `src/io.ts`.
- If you change how multipart or JSON bodies are represented in the manifest,
  update both the normalizer and the CLI execution path.
- If command naming logic changes in `normalize.ts`, review the skill docs and
  README examples because user-facing command names may change.

### 4. Version invariants

The version in `package.json` and the `VERSION` constant in `src/cli.ts` must
match before release.

### 5. README ↔ actual auth flow

If you change authentication behavior in `src/auth.ts`, also review:

- `README.md`
- `skills/clattio/SKILL.md`
- any tests covering auth behavior

The token setup flow, OAuth setup flow, and user-facing command examples must
stay consistent.

## Safe workflow for CLI surface changes

When changing anything that affects commands or flags:

1. Edit source files.
2. Regenerate if needed: `bun run generate`
3. Build: `bun run build`
4. Test: `bun run test`
5. Spot-check help output: `node dist/attio.js --help`
6. Update README and skill docs in the same change.

## Safe workflow for skill-only changes

If the CLI does not change and you are only improving the skill:

- update `skills/clattio/SKILL.md`
- update `skills/clattio/references/api-surface.md` if the main skill now
  points to sections that need more detail
- keep examples and terminology consistent with the real CLI help output
