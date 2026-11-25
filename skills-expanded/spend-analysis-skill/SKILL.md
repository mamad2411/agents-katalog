---
name: spend-analysis-skill
description: "Cleans and analyzes spend data to find supplier concentration, overlaps, anomalies, contract gaps, renewal risks, and validated sourcing opportunities."
license: MIT
compatibility: "Agent Skills compatible; no external dependencies. Human review required for procurement decisions."
metadata:
  author: Arun Balaji Raju
  version: "0.2.0"
  project: procurement-ai-assistant
---

## Skill Name
Procurement Spend Analysis Skill

## Purpose
This skill helps AI support procurement spend analysis through a structured, repeatable workflow.

Use this skill when a procurement professional needs to clean, classify, group, compare, and challenge spend data to identify patterns, anomalies, contract gaps, renewal risks, supplier concentration, overlapping products or services, and potential sourcing opportunities.

This skill should not simply summarize totals. It should help procurement understand where spend is going, what may require investigation, and where a human should validate a potential opportunity.

This skill does not automatically classify every overlap as waste, calculate final savings without evidence, recommend supplier termination, or replace procurement, finance, business-owner, legal, security, or technical review.

## Composability
This skill is standalone. If other Procurement AI Assistant skills are installed, the AI may combine relevant skills for a multi-step procurement request. Do not assume another skill is available; preserve this skill's own guardrails and human review points.

## Core Principle
Spend analysis is not only about totals.

It is about finding patterns that deserve procurement attention.

The AI should follow this workflow:

**Inspect -> Clean -> Normalize -> Classify -> Group -> Compare -> Challenge -> Validate -> Prioritize**

The goal is to move from a raw spend file to a procurement-ready opportunity and risk view.

## When to Use
Use this skill when the user needs help with:

- Spend data cleaning
- Supplier normalization
- Category classification
- Spend cube preparation
- Tail-spend analysis
- Supplier concentration analysis
- Duplicate or overlapping supplier review
- SaaS and software spend analysis
- Licence and usage review
- Contract coverage analysis
- Renewal pipeline review
- Maverick or off-contract spend review
- Invoice and purchase-order anomaly detection
- Category opportunity identification
- Supplier consolidation analysis
- Savings-opportunity preparation
- Executive spend summaries
- Procurement pipeline development

## Do Not Use This Skill For
Do not use this skill to:

- Treat every overlapping product or supplier as waste
- State final savings without validated baselines and assumptions
- Recommend cancelling a supplier or contract automatically
- Make sourcing or award decisions
- Invent categories, contract dates, owners, or savings values
- Change source data without preserving an audit trail
- Ignore tax, currency, accounting-period, or unit-of-measure differences
- Replace finance reconciliation
- Replace legal, security, technical, privacy, or business-owner review
- Expose confidential financial or supplier information unnecessarily

## Required Inputs

### Core Spend Data
- Supplier name and identifier
- Invoice or purchase-order description
- Amount and currency
- Transaction date and fiscal period
- Cost centre and general ledger code
- Business unit and category
- Requestor or business owner
- Contract, purchase-order, and invoice numbers

### Contract and Supplier Data
- Contract start, end, renewal, and notice dates
- Auto-renewal terms
- Contract value and committed spend
- Pricing model
- Supplier parent company
- Preferred or approved supplier status
- Contract owner
- Supplier risk rating

### Usage and Demand Data
- Users or licences purchased
- Assigned and active users
- Utilization
- Devices, sites, or transaction volumes
- Consumption levels
- Product modules
- Storage or data usage
- Business criticality

### Analysis Context
- Date range
- Geography and business units
- Currency and tax treatment
- Materiality threshold
- Category taxonomy
- Known exclusions
- Objective of the analysis

### Output Need
- Category plan
- Renewal review
- Sourcing pipeline
- Budget discussion
- Executive briefing
- Negotiation preparation
- Contract management

## Missing Information Rule
If critical data is missing, do not invent it.

Proceed with clearly stated assumptions and distinguish between confirmed findings and hypotheses.

Use this format:

```text
Assumptions I am using:
- ...

Data limitations:
- ...

Validation questions:
- ...

Items requiring human review:
- ...
```

Where missing data materially affects the analysis, state what cannot be concluded.

## Workflow

### Step 1: Confirm the Analysis Objective
Restate the objective in plain language.

Identify:

- Period covered
- Business units and geography
- Categories
- Materiality threshold
- Desired output
- Intended audience
- Focus: savings, risk, renewals, compliance, concentration, or data quality

### Step 2: Inspect the Data
Review the dataset before analysis.

Check:

- Column names and data types
- Missing values
- Duplicate rows
- Negative amounts
- Credits and reversals
- Currency differences
- Tax-inclusive vs tax-exclusive values
- Date consistency
- Supplier-name quality
- Category completeness
- Contract coverage
- Owner completeness

