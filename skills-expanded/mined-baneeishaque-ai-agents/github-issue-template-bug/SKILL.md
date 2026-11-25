---
name: github-issue-template-bug
description: Base skill — writes `.github/ISSUE_TEMPLATE/bug.yml` for standardized Bug Report issue templates in GitHub repositories.
category: GitHub-Community
---

# GitHub Issue Template — Bug Skill (v1)

> **Skill ID:** `github-issue-template-bug`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## 1. When to Apply

Use this skill — or a higher-level composer of it — whenever the agent must scaffold a **Bug Report** issue template into a GitHub repository. Typical triggers:

- "Add a bug report template to the repo."
- "Set up GitHub issue templates for the project."
- "Create the standard bug template in `.github/ISSUE_TEMPLATE/`."

**Anti-pattern:** If the agent needs a **Feature Request** or **Documentation Request** template instead, use the respective sibling skills. This skill deals exclusively with `bug.yml`.

## 2. Environment

- Python 3.10+ (`python3` on PATH, or resolve via `mise` per workspace convention).
- The target repository directory (default: current working directory).
- Write permission to create `.github/ISSUE_TEMPLATE/bug.yml`.

## 3. Operational Logic

### 3.1 Script catalogue

| Script | Purpose | Required args | Behavior |
|---|---|---|---|
| [`scripts/write-bug-template.py`](scripts/write-bug-template.py) | Generate `bug.yml` with Description, Steps to Reproduce, Expected/Actual Behavior, and Environment fields. | `--repo-root <path>` (default `.`) | Writes file to `<repo-root>/.github/ISSUE_TEMPLATE/bug.yml`. Prints confirmation to stdout. Exits 0 on success, 1 on error. |

### 3.2 Invocation example

```bash
# Write to current directory
python3 .agents/skills/github-issue-template-bug/scripts/write-bug-template.py

# Write to a specific repo
python3 .agents/skills/github-issue-template-bug/scripts/write-bug-template.py --repo-root /path/to/repo
```

### 3.3 Exit codes

| Code | Meaning |
|---|---|
| `0` | Template written successfully |
| `1` | Filesystem error (permissions, disk full, etc.) |

## 4. Composition by Higher-Level Skills

| Composer | Purpose |
|----------|---------|
| [`github-repo-templates`](../github-repo-templates/SKILL.md) | C1 — calls this skill as part of the template set |


