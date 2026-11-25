---
name: procurement-intake-skill
description: "Reviews procurement intake requests, identifies missing information and risks, and prepares stakeholder questions. Use at the start of a sourcing or renewal request."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement Intake and Triage Skill

## Purpose
This skill helps AI review an incoming procurement request before a sourcing strategy is selected.

Use it to separate the underlying business need from a proposed solution, identify missing information, classify risk and complexity, prepare stakeholder questions, and recommend possible next steps for human consideration.

This skill does not approve a purchase, choose a sourcing method, authorize a supplier, interpret policy as final authority, or replace procurement judgment.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
Do not automate an unclear request.

The workflow is:

**Understand -> Separate Need from Solution -> Identify Gaps -> Classify -> Assess Risk -> Prepare Questions -> Present Options -> Human Decision**

## When to Use
Use this skill for:

- New procurement requests
- Renewal or extension requests
- Preferred-supplier requests
- Urgent or emergency requests
- SaaS or software intake
- Consulting or professional services intake
- Goods, services, managed services, and hybrid requirements
- Early sourcing strategy preparation
- Requests with unclear scope, budget, timeline, or ownership
- Requests that may involve privacy, security, accessibility, legal, or financial review

## Do Not Use This Skill For
Do not use this skill to:

- Approve the request
- Select a sourcing method as a final decision
- Validate a sole-source justification as final
- Select or recommend a supplier for award
- Bypass competition, policy, approvals, or governance
- Invent requirements, budgets, timelines, or risk classifications
- Treat urgency as proof that competition is impossible

## Required Inputs
Collect what is available from the following areas.

### Business Need
- Problem or opportunity
- Desired outcome
- Users or beneficiaries
- Current process or solution
- Consequence of doing nothing
- Business criticality

### Proposed Requirement
- Scope
- Deliverables
- Quantity, users, licences, sites, transactions, or volumes
- Implementation needs
- Support and maintenance
- Integrations
- Data migration
- Training
- Transition and exit needs

### Commercial Context
- Estimated budget or value
- Funding status
- Expected term
- Desired start date
- Current pricing or incumbent spend
- One-time and recurring costs
- Growth assumptions

### Supplier Context
- Known or preferred suppliers
- Incumbent supplier
- Reason for supplier preference
- Existing contract or arrangement
- Market alternatives already considered
- Supplier dependency or lock-in concerns

### Risk and Compliance Context
- Personal, confidential, health, financial, or sensitive data
- Privacy and security requirements
- Data residency
- Accessibility
- Legal or regulatory obligations
- Business continuity
- Insurance
- Conflicts of interest

### Process Context
- Procurement stage
- Approval status
- Policy or trade-agreement considerations
- Required completion date
- Stakeholders and reviewers
- Existing documents

## Missing Information Rule
Ask only the questions needed to move the request forward.

If the request can still be assessed, proceed with assumptions and clearly label them.

Use:

```text
Assumptions:
- ...

Missing information:
- ...

Questions for the stakeholder:
- ...

Human decisions required:
- ...
```

## Workflow

### Step 1: Restate the Request
Summarize:

- What the stakeholder says they want
- The underlying business outcome
- The requested timeline
- Any preferred solution or supplier
- The current procurement stage

### Step 2: Separate the Need from the Proposed Solution
Identify:

- Business problem
- Required outcome
- Proposed product, supplier, or approach
- Assumptions connecting the solution to the need
- Whether alternatives appear to remain open

Use this table:

| Element | Stakeholder Statement | Procurement Interpretation | Validation Needed |
|---|---|---|---|

### Step 3: Identify Missing Information
Check for gaps in:

- Scope
- Deliverables
- Volumes
- Users
- Budget
- Funding
- Timeline
- Business owner
- Technical owner
- Contract status
- Usage data
- Market alternatives
- Privacy/security/accessibility
- Implementation and transition
- Evaluation expectations

### Step 4: Classify the Request
Classify the request by:

- New purchase, renewal, extension, amendment, replacement, or expansion
- Goods, services, software, SaaS, professional services, managed services, or hybrid
- Low, medium, high, or critical business impact
- Low, medium, or high commercial complexity
- Low, medium, or high supplier dependency
- Preliminary risk level

Do not present risk classifications as final if the underlying information is incomplete.

### Step 5: Review the Existing Contract or Arrangement
If an existing contract is involved, identify:

