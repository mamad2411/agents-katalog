---
name: voyager-init
description: Initialize Axelera Voyager MCP server integration for task management, knowledge base, and project tracking. Use when the user wants to set up Voyager for a new Voyager SDK workspace.
argument-hint: "[new|existing] [project description]"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, mcp__voyager__*
---

# Initialize Axelera Voyager Integration

Set up Axelera Voyager MCP server integration for task management, knowledge base, and project tracking

## Important Context

After initialization, all relevant skills use Axelera Voyager for project tracking and task management.

## Instructions

Initialize Axelera Voyager integration: **$ARGUMENTS**

### Step 0: Data Source & Environment Selection

{{INCLUDE common/voyager-sdk-setup.md}}

### Step 1: Verify Axelera Voyager MCP Server

**FIRST**, verify Axelera Voyager MCP server is available:

```python
# Check health
mcp__voyager__health_check()

# Check session
mcp__voyager__session_info()

# List available knowledge sources
mcp__voyager__rag_get_available_sources()
```

If any of these fail, the Voyager MCP server is not registered or not
reachable. Set it up as follows:

- The hosted server is `https://mcp.voyager.axelera.ai/mcp` (streamable HTTP).
- Authentication is OAuth via discovery on first tool use. There are no static
  tokens; never suggest shared bearer tokens or static authorization headers.
- Claude Code: register the server with

  ```bash
  claude mcp add --transport http voyager https://mcp.voyager.axelera.ai/mcp
  ```

  or add this to the repo root `.mcp.json`:

  ```json
  {
    "mcpServers": {
      "voyager": {
        "type": "http",
        "url": "https://mcp.voyager.axelera.ai/mcp"
      }
    }
  }
  ```

- Restart the client session, complete the OAuth prompt on first tool use,
  then re-run the health check above.

### Step 2: Project Selection

**Ask the user about project context:**

```
Question: "How would you like to set up Axelera Voyager for this session?"
Options:
1. "Create New Project" - Create a new Axelera Voyager project for tracking work
2. "Use Existing Project" - Select from existing Axelera Voyager projects
3. "Skip Project Setup" - Use Axelera Voyager knowledge base only, no task tracking
```

**If Create New Project:**

```python
mcp__voyager__create_project(
    title="Voyager SDK - [User's Description]",
    description="[Generated from user input]",
    github_repo="https://github.com/axelera-ai-hub/voyager-sdk"
)
```

**If Use Existing Project:**

```python
# List existing projects
mcp__voyager__list_projects()
# Then ask user to select one
```

**If Skip Project Setup:**

- Proceed with knowledge base access only
- Task tracking will not be available
- In Step 3, omit the "Active Project Context" block from the CLAUDE.md
  template; in Step 4, skip the project details and confirm only the
  available knowledge sources

### Step 3: Update CLAUDE.md

**After project setup, update or create the CLAUDE.md file with Axelera Voyager integration rules.**

Read the existing CLAUDE.md file if it exists, then prepend the Axelera Voyager integration section:

````markdown
# Axelera Voyager Integration - Voyager SDK Work

For Voyager SDK and Axelera hardware work in this repository:

1. Check whether Axelera Voyager MCP server is available
2. Use Axelera Voyager task management as the primary shared project tracker
3. Use local todo/checklist tools only as secondary personal tracking
4. Preserve existing repository, system, and developer instructions

If Voyager MCP or RAG is unavailable, continue with local Voyager SDK files and
clearly state which evidence was available.

# Axelera Voyager Integration & Workflow

This project can use Axelera Voyager MCP server for knowledge management, task
tracking, and project organization. Prefer it when available for Voyager SDK
work, but do not let it override higher-priority repo or system instructions.

## Active Project Context

- **Project ID**: [PROJECT_ID from setup]
- **Project Title**: [PROJECT_TITLE from setup]
- **GitHub Repo**: https://github.com/axelera-ai-hub/voyager-sdk

