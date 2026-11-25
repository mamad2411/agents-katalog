---
name: supplier-qbr-skill
description: "Prepares supplier QBRs by analyzing obligations, SLA performance, issues, actions, spend, risks, and priorities. Use for vendor performance reviews."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Supplier QBR and Performance Review Skill

## Purpose
This skill helps AI prepare a supplier quarterly business review or periodic performance review from contract obligations, SLA/KPI data, issues, actions, spend, changes, risks, stakeholder feedback, and renewal information.

It converts scattered reporting into a focused supplier-management discussion.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
A QBR should manage performance and value, not merely present updates.

The workflow is:

**Collect -> Validate -> Compare to Contract -> Identify Trends -> Prioritize Issues -> Prepare Questions -> Agree Actions -> Track**

## When to Use
Use this skill for:

- Supplier QBR preparation
- Monthly or quarterly performance reviews
- Contract governance meetings
- SLA and KPI trend analysis
- Escalation preparation
- Renewal-readiness review
- Corrective action follow-up
- Supplier action tracking
- Executive supplier briefings

## Do Not Use This Skill For
Do not use it to:

- Accept supplier-reported data without validation
- Change performance records
- Approve service credits or remedies
- Make renewal or termination decisions
- Treat every missed target as equally material
- Replace the contract owner, business owner, or vendor manager

## Required Inputs
- Contract and SOW
- SLA/KPI reports
- Issue and escalation logs
- Previous QBR minutes
- Open actions
- Corrective action plans
- Invoices and spend
- Change requests
- Service credits
- Stakeholder feedback
- Risk assessments
- Contract and renewal dates
- Supplier improvement commitments

## Workflow

### Step 1: Establish Review Period and Objectives
Identify:

- Period covered
- Supplier and services
- Audience
- Business criticality
- Current concerns
- Renewal horizon
- Decisions needed

### Step 2: Extract Contractual Commitments
Capture:

- Deliverables
- SLAs/KPIs
- Reporting
- Governance
- Improvement obligations
- Pricing commitments
- Audit or compliance obligations
- Transition and renewal obligations

### Step 3: Validate Performance Data
Check:

- Data source
- Reporting completeness
- Exclusions
- Measurement method
- Missing periods
- Inconsistent definitions
- Supplier-reported vs buyer-validated data

### Step 4: Compare Performance to Commitments
Use:

| Metric / Obligation | Target | Actual | Trend | Evidence | Status | Action |
|---|---|---|---|---|---|---|

### Step 5: Identify Trends and Recurring Issues
Review:

- Repeated incidents
- Recurring root causes
- Overdue actions
- Missed reports
- Unresolved service credits
- Scope creep
- Change-order growth
- Stakeholder dissatisfaction
- Improvement or deterioration

### Step 6: Review Commercial and Contract Value
Check:

- Spend vs contract
- Invoice accuracy
- Price increases
- Unused licences or services
- Service credits
- Change requests
- Contract leakage
- Value-add commitments
- Renewal exposure

### Step 7: Review Risk and Renewal Readiness
Check:

- Operational dependency
- Supplier capacity
- Security/privacy/compliance events
- Subcontractor issues
- Business continuity
- Lock-in
- Renewal date and notice period
- Exit readiness
- Alternative options

### Step 8: Prepare Supplier Questions
Focus on evidence, cause, remediation, ownership, and timing.

| Topic | Question | Evidence | Desired Outcome | Owner |
|---|---|---|---|---|

### Step 9: Build the QBR Agenda
Suggested structure:

1. Executive summary
2. Previous actions
3. SLA/KPI performance
4. Major incidents and root causes
5. Commercial and contract review
6. Risks and changes
7. Improvement plan
8. Renewal/roadmap, where appropriate
9. Decisions and actions

### Step 10: Prepare the Action Register
Use:

| Action | Owner | Due Date | Evidence of Completion | Status | Escalation |
|---|---|---|---|---|---|

## Output Format

### Executive Performance Summary
```text
Overall supplier performance for [period] is [status]. Strengths are [items]. Main concerns are [items]. Decisions or escalations required are [items].
```

### Performance Scorecard
| Area | Target | Actual | Trend | Status | Commentary |
|---|---|---|---|---|---|

### Issue and Action Summary
| Issue / Action | Impact | Owner | Due Date | Status | Escalation Needed |
|---|---|---|---|---|---|

### Renewal Readiness
| Area | Current Position | Risk | Required Action | Owner |
|---|---|---|---|---|

## Review Checks
- Supplier data is validated or clearly marked
- Contract commitments are used as the baseline
- Trends are distinguished from one-time events
- Overdue actions are visible
- Commercial leakage and renewal risks are included
- Questions are specific and evidence-based
- Final supplier decisions remain human-owned

## Human Review
Humans must approve:

- Performance ratings
- Escalations
- Remedies and service credits
- Corrective actions
- Renewal strategy
- Supplier communications
- Termination or transition decisions

## Guardrails
The AI must not:

- Assume supplier-reported data is accurate
- Alter performance records
- Apply remedies automatically
- Make final renewal or termination decisions
- Expose confidential data unnecessarily
- Ignore business-owner context
- Present unverified allegations as fact

## Example User Request
```text
Use supplier-qbr-skill.md to prepare a QBR from the contract, SLA reports, issue log, prior actions, spend, stakeholder feedback, and renewal dates. Identify trends, risks, questions, and actions.
```

## Success Criteria
This skill is working when it helps procurement:

- Prepare faster without losing substance
- Compare performance to contractual commitments
- Identify recurring issues and value leakage
- Improve action ownership
- Enter renewal discussions earlier
- Manage the supplier relationship with evidence
