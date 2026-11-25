---
name: automation-workflow
description: "Designs automation workflows with trigger-action sequences, tool connections, and error handling procedures. Use when automating repetitive business processes."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Automation Workflow

## When to Use This Skill

Use this skill when you need to:
- Design an automation workflow for a repetitive business process
- Map trigger-action sequences connecting multiple tools
- Build error handling and monitoring for automated processes
- Document automation workflows for maintenance and troubleshooting

**DO NOT** use this skill for coding custom integrations, selecting automation tools, or one-time batch processes. This is for designing repeatable automated workflows.

---

## Core Principle

AUTOMATE PROCESSES THAT ARE REPEATABLE, RULE-BASED, AND TIME-CONSUMING — IF A TASK REQUIRES JUDGMENT EVERY TIME, IT NEEDS A HUMAN, NOT AN AUTOMATION.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Process to automate** | "What repetitive task do you want to automate?" | No default — must be provided |
| **Current steps** | "Walk me through the manual steps, in order." | No default — must be provided |
| **Frequency** | "How often does this process run? Per day, week, trigger?" | Multiple times per week |
| **Tools involved** | "What tools are involved in this process?" | No default — list all tools |
| **Automation platform** | "Do you use Zapier, Make, n8n, or another automation tool?" | Zapier |
| **Error tolerance** | "What happens if the automation fails? Critical or minor impact?" | Minor — can recover manually |

**GATE: Confirm the brief before mapping the workflow.**

---

## Phase 2: Map the Workflow

### Process Documentation

Document the current manual process step by step:

```
## Current Manual Process: [Name]

**Trigger:** [What initiates this process]
**Steps:**
1. [Action] in [Tool] — [Time estimate]
2. [Action] in [Tool] — [Time estimate]
3. [Action] in [Tool] — [Time estimate]
...
**Output:** [What the completed process produces]
**Total time:** [X minutes/hours per occurrence]
**Frequency:** [X times per week/month]
```

### Automation Design

Convert manual steps to trigger-action format:

```
## Automated Workflow: [Name]

**Trigger:** [Event that starts the automation]
  ↓
**Step 1:** [Action] — [Tool] → [Output]
  ↓
**Step 2:** [Filter/Condition] — Only continue if [criteria]
  ↓
**Step 3:** [Action] — [Tool] → [Output]
  ↓
**Step 4:** [Action] — [Tool] → [Output]
  ↓
**End:** [Final output or notification]
```

### Decision Points

Identify steps that require conditions:

| Decision | If True | If False |
|----------|---------|----------|
| [Condition 1] | Continue to Step 3 | Skip to Step 5 |
| [Condition 2] | Send notification | Log and stop |

**GATE: Confirm the workflow map before building error handling.**

---

## Phase 3: Build

### Step-by-Step Setup Guide

For each step in the automation, document:

```
### Step [X]: [Action Name]

**Tool:** [Tool name]
**Trigger/Action:** [Specific trigger or action type]
**Configuration:**
- Field 1: [Value or mapping]
- Field 2: [Value or mapping]
- Field 3: [Value or mapping]

**Data mapping:**
- Input: [Where this data comes from]
- Output: [What this step produces for the next step]

**Test:** [How to verify this step works correctly]
```

### Error Handling

For each step, define failure scenarios:

| Step | Failure Mode | Detection | Recovery |
|------|-------------|-----------|----------|
| Step 1 | Trigger does not fire | Monitor for expected frequency | Check trigger configuration |
| Step 2 | API connection fails | Error notification | Retry 3 times, then alert |
| Step 3 | Data format mismatch | Validation check | Log error, skip record, notify |
| Step 4 | Destination unavailable | Error notification | Queue and retry in 1 hour |

### Monitoring Setup

- **Success notification:** Optional confirmation when the workflow completes
- **Failure alert:** Immediate notification (email or Slack) on any step failure
- **Daily digest:** Summary of runs, successes, and failures
- **Monthly review:** Check automation is still running correctly and producing expected results

---

## Phase 4: Polish

### 1. Workflow Documentation

```
## Workflow Documentation: [Name]

**Purpose:** [What this automation does in one sentence]
**Created:** [Date]
**Owner:** [Name]
**Platform:** [Zapier/Make/n8n]
**Estimated time saved:** [X] hours per [week/month]

### Workflow Diagram
[Trigger] → [Step 1] → [Condition] → [Step 2] → [Step 3] → [Output]

### Dependencies
- [Tool 1] account with [plan requirement]
- [Tool 2] API key or integration enabled
- [Data source] must be in [format]

### Maintenance
- Check monthly that all connections are active
- Update if any connected tool changes its API
- Review if the business process changes
```

### 2. ROI Calculation

```
## Automation ROI

**Time per manual execution:** [X] minutes
**Frequency:** [X] times per [period]
**Total manual time:** [X] hours per month
**Your hourly rate:** $[X]
**Monthly value of time saved:** $[X]
**Automation tool cost:** $[X]/month
**Net monthly savings:** $[X]
```

### 3. Quality Checklist

```
## Automation Workflow Checklist

- [ ] Manual process documented step by step with time estimates
- [ ] Trigger clearly defined (event, schedule, or condition)
- [ ] Each step has specific tool, action, and configuration documented
- [ ] Decision points and conditions are mapped
- [ ] Error handling defined for each step (detection + recovery)
- [ ] Failure alerts configured (email or Slack notification)
- [ ] Workflow tested end-to-end with real data
- [ ] Documentation includes dependencies and maintenance notes
- [ ] ROI calculated (time saved vs. tool cost)
- [ ] Monthly review scheduled to verify continued function
```

---

## Example

**Process:** New customer onboarding

```
## Automated Workflow: New Customer Onboarding

**Trigger:** New payment received in Stripe
  ↓
**Step 1:** Create customer record in CRM (Notion/Airtable)
  ↓
**Step 2:** Send welcome email via email tool (with login credentials)
  ↓
**Step 3:** Add customer to onboarding email sequence
  ↓
**Step 4:** Create project in project management tool
  ↓
**Step 5:** Send Slack notification to team: "New customer: [Name]"
  ↓
**End:** Customer is set up in all systems automatically

**Time saved:** 25 minutes per new customer × 8 new customers/month = 3.3 hours/month
**Tool cost:** $20/month (Zapier Starter)
**ROI:** $247/month saved at $75/hour
```

---

## Anti-Patterns

- **Automating a broken process** — if the manual process is flawed, the automation just breaks faster. Fix the process first.
- **No error handling** — automations fail silently unless you build alerts. Always configure failure notifications.
- **Over-automating** — a 15-step automation with 8 conditions is fragile. If it breaks, nobody knows how to fix it. Keep workflows under 7 steps.
- **No documentation** — an automation nobody understands is an automation nobody can fix or improve.
- **Skipping the test** — always test with real data before relying on the automation. Edge cases reveal themselves in testing.

---

## Recovery

- **Automation stops working:** Check each connection. Most failures come from expired API tokens or changed tool permissions.
- **Wrong data flowing through:** Add a validation step that checks data format before processing. Log rejected records.
- **Automation runs too often or not enough:** Verify the trigger configuration. Add rate limits or scheduling constraints.
- **Process changes but automation does not:** This is why documentation matters. Review the workflow whenever the business process changes.
