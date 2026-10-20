# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Common Memory Bank is a collection of integrated memory bank rules for AI development tools. It provides memory bank rule files that can be used across various AI development tools such as Cursor, Windsurf, Cline, RooCode, etc. It's specifically designed to work with TaskMaster AI for maintaining context across sessions.

## Memory Bank Architecture

The Memory Bank follows a structured hierarchy with these core files:

```
memory-bank/
├── projectbrief.md       # Foundation document with core requirements and goals
├── productContext.md     # Product purpose, problems solved, user experience
├── systemPatterns.md     # System architecture, design patterns, technical decisions
├── techContext.md        # Technologies, development setup, technical constraints
└── activeContext.md      # Current focus, recent changes, next steps
```

When working with this project, always check the memory bank files first to understand the current state and context of the project.

## TaskMaster Integration

This project is designed to work with TaskMaster AI. When using TaskMaster:

1. Always synchronize memory bank files with task status changes
2. Update `activeContext.md` whenever a task status changes
3. Check consistency between TaskMaster state and memory bank contents

### Task Status Change Process

When changing a task status:
1. Change the task status with TaskMaster command (e.g., `set_task_status`)
2. Update `activeContext.md` to reflect the current task focus change
3. Update the next steps and considerations

## Common Commands

### TaskMaster Commands

```bash
# Initialize TaskMaster
task-master init

# Parse PRD to generate tasks
task-master parse-prd scripts/prd.txt

# Generate individual task files
task-master generate

# Show all tasks
task-master list

# Get next task
task-master next

# Set task status
task-master set-task-status <id> <status>

# Add a subtask
task-master add-subtask <id>

# Expand a task into subtasks
task-master expand-task <id>
```

## Project Workflow

### Setup Workflow

1. Install TaskMaster AI globally: `npm install -g task-master-ai`
2. Initialize TaskMaster: `task-master init`
3. Set up LLM API keys in `.env` for TaskMaster
4. Initialize memory bank based on project requirements
5. Create `scripts/prd.txt` if it doesn't exist
6. Parse PRD to generate tasks: `task-master parse-prd scripts/prd.txt`
7. Generate task files: `task-master generate`

### Development Workflow

1. Check current task status: `task-master list`
2. Get next task: `task-master next`
3. Work on task and update status when complete
4. Update `activeContext.md` with changes
5. Create/update subrules for specific folders when needed

## Additional Features

### Subfolder Rules

The project supports a Folder Path-Based Sub Rule Management System:
- Rules are stored in `.cursor/rules/subrules/` directory
- Rule paths are recorded in `.cursor/rules/subrules/rule_list.txt`
- Create subrules for folders that need special architectural patterns or context

### PRD and Task Chain Review

When core memory bank files are modified:
1. Review consistency with PRD (`scripts/prd.txt`)
2. If PRD is modified, analyze impact on tasks and propose updates

## Consistency Checks

Regularly perform these consistency checks:
- Verify TaskMaster state matches memory bank content
- Ensure `activeContext.md` reflects current task focus
- Check that dependencies between tasks are reflected in documentation