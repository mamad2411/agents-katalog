---
name: init-agent-sync
description: Initializes the AGENT_SYNC.md hub for AI agent coordination and task tracking.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: project-setup
---

## What I do

- Create an `AGENT_SYNC.md` file in the root of the project if one doesn't exist.
- Populate it with standard AI agent instructions, context tracking, a session task board, and a handoff log.
- Set up the foundation for multi-agent workflows so AI assistants can cleanly hand off tasks to one another.

## When to use me

Use this when starting a new project, or when you want to introduce the AI agent synchronization system to an existing repository. 

## Execution Steps

When invoked, execute the following steps:
1. **Check for existing file:** Check if `AGENT_SYNC.md` already exists in the project root. If it does, inform the user and ask if they want to overwrite it.
2. **Create the file:** Use the Write tool to create `AGENT_SYNC.md` with the following template:

```markdown
# 🤖 Agent Synchronization & Handoff Hub

**⚠️ INSTRUCTIONS FOR ALL AI AGENTS ⚠️**
1. **Read this file first** upon waking up or starting a new session.
2. **Check the Handoff Log** for context, recent changes, and messages directed at you.
3. **Master Trackers:** Always consult `progress.md` (or equivalent) for the *master project roadmap*. This file (`AGENT_SYNC.md`) is specifically for inter-agent communication, technical handoffs, and session-level tasks.
4. **Task Management:** When you start a task, update the Short-Term Tasks section (mark as `[~] In Progress`). When finished, mark as `[x] Completed`.
5. **Session Wrap-up:** Before ending your session or asking the user to switch agents, **append a brief summary** of what you accomplished and any blockers to the **Handoff Log**.

---

## 🎯 Current Context & Technical State
- **Active Branch:** `main`
- **Current Phase:** Initial Setup
- **Master Reference:** `progress.md`

---

## 📋 Session Task Board (Granular / Short-Term)
*Note: High-level goals live in master trackers. Use this for immediate, technical sub-tasks.*

- [ ] Define initial tasks here

---

## 💬 Handoff & Discussion Log
*Format: `**[YYYY-MM-DD] - [User/Agent Name]:** Message @Mention`*

**[Current Date] - Setup Agent:**
### Session Summary: Hub Initialization
**Objectives Accomplished:**
1. Initialized the AGENT_SYNC.md coordination hub.
```

3. **Commit:** Automatically run `git add AGENT_SYNC.md && git commit -m "chore: initialize AGENT_SYNC.md for AI coordination"` if inside a git repository.