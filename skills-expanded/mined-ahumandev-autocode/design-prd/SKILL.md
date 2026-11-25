---
name: design-prd
description: Use `design-prd` to get Product Requirements when planning any feature or to understand project business requirements, user roles, and success criteria.
---

## Problem Statement
AutoCode helps users research, plan, and solve work inside OpenCode. OpenCode sessions own workflow and state. Users choose guidance, shared control, or autonomous work. Unsafe work goes to human.

## Feature Requirements
- **OpenCode sessions**: Start work in OpenCode session. Session owns workflow and state.
- **Work modes**: Advise gives guidance. Design proposes solution. Assist works with user. Auto solves work alone.
- **Safe hand-off**: Give human manual steps when work is unsafe.
- **Tool suite**: Give permitted tools for read-only data, sandbox work, cross-project tasks, SSH, Git, and HTTP.
- **Learned skills**: Save corrections, env facts, permissions, and preferences for later sessions.

## User Roles
- **User**: Start sessions, choose agent, confirm risky work.
- **advise agent**: Research and give manual guidance. No project changes.
- **design agent**: Review context and propose solution. No project changes.
- **assist agent**: Make permitted changes with user steering.
- **auto agent**: Make permitted changes alone.
- **spy agent**: Inspect permitted private data. Read-only.

## Constraints & Assumptions
- Plugin runs inside OpenCode. No web server or special UI.
- OpenCode sessions own workflow and state.
- Dangerous work needs human hand-off.
- External directory rule is `allow`, `ask`, or `deny`.
- Secrets stay hidden from agents. Runtime resolves credentials.

## Success Metrics
- User chooses fitting work mode.
- Session state lets work continue.
- Unsafe work gets clear human steps.
- Permitted tools do not expose secrets.
- Learned facts help later sessions.

## UX/UI Considerations
No special UI. Use OpenCode sessions and current slash commands. Show agent mode, risks, next action, and human hand-off when needed.

## User Stories
- As a user, I want choose work mode so control matches task.
- As a user, I want session state so work can continue.
- As a user, I want manual steps for unsafe work so I can finish safely.
- As a user, I want saved preferences so later work fits me.

---

**IMPORTANT**: Edit this `design-prd` skill whenever product requirements, user roles, or business rules change.
