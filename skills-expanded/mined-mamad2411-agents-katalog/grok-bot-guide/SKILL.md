---
name: grok-bot-guide
description: Decision guide from the @tinrovicai carousel "8 things Grok Bot can do while your laptop is closed" - what an autonomous cloud agent is versus a chatbot, eight business use cases (sales outreach, recruiting, paid media monitoring, expense reporting, account health, chief of staff, bug reproduction, product KPI monitoring), the six-step setup, rules-based tools (Zapier, n8n) versus judgment-based agents, the beta risks, and a pilot test. Use when deciding whether a recurring task suits an autonomous agent or a fixed workflow, or when planning a first agent pilot. The Grok Bot product claims are the source's and were not verified. Source @tinrovicai (Batch 101).
---

# Autonomous agent guide (from the Grok Bot carousel)

**Verification:** the carousel describes xAI's "Grok Bot", "now in early beta". I could not verify the product, its pricing or its claims from the slides, so use this as a decision framework that applies to any autonomous agent, not as a product review.

## Chat versus bot

| | Chat | Bot |
|---|---|---|
| You give it | a text prompt | a task to own |
| You get back | an answer or draft | a finished action across apps |
| You are needed | every turn | only for approvals |
| It runs for | one turn | hours to days, unattended |

## Eight tasks to hand over (use cases 01 to 08)

1. **Sales outreach:** research prospects, draft personalised sequences, log CRM activity.
2. **Recruiting:** scan LinkedIn, job boards and GitHub, score candidates against your brief.
3. **Paid media monitoring:** watch ad performance, flag anomalies, draft budget recommendations.
4. **Expense reporting:** categorise receipts, reconcile spend against budgets, build finance-ready reports.
5. **Account health:** track usage signals, flag at-risk accounts, surface upsell triggers.
6. **Chief of staff:** manage calendars, triage the inbox, draft briefings, prep meeting agendas.
7. **Bug reproduction:** replicate a reported bug in a sandbox and log structured findings.
8. **Product KPI monitoring:** track DAU, retention and conversion, alert on breaches, send weekly summaries.

Here these map to OS agents where they exist: `os-prospect`, `os-ads`, `os-bookkeeping`, `os-health`, `os-chief-of-staff`, `os-business-analyst`. Those draft only and a human approves.

## How it works under the hood

Its own cloud computer, so work continues with your laptop off. You hand over session credentials once and it signs in as you. It acts, then asks when a human is needed. **Limit credential scope and review permissions**, because a bot with your logins can do anything you can.

## Set up your first bot (6 steps)

1. Define the goal. 2. Record one clean example. 3. Set a trigger or schedule. 4. Test across 3 to 5 runs. 5. Deploy. 6. Monitor and refine. Record clean, linear workflows and skip edge cases on the first run.

## Rules or judgment?

- **Rule-based, repetitive, high-volume, predictable:** Zapier or n8n. n8n adds self-hosting and data control.
- **Judgment-heavy, adaptive:** an agent you message like a coworker, which makes calls mid-workflow. Faster to start for non-developers.

## Before you commit (the beta caveats on slide 07)

Task drift on complex multi-branch workflows; the login handover raises security questions; fewer native integrations than Zapier; a thinner audit trail than n8n or enterprise RPA. **Good fit:** startups, lean ops teams, solo founders, technical product teams. **Wait if** you are heavily regulated or need full audit logs or on-prem.

## Your move

Pick one use case, run a small pilot, measure hours saved. The test: if you would hand it to a junior employee with a checklist, it is a bot task. Command: `/bot-task-test`.
