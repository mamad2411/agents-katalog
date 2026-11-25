---
name: draxarp
description: Manage Draxarp Intelligence — projects, tasks, specs, docs, memories, sprints, knowledge graph, context captures, and task decomposition via orbit CLI
triggers:
  - draxarp
  - intelligence
  - development intelligence
  - second brain
  - knowledge base
  - project memory
  - list projects
  - create task
  - create spec
  - create memory
  - sync docs
  - documentation
  - list memories
  - list tasks
  - list specs
  - list docs
  - doc toc
  - store memory
  - architecture decision
  - design pattern
  - domain knowledge
  - task focus
  - task handoff
  - task context
  - activity log
  - task dependencies
  - sprint
  - sprint planning
  - velocity
  - knowledge graph
  - impact analysis
  - decompose task
  - context capture
---

# Draxarp Intelligence — orbit CLI

Alias: `dx`

The `orbit draxarp` (or `orbit dx`) command manages the Draxarp Development Intelligence module — a second brain for LLM-assisted development. It covers nine resource types:

## Resources

| Resource | Alias | Description |
|----------|-------|-------------|
| `project` | `proj` | Intelligence projects — group tasks, specs, memories, and docs |
| `task` | — | Development tasks with status, priority, activity logs, handoffs, focus, and dependencies |
| `memory` | `mem` | Persistent knowledge — patterns, bugs, decisions, domain context |
| `spec` | — | Specifications with review workflow (draft → review → approved/rejected) |
| `doc` | — | Technical documentation with slug-based addressing and wikilink support |
| `sprint` | — | Sprint planning with velocity tracking and AI content suggestions |
| `capture` | `cap` | Context captures — git commits, PRs, CI events, deployments |
| `graph` | `kg` | Knowledge graph — nodes, edges, impact analysis, subgraph, path finding |
| `decompose` | — | AI-powered task decomposition from descriptions |

## Quick Reference

### Projects
```bash
orbit dx proj ls                              # List projects
orbit dx proj view <id-or-slug>               # View project details
orbit dx proj create --name "My Project"      # Create project
orbit dx proj delete <id>                     # Delete project
```

> **Slugs everywhere:** All `--project` flags and resource IDs accept either UUIDs or slugs.
> Use slugs for readability: `--project draxarp-portal` instead of `--project 019cf38c-...`

### Tasks — Core CRUD
```bash
orbit dx task ls --project <id>               # List tasks for a project
orbit dx task ls --status in_progress         # Filter by status
orbit dx task ls --type epic --project <id>   # List only epics
orbit dx task ls --parent <epic-id>           # List children of an epic
orbit dx task view <id>                       # View task details + last 5 activity logs
orbit dx task create --title "Fix bug" --project <id> --priority high
orbit dx task create --title "Wire frontend" --project <id> --depends-on <blocker-id>
orbit dx task create --title "Auth" --project <id> --type epic      # Create an epic
orbit dx task create --title "JWT" --project <id> --type story --parent <epic-id>  # Story under epic
orbit dx task update <id> --status testing --activity "Running PHPUnit"
orbit dx task assign <id> --assignee claude   # Assign task
orbit dx task start <id>                      # Set status to in_progress
orbit dx task complete <id>                   # Mark completed (with guard checks)
orbit dx task delete <id>                     # Delete task
orbit dx task epic <id>                       # Show epic progress (% complete, children)
```

Task types: `task` (default), `epic`, `story`

### Tasks — Focus & Next (session management)
```bash
orbit dx task focus <id>                      # One command: assign + start + set focus
orbit dx task focus <id> --agent claude       # Specify agent (default: claude)
orbit dx task current                         # Show currently focused task
orbit dx task current --agent claude          # For a specific agent
orbit dx task next --project <id>             # Next available task by priority (skips epics & blocked)
```

### Tasks — Activity Logs
```bash
orbit dx task log <id> "Implemented API endpoints" --tag progress
orbit dx task log <id> "Blocked on DB schema" --tag blocker --agent claude
orbit dx task log <id> "Chose approach A over B" --tag decision
orbit dx task logs <id>                       # List all logs (newest first)
orbit dx task logs <id> --tag blocker         # Filter by tag
orbit dx task logs <id> --limit 10            # Limit results
orbit dx task logs <id> -o json               # JSON output
```

