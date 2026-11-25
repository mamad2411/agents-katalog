---
name: fork-idea-branch
description: Split an active research path into multiple parallel product paths, archiving the original and scaffolding fresh starts per branch
type: planning
version: v0.0
required_conventions: [alignment-page]
argument-hint: "[path-a-label] [path-b-label] [--from <skill>] [--reuse <artifact-types>]"
---

# Fork Idea Branch

Use this skill when a single research path should split into multiple parallel product paths - for example, two compelling ICPs with conflicting pain points that need separate products, or positioning evidence showing the concept serves fundamentally different markets. This skill archives the current research, scaffolds new product paths, and routes each back to `$idea-scope-brief` for a fresh start.

This is a base helper, not part of any pack's linear workflow. It can be invoked directly by the user or suggested by research skills when alignment page answers indicate divergent paths.

This skill is distinct from `$product-line fork` (which adds a path to the portfolio). This skill splits and restarts research from scratch.

## Process

### 0. Validate Preconditions

Read `research/.progress.yaml` (normalize legacy fields: treat `active_path` as `active_paths`, `abandoned` as `archived`). If no active research exists (no manifest active paths, no research directories with content), explain there is nothing to fork and route to `$idea-scope-brief`. Stop.

### 1. Capture Fork Context

Parse `$ARGUMENTS` for:
- Branch labels/slugs (positional arguments)
- `--from <skill>` - the skill that triggered this fork
- `--reuse <artifact-types>` - comma-separated list of artifact types to carry forward

If arguments are incomplete, interview the user:
- What diverged? (ICP hypotheses, market segments, value wedges, etc.)
- How many branches? (minimum 2)
- Working labels for each branch

Normalize slugs (lowercase, hyphenated). Validate no collisions with existing `research/` paths or manifest entries. If `--from` is not provided, mark the source as `user-initiated`.

### 2. Present Reuse Decision (Alignment Page)

Build alignment page at `alignment/fork-idea-branch-{source-slug}.html` with these gates:

1. **Fork rationale gate** - Why the split is needed, source evidence supporting divergence.
2. **Per-branch scope gate** - For each branch: label, slug, ICP hypothesis, value wedge hypothesis.
3. **Reuse decisions gate** - Per branch: fresh start (default, recommended) vs. carry-forward with artifact type selection (e.g., ICP research, competitive analysis, journey maps). Explain contamination risk: carried-forward artifacts were shaped by assumptions that may not hold for the new branch's ICP/market. Users must opt in per artifact type.
4. **Archive confirmation gate** - Confirm the current path will be archived. Show the source path and proposed archive location.
5. **Proposed file changes gate** - Full inventory of files to create, move, and modify.
6. **Post-approval route gate** - Show the restart checklist that will be emitted after scaffolding.

Pre-approval stop applies - no archiving or scaffolding until the user approves the compiled YAML.

### 3. Archive Current Path

After approval:

1. Move `research/{old-slug}/` to `research/_archive/{old-slug}-pre-fork/`.
2. Archive alignment pages to `docs/history/archive/YYYY-MM-DD/HHMMSS/`.
3. Update `research/.progress.yaml` manifest:
   - Old path entry -> `status: archived`, `archive_reason: forked-to-{slug-a}+{slug-b}`, `archived_at: <date>`.

### 4. Scaffold New Paths

For each branch:

1. Create `research/{new-slug}/`.
2. Write `research/{new-slug}/_working/fork-seed.md` with ground-truth inputs only:
   - Original idea (from the source path's idea brief or concept)
   - This branch's ICP hypothesis
   - This branch's pain point hypothesis
   - This branch's value wedge hypothesis
3. If carry-forward was approved for this branch: copy selected artifacts from archive to `research/{new-slug}/` with a contamination header note at the top of each carried file:
   ```
   <!-- Carried forward from research/_archive/{old-slug}-pre-fork/ during fork on YYYY-MM-DD. Original assumptions may not hold for this path's ICP/market. Review critically. -->
   ```
4. Update `research/.progress.yaml` manifest - add entries per branch:
   - `status: active`
   - `source_skill: fork-idea-branch`
   - `pipeline_stage: idea-scope-brief`
   - `next_skill: $idea-scope-brief {slug}`

Respect `max_concurrent` from the manifest - if adding branches would exceed the limit, set excess branches to `status: deferred` and note they will activate when a slot opens.

### 5. Write Fork Memo

Write `research/_working/fork-memo-{date}.md` with:
- Source skill (the `--from` value or `user-initiated`)
- Source path (the archived slug)
- Branches created (slug, label, status per branch)
- Rationale summary
- Reuse decisions per branch (fresh start or which artifacts carried forward)
- Full artifact inventory (what moved where)
- Restart instructions (the `$idea-scope-brief {slug}` commands)

### 6. Emit Restart Checklist

Present the restart commands:
```
$idea-scope-brief {slug-a}
$idea-scope-brief {slug-b}
```

Note reuse status per branch (fresh start vs. carry-forward with which artifacts). Recommend sequential execution - complete one branch's idea-scope-brief before starting the next to avoid cross-contamination of thinking.

## Constraints

- Does not run `$idea-scope-brief` or any downstream skills. It scaffolds and stops.
- Does not merge research across paths. Each branch starts clean (or with explicitly opted-in carry-forward artifacts).
- Does not create task entries in `tasks/todo.md`. The restart checklist is the handoff.
- Uses "path" not "branch" in manifest terminology to avoid confusion with git branches.
- Distinguishes itself from `$product-line fork` (which adds a path to the portfolio; this skill splits and restarts research).

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/fork-idea-branch-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention.
