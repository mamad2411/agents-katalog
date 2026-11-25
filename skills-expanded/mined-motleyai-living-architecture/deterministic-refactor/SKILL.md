---
name: deterministic-refactor
description: Use to rename or move a module/class/function/method/attribute (Python or TypeScript) and update all imports/references, with a deterministic check that nothing was missed. Mutator = dr-refactor; the guarantee = dr-typecheck + dr-mock-lint + the test suite. Only sound on a compliant target (see docs/deterministic-refactoring.md).
---

**Preflight:** run `dr-doctor --plugin <this skill's base directory> --require-config` once per session before using any `dr-*` command. If it reports the missing-config finding (the one naming `/dr:init`), run the fast path of the `dr:init` skill, then re-run this preflight; stop and show the user its output on anything it still reports, or on any other failure.

# Deterministic refactor

The mutator is best-effort — no tool reliably rewrites every annotated
`obj.attr`, `super()` call, and override. The **type-check gate is the
guarantee**, and it is only sound on code that meets the compliance conditions
(`docs/deterministic-refactoring.md`). If the blast radius is not typed, run `dr:make-refactor-target-compliant`
first.

The file's language decides the mutator and its idioms: read
`<this skill's base directory>/../../languages/<language>.md` for each language
the refactor touches (`dr-config get languages` lists the repo's).

## Procedure

1. **Name the symbols**: each by its file and its path inside it
   (`--file F --symbol Class.method`; also `func.<locals>.inner`,
   `Class.method(param)`, `Alias['value']` for a `Literal` member). Related
   renames go in one rename map: one dry-run, one apply, one gate.
2. **Check the verifier**: run `dr-typecheck`. It runs the project's type
   checker in the project env (the one the tests use) against its committed
   baseline, and it must pass before you start. If it prints "nothing to
   check", STOP and tell the user: with no type check there is no guarantee,
   so offer to set one up (`commands.typecheck` and
   `dr-typecheck --write-baseline`) first.
3. **Type the receivers** (member renames):
   `dr-compliance --select attr-blindspot,string-blindspot --attr OLD <repo>` (one `--attr` per
   old name) lists each receiver the checker cannot type. Type them
   (`dr:make-refactor-target-compliant`) until it reports nothing; `dr-refactor`
   refuses a member rename while any remain.
4. **Dry-run** (default):
   `dr-refactor --project <repo> rename --file F --symbol Q --new-name N --docs`,
   or `dr-refactor --project <repo> rename-map MAP --docs`.
   Method renames rename the hierarchy by default. Re-run until it is the rename you want:
   - `stand-in`: a class outside the hierarchy declares `OLD`. `--with PATH:LINE` renames it too
     (a duck-typed implementation: a cache, a fake, a `cast()` target); `--without PATH:LINE` leaves it
     (an unrelated class). To give it a different new name, add it to the map as its own entry.
     Pytest fixtures are left by default.
   - `attr-blindspot` or `string-blindspot` on a receiver that cannot be typed (a third-party `Any`): `--allow-blindspots`,
     and tell the user which.
   - `unlinked-keyword`: a call keyword `OLD=` the checker cannot link to the renamed parameter or field (a
     decorator that erases the signature, a `**kwargs` helper that copies its dict or passes it on). Read each
     listed call and the helper it reaches: `--unsure include --allow-blindspots` renames the keywords,
     `--allow-blindspots` alone leaves them. Neither changes a key the helper reads by its old name, so fix
     those by hand. Tell the user which.
   - a site that must keep the old name (a back-compat test or shim): `--keep PATH:LINE`, or
     `--keep PATH` for a whole file.
   - a `leftover` mention that does name the renamed symbol (an untyped document body, a docstring two
     map entries reach): `--docs-pick PATH:LINE` rewrites the mentions listed on that line; add `=ENTRY`
     where two entries rename that word to different names.
   - a literal that must keep its old keys (a versioned stored document): `--keep-literal KEY` leaves
     every dict or object literal holding that key.
   - code still using the back-compat alias of an earlier rename: a `retarget` entry moves it to
     the new name and keeps the alias.
   Show the diff.
5. **Apply**: `--apply` is a GLOBAL flag and goes before the subcommand
   (`dr-refactor --project <repo> --apply rename ...`); trailing it errors.
   It realigns the type-check baseline too; never edit the baseline by hand.
6. **GATE — done only when ALL pass:**
   - `dr-typecheck` passes: **no new errors** vs the baseline;
   - `dr-mock-lint <tests>` passes; when the base branch already has findings,
     `dr-mock-lint --base <base-branch> <tests>` reports only the new ones;
   - the full non-integration test suite (`dr-config get commands.test`) passes;
   - by hand, only these: each `leftover` and `unverified-read` line the apply printed, each receiver and keyword
     `--allow-blindspots` let through, and the string-only references the language doc lists.
7. Review the diff. The user commits — never commit or `git add -A`.

## Commands

`dr-refactor` subcommands: `rename` / `rename-map` / `generate-map` / `retarget` / `move-symbol` /
`move-module`. Dry-run is default; `--apply` writes, baseline included;
`--timings` (also before the subcommand) prints each phase's wall time on stderr;
`--project` defaults to cwd. Locator: `--symbol Q` (the path inside `--file`,
quoted for the shell: `'f.<locals>.g'`, `'C.m(p)'`, `"Alias['value']"`; no match
or several exit 2 listing the candidates), `--line [--col]` (1-based)
or `--offset N` (0-based). A `rename` given `--file` a module and no locator, or a Python `rename` located on
an import that names a module, renames the module: its file (a Python package's directory) moves beside itself, a
TypeScript module keeping its extension (`--new-name` is the new stem), and every import follows, while
`move-module` only moves a module into an existing package under its own name. `--stub REMOVAL` (Python) leaves a
stub at the old path from the repo's `refactor.python.moved_module_stub`. `rename-map MAP` reads a YAML list of
`{file, symbol, new_name}`, `{file, symbol, retarget}` or `{module, new_name}` entries
(paths relative to `--project`), resolves every entry before renaming any (so entries may chain or swap names), and writes all or nothing. `retarget --file F --symbol OLD --target NEW` rewrites what resolves to
the alias `OLD` to name `NEW`, its target declared or imported in the same class or
module, imports `NEW` where a file lacks it, and leaves `OLD` and its re-exports in
place. `rename`, `rename-map` and `retarget` also take `--with` /
`--without PATH:LINE`, `--keep PATH[:LINE]` (site paths relative to `--project`), `--allow-blindspots` and `--docs`
(comments, docstrings, strings and prose files: qualified mentions everywhere;
code-marked ones in the declaring files where the class owning the mention has
the renamed member, or outside such a class where every declaration of the name
in the file is renamed to one name; the rest listed as `leftover`, as are
declarations whose name contains the old name). `rename` and `rename-map` also
take `--docs-pick PATH:LINE[=ENTRY]` (rewrite the mentions listed on that line)
and `--keep-literal KEY` (leave every dict or object literal holding that key).
A string matching a pattern of the repo's `refactor.string_forms` is respelled
with a renamed class or module-level symbol, with or without `--docs`. Move destinations must already
exist, and a `move-symbol` destination is a file of the same language. Run the
repo's formatter afterwards.

A vocabulary rename (one word replaced across the repo) starts from a word table.
`dr-refactor --project <repo> generate-map TABLE > MAP` writes one entry per declaration and
module whose name holds a word (`words: [{from, to}]`, one row per inflection). `carve_outs`
(`{words, annotated | paths | symbols}`) leave out a declaration where the word keeps its old sense, and
`entries` holds hand-written map entries, kept on every regeneration. Change the table and regenerate;
never edit MAP by hand. Pass the table to the rename as `--words TABLE`: carved stand-ins are left and
carved `--docs` mentions are listed as `leftover`. A map entry
`{file, symbol: '*.<locals>.NAME', new_name}` renames every local of that name in the file.
