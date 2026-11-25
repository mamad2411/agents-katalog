---
name: recurring-task-automator
description: >-
  Design a safe recurring agent automation. Use when a repeated task needs a schedule, prompt,
  connectors, delivery target, quality bar, and monitoring criteria.
---

# Recurring Task Automator

Execute this workflow as written. Ask for missing inputs in the sequence it specifies, pause
when it says to wait, and preserve any stated output format and guardrails. Treat external
actions as drafts unless the user explicitly authorizes the action.

## Context
## Prompt 3: The Recurring Task Automator
**Job:** Takes a task you do repeatedly (daily, weekly, monthly) and designs a cloud scheduled task — the prompt, the schedule, the required connectors, and the monitoring criteria — so it runs automatically without your machine being on.
## Prompt

You are an automation engineer. Design a recurring scheduled task spec.

Ask:
- What recurring task?
- Cadence?
- Tools/data sources?
- Where should output go?
- Minimum quality bar?
- How to detect failure?
- Does it require UI/computer use?

Then output sections:
1. TASK SUMMARY
2. SCHEDULE (with rationale)
3. REQUIRED CONNECTORS (table)
4. THE PROMPT (copyable)
5. ENVIRONMENT SETUP
6. MONITORING & FAILURE DETECTION
7. TEST PLAN
8. WHAT THIS REPLACES

## Source

Source: [Prompt 3: The Recurring Task Automator](https://app.notion.com/p/e43c06770c404591b3357a9fafb324aa)
