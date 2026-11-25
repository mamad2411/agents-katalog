---
name: opsxp-ff
description: Create the minimum apply-ready OpenSpec artifacts, optional task linkage, branch, metadata, and draft PR without unnecessary planning or push cycles.
---

# OPSXP FF

Create only what Apply needs. Reuse an existing change, branch, metadata file, or PR instead of duplicating it.

## 1. Resolve context

1. Read repo instructions and validate `openspec/opsxp.yaml` against its schema.
2. Resolve the requested change and intent. Ask only when the goal is materially unclear.
3. If the change exists, inspect status and continue only missing FF work.
4. If a standalone OpenSpec store is explicitly used, resolve it once and reuse its option.

## 2. Start from current target

When Git is available and `git.sync_target_before_ff: true`:

1. Preserve unrelated changes; stop if branch work would overwrite them.
2. Fetch/prune, inspect worktree ownership, and fast-forward the configured target.
3. Create or reuse `<branch_prefix><change>` from the current target.

Do not clean old branches. With optional/no Git, continue file-based and skip PR automation.

## 3. Resolve optional task linkage

- With `notion_enabled: false`, do not prompt for or access Notion.
- When enabled and a link is supplied, read the page and capture canonical ID, page ID, and URL.
- Ask for a missing link only when `task_link_required_on_ff: true`.
- Never infer the task ID from title or URL when `task_id_property` is available.

Notion, PR creation, metadata, and push policy are independent.

## 4. Build apply-ready artifacts

1. Create the change when missing:
   ```bash
   openspec new change "<change>"
   ```
2. Read status and `applyRequires`:
   ```bash
   openspec status --change "<change>" --json
   ```
3. For each ready required artifact, read its current instructions, dependencies, template, and resolved output path.
4. Write the artifact, refresh status, and stop when all apply-required artifacts are done.

### Task style

- Use the fewest ordered tasks that preserve independent proof; one task is valid.
- Keep each task to one sentence naming the behavior or artifact and its smallest proof.
- Split only where parts can be implemented and checked independently.
- Do not add task packets, exhaustive file plans, repeated non-goals, or a full-test task.
- Apply owns RED/GREEN; Verify owns the required release profile.

## 5. Persist linkage and draft PR

When `pr.metadata_artifact` is enabled:

1. Resolve it inside the `changeRoot` returned by status.
2. Write schema version 1 with change, project, optional task, branch/target, and nullable PR identity.
3. Validate every write against `pr.metadata_schema` without adding a dependency.

When metadata is disabled, skip it. Draft PR creation still works; cross-session Notion writeback does not.

For Git and PR actions:

1. Make one initial commit and push when policy permits: `always` pushes; `when_pr_active` pushes when `pr.draft_on_ff: true`; `manual` never auto-pushes.
2. Create or reuse the draft PR through any available Git-host capability. If policy left the branch local, report the one manual push needed first.
3. Prefix the title and add the body task link only when a task is linked.
4. Record the returned PR number and URL in metadata and validate it locally.
5. Include that metadata update in the next coherent commit from Apply or Archive; do not create a second FF-only commit/push cycle.
6. If no Git-host capability exists, keep local artifacts valid and report one manual PR action.

## Output

Report change, branch, task ID if any, draft PR state, artifacts created, expected local metadata update, and `Ready for Apply`.
