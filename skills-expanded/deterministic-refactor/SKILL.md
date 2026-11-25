---
name: deterministic-refactor
description: Use to rename or move a module/class/function/method/attribute (Python or TypeScript) and update all imports/references, with a deterministic check that nothing was missed. Mutator = dr-refactor; the guarantee = la-typecheck + dr-mock-lint + the test suite. Only sound on a compliant target (see docs/deterministic-refactoring.md).
---

**Preflight:** run `la-doctor --plugin <this skill's base directory> --require-config` once per session before using any `la-*` or `dr-*` command. If it reports the missing-config finding (the one naming `/la:init`), run the fast path of the `la:init` skill, then re-run this preflight; stop and show the user its output on anything it still reports, or on any other failure.

# Deterministic refactor

The mutator is best-effort — no tool reliably rewrites every annotated
`obj.attr`, `super()` call, and override. The **type-check gate is the
guarantee**, and it is only sound on code that meets the compliance conditions
(`docs/deterministic-refactoring.md`). If the blast radius is not typed, run `la:make-refactor-target-compliant`
first.

The file's language decides the mutator and its idioms: read
`<this skill's base directory>/../../languages/<language>.md` for each language
the refactor touches (`la-config get languages` lists the repo's).

## Procedure

1. Locate the symbol with the editor/LSP (not grep) → file, line, col.
2. **Check the verifier**: run `la-typecheck`. It runs the project's type
   checker in the project env (the one the tests use) against its committed
   baseline, and it must pass before you start. If it prints "nothing to
   check", STOP and tell the user: with no type check there is no guarantee,
   so offer to set one up (`commands.typecheck` and
   `la-typecheck --write-baseline`) first.
3. **Dry-run** (default):
   `dr-refactor --project <repo> rename --file F --line L --col C --new-name N`.
   Show the diff. Method renames rename the hierarchy by default.
4. **Apply**: `--apply` is a GLOBAL flag and goes before the subcommand
   (`dr-refactor --project <repo> --apply rename ...`); trailing it errors.
5. **GATE — done only when ALL pass:**
   - `la-typecheck` passes: **no new errors** vs the baseline (a missed
     annotated usage, `super()` call, or orphaned override surfaces here; the
     language doc lists the mutator's known misses);
   - `dr-mock-lint <tests>` passes;
   - the full non-integration test suite (`la-config get commands.test`) passes;
   - grep the string-only references no static tool sees (listed per language
     in the language doc).
6. Review the diff. The user commits — never commit or `git add -A`.

## Commands

`dr-refactor` subcommands: `rename` / `move-symbol` / `move-module`. Dry-run is
default; `--apply` writes; `--project` defaults to cwd. Locator: `--line [--col]`
(1-based), `--offset N` (0-based), or `--name` (first declaration, else first
use). Move destinations must already exist, and a `move-symbol` destination is
a file of the same language. Run the repo's formatter afterwards.
