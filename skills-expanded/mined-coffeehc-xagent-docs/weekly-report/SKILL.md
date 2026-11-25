---
name: weekly-report
description: Use when creating, rewriting, consolidating, or reviewing weekly reports, status updates, team rollups, manager updates, client progress reports, executive summaries, 3P updates, or recurring work progress materials. Prefer this Skill when the task needs progress/blocker/plan structure, audience-specific tone, source-backed facts, metrics, action requests, or a reusable report artifact.
meta:
  version: 1
  display_name: 周报生成
  source: claude-office-skills/skills weekly-report
  license: MIT
---

# Weekly Report

## Purpose

Create production-ready weekly reports that communicate completed work, current progress, blockers, next steps, decisions needed, metrics, and risks in a format suitable for the intended audience.

This XAgent built-in Skill adapts the open-source `weekly-report` candidate into a source-backed workflow. It removes the upstream `office-mcp` dependency and does not assume DOCX templates, calendars, project trackers, or external reporting systems are available.

## Use When

Use for:

- Individual weekly reports to a manager, lead, mentor, or client.
- Team rollups from several individual updates.
- Project or workstream status reports.
- Executive weekly summaries that need risks, asks, and metrics.
- 3P reports: progress, plans, problems.
- Rewriting a rough update into a polished shareable report.
- Reviewing an existing weekly report for missing facts, vague blockers, or unclear asks.

## Do Not Use When

Do not use for:

- Meeting minutes or transcript cleanup; use `meeting-notes` or `meeting-recap`.
- Meeting outcome communication to non-attendees; use `meeting-recap` for the source record or `internal-comms` for an internal update.
- Formal government or institutional documents; use `official-document-drafting`.
- Long research reports or market analysis unless the user specifically asks for a weekly status format.
- Fabricating status from calendars, trackers, commits, chats, or emails that have not been provided or retrieved through visible XAgent tools.

## Material Gate

Before writing, identify:

- Reporting period, author, audience, project/team, and desired channel.
- Completed work, in-progress work, blocked work, risks, metrics, decisions, and next-week plan.
- Source material: user bullets, notes, tickets, commits, docs, tables, emails, meeting notes, or prior reports.
- Whether the report is internal, client-facing, executive-facing, or personal.
- Required format, length, tone, confidentiality constraints, and artifact path if the report should be saved.

If key facts are missing, keep placeholders or mark `未提供/待确认`. Do not invent progress, dates, owners, metrics, blockers, decisions, or client commitments.

## Workflow

1. Classify the report mode: individual, team rollup, project status, executive summary, client update, or 3P.
2. Read or inspect all provided source material before summarizing. If the source is a rough message, preserve every concrete fact that affects status, blockers, metrics, dates, or asks.
3. Normalize facts into this evidence model:
   - accomplishments
   - in progress
   - blockers and impact
   - metrics
   - risks
   - decisions or support needed
   - next-week priorities
4. Select the audience pattern from `references/report-patterns.md` when the report type is unclear or the audience is high-stakes.
5. Use `templates/weekly-report.md` when the user wants a durable Markdown artifact or a consistent recurring format.
6. Write the report in the user's language by default. Use concise headings, concrete verbs, and measurable outcomes.
7. Separate facts from interpretation. Label inferred risk, inferred priority, or missing evidence.
8. For team rollups, consolidate repeated blockers and cross-team dependencies instead of pasting each person's update unchanged.
9. For executive/client reports, lead with outcome and ask. Keep implementation detail below the main status.
10. Before finalizing, run the checks below.

## Checks

- Reporting period, audience, and scope are explicit.
- Every accomplishment is concrete enough to be useful.
- Blockers include impact and requested help when known.
- Next steps are realistic, ordered, and tied to owners or dependencies when provided.
- Metrics include units and period. Missing or unverified metrics are not invented.
- Risks and decisions needed are visible; they are not buried in prose.
- Client-facing reports do not expose internal-only details.
- Executive summaries lead with status, risk, and ask, not a chronology.
- The output remains a report, not a generic motivational narrative.

## Outputs

Produce one or more of:

- weekly status report
- 3P update
- team rollup
- executive summary
- client progress update
- blocker/escalation section
- review notes for an existing report
- Markdown artifact content ready for XAgent artifact tools

## Recovery

If evidence is weak, produce a partial report with a `待确认` section and name the missing facts. If multiple source materials conflict, present the conflict and either choose the most recent explicit source or ask for confirmation when the conflict changes the report's status, risk, or commitments.

## Boundary

Skill owns workflow, report structure, audience adaptation, fact discipline, and reusable reporting templates.

It does not own XAgent tool schemas, ToolResult fields, runtime path selection, file permissions, tracker access, calendar access, email sending, external system sync, DOCX generation, or final management approval. It must not run shell, Python, Node, curl, Office, tracker, email, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/report-patterns.md`: audience patterns, status models, blocker writing, and review checklist.
- `templates/weekly-report.md`: production Markdown template for individual, team, executive, and client reports.
- `LICENSE`: source and license notice.
