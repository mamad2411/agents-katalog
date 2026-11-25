---
name: letter-of-intent
description: "Creates letters of intent for business transactions with key terms, conditions, and timeline. Use when formalizing preliminary agreement on a business deal."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Letter of Intent

## When to Use This Skill

Use this skill when you need to:
- Draft a letter of intent (LOI) for a business acquisition, partnership, or investment
- Formalize preliminary agreement on key deal terms before drafting a full contract
- Establish exclusivity periods and due diligence timelines
- Create a non-binding framework for a business transaction

**DO NOT** use this skill for final contracts, binding agreements, or simple proposals. An LOI captures deal terms before the definitive agreement is drafted. Always have an attorney review.

---

## Core Principle

A LETTER OF INTENT ALIGNS BOTH PARTIES ON KEY TERMS BEFORE INVESTING IN EXPENSIVE LEGAL DRAFTING — IT IS A HANDSHAKE PUT ON PAPER.

---

## Phase 1: Transaction Details

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Transaction type** | "What type of deal? (acquisition, investment, partnership, licensing, real estate)" | No default — must be provided |
| **Parties** | "Who are the parties involved?" | No default — must be provided |
| **Key terms** | "What are the proposed deal terms? (price, structure, timeline)" | No default — must be provided |
| **Binding provisions** | "Should confidentiality and exclusivity be binding?" | Yes — confidentiality and exclusivity binding |
| **Due diligence period** | "How long for due diligence?" | 30-60 days |
| **Target closing date** | "When do you want to close?" | 60-90 days from LOI signing |

**GATE: Do not proceed without transaction type, parties, and key terms.**

---

## Phase 2: LOI Structure

```
## Letter of Intent

[Date]

[Recipient Name]
[Recipient Title]
[Recipient Company]
[Address]

Re: Letter of Intent — [Brief Description of Transaction]

Dear [Name],

This Letter of Intent ("LOI") sets forth the principal terms under
which [Your Company] ("Buyer/Investor/Partner") proposes to
[acquire/invest in/partner with] [Target Company] ("Seller/Company/
Target"). This LOI is intended to facilitate further discussion and
negotiation of a definitive agreement.

### 1. Transaction Structure

[Description of the proposed transaction — asset purchase, stock
purchase, investment, partnership, licensing arrangement]

### 2. Purchase Price / Investment Amount

- Total consideration: $[X]
- Structure: [Cash / stock / earnout / combination]
- Payment terms: [$X at closing, $X over [X] months, $X based on
  performance milestones]

[For acquisitions, include:]
- Valuation basis: [Multiple of revenue / EBITDA / assets / other]
- Price adjustments: [Working capital adjustment / earn-out based
  on [metrics] over [period]]

### 3. Key Terms and Conditions

| Term | Detail |
|------|--------|
| Closing date | On or before [Date] |
| Employees | [Retained / offered employment / not included] |
| Assets included | [List key assets included] |
| Liabilities assumed | [List or "none"] |
| Representations and warranties | Standard for this type of transaction |
| Non-compete | [Duration and scope for seller] |
| Transition period | [X months of seller support] |

### 4. Conditions Precedent

The closing of this transaction is subject to:
a) Satisfactory completion of due diligence by [Buyer/Investor]
b) Negotiation and execution of a definitive agreement
c) [Board / partner / investor] approval by both parties
d) [Any regulatory approvals required]
e) No material adverse change in the Target's business
f) [Other conditions specific to the deal]

### 5. Due Diligence

[Buyer/Investor] shall have [30-60] days from the execution of this
LOI to conduct due diligence, including review of:
- Financial statements and tax returns ([3-5] years)
- Customer and vendor contracts
- Employee and contractor agreements
- Intellectual property assets
- Legal proceedings and compliance
- [Other relevant areas]

[Seller/Target] agrees to provide reasonable access to information,
personnel, and premises during the due diligence period.

### 6. Exclusivity (BINDING)

During the period from the execution of this LOI until [date or
X days], [Seller/Target] agrees not to solicit, encourage, or
entertain any proposals or offers from third parties regarding a
similar transaction. [Seller/Target] shall immediately notify
[Buyer/Investor] if any unsolicited offers are received.

### 7. Confidentiality (BINDING)

Both parties agree to keep all information exchanged during
negotiations and due diligence strictly confidential. Neither party
shall disclose the existence or terms of this LOI to third parties
without the other party's written consent, except to professional
advisors who are bound by confidentiality obligations.

### 8. Non-Binding Nature

Except for Sections 6 (Exclusivity), 7 (Confidentiality), and
this Section 8, this LOI is not binding and does not create any
legal obligation for either party to consummate the proposed
transaction. A binding obligation will arise only upon execution
of a definitive agreement.

### 9. Expenses

Each party shall bear its own costs and expenses (legal, accounting,
advisory) in connection with this LOI and the proposed transaction.

### 10. Governing Law

This LOI is governed by the laws of [State].

### 11. Expiration

This LOI expires if not executed by both parties by [Date — typically
7-14 days from delivery].

---

Sincerely,

[Your Name]
[Your Title]
[Your Company]

**ACKNOWLEDGED AND AGREED:**

[Recipient Name]
[Recipient Title]
[Recipient Company]
Date: _______________
```

---

## Phase 3: Review Key Terms

- Verify price and payment structure align with both parties' expectations
- Confirm exclusivity period is long enough for due diligence
- Ensure binding vs. non-binding sections are clearly designated
- Check that conditions precedent are achievable within the timeline

---

## Phase 4: Delivery

```
## LOI Checklist

- [ ] Transaction structure clearly described
- [ ] Price and payment terms specified
- [ ] Due diligence period and scope defined
- [ ] Exclusivity period set (binding)
- [ ] Confidentiality clause included (binding)
- [ ] Non-binding nature clearly stated for other provisions
- [ ] Expiration date included
- [ ] Conditions precedent listed
- [ ] Reviewed by legal counsel
- [ ] Sent with appropriate cover communication
```

---

## Example: Small Business Acquisition

**Transaction:** Buyer acquiring an e-commerce business for $250K. **Structure:** $175K at closing, $75K earn-out over 12 months based on maintaining 80% of trailing revenue. **Due diligence:** 45 days. **Exclusivity:** 60 days. **Conditions:** Clean financials, no undisclosed liabilities, seller non-compete for 24 months. **Transition:** Seller provides 90 days of support post-closing.

---

## Anti-Patterns

- **Making the entire LOI binding** — only confidentiality, exclusivity, and expenses should be binding. Everything else is subject to the definitive agreement.
- **Vague price terms** — "we will agree on a fair price" is not a term. Include a specific number or formula.
- **No expiration date** — an LOI without an expiration can leave the other party waiting indefinitely. Set a clear deadline.
- **Skipping exclusivity** — without exclusivity, the other party can shop your offer around. Include an exclusivity period.
- **Using an LOI as the final agreement** — an LOI is a precursor, not a replacement for a definitive agreement.

---

## Recovery

- **Other party pushes back on terms:** LOIs are negotiable. Identify must-haves vs. nice-to-haves and focus on finding common ground on critical terms.
- **Due diligence reveals problems:** The LOI is non-binding for exactly this reason. Renegotiate terms, adjust price, or walk away.
- **Exclusivity period expiring:** Extend by mutual agreement if due diligence needs more time. Do not let exclusivity lapse without a decision.
- **Other party wants to skip the LOI:** Strongly recommend an LOI to avoid expensive legal drafting before terms are aligned. It saves both parties time and money.
