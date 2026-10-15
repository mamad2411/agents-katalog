---
name: pm-migration
description: Use when migrating tasks/issues between project management systems (ClickUp to Linear, Jira to Linear, etc). Handles status mapping, user mapping, and bulk task migration with confirmation workflow.
---

# Project Management Migration

Migrate tasks between project management systems with intelligent status mapping and user confirmation.

## Supported Migrations

| Source | Target | Status |
|--------|--------|--------|
| ClickUp | Linear | ✅ Implemented |
| Jira | Linear | 🔜 Planned |
| Asana | Linear | 🔜 Planned |

## Migration Workflow

```
1. DISCOVER     → Fetch source statuses and target workflow states
2. MAP          → Build status mapping (exact match + fuzzy + overrides)
3. CONFIRM      → Present mapping to user for approval
4. MIGRATE      → Execute migration with progress tracking
5. VERIFY       → Show summary and handle failures
```

## Quick Start

### ClickUp → Linear Migration

```bash
# Step 1: Show status mapping for approval
python .claude/skills/pm-migration/scripts/clickup_to_linear.py \
  --clickup-list-id 901317567354 \
  --linear-project-id ae2788e1-6e34-4a71-be49-31f9a48f8a9e \
  --show-mapping

# Step 2: Run migration (after confirming mapping)
python .claude/skills/pm-migration/scripts/clickup_to_linear.py \
  --clickup-list-id 901317567354 \
  --linear-project-id ae2788e1-6e34-4a71-be49-31f9a48f8a9e

# Optional: Custom status overrides
python .claude/skills/pm-migration/scripts/clickup_to_linear.py \
  --clickup-list-id 901317567354 \
  --linear-project-id ae2788e1-6e34-4a71-be49-31f9a48f8a9e \
  --override "inbox:Backlog" \
  --override "badges:Backlog"
```

## Status Mapping Logic

The migration uses a 3-tier mapping strategy:

1. **Explicit Overrides** - User-specified mappings (highest priority)
2. **Exact Match** - Case-insensitive name match
3. **Type-Based Fallback** - Maps by status type (open→backlog, closed→completed)

## Configuration

### Environment Variables

```bash
# ClickUp
CLICKUP_API_KEY=pk_xxx

# Linear
LINEAR_API_KEY=lin_api_xxx
```

### Status Override Format

```bash
--override "source_status:Target Status"

# Examples:
--override "inbox:Backlog"
--override "in dev:In Progress"
--override "ready for release:Done"
```

## What Gets Migrated

| Field | Migrated | Notes |
|-------|----------|-------|
| Title | ✅ | Truncated to 255 chars |
| Description | ✅ | Markdown preserved |
| Status | ✅ | Via mapping |
| Priority | ✅ | 1-4 scale (urgent→low) |
| Assignee | ✅ | Best effort by email |
| Due Date | ✅ | Unix timestamp → ISO date |
| Original URL | ✅ | Added to description |
| Original Assignee | ✅ | Added if no Linear match |

## Error Handling

- **Rate Limits**: Automatic 200ms delay between requests
- **API Errors**: Logged and counted, migration continues
- **Missing Users**: Original assignee noted in description
- **Free Tier Limits**: Script reports limit errors clearly

## Common Issues

### Linear Free Tier Limit
Linear free workspaces have issue limits. If migration fails partway:
1. Upgrade Linear workspace, or
2. Archive/delete completed issues to free slots
3. Re-run migration (script creates new issues, doesn't duplicate)

### Missing Status Mapping
If a ClickUp status doesn't map correctly:
1. Use `--show-mapping` to see current mapping
2. Add `--override "status:Target"` for corrections
3. Re-run migration

### User Mapping Failures
Linear must have users invited first. Unmapped assignees are noted in the issue description.

## Scripts Reference

```
scripts/
├── clickup_to_linear.py    # Main migration script
└── delete_linear_issues.py # Utility to clear Linear project
```

### clickup_to_linear.py

```
Usage: clickup_to_linear.py [OPTIONS]

Options:
  --clickup-list-id ID      ClickUp list to migrate from (required)
  --linear-project-id ID    Linear project to migrate to (required)
  --linear-team-id ID       Linear team (auto-detected if not set)
  --show-mapping            Show status mapping and exit
  --override KEY:VALUE      Status override (repeatable)
  --limit N                 Migrate only first N tasks
  --skip-completed          Skip tasks with 'completed' status
  -h, --help                Show help
```

### delete_linear_issues.py

```
Usage: delete_linear_issues.py --project-id ID [--dry-run | --confirm]

Deletes all issues from a Linear project. Use to reset before re-migration.

SAFETY: Requires --confirm flag AND typing 'DELETE ALL ISSUES' to execute.

Options:
  --dry-run     Preview what would be deleted (safe)
  --confirm     Enable deletion mode (still requires interactive confirmation)
```
