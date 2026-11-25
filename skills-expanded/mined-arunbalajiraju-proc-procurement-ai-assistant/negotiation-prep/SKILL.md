---
name: negotiation-prep-skill
description: "Builds supplier negotiation briefs with asks, leverage, concessions, pushback, fallbacks, and approvals. Use before pricing, renewal, or contract negotiations."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement Negotiation Preparation Skill

## Purpose
This skill helps AI build a structured negotiation brief from supplier proposals, pricing, performance, contract risks, alternatives, stakeholder priorities, and approval limits.

It supports preparation. It does not negotiate autonomously or make final trade-off decisions.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
Good negotiation starts before the meeting.

The workflow is:

**Define Objectives -> Gather Evidence -> Map Leverage -> Prioritize Asks -> Design Trades -> Anticipate Pushback -> Set Fallbacks -> Obtain Approval**

## When to Use
Use this skill for:

- Renewal negotiations
- Supplier price increases
- New-contract negotiations
- Contract-risk negotiations
- SLA and service-credit negotiations
- Implementation and transition negotiations
- Professional-services rates
- Volume and licence negotiations
- Supplier performance remediation discussions

## Do Not Use This Skill For
Do not use it to:

- Invent leverage or alternatives
- Recommend deception, coercion, collusion, or unethical tactics
- Make unauthorized commitments
- Ignore public procurement fairness or communication controls
- Decide final concessions
- Contact suppliers without approval

## Required Inputs
- Supplier proposal
- Current and historical pricing
- Contract and renewal terms
- Performance data
- Business priorities
- Must-haves and preferences
- Alternatives and switching cost
- Market evidence
- Supplier dependencies
- Internal approval limits
- Timing and stakeholders

## Workflow

### Step 1: Define the Negotiation Objective
Identify:

- Desired outcome
- Minimum acceptable outcome
- Non-negotiables
- Preferences
- Risks to protect
- Timeline

### Step 2: Build the Fact Base
Review:

- Pricing and cost drivers
- Historical increases
- Usage and demand
- SLA performance
- Open issues
- Contract terms
- Market alternatives
- Switching cost
- Supplier investment and dependency

Distinguish evidence from assumptions.

### Step 3: Map Buyer and Supplier Leverage
Possible buyer leverage:

- Credible alternatives
- Volume or growth
- Consolidation opportunity
- Contract timing
- Poor supplier performance
- Competitive benchmark
- Reference value
- Faster decision or longer commitment, if approved

Possible supplier leverage:

- High switching cost
- Proprietary technology
- Urgent timeline
- Limited alternatives
- Critical dependency
- Data migration difficulty
- Strong performance

Use:

| Leverage Point | Party | Evidence | Strength | Risk of Using It |
|---|---|---|---|---|

### Step 4: Prioritize Asks
Classify:

- Must achieve
- High priority
- Tradeable
- Nice to have
- Do not concede without approval

Asks may include:

- Price reduction or phased increase
- Price hold or escalation cap
- Volume bands
- Licence optimization
- Implementation commitments
- Included professional services
- SLA remedies
- Reporting
- Transition support
- Data return/deletion
- Payment terms
- Renewal flexibility

### Step 5: Design Concessions and Trades
For each possible concession, state:

- What the buyer gives
- What the buyer receives
- Cost/risk to buyer
- Approval required
- Whether the trade is reversible

Never recommend giving a concession without a reciprocal outcome.

### Step 6: Anticipate Supplier Pushback
Prepare likely arguments and evidence-based responses.

| Supplier Pushback | Likely Basis | Buyer Response | Evidence Needed | Escalation |
|---|---|---|---|---|

### Step 7: Set Fallback Positions
Define:

- Preferred position
- Target position
- Acceptable fallback
- Walk-away or escalation point
- Items that cannot be agreed in the room

### Step 8: Prepare Meeting Plan
Include:

- Participants and roles
- Opening position
- Order of issues
- Questions
- Planned pauses or internal caucus points
- Approval limits
- Notes and action tracking

### Step 9: Run a Red-Team Review
Ask:

- Is the leverage credible?
- Are assumptions unsupported?
- What will the supplier challenge?
- What is the cost of delay?
- What is the cost of switching?
- Are we trading away a critical control?
- Are approvals clear?

## Output Format

### Negotiation Brief
1. Objective
2. Fact base
3. Buyer and supplier leverage
4. Prioritized asks
5. Concession plan
6. Pushback responses
7. Fallback positions
8. Approval items
9. Meeting plan

### Ask and Concession Table
| Priority | Ask | Rationale | Evidence | Possible Trade | Approval |
|---|---|---|---|---|---|

### Fallback Table
| Issue | Preferred | Target | Fallback | Escalation / Walk-Away |
|---|---|---|---|---|

## Review Checks
- Leverage is supported by evidence
- Must-haves are separated from preferences
- Every concession has a return
- Approval limits are visible
- Supplier pushback is considered
- Public procurement communication controls are respected
- Humans own final decisions

## Human Review
Humans must approve:

- Negotiation mandate
- Concessions
- Final fallback positions
- Walk-away points
- Supplier communications
- Legal and policy deviations
- Final agreement

## Guardrails
The AI must not:

- Invent leverage
- Recommend deception or unethical tactics
- Make commitments
- Ignore approval limits
- Advise collusion or anti-competitive conduct
- Bypass procurement communication controls
- Make final trade-offs

## Example User Request
```text
Use negotiation-prep-skill.md to build a negotiation brief from this proposal, pricing, contract, performance data, alternatives, priorities, and approval limits.
```

## Success Criteria
This skill is working when it helps procurement:

- Enter negotiations with a clear fact base
- Protect priority outcomes
- Prepare reciprocal trades
- Anticipate supplier arguments
- Clarify approvals and fallback positions
- Avoid invented leverage and unmanaged concessions
