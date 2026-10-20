---
<<<<<<< HEAD
description:
globs:
alwaysApply: false
=======
description: Rules for GitHub and Taskmaster integration in the workflow
globs: tasks/*.md, tasks/tasks.json, app/**/*
alwaysApply: true
---

>>>>>>> 1328a9a9fe85870642332260aa801a5d338ff3e3
# GitHub-Taskmaster Integration for Continuous Project Management

- **Automatic GitHub Issue Creation**
  - When a new task is created in Taskmaster, automatically create a corresponding GitHub issue
  - Include the task ID in the issue title format: `Task #X: [Task Title]`
  - Transfer task description, implementation details, and test strategy to issue body
  - Apply appropriate labels based on task type/category

- **Task-Issue Synchronization**
  - Include GitHub issue URL/number in Taskmaster task details
  - Update GitHub issue when task details are modified in Taskmaster
  - Ensure bidirectional traceability between Taskmaster tasks and GitHub issues

- **Automatic Issue Closure**
  - When a task is marked as "done" in Taskmaster, automatically close the associated GitHub issue
  - Add a closing comment referencing the completion status
  - If a task is changed from "done" to another status, reopen the associated issue

- **Subtask Management**
  - For parent tasks with subtasks, create a parent issue with a task list in GitHub
  - Each subtask should be represented as a checkbox item in the parent issue
  - Update checkboxes as subtasks are completed
  - For complex subtasks, consider creating child issues linked to the parent

- **Dependencies and Progress**
  - Reflect task dependencies as issue relationships where possible
  - Update issue comments with progress notes from Taskmaster task updates
  - Include task completion percentage in issue body as tasks progress

- **Implementation Code Examples**
  ```typescript
  // Example implementation for creating a GitHub issue when a task is added
  async function createGitHubIssueForTask(task) {
    const issueTitle = `Task #${task.id}: ${task.title}`;
    
    const issueBody = `## Description
${task.description}

## Implementation Details
${task.details}

## Test Strategy
${task.testStrategy}

## Dependencies
${task.dependencies.map(dep => `- [ ] Task #${dep}`).join('\n')}`;

    // Use GitHub MCP to create the issue
    const result = await mcp_github_create_issue({
      owner: "Abdi1717",
      repo: "LifeFlow4",
      title: issueTitle,
      body: issueBody,
      labels: ["taskmaster", task.priority]
    });
    
    return result;
  }
  
  // Example implementation for closing an issue when a task is completed
  async function closeGitHubIssueForTask(task, issueNumber) {
    // First add a comment
    await mcp_github_create_issue_comment({
      owner: "Abdi1717",
      repo: "LifeFlow4",
      issue_number: issueNumber,
      body: `This task has been completed on ${new Date().toISOString().split('T')[0]}.`
    });
    
    // Then close the issue
    await mcp_github_update_issue({
      owner: "Abdi1717",
      repo: "LifeFlow4",
      issue_number: issueNumber,
      state: "closed"
    });
  }
  ```

- **Event Listeners**
  - Implement listeners for Taskmaster events:
    - `task-created`: Create new GitHub issue
    - `task-updated`: Update corresponding GitHub issue
    - `task-status-changed`: Close/reopen GitHub issue
    - `task-expanded`: Update issue with subtasks
    - `subtask-completed`: Update checklist in parent issue

- **Best Practices**
  - Always include hyperlinks between Taskmaster and GitHub for easy navigation
  - Use consistent labeling strategy across all issues
  - Include task ID in all commit messages related to a task
  - Reference the GitHub issue in commits using `#issue_number` syntax

This integration ensures that project management stays synchronized between Taskmaster and GitHub, providing visibility to all team members and stakeholders while maintaining the structured task management approach of Taskmaster.

