---
name: off-the-plan-risk
description: "Use when you are considering an off-the-plan purchase and want to understand the risks before signing."
---

# Skill — Off-the-Plan Risk

**Stage:** 1 — Analyse / 3 — Stress-Test
**Hook:** Off-the-plan looks great on the brochure. Here's what the brochure doesn't show you.
**Use when:** You are considering an off-the-plan purchase and want to understand the risks before signing.

---

## Purpose

This skill produces a structured risk analysis for off-the-plan property purchases in Australia. It covers the most common risks — valuation shortfall at settlement, developer default, contract terms, strata and body corporate unknowns, and lender policy — and generates the questions to ask before signing a contract.

---

## Reads from

- Property File: SNAPSHOT (if started with a listing analysis)
- Property details: developer, project, price, expected settlement date

## Writes to

- Property File: RED FLAGS (open) — off-the-plan specific flags

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
DEVELOPMENT: [project name, suburb, state, developer name if known]
PROPERTY TYPE: [apartment / townhouse / house and land]
PRICE: $[amount]
EXPECTED SETTLEMENT: [approximate date or "X months/years"]
MY PURPOSE: [owner-occupier / investor]
DEPOSIT PAID: $[amount or "not yet"]
PRE-APPROVAL STATUS: [pre-approved / not yet / speaking to broker]
PLANNED LVR: [% you intend to borrow — e.g. 80%. If unknown, state the assumption]
CASH ON HAND AT SETTLEMENT: $[savings available to cover any shortfall]
```

---

## Output contract

Return exactly these 7 sections:

### 1. WHAT OFF-THE-PLAN ACTUALLY MEANS
Plain-English explanation of what the buyer is signing:
- You are contracting to buy a property that does not yet exist
- Settlement occurs on completion (which may be 1–4+ years away)
- The contract price is fixed, but the property's value at settlement is not
- Finance pre-approval at signing does not guarantee finance at settlement
- The deposit (typically 10%) is held in trust — but developer insolvency risk exists

### 2. VALUATION RISK (the most important risk)
- At settlement, the bank will value the completed property
- If the property has declined in value since you signed, the bank will lend against the lower valuation — not the contract price
- You may need to fund the shortfall from your own savings
- **This risk is highest in:** oversupplied inner-city apartment markets; cooling markets; areas with a large pipeline of new stock

**How the numbers are worked out**

Always model the same downside BAND — value holds, −5%, −10% — using the PLANNED LVR from Inputs (do not assume 80% unless that is what was supplied).

```
bank lends       = settlement valuation × planned LVR
extra cash needed = (contract price × planned LVR) − bank lends
                  = (contract price − settlement valuation) × planned LVR
```

| Scenario | Settlement value | Bank lends (80% LVR) | Extra cash needed at settlement | Assumption — verify with broker + valuer |
|----------|-----------------|----------------------|--------------------------------|-------------------------------------------|
| Value holds | $700,000 | $560,000 | $0 | Estimate only |
| −5% | $665,000 | $532,000 | $28,000 | Estimate only |
| −10% | $630,000 | $504,000 | $56,000 | Estimate only |

Compare each "extra cash needed" figure against CASH ON HAND AT SETTLEMENT from Inputs to see whether the shortfall is coverable. (Illustration only — verify every input. Contract price $700k, 80% LVR assumed.)

### 3. DEVELOPER RISK
Questions to research about the developer:
- How many projects have they completed in the last 5 years?
- Have they experienced insolvencies, stalled projects, or construction defects?
- Do they hold a builder's licence as well as a developer's licence?
- Is the project covered by home warranty insurance (if applicable in your state)?
- Are they a related party builder or an independent builder? (Related-party risk: less competitive procurement)

### 4. CONTRACT RISK FLAGS
Questions for your solicitor or conveyancer before signing:

> **State-specific check:** Home-warranty/builders-warranty insurance and sunset-clause law both differ by state (e.g. cover thresholds and exclusions, and the developer's obligations before triggering a sunset clause). Confirm the rules for the property's state with your solicitor — do not assume the interstate position applies.

**Price and specifications:**
- Is the sunset clause date reasonable? What happens if the developer triggers it?
- Can the developer change specifications, inclusions, or finishes without your consent?
- What is included vs excluded? Car spaces, storage cages, balconies?
- What happens if a variation reduces the value?

**Settlement and finance:**
- What is the sunset clause date? (the last date the contract can be completed)
- Is there a "developer's option" to extend settlement? How many times?
- What is the deposit bond vs cash deposit position?
- What are the termination rights if finance cannot be obtained at settlement?

**Strata and common property:**
- Is the strata plan, by-laws, and initial levy schedule in the contract?
- Who controls the body corporate for the first year or two?
- Are there guaranteed rental returns? (If yes — understand what they mask)

### 5. LENDER RISK FLAGS
Questions for your mortgage broker:
1. "Is this project on any lender's blacklist or subject to LVR restrictions for this postcode?"
2. "Does any lender have a restriction on the percentage of investment properties in this building?"
3. "Will my pre-approval still be valid at settlement in [X years]? What could change?"
4. "What happens to my finance position if I change jobs or my income changes before settlement?"
5. "How is this off-the-plan purchase treated for LMI?"

### 6. RED FLAGS TO WATCH FOR
- Developer offering above-market rental guarantees (masks poor rental demand)
- Sunset clause date is very close to expected completion (developer can trigger and resell at higher price)
- Body corporate levies are unusually low in the contract (will rise significantly after developer control ends)
- Developer cannot demonstrate completed projects of comparable scale
- Apartment is in a postcode with known oversupply or high vacancy rates
- Foreign buyer surcharges apply but were not disclosed upfront
- No independent solicitor review of the contract before signing

### 7. PROFESSIONAL REVIEW CHECKLIST
Before signing any off-the-plan contract:
- [ ] Independent solicitor or conveyancer reviews the full contract (not the developer's lawyer)
- [ ] Mortgage broker confirms lender appetite for this project, building, and postcode
- [ ] Research the developer's track record independently
- [ ] Comparable sales and rental demand research for this suburb and building type
- [ ] Sunset clause risk assessed and understood
- [ ] Cash position to fund a valuation shortfall at settlement — can you cover it?

---

## Safety boundaries

- Never advise whether a specific off-the-plan project is "safe" or "good value"
- Never comment on specific developer financial stability without disclosure
- Never recommend signing without independent legal advice
- Always flag the valuation shortfall risk — it is the most commonly misunderstood risk

---

## Pairs with

- [Suburb Research](suburb-research.md) — oversupply and demand signals
- [Property Cash Flow](property-cash-flow.md) — model the investment case
- [Broker Prep](broker-prep.md) — finance readiness for OTP settlement
- [Due Diligence Risk Scan](due-diligence-risk-scan.md) — contract and legal flags

---

## Disclaimer

> This output is general information and educational preparation only. Off-the-plan property purchases carry significant risks that depend on the specific developer, project, contract terms, and market conditions. Do not sign an off-the-plan contract without independent legal advice from a qualified solicitor or conveyancer. This output is not financial, credit, legal, or investment advice. See [disclaimers/not-legal-advice.md](../disclaimers/not-legal-advice.md) and [disclaimers/not-financial-advice.md](../disclaimers/not-financial-advice.md).
