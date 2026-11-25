---
name: create-marketplace-local
description: Scaffold a vanilla local Claude Code skill marketplace folder with .claude-plugin/marketplace.json
argument-hint: "<dir_name>"
allowed-tools: Bash, Write
---

# Create Local Skill Marketplace

Scaffold a new local Claude Code skill marketplace directory with the required `.claude-plugin/marketplace.json` structure.

## Input

- **$0** (required): Directory path for the new marketplace (absolute or relative to `$HOME`).
  - Examples: `~/my-marketplace`, `~/projects/team-skills`, `my-marketplace`
  - If no leading `/` or `~/`, resolve relative to `$HOME`.

## Workflow

### Step 1: Parse & Validate Arguments

1. Extract `dir_name` from `$0`. If missing, print usage and stop:
   ```
   Usage: /create-marketplace-local <dir_name>
   Example: /create-marketplace-local ~/my-marketplace
   ```

2. Expand `~` to `$HOME` if present. If path is relative (no leading `/`), prepend `$HOME/`.

3. Derive `marketplace_name` from the final path component (basename):
   - Lowercase the basename
   - Replace spaces and underscores with hyphens
   - Strip characters that are not `[a-z0-9-]`
   - Collapse multiple hyphens
   - Example: `My Cool Skills` → `my-cool-skills`

4. Check that `marketplace_name` is not one of the reserved names:
   `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`,
   `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`,
   `knowledge-work-plugins`, `life-sciences`.
   If reserved, stop with:
   ```
   ❌ "<marketplace_name>" is a reserved marketplace name. Choose a different directory name.
   ```

5. Check if the target directory already exists (using Bash `test -d <dir>`):
   - If it exists AND `.claude-plugin/marketplace.json` already exists inside it, stop with:
     ```
     ❌ Marketplace already exists at <dir_name>. Remove it first or choose a different name.
     ```
   - If the directory exists but has no `marketplace.json`, continue (will scaffold into it).

### Step 2: Create Directory Structure

Run via Bash:
```bash
mkdir -p "<dir_name>/.claude-plugin"
```

### Step 3: Write marketplace.json

Write the following file to `<dir_name>/.claude-plugin/marketplace.json`, substituting `marketplace_name`:

```json
{
  "name": "<marketplace_name>",
  "owner": {
    "name": "<your-name>"
  },
  "metadata": {
    "description": "Local skill marketplace",
    "version": "1.0.0"
  },
  "plugins": []
}
```

Set `<your-name>` to the system username from `$USER` (via Bash).

### Step 4: Output Summary

```
✅ Marketplace scaffolded!

📁 <dir_name>/
└── .claude-plugin/
    └── marketplace.json

Marketplace name : <marketplace_name>
Owner            : <your-name>

Next steps:
  • Copy skill folders into <dir_name>/
  • Add a plugin entry to marketplace.json for each skill:

      {
        "name": "<plugin-name>",
        "description": "...",
        "source": "./",
        "strict": false,
        "skills": ["./skill-folder-name"]
      }

  • Register with Claude Code:
      /plugin marketplace add <dir_name>

  • Install a plugin:
      /plugin install <plugin-name>@<marketplace_name>
```

## Error Handling

| Error | Action |
|-------|--------|
| Missing `$0` | Print usage and stop |
| Reserved marketplace name | Stop with clear message |
| `marketplace.json` already exists | Stop with clear message |
| `mkdir` fails (permissions etc.) | Surface the shell error and stop |