Produce a data-quality summary before making procurement conclusions.

### Step 3: Preserve the Source Data
Do not overwrite the original data.

Create separate fields for:

- Normalized supplier name
- Normalized parent supplier
- Proposed category and subcategory
- Contract status
- Renewal risk
- Opportunity type
- Confidence level
- Validation status
- Analyst notes

All transformations should be traceable.

### Step 4: Normalize Supplier Names
Identify suppliers that may appear under multiple names.

Examples:

- Legal entity vs trading name
- Parent vs subsidiary
- Abbreviations
- Punctuation differences
- Spelling variations
- Regional entities
- Marketplace or reseller names

Use this table:

| Original Supplier Name | Proposed Normalized Name | Parent Supplier | Confidence | Validation Needed |
|---|---|---|---|---|

Do not merge suppliers only because their names are similar. Flag uncertain matches for review.

### Step 5: Clean and Classify Spend
Classify transactions using the approved taxonomy where available.

Possible hierarchy:

- Category
- Subcategory
- Commodity
- Product or service
- Business use case

Use source descriptions, GL codes, supplier information, contract records, and business-owner data.

Use this table:

| Transaction / Supplier | Current Category | Proposed Category | Basis for Classification | Confidence | Validation Needed |
|---|---|---|---|---|---|

Mark low-confidence classifications clearly.

### Step 6: Build the Spend View
Aggregate spend by relevant dimensions.

Examples:

- Supplier and parent supplier
- Category and subcategory
- Business unit and cost centre
- Contract owner
- Geography
- Month or quarter
- Contract status
- Renewal period

Calculate where possible:

- Total spend
- Transaction count
- Average transaction value
- Supplier share
- Category share
- Contracted vs uncontracted spend
- Recurring vs one-time spend
- Renewal exposure

### Step 7: Identify Supplier Concentration
Review concentration by category and business area.

Check:

- Percentage of spend with the top supplier
- Percentage with the top three or five suppliers
- Single-source dependency
- Fragmented spend across many small suppliers
- Parent-company concentration hidden by multiple entities
- Concentration in business-critical areas

Use this table:

| Category | Total Spend | Top Supplier | Top Supplier Share | Concentration Risk | Review Needed |
|---|---|---|---|---|---|

High concentration is not automatically negative. Consider market structure, switching cost, standardization, and supplier performance.

### Step 8: Identify Duplicate or Overlapping Spend
Look for products or services that may serve similar purposes.

Examples:

- Multiple project-management tools
- Multiple e-signature tools
- Multiple collaboration platforms
- Multiple staffing suppliers
- Multiple maintenance providers
- Similar consulting services
- Duplicate support contracts
- Overlapping software modules

Use this table:

| Product / Service Group | Suppliers | Business Owners | Spend | Possible Overlap | Validation Questions |
|---|---|---|---|---|---|

Do not label overlap as waste without validating business, technical, security, regulatory, or contractual requirements.

### Step 9: Identify Contract and Renewal Gaps
Check:

- Spend with no contract reference
- Expired contracts
- Contracts nearing renewal
- Auto-renewal exposure
- Missing notice dates
- Spend above contract value
- Spend outside contract scope
- Multiple contracts with the same supplier
- Unclear contract owner
- Off-contract or maverick spend

Use this table:

| Supplier / Category | Spend | Contract Status | Renewal / Notice Date | Risk | Recommended Review |
|---|---|---|---|---|---|

### Step 10: Identify Anomalies
Look for transactions that differ from normal patterns.

Examples:

- Sudden spend increases
- New supplier with material spend
- Duplicate invoice numbers
- Repeated invoice amounts
- Split purchases
- Unusual month-end activity
- Credits without matching invoices
- Spend after contract expiry
- Amounts outside expected ranges
- Different rates across business units

Treat anomalies as review flags, not proof of error or misconduct.

Use this table:

| Record / Supplier | Anomaly | Evidence | Possible Explanation | Validation Needed |
|---|---|---|---|---|

### Step 11: Review Licence and Usage Data
Where software or subscription data is available, compare:

- Licences purchased
- Licences assigned
- Active users
- Utilization rate
- Modules purchased and used
- Contracted tier
- Actual usage
- Renewal date
- Unit price

Flag:

- Unused licences
- Underused modules
- Duplicate tools
- Growth beyond contracted bands
- Auto-renewal risk
- Pricing tiers that no longer fit demand

Do not assume unused licences can be removed without business and contract validation.

### Step 12: Identify Potential Opportunities
Classify findings into opportunity types:

