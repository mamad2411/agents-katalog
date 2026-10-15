---
name: cfo-orchestrator
description: Routes CFO and financial operations requests to specialized sub-skills based on user intent matching, task classification, and multi-skill chain assembly. Use when the user mentions startup CFO tasks, financial operations, reporting, fundraising questions, cash management, financial planning, strategic advisory, or asks about running any CFO-related workflow.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, orchestrator, startup, routing, financial-operations]
related_skills:
  - transaction-processing
  - accounts-payable-management
  - accounts-receivable-management
  - payroll-processing
  - ledger-management
  - subscription-management
  - cash-monitoring
  - cash-forecasting
  - working-capital-optimization
  - bank-reconciliation
  - banking-relationship-management
  - data-room-management
  - fundraising-financials
  - cap-table-management
  - investor-relations
  - fundraising-process-management
  - term-sheet-analysis
  - budget-creation-management
  - revenue-forecasting
  - scenario-planning
  - unit-economics-analysis
  - business-case-modeling
  - forecast-accuracy-tracking
  - monthly-close-process
  - financial-statement-generation
  - board-reporting
  - audit-preparation
  - tax-compliance-management
  - internal-controls-design
  - pricing-strategy-advisory
  - profitability-analysis
  - strategic-initiative-modeling
  - risk-management
  - cost-optimization
  - headcount-and-comp-planning
inputs_required:
  - user-request-text
  - skill-registry
  - session-context
  - organizational-stage-information
deliverables:
  - matched-skill-slugs
  - loaded-skill-content
  - execution-plan-with-dependency-order
  - guardrail-flags
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# CFO Orchestrator

## Purpose

The CFO Orchestrator is the master router for all startup CFO and financial operations tasks. It exists to classify ambiguous user requests, match them to the correct specialized sub-skill, and assemble multi-skill chains when a task spans multiple domains. Without it, agents would need to guess which skill to load, leading to incorrect routing, missed dependencies, and inefficient workflows.

## When to Use

- "Help me with a CFO task"
- "I need finance help / financial operations support"
- "Route this request to the right finance skill"
- Any startup finance query where the specific sub-skill is not yet identified
- "What skills do you have for CFO work?"

## Inputs Required

| Input | Description |
|---|---|
| **User request text** | The natural-language query or task description from the user |
| **Skill registry** | The canonical set of 35 CFO sub-skills with their directory slugs |
| **Session context** | Previously loaded skills, prior tasks, organizational stage |

## Quick Reference

| Concept | Description | Example |
|---------|-------------|---------|
| Intent Classification | Parse domain, verb, entities, and urgency from the user request | "Process payroll" → Domain: FinOps, Verb: Process |
| Skill Matching | Map classified intent to 1 of 35 sub-skills via routing tables | "Pay vendors" → accounts-payable-management |
| Skill Chain | Ordered sequence of skills for multi-domain tasks | monthly-close-process → financial-statement-generation → board-reporting |
| Guardrail Check | Verify confidentiality, no auto-execution, explicit assumptions | Block auto-posting of transactions without human review |

## Procedure

### Step 1: Intent Classification

Parse the user request. Identify:
- **Domain**: Financial Ops, Cash & Treasury, Fundraising, FP&A, Reporting & Compliance, Strategic Advisory
- **Verb**: Process, Generate, Analyze, Plan, Reconcile, Advise, Track, etc.
- **Entities**: Vendors, customers, employees, investors, accounts, statements, etc.
- **Urgency**: Immediate, this week/period, ongoing/recurring

### Step 2: Skill Matching

Match against the routing map below. If multiple skills match, determine the dependency order.

#### Routing Map

##### Tier 1: Financial Operations

| User says something like... | Load this skill |
|---|---|
| "Process these invoices / expenses / receipts / transactions" | `transaction-processing` |
| "Pay these vendor invoices / schedule payments / reconcile a vendor" | `accounts-payable-management` |
| "Invoice this customer / collect payment / track DSO" | `accounts-receivable-management` |
| "Run payroll / calculate tax withholding / track benefits" | `payroll-processing` |
| "Update the general ledger / journal entries / chart of accounts" | `ledger-management` |
| "Manage our SaaS subscriptions / track renewals / optimize costs" | `subscription-management` |

