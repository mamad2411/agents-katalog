---
name: makecli
description: "Use when the user asks to manage Make platform resources with makecli — create/deploy apps, entities, relations, records, inspect resources, or run makecli CLI commands. Also triggered by requests like \"部署\", \"apply\", \"查看应用\", \"创建记录\", or \"/makecli\". Does not own DSL schema design (use makedsl), frontend UI (makeui), auth (make-app-auth), Service/API code (make-app-service), runtime packaging (make-app-runtime), OCR integration (make-integration), or canvas-table behavior."
---

# makecli — Make Platform CLI

makecli is the CLI for the Make agentic development platform.
It manages Apps, Entities, Relations, and Records via Meta/Data Services.

## Installation

```bash
brew tap qfeius/makecli
brew install makecli
```

## Pre-flight Check

Before executing ANY makecli command, verify the environment:

0. Check `makecli` is installed
   - Missing: run the installation commands above

1. Run `makecli configure verify --output=json` to check token status
   - Not configured: user must run `makecli configure token`
   - **INTERACTIVE** (masked input) — instruct user to run via `!`

## Decision Tree

```
User request arrives
    |
    +- makecli not installed? --> Installation above
    |
    +- Environment not configured? --> Pre-flight Check above
    |
    +- Create/update schema (app, entity, relation)?
    |   --> Declarative Workflow (preferred)
    |
    +- Delete resource / one-off operation?
    |   --> Imperative Workflow
    |
    +- Query / inspect?
        --> Direct list/get commands
```

## Workflow: Declarative Deployment (Primary)

**When:** Creating or updating schema resources (App, Entity, Relation).
**Why preferred:** Reproducible, diffable, safe (preview before apply).

1. **Write** DSL YAML — invoke the `makedsl` skill for schema reference
2. **Diff:** `makecli diff -f <path>` — preview changes against remote
3. **Confirm** diff output with user
4. **Apply:** `makecli apply -f <path>` — deploy changes
5. **Verify:** `makecli entity list --app <name>` or `makecli relation list --app <name>`

Key rules:
- Semantics: create if new, update if exists
- diff exit code: 0 = no differences, 1 = differences found

## Workflow: Imperative Operations

**When:** Single deletions, operations not supported by apply, or user preference.

Read `@references/cli-reference.md` for exact flag syntax.

Common imperative operations:
```bash
# App
makecli app create [name] [--description <desc>] [--render-name <display>] [-f app.yaml]
makecli app delete <name>
makecli app list [--output json]

# Entity (requires --app)
makecli entity create <name> --app <app> [--json fields.json]
makecli entity delete <name> --app <app>
makecli entity list [<name>] --app <app>

# Relation (requires --app)
makecli relation create <name> --app <app> --json relation.json
makecli relation update <name> --app <app> --json relation.json
makecli relation delete <name> --app <app>
makecli relation list [<name>] --app <app>
```

## Workflow: Environment Configuration

```bash
# Step 1: Set access token (INTERACTIVE -- user must run via !)
! makecli configure token

# Step 2: Set server URL and headers (if non-default)
makecli configure set server-url https://your-server.com/api/make
makecli configure set X-Tenant-ID <tenant>
makecli configure set X-Operator-ID <operator>

# Verify
makecli configure get server-url
```

**Profiles:** All commands accept `--profile <name>` (default: "default").
**Config files:** `~/.make/credentials` and `~/.make/config` (INI format).

## Common Patterns

**From zero to deployed app:**
```bash
# 1. Configure (user runs interactively)
! makecli configure token

# 2. Write DSL (use makedsl skill for schema reference)
# 3. Preview -> Deploy -> Verify
makecli diff -f app.yaml
makecli apply -f app.yaml
makecli entity list --app MyApp
```

**Inspect remote state:**
```bash
makecli app list
makecli entity list --app <app>
makecli entity list <entity-name> --app <app>    # detail view with fields
makecli relation list --app <app>
```

**Initialize AI provider config in project directory:**
```bash
makecli app init <folder> --provider anthropic    # creates CLAUDE.md
makecli app init <folder> --provider openai       # creates AGENTS.md
makecli app init <folder> --provider google       # creates GEMINI.md
makecli app init <folder> --provider cursor       # creates .cursorrules
```

**Self-update:**
```bash
makecli update
makecli version
```

## Anti-Patterns

- **Don't skip diff before apply.** Always preview changes first.
- **Don't use imperative commands for bulk schema setup.** Use YAML + apply instead.
- **Don't guess CLI flags.** Read `@references/cli-reference.md` if unsure.
- **Don't run `configure token` or `configure config` via Bash tool.** These are interactive — tell user to run via `!`.
- **Don't write DSL YAML from memory.** Invoke the `makedsl` skill for schema reference.
