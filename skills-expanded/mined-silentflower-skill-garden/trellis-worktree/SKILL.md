---
name: trellis-worktree
description: "Prepare and diagnose branch-local Trellis usage inside linked Git worktrees. Use when the user mentions worktree, linked worktree, worktree development, missing .trellis in a worktree, or parallel branch development."
---

# Trellis Worktree

Use this skill before normal Trellis routing when the current request is about linked worktrees or parallel branch development.

Each worktree owns the Trellis and platform files checked out by its branch. Load workflow and platform content only from the target branch. Flower installation records may be inherited through the verified CLI preparation below; never create whole-directory symlinks between worktrees.

## Workflow

1. Identify the target worktree. Use the explicit path if present; otherwise use the current working directory.
2. Run external diagnosis first:

```bash
flower-trellis worktree status --target <target-worktree> --json
```

3. Route by status:
   - `ready-local`: inspect `flower.installation` before continuing. If it is `incomplete`, follow Flower Preparation below; Trellis readiness does not prove Flower installation completeness.
   - `needs-prepare`: run `flower-trellis worktree prepare --target <target-worktree>` with an explicit developer identity when requested. Include the Flower Preparation options when records are incomplete. Add `--inherit-route-prefs` only when the user wants the same developer's normalized personal route defaults.
   - `needs-init`: initialize Trellis in that branch; do not copy another worktree's version.
   - `needs-migration`: run `flower-trellis worktree migrate --target <target-worktree> --dry-run` before the real migration.
   - `blocked` or `error`: stop and report the stable reason and conflict paths.
4. For a new parallel task, load Trellis package context before requesting the plan:

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
```

   Treat the default package as the selected root repository. Correlate package entries marked as Git repositories with the engine's submodule inventory. Display every additional independent Git package by name and path, and require its base/branch to be confirmed separately after handoff; never infer a child repository base from the root branch.
5. Request the read-only create plan before planning files exist. Omit `--base` to use the current source branch; detached sources fall back to `HEAD`:

```bash
flower-trellis worktree create --target <path> --branch <branch> [--base <ref>] \
  --task-title <title> --task-slug <slug>
```

6. Present one compact confirmation view containing the selected root repository/branch/HEAD, requested and resolved base, target branch/path/task, root dirty warning, selected-commit submodules, independent Git packages, developer initialization, normalized route preference action, Flower transfer source/action/paths and pending target validation, and excluded local state. Flower records are included in the same plan fingerprint; content mismatch after checkout rolls back creation. State explicitly that only the selected root gets the new branch; submodules and independent Git packages are inventory-only.
7. Ask for exactly one choice: confirm the displayed plan, change its inputs, or cancel. On confirmation, execute the exact plan fingerprint returned by preflight:

```bash
flower-trellis worktree create --target <path> --branch <branch> [--base <ref>] \
  --task-title <title> --task-slug <slug> \
  --yes --plan-fingerprint <fingerprint>
```

8. If the engine returns `create-plan-changed`, show the latest returned plan and require a new confirmation. Never reuse the old fingerprint.
9. Continue task planning in a new AI session whose cwd/workspace root is the returned handoff directory. Do not continue the source session inside the new worktree.

## Flower Preparation

Use the initiating worktree as the source. In a new session already inside the target, use `git worktree list --porcelain` to locate the same repository's main worktree. If it is the target itself or no suitable source is known, report unavailable evidence; do not combine records from arbitrary branches.

```bash
flower-trellis worktree prepare --target <target> --inherit-flower --source <source> [--developer <name>] --json
```

The CLI fills missing `plugins.json`, `plugin-lock.json`, and `state.json` only after matching the source installation and target managed content. It may inherit normalized `settings.json` policy for the same developer. Existing target records take precedence; files remain independent after preparation. Create includes this transfer automatically.

Read `localStateTransfer.flower`: `inherited` or `preserved` completes preparation; `unavailable` means installation evidence is still missing, not that the project is up to date. Pure Trellis remains usable. Invalid records, incompatible target versions, disabled/recovery state, or content drift require reporting the reason and paths; do not overwrite records, copy plugin content, or install updates to bypass the conflict. Re-run status after repair.

## Safety Rules

- `status` is read-only.
- A `create` call without `--yes` is also read-only and must return `confirmation-required` plus a fingerprint.
- `prepare` initializes target-local state and registry metadata. By default it reads no other worktree. Explicit Flower inheritance requires the same canonical Git common dir and verified installation content. Personal route/settings inheritance additionally requires the same developer and preserves existing target preferences.
- `migrate` may replace only schema v1 manifest-managed symlinks, and only with content reconstructed from the target branch itself.
- Do not read the legacy `sourceRoot` as migration content.
- `create` does not attach or move an existing task.
- Root tracked, staged, untracked, and conflict state is not included in the selected base commit or stashed. Only the explicitly planned Flower record whitelist may be inherited separately; source plugin content is never copied to make its records match the target.
- Personal inheritance is limited to normalized `.trellis/.route-prefs.tmp` and Flower update policy. Route preferences accept only legal `implement` and `check` values in fixed order; never copy raw preference bytes or update-check caches.
- Do not inherit session/current-task state, pre-check/untracked/auto-loop/Ralph state, agent temporary state, Flower control/detached state, `.claude/settings.local.json`, caches, transactions, or backups.
- Selected-commit submodules are inventory facts. Report initialized source branch/HEAD without fetching, checking out, or copying submodule working trees.
- `remove` requires a clean worktree with no active task, session, or lock; it preserves the branch.
- Do not use force, copy directories between worktrees, or treat setup as approval to start, check, commit, merge, or push.

## Expected Results

- `ready-local`: local real directories are active for this branch.
- `needs-init`: the branch lacks versioned Trellis content.
- `needs-prepare`: local runtime or developer state is missing.
- `needs-migration`: a valid legacy projection was detected.
- `blocked`: user paths, symlink drift, registry drift, dirty state, task state, or locks prevent mutation.
- `error`: Git metadata or an operation failed with a stable reason.
