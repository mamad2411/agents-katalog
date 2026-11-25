---
name: pricing-model-review-skill
description: "Reviews pricing models for cost drivers, hidden fees, comparability, renewal exposure, TCO, and exit risk. Use for commercial envelopes and supplier pricing."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement Pricing Model Review Skill

## Purpose
This skill helps AI support procurement pricing model review through a structured, repeatable commercial analysis workflow.

Use this skill when a procurement professional needs to review a pricing table, commercial envelope, supplier pricing response, renewal pricing, SaaS pricing, licence model, implementation pricing, professional services rate card, or total cost of ownership structure.

This skill should not simply summarize pricing. It should help identify commercial risk, hidden cost drivers, unclear assumptions, pricing comparability issues, renewal exposure, implementation cost risk, optional cost risk, and exit or transition cost exposure.

This skill does not select the winning supplier, make an award recommendation, approve pricing, or replace procurement/commercial judgment.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
Pricing is not just a number.

It is a commercial structure.

A pricing table can look clean and still create risk if the model allows cost to grow later, makes suppliers difficult to compare, hides implementation effort, separates required services as optional, or weakens renewal and exit control.

The AI should follow this workflow:

**Extract -> Classify -> Test -> Compare -> Flag Risk -> Ask Questions -> Recommend Review Points**

The goal is to help procurement move from price checking to pricing-model review.

## When to Use
Use this skill when the user needs help with:

- Pricing model review
- Commercial envelope development
- RFP/RFB/RFQ pricing schedule review
- Supplier pricing response analysis
- SaaS pricing review
- Licence vs subscription comparison
- Implementation pricing review
- Professional services rate card review
- Renewal pricing review
- Optional services pricing review
- Total cost of ownership review
- Cost-driver identification
- Pricing clarification questions
- Pricing risk table creation
- Evaluation comparability review
- Commercial negotiation preparation

## Do Not Use This Skill For
Do not use this skill to:

- Choose the winning supplier
- Make final award recommendations
- Autonomously normalize or adjust supplier pricing without showing assumptions
- Invent missing pricing
- Create financial projections without clear assumptions
- Replace finance, legal, tax, or procurement approval
- Ignore procurement fairness or evaluation rules
- Treat the lowest price as automatically best value
- Change supplier-submitted pricing in an active evaluation

## Required Inputs
Before starting, identify which of the following inputs are available.

### Procurement Context
- What is being purchased?
- What procurement stage are we in?
- Is this pre-RFx, active RFx, evaluation support, negotiation, renewal, or contract management?
- Is the process public-sector, private-sector, or internal only?
- Is the pricing being reviewed for document design, supplier clarification, evaluation support, negotiation, or renewal planning?

### Pricing Documents
- Pricing table or commercial envelope
- Supplier pricing response, if available
- Pricing instructions
- Assumptions
- Evaluation formula or pricing evaluation method
- Contract term
- Renewal terms
- Optional years
- Pricing escalation language
- Rate cards
- Implementation pricing
- Support and maintenance pricing
- Optional modules or services
- Transition or exit pricing

### Volume and Usage Assumptions
- Number of users
- Number of licences
- Number of devices
- Number of sites
- Number of transactions
- Number of patient/client/customer records, if applicable
- Data/storage assumptions
- Support volumes
- Service hours
- Implementation phases
- Growth assumptions
- Contract term and renewal period

### Commercial Context
- Budget or affordability range
- Expected total contract value
- One-time vs recurring costs
- Fixed vs variable costs
- Capex vs opex treatment, if relevant
- Known incumbent pricing
- Known benchmark or market pricing
- Business criticality
- Need for scalability
- Need for flexibility
- Exit or transition expectations

### Output Need
- What should the final output be?
- Is the output for RFP design, supplier clarification, evaluation support, negotiation, manager briefing, or stakeholder review?
- Should the output be a table, memo, email, pricing risk log, commercial envelope, or review checklist?

## Missing Information Rule
If key pricing inputs are missing, do not invent them.

Proceed only with clearly stated assumptions and mark uncertain items.

Use this format:

```text
Assumptions I am using:
- ...

Pricing information missing:
- ...

Questions to confirm:
- ...

Items requiring human review:
- ...
```

If the missing information prevents meaningful review, ask the minimum required questions before proceeding.

## Workflow

### Step 1: Understand the Pricing Context
Restate the pricing review objective in plain language.

Identify:

- Product/service being priced
- Procurement stage
- Buyer context
- Contract term
- Pricing model type
- Evaluation or negotiation purpose
- Business-critical cost drivers
- Required output

### Step 2: Extract Pricing Components
Break the pricing into clear components.

