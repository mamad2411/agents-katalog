# Jira MCP Integration Guidelines

When the Jira MCP server is active, you have access to tools for managing Jira issues and projects directly within Vinylmania.

## Available Capabilities
- **Issue Lookup & Search**: Use `jira_get_issue` with the issue key (e.g., `VM-123`) or `jira_search_jql` to search for open tasks, bugs, or user stories.
- **Issue Creation**: Use `jira_create_issue` when converting User Stories (`.hu/`) or SpecKit tasks (`tasks.md`) into Jira tickets. Supports Markdown formatting (converted to ADF).
- **Issue Updates & Comments**: Use `jira_edit_issue`, `jira_add_comment`, and `jira_transition_issue` to reflect progress, link PRs, or update statuses (e.g. *In Progress*, *Done*).

## Best Practices
1. The default Jira project key for all issues, epics, and tasks is **`VINYLMANIA`** (e.g. `VINYLMANIA-123`).
2. Follow the BDD and Constitution criteria defined in [user-stories.md](file:///Users/fortizfe/Repositories/vinylmania/.agents/rules/user-stories.md).
3. In issue descriptions, provide clear context: Summary, Acceptance Criteria (BDD Given-When-Then), and references to spec files in `specs/`.
4. Never log or output the `JIRA_API_TOKEN` in chat or notes.