- Expiry date
- Renewal options
- Notice period
- Auto-renewal
- Remaining value
- Scope limitations
- Pricing and escalation
- Performance history
- Termination rights
- Transition support

Flag items requiring legal or contract-management review.

### Step 6: Run the Intake Risk Check
Review:

#### Commercial
- Missing budget
- Unclear pricing model
- Uncapped volumes
- Renewal increases
- Hidden implementation or support costs
- Unclear total cost of ownership

#### Competition and Fairness
- Preferred-supplier bias
- Solution specified before requirements
- Supplier-specific requirements
- Insufficient time for competition
- Unclear sole-source rationale

#### Operational
- Unrealistic timeline
- Unclear implementation ownership
- Integration dependency
- Business continuity
- Weak transition planning

#### Data, Privacy, Security, and Accessibility
- Sensitive data
- Data residency
- Cybersecurity review
- Accessibility requirements
- AI/data-use concerns

#### Supplier and Contract
- Incumbent lock-in
- No credible alternative
- Poor performance history
- Missing contract coverage
- Exit difficulty

### Step 7: Prepare Stakeholder Questions
Prioritize questions that materially affect strategy.

Use:

| Topic | Question | Why It Matters | Required Before Next Step? |
|---|---|---|---|

### Step 8: Present Possible Procurement Routes
Present options for human consideration, not final directions.

Possible routes may include:

- Market research
- RFI or market sounding
- Competitive RFx
- Second-stage process under an existing arrangement
- Renewal or extension review
- Negotiation with incumbent
- Contract amendment
- Further business-case development
- Risk, privacy, security, legal, or accessibility review

For each option, state:

- Why it may fit
- What information is still required
- Key risks
- Human approval needed

### Step 9: Route to Other Child Skills
Where appropriate, recommend use of:

- `spend-analysis-skill.md` for spend, usage, overlap, and renewal data
- `market-research-skill.md` for supplier and market options
- `pricing-model-review-skill.md` for pricing structure and future cost exposure
- `contract-risk-review-skill.md` for contract and renewal terms
- `rfp-drafting-skill.md` for supplier-facing documents
- `negotiation-prep-skill.md` for incumbent or renewal negotiation

### Step 10: Produce the Intake Decision Pack
Default output:

1. Intake summary
2. Need vs proposed solution
3. Missing information
4. Risk flags
5. Stakeholder questions
6. Possible procurement routes
7. Required reviewers
8. Recommended next actions for human approval

## Output Format

### Intake Summary
```text
The stakeholder is requesting [request] to achieve [outcome]. The main gaps are [gaps]. The preliminary risks are [risks]. Procurement should validate [items] before selecting a sourcing route.
```

### Risk Table
| Risk Area | Finding | Why It Matters | Recommended Validation | Reviewer |
|---|---|---|---|---|

### Route Options
| Possible Route | When It May Fit | Information Required | Main Risk | Human Approval |
|---|---|---|---|---|

## Review Checks
Before finalizing, confirm:

- The business need is separated from the proposed solution
- Missing information is clearly identified
- Supplier preference is not treated as strategy
- Urgency is challenged constructively
- Contract and renewal dates are considered
- Privacy, security, accessibility, legal, and finance reviews are flagged
- Possible routes are presented as options
- Final decisions remain with accountable humans

## Human Review
Humans must approve:

- Procurement strategy
- Competition or exemption decisions
- Supplier engagement
- Budget and funding
- Risk acceptance
- Final scope
- Contracting route
- Final timeline and approvals

## Guardrails
The AI must not:

- Approve the procurement request
- Choose the final sourcing route
- Validate sole-source justification as final
- Invent facts or requirements
- Assume a preferred supplier is qualified
- Ignore policy, fairness, or conflicts of interest
- Treat urgency as permission to bypass process
- Expose confidential information unnecessarily

## Example User Request
```text
Use procurement-intake-skill.md to review this request. Separate the business need from the proposed solution, identify missing information and risks, prepare stakeholder questions, and present possible next procurement steps for human decision.
```

## Success Criteria
This skill is working when it helps procurement:

- Challenge unclear requests early
- Reduce rework later
- Identify risk and reviewers before sourcing begins
- Separate business outcomes from supplier preferences
- Route the request to the right next workflow
- Preserve human accountability
