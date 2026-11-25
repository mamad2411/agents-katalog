---
name: omni-code-todo-management
description: Use when creating, updating, prioritizing, or querying GitHub Project todo items for omni-stream-ai/omni-code, especially backlog drafts, issue promotion, status changes, labels, and priority edits.
---

# Omni-code Todo Management

## Overview
Use this skill to keep the `omni-code` GitHub Project organized and consistent. Backlog stays draft-only; Todo and later use real GitHub issues.

## Project Rules
- Project: `https://github.com/orgs/omni-stream-ai/projects/2`
- Keep card text in English.
- One task per card.
- Use `Backlog` for draft items only.
- Create a GitHub Issue only when the item moves to `Todo`.
- Do not create a branch in `Todo`.
- Create a linked branch only when the item moves to `In Progress`.
- Keep active work limited; `In Progress` should usually have one owner.

## Status Flow
- `Backlog`: draft only, not yet an issue.
- `Todo`: real issue exists, but no branch yet.
- `In Progress`: actively being worked on and should usually have a linked branch.
- `Review`: waiting for review or verification.
- `Blocked`: waiting on a dependency.
- `Done`: complete and verified.

## Labels
Use these base labels:
- `bug`
- `feature`
- `refactor`
- `docs`
- `test`
- `infra`

## Priority Heuristics
- `High`: core session, agent, or model behavior.
- `Medium`: session settings, model controls, or tool output UX.
- `Low`: polish, navigation, or convenience work.

## Common Workflow
1. Read current project state with `gh project item-list 2 --owner omni-stream-ai --format json`.
2. Add a backlog draft with `gh project item-create 2 --owner omni-stream-ai --title ... --body ...`.
3. When the item is ready, create the GitHub Issue in `omni-stream-ai/omni-code`, add labels, and move `Status` to `Todo`.
4. When actual coding starts, move the issue to `In Progress`, create a linked branch from the issue's `Development` relationship, and fetch that branch into the local repository.
5. Use `gh project item-edit` to change title, body, status, and priority.
6. Resolve current field and option IDs with `gh project field-list 2 --owner omni-stream-ai --format json` before editing if needed.

## Scripts
Use the bundled scripts for the recurring operations:
- `scripts/create_backlog_draft.sh "<title>" "<body>" [priority]`
- `scripts/promote_draft_to_todo.sh <project-item-id-or-exact-title> [labels]`
- `scripts/start_issue_work.sh <issue-number> [branch-name] [--checkout]`
- `scripts/list_project_items.sh [status]`

The scripts intentionally follow the current workflow:
- backlog is draft-only
- Todo has an issue but no branch
- In Progress creates a linked branch and fetches it locally
- `--checkout` additionally switches the local worktree to that branch

## Notes
- Draft content IDs start with `DI_`.
- Project item IDs start with `PVTI_`.
- See `references/project-facts.md` for current field and option IDs.
- Branch names should usually include the issue number, for example `feat/2-continuous-voice-conversations`.
- Current recurring themes:
  - continuous voice conversations
  - switching agents mid-session
  - shared model configuration
  - per-session settings
  - clickable code file content
  - tool output presentation
  - additional system prompts
