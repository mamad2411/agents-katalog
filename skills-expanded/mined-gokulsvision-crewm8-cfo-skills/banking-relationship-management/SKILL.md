---
name: banking-relationship-management
description: Manages banking relationships — account optimization, fee negotiation, credit facility oversight, treasury yield, and fraud prevention. Use when the user mentions banking setup, bank fees, credit facility, treasury yield, investing excess cash, opening new accounts, or asks about banking architecture, account optimization, or fraud prevention.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, cash, treasury, banking, fraud-prevention]
related_skills:
  - cash-monitoring
  - cash-forecasting
  - working-capital-optimization
  - bank-reconciliation
inputs_required:
  - current-banking-inventory-all-accounts-and-institutions
  - fee-statements-last-3-months
  - yield-data-on-deposits
  - credit-facility-terms-if-applicable
  - cash-forecast-from-cash-forecasting
deliverables:
  - banking-architecture-summary-with-recommendations
  - fee-analysis-with-negotiation-targets
  - yield-optimization-plan-and-fraud-prevention-checklist
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Banking Relationship Management

Manage the company's banking infrastructure — choose the right banks, optimize accounts, negotiate fees, oversee credit facilities, maximize yield on idle cash, and prevent fraud. Goal: the banking stack is efficient, secure, and invisible.

## Purpose

Banks are the most important vendor a startup never thinks about — until something goes wrong. An account freeze, an unnoticed fee bleed, or a fraud event can paralyze operations. This skill ensures the banking architecture is right-sized, cost-efficient, yield-optimized, and properly secured so that banking becomes a non-issue.

## When to Use

- "Review our banking setup"
- "Should we open another account?"
- "Can we get better rates on our deposits?"
- "Negotiate bank fees"
- "Review our credit facility"
- "How should we invest excess cash?"

## Inputs Required

1. **Current banking inventory** — which banks, which accounts, what they're used for.
2. **Fee statements** — last 3 months of bank fees across all accounts.
3. **Yield data** — current interest rates earned on deposits.
4. **Credit facility terms** — if any venture debt or line of credit exists.
5. **Cash forecast** — from `cash-forecasting` to plan cash needs.

## Quick Reference

| Layer | Purpose | Example |
|---|---|---|
| Operating account | Day-to-day cash in/out, payroll, vendor payments | Mercury, SVB, Brex |
| Reserve/savings | Excess cash earning yield | Mercury Treasury, SVB Money Market |
| Credit card | Employee spend, recurring subscriptions | Brex, Ramp, Mercury IO |
| Payment processor | Customer payment collection | Stripe, Paddle |
| **Yield vehicle** | **Typical yield (2026)** | **Liquidity** |
| Money market / savings | 3-5% | Next-day |
| T-bills (short-term) | 4-5% | At maturity or secondary sale |
| Managed treasury sweep | 4-5% | Same-day |
| Money market funds | 4-5% | Next-day |

## Procedure

### 1. Banking Architecture Review

The standard startup banking stack:

| Layer | Purpose | Example |
|---|---|---|
| **Operating account** | Day-to-day cash in/out, payroll, vendor payments | Mercury, SVB, Brex |
| **Reserve/savings** | Excess cash earning yield | Mercury Treasury, SVB Money Market, TreasuryDirect |
| **Credit card** | Employee spend, recurring subscriptions | Brex, Ramp, Mercury IO |
| **Payment processor** | Customer payment collection | Stripe, Paddle |

Evaluate: is the stack right-sized? Too many banks = reconciliation complexity. Too few = concentration risk.

### 2. Fee Analysis & Negotiation

Track all fees over the last 3 months:

| Fee Type | Monthly Avg | Annualized | Negotiable? |
|---|---|---|---|
| Wire transfer fees (domestic) | $75 (3 × $25) | $900 | Yes — ask for a bundle or free tier |
| Wire transfer fees (international) | $90 (2 × $45) | $1,080 | Sometimes — volume-based |
| ACH fees | $0 | $0 | Usually free |
| Account maintenance | $0 | $0 | Most startup banks are free |
| FX conversion markup | ~1–3% hidden | 1-3% of volume | Can negotiate tighter spreads |
| Card processing (Stripe) | ~2.9% + $0.30 | Depends on volume | Volume-based discount at > $100k/mo |

- Any fee > $500/yr that isn't competitive → open a negotiation.
- "We're considering consolidating to fewer banks" is the most effective negotiation opener.

### 3. Yield Optimization

For excess cash (anything beyond 2 months of operating expenses):

| Vehicle | Typical Yield (2026) | Liquidity | Risk |
|---|---|---|---|
| Business savings / money market | 3-5% | Next-day | Very low |
| Treasury bills (short-term) | 4-5% | Maturity or secondary sale | Essentially zero credit risk |
| Sweep accounts / managed treasury | 4-5% | Same-day | Very low, FDIC insured via network |
| Corporate bonds | 5-6% | Secondary market | Credit risk, duration risk |
| Money market funds (SNAXX, VMFXX) | 4-5% | Next-day | Very low, not FDIC insured |

