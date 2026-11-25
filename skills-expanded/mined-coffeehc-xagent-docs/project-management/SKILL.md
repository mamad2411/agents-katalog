---
name: project-management
description: Use when planning, organizing, reviewing, or rescuing a project, initiative, roadmap, delivery plan, cross-functional workstream, milestone plan, risk log, status report, dependency map, or action plan. Prefer this Skill when the task needs scope, owners, milestones, risks, dependencies, decision points, and execution cadence. Do not use for ticket writes, project tool automation, or formal PMO approval.
meta:
  version: 1
  display_name: 项目管理
---

# Project Management

## Purpose

Turn ambiguous work into a manageable plan with scope, owners, milestones, dependencies, risks, decisions, and status rhythm.

## Use When

Use for:

- project kickoff plans
- milestone planning
- cross-functional coordination
- risk and dependency review
- project rescue
- roadmap workstream planning
- status report structure
- action plan creation

## Material Gate

Identify:

- goal, sponsor, owner, stakeholders, deadline, and constraints
- scope, non-goals, deliverables, milestones, and dependencies
- known risks, blockers, open decisions, and communication cadence
- desired artifact: plan, risk log, status, or roadmap

If owner, deadline, or scope is unclear, flag it before planning.

## Workflow

1. State the outcome and definition of done.
2. Define scope, non-goals, deliverables, and constraints.
3. Break work into phases, milestones, tasks, owners, and dependencies.
4. Identify risks, blockers, decisions, and escalation paths.
5. Set status cadence and evidence required for progress.
6. Create next actions with owners and dates.
7. Use `weekly-report` for recurring updates when appropriate.
8. Use `html-report-builder` for roadmap or project review reports.

## Checks

- Every critical workstream has an owner.
- Milestones are outcome-based, not activity-only.
- Dependencies and decisions are visible.
- Risks include mitigation and escalation.
- Status language is evidence-backed.

## Outputs

- project plan
- milestone roadmap
- dependency map
- risk log
- action plan
- status update
- project rescue plan

## Boundary

This Skill owns project structure, planning, risk framing, and status cadence. It does not own project-management tool writes, budget approval, staffing authority, procurement approval, or final delivery acceptance.

It must not run shell, Python, Node, npm, curl, MCP, project-management, ticketing, calendar, email, Slack, Teams, spreadsheet, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
