---
name: brain-query
description: |
  Query the claude-teams-brain for context about a specific role or topic
user_invocable: true
---

# brain-query

Preview exactly what memory a new teammate would receive when they spawn. Useful for debugging memory, verifying a role has context, or understanding what the brain knows before starting a session.

## Instructions

The user provides a role name as an argument (e.g. `/brain-query backend`).

Run:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py query-role "$ARGS" "$CLAUDE_PROJECT_DIR"
```

Display the returned context in a readable format, showing:
- Project rules and conventions injected into this role
- Past work completed by this role
- Key team decisions relevant to this role
- Files this role has worked on

## Role names

Use the same names as your agent teammates. Common roles:

| Role | Use for |
|------|---------|
| `backend` | API, server logic, middleware |
| `frontend` | UI, React/Vue components, CSS |
| `database` | Schema, migrations, queries |
| `tests` | Unit, integration, e2e tests |
| `devops` | Docker, CI/CD, deployment |
| `security` | Auth, permissions, encryption |
| `architect` | System design, refactoring |

The brain also auto-infers roles from task descriptions — an agent with no explicit role that worked on React components will have its memory tagged as "frontend" automatically.

## If no memory is found

Suggest:
1. Running an Agent Team session with a teammate using this role name
2. Using `/brain-remember` to manually seed rules for this role
3. Using `/brain-seed <profile>` to load stack conventions
