---
name: broker-prep
description: "Use when you are ready to speak with a mortgage broker and want to prepare a structured briefing pack."
---

# Skill — Broker Prep

**Stage:** 4 — Decide and Act
**Hook:** Walk into your broker conversation knowing what to ask.
**Use when:** You are ready to speak with a mortgage broker and want to prepare a structured briefing pack.

---

## Purpose

This skill produces a structured preparation pack for a mortgage broker conversation. It summarises the user's financial position, the property under consideration, and generates the specific questions to ask — based on the user's situation and what the Property File has surfaced so far.

This is preparation material only. The broker provides the credit advice.

---

## Reads from

- Property File: SNAPSHOT, CASH-FLOW ASSUMPTIONS, FINANCE POSITION, RED FLAGS, SUBURB & DEMAND
- Investor Profile: income type, liabilities, deposit, property purpose

## Writes to

- Property File: VERIFY-WITH-A-PRO (broker questions)

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
MY INCOME: [gross annual $X; type: PAYG / self-employed / rental / other]
CO-BORROWER: [yes — gross $X, type / no]
LIABILITIES: [HECS $X / cards total limit $X / personal loans $X / existing mortgages $X]
DEPOSIT AVAILABLE: $[amount]
PROPERTY: [suburb, state, type, price $X, purpose: owner-occupied / investment]
LVR TARGET: [80% / 90% / unsure]
LOAN TYPE PREFERENCE: [interest-only / P&I / unsure]
KEY QUESTIONS I ALREADY HAVE: [list anything you know you want to ask]
```

---

## Output contract

Return exactly these 6 sections:

### 1. WHAT TO BRING TO YOUR BROKER
A checklist of documents typically required. Mark any item that does not apply to the user's situation as **N/A** (for example, "rental income" for a first purchase, or "existing mortgage statements" with no current loan) rather than leaving an empty box — this keeps the list honest and shows nothing was missed.

**Income verification:**
- [ ] Last 2 payslips (PAYG)
- [ ] Last 2 years tax returns and NOAs (self-employed)
- [ ] PAYG Summaries / income statements
- [ ] Rental income: lease agreement and property manager statements

**Assets and savings:**
- [ ] Last 3 months bank statements (savings accounts)
- [ ] Evidence of deposit source: savings history, sale proceeds, gift letter
- [ ] Superannuation statements (if using first home super saver)

**Liabilities:**
- [ ] Credit card statements (total limits, not just balances)
- [ ] Loan statements (personal, car, HECS)
- [ ] Existing mortgage statements (if applicable)

**Identity:**
- [ ] Driver's licence and passport (or 100-point ID)

**Property:**
- [ ] Listing URL or contract of sale (if you have it)

### 2. YOUR FINANCIAL SUMMARY (for the broker conversation)
A plain-English summary the user can share or read from:

- Gross income: $X per year ([income type])
- Co-borrower: [yes $X / no]
- Key liabilities: HECS $X, card limits $X, [other]
- Deposit available: $X
- Target purchase price: $X
- Purpose: [owner-occupied / investment]
- Preferred LVR: [80% / 90%]
- Preferred loan type: [IO / P&I / flexible]

### 3. QUESTIONS TO ASK YOUR BROKER
Based on this profile and the Property File, ask your broker:

**About your borrowing position:**
1. "Based on my income, liabilities, and the APRA serviceability buffer, what is your estimate of my borrowing capacity?"
2. "Which lenders are most likely to suit my [income type] situation?"
3. "What is the biggest risk to my approval from my current financial profile?"

**About this specific property:**
4. "Are there any lender restrictions on this property type in this postcode? What LVR can I access?"
5. "Is LMI required at my LVR, and what does it cost? Is it worth paying to keep more cash?"

**About loan structure:**
6. "Should I fix, go variable, or split? What are the trade-offs at current rates?"
7. "Interest-only vs P&I — what is the post-tax difference for an investment property at my tax rate?"
8. "What offset account structure gives me the most flexibility if I want to access equity later?"

**About the process:**
9. "What is your estimated timeline from application to pre-approval and formal approval?"
10. "What could delay my approval? What do you need from me to avoid that?"

**Tailoring — add these questions when the profile triggers them:**
- If income type includes **self-employed**: "As a sole trader / company director, which lenders assess my income most favourably, and can any lend on one year of returns rather than two? What add-backs do you apply?"
- If **LVR target ≥ ~88%**: "At this LVR, can the LMI premium be capitalised on top of the loan rather than paid upfront, and how does that change my repayments and total cost?"

### 4. FLAGS TO RAISE (from the Property File)
If the Property File has open red flags, list them here for the broker conversation.

**No Property File? (the normal standalone case)** Derive the flags directly from the Inputs block, for example:
- Self-employed or non-PAYG income → "ask which lenders accept [income type] most favourably"
- LVR target ≥ 88% → "ask about LMI cost and whether it can be capitalised"
- High card limits or HECS → "ask how these reduce borrowing capacity"
- Apartment / high-density postcode → "ask about lender LVR caps for this property type"
- Interest-only preference → "ask which lenders offer it and at what rate premium"

Example flags:
- [e.g. "High-density postcode — ask about lender LVR caps"]
- [e.g. "Self-employed income — ask which lenders accept [income type] most favourably"]
- [e.g. "Strata building over 10 storeys — ask about lender appetite"]

### 5. WHAT TO EXPECT FROM A GOOD BROKER CONVERSATION
A good broker conversation should cover:
- Your full financial picture, not just income
- Multiple lender options, not just one
- Loan structure recommendations with reasons
- A realistic timeline and process overview
- Honest assessment of any risks or complications in your profile

If a broker does not ask about your liabilities, living expenses, or other assets — ask them to revisit.

### 6. AFTER THE CONVERSATION
Questions to ask yourself after the broker meeting:
- Did they explain their lender recommendations and why?
- Do I understand the total cost of the loan (rate, fees, LMI if any)?
- Do I know the next steps and timeline?
- Did they give me a Credit Proposal Disclosure document?

---

## Safety boundaries

- Never recommend a specific lender or loan product
- Never advise on borrowing capacity as if it is a lender assessment
- Never present broker preparation as a substitute for broker advice
- Always direct final credit decisions to the licensed mortgage broker

---

## Pairs with

- [Cash Flow Stress Test](property-cash-flow.md) — the numbers to discuss with the broker
- [Due Diligence Risk Scan](due-diligence-risk-scan.md) — the property flags to raise
- [Suburb Research](suburb-research.md) — the demand picture behind the property

---

## Disclaimer

> This output is general information and preparation only. It is not credit advice or a credit assessment. Your borrowing capacity, loan structure, and lender selection depend on your individual circumstances and the credit policy of specific lenders. Seek advice from the holder of an Australian Credit Licence (ACL) before making any financing decision. See [disclaimers/not-credit-advice.md](../disclaimers/not-credit-advice.md).
