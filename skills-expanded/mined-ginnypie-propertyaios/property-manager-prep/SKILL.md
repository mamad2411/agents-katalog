---
name: property-manager-prep
description: "Use when you are appointing a property manager for an investment property and want to prepare a structured brief and question set."
---

# Skill — Property Manager Prep

**Stage:** 4 — Decide and Act
**Hook:** Interview your property manager before they interview the tenant.
**Use when:** You are appointing a property manager for an investment property and want to prepare a structured brief and question set.

---

## Purpose

This skill produces a preparation brief for a property manager appointment conversation. It helps investors understand what to ask about rental appraisal, vacancy management, fees, and property management processes — so they can appoint the right manager and set clear expectations.

---

## Reads from

- Property File: SNAPSHOT, CASH-FLOW ASSUMPTIONS
- Investor profile: investment goals, timeline, property type

## Writes to

- Standalone document (property manager brief)

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PROPERTY: [suburb, state, property type, beds/baths/parking]
SETTLEMENT DATE: [approximate]
CURRENT CONDITION: [vacant / tenanted / to be renovated first]
MY GOAL: [maximise rent / minimise vacancy / minimise management involvement / combination]
ESTIMATED RENT (MY ASSUMPTION): $[/week] (if I have one)
SPECIAL REQUIREMENTS: [pets allowed / furnished / short-stay considered]
```

### Input-branching — add questions based on condition

- **If CURRENT CONDITION is "tenanted":** add — "Am I inheriting the existing lease, and when does it expire?", "What is the current rent versus market?", "Is the bond lodged with the state authority and correctly transferred?", "Are there any rent arrears, disputes, or outstanding maintenance I'm taking on?"
- **If SPECIAL REQUIREMENTS includes "pets allowed":** add — "Can a pet bond or extra bond be charged in this state, and how much?", "How do you handle pet-related damage claims at end of lease?"
- **If SPECIAL REQUIREMENTS includes "short-stay considered":** add — "Is short-stay letting permitted by the local council zoning, owners corporation / body corporate rules, and any state STRA registration scheme?", "Do you manage short-stay, and how do fees differ from long-term management?"

*Assumption — verify tenancy, bond, and short-stay rules with a solicitor/conveyancer and the relevant state tenancy authority; they vary by state.*

---

## Output contract

Return exactly these 5 sections:

### 1. RENTAL APPRAISAL QUESTIONS
Ask each prospective property manager:
1. "What is the current weekly rent range for [property type, beds/baths] in [suburb]?"
2. "What is the current vacancy rate for this property type in this suburb?"
3. "How long are properties like this typically sitting before they find a tenant?"
4. "Is there anything about this property that would limit the tenant pool or rent potential?"
5. "What rental growth have you seen in this suburb over the last 12 months?"

### 2. FEE AND CONTRACT QUESTIONS
Fees vary significantly. Ask:
1. "What is your management fee as a percentage of gross weekly rent?"
2. "Do you charge a letting fee? What is it — and does it apply every time there's a new tenant or just the first time?"
3. "What other fees do you charge? Inspection fees, lease renewal fees, statement fees, VCAT fees?"
4. "Can I see a copy of your management agreement before I sign?"
5. "What is the notice period to terminate the management agreement if I'm not satisfied?"

### 3. MANAGEMENT PROCESS QUESTIONS
1. "How do you screen tenants? What checks do you run?"
2. "How do you handle maintenance requests? What is your approval threshold for spending without calling me?"
3. "How often do you conduct routine inspections, and do you provide a written report with photos?"
4. "How do you handle rent arrears? What is your process if a tenant falls behind?"
5. "How quickly do you typically re-let a property after a vacancy?"

### 4. LOCAL KNOWLEDGE QUESTIONS
1. "What tenant type is most common for this property type in this suburb — families, professionals, students?"
2. "Are there seasonal vacancy patterns I should know about?"
3. "What do tenants in this area prioritise — parking, outdoor space, storage, internet?"
4. "Are there any upcoming developments in this suburb that could increase rental supply?"

### 5. FEE COMPARISON TEMPLATE
A simple comparison table for up to 3 property managers:

| Fee item | PM 1 | PM 2 | PM 3 |
|---|---|---|---|
| Management fee (% gross rent) | | | |
| Letting fee | | | |
| Routine inspection fee | | | |
| Lease renewal fee | | | |
| Maintenance admin fee | | | |
| VCAT / tribunal representation | | | |
| **Annual cost estimate** | | | |

*Assumption — verify every fee against each written management agreement; fees vary by agency and state.*

### How the numbers are worked out

```
annual management cost ≈ mgmt% × annual rent + letting fee + inspection fees + renewal fee
annual rent = weekly rent × 52
```

Worked example: rent $600/week → annual rent $31,200. Management fee 7% → $2,184. Plus a letting fee of ~1 week's rent ($600), two routine inspections at $30 ($60), and a lease renewal fee ($150). Estimated annual management cost ≈ $2,994. (Illustration only — verify every input and fee against the actual agreement.)

---

## How to use this brief

Take these questions to 2–3 property managers, record their answers in the fee comparison table, and compare total annual cost — not just the headline management percentage — before appointing anyone.

**Red flags to watch for:**
- No written management agreement, or reluctance to share it before you sign
- Undisclosed or vaguely described fees ("we'll sort that out later")
- A rental appraisal well above comparable listings with no evidence
- Unclear maintenance approval threshold or inspection process

---

## Safety boundaries

- Never recommend a specific property management company
- Never advise on whether to self-manage vs appoint a manager
- Rental appraisals from a property manager are estimates — flag as such

---

## Pairs with

- [Property Cash Flow](property-cash-flow.md) — use the rental appraisal from the PM to validate your cash-flow assumptions

---

## Disclaimer

> This output is general information and preparation only. It does not constitute financial, credit, tax, legal, or investment advice, and it is not a recommendation to appoint any particular property manager or agency. Rental appraisals provided by property managers are estimates only and do not guarantee rental income. Property management fees, contract terms, tenancy laws, bond rules, and short-stay regulations vary by state and by agency — confirm them independently. Review any management agreement with a licensed solicitor or conveyancer, and confirm the tax treatment of management fees with a registered tax agent before acting.
>
> See [disclaimers/general-information.md](../disclaimers/general-information.md) and [disclaimers/not-financial-advice.md](../disclaimers/not-financial-advice.md) for the full disclaimer.