Possible components include:

- Base subscription fees
- Licence fees
- Maintenance and support
- Implementation fees
- Configuration fees
- Integration fees
- Data migration fees
- Training fees
- Support tiers
- Professional services rates
- Managed services fees
- Hardware costs
- Hosting fees
- Storage fees
- Transaction fees
- User-based charges
- Device-based charges
- Module fees
- Optional services
- Renewal fees
- Price escalation
- Transition fees
- Exit fees

Use this table:

| Pricing Component | One-Time / Recurring | Fixed / Variable | Required / Optional | Cost Driver | Notes |
|---|---|---|---|---|---|

### Step 3: Classify the Pricing Model
Classify the pricing model.

Common models:

- Fixed fee
- Time and materials
- Licence plus maintenance
- Subscription
- Per-user
- Per-seat
- Per-device
- Per-transaction
- Usage-based
- Tiered pricing
- Module-based pricing
- Outcome-based pricing
- Hybrid pricing
- Rate card pricing
- Cost-plus
- Milestone-based implementation pricing

Explain how the model works and where cost growth may occur.

### Step 4: Identify Cost Drivers
Identify what causes price to increase.

Examples:

- Number of users
- Number of licences
- Number of devices
- Number of locations
- Number of transactions
- Data volume
- Storage volume
- Support hours
- Service level tier
- Implementation complexity
- Number of integrations
- Number of environments
- Number of modules
- Number of reports
- Number of business units
- Volume growth
- Renewal escalation
- Professional services hours

Use this table:

| Cost Driver | Pricing Impact | Risk Level | Why It Matters | Validation Needed |
|---|---|---|---|---|

### Step 5: Separate One-Time, Recurring, Optional, and Future Costs
Separate the cost structure.

Check for:

- One-time implementation cost
- Recurring subscription/licence cost
- Annual maintenance and support
- Optional modules
- Optional professional services
- Renewal costs
- Extension-year pricing
- Cost escalation
- Exit or transition support
- Post-award change order exposure

Use this table:

| Cost Type | Included? | Clearly Priced? | Risk / Unknown | Recommended Action |
|---|---|---|---|---|

### Step 6: Test Pricing Growth Scenarios
Where useful, test simple growth scenarios.

Examples:

- What happens if users increase by 25%?
- What happens if volumes double?
- What happens if implementation takes longer?
- What happens if optional modules become required?
- What happens if support needs increase?
- What happens during renewal years?
- What happens if the buyer exits or transitions?

Do not create exact projections unless the inputs are available.

If inputs are incomplete, describe the scenario qualitatively.

Use this table:

| Scenario | Likely Pricing Impact | Risk | Questions to Ask |
|---|---|---|---|

### Step 7: Check Comparability
Assess whether supplier pricing can be compared fairly.

Check:

- Are suppliers pricing the same scope?
- Are assumptions standardized?
- Are volumes defined?
- Are optional items separated?
- Are required costs included in evaluated price?
- Are implementation and recurring costs treated consistently?
- Are professional services assumptions consistent?
- Are renewal prices included?
- Are pricing forms clear enough to avoid inconsistent responses?
- Are exclusions allowed, and if so, how are they evaluated?

For public procurement, flag any issue that could create evaluation ambiguity, unequal treatment, or audit defensibility concerns.

### Step 8: Identify Pricing Risks
Review the pricing model using the following risk lenses.

#### Commercial Risk
- Uncapped cost growth
- Hidden fees
- Required services listed as optional
- Weak renewal price protection
- Unclear escalation
- Cost shifting to professional services
- Unclear support costs
- Implementation assumptions not priced
- No cap on travel or expenses
- No clear transition or exit pricing

#### Evaluation Risk
- Suppliers may interpret pricing instructions differently
- Evaluated price may not reflect true total cost
- Optional items may distort comparison
- Pricing forms may not capture all required costs
- Suppliers may load costs into non-evaluated areas
- Different pricing models may be difficult to compare

#### Operational Risk
- Underpriced implementation
- Poorly scoped support
- Unclear service hours
- Pricing not aligned to expected usage
- Business growth not reflected
- Change order exposure

#### Renewal and Exit Risk
- No extension-year pricing
- No price escalation cap
- No renewal benchmark
- Auto-renewal risk
- Exit support not priced
- Data migration or transition fees unclear
- Supplier lock-in through pricing structure

### Step 9: Prepare Supplier Clarification Questions
Generate questions that procurement or the sourcing team can ask before finalizing the pricing model or during clarification.

Use this table:

| Topic | Clarification Question | Why This Matters |
|---|---|---|

Examples:

