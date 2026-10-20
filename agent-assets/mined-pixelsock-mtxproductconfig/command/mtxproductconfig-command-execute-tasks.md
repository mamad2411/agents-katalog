---
name: execute-tasks
description: Execute tasks from a specification using Agent OS
---

Execute the Agent OS task execution workflow by loading and running the instructions at `.agent-os/instructions/core/execute-tasks.md`.

This command will:
1. Set up git branch management
2. Execute all tasks in the specified spec
3. Run post-execution steps (tests, git workflow, etc.)
4. Generate completion summary and recap

Usage: `/execute-tasks [spec-folder-path] [task-numbers]`
       `/execute-tasks` (for next unfinished task)