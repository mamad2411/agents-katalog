---
name: writing-event-report
description: Use when documenting operational events as structured Markdown reports, including incidents, faults, outages, deployments, configuration changes, routine maintenance, security events, postmortems, RCA requests, event records, or analysis reports.
---

# Writing Event Report

Create factual, source-backed operational event reports in Markdown. Do not invent evidence; mark unknown fields as `待确认`, `未提供`, `无法验证`, or `不适用`.

## Event Types

| Type | Use for | Template |
|------|---------|----------|
| Fault event | Outages, crashes, degradation, OOM, database or network failures | `templates/fault-event-template.md` |
| Change event | Deployments, configuration changes, upgrades, migrations | `templates/change-event-template.md` |
| Operation event | Maintenance, backups, inspections, capacity planning | `templates/operation-event-template.md` |
| Security event | Unauthorized access, malware, breaches, policy violations, audit findings | `templates/security-event-template.md` |

If the event spans multiple types, use the dominant type and add cross-impact notes in the report.

## Workflow

1. Identify the event type, time range, affected systems, severity, and intended audience.
2. Read exactly one matching template from `templates/`.
3. Confirm what environment the evidence belongs to before running diagnostics.
4. Collect available evidence from the conversation, files, logs, commands, tickets, monitoring links, or user-provided notes.
5. Draft the report using the template structure. Keep conclusions tied to explicit data sources.
6. Save the report as Markdown when the user asks for a file, a report record, or does not specify inline-only output.

Default filename: `YYYY-MM-DD-event-type-brief-description.md`, for example `2026-07-21-fault-metabase-oom-crash.md`. Use the user-specified directory when provided; otherwise save in the current working directory.

## Environment and Authorization

- Confirm the target system. Do not assume the current shell is the affected server.
- Prefer user-provided logs, command output, tickets, and monitoring screenshots when direct access is unavailable.
- Run only read-only commands unless the user explicitly authorizes a state-changing operation.
- Do not run containment, restart, kill, delete, chmod, firewall, package install, or configuration-change commands as part of report writing.
- If evidence cannot be collected safely or with authorization, document it under data sources as `未提供` or `无法验证`.

## Evidence Collection

Use conversation context first. If live evidence collection is needed and authorized, read `references/evidence-sources.md` for read-only command examples and source categories.

## Report Requirements

Every report should include metadata, summary, timeline, analysis, impact, data sources, recommendations, and lessons learned or follow-up items. Distinguish facts, assumptions, hypotheses, and unknowns.

## Supporting Files

Templates live in `templates/`. Use `references/evidence-sources.md` only when live evidence collection is needed. `examples/server-crash-example.md`, `references/schemas.md`, `evals/evals.json`, and `agents/grader.md` support examples, schemas, evaluation, and grading.

## Quality Bar

- Cite every important conclusion to a data source.
- Keep recommendations actionable and scoped.
- Use tables for timelines, evidence, and impact summaries.
- Avoid blaming individuals; describe system conditions and process gaps.
