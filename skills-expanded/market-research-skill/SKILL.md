---
name: market-research-skill
description: "Runs structured supplier and market research, capability comparison, pricing observations, and risk checks. Use for market scans, longlists, and sourcing research."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement Market Research Skill

## Purpose
This skill helps AI support procurement market research through a structured, repeatable workflow.

Use this skill when a procurement professional needs to understand a supplier market, identify potential suppliers, compare capabilities, flag market and supplier risks, and prepare a human-reviewable market research output.

This skill should not produce a random vendor list. It should organize supplier and market research in a way that supports procurement judgment, sourcing strategy, and defensible decision preparation.

This skill does not qualify suppliers, make shortlist decisions, recommend awards, or replace procurement review.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
Market research is not a one-shot search.

It is a loop:

**Define -> Search -> Read -> Compare -> Gap Check -> Search Again -> Validate -> Summarize**

The goal is to help procurement move from fragmented internet searching to structured supplier intelligence.

## When to Use
Use this skill when the user needs help with:

- Supplier market research
- Vendor longlist development
- Market scan preparation
- Supplier capability comparison
- Category research
- Sourcing strategy input
- New supplier discovery
- Existing supplier landscape review
- Public-sector or private-sector sourcing preparation
- RFI or RFP planning
- Competitive landscape review
- Market risk identification
- Pricing model research
- Supplier ecosystem mapping
- Incumbent alternative research

## Do Not Use This Skill For
Do not use this skill to:

- Make final supplier selection decisions
- Confirm that a supplier is qualified without evidence
- Score suppliers in an active procurement evaluation
- Replace formal due diligence
- Replace legal, privacy, security, accessibility, or financial review
- Produce supplier claims without validation
- Recommend a procurement award
- Communicate directly with suppliers without human approval

## Required Inputs
Before starting, identify which of the following inputs are available.

### Business Need
- What is the organization trying to buy or solve?
- What outcome does the business need?
- Who are the end users or stakeholders?
- Is the need new, replacement, renewal, expansion, or transformation-related?

### Category and Scope
- What category, product, service, or solution is being researched?
- What is in scope?
- What is out of scope?
- Is the requirement for goods, services, software, SaaS, professional services, managed services, or a hybrid model?
- Are there subcategories or streams?

### Geography and Buyer Context
- What geography applies?
- Is the buyer public sector, healthcare, education, municipal, enterprise, or private sector?
- Are there local presence, data residency, accessibility, security, or regulatory expectations?

### Capability Requirements
- What are the must-have capabilities?
- What are the nice-to-have capabilities?
- What integrations, implementation services, support services, reporting, training, or transition services may be required?
- Are there technical, operational, privacy, security, or compliance requirements?

### Commercial Context
- Is there an estimated budget or spend range?
- What term or contract duration is expected?
- Are common pricing models known?
- Are volumes, users, transactions, licences, locations, devices, modules, or service levels known?

### Existing Market Knowledge
- Are there known suppliers?
- Is there an incumbent?
- Are there suppliers to exclude?
- Are there preferred contract vehicles or existing agreements?
- Are there previous procurements, RFx documents, vendor lists, or internal notes?

### Output Need
- What should the final output look like?
- Is this for internal procurement planning, stakeholder discussion, executive briefing, sourcing strategy, RFx drafting, or supplier outreach planning?

## Missing Information Rule
If key context is missing, do not stop unless the missing information prevents meaningful work.

Proceed with assumptions and flag open questions.

Use this format:

```text
Assumptions I am using:
- ...

Open questions:
- ...

Items requiring human confirmation:
- ...
```

Ask only the minimum questions needed to continue.

## Workflow

### Step 1: Understand the Research Objective
Restate the market research objective in plain language.

Identify:

- Category
- Business need
- Buyer type
- Geography
- Key capabilities
- Risk level
- Expected output
- Any known constraints

### Step 2: Define the Market Boundary
Clarify the market before identifying suppliers.

Determine:

- What supplier types may exist
- Whether the market includes OEMs, resellers, integrators, SaaS providers, consultants, managed service providers, distributors, niche specialists, or platform providers
- Whether the category has regional, national, or global players
- Whether public-sector buying may require special supplier experience
- Whether the market is mature, fragmented, emerging, specialized, or highly concentrated

Output a short market boundary statement.

