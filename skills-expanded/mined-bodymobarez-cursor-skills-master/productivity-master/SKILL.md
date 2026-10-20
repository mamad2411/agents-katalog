---
name: productivity-master
description: Master hub for Productivity & workflow. Use for workflow productivity: context saving, onboarding, parallel exploration, project switching. Bundles 14 specialized skills (in skills/<name>/GUIDE.md). Use this for any productivity task.
---

# Productivity & workflow — Master Hub

Use for workflow productivity: context saving, onboarding, parallel exploration, project switching.

## How to use this hub

This single skill bundles **all 14 productivity skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **best-of-n-solving** — Solve a hard problem by trying multiple approaches in parallel using isolated git worktrees. Each attempt runs in its own branch, and the best solution is selected. Use for complex refactors, trick...  
  → `skills/best-of-n-solving/GUIDE.md`
- **blastum-conversation-notes** — Save a note summarizing what was learned in the current conversation. Use when the user says "make a note", "note that", "summarize what we learned", or similar.  
  → `skills/blastum-conversation-notes/GUIDE.md`
- **blastum-file-change-tracker** — Mandates providing organized list of changed files grouped by folder as links at end of responses. Always active when files are modified.  
  → `skills/blastum-file-change-tracker/GUIDE.md`
- **blastum-ical** — Author valid iCalendar (.ics) text per RFC 5545 with 7986/6868 updates, folding, recurrence, time zones, and client interoperability. Use when generating, fixing, or reviewing .ics feeds, exports, ...  
  → `skills/blastum-ical/GUIDE.md`
- **blastum-jira-acli** — Jira CRUD via ACLI and local md→ADF. Use when searching, creating, editing, or managing Jira issues without MCP. Triggers: jira, acli, create issue, search jira, edit jira, jql, transition, comment.  
  → `skills/blastum-jira-acli/GUIDE.md`
- **blastum-notebook** — Build and query document knowledge bases with indexed metadata and citations. Use when researching a topic, collecting sources, querying documents, or storing plans and options.  
  → `skills/blastum-notebook/GUIDE.md`
- **blastum-pi-ssh-access** — SSH access and management for Raspberry Pi devices. Use when connecting to, managing, or troubleshooting Raspberry Pi systems via SSH.  
  → `skills/blastum-pi-ssh-access/GUIDE.md`
- **blastum-workspace-context** — Organize workspace context files in tmp/ subfolders. Use when saving plans, results, notes, or docs.  
  → `skills/blastum-workspace-context/GUIDE.md`
- **codebase-onboarding** — Launch multiple explore subagents in parallel to investigate architecture, data models, auth, APIs, and deployment. Synthesize into an onboarding document.  
  → `skills/codebase-onboarding/GUIDE.md`
- **mattpocock-handoff** — Compact the current conversation into a handoff document for another agent to pick up.  
  → `skills/mattpocock-handoff/GUIDE.md`
- **parallel-exploring** — Explore a large codebase in parallel by launching multiple explore subagents that each investigate a different area simultaneously. Use when onboarding onto a new project, understanding architectur...  
  → `skills/parallel-exploring/GUIDE.md`
- **saving-workspace-context** — Automatically persist useful context — research, decisions, learnings, templates — to workspace files so knowledge survives across conversations.  
  → `skills/saving-workspace-context/GUIDE.md`
- **switching-projects** — Switch the current Cursor workspace to a different project directory using the cursor-app-control MCP. Use when the user asks to switch projects, open another repo, jump to a different codebase, or...  
  → `skills/switching-projects/GUIDE.md`
- **updating-npm-package** — Safely update an npm package by checking npmjs.com for the latest version, reading release notes, and handling minor vs major upgrades differently. For minor updates, just do it. For major updates,...  
  → `skills/updating-npm-package/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
