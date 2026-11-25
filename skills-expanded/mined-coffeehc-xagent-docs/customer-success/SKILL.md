---
name: customer-success
description: Use when creating, reviewing, or improving customer success plans, onboarding plans, QBRs, renewal risk summaries, adoption analysis, stakeholder maps, health score narratives, expansion plans, or customer value reports. Prefer this Skill when the task needs outcome mapping, adoption signals, renewal risk, executive narrative, or next-step planning. Do not use for CRM writes, contract approval, or revenue guarantees.
meta:
  version: 1
  display_name: 客户成功
---

# Customer Success

## Purpose

Help teams retain and grow customers by turning usage, goals, risks, and stakeholder context into success plans, QBR narratives, and renewal actions.

## Use When

Use for:

- onboarding plans
- customer health summaries
- QBR or EBR preparation
- renewal risk review
- adoption and value narrative
- stakeholder maps
- expansion planning

## Material Gate

Identify:

- customer goal, contract scope, lifecycle stage, renewal date, and owner
- usage, adoption, support issues, outcomes, and stakeholder signals
- known risks, blockers, commercial context, and next meeting
- evidence source and freshness

If customer data is incomplete, mark confidence and avoid pretending health score precision.

## Workflow

1. State customer outcomes and success criteria.
2. Summarize adoption and value evidence.
3. Identify risks by category: usage, executive alignment, unresolved issues, value gap, procurement, champion loss, or competitor.
4. Map stakeholders and missing relationships.
5. Define next actions with owner and date.
6. Draft customer-facing and internal versions separately.
7. Use `html-report-builder` for QBR, health, or value-report artifacts.

## Checks

- Value claims are tied to evidence.
- Renewal risk has cause, signal, severity, and mitigation.
- Next actions are specific and owned.
- Customer-facing material avoids internal risk language unless intended.
- Expansion ideas follow value, not just seller wish.

## Outputs

- customer success plan
- onboarding plan
- QBR outline or narrative
- renewal risk summary
- stakeholder map
- adoption/value report
- next-action plan

## Boundary

This Skill owns customer success reasoning, value narrative, renewal risk framing, and account action planning. It does not own CRM writes, commercial approval, contract terms, support resolution, billing actions, or external sending.

It must not run shell, Python, Node, npm, curl, MCP, CRM, billing, product analytics, helpdesk, email, calendar, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
