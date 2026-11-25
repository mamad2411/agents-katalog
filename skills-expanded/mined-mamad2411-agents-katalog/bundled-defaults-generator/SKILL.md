---
name: bundled-defaults-generator
description: Inline source-text via JSON-escaped string literals at build time (with `--check` mode) so compiled Bun binaries and Node can both load them.
category: bun
version: 1.0.0
version_origin: extracted
tags: [bun, codegen, compile, bundled-defaults, validation]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
---

# Bundled Defaults Generator (JSON-Escaped Inline Literals + `--check`)

## When to use

- You ship a CLI that bundles a set of template / default files (commands, workflows, SQL seeds, example YAML) that must be readable even when there is no filesystem alongside the binary (compiled `bun build --compile`, Deno compile, pkg).
- You want the same module to load **both** in dev (TypeScript source) and in Node (no Bun-specific import attributes).
- You want CI to fail loudly if someone edited a source file but forgot to regenerate the bundle.

Bun supports `import X from './file.yaml' with { type: 'text' }`, but this attribute is Bun-specific and breaks the module on Node. Inlining as `JSON.stringify(content)` string literals keeps portability.

## Steps

1. **Define a generator script** (`scripts/generate-bundled-defaults.ts`) that:
   - Reads every eligible file from one or more source dirs (e.g. `.archon/commands/defaults/*.md`).
   - Validates filenames (reject non-kebab-case, reject name collisions across extensions, reject empty files).
   - **Sorts entries before emission** (`localeCompare`) so output is deterministic for git diffs and `--check`.
   - Normalizes line endings to LF (`replace(/\r\n/g, '\n')`) so Windows `core.autocrlf=true` checkouts don't cause drift.
2. **Emit a single `*.generated.ts` file** with a header warning ("AUTO-GENERATED — DO NOT EDIT") and one or more `Record<string, string>` exports:

   ```ts
   export const BUNDLED_COMMANDS: Record<string, string> = {
     "archon-assist": "…JSON-escaped text…",
     "archon-review": "…JSON-escaped text…",
   };
   ```

3. **Support `--check` mode.** Regenerate into memory, read the committed file (LF-normalized), compare. If different, print a clear error and `process.exit(2)`. `0` = up-to-date, `1` = unexpected error, `2` = stale. Distinct exit codes let CI distinguish "broken generator" from "forgot to regenerate."
4. **Wire it into `bun run validate`** so `check:bundled` runs alongside type-check, lint, format, and tests. One broken auto-regen breaks the commit.
5. **Document the explicit regen command** in the project's `CLAUDE.md` / `CONTRIBUTING.md`: "After adding/editing a default file, run `bun run generate:bundled`."

## Counter / Caveats

- `JSON.stringify` escapes non-ASCII as `\uXXXX`, producing large files. For binary assets or >MB text, use base64 in a separate artifact instead.
- Don't try to import the generated file dynamically with a computed path — it should be a **static** import so the bundler inlines it. Dynamic `import()` may silently revert to filesystem resolution in dev.
- If you also have a `bundled-defaults.ts` (non-generated) that wraps the generated record with a runtime `isBinaryBuild()` check, keep the generated file limited to the raw Record; mix only in the hand-written wrapper.

## Evidence

- `scripts/generate-bundled-defaults.ts` (179 lines): complete generator with `--check`, LF normalization, kebab-case filename validation, collision detection, deterministic sort, distinct exit codes.
- `packages/workflows/src/defaults/bundled-defaults.generated.ts`: the emitted artifact (two `Record<string, string>` exports).
- `packages/workflows/src/defaults/bundled-defaults.ts`:23-41: runtime wrapper that reads `BUNDLED_IS_BINARY` from `@archon/paths` to decide whether to use the bundle or the filesystem.
- Root `CLAUDE.md`:717: "After adding, removing, or editing a default file, run `bun run generate:bundled`. `bun run validate` (and CI) run `check:bundled`."
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
