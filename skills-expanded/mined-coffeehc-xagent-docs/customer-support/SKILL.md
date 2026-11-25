---
name: customer-support
description: Use when drafting, rewriting, triaging, summarizing, or reviewing customer support replies, ticket notes, escalation summaries, bug reports from customer issues, refund or policy responses, troubleshooting steps, or service recovery messages. Prefer this Skill when the task needs empathy, accuracy, SLA awareness, issue classification, escalation criteria, or next-step clarity. Do not use for sending messages, granting refunds, legal commitments, or unsupported technical claims.
meta:
  version: 1
  display_name: 客服支持
---

# Customer Support

## Purpose

Produce clear, empathetic, accurate customer support work that separates what is known, what needs troubleshooting, what must be escalated, and what can be promised.

## Use When

Use for:

- customer reply drafts
- ticket triage
- troubleshooting instructions
- escalation summaries
- refund or policy response drafts
- customer issue summaries for engineering
- service recovery messages

## Material Gate

Identify:

- customer issue, product area, account context, severity, and channel
- known facts, logs, screenshots, order data, or prior replies
- policy, SLA, entitlement, or refund rules
- desired tone and next action

Do not invent diagnosis, policy approval, credits, refunds, timelines, or engineering commitments.

## Workflow

1. Classify issue type, severity, urgency, and owner.
2. Extract confirmed facts and unknowns.
3. Decide whether the response should troubleshoot, acknowledge, escalate, resolve, or request information.
4. Draft with empathy first, then concrete action.
5. Include only steps the customer can safely perform.
6. Escalate when impact, risk, missing access, policy, or technical uncertainty exceeds support authority.
7. Use `html-report-builder` for support trend reports or incident-style customer impact summaries.

## Checks

- Reply acknowledges the customer's problem directly.
- Promises are limited to verified authority.
- Troubleshooting steps are ordered, safe, and clear.
- Escalation includes facts, impact, reproduction, and requested help.
- Internal notes are not mixed into customer-facing copy.

## Outputs

- customer reply
- ticket summary
- escalation brief
- troubleshooting checklist
- bug report from support evidence
- service recovery message
- support trend summary

## Boundary

This Skill owns support communication, issue triage, escalation framing, and troubleshooting explanation. It does not own refund approval, legal commitments, account actions, product changes, incident command, or external message sending.

It must not run shell, Python, Node, npm, curl, MCP, helpdesk, CRM, billing, email, chat, refund, account-management, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
