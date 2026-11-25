---
name: claude-sync
description: Pull global config, scaffold per-project Tier-3 skill configs, sync project-local forks of global skills for shared repos, and migrate a project off the retired template tier
---

# Claude Sync

Pull global config, then set up or refresh the two things a project can legitimately carry: **Tier-3 skill configs** and **project-local forks of global skills**.

Input: `$ARGUMENTS` (optional — `fresh` to force re-scaffold, or skill names to scope)

**There is no longer a template tier.** Every skill is global and discovers project context at runtime from `CLAUDE.md`, the project's `.claude/rules/`, and an optional committed `.claude/skill-config/<name>.md`. See `rules/meta-skill-tiers.md`.

## Tier-3 skill configs

Global skills that need project-specific values read `.claude/skill-config/<name>.md`, **committed** so colleagues get it on clone. Currently `/build` (build command, preview server) and `/test` (build command, tier table, baseline path, drift mapping); `/refactor-comments` optionally takes a curated partition table. Always optional — scaffold on request, not by default. If a project has a config in the old gitignored `.claude/local/skills/<name>/config.md`, move it — nothing reads that path any more.

## Forked-Global Skills (project-local copies)

Per `meta-project-local-skill-copies.md`, some projects ship local copies of global skills in `.claude/skills/<name>/` so colleagues without `~/.claude/` get the workflow on clone.

### Classification

For each `.claude/skills/<name>/SKILL.md`:

- **Forked-global** — `~/.claude/skills/<name>/SKILL.md` exists. Handled by the fork flow.
- **Project-unique** — no matching global. Leave alone; never treat as a fork.

### Transformations (applied when syncing global → project)

- `(~|$HOME)/.claude/` → `.claude/` (project-relative paths).
- `powershell.exe` → `pwsh` (cross-platform per the rule).

`mirror-skill.ps1` applies these to every file it mirrors. Apply them yourself only to the shared `.claude/scripts/` utilities in 2.3.

### Script sync (wholesale by directory)

`mirror-skill.ps1` mirrors a fork's whole skill directory — `SKILL.md`, templates, and `scripts/`. Shared utilities in `.claude/scripts/*.ps1` are separate: sync every one present in the project from `~/.claude/scripts/`, **and** copy any the fork now depends on that the project lacks.

---

## Step 0 — Pull

Run: `pwsh -NoProfile -File "$HOME/.claude/scripts/pull-config.ps1"`

If pull fails: ask the user — continue against the local global config, or abort?

## Step 1 — Detect Mode

`.claude/local/config-version.json` exists? → **Sync** (Step 3). Missing → **Initial Setup** (Step 2).
`$ARGUMENTS = "fresh"` → force Initial Setup. Skill names → scope to those skills in the detected mode.

## Step 2 — Initial Setup

### 2.1 Git workflow

If `.claude/rules/git-workflow.md` already exists, skip this step.

Ask via `AskUserQuestion`: which workflow does this project use?

- **Feature branches (Recommended)** — `/implement` creates `implement/{plan-name}` per plan, `/commit` pushes to that branch. PR-based merge to main.
- **Direct to main** — solo project or prototype. `/implement` works on main directly, `/commit` pushes straight to main. No PR step.
- **Worktree per feature** — like feature branches, but each plan gets its own worktree.

