---
name: Manage Jira Tasks
description: Skill for managing and updating Jira tasks during work execution, including appending plans to descriptions and commenting on progress.
---

# Manage Jira Tasks Skill

This skill provides instructions on how to interact with Jira during task execution. When managing Jira tasks, follow these policies carefully.

## 1. Updating the Jira Ticket Description with the Plan

When an implementation plan is created and approved:

- Read the current description of the active Jira task.
- Append the proposed plan **after** the initial description. Do not overwrite or delete the original problem description provided by the user or the reporter.
- Use styling (e.g., `h2` headers, bullet points, or bold text) to clearly separate the original description from your newly added implementation plan.

## 2. Documenting Advances and Tasks Done

When tasks are completed or significant progress is made:

- Add a **Comment** to the active Jira ticket summarizing the tasks that have just been done.
- Include context such as the files changed, infrastructure configurations made, or any test results.
- Keep the language format professional and concise.

## 3. Recommended Tools

- `mcp_atlassian-mcp-server_editJiraIssue`: Use this to update the ticket description.
- `mcp_atlassian-mcp-server_addCommentToJiraIssue`: Use this to add comments summarizing the advances.
- `mcp_atlassian-mcp-server_getJiraIssue`: Use this to read the current description before modifying it so you do not accidentally overwrite the original requirements.
