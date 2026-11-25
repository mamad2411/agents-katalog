---
name: vault-process
description: Autonomous agent queue processor that picks up bugs and tasks from the vault and feeds them through the enterprise pipeline. Low-complexity items are processed autonomously. Medium/high-complexity items pause for human approval. Use when the user says "process the queue", "work on bugs", or invokes /vault-process. Can be run on a loop with /loop 10m /vault-process for continuous processing.
---

# Vault Process — Autonomous Queue Processor

## Trigger
User says "process the queue", "work on bugs", or invokes `/vault-process`.
Can be run on a loop with `/loop 10m /vault-process` for continuous processing.

## Procedure

### Step 1: Load Standards

For Helpdesk items, the standards and routing source of truth is the MCP-backed platform, not vault prose:

- Read the relevant explicit skill file directly before choosing a workflow lane. Do not route skill loading through `skills-index`.
- Use `mcp__standards_mcp__standards_for_task(...)` for the applicable task types before autonomous code changes.
- If the item is a Helpdesk bug, route through `helpdesk-bug` and let that lane create or refresh `.codex/enterprise-state/<slug>-standards.json`.

For non-Helpdesk projects, read coding standards from the vault's `_standards/` directory:

```
Glob for files: {{VAULT_PATH}}/_standards/**/*
```

Read each standards file. These standards MUST be enforced during any autonomous code changes made in later steps.

### Step 2: Load Active Control Board

Fetch open, claimed, in-progress, and blocked bugs/tasks. Before starting fresh open work, surface context-needed active slices and resume or refresh them when appropriate.

```
mcp__vault-index__control_board(active_slice_limit_per_project=5)
mcp__vault-index__list_vault(folder="01-Bugs", status="open")
mcp__vault-index__list_vault(folder="02-Tasks", status="open")
mcp__vault-index__list_vault(status="claimed")
mcp__vault-index__list_vault(status="in-progress")
mcp__vault-index__list_vault(status="blocked")
```

Combine the lists into a single work queue. Do not cap active projects. A project may have 5+ active slices; this is portfolio load, not an error.

### Step 3: Filter Out Blocked Items

For each item with a `blocked_by` field:

1. Use `mcp__vault-index__get_vault_item` to fetch the blocking item
2. If the blocker's `status` is NOT `done` or `archived`, **skip** this item — it stays in queue
3. If the blocker IS resolved, clear the `blocked_by` field via the **Edit** tool and continue processing

### Step 4: Sort the Queue

Sort remaining items by:
1. **Priority** (descending): `critical` > `high` > `medium` > `low`
2. **Age** (descending): oldest `created` date first

### Step 5: Process Each Item

For each item in the sorted queue, determine the processing path based on `complexity` frontmatter:

#### 5a. No Complexity Set

If the item has no `complexity` field:
1. Read the item content and any referenced files
2. Assess complexity:
   - **Low**: Single file change, clear fix, no cross-module impact
   - **Medium**: Multiple files, single module, moderate testing needed
   - **High**: Cross-module, architectural implications, extensive testing
3. Update the item's frontmatter with the assessed `complexity` via the **Edit** tool
4. Continue to the appropriate path below

#### 5b. Autonomous Processing (complexity: low)

1. Update item status to `in-progress` and move to `04-In-Progress/` folder
2. Route by item type:
   - If `type == bug` and `project == helpdesk`, feed into `helpdesk-bug`.
     - Reuse the current vault item instead of creating a new one.
     - `helpdesk-bug` must begin by actually calling `mcp__standards_mcp__standards_for_task(task_type="bugfix")`.
     - Follow the debug-first path before any code fix.
   - Otherwise, feed into `/enterprise` **QUICK** path:
     - Identify the project repo from the `project` field:
       - `my-project` → `{{PROJECT_DIR}}`
       - `my-project` → `{{PROJECT_DIR}}`
       - `my-project` → `{{PROJECT_DIR}}`
     - Create a worktree for the work
     - Implement the fix/task following loaded standards
     - Run tests
     - Create a PR
3. On successful completion:
   - Update item status to `done`
   - Move item to `05-Archive/`
   - Record the PR URL in the item's frontmatter
4. On failure:
   - Leave item in `04-In-Progress/`
   - Add a `notes` field describing what failed
   - Continue to next item

#### 5c. Needs Approval (complexity: medium or high)

Present to user:

> "**[Bug/Task] #X: [title]**
> - Priority: [priority]
> - Complexity: [medium/high]
> - Project: [project]
> - Module: [module]
> - Affects: [description of scope]
>
> This item affects [multiple modules / has architectural implications / etc.].
> Approve autonomous processing? **[Y / N / Skip]**"

- **Y (approved)**: Feed into `/enterprise` **STANDARD** path (medium) or **FULL** path (high). Follow same completion/failure flow as 5b.
- **Y (approved)**:
  - If `type == bug` and `project == helpdesk`, feed into `helpdesk-bug` and let it pause or continue according to its own debug-first risk routing.
  - Otherwise, feed into `/enterprise` **STANDARD** path (medium) or **FULL** path (high).
  - Follow the same completion or failure flow as 5b.
- **N (rejected)**: Leave in queue, move to next item.
- **Skip**: Leave in queue, move to next item. Do not ask again this session.

### Step 6: Re-index After Each Item

After processing each item (regardless of outcome), re-index the vault:

```
mcp__vault-index__index_vault(incremental=true)
```

This ensures subsequent items see accurate blocker statuses.

### Step 7: Report

After all items are processed (or queue is empty), output a summary:

```
## Queue Processing Report

- **Processed autonomously**: X items (Y bugs, Z tasks)
- **Awaiting approval**: W items (medium/high complexity)
- **Blocked**: B items (open blockers)
- **Failed**: F items (see notes in vault)

### Completed Items
| Item | Type | Project | PR |
...

### Needs Your Approval
| Item | Type | Complexity | Project |
...
```

### Step 8: Loop Mode Behavior

If invoked via `/loop 10m /vault-process`:

- Process **ONE item only** per invocation to avoid long-running sessions
- Pick the highest-priority, oldest item from the sorted queue
- If the top item needs approval, present it and stop (do not auto-skip to find an autonomous item)
- The next loop invocation will pick up where this one left off

## Notes

- The vault path is `{{VAULT_PATH}}`.
- Standard folders: `00-Inbox`, `01-Bugs`, `02-Tasks`, `03-Ideas`, `04-In-Progress`, `05-Archive`, `_standards`.
- Project repos: my-project (`{{PROJECT_DIR}}`), my-project (`{{PROJECT_DIR}}`), my-project (`{{PROJECT_DIR}}`).
- Frontmatter schema: `id`, `type`, `priority`, `project`, `module`, `agent`, `status`, `branch`, `worktree_path`, `complexity`, `next_action`, `proof_state`, `blocked_by`, `related`, `tags`, `created`, `updated`.
- This skill depends on `/enterprise` for generic work and `helpdesk-bug` for Helpdesk bug items.
- Standards loaded in Step 1 apply to ALL autonomous code changes — never skip standards enforcement.
