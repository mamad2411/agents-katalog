# CLAUDE.md

Instructions for AI coding agents and contributors working with this codebase.

## Project Overview

`hsize` is a TypeScript/Bun library for converting between raw byte counts and human-readable sizes.
It provides:

- Formatting (`format`) with SI/IEC/JEDEC systems
- Parsing (`parse`) from strings to bytes
- Polymorphic main function (`hsize`) that formats numbers and parses strings
- Chainable unit arithmetic (`HSizeUnit`)
- Comparison and range helpers (`gt`, `eq`, `between`, `formatRange`, etc.)
- Aggregation helpers (`sum`, `average`, `median`)
- Percentage and diff helpers (`percent`, `percentOf`, `remaining`, `diff`)
- Rate helpers (`formatRate`, `parseRate`)
- Natural language parser (`parseNatural`)
- Factory/custom units (`create`)
- CLI (`hsize` binary from `dist/cli.mjs`)

Core deterministic math is implemented with `decimal.js` through local wrappers in `src/decimal.ts`.

## Runtime, Tooling, and Build

- Runtime/package manager: Bun
- Language: TypeScript (strict)
- Bundler: `tsdown`
- Lint/format: Ultracite (`bun ultracite check`, `bun ultracite fix`)
- Typecheck: `tsc --noEmit`

Key scripts from `package.json`:

- `bun run build` -> build ESM + d.ts into `dist/`
- `bun test` -> run all tests
- `bun run lint` -> formatting + lint checks
- `bun run format` -> auto-fix formatting/lint issues
- `bun run typecheck` -> static type check
- `bun run prepublishOnly` -> lint + typecheck + build

## Repository Layout

- `src/index.ts`
  - Public entrypoint; exports all runtime APIs and types.
- `src/cli.ts`
  - CLI argument parsing and command execution.
- `src/types.ts`
  - Public/shared type definitions.
- `src/constants.ts`
  - Unit tables, regexes, defaults.
- `src/decimal.ts`
  - Decimal wrappers and cached power helpers.
- `src/utils.ts`
  - Number formatting/parsing internals, rounding, byte resolution.

Primary domain modules:

- `src/format.ts` -> bytes -> formatted output
- `src/parse.ts` -> string/number/bigint -> bytes
- `src/unit.ts` -> chainable `HSizeUnit`
- `src/factory.ts` -> configurable instances, custom unit systems
- `src/rate.ts` -> rates (`/s`, `/min`, `/h`, `bps`)
- `src/aggregate.ts` -> `sum`, `average`, `median`
- `src/compare.ts` -> `gt`, `lt`, `eq`, `between`, `min`, `max`
- `src/diff.ts` -> signed deltas and percentage change
- `src/percentage.ts` -> percentage calculations
- `src/range.ts` -> range formatting
- `src/approximate.ts` -> fuzzy output (`~`, `almost`, `just over`)
- `src/extract.ts` -> regex extraction from free text
- `src/natural.ts` -> natural-language parser
- `src/validators.ts` -> `isBytes`, `isUnit`, `isParsable`
- `src/partial.ts` -> partially applied formatter helper
- `src/clamp.ts` -> min/max clamping
- `src/presets.ts` -> opinionated format presets

Tests:

- `tests/*.test.ts` with one module-focused test file per major feature plus integration and CLI tests.

## Core Behavioral Invariants

When making changes, preserve these invariants unless intentionally changing behavior (and update docs/tests):

1. Formatting defaults to IEC (`KiB`, `MiB`, ...).
2. Parsing ambiguous uppercase JEDEC-style units (`KB`, `MB`, ...) defaults to 1024-based behavior, controlled by `ParseOptions.iec`.
3. Parsing lowercase `kB`/`kb` remains SI-oriented (1000-based), while IEC-prefixed forms (`KiB`, `Kib`) remain 1024-based.
4. `parse` behavior:
   - Non-strict invalid input -> `NaN`
   - Strict invalid input -> throws `TypeError`
5. Overflow parse handling for numeric strings:
   - Non-strict overflow -> `NaN`
   - Strict overflow -> throws `TypeError`
6. BigInt handling:
   - `parse(bigint)` keeps its warn/strict behavior for precision-loss cases.
   - Number-space helper APIs reject out-of-safe-range `bigint` with `RangeError` to avoid silent precision corruption.
7. `parseRate` bit semantics:
   - unit suffix lowercase `b` => bits
   - unit suffix uppercase `B` => bytes
8. Public APIs should remain side-effect free except expected warnings/errors and CLI I/O.

## High-Risk Areas (Read Before Editing)

- `src/parse.ts` and `src/format.ts`:
  - Many modules depend on these core semantics.
  - Small changes can cascade into broad behavior differences.
- `src/constants.ts` regexes and unit maps:
  - Shared across parse/extract/validators.
  - Changes must be verified with targeted tests.
- BigInt conversions across helper modules:
  - Avoid direct `Number(bigint)` in number-space code paths.
  - Prefer centralized utility methods in `src/utils.ts`.
- CLI behavior (`src/cli.ts`):
  - Keep UX and exit codes stable.

## Testing Expectations

For any non-trivial change:

1. Add or update focused unit tests in the corresponding `tests/*` file.
2. Run full test suite: `bun test`.
3. Run typecheck: `bun run typecheck`.
4. Run lint: `bun run lint`.

Suggested test mapping:

- parse/format internals -> `tests/parse.test.ts`, `tests/format.test.ts`, `tests/internals.test.ts`, `tests/parse-internals.test.ts`
- rate behavior -> `tests/rate.test.ts`
- BigInt safety in helpers -> `tests/compare.test.ts`, `tests/diff.test.ts`, `tests/percentage.test.ts`, `tests/clamp.test.ts`, `tests/range.test.ts`, `tests/aggregate.test.ts`, `tests/factory.test.ts`, `tests/approximate.test.ts`
- CLI output/exit behavior -> `tests/cli.test.ts`

## Documentation Expectations

When behavior changes:

- Update `README.md` examples and semantics notes.
- Add/update release notes in `CHANGELOG.md`.
- Keep examples consistent with current implementation and tests.

## Release and Packaging Notes

- Publish artifacts come from `dist/` only.
- Do not hand-edit `dist/`; regenerate with `bun run build`.
- Entrypoints configured in `tsdown.config.ts`:
  - `src/index.ts`
  - `src/cli.ts`

## Contributor Workflow

1. Make minimal, focused changes.
2. Keep API compatibility unless change is intentional and documented.
3. Prefer deterministic decimal helpers over native floating-point math in core logic.
4. Add regression tests for every bug fix.

## Source Code Reference

<!-- opensrc:start -->

### Source Code Reference

Source code for dependencies is available in `opensrc/` for deeper understanding of implementation details.

See `opensrc/sources.json` for the list of available packages and their versions.

Use this source code when you need to understand how a package works internally, not just its types/interface.

#### Fetching Additional Source Code

To fetch source code for a package or repository you need to understand, run:

```bash
npx opensrc <package>           # npm package (e.g., npx opensrc zod)
npx opensrc pypi:<package>      # Python package (e.g., npx opensrc pypi:requests)
npx opensrc crates:<package>    # Rust crate (e.g., npx opensrc crates:serde)
npx opensrc <owner>/<repo>      # GitHub repo (e.g., npx opensrc vercel/ai)
```

<!-- opensrc:end -->
