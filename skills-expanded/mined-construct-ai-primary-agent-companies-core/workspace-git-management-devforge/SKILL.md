---
name: workspace-git-management-devforge
description: >
  Use when managed workspace git clone race conditions occur, isolated_workspace fails
  on first use, worktree creation crashes, or git repository initialization issues block
  agent heartbeats. Handles ensureManagedProjectWorkspace and realizeExecutionWorkspace.
---

# Workspace Git Management - DevForge AI

## Overview
Handles workspace and git management issues in the Paperclip codebase. Resolves managed workspace git clone race conditions, isolated_workspace failures on first use, worktree creation crashes, and git repository initialization issues that block agent heartbeats.

## When to Use
- When `fatal: not a git repository` error occurs during first agent heartbeat
- When `ensureManagedProjectWorkspace` returns success with warning for non-git directory
- When `realizeExecutionWorkspace` crashes at `git rev-parse --show-toplevel`
- When `sourceType: "git_repo"` with `isolated_workspace` policy fails
- When worktree creation fails on incomplete clone
- **Don't use when:** It's a general git connectivity issue (use cloudops-devforge-cloud-operations)

## Core Procedures
### Workspace Clone Fix Workflow
1. **Identify Race Condition** - Check if clone completed before workspace resolution
2. **Validate Git Repo** - Ensure `baseCwd` has `.git` directory before worktree ops
3. **Fix Clone Logic** - Make `ensureManagedProjectWorkspace` throw on missing clone, not warn
4. **Add Pre-Check** - Verify `baseCwd` is valid git repo before `realizeExecutionWorkspace`
5. **Test First-Use** - Verify workspace works on first heartbeat, not just subsequent ones

### Common Failure Points
- `ensureManagedProjectWorkspace` returns success for existing non-git directory (lines 175-183)
- `realizeExecutionWorkspace` runs `git rev-parse` before clone completes (line 590)
- Lazy clone means first heartbeat always fails, second succeeds with fallback

## Agent Assignment
**Primary Agent:** cloudops-devforge-cloud-operations
**Company:** DevForge AI
**Role:** Workspace Git Specialist
**Reports To:** cloudops-devforge-cloud-operations
**Backup Agents:** devcore-devforge-core-development, codesmith-devforge-backend-engineer

## Success Metrics
- First heartbeat succeeds with git_repo sourceType
- No fallback to shared_workspace when isolated_workspace configured
- Clone completes before workspace resolution
- Worktree creation always succeeds

## Error Handling
- **Error:** Clone fails (invalid URL, network issue)
  **Response:** Surface error immediately, don't return success with warning
- **Error:** Worktree creation fails on existing directory
  **Response:** Clean directory, retry clone, or provide eager provisioning API

## Cross-Team Integration
**Gigabrain Tags:** devforge, workspace, git, clone, worktree, isolated-workspace
**Related Skills:** cloudops-devforge-cloud-operations, devcore-devforge-core-development, codesmith-devforge-backend-engineer
**Last Updated:** 2026-04-07