##### Tier 2: Cash & Treasury

| User says something like... | Load this skill |
|---|---|
| "What's our cash position? / Any unusual transactions? / Daily cash check" | `cash-monitoring` |
| "Build a cash forecast / 13-week forecast / scenario cash model" | `cash-forecasting` |
| "Optimize payment timing / improve DPO / working capital" | `working-capital-optimization` |
| "Reconcile bank accounts / match transactions / card reconciliation" | `bank-reconciliation` |
| "Review our banking relationships / negotiate fees / credit facility" | `banking-relationship-management` |

##### Tier 3: Fundraising & Capital

| User says something like... | Load this skill |
|---|---|
| "Set up data room / organize investor docs / due diligence" | `data-room-management` |
| "Build fundraising model / pitch deck numbers / investor Q&A" | `fundraising-financials` |
| "Cap table update / dilution analysis / SAFE notes" | `cap-table-management` |
| "Send investor update / board prep / monthly investor letter" | `investor-relations` |
| "Plan our fundraising round / timeline / round structure" | `fundraising-process-management` |
| "Analyze this term sheet / negotiate terms / liquidation preferences" | `term-sheet-analysis` |

##### Tier 4: Financial Planning & Analysis

| User says something like... | Load this skill |
|---|---|
| "Create a budget / annual plan / departmental budgets" | `budget-creation-management` |
| "Revenue forecast / cohort model / pipeline forecast / SaaS metrics" | `revenue-forecasting` |
| "Run scenarios / sensitivity analysis / best case worst case" | `scenario-planning` |
| "Analyze unit economics / CAC / LTV / payback period" | `unit-economics-analysis` |
| "Build a business case / ROI model / NPV for this initiative" | `business-case-modeling` |
| "How accurate were our forecasts? / track forecast variance" | `forecast-accuracy-tracking` |

##### Tier 5: Reporting & Compliance

| User says something like... | Load this skill |
|---|---|
| "Run monthly close / revenue recognition / accruals" | `monthly-close-process` |
| "Generate P&L / balance sheet / cash flow statement" | `financial-statement-generation` |
| "Prepare board report / executive summary / variance commentary" | `board-reporting` |
| "Get ready for the audit / schedules / walkthroughs" | `audit-preparation` |
| "Handle tax filings / compliance calendar / multi-state" | `tax-compliance-management` |
| "Design internal controls / segregation of duties / audit trails" | `internal-controls-design` |

##### Tier 6: Strategic Advisory

| User says something like... | Load this skill |
|---|---|
| "Advise on pricing / competitive analysis / tiers / increases" | `pricing-strategy-advisory` |
| "Profitability analysis by product/customer/channel" | `profitability-analysis` |
| "Model this strategic initiative / expansion / M&A" | `strategic-initiative-modeling` |
| "Identify our financial risks / operational risks / insurance gaps" | `risk-management` |
| "Optimize our costs / renegotiate vendors / find savings" | `cost-optimization` |
| "Review headcount plan / comp benchmarks / hiring ROI" | `headcount-and-comp-planning` |

### Step 3: Skill Loading & Chain Assembly

Load the primary skill. If the task requires a chain, load all skills in dependency order and present the full chain to the user.

#### Multi-Skill Chains

When a user request spans multiple functions, load and chain them in order:

| Request Pattern | Skill Chain |
|---|---|
| "Run monthly close" | `monthly-close-process` → `financial-statement-generation` → `board-reporting` |
| "Process payroll" | `payroll-processing` → `tax-compliance-management` → `ledger-management` |
| "New fundraising round" | `fundraising-financials` → `fundraising-process-management` → `data-room-management` → `cap-table-management` |
| "Annual planning" | `budget-creation-management` → `revenue-forecasting` → `scenario-planning` |
| "Cost optimization sprint" | `cost-optimization` → `subscription-management` → `profitability-analysis` |
| "Audit prep + close" | `audit-preparation` → `monthly-close-process` → `financial-statement-generation` |
| "Board meeting prep" | `board-reporting` → `financial-statement-generation` → `investor-relations` |

