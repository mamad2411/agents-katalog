---
name: sla-review-skill
description: "Reviews SLAs and KPIs for clear metrics, measurement, reporting, remedies, escalation, and business criticality. Use before award or during contract management."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement SLA Review Skill

## Purpose
This skill helps AI support procurement professionals with structured review of service levels, KPIs, performance requirements, service credits, reporting obligations, escalation processes, and supplier performance management language.

Use this skill when reviewing or drafting SLA/KPI content for an RFP, contract, SOW, supplier proposal, vendor performance framework, or QBR preparation.

This skill should not create generic SLA language. It should help determine whether each SLA is measurable, reportable, enforceable, commercially appropriate, and aligned to business criticality.

This skill does not finalize legal remedies, approve penalties, set operational targets without business-owner validation, or replace procurement, legal, finance, technical, or business-owner review.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
A weak SLA often looks fine until something goes wrong.

The AI should not only ask whether an SLA exists.

It should ask whether the SLA can actually be managed after award.

Every SLA should pass five tests:

**Metric -> Measurement -> Reporting -> Remedy -> Escalation**

If one of these is missing, the SLA may be difficult to manage, enforce, or use in supplier performance discussions.

## When to Use
Use this skill when the user needs help with:

- SLA review
- KPI review
- Service level drafting
- Performance requirement drafting
- RFP/RFB/RFQ/SOW SLA sections
- Contract SLA schedules
- Supplier proposal review
- Vendor performance management framework
- Service credit review
- Reporting obligation review
- Escalation process review
- QBR preparation
- Supplier performance issue analysis
- SLA gap analysis
- Business-owner SLA validation questions

## Do Not Use This Skill For
Do not use this skill to:

- Invent operational targets
- Finalize legal remedies
- Create penalties without human review
- Apply the same SLA structure to every service without context
- Ignore business criticality
- Replace technical, operational, legal, finance, or business-owner review
- Approve supplier performance remedies
- Make final contract decisions
- Score supplier submissions in an active evaluation

## Required Inputs
Before starting, identify which of the following inputs are available.

### Service Context
- What service, system, product, or supplier obligation is being measured?
- Why is the service important?
- Who are the end users?
- What is the business impact if performance fails?
- Is the service business-critical, operationally important, or low risk?
- Is this pre-award drafting, contract negotiation, post-award management, or QBR review?

### SLA/KPI Content
- Existing SLA/KPI table or clause
- Service description
- Performance targets
- Measurement method
- Reporting frequency
- Supplier reporting obligations
- Service credit or remedy language
- Escalation process
- Exclusions
- Governance model
- Issue management process
- Historical performance data, if available

### Operational Inputs
- Support hours
- Response and resolution expectations
- Severity levels
- Availability expectations
- Maintenance windows
- Incident management process
- Business continuity requirements
- Implementation dependencies
- User volumes
- Transaction volumes
- Critical periods
- Reporting cadence
- Governance meeting cadence

### Commercial and Contract Inputs
- Contract term
- Supplier obligations
- Remedies
- Service credits
- Termination rights
- Renewal terms
- Vendor performance management language
- Acceptance criteria
- Transition/exit obligations
- Pricing impact of service levels

### Output Need
- What should the final output be?
- Is this for RFP drafting, contract review, negotiation, supplier clarification, business-owner discussion, QBR preparation, or performance issue review?
- Should the output be a table, memo, revised SLA wording, checklist, or stakeholder question list?

## Missing Information Rule
If key SLA inputs are missing, do not invent them.

Proceed with assumptions only where reasonable and clearly flag what needs business-owner confirmation.

Use this format:

```text
Assumptions I am using:
- ...

Missing SLA information:
- ...

Questions for the business owner:
- ...

Items requiring legal/procurement review:
- ...
```

If a target cannot be recommended safely without operational context, say so and provide a question instead of inventing a target.

## Workflow

### Step 1: Understand the SLA Context
Restate the service/performance issue in plain language.

Identify:

