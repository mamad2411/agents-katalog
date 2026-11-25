---
name: gh-repo-edit-metadata
description: Base skill — wrap `gh repo edit` for description and topic management on an existing GitHub repository. Pure Python subprocess wrapper consumed by higher-level publish composers.
category: GitHub-Automation
---

# GitHub Repo Edit Metadata Skill (v1)

> **Skill ID:** `gh-repo-edit-metadata`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../skill-factory/SKILL.md))

## 1. When to Apply

Use this skill whenever the agent must **edit a GitHub repository's description or topics** via the `gh` CLI, such as:

- "Set the repo description to explain what this project does."
- "Add topics `agent-skills` and `devops` to the repo."
- Post-publish step in a higher-level workflow.

**Anti-trigger:** If the repo does not exist yet, use [`gh-repo-create`](../gh-repo-create/SKILL.md) first. If you need the full publish workflow, use [`github-repo-publish`](../github-repo-publish/SKILL.md).

## 2. Environment & Dependencies

| Tool | Purpose | Verification |
|---|---|---|
| `gh` (GitHub CLI 2.x+) | Metadata editing | `gh --version` |
| `python3` (3.10+) | Script engine | `python3 --version` |

### 2.1 Authentication

```bash
gh auth status
```

## 3. Operational Logic

### 3.1 Script Catalogue

| Script | Purpose | Required Args |
|---|---|---|
| [`scripts/gh-repo-edit-metadata.py`](scripts/gh-repo-edit-metadata.py) | Edit repo description and/or topics | `--repo <owner/name>` |

### 3.2 Invocation

```bash
python3 .agents/skills/gh-repo-edit-metadata/scripts/gh-repo-edit-metadata.py \
    --repo octocat/hello-world \
    --description "My project description" \
    --add-topic agent-skills \
    --add-topic devops
```

**Flag-by-flag breakdown:**

| Flag | Purpose |
|---|---|
| `--repo` | Target repository in `OWNER/NAME` format |
| `--description` | New repository description |
| `--add-topic` | Topic to add (repeatable for multiple topics) |
| `--remove-topic` | Topic to remove (repeatable) |

### 3.3 Output

On success, prints JSON to stdout:

```json
{"repo": "octocat/hello-world", "description": "My project description", "add_topics": ["agent-skills", "devops"], "changed": true}
```

### 3.4 Exit Codes

| Code | Meaning |
|---|---|
| `0` | Metadata updated (or no changes requested) |
| `1` | `gh` CLI missing, auth failure, or API error |
| `2` | Config error (missing `--repo`) |

### 3.5 No-Op Guard

If neither `--description`, `--add-topic`, nor `--remove-topic` is passed, the script prints a warning to stderr, outputs `{"changed": false}`, and exits 0.

## 4. Prohibited Behaviors

- Editing metadata without confirming the repo name with the user first.
- Removing existing topics without explicit user authorization.
- Passing an empty `--description` to clear the description without asking.

## 5. Composition by Higher-Level Skills

| Composer | Purpose |
|----------|---------|
| [`github-repo-publish`](../github-repo-publish/SKILL.md) | C7 — calls this skill during publish orchestration |

## 6. Related Skills

- [`gh-repo-create`](../gh-repo-create/SKILL.md) — companion base skill for repo creation
- [`github-sync`](../github-sync/SKILL.md) — automated metadata sync via CI workflow
