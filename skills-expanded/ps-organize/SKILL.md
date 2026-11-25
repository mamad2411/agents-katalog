---
name: ps-organize
description: Organize a Process Street library into a clean folder structure — list folders and workflows, propose a structure, create folders, and re-file workflows. Use when the user wants to organize, tidy, or restructure their workflows/folders.
---

# Organize the Process Street library

Bring order to a Process Street workspace: propose a sensible folder structure and move workflows into it.

**CLI:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" <command>` (plugin) or `scripts/process_street.py` (repo). Needs `PROCESS_STREET_API_KEY`.

## 1. Survey what exists

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" folders     # current folders
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" workflows   # all workflows
```

Group the workflows by what they're for (Sales, Customer Success, Finance, HR, Ops…) and note obvious duplicates, drafts, or stale templates.

## 2. Propose a structure

Recommend folders **by team or function** (not by date or person), per `reference/best-practices.md`:
- Keep active templates separate from archived/draft ones.
- Consistent, outcome-based names.
- Don't over-nest — one clear level is usually enough.

Show the user the proposed folder list and which workflows go where. Get a yes before changing anything.

## 3. Create folders & re-file

Create any missing folders:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" folder-create --name "Customer Success"   # note the returned folder ID
```

Move a workflow into a folder by updating its folder (the API does not return a workflow's current folder/share settings, so `--folder-id` is **required** and unspecified sharing flags fall back to defaults — pass them if the workflow has non-default sharing):
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" update-workflow <workflowId> --folder-id <folderId> [--name "..."] [--share-level Run]
```

Do moves one at a time and confirm each. After re-filing, list folders/workflows again to verify the new structure.

## Notes
- There's no bulk "move" endpoint — re-file workflows individually with `update-workflow`.
- You can also set folder **permissions**: `folder-permissions <folderId> --permissions '[{"email":"team@co.com","accessLevel":"Edit"}]'`.
- To delete an empty folder, use the Process Street UI (folder deletion isn't wired into this CLI). Re-filing its workflows first is the safe path.
