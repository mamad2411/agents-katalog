---
name: crm-pipeline-management
description: Use when organizing, reviewing, forecasting, or improving a sales pipeline, CRM notes, opportunity stages, deal risks, next steps, account plans, qualification, handoffs, or sales manager updates. Prefer this Skill when the task needs pipeline hygiene, deal qualification, risk flags, next-action discipline, or forecast narrative. Do not use for CRM writes, revenue guarantees, or sales compensation decisions.
meta:
  version: 1
  display_name: CRM 管道管理
---

# CRM Pipeline Management

## Purpose

Turn messy sales notes, opportunities, and account information into clear pipeline status, deal risks, next actions, and forecast-ready summaries.

## Use When

Use for:

- CRM note cleanup
- deal review preparation
- opportunity qualification
- pipeline risk analysis
- forecast narrative
- account plan updates
- sales handoff summaries

## Material Gate

Identify:

- account, opportunity, stage, owner, value, timeline, and source date
- buyer problem, decision process, stakeholders, budget, competition, and next step
- evidence for stage, probability, and forecast category
- missing fields that affect qualification or forecast

If CRM data is not provided or current, label the output as a draft.

## Workflow

1. Normalize opportunity facts from notes, tables, or user input.
2. Separate verified facts, seller opinion, and missing data.
3. Assess stage fit and qualification evidence.
4. Identify deal risks: no pain, no champion, no budget, no timeline, no next meeting, legal/procurement, competitor, or stale activity.
5. Produce next actions with owner, due date, and purpose.
6. Summarize forecast implication and confidence without overclaiming.
7. Use `html-report-builder` for pipeline review reports when useful.

## Checks

- Each deal has an explicit next action or is flagged stale.
- Forecast language is tied to evidence.
- Missing qualification fields are visible.
- Risks are actionable, not just labels.
- No CRM update is claimed unless a tool actually performed it.

## Outputs

- pipeline review
- deal risk summary
- account plan
- CRM cleanup notes
- forecast narrative
- next-action list
- sales handoff

## Boundary

This Skill owns pipeline reasoning, opportunity hygiene, qualification structure, and sales update drafting. It does not own CRM schema, CRM writes, account ownership, quota policy, compensation, legal approval, or revenue commitments.

It must not run shell, Python, Node, npm, curl, MCP, CRM, enrichment, email, calendar, spreadsheet, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