### Step 4: Guardrail Check

Before routing to execution, verify:
- Confidential data is handled appropriately
- No auto-execution of transactions
- Assumptions are explicit and stated

### Heuristics

- **Match on verbs first**: "Process", "Generate", "Analyze", "Plan" narrow down the tier immediately
- **Entity nouns confirm the domain**: "vendor" → AP, "customer" → AR, "investor" → Fundraising
- **Default to the most specific skill**: If unclear between transaction-processing and accounts-payable-management, ask the user one clarifying question
- **Single-tier tasks are common**: Most user requests resolve to one skill. Only escalate to chains when the task explicitly spans multiple domains
- **Stage-awareness**: Seed-stage startups rarely need `internal-controls-design` or `audit-preparation` in depth; adjust depth accordingly

### Edge Cases

- **Ambiguous requests**: If a query could match 2+ skills equally, present both options and let the user choose. Example: "Handle these invoices" could be AP or AR depending on context
- **Cross-tier workflows**: Some requests genuinely span tiers (e.g., "Prepare for our Series A" touches Fundraising, FP&A, and Reporting). Build the chain explicitly
- **User references a prior conversation**: Re-load previously used skills before attempting new routing
- **Non-finance requests**: If the user request is clearly outside the CFO domain, politely decline and suggest the appropriate domain

## Output Format

- Matched skill slugs (primary + chain)
- Loaded SKILL.md content for each matched skill
- Execution plan with dependency order
- Guardrail flags (if any)

## Done Criteria

The skill is complete when:
1. User intent is correctly classified into domain, verb, entities, and urgency
2. At least one sub-skill is matched to the user request with high confidence
3. Multi-skill chains are assembled in the correct dependency order when the task spans domains
4. Guardrail checks are performed before routing to execution
5. All assumptions about organizational stage and task scope are surfaced to the user
6. The user has confirmed the routing decision before any skill is loaded

## Pitfalls

- **Over-routing**: Loading 5+ skills for a simple "what's our cash" question. Start with one, add only when the user confirms scope
- **Skipping guardrails**: Routing directly to execution without the confidentiality and transaction-safety checks
- **Assuming stage maturity**: Applying Series B-level processes (full internal controls, multi-entity consolidation) to a seed-stage startup with 5 employees
- **Chain without dependency order**: Loading skills in random order rather than the correct dependency sequence (e.g., `board-reporting` before `financial-statement-generation` makes no sense)
- **Misclassifying urgency**: Treating a routine monthly task with the same urgency as a "we're running out of cash in 3 weeks" crisis

## Verification

Can you trace any user request to a specific routing table entry? Is the dependency order correct for multi-skill chains? Are guardrails preventing auto-execution of potentially destructive actions? If the user's request is ambiguous, has the orchestrator presented multiple options rather than guessing?

## Example

**Example 1: Simple Routing**
> User: "Run payroll for this pay period"

→ Orchestrator matches to `payroll-processing`. Loads the skill. Confirms: "I'll load the payroll processing skill to handle this. What's your pay period dates and employee roster?"

**Example 2: Multi-Skill Chain**
> User: "We need to close the books for March and get ready for our board meeting"

→ Orchestrator identifies: `monthly-close-process` → `financial-statement-generation` → `board-reporting`. Loads all three in order. Confirms: "This will be a 3-step chain: monthly close first, then financial statements, then the board report. Shall I start with the close checklist?"

**Example 3: Ambiguous Request**
> User: "Handle these invoices"

→ Orchestrator detects ambiguity (AP vs AR). Asks: "Are these vendor invoices you need to pay (accounts payable), or customer invoices you need to send and collect (accounts receivable)?"

## Guardrails

- **Confidentiality**: Never output full cap tables, full bank account numbers, or personally identifiable information without user confirmation.
- **Assumptions are explicit**: Always state what you're assuming (e.g., "Assuming a 30% tax rate").
- **No auto-execution of financial transactions**: Present the work, ask for review before any action that would move money or commit to a filing.
- **All outputs are advisory**: Remind the user that final decisions are theirs and their CPA's/lawyer's.
