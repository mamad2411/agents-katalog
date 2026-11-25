---
name: demo-build
description: Build a copy-paste-ready Process Street demo workflow for a prospect — confirm scope, map discovery pain to demo moments, draft the workflow blueprint (tasks, typed fields, conditional logic, approvals, integrations), and supply talking points. Use when someone says "build a demo", "demo build", "build demo", "build a workflow demo", "build me a demo", or wants a prospect-facing PS demo from a use case, transcript, or SOP.
---

# PS Demo Build Skill

## Purpose

Build a custom Process Street demo for a prospect. Output must be **copy-paste ready** for the PS AI Builder or manual workflow construction.

---

## Inputs Required

Provide any combination of:
- Company name + URL
- Use case / goal (what workflow to build)
- A discovery-call transcript or recording
- SOPs, spreadsheets, or process documentation from the team
- Audience context (who will watch the demo and what they care about)

---

## Output Structure

Always produce in this order:

### 1. Demo Scope Confirmation

Before building, confirm:
- **Workflow title** (what it will be called in PS)
- **Trigger** (manual, Salesforce, webhook, schedule)
- **Primary user** (who runs this workflow day-to-day)
- **Key outcome** (what "done" looks like)
- **Demo constraints** (time limit, live vs. recorded, AI Builder vs. manual)

### 2. GAP → Demo Mapping

| GAP Element | Demo Moment |
|-------------|-------------|
| Current state pain | Show before (chaos/manual) → after (PS) |
| Key integration need | Show the integration live if possible |
| Reporting gap | Show the dashboard/overview |
| Compliance requirement | Show form fields, audit trail, required steps |

### 3. Workflow Blueprint

Provide step-by-step, copy-paste ready:

```
## [Section Header]

### Task 1: [Task Name]
- Assignee: [role or person]
- Due date: [X days from trigger or specific]
- Form fields:
  - [Field name] — [type: text/dropdown/date/file/checkbox]
  - [Field name] — [type]
- Content/instructions: [what the task assignee sees]
- Conditional logic: [if X then Y]
- Automations: [what fires on completion]

### Task 2: [Task Name]
...
```

### 4. Integration Points

For each integration needed:
- Tool (Salesforce, Jira, Zapier, API)
- Trigger/action
- Whether PS supports it natively or via Zapier
- Any known gotchas

### 5. What to Say During the Demo

3–5 talking points that connect workflow steps to the prospect's specific pain from the discovery transcript.

---

## Demo Build Speed Modes

| Mode | When to Use | Output |
|------|-------------|--------|
| **Fast** | < 30 min to build | Blueprint only, no detailed content |
| **Standard** | 1–2 hours | Full blueprint with copy-paste fields |
| **Deep** | 2+ hours | Full blueprint + talking points + integrations |

Default to **Standard** unless the user specifies otherwise.

---

## Common PS Components to Include

- **Conditional logic**: "If [field] = X then show/hide/assign Y"
- **Approvals**: Flag any task that should require sign-off
- **Due dates**: Use relative dates (e.g., "3 days after task X completes")
- **Assignees**: Separate tasks by role, not individual
- **Automations**: Slack/email notifications on completion, Salesforce field updates
- **Form fields**: Use dropdowns for compliance-sensitive fields; free text for context

---

## Example Patterns

| Use Case | Key Pattern |
|----------|-------------|
| Lead-to-Lease Policy | SOPs → workflow blueprint; conditional logic by state |
| Financial Statement Process | Excel tracker → PS workflow; many client associations |
| Client Onboarding (Tier 1) | Salesforce trigger, first 30 days only |
| Investment Approval | Discovery transcript + Excel process map |
| HR Onboarding | Sector compliance; GAP analysis → demo plan |