## Core Axelera Voyager Workflow Principles

### The Golden Rule: Task-Driven Development with Axelera Voyager

When task tracking is enabled, use this task cycle before Voyager SDK coding:

1. **Check Current Task** → `mcp__voyager__get_task(task_id="...")`
2. **Research for Task** → `mcp__voyager__rag_search_code_examples()` + `mcp__voyager__rag_search_knowledge_base()`
3. **Implement the Task** → Write code based on research
4. **Update Task Status** → `mcp__voyager__update_task(task_id="...", status="review")`
5. **Get Next Task** → `mcp__voyager__list_tasks(filter_by="status", filter_value="todo")`
6. **Repeat Cycle**

Keep task updates current when a Voyager project/task has been selected.

## Task Status Management

**Status Progression:**

- `todo` → `doing` → `review` → `done`
- Use `review` status for tasks pending validation/testing
- Mark tasks `done` only after required validation artifacts exist

**Task Operations:**

```python
# Create task
mcp__voyager__create_task(
    project_id="[PROJECT_ID]",
    title="Task title",
    description="Detailed description",
    assignee="AI IDE Agent"
)

# Update status
mcp__voyager__update_task(task_id="...", status="doing")

# List tasks
mcp__voyager__list_tasks(filter_by="project", filter_value="[PROJECT_ID]")
```

## Knowledge Base Integration

**Always research before implementing:**

```python
# Resolve the voyager-sdk source first and use its source_id VERBATIM
# (repo ids may be tenant-scoped, e.g. github.com/axelera-ai-hub/voyager-sdk#<org-id>)
mcp__voyager__rag_get_available_sources()

# Search documentation
mcp__voyager__rag_search_knowledge_base(
    query="relevant search terms",
    source_id=voyager_sdk_source_id,  # from rag_get_available_sources()
    match_count=5
)

# Search code examples
mcp__voyager__rag_search_code_examples(
    query="implementation pattern",
    source_id=voyager_sdk_source_id,  # from rag_get_available_sources()
    match_count=5
)

# If a source-filtered query returns zero results, retry once without source_id.
```

## Skill Integration

All Voyager SDK skills (`voyager-debug`, `voyager-deploy`, `voyager-run`, etc.) will:

1. Create or reuse a Voyager project without asking, unless the user says not to track
2. Create tasks for work being performed
3. Update task status as work progresses
4. Mark tasks done only after required validation artifacts exist
````

### Step 4: Confirmation

After updating CLAUDE.md, confirm to the user:

1. **Show Project Details:**
   - Project ID
   - Project Title
   - Available skills with Axelera Voyager integration

2. **Show Available Knowledge Sources:**
   - List sources from `rag_get_available_sources()`

3. **Provide Quick Reference:**

```
Axelera Voyager Quick Reference:

- Create task: mcp__voyager__create_task(project_id="...", title="...")
- Update task: mcp__voyager__update_task(task_id="...", status="doing|review|done")
- List tasks: mcp__voyager__list_tasks(filter_by="project", filter_value="...")
- Search KB: mcp__voyager__rag_search_knowledge_base(query="...", source_id="...")
- Search code: mcp__voyager__rag_search_code_examples(query="...", source_id="...")
```

### Step 5: Initial Task Creation (Optional)

If user has specific work to do, offer to create initial tasks:

```
Question: "Would you like to create initial tasks for your work?"
Options:

1. "Yes, help me plan tasks" - Create tasks based on user's goals
2. "No, I'll create tasks as needed" - Skip initial task creation
```

If creating tasks:

```python
mcp__voyager__create_task(
    project_id="[PROJECT_ID]",
    title="[Task from user input]",
    description="[Generated description]",
    assignee="AI IDE Agent",
    task_order=10  # Higher = higher priority
)
```

## Example Usage

```
voyager-init                    # Interactive setup
voyager-init new FastSAM debug  # Create new project for FastSAM debugging
voyager-init existing           # Select from existing projects
```