Activity log tags: `progress`, `blocker`, `decision`, `hypothesis`, `tried`, `result`, `handoff`, `note`

### Tasks — Structured Handoffs & Context
```bash
# Record a handoff (session continuity)
orbit dx task handoff <id> \
  --done "Implemented X" --done "Added tests for Y" \
  --remaining "Wire up frontend" --remaining "Add error handling" \
  --decision "Used approach A because of constraint B" \
  --uncertain "Not sure if Z is the right abstraction" \
  --files "backend/Services/Foo.php,frontend/Show.tsx" \
  --agent claude

# Get AI-optimized context for resuming work
orbit dx task context <id>                    # Human-readable
orbit dx task context <id> -o json            # Structured JSON
```

### Tasks — Dependencies
```bash
orbit dx task dep <id> --on <blocking-task-id>    # Add dependency
orbit dx task deps <id>                            # Show dependency tree (blocks/blocked-by)
orbit dx task deps <id> -o json                    # JSON output
```

Task statuses: `pending`, `in_progress`, `testing`, `completed`, `blocked`, `cancelled`
Task priorities: `low`, `medium`, `high`, `critical`

### Memories
```bash
orbit dx mem ls --project <id>                # List memories
orbit dx mem ls --type architecture           # Filter by type
orbit dx mem view <id>                        # View memory content
orbit dx mem create --title "Pattern: Repo" --content "..." --project <id> --type patterns
orbit dx mem archive <id>                     # Archive memory
```

Memory types: `architecture`, `patterns`, `bugs`, `domain`, `decisions`, `preferences`, `context`

### Specs
```bash
orbit dx spec ls --project <id>               # List specs
orbit dx spec view <id>                       # View spec content
orbit dx spec create --title "Auth Spec" --content "..." --project <id>
orbit dx spec submit <id>                     # Submit for review
orbit dx spec approve <id>                    # Approve spec
orbit dx spec reject <id>                     # Reject spec
orbit dx spec delete <id>                     # Delete spec
```

Spec statuses: `draft`, `in_review`, `approved`, `rejected`

### Docs
```bash
orbit dx doc ls                               # List all docs
orbit dx doc ls --category architecture       # Filter by category
orbit dx doc toc                              # Table of contents (no content)
orbit dx doc view <id>                        # View doc by ID
orbit dx doc view architecture/overview       # View by slug (auto-detected)
orbit dx doc create --title "API Guide" --category api --slug api/guide
orbit dx doc sync docs.json                   # Batch sync from JSON file
orbit dx doc publish <id>                     # Publish draft doc
orbit dx doc archive <id>                     # Archive doc
orbit dx doc delete <id>                      # Delete doc
```

Doc categories: `architecture`, `components`, `flows`, `security`, `api`, `infrastructure`, `general`
Doc statuses: `draft`, `published`, `archived`

