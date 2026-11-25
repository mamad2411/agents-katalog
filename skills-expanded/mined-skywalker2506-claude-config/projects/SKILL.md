---
name: projects
description: "List and inspect projects registered in projects.json — show paths, git repos, and status. Triggers: projects list, show projects, what projects, list all projects."
triggers: projects, list projects, show projects, project list, tum projeler, projeler
---

# /projects

List all projects registered in `~/Projects/ClaudeHQ/projects.json` with their paths, git repos, and active status.

## Usage

```
/projects              # list all active projects
/projects --all        # include archived/inactive
/projects <name>       # show details for one project
```

## Output

```
━━ Projects ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  #   Name              Path                        Git
  ──  ────────────────  ──────────────────────────  ─────  ─────────────────────────────────
  1   claude-config     ~/Projects/claude-config    CC     SkyWalker2506/claude-config
  2   ClaudeHQ          ~/Projects/ClaudeHQ         CHQ    SkyWalker2506/ClaudeHQ
  3   CoinHQ            ~/Projects/CoinHQ           CHQ    SkyWalker2506/CoinHQ
  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: N active projects
```

## Implementation

1. Read `~/Projects/ClaudeHQ/projects.json`
2. Filter by `active: true` (unless `--all`)
3. If project name argument given, show full detail block for that project
4. Print formatted table

## When NOT to Use
- User wants to create/add a new project → use `hq new`
- User wants to scan for new projects → use `hq scan`