Example:

```text
Market boundary:
This research focuses on Canadian suppliers and platform providers that can deliver [category/service] to [buyer type], including implementation, support, and ongoing service management. Pure advisory firms and suppliers without evidence of relevant capability are excluded unless they are part of the implementation ecosystem.
```

### Step 3: Build Search Strategy
Create a search plan before searching.

Include:

- Search themes
- Supplier-type searches
- Capability-specific searches
- Geography-specific searches
- Public-sector or industry-specific searches
- Pricing model searches
- Risk and implementation searches

Example search themes:

- Category overview
- Supplier ecosystem
- Public-sector suppliers
- Capability-specific providers
- Implementation partners
- Pricing models
- Market risks
- Case studies or client examples

### Step 4: Identify Supplier Types
Before naming suppliers, classify the supplier ecosystem.

Possible supplier types:

- Product vendors
- SaaS providers
- OEMs
- Resellers
- Value-added resellers
- System integrators
- Managed service providers
- Professional services firms
- Implementation partners
- Niche specialists
- Marketplace providers
- Regional providers
- Incumbent alternatives

For each supplier type, explain why it may or may not be relevant.

### Step 5: Build the Initial Longlist
Create an initial supplier longlist using available evidence.

For each supplier, capture:

- Supplier name
- Supplier type
- Website or source
- Geography served
- Relevant capabilities
- Evidence found
- Potential fit
- Validation needed

Do not include a supplier only because the name sounds relevant. Include the reason it may fit.

### Step 6: Verify Capabilities
For each supplier, verify claims against the required capabilities.

Use this structure:

| Supplier | Supplier Type | Evidence of Capability | Relevant Capabilities | Gaps / Unknowns | Validation Needed |
|---|---|---|---|---|---|

Check whether the supplier has evidence of:

- Relevant product or service
- Similar client type
- Similar geography
- Implementation capability
- Support capability
- Security/privacy/compliance posture, if relevant
- Public-sector, healthcare, education, or enterprise experience, if relevant
- Partner ecosystem, if relevant

Do not treat vendor marketing language as proof. Mark it as a claim unless independently supported.

### Step 7: Compare Suppliers Against Must-Have Needs
Create a capability matrix.

Use simple indicators:

- Yes
- Partial
- No
- Unknown
- Needs validation

Example:

| Capability | Supplier A | Supplier B | Supplier C | Notes |
|---|---|---|---|---|
| Core solution capability | Yes | Yes | Partial | Supplier C appears to require partner support |
| Implementation services | Yes | Unknown | Yes | Validate during RFI |
| Canadian public-sector experience | Partial | Yes | Unknown | Evidence varies |
| Data residency support | Unknown | Yes | Unknown | Requires supplier confirmation |

### Step 8: Research Pricing Models
Identify common pricing structures in the market.

Check for:

- Subscription pricing
- Licence plus maintenance and support
- Per-user pricing
- Per-seat pricing
- Per-device pricing
- Per-transaction pricing
- Tiered pricing
- Usage-based pricing
- Implementation fees
- Professional services rates
- Support tiers
- Optional modules
- Renewal escalation
- Exit or transition fees

Output:

- Common pricing models
- Cost drivers
- Pricing risks
- Questions to include in future RFx or supplier clarification

### Step 9: Identify Market and Supplier Risks
Run a procurement risk check.

#### Market Risks
- Limited competition
- Market concentration
- Immature supplier market
- Rapidly changing technology
- Limited local availability
- Supplier lock-in
- Proprietary ecosystem dependency
- Reseller/channel complexity

#### Commercial Risks
- Unclear pricing model
- Usage-based cost growth
- Optional modules becoming necessary later
- Implementation costs not visible upfront
- Renewal escalation risk
- Support costs separated from subscription or licence fees
- Exit costs not transparent

#### Operational Risks
- Implementation complexity
- Integration dependency
- Training burden
- Weak support model
- Unclear service levels
- Transition risk
- Business continuity risk

#### Data, Privacy, Security, and Compliance Risks
- Personal or sensitive data handling
- Data residency concerns
- Cybersecurity posture unknown
- Accessibility requirements unknown
- AI/data-use restrictions unclear
- Subcontractor or fourth-party risk

