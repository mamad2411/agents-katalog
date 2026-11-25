# Linear API Skill

Manage Linear issues, boards, and cycles. Uses **Linear MCP** for standard operations and **plugin commands** for unique features.

## When to Use This Skill

Use this skill when the user wants to:
- View a kanban board of current tasks (`/linear:board`)
- Manage sprints/cycles and track velocity (`/linear:cycle`)
- Archive or delete issues (`/linear:delete`)
- Edit or delete comments (`/linear:comment`)
- Auto-enrich issues with code context (issue-enricher agent)

**For standard CRUD operations** (create, get, list, update, search issues, add comments, manage projects/teams), use the **Linear MCP tools** directly — they are provided by the official Linear MCP server.

**Trigger phrases for plugin commands:**
- "What's on the board?" / "Show kanban"
- "Current sprint status" / "Sprint velocity"
- "Archive issue TEAM-123"
- "Edit comment on TEAM-456"

## Architecture: MCP + Plugin

### Linear MCP (standard operations)

The official Linear MCP server (`mcp.linear.app`) provides ~21 tools:
- Issues: `list_issues`, `list_my_issues`, `get_issue`, `create_issue`, `update_issue`, `search`
- Projects: `list_projects`, `get_project`, `create_project`, `update_project`
- Teams: `list_teams`, `get_team`
- Users: `list_users`, `get_user`
- Comments: `list_comments`, `create_comment`
- Documents: `get_document`, `list_documents`, `search_documentation`
- Workflow: `list_issue_statuses`, `get_issue_status`, `list_issue_labels`
- Initiatives, milestones, project updates

### Plugin commands (unique features)

| Command | Feature |
|---------|---------|
| `/linear:board` | ASCII kanban board visualization |
| `/linear:cycle` | Cycle management with velocity stats |
| `/linear:delete` | Archive/delete issues |
| `/linear:comment` | Edit/delete comments (MCP only supports create) |

### issue-enricher agent

Analyzes codebase to auto-suggest issue attributes (description, labels, estimate, priority). Works with both MCP `create_issue` and `/linear:create` flows.

## Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LINEAR_API_KEY` | Personal API Key from Linear Settings > API | `lin_api_XXXXXXXXXXXX` |
| `LINEAR_TEAM` | Default team key | `ENG` |

Set in `~/.claude/settings.local.json`:

```json
{
  "env": {
    "LINEAR_API_KEY": "lin_api_XXXXXXXXXXXX",
    "LINEAR_TEAM": "ENG"
  }
}
```

### Linear MCP Setup

The MCP server is configured in `.mcp.json` at the repository root. It connects automatically when the plugin is installed.

To add manually: `claude mcp add --transport http linear-server https://mcp.linear.app/mcp`

### Smart Defaults (plugin commands)

- **Team**: `$LINEAR_TEAM` environment variable
- **Project**: `basename $(pwd)` — auto-detected from current directory

## API Pattern (for plugin commands)

Plugin commands use Linear's GraphQL API directly:

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "...", "variables": {...}}'
```

### Error Handling

1. Check `LINEAR_API_KEY` is set — show setup instructions if missing
2. Parse response with `jq`
3. Check for errors: `echo "$RESPONSE" | jq -e '.errors' > /dev/null 2>&1`
4. If errors exist, extract message: `echo "$RESPONSE" | jq -r '.errors[0].message'`

### Pagination

Linear uses cursor-based pagination:

```graphql
issues(first: 50, after: $cursor) {
  nodes { ... }
  pageInfo { hasNextPage endCursor }
}
```

Loop while `hasNextPage` is true, passing `endCursor` as `after`.

## References

- [GraphQL Queries](references/graphql-queries.md) — Queries for board, cycles, delete, and comment edit/delete
- [Filtering](references/filtering.md) — Filter syntax and operators
- [Workflow States](references/workflow-states.md) — Status model and transitions