- Supplier consolidation
- Demand reduction
- Licence optimization
- Contract compliance
- Competitive sourcing
- Renewal negotiation
- Pricing standardization
- Category standardization
- Tail-spend management
- Process improvement
- Contract rationalization
- Data-quality improvement

Use this table:

| Opportunity | Evidence | Indicative Value Basis | Complexity | Risk | Next Validation Step |
|---|---|---|---|---|---|

Do not state a final savings figure unless the baseline, addressable spend, implementation cost, timing, and assumptions are validated.

### Step 13: Prioritize Opportunities
Assess:

- Potential value
- Ease of implementation
- Time to impact
- Stakeholder readiness
- Contract timing
- Supplier dependency
- Operational risk
- Data confidence

Suggested priority labels:

- Immediate review
- Near-term sourcing opportunity
- Renewal opportunity
- Strategic category initiative
- Data validation required
- Monitor only

### Step 14: Run the Validation Loop
Before finalizing, ask:

- Are supplier names normalized correctly?
- Are category assignments supported?
- Are credits and reversals handled correctly?
- Are currencies and taxes consistent?
- Are apparent overlaps genuinely comparable?
- Are contract records complete?
- Are usage assumptions current?
- Are opportunity values supported?
- What requires business-owner confirmation?
- What cannot be concluded from the data?

### Step 15: Prepare the Spend Analysis Output
Default structure:

1. Executive summary
2. Scope and assumptions
3. Data-quality findings
4. Spend overview
5. Supplier concentration
6. Category findings
7. Contract and renewal risks
8. Overlap and anomaly findings
9. Potential opportunities
10. Prioritization
11. Validation questions
12. Human review items

## Output Format

### Executive Summary
```text
Summary:
The analysis covers [period/scope] and [total spend, if validated]. The main findings are [findings]. The highest-priority review areas are [areas]. Potential opportunities require validation of [assumptions/data].
```

### Data-Quality Table
| Data Issue | Impact on Analysis | Severity | Recommended Action |
|---|---|---|---|

### Spend Summary Table
| Category / Supplier | Spend | Share of Total | Contract Status | Key Observation |
|---|---|---|---|---|

### Opportunity Table
| Opportunity | Evidence | Potential Value Basis | Complexity | Confidence | Next Step |
|---|---|---|---|---|---|

### Renewal Risk Table
| Supplier / Contract | Spend | Renewal Date | Notice Date | Risk | Recommended Action |
|---|---|---|---|---|---|

### Anomaly Table
| Transaction / Supplier | Anomaly | Why It Matters | Validation Needed |
|---|---|---|---|

### Human Review Table
| Reviewer | Item to Validate | Why It Matters |
|---|---|---|

## Review Checks
Before finalizing, check:

- Was the original data preserved?
- Were supplier-name changes traceable?
- Were category assignments given confidence levels?
- Were credits, reversals, taxes, and currencies handled?
- Were duplicate rows identified?
- Were overlaps treated as hypotheses?
- Were anomalies treated as review flags?
- Were contract and renewal risks included?
- Were savings claims avoided unless validated?
- Were data limitations stated?
- Were human review items identified?

## Human Review
Humans must review and approve:

- Supplier normalization
- Category classification
- Opportunity validation
- Savings baselines
- Contract interpretation
- Renewal strategy
- Supplier consolidation decisions
- Tool or licence rationalization
- Sourcing pipeline
- Business-impact assumptions
- Final executive recommendations

## Guardrails
The AI must not:

- Invent spend, suppliers, owners, contracts, categories, or renewal dates
- Treat every overlap as waste
- Treat every anomaly as an error or compliance issue
- Claim final savings without validated assumptions
- Recommend supplier termination automatically
- Change source data without traceability
- Ignore currencies, taxes, credits, or accounting periods
- Expose confidential spend information unnecessarily
- Replace finance reconciliation
- Replace procurement, legal, security, technical, privacy, or business-owner review
- Make supplier selection or award decisions

## Example User Request
```text
Use the spend-analysis-skill.md workflow to review this spend file. Normalize suppliers, classify spend, identify overlaps, anomalies, contract gaps, renewal risks, supplier concentration, and potential opportunities. Clearly separate confirmed findings from items requiring validation.
```

## Example Output Instruction
```text
Do not simply summarize total spend. First inspect data quality, preserve the source data, normalize suppliers, classify transactions, and identify patterns. Then provide a spend summary, opportunity table, renewal risks, anomalies, validation questions, and human review items.
```

## Success Criteria
This skill is working when it helps the user:

- Move from raw spend data to procurement-ready insight
- Improve supplier and category visibility
- Identify contract and renewal risks earlier
- Find potential overlaps and anomalies for review
- Build a sourcing or renewal pipeline
- Avoid unsupported savings claims
- Preserve an auditable analysis process
- Keep final decisions with accountable humans
