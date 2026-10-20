---
name: project-management-category-pointer
description: "Pointer to a library of 22 specialized Project Management skills. Use when working on project-management-related tasks."
risk: none
---

# Project Management Capability Library 🎯

This is a **pointer skill**. The 22 specialized Project Management skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **asana-automation** — Automate Asana tasks via Rube MCP (Composio): tasks, projects, sections, teams, workspaces. Always search tools first for current schemas.
- **basecamp-automation** — Automate Basecamp project management, to-dos, messages, people, and to-do list organization via Rube MCP (Composio). Always search tools first for current schemas.
- **confluence-automation** — Automate Confluence page creation, content search, space management, labels, and hierarchy navigation via Rube MCP (Composio). Always search tools first for current schemas.
- **feature-tracking** — Maintain durable feature-level memory across AI coding sessions with lightweight Markdown tracks for status, source-of-truth docs, decisions, risks, and changes.
- **freshservice-automation** — Automate Freshservice ITSM tasks via Rube MCP (Composio): create/update tickets, bulk operations, service requests, and outbound emails. Always search tools first for current schemas.
- **github-issue-creator** — Turn error logs, screenshots, voice notes, and rough bug reports into crisp, developer-ready GitHub issues with repro steps, impact, and evidence.
- **jira-automation** — Automate Jira tasks via Rube MCP (Composio): issues, projects, sprints, boards, comments, users. Always search tools first for current schemas.
- **linear-automation** — Automate Linear tasks via Rube MCP (Composio): issues, projects, cycles, teams, labels. Always search tools first for current schemas.
- **linear-claude-skill** — Manage Linear issues, projects, and teams
- **miro-automation** — Automate Miro tasks via Rube MCP (Composio): boards, items, sticky notes, frames, sharing, connectors. Always search tools first for current schemas.
- **monday-automation** — Automate Monday.com work management including boards, items, columns, groups, subitems, and updates via Rube MCP (Composio). Always search tools first for current schemas.
- **progressive-estimation** — Estimate AI-assisted and hybrid human+agent development work with research-backed PERT statistics and calibration feedback loops
- **project-state-governor** — Govern evidence-backed canonical project state across sessions, branches, reviews, and research cycles without inventing product intent.
- **sred-project-organizer** — Take a list of projects and their related documentation, and organize them into the SRED format for submission.
- **sred-work-summary** — Go back through the previous year of work and create a Notion doc that groups relevant links into projects that can then be documented as SRED projects.
- **team-collaboration-issue** — You are a GitHub issue resolution expert specializing in systematic bug investigation, feature implementation, and collaborative development workflows. Your expertise spans issue triage, root cause an
- **team-collaboration-standup-notes** — You are an expert team communication specialist focused on async-first standup practices, AI-assisted note generation from commit history, and effective remote team coordination patterns.
- **to-issues** — Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices.
- **to-prd** — Turn the current conversation into a PRD and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed.
- **todoist-automation** — Automate Todoist task management, projects, sections, filtering, and bulk operations via Rube MCP (Composio). Always search tools first for current schemas.
- **trello-automation** — Automate Trello boards, cards, and workflows via Rube MCP (Composio). Create cards, manage lists, assign members, and search across boards programmatically.
- **wrike-automation** — Automate Wrike project management via Rube MCP (Composio): create tasks/folders, manage projects, assign work, and track progress. Always search tools first for current schemas.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/project-management/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/project-management`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