- **For startups**: never chase yield. Liquidity and principal preservation > extra 0.5%.
- **Model**: if you have $2M excess cash, every 1% of additional yield = $20k/yr. Worth spending time on.

### 4. Credit Facility Management

If you have venture debt or a line of credit:

- Track: drawn amount, undrawn amount, interest rate, interest-only period end, amortization start, covenants.
- **Covenant compliance check**: minimum cash, liquidity ratio, or ARR-based covenants. Run this monthly.
- **Draw planning**: time draws to minimize average balance × interest rate. Only draw what you need for the next 30 days.
- **Refinancing triggers**: if your ARR has grown > 3x since the facility was issued AND rates have dropped, it's worth shopping.

### 5. Fraud Prevention

Bank fraud is the #1 financial risk for startups. Implement:

- **Dual approval**: any payment > $X requires two people.
- **ACH positive pay / debit blocks**: prevent unauthorized ACH pulls.
- **Payment instruction verification**: always call a known number (not the one in the email) to verify payment change instructions.
- **Beneficiary pre-registration**: whitelist known vendors, block new ones by default.
- **Fraud insurance / cyber insurance** — make sure the policy covers social engineering / wire fraud.

## Output Format

- Banking architecture summary with recommendations
- Fee analysis with negotiation targets
- Yield optimization plan with projected incremental interest income
- Credit facility covenant compliance tracker
- Fraud prevention checklist

## Done Criteria

The skill is complete when:
1. Banking architecture is assessed against the standard startup stack with recommendations
2. Fee analysis is completed with annualized costs and negotiation targets
3. Yield optimization plan is sized to the excess cash available from the cash forecast
4. Credit facility compliance (if applicable) is checked against covenants
5. Fraud prevention controls are reviewed and gaps documented

## Pitfalls

- **Single-bank dependency**: relying on one bank for all operating cash, reserves, and credit cards creates a single point of failure. If that bank freezes the account for a compliance review (common in fintech and crypto-adjacent startups), payroll and vendor payments stop. Always maintain at least two banking relationships with enough operating cash in each to cover one payroll cycle.
- **Chasing yield at the expense of liquidity**: locking idle cash into 12-month CDs, corporate bonds, or illiquid instruments to capture an extra 1% yield. When a cash crunch hits (delayed customer payment, unexpected tax bill), the funds are inaccessible without penalty or fire-sale pricing. Match maturities to the cash forecast: only invest beyond money market funds what you are certain you won't need within the instrument's lockup period.
- **Not renegotiating bank fees annually**: accepting the same wire fees, FX spreads, and card processing rates year after year. As transaction volume grows, fee structures that were reasonable at $50k/month volume become punitive at $500k/month. Schedule a banking fee audit every 12 months regardless of whether there's an obvious problem.
- **Treating credit facilities as "free money"**: drawing a venture debt facility to extend runway without modeling the full cost (interest + warrant dilution + covenant constraints). Venture debt is typically 12-18% all-in cost — more expensive than it appears on the rate sheet. Only draw what's needed and model the true all-in cost before committing.
- **Neglecting fraud controls on lower-volume accounts**: implementing dual approval and positive pay on the primary operating account but leaving secondary savings accounts, money market accounts, or reserve accounts with single-signer access. Fraudsters target the least-protected accounts. Every account holding > $10k must have the same fraud controls as the operating account.

## Verification

Can you answer "is our banking architecture right-sized and diversified?" Can you identify every fee above $500/year with a negotiation target? Are yield recommendations sized to the actual cash forecast with liquidity constraints documented? Are fraud control gaps identified for every account? If not, the review is incomplete.

## Example

**User prompt**: "Review our banking setup and tell me if we have the right accounts."
**What should happen**: Inventory all current bank accounts, payment processors, and credit cards, assess the architecture against the standard startup banking stack, check concentration risk (is > 65% of cash in one bank?), verify the two-bank rule is satisfied, and produce a recommendation report with specific account consolidation or expansion suggestions and rationale.

**User prompt**: "How much are we paying in bank fees and can we reduce it?"
**What should happen**: Pull the last 3 months of fee statements across all accounts, categorize fees by type (wire, FX, card processing, maintenance), annualize each category, identify any fee > $500/year that is above market, recommend specific negotiation targets with dollar savings estimates, and provide negotiation scripts tailored to each banking partner.

**User prompt**: "Our cash balance has grown — how should we invest the excess to earn more yield?"
**What should happen**: Calculate excess cash (total cash minus 2× monthly gross burn), map the excess against the 13-week cash forecast to determine how much can be locked up and for how long, present yield options ranked by liquidity and risk, recommend an allocation split (e.g., 50% same-day sweep, 30% 4-week T-bills, 20% money market fund), and estimate the incremental annual interest income from the proposed allocation.

## Linked Skills

- Monitor daily cash and flag anomalies → `cash-monitoring`
- Model banking costs in forecast → `cash-forecasting`
- Payment timing strategy → `working-capital-optimization`
- Reconciliation workflow → `bank-reconciliation`
