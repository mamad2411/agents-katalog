---
name: vault-triage
description: Walk through inbox items one by one and route them to the right queue. Use when the user says "triage the inbox", "process inbox", "clear the inbox", or invokes /vault-triage. Also suggested when the vault-gates hook blocks /enterprise due to inbox items older than 48 hours. Presents each item and asks where to route it.
---

# vault-triage

Walk through all inbox items one by one, presenting each to the user and routing it to the correct queue.

Vault path: `{{VAULT_PATH}}`
Vault folders: 00-Inbox, 01-Bugs, 02-Tasks, 03-Ideas, 04-In-Progress, 05-Archive
Frontmatter schema: id, type, priority, project, module, agent, status, branch, worktree_path, complexity, next_action, proof_state, blocked_by, related, tags, created, updated

## Steps

### 1. List inbox items

Use `mcp__vault-index__list_vault(folder="00-Inbox")` to get all items in the inbox. Sort by age, oldest first.

### 2. Handle empty inbox

If the inbox is empty, respond with:

```
Inbox is empty. Nothing to triage.
```

Then stop.

### 3. Process each item

For each item in the inbox, do the following:

#### a. Present the item

Show the user a summary with these fields:
- **Type**: from frontmatter `type`
- **Project**: from frontmatter `project`
- **Priority**: from frontmatter `priority`
- **Excerpt**: a brief excerpt from the body (first ~2 lines)
- **Age**: how long ago the item was created

#### b. Ask for routing

Ask the user:

```
Route to: Bugs (B), Tasks (T), Ideas (I), Archive (A), or Skip (S)?
```

Wait for the user's response before proceeding.

#### c. Route the item

Based on the user's choice:

| Choice       | Action                                                                 |
|-------------|------------------------------------------------------------------------|
| **B** (Bugs)    | Move to `01-Bugs/`. Set `type: bug`. Assess and set `complexity` (low/medium/high). |
| **T** (Tasks)   | Move to `02-Tasks/`. Set `type: task`. Assess and set `complexity` (low/medium/high). |
| **I** (Ideas)   | Move to `03-Ideas/`. Set `type: idea`.                                 |
| **A** (Archive) | Move to `05-Archive/`. Set `status: wont-do`.                          |
| **S** (Skip)    | Leave in inbox, move to the next item.                                 |

For Bugs and Tasks: assess the item and set `complexity` to low, medium, or high based on the scope described.

Update the `updated` field in frontmatter to the current ISO timestamp.

#### d. Move the file

To move a file between folders:
1. Use the Edit tool to update the frontmatter in the source file
2. Write the updated file content to the new path using the Write tool
3. Delete the old file using Bash: `rm "<old path>"`

### 4. Refresh the index after each move

Call `mcp__vault-index__index_vault(incremental=true)` after each item is moved.

### 5. Continue or stop

Continue processing items until:
- The inbox is empty, or
- The user says "stop", "done", "quit", or similar

### 6. Print summary

After finishing, print a summary line:

```
Triaged X items: Y -> Bugs, Z -> Tasks, W -> Ideas, V -> Archive. Inbox: N items remaining.
```
