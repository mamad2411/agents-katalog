---
name: contract-risk-review-skill
description: "Maps procurement and commercial risks in contract terms and flags legal escalation points. Use for first-pass contract review, renewals, and negotiations."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement Contract Risk Review Skill

## Purpose
This skill helps AI perform a first-pass procurement and commercial risk review of a contract, master agreement, SOW, amendment, renewal, supplier terms, or clause set.

It identifies what a clause says, the possible business and commercial impact, questions to clarify, possible procurement positions, and issues that require legal or specialist review.

This skill does not provide final legal advice, approve contract language, or replace legal counsel.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
Legal wording and commercial impact are related but not identical.

The workflow is:

**Extract -> Classify -> Interpret Operationally -> Assess Commercial Impact -> Prioritize -> Prepare Position -> Escalate**

## When to Use
Use this skill for:

- Contract and clause review
- Supplier paper review
- Master agreement or SOW review
- Renewal and amendment review
- SaaS and software agreements
- Professional and managed services contracts
- Contract negotiation preparation
- Commercial-risk summaries
- Legal escalation preparation
- Contract comparison against an approved position

## Do Not Use This Skill For
Do not use it to:

- Give final legal advice
- Approve or sign a contract
- Replace counsel
- State that a clause is enforceable in a jurisdiction without qualified review
- Rewrite approved legal language as final
- Treat every deviation as equally serious
- Ignore deal value, business criticality, or risk context

## Required Inputs
- Contract or clauses
- Transaction type and value
- Scope and deliverables
- Contract term and renewal structure
- Data and security context
- Business criticality
- Supplier role and dependency
- Approved template or fallback position, if available
- Known negotiation priorities
- Required output and audience

## Workflow

### Step 1: Establish Deal Context
Identify:

- What is being purchased
- Contract value and term
- Supplier criticality
- Data sensitivity
- Implementation and transition complexity
- Incumbent or lock-in risk
- Procurement stage

### Step 2: Extract and Classify Clauses
Classify clauses under:

- Fees and payment
- Price escalation and renewal
- Scope and change control
- Service levels and remedies
- Warranties
- Liability
- Indemnities
- Insurance
- Confidentiality
- Privacy and data protection
- Security and incidents
- Intellectual property and licences
- Audit and records
- Subcontracting
- Compliance
- Termination
- Transition and exit
- Dispute resolution
- Governing law
- Force majeure and business continuity

### Step 3: Summarize the Clause in Plain Language
For each material clause, state:

- What the supplier must do
- What the buyer must do
- What happens if either party fails
- What is missing or unclear

Do not overstate legal meaning.

### Step 4: Assess Commercial and Operational Impact
Check:

- Cost exposure
- Uncapped or poorly controlled increases
- Service-performance exposure
- Supplier dependency
- Implementation and change-order risk
- Data and security exposure
- Weak remedies
- Renewal or auto-renewal exposure
- Termination difficulty
- Transition and exit cost
- Auditability

### Step 5: Prioritize Risk
Use:

- Critical
- High
- Medium
- Low
- Needs specialist review

Explain the basis and avoid false precision.

### Step 6: Prepare Procurement Position
For each issue, provide:

- Preferred commercial outcome
- Clarification question
- Possible fallback concept
- Trade-off or consequence
- Required approval

Do not present draft legal wording as final unless the user specifically asks for proposed language, and clearly mark it for legal review.

### Step 7: Route Specialist Issues
Flag:

- Legal
- Privacy
- Cybersecurity
- Accessibility
- Finance/tax
- Insurance
- Records management
- Technical architecture
- Business continuity

### Step 8: Prepare Negotiation Inputs
Where relevant, route findings to `negotiation-prep-skill.md`.

## Output Format

### Contract Risk Table
| Clause / Topic | Plain-Language Effect | Risk | Business Impact | Procurement Position | Specialist Review |
|---|---|---|---|---|---|

### Negotiation Issue Table
| Priority | Ask | Rationale | Possible Fallback | Approval Needed |
|---|---|---|---|---|

### Executive Summary
```text
The highest-risk issues are [issues]. They may affect [cost/performance/data/exit]. Procurement should prioritize [actions] and obtain specialist review for [items].
```

## Review Checks
- Deal context is considered
- Commercial and legal issues are separated
- Risk is prioritized
- Renewal and exit are reviewed
- Data/security issues are escalated
- Assumptions are visible
- Final approval remains with humans

## Human Review
Humans must approve:

- Legal interpretation
- Final redlines
- Risk acceptance
- Liability and indemnity positions
- Privacy and security terms
- Final commercial position
- Contract signature

## Guardrails
The AI must not:

- Provide final legal advice
- Approve clauses
- State enforceability as fact without qualified review
- Ignore jurisdiction or context
- Invent missing clauses
- Treat all risks as equal
- Recommend unethical or unfair tactics
- Expose confidential terms unnecessarily

## Example User Request
```text
Use contract-risk-review-skill.md to review this agreement from a procurement and commercial perspective. Identify material risks, business impacts, negotiation points, specialist escalations, and human decisions.
```

## Success Criteria
This skill is working when it helps procurement:

- Understand contract impact in plain language
- Escalate legal and specialist issues clearly
- Prioritize negotiation effort
- Protect pricing, performance, data, renewal, and exit outcomes
- Enter legal review better prepared
