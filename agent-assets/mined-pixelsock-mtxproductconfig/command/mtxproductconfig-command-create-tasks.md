---
name: create-tasks
description: Generate tasks from a specification
---

Execute the Agent OS task creation workflow by loading and running the instructions at `.agent-os/instructions/core/create-tasks.md`.

This command will:
1. Analyze the current spec in focus
2. Break down the spec into actionable tasks
3. Create `tasks.md` with detailed implementation steps
4. Organize tasks into parent/child hierarchies

Usage: `/create-tasks [spec-folder-path]`
       `/create-tasks` (for most recent spec)