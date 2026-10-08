# HumbleStudio Proposal Artifact Loop

Use when extending HumbleStudio's native review flow around markdown change proposals stored in the repository.

## Goals

- keep proposal capture repo-aware and stable
- let reviewers read proposal artifacts back inside the macOS app
- preserve a strict boundary between proposal authoring and future write-back

## Workflow

1. Start from native review context:
   - component id or view id
   - evidence path
   - preview coverage
   - current truth gap
2. Save proposal artifacts into `docs/change-proposals/` with predictable scope-based filenames.
3. Add native readback:
   - list matching proposals for the current selection
   - if useful, also surface proposal linkage in adjacent review or navigation inspector summaries
   - once the loop becomes dense enough, promote it into a dedicated native proposal workspace instead of keeping everything buried inside inspectors
   - show scope, coverage, evidence, updated time, and richer proposal metadata when available
   - prefer native filtering and sorting by scope, status, and coverage before creating a dedicated artifact workspace
   - prefer structured metadata such as `Area`, `Why`, `Token candidate`, `Component candidate`, and `View candidate`
   - tolerate older proposal markdown that only contains `Intent`, `Targets`, and basic acceptance notes
   - surface typed recovery states for `docs/change-proposals/` reload issues such as missing folder, unreadable directory, or unreadable markdown files
   - support refresh and open/reveal actions
4. Keep the markdown shape aligned with `docs/change-marking-contract.md`.
5. Do not couple proposal capture to automatic apply logic in the same slice.

## Output Expectations

- proposal save path is deterministic
- matching artifacts are visible from the native inspector
- documentation mentions the repo-aware proposal loop
