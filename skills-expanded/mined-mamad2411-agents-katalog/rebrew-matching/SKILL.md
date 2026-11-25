---
name: rebrew-matching
description: >-
  Resolve stalled Rebrew byte matches with structural diffs, compiler flag sweeps, GA,
  statement/qualifier search, symbolic proving, and library flag overrides. Use after
  ordinary C edits stop improving a match; use rebrew-workflow for the initial edit/test
  loop.
license: MIT
---

```mermaid
graph TD
    Diff[Diff analysis<br/>rebrew diff --json] --> FixBlocker[Classify blockers<br/>rebrew diff --fix-blocker]
    FixBlocker --> Sensitive{flag_sensitive?<br/>structural similarity}
    Sensitive -->|yes| Sweep[Flag sweep<br/>rebrew match flags --tier &lt;tier&gt;]
    Sensitive -->|no| Ga[GA engine<br/>rebrew match run]
    Sweep -->|EXACT / RELOC| RoundTrip[Round-trip validation<br/>rebrew build round-trip --json]
    Sweep -->|still NEAR| Ga
    Ga -->|EXACT / RELOC| RoundTrip
    Ga -->|NEAR_MATCHING| Classify[Classify delta<br/>rebrew diagnose near --json]
    Classify -->|register / equivalent| Edit[C-level tweaks<br/>edit .c source]
    Edit --> Diff
    Classify -->|structural| Prove[Prove equivalence<br/>rebrew prove --watch-va]
    Prove -->|PROVEN| Held[Not spliced<br/>next test/verify records bytes]
    Prove -->|not proven| Edit
```

# Rebrew Matching

Deep dive into diff analysis and the GA engine.
For the overall reversing workflow, see the `rebrew-workflow` skill.

## When NOT to use this skill

- Picking which function to work on → use `rebrew-workflow` (`rebrew todo`)
- Generating skeletons / editing source / verifying STATUS → use `rebrew-workflow`
- `XX` rows or `missing_globals` hints (wrong or unresolved globals) → use `rebrew-data-analysis`

## 1. Diff Analysis (Always Start Here)

```bash
rebrew diff src/<target>/<file>.c --json         # structured diff + structural similarity
rebrew diff src/<target>/<file>.c --mismatches-only --json      # mismatches only (** lines)
rebrew diff src/<target>/<file>.c --register-aware --json      # register-aware (mark RR encoding diffs)
rebrew diff src/<target>/<file>.c --format csv   # CSV for spreadsheet analysis
rebrew diff 0x10009310 --json                    # resolve a VA directly (no .c path needed)
rebrew diagnose drift src/<target>/<file>.c --json        # localise branch-target drift windows
rebrew diagnose near src/<target>/<file>.c --json    # classify WHY it doesn't match (first-mismatch diagnosis)
rebrew diagnose gap src/<target>/<file>.c --json    # length-gap trace (short body? early table?) when scores stall flat
rebrew export objdiff --output objdiff.json                # GUI diffing project (objdiff) from target objects
```

`rebrew export objdiff` synthesizes one target COFF object per annotated source file
from the reference binary and writes an objdiff project config; open
`objdiff.json` in the objdiff GUI for instruction-level diffing of every
function at once (objdiff rebuilds base objects via `rebrew build objdiff-driver`).

> **VA on a multi-function file**: `rebrew diff/match/prove/test 0x<va>` targets the
> annotation whose VA matches, NOT the first function in the file. When the
> resolved file covers a different function than the VA, the tool errors out
> instead of silently diffing the wrong bytes.

### Diff Markers

- `==` identical bytes
- `~~` relocation difference (acceptable, counts as RELOC)
- `RR` register encoding difference (only with `-r` / `--register-aware`)
- `**` structural difference (needs fixing)
- `XX` invalid relocation difference (wrong target VA, counts as MISMATCH)

Relocations are resolved from the COFF object's symbols against the data catalog.
If the diff shows only `~~` lines, the function is already RELOC: `rebrew test` will promote it.

Exit codes: `0` = no structural differences (EXACT/RELOC), `1` = structural `**` lines
found (fix them), `2` = build error. With `--json`, read `summary.exact / summary.reloc /
summary.reg / summary.structural` instead of parsing lines.

### Auto-Classified Blockers

`rebrew diff` auto-classifies systemic compiler differences from `**` / `RR` lines
(e.g. "register allocation", "loop rotation / branch layout", "stack frame choice").
Use `--fix-blocker` to auto-write these to the `rebrew-functions.toml` metadata file:

```bash
rebrew diff --fix-blocker src/<target>/<file>.c        # auto-write BLOCKER to metadata file
rebrew diff --fix-blocker --json src/<target>/<file>.c # with JSON output
rebrew diagnose near src/<target>/<file>.c --fix-blocker   # BLOCKER from the near-miss classification
# Ad-hoc BLOCKERs that diff cannot classify (needs structs, SEH helper, etc.):
rebrew blocker set src/<target>/<file>.c "needs RE structs -- see rebrew types recover" --delta 3
rebrew blocker clear src/<target>/<file>.c
```

BLOCKER/BLOCKER_DELTA land in `rebrew-functions.toml` under `["<MODULE>.0x<VA>"]`.
When no structural diffs remain, `--fix-blocker` clears them.
`test`/`verify` keep that BLOCKER when the source still has `__asm`, `_asm`, or `__emit` (lint W020). This writer still clears a clean diff; do not use it to drop that note.
**Never hand-edit `rebrew-functions.toml` for BLOCKER: use `rebrew blocker set/clear` or the `--fix-blocker` writers.**