- Are implementation services included in the base price?
- What assumptions are included in implementation pricing?
- Are all mandatory requirements priced in the evaluated total?
- What costs are excluded?
- What triggers additional fees?
- How are renewal prices calculated?
- Are optional modules required for full functionality?
- Are professional services hours capped?
- Are travel and expenses included or additional?
- What transition or exit costs may apply?
- How does pricing change if users, sites, transactions, or volumes increase?

### Step 10: Prepare Recommended Pricing Improvements
If reviewing a draft pricing schedule or commercial envelope, recommend improvements.

Possible recommendations:

- Separate one-time and recurring costs
- Require all mandatory costs to be included in evaluated pricing
- Create separate optional pricing schedule
- Include renewal-year pricing
- Add volume bands
- Add implementation milestone pricing
- Add professional services rate card
- Cap travel and expenses or require pre-approval
- Require suppliers to state assumptions
- Require suppliers to state exclusions
- Require transition and exit pricing
- Add pricing scenario fields for evaluation
- Require support and maintenance pricing clarity

### Step 11: Identify Human Review Items
Flag where human review is required.

Examples:

- Procurement review of pricing evaluation approach
- Finance review of affordability and budget impacts
- Business-owner validation of usage assumptions
- Legal review of escalation, renewal, and price adjustment clauses
- Evaluation team review of comparability
- Executive/stakeholder review of commercial risk
- Supplier clarification before relying on assumptions

## Output Format

### Short Summary
Start with a plain-language commercial summary.

```text
Summary:
The pricing model appears to be [model type]. The main cost drivers are [drivers]. The key risks are [risks]. The pricing can/cannot be compared easily because [reason]. Human review is needed for [items].
```

### Pricing Component Table
Use this table:

| Component | Cost Type | Fixed / Variable | Required / Optional | Cost Driver | Risk / Comment |
|---|---|---|---|---|---|

### Cost Driver Table
Use this table:

| Cost Driver | What Triggers Cost Growth | Risk Level | Why It Matters | Validation Needed |
|---|---|---|---|---|

### Pricing Risk Table
Use this table:

| Risk Area | Finding | Why It Matters | Recommended Action | Human Review Needed |
|---|---|---|---|---|

### Scenario Table
Use this table when useful:

| Scenario | Expected Cost Impact | Risk | Clarification Needed |
|---|---|---|---|

### Supplier Clarification Questions
Use this table:

| Topic | Question | Why This Matters |
|---|---|---|

### Human Review Items
List the items procurement, finance, legal, business owners, or evaluation teams should review.

## Review Checks
Before finalizing, check:

- Did the analysis separate one-time and recurring costs?
- Did it identify fixed and variable costs?
- Did it identify required vs optional costs?
- Did it identify hidden or excluded costs?
- Did it identify renewal and escalation risks?
- Did it identify transition or exit costs?
- Did it check if suppliers can be compared fairly?
- Did it show assumptions clearly?
- Did it avoid inventing missing pricing?
- Did it avoid making supplier selection or award recommendations?
- Did it flag human review items?

## Human Review
Humans must review and approve:

- Pricing evaluation model
- Supplier clarification questions
- Pricing normalization assumptions
- Scenario assumptions
- Total cost of ownership assumptions
- Final negotiation position
- Commercial risk acceptance
- Award recommendation
- Contract pricing terms
- Renewal and escalation clauses
- Exit or transition pricing

## Guardrails
The AI must not:

- Pick the cheapest supplier as the winner
- Make award recommendations
- Invent missing pricing
- Hide assumptions
- Normalize supplier prices without explaining the method
- Treat optional costs as irrelevant without checking whether they may become required
- Ignore renewal pricing
- Ignore transition or exit costs
- Ignore implementation assumptions
- Ignore evaluation fairness
- Change supplier-submitted pricing in an active procurement evaluation
- Provide final legal, finance, or tax advice

## Example User Request
```text
Use the pricing-model-review-skill.md workflow to review this pricing table. Identify fixed and variable costs, one-time and recurring fees, optional charges, hidden cost exposure, renewal risk, supplier clarification questions, and human review items.
```

## Example Output Instruction
```text
Do not simply summarize the pricing table. Review the pricing model as a procurement commercial advisor. Identify cost drivers, comparability issues, TCO risks, renewal and exit exposure, and questions we should ask before finalizing the pricing schedule or evaluating the supplier response.
```

## Success Criteria
This skill is working when it helps the user:

- Move from price checking to pricing-model review
- Identify hidden or future cost exposure
- Improve pricing schedule design
- Create better supplier clarification questions
- Improve evaluation comparability
- Support negotiation preparation
- Review total cost of ownership more clearly
- Keep final commercial decisions with accountable humans
