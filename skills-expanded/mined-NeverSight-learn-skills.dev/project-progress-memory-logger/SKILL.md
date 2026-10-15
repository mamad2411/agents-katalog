---
name: project-progress-memory-logger
description: Use this skill when a project task is completed or when the user asks to record progress, save context, update project memory, write a project log, or capture a handoff. It creates and updates a project-local Docs/progress memory system with session logs, code changes, commands, tests, decisions, todos, environment notes, cross-device context, redaction, and future AI recovery notes.
metadata:
  short-description: Log project progress after each task
---

# Project Progress Memory Logger

## Purpose

Use this skill to preserve durable, project-local memory after AI-assisted work. The record should let a future AI agent or human maintainer recover the task context, understand what changed, verify what was run, and continue from the right next step without reading the original chat.

## Trigger Conditions

Use this skill when any of these are true:

- The user asks to record the task, write a project log, save context, update project memory, create a handoff, or says phrases such as "记录一下", "保存上下文", "写入项目日志", "更新项目记忆", or "收尾".
- A code, documentation, experiment, paper, planning, debugging, deployment, data, or environment task has been completed.
- The task produced project state that matters later: code changes, commands, test results, experiment metrics, generated reports, decisions, todos, environment changes, or cross-device notes.
- The user wants the conversation to become long-term project memory.

Skip only when the user explicitly says not to record, the interaction was a simple standalone Q&A with no project-state change, safe redaction is impossible, or no project root can be confirmed.

## Default Output System

Create or update this tree in the target project:

```text
Docs/progress/
  index.md
  project_memory.md
  sessions/
  decisions.md
  todos.md
  environment.md
```

Use `Docs/progress/` by default. If the user project uses another docs root, such as `docs/progress/`, adapt to that root and record the choice in `environment.md`.

## Language Selection

Choose the language for `Docs/progress/` records from the user's context instead of defaulting to English:

- Use the language of the user's current request for new session records and related updates.
- If the current request mixes languages, use the language that carries the task instructions, unless the user explicitly asks for another language.
- When updating an existing progress file, keep the existing file's language if the update is small; switch only when creating a new file or when the user context clearly asks for a different language.
- Keep frontmatter keys, file names, code identifiers, commands, paths, and quoted source text unchanged when they need to stay machine-readable or faithful to the source.
- Apply the same language choice consistently across `sessions/`, `index.md`, `project_memory.md`, `decisions.md`, `todos.md`, and `environment.md` updates for the same task.

## Standard Workflow

1. Decide whether the task needs a progress record.
2. Confirm the project root. Prefer the Git root; otherwise use the user-specified directory or a directory containing project markers such as `README.md`, `AGENTS.md`, `CLAUDE.md`, `pyproject.toml`, `package.json`, or `Docs/`.
3. Inspect or initialize `Docs/progress/`. Use `scripts/init_progress.py` when available.
4. Collect the user request, agent understanding, task plan, execution timeline, tool calls, commands, file changes, Git state, tests, outputs, decisions, unresolved issues, next steps, and cross-device context.
5. Redact secrets and sensitive information before writing. Follow `references/redaction-policy.md`.
6. Create one detailed session record under `Docs/progress/sessions/` using `templates/session-log.md`.
7. Update `index.md`, `project_memory.md`, `decisions.md`, `todos.md`, and `environment.md` when the current task changes them.
8. Run `scripts/update_index.py` when available, then run the completeness checklist from `references/maintenance-guide.md`.
9. Tell the user which files were created or updated and which items remain open.

## What To Load When Needed

- `templates/session-log.md` for a single-task detailed record.
- `templates/index.md`, `templates/project-memory.md`, `templates/decisions.md`, `templates/todos.md`, and `templates/environment.md` when initializing the progress tree.
- `references/field-guide.md` for field meanings and conditional sections.
- `references/redaction-policy.md` before writing commands, credentials-adjacent text, logs, or environment details.
- `references/cross-device-guide.md` for laptop/server/lab-machine workflows.
- `references/maintenance-guide.md` before finalizing and updating indexes.

## Quality Bar

A good progress record answers these questions without the original chat:

- What did the user ask for?
- What did the agent understand and decide to do?
- What steps were performed, with which commands or tools?
- Which files, outputs, results, and tests changed?
- What failed, what was fixed, and what remains unverified?
- What decisions were made and why?
- Which machine or environment was used?
- What should the next AI session read and do first?
