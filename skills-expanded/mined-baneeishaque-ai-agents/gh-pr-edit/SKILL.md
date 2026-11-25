---
name: gh-pr-edit
description: Generic protocol for viewing and editing GitHub PR title and body via gh CLI with multi-line body support.
category: GitHub Operations
---

# GitHub PR Edit Skill

Automates viewing and editing GitHub Pull Request details (title, body) using the `gh` CLI. Handles multi-line body text
by writing it to a temporary file, avoiding shell quoting issues with long bodies.

***

## 1. Environment & Dependencies

| Tool | Purpose | Verification |
| --- | --- | --- |
| `gh` (GitHub CLI 2.x+) | View and edit PRs | `gh --version` |
| `python3` (3.12+) | Script engine | `python3 --version` |

### 1.1 Authentication

The `gh` CLI MUST be authenticated with an account that has **write** access to the target repository:

```bash
gh auth status
```

If a different token is needed per-call, pass `--token <PAT>` to the script or set `GH_TOKEN` in the environment.

***

## 2. View Current PR State

Before editing, always view the current state to confirm the correct PR:

```bash
python3 scripts/gh-pr-edit.py view --pr <NUMBER> --repo <owner/repo>
```

Outputs JSON with `title`, `body`, `headRefName`, `number`, `url`, `state`, `author`.

***

## 3. Edit PR Title and/or Body

### 3.1 Update Title Only

```bash
python3 scripts/gh-pr-edit.py edit \
  --pr <NUMBER> \
  --repo <owner/repo> \
  --title "New PR Title"
```

### 3.2 Update Body Only

```bash
python3 scripts/gh-pr-edit.py edit \
  --pr <NUMBER> \
  --repo <owner/repo> \
  --body "Multi-line\nPR body text"
```

For very long bodies, pre-write to a file and use `--body-file`:

```bash
cat > /tmp/pr_body.md <<'BODY'
Line 1
Line 2
...
BODY

python3 scripts/gh-pr-edit.py edit \
  --pr <NUMBER> \
  --repo <owner/repo> \
  --body-file /tmp/pr_body.md
```

### 3.3 Update Title and Body Together

```bash
python3 scripts/gh-pr-edit.py edit \
  --pr <NUMBER> \
  --repo <owner/repo> \
  --title "New Title" \
  --body-file /tmp/body.md
```

### 3.4 GitHub API Fallback

If `gh pr edit` fails (e.g. the PR body exceeds CLI limits), fall back to the GitHub REST API:

```bash
gh api -X PATCH "repos/<owner>/<repo>/pulls/<NUMBER>" \
  --field title="New Title" \
  --field body="New body text" > /dev/null
```

***

## 4. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| *(none registered)* | |

Composers SHOULD call `scripts/gh-pr-edit.py` with the appropriate subcommand and pass through `--repo`, `--token` from
their own context.

***

## Related Skills

- [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) — when `gh` CLI is not authenticated
- [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) — REST API alternative when `gh` CLI is unavailable

***

## Environment & Dependencies

All dependencies: `gh` CLI, `python3`.

***

## Related Conversations & Traceability

- **Session 2026-06-09**: PR edit workflow — extracted from `<TICKET-ID>` traceability session. Protocol for editing
existing PRs to match standard format (`Epic <TICKET-ID> - Task <TICKET-ID>: <title>`).
