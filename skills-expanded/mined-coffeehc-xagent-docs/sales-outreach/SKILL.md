---
name: sales-outreach
description: Use when creating, improving, personalizing, or reviewing sales outreach such as cold emails, LinkedIn messages, call scripts, discovery openers, follow-up sequences, objection responses, account-specific value propositions, or prospecting copy. Prefer this Skill when the task needs buyer relevance, concise messaging, sequence logic, personalization, or CTA clarity. Do not use for spam, deceptive claims, legal compliance approval, or sending messages.
meta:
  version: 1
  display_name: 销售触达
---

# Sales Outreach

## Purpose

Create buyer-relevant sales outreach that is specific, concise, source-grounded, and tied to a clear next action.

## Use When

Use for:

- cold outbound email or message drafts
- follow-up sequences
- call openers and discovery scripts
- account-based personalization
- objection handling copy
- meeting request messages
- value proposition testing

## Material Gate

Identify:

- target buyer, role, company, segment, and likely pain
- product or service value proposition
- proof points, case studies, differentiators, or known constraints
- channel, tone, and CTA
- whether personalization facts are provided or inferred

Do not invent company facts, customer results, endorsements, urgency, or relationship history.

## Workflow

1. Define the buyer problem in the buyer's language.
2. Separate known facts from assumptions.
3. Choose one main value proposition and one CTA.
4. Draft concise copy for the requested channel.
5. Add personalization only when backed by provided or inspected evidence.
6. Provide variants by angle, seniority, or CTA when useful.
7. Include follow-up logic only if the user asks for a sequence.
8. Use `html-report-builder` for campaign or account-plan reports when needed.

## Checks

- Message is short enough for the channel.
- CTA is specific and low-friction.
- Claims are evidence-backed or removed.
- Personalization is not creepy, false, or generic filler.
- Tone fits buyer seniority and relationship stage.
- No sending, scraping, or CRM write is implied.

## Outputs

- outreach email
- LinkedIn or short message
- call opener
- follow-up sequence
- objection response
- account-specific value proposition
- outreach critique

## Boundary

This Skill owns sales messaging structure, buyer relevance, sequence reasoning, and CTA clarity. It does not own lead sourcing, email sending, CRM updates, deliverability setup, consent compliance, legal approval, or revenue forecasts.

It must not run shell, Python, Node, npm, curl, MCP, email, CRM, LinkedIn, dialer, enrichment, scraping, sequencing, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
