---
name: use-glab
description: Manages GitLab merge requests using the glab CLI — creation, viewing, merging, and commenting (top-level and inline). Use when creating MRs, posting comments, merging, or any glab mr operation.
compatibility: Requires glab CLI (brew install glab) and GitLab authentication
---

# glab

## Essential Principles

- **Always squash commits** via `--squash-before-merge` on create or `--squash` on merge
- **Always delete source branch** via `--remove-source-branch` on create or `-d` on merge
- **Use MR templates** when `.gitlab/merge_request_templates/` exists in the repo
- **Inline comments require `glab api`** — `glab mr note` only posts top-level comments
- **API path placeholder:** Use `:fullpath` (not `:id`) for project reference in `glab api` calls

## Prerequisites

```bash
command -v glab >/dev/null 2>&1
```

If not found: `brew install glab`.

Verify authentication:

```bash
glab auth status
```

If not authenticated: `glab auth login`.

## Quick Start

```bash
glab mr create --title "[PROJ-123] Feature title" --squash-before-merge --remove-source-branch --push
glab mr merge <ID> --squash --remove-source-branch --yes  # use --yes only after user confirms
glab mr note <ID> -m "Comment"                             # top-level comment
glab api "projects/:fullpath/merge_requests/<IID>/discussions" --method POST --input comment.json  # inline comment
```

## MR Creation

### Step 1: Detect MR Templates

```bash
ls .gitlab/merge_request_templates/ 2>/dev/null
```

If templates exist: list them and ask user which applies. Use `default.md` if present and user doesn't specify. Read the chosen template and use its content as the `--description` value.

### Step 2: Create MR

```bash
glab mr create \
  --title "[PROJ-123] Feature title" \
  --description "<template content or description>" \
  --target-branch main \
  --squash-before-merge \
  --remove-source-branch \
  --push
```

| Flag | Purpose |
|------|---------|
| `--title` | `[TICKET-KEY] Title` format — always include ticket prefix |
| `--squash-before-merge` | Squash commits into one on merge |
| `--remove-source-branch` | Delete branch after merge |
| `--push` | Push branch to remote before creating MR — required if branch not yet pushed |
| `--draft` | Mark as draft if work-in-progress |
| `--reviewer` | Request reviewers by username (comma-separated) |
| `--label` | Add labels (comma-separated) |
| `--assignee` | Assign to user(s) by username (comma-separated) |

**Do NOT use `--related-issue` with Jira ticket IDs** — it expects GitLab issue numbers.

## MR View and Merge

### View MR

```bash
glab mr view <ID> -F json    # structured data (includes diff_refs)
glab mr view <ID> -c          # with comments
glab mr diff <ID>             # view diff
```

### Approve and Merge

```bash
glab mr approve <ID>
glab mr merge <ID> --squash --remove-source-branch --squash-message "<MR title>"
```

`--squash-message` defaults to the MR title. Set explicitly if the default doesn't match.

## Comments

### Top-Level Comment

```bash
glab mr note <ID> -m "Comment text"
```

### Inline Comment (File + Line)

Inline comments require the GitLab Discussions API via `glab api`.

**Step 1 — Get diff refs:**

```bash
glab mr view <ID> -F json
```

Extract `diff_refs.base_sha`, `diff_refs.start_sha`, `diff_refs.head_sha` from the JSON output.

**Step 2 — Write comment JSON to temp file:**

```json
{
  "body": "Comment text here",
  "position": {
    "base_sha": "<BASE_SHA>",
    "start_sha": "<START_SHA>",
    "head_sha": "<HEAD_SHA>",
    "position_type": "text",
    "new_path": "src/file.ts",
    "new_line": 42
  }
}
```

| Position field | When to use |
|----------------|-------------|
| `new_path` + `new_line` | Added or changed lines |
| `old_path` + `old_line` | Deleted lines (omit `new_path`/`new_line`) |
| Both `old_path` + `new_path` | Renamed files |

**Step 3 — Post via API:**

```bash
glab api "projects/:fullpath/merge_requests/<MR_IID>/discussions" \
  --method POST \
  -H "Content-Type: application/json" \
  --input /tmp/glab-comment.json
```

**If post fails:** Verify line number exists in file at HEAD_SHA, or SHAs are current after rebase. Re-fetch `diff_refs` and retry if stale.

## Other Operations

| Operation | Command |
|-----------|---------|
| List open MRs | `glab mr list` |
| List my MRs | `glab mr list --author=@me` |
| List MRs for review | `glab mr list --reviewer=@me` |
| Close MR | `glab mr close <ID>` |
| Reopen MR | `glab mr reopen <ID>` |
| Update MR | `glab mr update <ID> --title "..." --label "..."` |
| Mark ready | `glab mr update <ID> --ready` |
| Mark draft | `glab mr update <ID> --draft` |
| Rebase MR | `glab mr rebase <ID>` |
| Compare commits | `glab api "projects/:fullpath/repository/compare?from=<SHA>&to=<SHA>"` |

## Success Criteria

- Squash and delete-source-branch set on every MR create and merge
- MR templates used when available in the repo
- Inline comments posted via `glab api` with correct position data
- User confirmed before any mutation (create, merge, comment) — only pass `--yes` after explicit user approval