- Service being measured
- Business criticality
- Procurement or contract stage
- Supplier obligation
- Buyer impact if performance fails
- Required output
- Human reviewers needed

### Step 2: Extract Each SLA or KPI
Break the SLA section into individual obligations or metrics.

Use this table:

| SLA / KPI | Service Area | Target / Standard | Reporting Requirement | Remedy / Escalation | Notes |
|---|---|---|---|---|---|

If the SLA is written in paragraph form, extract each measurable or implied performance obligation.

### Step 3: Run the Five-Part SLA Test
For each SLA, check the following.

#### 1. Metric
What exactly is being measured?

Examples:

- Availability
- Response time
- Resolution time
- Incident severity
- Delivery milestone
- Report submission
- Processing time
- Accuracy rate
- Defect rate
- Implementation milestone
- Customer satisfaction
- Compliance activity
- Issue backlog
- Root cause analysis completion

#### 2. Measurement
How is performance calculated or verified?

Check:

- Formula
- Data source
- Measurement period
- System of record
- Evidence required
- Exclusions
- Who validates performance

#### 3. Reporting
How is performance reported?

Check:

- Reporting frequency
- Report format
- Recipient
- Delivery timeline
- Supporting data
- Exception reporting
- Governance forum

#### 4. Remedy
What happens if the target is missed?

Check:

- Service credit
- Corrective action plan
- Root cause analysis
- Remediation timeline
- Escalation
- Cure period
- Repeated failure consequences
- Termination trigger, if applicable

#### 5. Escalation
What happens if the issue repeats or becomes serious?

Check:

- Escalation path
- Supplier executive involvement
- Buyer governance forum
- Issue priority
- Action tracking
- Repeated failure management
- Dispute resolution interface

### Step 4: Identify SLA Weaknesses
Flag common weaknesses:

- Vague wording
- No target
- No defined measurement method
- No reporting cadence
- No owner
- No remedy
- No service credit
- No escalation path
- No severity definitions
- No exclusions
- No business continuity link
- No repeated failure consequence
- No root cause analysis requirement
- No corrective action plan
- Target not aligned to business criticality
- SLA not tied to supplier reporting obligations
- SLA not tied to governance meetings

### Step 5: Assess Business Criticality
Classify each SLA by business impact.

Possible levels:

- Critical
- High
- Medium
- Low
- Needs business-owner validation

Check:

- Would failure stop business operations?
- Would failure affect users, patients, customers, or clients?
- Would failure create compliance, privacy, security, financial, or reputational risk?
- Would failure affect service continuity?
- Would failure create additional cost?
- Is the SLA proportionate to the risk?

Do not assume business criticality if the context is unclear.

### Step 6: Review Service Credits and Remedies
If service credits or remedies are included, check:

- Are they clear?
- Are they meaningful?
- Are they proportionate?
- Are they tied to the right metrics?
- Are they capped?
- Are they the only remedy?
- Do repeated failures trigger stronger action?
- Are service credits automatic or claimed?
- Are reporting and calculation methods clear?
- Is legal review needed?

Do not finalize penalties or legal remedies. Flag them for legal and commercial review.

### Step 7: Review Reporting and Governance
Check whether SLA management is operationally practical.

Ask:

- Who provides SLA reports?
- How often are reports provided?
- What data supports the report?
- Is there a governance meeting?
- Are missed SLAs tracked?
- Are action items documented?
- Are repeated issues escalated?
- Is supplier performance reviewed in QBRs?
- Are corrective action plans required?

### Step 8: Prepare Revised SLA Suggestions
When appropriate, suggest improved wording or structure.

Suggested SLA structure:

```text
The Supplier shall [perform service obligation] within [target/threshold], measured by [measurement method], reported [frequency] through [reporting mechanism]. Failure to meet the target shall require [remedy/corrective action/service credit], with repeated failures escalated through [escalation process].
```

Only suggest targets if the user provided sufficient operational context. Otherwise, leave placeholders and provide business-owner questions.

