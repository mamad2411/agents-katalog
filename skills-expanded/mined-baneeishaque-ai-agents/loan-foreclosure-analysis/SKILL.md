---
name: loan-foreclosure-analysis
description: Industrial protocol for analyzing loan repayment schedules, calculating foreclosure savings, and making optimal financial decisions.
category: Financial-Analysis
---

# Loan Foreclosure Analysis Skill (v1)

This skill provides standardized calculation protocols for personal loan analysis,
foreclosure savings calculations, and optimal financial decision-making.

***

## 1. Core Calculation Protocols

### 1.1 Installment Breakdown Analysis

The agent MUST:

1. Extract all monthly installment principal/interest breakdowns
2. Calculate cumulative principal and interest paid after N installments
3. Verify calculations using Opening/Closing Principal difference
4. Format results in lint-compliant markdown tables per [Markdown Generation Rules](../../../ai-agent-rules/markdown-generation-rules.md)

### 1.2 Remaining Interest Calculation

The agent MUST:

1. Sum interest amounts for all remaining installments
2. Calculate total remaining payments (remaining installments × EMI)
3. Verify against remaining principal balance
4. Identify interest rate pattern (flat/reducing balance)

### 1.3 Interest Rate Verification

The agent MUST:

1. Calculate monthly rate using: `(Interest Amount / Opening Principal) × 100`
2. Verify consistency across multiple installments
3. Convert to annual percentage rate (APR)
4. Document the calculation methodology

***

## 2. Foreclosure Analysis Protocol

### 2.1 Savings Calculation

When provided with a foreclosure amount:

1. Calculate: `Total Remaining Payments - Foreclosure Amount = Gross Savings`
2. Compare loan interest rate vs alternative investment rates
3. Perform month-by-month opportunity cost analysis
4. Provide clear, data-driven recommendation

### 2.2 Opportunity Cost Analysis

The agent MUST create a comparison table showing:

- Installment amount
- Loan interest paid
- Remaining balance
- Alternative investment interest earned
- Net cash position for each scenario

#### 2.2.1 Precise Daily Interest Calculation (Mandatory)

For accurate opportunity cost analysis, the agent MUST:

1. Calculate interest from **current date** to **actual installment dates**, not full calendar months
2. Use daily interest rate: `(annual rate / 365)`
3. Show **exact period dates** and **number of days** for each cash flow segment
4. Show **available cash flow** for each period
5. Calculate period-wise interest earnings

Example table format:

| Period | Dates | Days | Available Cash Flow | Interest Earned |
|--------|-------|------|---------------------|-----------------|
| Period 1 | [Start Date] - [Installment Date] | X days | ₹X,XXX.XX | ₹XX.XX |

### 2.3 Cash Flow Analysis Protocol

The agent MUST perform cash flow analysis when requested:

1. Show available cash flow for each period
2. Highlight when and how cash flow decreases
3. Verify user cash flow assumptions for accuracy
4. Document cash flow dates and amounts precisely

### 2.4 Decision Framework

The agent MUST evaluate and rank these options:

1. **Foreclose immediately** - Net savings calculation
2. **Continue paying all installments** - Net cost calculation
3. **Partial keep then close** - Breakeven point analysis

***

## 3. Environmental & Dependencies

Required tools for verification:

- `markdownlint-cli2` for document validation
- Standard arithmetic operations (no external libraries required)

All generated documents MUST:

- Comply with 120-character line limit
- Use properly formatted markdown tables
- Pass `markdownlint-cli2` audit
- Reference standard calculation protocols

***

## 4. Document Organization Protocol

All loan documents MUST follow the standardized naming convention:

- Prefix: `[user-identifier]-[lender]-[loan-type]-`
- Document name: descriptive kebab-case
- Extension: `.pdf` / `.png` / `.md`

Example: `banee-ishaque-k-bajaj-finserv-personal-loan-foreclosure-payment-receipt.pdf`

***

## 5. Final Settlement Protocol

After loan closure:

1. Calculate total amount paid (installments + foreclosure)
2. Calculate total interest paid (total paid - principal)
3. Calculate savings achieved vs full tenure
4. Document final rates and statistics
5. Generate final settlement summary document
6. Verify all closure documentation is present:
   - Foreclosure payment receipt
   - No due certificate
   - Final statement of account
7. Organize and rename all supporting documents to standardized format

***

## 6. Traceability

Reference Implementation:

- [Loan Analysis Conversation Log](docs/conversation-log.md)

This skill follows all standards defined in:

- [AI Rule Standardization Rules](../../../ai-agent-rules/ai-rule-standardization-rules.md)
- [Markdown Generation Rules](../../../ai-agent-rules/markdown-generation-rules.md)
