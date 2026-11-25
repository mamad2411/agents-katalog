---
name: bmad-create-wave
description: >
  Decompose a set of epics and stories into a wave map. Reads epics.md, story
  files, and architecture.md; constructs a story dependency graph; produces a
  draft wave decomposition; presents it inline for user review; writes the
  approved wave map to disk.
when_to_use: |
  Use at the start of Phase 4 (Implementation), after epics and stories have
  been produced and the implementation-readiness gate has PASSED. Use again in
  update mode whenever a course correction adds or removes stories, or
  whenever the epic structure changes materially mid-project.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
metadata:
  version: 1.1.1
  output-locations:
    - _bmad-output/planning-artifacts/waves.md
    - docs/epics.md   # Appendix C of epics.md, if --inline mode is selected
    - .bmad/wave-<id>/wave.md   # one lifecycle record per new wave, status draft
---

# bmad-create-wave
Decompose a set of epics and stories into a wave map. The wave map is consumed
by /bmad-dev-wave, /bmad-merge-wave, /bmad-status-wave, and /bmad-close-epic.
This skill is Stage 1 of the four-stage wave cycle.

## Inputs
### Required
- docs/epics.md
- docs/stories/**/*.md
### Optional
- docs/architecture.md
- docs/risk-register.md
### Partial-Input Behavior
- Missing epics.md: halt; instruct user to produce epics and stories first.
- Missing story file referenced by epics.md: warn; exclude story; proceed.
- Missing architecture.md: skip architecture-aware heuristics.
- Missing risk-register.md: skip risk-aware load-bearing bump.

## Outputs
### Default mode
Writes _bmad-output/planning-artifacts/waves.md.
### --inline mode
Appends to docs/epics.md as Appendix C.
### Schema (both modes)
| Field | Type | Notes |
|---|---|---|
| Wave | string | e.g. "1A", "1B", "2A" -- epic + letter |
| Pattern | enum | serial or parallel |
| Stories | list[string] | Story IDs in this wave |
| Spine-only | bool | True if no user-visible value |
| Load-bearing | bool | True if any downstream wave depends on it |
| Branch suffix | string | Used by /bmad-dev-wave |
| Notes | string | Free-form rationale |

## Workflow
1. Ingest inputs.
2. Build dependency graph; abort on cycle.
3. Topological sort (Kahn) with level tracking; group into batches.
4. Semantic clustering: demote coupled pairs out of parallel batches.
5. Flag assignment: load-bearing and spine-only per wave.
6. Render draft inline.
7. Halt for propose-and-confirm; accept "approved", "edit: <instruction>",
   or "abort".
8. Write file on approval, then open a lifecycle record at `draft` for every
   wave the map gained (see The Status Record).

## The Status Record
Every wave in the map carries a lifecycle status, and this skill opens it. For
each wave the approved map adds:

    python3 {skill-root}/../bmad-dev-wave/scripts/wave_status.py set \
        --project-root {project-root} --wave <id> --status draft

`draft` is the entry status: the row exists and /bmad-dev-wave has not run
past step 5. The vocabulary is defined once, in that script, and tabled in
/bmad-dev-wave; do not restate the status names here.

In update mode, only new waves get a record. A wave already in the map keeps
the status it has, including `blocked` -- re-running this skill is not a way
to clear one, and the script refuses the write if it tried. Re-deciding a
wave's stage from a re-planned map would discard what the wave actually did.

A wave removed from the map keeps its record on disk. It is unreachable, since
every other skill refuses a wave that is not in the map, and deleting state
for a wave a course correction might restore buys nothing.

## Wave-Classification Logic
### Dependency-Graph Extraction
- Nodes: every story across every epic.
- Intra-epic edges: from story "Depends on:" lines.
- Cross-epic edges: from epics.md, expanded into per-story edges pointing at
  the dependent epic's foundation wave.
- Cycle detection: DFS; abort on back-edge.
### Topological Sort for Parallel Batches
- Kahn's algorithm with level tracking.
- Each batch becomes a candidate parallel wave (>1 story) or serial wave
  (1 story).
- Wave labels: <epic><letter>; letter resets per epic.
### Semantic Clustering Within Batches
For each parallel batch, check pairwise for:
1. Shared "Files to modify:" overlap.
2. Shared "tightly-coupled:" frontmatter tag.
3. Shared story-ID prefix beyond the epic number.
4. (Optional) shared deployment unit per architecture.md.
Demote on any positive match; split the batch and re-label.
### Flag Assignment
For each wave:
- load-bearing(W) = true if any later wave contains a story whose dependencies
  reference W. Forced to true if any story in W is high-risk per
  risk-register.md.
- spine-only(W) = true if every story in W has "spine-only: true" frontmatter,
  or W matches the foundation-wave pattern (*A label, foundation-naming story
  IDs).

## Error Handling
- Status record write refused (the wave is blocked): report it and continue
  writing the map. The map is the planning artifact; a blocked wave's record
  is a live control this skill has no standing to overwrite.
- Missing epics.md: halt.
- Cyclic graph: halt; report cycle.
- Malformed story file: warn; exclude; proceed.
- Missing story referenced by epics.md: warn; exclude; proceed.
- Ambiguous classification: flag in Notes; resolve in propose-and-confirm.

## Version history
- 1.1.1 (2026-10-01, R4 of docs/reviews/harness-engineering-review-v1.md):
  frontmatter only. `when-to-use` is `when_to_use`, the field Claude
  Code reads, so it now reaches the skill listing; `version` and
  `output-locations` sit under
  `metadata:`, which Claude Code leaves to the fork's own tooling. Nothing in
  the body changed.
- 1.1.0 (2026-09-11, Phase 2 of docs/harness-conversion-plan.md): step 8 opens
  a lifecycle record at `draft` for every wave the map gains, so a wave starts
  with a recorded stage instead of one inferred at first dispatch. Update mode
  leaves existing records alone, blocked ones included.

## See also
- /bmad-dev-wave consumes this skill's output, and owns the status vocabulary
  this skill writes.
- Wave methodology deep dive: manual Part 5.
