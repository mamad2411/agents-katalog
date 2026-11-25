---
name: process-automation-audit
description: "Identifies automation opportunities in business processes with tool recommendations, ROI estimates, and implementation priority rankings."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Process Automation Audit

## When to Use This Skill

Use this skill when you need to:
- Identify which business processes should be automated first
- Estimate ROI for automating specific workflows
- Get tool recommendations for automating repetitive tasks
- Build a prioritized automation roadmap for a solopreneur or small team

**DO NOT** use this skill for building the actual automations, writing code, or configuring specific tools. This is for auditing and planning only.

---

## Core Principle

AUTOMATE THE BORING, REPETITIVE, AND ERROR-PRONE — NEVER AUTOMATE WHAT REQUIRES JUDGMENT, CREATIVITY, OR HUMAN RELATIONSHIPS.

---

## Phase 1: Process Inventory

Map all current processes before identifying automation candidates.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | No default — must be provided |
| **Pain points** | "Which tasks eat the most time or cause the most frustration?" | No default |
| **Current tools** | "What tools/software do you currently use?" | Google Workspace, basic accounting |
| **Team size** | "How many people handle operations?" | 1 (solopreneur) |
| **Budget for tools** | "Monthly budget for automation tools?" | $50-100/month |
| **Tech comfort** | "Rate your comfort with tech setup: low, medium, high" | Medium |

### Process Mapping

For each process the user describes, document:

```
## Process: [Name]

**Frequency:** [Daily/Weekly/Monthly]
**Time per occurrence:** [X minutes/hours]
**Monthly time cost:** [Frequency x Time]
**Error rate:** [Low/Medium/High]
**Current method:** [Manual/Semi-automated/Fully manual]
**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

**GATE: Present the process inventory and confirm completeness before scoring.**

---

## Phase 2: Score and Prioritize

Evaluate each process for automation potential.

### Automation Scoring

Score each process on four dimensions (1-5):

| Dimension | 1 (Low) | 5 (High) |
|-----------|---------|----------|
| **Time savings** | Under 30 min/month | Over 5 hours/month |
| **Repeatability** | Varies every time | Same steps every time |
| **Error impact** | Errors are trivial | Errors cost money or reputation |
| **Ease of automation** | Requires custom dev | Off-the-shelf tool exists |

```
## Automation Priority Matrix

| Process | Time Saved | Repeatability | Error Impact | Ease | Total | Priority |
|---------|-----------|---------------|-------------|------|-------|----------|
| Invoice sending | 5 | 5 | 4 | 5 | 19 | HIGH |
| Social scheduling | 4 | 4 | 2 | 5 | 15 | MEDIUM |
| Report generation | 3 | 3 | 3 | 2 | 11 | LOW |
```

### ROI Estimate

For each high-priority process:

```
**Process:** Invoice sending
**Current time cost:** 4 hours/month
**Hourly value of your time:** $100
**Monthly cost of manual process:** $400
**Recommended tool:** [Tool name]
**Tool cost:** $30/month
**Setup time:** 2 hours (one-time)
**Monthly time after automation:** 30 minutes
**Monthly savings:** $350 (net of tool cost)
**Payback period:** Immediate
```

**GATE: Present priorities and ROI estimates. Get approval before recommending tools.**

---

## Phase 3: Tool Recommendations

Match each automation opportunity with specific tools.

### Recommendation Format

For each process, recommend 1-2 tools:

```
## Recommended Automations

### 1. [Process Name] — Priority: HIGH

**Recommended tool:** [Primary recommendation]
**Alternative:** [Backup option]
**What it automates:** [Specific steps from the process map]
**What still needs human input:** [Steps that cannot be automated]
**Setup complexity:** [Low/Medium/High]
**Monthly cost:** $[X]
**Integration with current stack:** [How it connects to existing tools]
```

### Common Solopreneur Automation Stack

Reference these categories when making recommendations:
- **Email/CRM:** Follow-up sequences, lead tagging, welcome emails
- **Invoicing:** Recurring invoices, payment reminders, expense tracking
- **Scheduling:** Appointment booking, calendar management
- **Social media:** Content scheduling, cross-posting
- **Documents:** Proposal generation, contract sending
- **Reporting:** Dashboard creation, metric alerts

---

## Phase 4: Implementation Roadmap

Deliver a phased plan for implementing automations.

### 90-Day Roadmap

```
## Automation Roadmap

**Month 1 — Quick Wins**
- [ ] Set up [Tool 1] for [Process] (estimated: 2 hours)
- [ ] Set up [Tool 2] for [Process] (estimated: 1 hour)
- Expected time savings: [X] hours/month

**Month 2 — Core Systems**
- [ ] Implement [Tool 3] for [Process] (estimated: 4 hours)
- [ ] Connect [Tool 1] to [Tool 3] via [integration]
- Expected time savings: [X] hours/month

**Month 3 — Optimization**
- [ ] Review automation performance
- [ ] Fix any broken workflows
- [ ] Identify next batch of processes to automate
- Expected total time savings: [X] hours/month
```

### Maintenance Schedule

Recommend a monthly 30-minute automation check: verify workflows are running, review error logs, update any broken integrations.

---

## Anti-Patterns

- **Automating everything at once** — implement one automation at a time. Stack failures are hard to debug.
- **Automating broken processes** — fix the process first, then automate. Automating a bad process makes bad things happen faster.
- **Over-engineering** — a simple Zapier workflow beats a custom-coded solution for most solopreneurs.
- **Ignoring the human steps** — every automation has handoff points where a human needs to review, approve, or intervene.
- **No error handling** — automations fail silently. Always set up failure notifications.

---

## Recovery

- **User has no budget:** Recommend free tiers first (most tools have generous free plans). Prioritize automations that save enough time to justify paid upgrades later.
- **User is not technical:** Stick to no-code tools with visual builders. Avoid anything requiring API configuration.
- **User automates something and it breaks:** Help them identify the failure point, set up error alerts, and create a manual fallback procedure.
- **Process is too complex to automate fully:** Recommend semi-automation — automate the repeatable parts and keep human judgment for the rest.
- **User has analysis paralysis:** Pick the single highest-ROI automation and start there. One working automation builds confidence for the next.