**Slug auto-detection:** `doc view` automatically detects whether the argument is a UUID or slug — no `--slug` flag needed (though it's still supported for explicit override).

**Batch sync:** `doc sync` accepts a JSON file with an array of doc objects:
```json
[{"slug": "api/guide", "title": "API Guide", "content": "...", "category": "api"}]
```
Existing docs (matched by slug) are updated; new slugs are created.

### Sprints
```bash
orbit dx sprint ls --project <id>             # List sprints
orbit dx sprint view <id>                     # View sprint details
orbit dx sprint create --project <id> --name "Sprint 1" --starts-at 2026-03-16 --ends-at 2026-03-30
orbit dx sprint create --project <id> --name "Sprint 2" --starts-at 2026-03-30 --ends-at 2026-04-13 --goal "Ship auth" --velocity-target 20
orbit dx sprint start <id>                    # Start a sprint
orbit dx sprint complete <id>                 # Complete a sprint
orbit dx sprint suggest <id>                  # AI-powered sprint content suggestions
orbit dx sprint velocity --project <id>       # Velocity history (last 5 sprints)
orbit dx sprint velocity --project <id> --count 10  # More history
```

### Context Captures
```bash
orbit dx capture ls --project <id>            # List captures for a project
orbit dx capture view <id>                    # View capture details + payload
orbit dx capture webhook --project <id> --source git_commit --payload '{"sha":"abc","message":"fix"}'
orbit dx capture persist <id>                 # Persist capture as a memory
```

Context sources: `git_commit`, `git_pr`, `ci_pipeline`, `deployment`, `code_review`, `manual`

### Knowledge Graph
```bash
# Nodes
orbit dx graph nodes --project <id>           # List nodes
orbit dx graph nodes --type module            # Filter by type
orbit dx graph node <id>                      # View node details
orbit dx graph create-node --project <id> --type module --name "AuthService"
orbit dx graph delete-node <id>               # Delete a node

# Edges
orbit dx graph create-edge --from <id> --to <id> --relationship depends_on
orbit dx graph delete-edge <id>               # Delete an edge

# Analysis
orbit dx graph impact <node-id>               # Impact analysis (depth 3)
orbit dx graph impact <node-id> --depth 5     # Deeper analysis
orbit dx graph subgraph <node-id>             # Local subgraph (depth 2)
orbit dx graph paths --from <id> --to <id>    # Find paths between nodes
orbit dx graph paths --from <id> --to <id> --max-depth 8
```

### Task Decomposition
```bash
orbit dx decompose create --project <id> --description "Build user auth with JWT"
orbit dx decompose create --project <id> --description "..." --spec <spec-id>  # With spec context
orbit dx decompose ls --project <id>          # List decompositions
orbit dx decompose view <id>                  # View decomposition + options
orbit dx decompose accept <id> --indexes 0,1,2  # Accept and create tasks from selected options
orbit dx decompose reject <id>                # Reject decomposition
```

## Typical Agent Workflow

```bash
# 1. Orient
orbit dx context -p draxarp --project <id>

# 2. Pick up or create task
orbit dx task next --project <id> -p draxarp     # Or create new
orbit dx task focus <task-id> -p draxarp          # One command: assign + start + focus

# 3. Work (hooks auto-log progress)
# ... edit files, run tests ...

# 4. Log key decisions/blockers manually
orbit dx task log <id> "Chose X because Y" --tag decision -p draxarp
orbit dx task log <id> "Blocked on Z" --tag blocker -p draxarp

# 5. Handoff before session ends
orbit dx task handoff <id> --done "API done" --remaining "Frontend" --agent claude -p draxarp

# 6. Complete
orbit dx task complete <id> -p draxarp

# 7. Next session picks up with context
orbit dx task context <id> -p draxarp
```

## Configuration

Add to `~/.config/orbit/config.yaml`:
```yaml
profiles:
  - name: my-project
    services:
      - name: draxarp
        type: draxarp
        base_url: https://your-draxarp-instance.com
        auth:
          method: token
          token: "your-api-token"
        headers:                              # Optional custom headers
          X-Tenant: my-tenant-slug            # Required for tenant-scoped access
```

For multi-tenant setups, the `X-Tenant` header scopes all API responses to that tenant's workspaces and projects. Tokens can be either platform admin (Sanctum) or tenant user (PAT) tokens.

## Profile Selection

Use `-p <profile>` to target a specific profile:
```bash
orbit dx proj ls -p draxarp
orbit dx task ls -p draxarp --project <id>
```

## JSON Output

All commands support `-o json` for machine-readable output:
```bash
orbit dx proj ls -o json
orbit dx mem view <id> -o json
orbit dx doc toc -o json
orbit dx task context <id> -o json
orbit dx sprint ls --project <id> -o json
orbit dx graph nodes --project <id> -o json
```

## API Details

The orbit CLI communicates with the Draxarp API at:
- Intelligence resources: `/api/admin/v1/intelligence/*` (tasks, memories, specs, docs, sprints, graph, captures, decompose)
- Platform resources: `/api/admin/v1/*` (projects, workspaces)
- Auth: `Authorization: Bearer <token>` (platform-api or tenant-api Sanctum guard)
- Tenant scoping: `X-Tenant: <slug>` header (required for tenant-bound tokens)
- Pagination: `{ "success": true, "data": [...], "meta": { "current_page", "last_page", "per_page", "total" } }`
- Single resource: `{ "success": true, "data": { ... } }`