#### Supplier Risks
- New or unproven supplier
- Limited referenceability
- Financial stability unknown
- Heavy reliance on partners
- Capacity constraints
- Incumbent advantage
- Vendor lock-in

### Step 10: Run the Research Loop
After the first pass, loop back.

Ask:

- Did we find enough suppliers?
- Are there missing supplier types?
- Are all must-have capabilities covered?
- Are we relying too much on vendor marketing?
- Are there public-sector or industry-specific suppliers missing?
- Are there regional suppliers missing?
- Are pricing models clear enough?
- Are there contradictions or weak claims?
- What should be searched again?

If gaps remain, refine the search and update the findings.

### Step 11: Prepare the Market Research Output
Produce a procurement-ready output.

Default structure:

1. Research objective
2. Assumptions and scope
3. Market overview
4. Supplier ecosystem
5. Supplier longlist
6. Capability matrix
7. Pricing model observations
8. Market and supplier risks
9. Suggested RFx questions
10. Human review items
11. Open questions
12. Sources or evidence notes, where applicable

## Output Format

### Short Summary
Provide a short executive-style summary.

```text
Summary:
Based on the available information, the market appears to include [supplier types]. The strongest potential fit appears to be suppliers with [capabilities]. The main risks to validate are [risks]. Further human validation is required before any sourcing or shortlist decision.
```

### Supplier Longlist Table
Use this table:

| Supplier | Supplier Type | Relevant Capability | Evidence / Source Note | Potential Fit | Gaps / Validation Needed |
|---|---|---|---|---|---|

### Capability Matrix
Use this table:

| Requirement / Capability | Supplier 1 | Supplier 2 | Supplier 3 | Notes |
|---|---|---|---|---|

Use:

- Yes
- Partial
- No
- Unknown
- Needs validation

### Risk Table
Use this table:

| Risk Area | Finding | Why It Matters | Recommended Action | Human Review Needed |
|---|---|---|---|---|

### RFx / Supplier Clarification Questions
Use this table:

| Topic | Question | Why This Matters |
|---|---|---|

### Human Review Items
List items procurement should validate before relying on the research.

Examples:

- Confirm supplier eligibility
- Validate supplier capabilities through RFI/RFP
- Confirm pricing model directly with supplier
- Validate privacy/security/data residency requirements
- Check contract vehicle availability
- Review conflicts of interest or incumbent considerations
- Confirm stakeholder must-have requirements

## Review Checks
Before finalizing, check:

- Is the market boundary clear?
- Are supplier types identified before supplier names?
- Are supplier capabilities supported by evidence?
- Are assumptions clearly marked?
- Are unknowns clearly marked?
- Are pricing models separated from supplier capability?
- Are risks clearly stated?
- Are supplier claims treated as claims, not facts?
- Is the output useful for procurement planning?
- Are final decisions reserved for humans?

## Human Review
Humans must review and approve:

- Final supplier inclusion or exclusion
- Supplier qualification decisions
- RFx strategy
- Shortlist decisions
- Supplier communication
- Use of market research in formal procurement documents
- Privacy, security, legal, accessibility, and policy implications
- Any commercially sensitive or confidential information

## Guardrails
The AI must not:

- Invent suppliers
- Invent supplier capabilities
- Assume a supplier is qualified
- Make supplier selection decisions
- Recommend an award
- Treat marketing claims as verified facts
- Ignore missing evidence
- Ignore local policy, public-sector fairness, or trade agreement considerations
- Contact suppliers
- Use confidential information unnecessarily
- Present research as final due diligence

## Example User Request
```text
Create a market research summary for [category] in [geography]. I need a supplier longlist, supplier types, capability matrix, pricing model observations, market risks, and questions I should ask stakeholders before drafting the RFx.
```

## Example Output Instruction
```text
Use the market-research-skill.md workflow. Do not provide a random vendor list. First define the market boundary and supplier types. Then create a supplier longlist, capability matrix, pricing model observations, risk table, RFx questions, and human review items. Clearly mark assumptions and unknowns.
```

## Success Criteria
This skill is working when it helps the user:

- Move from generic supplier searching to structured market intelligence
- Build a useful supplier longlist
- Compare suppliers against relevant procurement needs
- Identify pricing, market, supplier, and implementation risks earlier
- Prepare better stakeholder questions
- Support sourcing strategy without replacing procurement judgment
- Reuse and improve the workflow across multiple categories