### Step 9: Prepare Business-Owner Questions
Generate questions the procurement professional can ask the business owner.

Examples:

- What level of downtime is acceptable?
- What is the business impact of delayed response?
- Which incidents are critical vs high vs medium?
- What reporting cadence do you need to manage the supplier?
- What evidence should the supplier provide?
- What should happen after repeated failures?
- Are service credits meaningful for this service?
- What implementation milestones should be tracked?
- Are maintenance windows acceptable?
- What exclusions should be allowed?

### Step 10: Identify Human Review Items
Flag where human review is needed.

Examples:

- Business owner validates operational targets
- Technical team validates measurement method
- Procurement validates performance framework
- Legal validates remedies and service credit language
- Finance validates commercial impact of credits or remedies
- Security/privacy validates related incident metrics
- Contract manager validates reporting and governance process

## Output Format

### Short Summary
Start with a plain-language summary.

```text
Summary:
The SLA section includes [number/type] of performance obligations. The main weaknesses are [weaknesses]. The highest-risk gaps are [gaps]. Business-owner review is needed for [items]. Legal/procurement review is needed for [items].
```

### SLA Review Table
Use this table:

| SLA / KPI | Metric Clear? | Measurement Clear? | Reporting Clear? | Remedy Clear? | Escalation Clear? | Risk / Comment |
|---|---|---|---|---|---|---|

### Weakness Table
Use this table:

| SLA / Clause | Weakness | Why It Matters | Suggested Improvement | Human Review Needed |
|---|---|---|---|---|

### Missing KPI List
Use this table:

| Service Area | Missing KPI / SLA | Why It May Be Needed | Business-Owner Question |
|---|---|---|---|

### Suggested Revised Wording
Use this format:

| Current Wording | Issue | Suggested Revised Wording | Review Needed |
|---|---|---|---|

### Business-Owner Questions
Use this table:

| Topic | Question | Why This Matters |
|---|---|---|

### Human Review Items
Use this table:

| Reviewer | Item to Review | Why It Matters |
|---|---|---|

## Review Checks
Before finalizing, check:

- Did every SLA pass the metric, measurement, reporting, remedy, escalation test?
- Are vague terms flagged?
- Are missing measurement methods flagged?
- Are reporting obligations clear?
- Are remedies or service credits clearly marked for review?
- Are repeated failure scenarios addressed?
- Are business-owner validation questions included?
- Are legal/commercial review items clearly separated?
- Did the output avoid inventing operational targets?
- Did the output avoid final legal conclusions?
- Did it account for business criticality?

## Human Review
Humans must review and approve:

- Final SLA targets
- Severity levels
- Measurement methods
- Reporting cadence
- Service credits
- Remedies
- Escalation process
- Repeated failure consequences
- Business continuity requirements
- Legal enforceability
- Commercial reasonableness
- Supplier performance management process

## Guardrails
The AI must not:

- Invent operational targets
- Finalize legal remedies
- Create penalties without review
- Treat service credits as automatically appropriate
- Ignore business criticality
- Apply the same SLA to every service
- Assume supplier reporting is reliable without validation
- Ignore exclusions
- Ignore repeated failure scenarios
- Replace business-owner, technical, procurement, legal, or finance review
- Make final contract decisions

## Example User Request
```text
Use the sla-review-skill.md workflow to review these SLAs. Identify which clauses are hard to manage after award, what is missing, what should be clarified, and what business-owner questions we should ask.
```

## Example Output Instruction
```text
Do not simply rewrite the SLA section. Test each SLA against metric, measurement, reporting, remedy, and escalation. Provide a weakness table, missing KPI list, revised wording suggestions, business-owner questions, and human review items.
```

## Success Criteria
This skill is working when it helps the user:

- Move from generic SLA drafting to structured SLA review
- Identify weak or vague service levels before contract award
- Improve supplier performance management language
- Create better business-owner questions
- Separate operational targets from legal remedies
- Improve reporting, governance, and escalation structure
- Keep final SLA decisions with accountable humans
