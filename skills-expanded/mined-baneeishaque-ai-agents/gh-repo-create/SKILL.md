---
name: gh-repo-create
description: Base skill — wrap `gh repo create` with structured arguments for source directory, visibility, remote name, and push flag. Pure Python subprocess wrapper consumed by higher-level publish composers.
category: GitHub-Automation
---

# GitHub Repo Create Skill (v1)

> **Skill ID:** `gh-repo-create`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../skill-factory/SKILL.md))

## 1. When to Apply

Use this skill whenever the agent must **create a new GitHub repository** via the `gh` CLI, such as:

- "Create a new private repo for this project."
- "Publish this local directory as a new GitHub repo."
- Pre-requisite step in a higher-level publish workflow.

**Anti-trigger:** If the repo already exists and you only need to edit its metadata, use [`gh-repo-edit-metadata`](../gh-repo-edit-metadata/SKILL.md) instead. If you need the full publish workflow (repo creation + file population + metadata), use [`github-repo-publish`](../github-repo-publish/SKILL.md).

## 2. Why a Separate Skill

Repo creation is a single atomic operation with well-defined flags. Making it a base skill means:

- Higher-level composers (`github-repo-publish`, custom scripts) can invoke it without re-deriving the `gh repo create` command.
- Error handling (missing `gh`, auth failures, API errors) is centralized.
- The script is testable in isolation.

## 3. Environment & Dependencies

| Tool | Purpose | Verification |
|---|---|---|
| `gh` (GitHub CLI 2.x+) | Repo creation | `gh --version` |
| `python3` (3.10+) | Script engine | `python3 --version` |

### 3.1 Authentication

The `gh` CLI MUST be authenticated with `repo` scope:

```bash
gh auth status
```

Expected: `Logged in to github.com as <username>`. If absent, run `gh auth login`.

## 4. Operational Logic

### 4.1 Script Catalogue

| Script | Purpose | Required Args |
|---|---|---|
| [`scripts/gh-repo-create.py`](scripts/gh-repo-create.py) | Create a GitHub repo via `gh repo create` | `--repo <owner/name>` |

### 4.2 Invocation

```bash
python3 .agents/skills/gh-repo-create/scripts/gh-repo-create.py \
    --repo octocat/hello-world \
    --source /path/to/project \
    --visibility private \
    --remote origin \
    --push
```

**Flag-by-flag breakdown:**

| Flag | Default | Purpose |
|---|---|---|
| `--repo` | required | Target repository in `OWNER/NAME` format |
| `--source` | `.` | Local directory to use as repo source |
| `--visibility` | `private` | Visibility: `public`, `private`, or `internal` |
| `--remote` | `origin` | Name for the Git remote created locally |
| `--push` | `true` | Push local commits after creation; pass `--no-push` to skip |

### 4.3 Output

On success, prints JSON to stdout:

```json
{"repo": "octocat/hello-world", "url": "https://github.com/octocat/hello-world", "created": true}
```

On failure, prints diagnostics to stderr and exits non-zero.

### 4.4 Exit Codes

| Code | Meaning |
|---|---|
| `0` | Repo created (or already existed with matching settings) |
| `1` | `gh` CLI missing, auth failure, or API error |
| `2` | Config error (missing `--repo`) |

## 5. Prohibited Behaviors

- Calling `gh repo create` directly from prose instead of invoking this skill's script.
- Hard-coding visibility, source, or remote name in scripts — those are caller decisions.
- Creating a repo without first checking `gh auth status` unless auth was verified upstream.
- Pushing to a remote that already exists without confirming the user's intent.

## 6. Composition by Higher-Level Skills

| Composer | Purpose |
|----------|---------|
| [`github-repo-publish`](../github-repo-publish/SKILL.md) | C7 — calls this skill during publish orchestration |

## 7. Related Skills

- [`gh-repo-edit-metadata`](../gh-repo-edit-metadata/SKILL.md) — edit description and topics after creation
- [`github-repo-template`](../github-repo-template/SKILL.md) — populates a repo with standard files before push
- [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) — when `gh` is not authenticated
- [`github-repo-name-conflict-check`](../github/repo/github-repo-name-conflict-check/SKILL.md) — check
  destination name availability before creation (owner-token per-name lookups)