Write the choice to `.claude/rules/git-workflow.md` using the matching template in `git-workflow-templates.md` (this skill's directory). `/implement`, `/commit` and `/rebase-on-main` read it.

### 2.2 Tier-3 configs

Ask via `AskUserQuestion` (multiSelect): which global skills should get a project config? Offer `build` and `test`; mention `refactor-comments` only if the project is large enough that a curated partition table beats a derived one.

Read `CLAUDE.md` for context first, then gather per skill — build command, dev server name and port, test tiers and their commands, baseline path. Write each to `.claude/skill-config/<name>.md` as headed sections per the schema in `meta-skill-tiers.md`: commands, paths, names, small tables. Never architecture prose.

**Write project facts and nothing else** — no dates, provenance, or precedence notes (`meta-skill-tiers`). Owner-side context goes in a gitignored `.claude/local/skill-config-notes.md`.

### 2.3 Forked-globals (for shared repos)

Check `~/.claude/local/projects.md` first — if it lists this project, take its posture as the answer and say which line you used. Otherwise ask via `AskUserQuestion`: **is this a shared repo where colleagues may not have `~/.claude/` set up?**

- **No** (Recommended for solo projects) — skip to 2.4.
- **Yes** — colleagues will rely on local copies. Continue.

Either way, offer to record the answer in `local/projects.md` when the project was missing from it.

If yes, list the global skills via the Classification above and present via `AskUserQuestion` (multiSelect, no pre-selection): which to scaffold as project-local forks? Prefer skills integral to colleague workflow (`plan`, `implement`, `commit`, `rebase-on-main`).

For each selected fork, run `pwsh -NoProfile -File "$HOME/.claude/scripts/mirror-skill.ps1" -Name <name> -ProjectRoot <project root>` — it mirrors the whole skill directory (`SKILL.md`, templates, `scripts/`) with the Transformations applied.

Afterwards ensure `.claude/scripts/` has the shared utilities forks commonly depend on (`git-diff-scope.ps1`, `git-preflight.ps1`, `kill-port.ps1`), copied with transformations. Skip files the project already has — no overwrite without prompting.

Compute each fork's hash from its **transformed** content, for the `forks` map in 2.5.

### 2.4 Create `.claude/launch.json`

If a build or test config was written, a preview server was named, and the file doesn't exist.

### 2.5 Stamp `.claude/local/config-version.json`

Global version, date, and fork hashes under `forks`. There is no `skills` map any more — if an old one is present, drop it.

### 2.6 Report

List created files (including `git-workflow.md`). Remind about `.claude/local/` in `.gitignore`, and about `arch-claude-md-is-an-index` — `CLAUDE.md` is an orientation index, architecture substance belongs in the project's root `docs/`.

---

## Step 3 — Sync

### 3.1 Compare versions

Match, and no specific skills requested → "All current." Done. Differ → read `CHANGELOG.md` and summarize the **Project action** entries between the two versions.

### 3.1b One-time migration off the retired template tier

**Trigger:** the version file has a `skills` map — the project predates v1.1.17 and still carries template-scaffolded copies of now-global skills. Absent → skip. Present → follow `migrate-template-tier.md` (this skill's directory).

### 3.2 Per-fork drift categorization

For each fork: compute the hash of the transformed `~/.claude/skills/<name>/SKILL.md` and compare to the stored one. Categorize **Changed**, **Current**, or **New** (a global exists that the project doesn't fork yet — only offer these if the project already forks something).

### 3.3 Selection

Ask via `AskUserQuestion` (multiSelect, pre-select Changed + New).

### 3.4 Drift check (parallel Haiku fanout)

Before applying anything, compute drift per Changed fork independently. For each, spawn a Haiku agent (`model: "haiku"` — mechanical per-item comparison, per `wf-agents-on-sonnet`):

> Given the current project SKILL.md and the regenerated content (transformed global + reinserted `<ProjectSpecific>` blocks), return JSON `{ skill, drift: bool, lines: N, projectOnlyLines: N, sectionsAtRisk: [headings], sample: [first 20 +/- lines outside <ProjectSpecific> blocks] }`. Strip `<ProjectSpecific>` blocks from both before comparing.
>
> `projectOnlyLines` counts lines present in the project copy but absent from the regenerated content — the work an overwrite would destroy. `sectionsAtRisk` names the headings those lines sit under.

Wait for all to return.

### 3.5 Apply updates per fork

- **No drift** → apply silently via `mirror-skill.ps1` (as in 2.3).
- **Drift** → ask via `AskUserQuestion`: **Apply (overwrite drift)** (`mirror-skill.ps1 … -Force`) / **Show full diff** / **Skip this skill**.

**Name the loss in the prompt.** State `projectOnlyLines` and `sectionsAtRisk` in the Apply option's description — "discards 82 project-only lines under Phase 6.5, Phase 8", not a bare "overwrite drift".

When `projectOnlyLines` exceeds ~25, default the selection to **Skip** — that far ahead is an unmerged feature, not drift.

Applying a fork also resyncs its shared `.claude/scripts/` dependencies per Script sync above — unconditional, no per-script drift tracking.

**Missing matching global** → a project fork with no `~/.claude/skills/<name>/SKILL.md` counterpart means the global was removed or renamed. Warn and skip; the user decides whether to delete the orphan.

#### `<ProjectSpecific>` block preservation

`mirror-skill.ps1` re-inserts each block after its anchor heading (orphans land under `## Project additions` with a warning). Format and authoring: `rules/wf-project-specific-blocks.md`.

### 3.6 Update the version stamp

Write the new global version and date, and each fork's transformed hash under `forks`; drop any `skills` map.

### 3.7 Report

Updated, added, skipped, current forks. New version number.

---

## Edge Cases

- **No `forks` map in the version file**: scan `.claude/skills/` per Classification, register all as **New**, ask the user to accept; later runs handle drift normally.
- **A stale `skills` map** from the retired template tier: handled by Step 3.1b, not here. Never drop the map without running that migration.
- **Manual edits**: the drift check catches them. Wrapping edits in `<ProjectSpecific>` preserves them across syncs without prompting.
- **Project-unique skills**: no matching global → left alone, never treated as forks.
- **Pull fails**: offer to continue against the local global config.
