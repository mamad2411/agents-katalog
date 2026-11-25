---
name: self-employed-lending-prep
description: "Use when you (or your client) are self-employed, or own a business, company, trust, or SMSF, and need to gather the financials and ATO documents a lender requires for a home or investment loan."
---

# Skill — Self-Employed & Business-Owner Lending Prep

**Stage:** 2 — Finance
**Hook:** If you're self-employed, your loan lives or dies on the documents your accountant provides. Get the exact list ready *before* you apply — nothing stalls a self-employed application like a half-complete document pack.
**Use when:** You (or your client) are self-employed, or own a business, company, trust, or SMSF, and need to gather the financials and ATO documents a lender requires for a home or investment loan.

---

## Purpose

This skill produces the **exact set of documents a self-employed or business-owner borrower needs from their accountant** for a lending application — tailored to their entity structure — plus a ready-to-send request email (see the paired report template). It exists because self-employed applications are most often delayed by an incomplete or wrong document pack, not by serviceability.

It is a preparation checklist. It is **not** credit advice, and the definitive document list for a specific application always comes from the licensed broker or lender.

---

## Reads from

- Investor Profile: income type, entity structure (if available)
- Or: "Nothing — this is an entry point. The entity structure is enough."

## Writes to

- Property File: FINANCE POSITION (document checklist status)

---

> **Running this standalone:** This skill is self-contained. Give it the borrower's entity structure and the lending purpose — that's all it needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
BORROWER NAME(S): [applicant name(s)]
ENTITY STRUCTURE: [list EVERY entity involved — sole trader / partnership / company / trust / SMSF]
NUMBER OF ENTITIES: [how many businesses/entities in total]
LENDING PURPOSE: [purchase / refinance / investment]
FINANCIAL YEARS REQUIRED: [usually the last 2 completed FYs — e.g. 2024 & 2025]
GST REGISTERED / LODGES BAS: [yes / no / unsure]
ACCOUNTANT: [name / firm — only if you'll send the request email]
```

---

## The core document set (why lenders ask for each)

This is the standard self-employed pack most lenders want. Tailor it to the entity structure (see next section) — never present it as the final list for a specific lender.

| Document | Covers | Why the lender wants it |
|---|---|---|
| Business **financials** (P&L + balance sheet) — all businesses/entities, **last 2 FYs** | Each trading entity | Confirms business income, expenses, and profitability trend |
| **Tax returns** for all entities — last 2 FYs | Company / trust / partnership | Verifies declared entity income and distributions |
| **Individual tax returns** — all applicants, last 2 FYs | Each borrower | Verifies personal taxable income |
| Latest year **Notice of Assessment (NOA)** | Each borrower | Confirms the ATO-assessed income figure |
| Individual **ATO portal — Income Tax Account statement** | Each borrower | **Only if there is a debit balance on the latest NOA** — shows any personal ATO debt |
| Business **ATO portal — 12-month running balance on ITA & ICA** (all entities) | Each entity | Shows Income Tax Account + Integrated Client Account position — flags ATO arrears |
| Business **ATO portal — front-page summary of all tax accounts** | Each entity | Snapshot of every tax account balance |
| **BAS** — all ATO-lodged Business Activity Statements **since the end of the last FY** | GST-registered entities | Bridges the gap between the last financials and today |
| **Ownership confirmation** — shareholders / beneficial owners | Company / trust | AML/KYC and to confirm who controls the entity |

> ATO abbreviations: **ITA** = Income Tax Account · **ICA** = Integrated Client Account · **NOA** = Notice of Assessment · **BAS** = Business Activity Statement.

---

## Output contract

Return exactly these 5 sections:

### 1. TAILORED DOCUMENT CHECKLIST
Reproduce the document set above as a checkbox list, **tailored to the borrower's entity structure**:
- **Sole trader only:** individual tax returns + NOA + business schedule; drop company/trust-only items (entity tax returns, shareholder/beneficial-owner confirmation).
- **Company:** add company tax returns, company financials, shareholder confirmation, and (often) a company constitution.
- **Trust:** add trust tax returns, trust financials, the **trust deed**, and beneficiary/beneficial-owner confirmation.
- **SMSF (if borrowing in super):** add SMSF financials, SMSF tax return, the trust deed, and the bare/custodian trust documents — flag that SMSF lending is specialist.
- Include only the ATO-portal Income Tax Account statement **if** there is a debit balance on the latest NOA.

### 2. WHY EACH DOCUMENT MATTERS
A short plain-English line per document group (income verification / ATO-debt check / ownership) so the borrower and accountant understand the ask and can move quickly.

### 3. TAILORING BY STRUCTURE
State clearly what changes for this borrower's specific structure vs the generic list — what's added, what's dropped, and any specialist flag (e.g. SMSF, multiple trusts, recently changed structure).

### 4. READY-TO-SEND ACCOUNTANT REQUEST EMAIL
Produce a request email using the paired template ([self-employed-lending-doc-request.md](../report-templates/self-employed-lending-doc-request.md)), filled with the borrower's details and the tailored list. Keep client details as placeholders unless supplied. Include the note that the client has authorised the request and that documents must be shared securely.

### 5. NEXT STEPS & QUESTIONS FOR YOUR BROKER
- "Does the chosen lender accept **1 year** of figures, or require the **full 2 years**?"
- "Are there **addbacks** (depreciation, one-off expenses, interest) my accountant should note to lift assessable income?"
- "Is any **ATO payment arrangement** a problem for this lender, and how should we present it?"
- "Which lenders are most favourable for my structure and time trading?"

---

## Safety boundaries

- This is a document-preparation checklist, **not credit advice** and not a lender's document list — the exact requirements vary by lender and applicant and must be confirmed with a licensed broker (ACL holder) or the lender.
- Never request or handle a client's financial documents without their authority, and always share them through a **secure** channel — never plain email attachments.
- Never state a serviceability outcome or borrowing figure here — that is the job of [Borrowing Power](borrowing-power.md) and the broker.
- ATO processes, portal names, and lender document rules change — verify current requirements.

---

## Professional review prompts

- Ask your **mortgage broker (ACL holder)**: "For my structure and this lender, what is the exact document list and how many years?"
- Ask your **accountant / registered tax agent**: "Can you prepare these ATO-portal reports and confirm the entity ownership, and are all lodgements up to date?"

---

## Pairs with

- [Borrowing Power](borrowing-power.md) — estimate serviceability once the income picture is clear
- [Broker Prep](broker-prep.md) — the full package to bring to the broker
- [Accountant Prep](accountant-prep.md) — the tax-side conversation with your accountant

---

## Disclaimer

> This output is general information and educational preparation only. It is a document-preparation checklist, **not credit advice** and not a lender's document requirement list. Actual documents required depend on the lender, the applicant, and the entity structure, and must be confirmed with the holder of an Australian Credit Licence (ACL) or the lender. Client financial documents must only be requested with authority and shared securely. This is not financial, tax, or legal advice. See [disclaimers/not-credit-advice.md](../disclaimers/not-credit-advice.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