## 2. GA Engine (Single File)

For automated matching when manual tuning and diffs are insufficient:

```bash
rebrew match run src/<target>/<file>.c --generations 200 --pop-size 64 --jobs 16
```

Key flags: `-g/--generations` (default 100), `-p/--pop-size` (64), `-j/--jobs`,
`--seed`, `--seed-file`, `--no-seeds`, `--mutation-focus register|equivalent|structural|auto`,
`--seed-solved/--no-seed-solved`, `--output` (single-function only; default
`output/ga_runs`), `--compare-obj`, `--ignore-lint`, `--collect-pairs`.
Best source → `best.c` under `--output` and back into the `.c` when it wins.
Exit: `0` match · `1` no match · `2` build/config error.

## 3. Flag Sweep

When diff shows `flag_sensitive: true`, try compiler flag combinations before
the GA. Default to `match flags` (targeted tier). Escalation tiers,
`match batch` flags, and safety stops:
`references/flag-sweep.md`.

```bash
rebrew match flags src/<target>/<file>.c # targeted (default)
rebrew match flags src/<target>/<file>.c --tier quick # first pass
```

Do **not** run `--tier thorough` / `--tier full` or long `match batch` sweeps unless
the user asks. Hand-try `/O2` or `/O1` first; see `references/codegen-hints.md`.

## 4. Structural Similarity Metric

`rebrew diff` outputs a structural similarity breakdown:

```
Structural similarity (flags unlikely to help):
  Instructions: 12 exact, 3 reloc, 2 register, 1 structural (of 18 total)
  Mnemonic match: 94.4%  |  Structural ratio: 5.6%
```

With `--json`, the output includes a `structural_similarity` object:
- `mnemonic_match_ratio`: how similar the mnemonic sequences are (1.0 = identical)
- `structural_ratio`: fraction of instructions with real structural diffs
- `flag_sensitive`: `true` when flag sweeping may help

Use this to quickly rule out flag-based solutions before spending time on sweeps:
`flag_sensitive: false` means flag sweeping won't help: go straight to the GA or
`rebrew prove`. A high `mnemonic_match_ratio` with low `structural_ratio` means the
code is semantically close and C-level tweaks (or `rebrew diagnose near`) may finish
the job.

When kinds match but residue remains (statement order / qualifiers), prefer these
over another GA pass:

```bash
rebrew match climb src/<target>/<file>.c --json                 # adjacent statement-order hill-climb
rebrew match climb src/<target>/<file>.c --objective aligned --json
rebrew match qualifiers src/<target>/<file>.c --json            # declaration qualifier sweep
rebrew match qualifiers src/<target>/<file>.c --dry-run --json
```

`climb` = adjacent statement swaps; `qual-sweep` = exhaustive per-declaration
qualifier variants. Batch flag/GA details: `references/flag-sweep.md`.

## 5. Tips

- For library-origin functions (MSVCRT, ZLIB), use `rebrew library crt-match` to identify the reference source first.
- Common CFLAGS: `/O2 /Gd` (GAME); a library subtree takes its flags from a
  preset (§8), not from per-function CFLAGS.
- While iterating on a single function, `--watch` (on `diff`, `prove`, or `match run`) re-runs on every
  file save, faster than re-typing the command. It never exits on its own: start it only when the
  user wants a live loop, and stop it when they are done. `rebrew match run --watch` is single-function only;
  batch selection uses `rebrew match batch`.
- Use the authorized time/scope for GA batches. Clarify before a multi-hour
  run when that scope has not already been authorized.

## 6. Symbolic Equivalence Proving

When stuck at NEAR_MATCHING (register alloc / reorder / loop layout):

```bash
rebrew diagnose near src/<target>/<file>.c --json
rebrew prove src/<target>/<file>.c --json
```

`REGISTER (N% of delta)` verdicts are prime PROVEN candidates: prefer
`rebrew prove --all` before more GA. Full flags, EDX/`--watch-va` gotchas, and
angr mechanics: `references/prove.md`. Needs the `[prove]` extra (angr); if
missing, install it when dependency setup is authorized, otherwise report the
requirement and continue byte-matching work (see the reference).

## 7. End-to-End Round-Trip

Once a swept or GA'd function reaches EXACT/RELOC, splice it back with
`rebrew build round-trip --json` (`--dry-run` previews). Splice rules, resolution
fallbacks, and `compile_drift` / `catalog_resolution_drift` triage live in
`rebrew-workflow/references/round-trip.md`. Use in CI alongside
`verify --compare`.

## 8. Library Flag Overrides

A library subtree compiles as one unit, so its flags come from
`rebrew-libraries.toml` instead of per-function CFLAGS:

```bash
rebrew library set src/<target>/crt --preset msvcrt-static   # /O2 /Gd /MT
rebrew library set src/<target>/crt --cflags "/O1 /Gd"      # explicit flags win over the preset
rebrew library set src/<target>/crt --dry-run               # preview the write
rebrew library show src/<target>/crt                       # effective override (walk-up from here)
rebrew library list                                        # every rebrew-libraries.toml under the root
rebrew library remove src/<target>/crt --dry-run            # preview the removal
rebrew library remove src/<target>/crt                         # drop the override (back to project defaults)
```

Resolution runs most-specific-first: per-function `TOOLCHAIN`/`CFLAGS` in
`rebrew-functions.toml`, then the nearest `rebrew-libraries.toml` (walk-up),
then the project default. `--library` and `--preset` both set the same key and
are mutually exclusive; an unknown preset or profile is a hard error.
