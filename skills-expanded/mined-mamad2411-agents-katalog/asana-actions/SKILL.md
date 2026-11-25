---
name: asana-actions
description: "Manage Asana tasks, projects, and workspaces. Create, view, update, delete, move tasks. Search by assignee/tags/due date. Add comments, manage dependencies, track project status. Export reports to Google Docs."
---

# Asana Actions Skill

> **Prerequisite**: Run the `asana-authentication` skill first to set up the Asana MCP connection.

## How It Works

All Asana operations use the **Asana MCP V2 server** as the primary interface. Authentication is handled automatically via OAuth. The skill delegates execution to the `fe-asana-tools:asana-task-assistant` agent, which verifies the MCP connection, discovers the workspace, and performs the requested operation.

## Instructions

Delegate ALL Asana operations to the `fe-asana-tools:asana-task-assistant` agent. Pass the user's request as-is:

```
Agent(subagent_type="fe-asana-tools:asana-task-assistant", prompt="<user's request>")
```

## Key Operations

### View Tasks

Show tasks assigned to the user, filtered by due date, project, tags, or completion status. By default, only the top 10 tasks are shown, sorted by urgency (overdue > due today > due this week > nearest due date).

Example prompts:
- "Show me my Asana tasks due this week"
- "What tasks are overdue?"
- "Show all tasks in the Q2 Planning project"

### Create Tasks

Create tasks with a name, description, assignee, due date, and project. Supports subtasks (via parent GID) and custom fields.

Example prompts:
- "Create a task: Prepare demo environment, due Friday, assign to me"
- "Add a subtask under task 1234567890 for testing"

### Update Tasks

Modify task fields: name, notes, due date, assignee, completion status, custom fields. Move tasks between project sections (board columns).

Example prompts:
- "Mark task 1234567890 as complete"
- "Move 'Deploy staging' to the Done column"
- "Change the due date on my demo prep task to next Monday"

### Search and Filter

Search tasks by text, assignee, project, section, tag, completion status, or dependency state. See `resources/ASANA_API_REFERENCE.md` for all search parameters.

Example prompts:
- "Find all tasks tagged 'urgent' in Project Alpha"
- "Show blocked tasks in my workspace"

### Comments and Activity

Read comments and activity history on tasks. Add comments to existing tasks.

Example prompts:
- "Show comments on task 1234567890"
- "Add a comment to the deploy task: staging is ready"

### Project Overview

List projects, view project sections (board columns), and generate project summaries.

Example prompts:
- "Show my active projects"
- "What are the sections in the Q2 Planning board?"

### Export to Google Docs

Generate project status reports or weekly task summaries as Google Docs. Requires `google-auth` skill to be configured.

Example prompts:
- "Export my weekly task summary to Google Docs"
- "Create a project status report for Q2 Planning"

### Meeting Notes to Tasks

Paste meeting notes and extract action items as Asana tasks. Resolves assignees and sets due dates from the notes.

Example prompts:
- "Create tasks from these meeting notes: ..."

### Roadmap Tool (Databricks-specific)

Search the "Roadmap Tool" project for feature release status, timelines, and availability. Triggered by mentions of product roadmap, feature previews, release states (GA, public preview, private preview, beta), or upcoming releases.

## Data Formats

- **GIDs**: Strings like `"1234567890"` (not integers)
- **Dates**: `YYYY-MM-DD` (e.g., `"2026-03-15"`)
- **Datetimes**: ISO 8601 (e.g., `"2026-03-15T17:00:00.000Z"`)

See `resources/ASANA_API_REFERENCE.md` for the full API reference including search parameters, task fields, custom fields, project status types, tag colors, and goal status types.
