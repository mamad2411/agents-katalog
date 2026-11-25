---
name: install-github-plugin
description: "Installs Claude Code plugins from GitHub repos that lack a marketplace manifest. Use this skill whenever a `claude plugin install` fails due to SSH key errors, missing `.claude-plugin/marketplace.json`, or a GitHub repo that wasn't designed as a Claude plugin marketplace. Also use when the user says \"install plugin from GitHub\", \"add skills from a repo\", or \"the plugin install failed\". Handles the full workflow: cloning via gh CLI, inspecting repo structure, generating the marketplace manifest, and running the install."
---

# Install GitHub Plugin

## Overview

`claude plugin install` clones repos via SSH. If SSH auth isn't configured, or if the repo has no `.claude-plugin/marketplace.json` manifest, the install fails. This skill works around both problems.

## Workflow

### 1. Clone the repo via gh CLI (bypasses SSH)

```bash
gh repo clone <owner>/<repo> "~/.claude/plugins/marketplaces/<marketplace-name>"
```

Use the same directory the marketplace manager would have used (check `known_marketplaces.json` if the marketplace was already added).

### 2. Check for an existing manifest

```bash
ls "~/.claude/plugins/marketplaces/<name>/.claude-plugin/"
```

If `marketplace.json` exists, skip to step 4.

### 3. Inspect the repo structure and generate manifest

Common layouts to look for:
- `skills/<skill-name>/SKILL.md` — skill collection
- `agents/` — agent personas
- `hooks/` — session lifecycle hooks
- `.claude/commands/` — slash commands

Read one or two `SKILL.md` files to understand the content, then write `.claude-plugin/marketplace.json`:

```json
{
  "name": "<marketplace-name>",
  "owner": { "name": "<author>", "email": "" },
  "metadata": {
    "description": "<one-line description>",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "<plugin-name>",
      "description": "<what the plugin does>",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/<skill-1>",
        "./skills/<skill-2>"
      ]
    }
  ]
}
```

List every skill directory under `skills/` in the `skills` array.

### 4. Install the plugin

```bash
claude plugin install <plugin-name>@<marketplace-name>
```

### 5. Verify

```bash
claude plugin list
```

Confirm the plugin shows as `✔ enabled`.

## Notes

- If the marketplace was added via `claude plugin marketplace add` but the clone failed, the marketplace entry exists in `known_marketplaces.json` but the directory is empty or missing. Re-clone manually into the `installLocation` path shown there.
- Skills with only `SKILL.md` (no `plugin.json`) are bundled via the marketplace manifest's `skills` array — no per-skill plugin.json is needed.
- After install, a Claude restart is required for new skills to appear in the available-skills list.
