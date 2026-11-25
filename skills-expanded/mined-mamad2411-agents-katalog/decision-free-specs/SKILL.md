---
name: decision-free-specs
description: Write decision-free refactor specs/plans that a local small model (e.g. Qwen3.6-27B) can execute mechanically. Use when asked to plan a refactor for small-model execution, "make specs for X", or to set up/extend a specs/ program in a repo. Language-agnostic core; per-language inventory tools in languages/ (TypeScript, Python, Rust, Flutter/Dart).
---

# Decision-free refactor specs

Produce `specs/<target>/spec.md` + `plan.md` pairs that a ~27B local model executes
with **zero architectural decisions**. The expensive part of planning — knowing
exactly what is in each file — is a script, not a reading job. The planning model
(you) spends tokens only on judgment: pattern choice, interface tables,
trap-spotting.

The workflow below is language-agnostic. Everything language-specific (inventory
tooling, extraction procedures, recovery rules, traps) is a plug-in:

| Language | Status | Tooling |
|---|---|---|
| TypeScript / TSX | available | `languages/typescript/` |
| Python | available | `languages/python/` |
| Rust | available | `languages/rust/` |
| Flutter / Dart | available | `languages/dart/` |

Before planning, read `languages/<lang>/NOTES.md` for the target language. The
Python/Rust/Dart tools are fixture-validated (plus a CPython stdlib file for
Python); on first production use in a new codebase, hand-check one real file
against the inventory output. For a language with no plug-in, build the inventory
tool first (contract and procedure in `languages/README.md`) — do not fall back to
reading files manually; that recreates the cost this skill exists to remove.

## Step 0 — program bootstrap (first use in a repo only)

If the repo has no `specs/README.md` + `specs/conventions.md`, create them from
`templates/program-readme-example.md` and `templates/conventions-example.md`,
adapting: the verification commands for THIS repo, the import/module-path table for
THIS language (from the language NOTES), and the executor prompt template's repo
root. The program README owns the executor contract (prompt template, sampling
settings, one-step-per-session rule, failure protocol) — per-spec folders never
restate it.

## Step 1 — inventory by script (do NOT read the files first)

Run the target language's inventory tool from the repo root; it emits the contract
sections (`languages/README.md`): imports, the exhaustive top-level declarations
table (kind/name/lines/exported), language-specific signals (e.g. hooks, API call
sites, dynamic string-built identifiers), and — critically — **which other files
import the module and what names they import** (load-bearing exports needing
compatibility re-exports; this is how a test file importing three helpers was
caught in the first production run).

Only read source directly for the specific blocks you intend to extract into new
units (to write accurate interface tables) — never for symbol discovery.

## Step 2 — decide the architecture (this is YOUR job, record every decision)

Pattern menu, in order of preference:

1. **Model extraction** (always): pure types/constants/helpers → a model module.
2. **Leaf unit moves**: nested functions/components/widgets → own files. Verbatim.
3. **Block extraction** (UI panels, large match arms): only with a full interface
   table (props/params); the language's compiler-driven recovery rule covers
   misses mechanically.
4. **Strategy registry**: ONLY for ≥2-way *behavioral* variance (different fields,
   different validation, different request shapes). Labels and styling variants
   are NOT behavioral variance.
5. **Shared extraction**: if the inventory shows the same symbol duplicated across
   files, dedupe it in the FIRST plan that runs and mark the dependency in the
   program table.

Record negative decisions explicitly in spec.md ("No Strategy registry — X is the
only variance; do not create one", "the drawers stay inline by decision"). An
unrecorded non-decision is a decision the executor will make badly.

## Step 3 — write the documents

Per target folder:

- **spec.md**: source file + size, pattern + why, target file tree, **exhaustive
  symbol map table** (symbol → destination → exported), interface tables for any
  block extraction, dependency notes (exact import/module paths per the language
  NOTES), acceptance criteria. If the inventory's "Imported by" section is
  non-empty for moved exports, specify a compatibility re-export and name the
  importer.
- **plan.md**: prerequisites (cross-plan dependencies by name + step), numbered
  steps each small enough for one fresh-context session, exact commit message per
  step. Steps only state what differs from the repo's `specs/conventions.md`.

Hard rules learned in production:

- Order steps: pure moves first, unit moves second, block extraction last —
  every step independently committable, repo green between steps.
- Title every step `STEP k of N` and state N in the plan's preamble. In the first
  production run the executor stopped after step 1 of 3 on the hardest target and
  reported the whole plan complete; the step header is what makes "there are more
  steps" visible inside a fresh-context session.
- End every move-step with a **leftover check**: the exact count of symbols moved,
  plus a mechanical assertion that none of their declarations remain in the source
  file (the language NOTES give the grep shape). A 27-symbol move list silently
  lost one symbol in production; the compiler can't catch a type that still
  compiles where it was left.
- Anchor on **symbol names**, never line numbers (they drift).
- Every "if X then ask/choose" in a draft plan is a bug. Replace it with either a
  decision made now, or a mechanical rule ("copy version A and report the
  difference — do not reconcile").
- Verification gates per step come from the repo's conventions (format →
  typecheck/build → any co-located tests). If the target has a co-located test
  file, name it in the plan — its imports are exactly the compatibility surface.

## Step 4 — update the program and commit

1. Add rows to the program README's table (size, difficulty, dependencies).
2. Spot-check load-bearing claims the specs rely on (duplicated symbols, importer
   lists) — the script reports them, but confirm anything a plan's correctness
   hinges on.
3. Commit per the repo's conventions.

## Step 5 — audit the executor's output (do not trust "all done")

The exact commit messages in the plans double as a completion manifest. When the
executor (or its operator) reports the program finished, diff expectation against
reality before believing it:

```bash
grep -A2 "Commit message" specs/*/plan.md   # expected messages
git log --format=%s <baseline>..HEAD        # actual messages
```

Every expected message must appear, one commit each. Production failure modes this
catches: steps silently skipped (the executor stopped early on the hardest target),
and two steps squashed into one commit (the work existed but the per-step
verification gates never ran for the squashed step — re-verify those by hand).
Then run the full verification suite once at program level, including test files
near refactored code that the per-step gates didn't name.

## Executor settings (defaults; the program README is authoritative per repo)

Target class: local ~27B instruct model (Qwen3.6-27B preferred for agentic-coding
strength). Temperature 0.2, top_p 0.9 — mechanical edits want determinism. One step
per fresh-context session. Two failures on a step → reset the working tree, report
FAILED with the error, stop. Never improvise around a failing step.
