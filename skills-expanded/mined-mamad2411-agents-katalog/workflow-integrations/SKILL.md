---
name: workflow-integrations
description: PM productivity and issue-tracker integrations. Use when connecting planning tools, execution systems, and status automations across the product workflow.
source: https://github.com/github/docs/tree/main/content/issues/planning-and-tracking-with-projects
---

# Workflow Integrations

Patterns for connecting product planning, issue tracking, and workflow automation across teams.

## GitHub Signals

- GitHub Projects supports built-in automations, API-driven updates, and Actions-based workflow orchestration
- GitHub integrations guidance highlights Slack, Teams, GitHub Apps, and issue/project APIs as reusable workflow building blocks
- Product workflows stay healthier when status movement, intake, and reporting are automated rather than manually mirrored

## When to Use

- Sync product planning systems with engineering execution tools
- Automate status updates, triage, and backlog movement across repositories or teams
- Connect support, customer feedback, or analytics signals into roadmap workflows
- Design a workflow where humans decide priorities but machines handle routine state transitions

## Coverage Areas

### Work Intake And Triage

- Move customer feedback, sales requests, and support issues into a normalized backlog shape
- Define who owns deduplication, tagging, and severity assignment before automation starts writing into your system
- Keep the canonical source of truth explicit so duplicate tools do not drift

### Project Automation

- Use built-in automations first for simple state changes, then layer APIs or Actions for cross-system workflows
- Model the fields, transitions, and permissions that automation is allowed to change
- Prefer observable automations with audit trails, retries, and clear failure notifications

### Communication And Governance

- Route updates into chat or stakeholder channels without making those channels the system of record
- Protect sensitive roadmap or customer data before syncing across tools
- Document authentication, ownership, and maintenance expectations for every integration you add
