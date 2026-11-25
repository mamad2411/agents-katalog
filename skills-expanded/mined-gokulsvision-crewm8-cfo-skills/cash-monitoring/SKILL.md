---
name: cash-monitoring
description: Monitors daily cash position across all accounts, flags anomalies, tracks burn rate, and produces a daily cash snapshot. Use when the user mentions cash position, daily cash check, burn rate, bank balance, or asks about unusual transactions or cash alerts.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, cash, treasury, burn-rate, anomaly-detection]
related_skills:
  - cash-forecasting
  - bank-reconciliation
  - banking-relationship-management
  - working-capital-optimization
inputs_required:
  - bank-account-balances-from-all-operating-accounts
  - transaction-log-last-30-days
  - payment-processor-stripe-paypal-balances
  - expected-large-inflows-outflows-this-week
deliverables:
  - daily-cash-snapshot-dashboard
  - anomaly-report-with-flagged-transactions
  - burn-rate-trend-and-runway-projection
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cash Monitoring

Monitor the company's cash position daily across all bank accounts, payment processors, and deposit accounts. Flag unusual transactions, track burn rate, surface cash anomalies, and produce a daily cash snapshot.

## Purpose

Cash is the lifeblood of any startup — running out is the single fastest way to die. This skill ensures that the company's cash position is known at all times, anomalies are caught before they become problems, and burn rate and runway are tracked continuously so leadership can make informed decisions about spending and fundraising timing.

## When to Use

- "What's our cash position right now?"
- "Any unusual transactions today?"
- "Daily cash check / cash snapshot"
- "What's our burn rate this month?"
- "Alert me if cash drops below X"

## Inputs Required

1. **Bank account balances** — current balance for every operating account, via bank API, CSV export, or manual input.
2. **Transaction log (last 30 days)** — for burn rate calculation and anomaly detection.
3. **Stripe/PayPal/processor balances** — funds not yet deposited to the bank.
4. **Expected large inflows/outflows this week** — payroll dates, major vendor payments, expected customer payments.

## Quick Reference

| Metric | Formula | Purpose |
|--------|---------|---------|
| Cash on hand | Sum of all bank + processor + short-term balances | Total available liquidity |
| Net burn | Cash end of month - cash start of month | True cash consumption rate |
| Gross burn | Total operating expenses | Total cash spent before revenue |
| Runway | Cash on hand / avg monthly net burn | Months until cash runs out |
| Restricted cash | Security deposits, escrow, L/C collateral | Non-spendable cash (track separately) |

## Procedure

### 1. Gather Current Balances

For every account, record:
- Account name/nickname
- Financial institution
- Current balance
- Available balance (may differ if there are holds)
- Pending transactions

### 2. Calculate Total Cash Position

```
Cash on hand = sum of all bank account balances
             + sum of all payment processor balances
             + any money market / short-term investment balances

Restricted cash (security deposits, letter of credit collateral) → track separately
```

### 3. Burn Rate Calculation

**Net burn** (most common): cash at end of month − cash at start of month.
**Gross burn**: total operating expenses (excludes revenue).

Rolling 3-month average (more stable than single-month).

### 4. Runway Calculation

```
Runway (months) = Cash on hand / Average monthly net burn
```

- **Green**: > 18 months runway
- **Yellow**: 12–18 months
- **Orange**: 6–12 months — start fundraising or cut burn
- **Red**: < 6 months — critical, immediate action needed

### 5. Anomaly Detection

Scan the last 7 days of transactions. Flag:

- Any single transaction > $5,000 not matching a known vendor pattern.
- Any transaction between 10 PM and 5 AM (unusual for business).
- Round-number transactions ($1,000.00, $10,000.00) — often estimates or manual entries.
- Duplicate payments to the same vendor within 48 hours.
- Transfers between accounts (should not be double-counted).
- Sudden balance decreases > 20% in any single account.
- New counterparties that haven't appeared in the prior 90 days.

### 6. Daily Cash Snapshot

Produce a one-page dashboard:

```
===== DAILY CASH SNAPSHOT - April 28, 2026 =====

TOTAL CASH:        $2,847,000
  Operating:       $2,600,000  (SVB Checking + Mercury)
  Reserves:          $230,000  (Mercury Treasury)
  Processors:         $17,000  (Stripe balance)

BURN RATE:          $85,000/mo  (3-mo trailing net burn)
                     $120,000/mo  (gross burn)

RUNWAY:             33.5 months (net)
                    23.7 months (gross)

FLAGS (last 7 days):
  None / 1 pending / 3 anomalies

CHANGE FROM YESTERDAY:
  Cash: -$14,200  (vendor payments: $12,000, AWS charge: $2,200)
```

## Output Format

- Daily cash snapshot (plain-text dashboard)
- Anomaly report (if any flags)
- Burn rate trend (3-month sparkline or table)
- Runway projection
- Recommendations (if runway < 12 months)

## Done Criteria

The skill is complete when:
1. All bank and processor balances are gathered and netted correctly (no double-counting)
2. Net burn and gross burn are calculated using rolling 3-month average
3. Runway is computed and severity color is assigned
4. Last 7 days of transactions are scanned with anomalies flagged
5. Daily cash snapshot dashboard is produced
6. Recommendations are provided if runway is below 12 months

## Pitfalls

- **Counting restricted cash as available**: security deposits, letter-of-credit collateral, and funds held in escrow are not spendable. Including them in runway calculations creates a dangerously rosy picture.
- **Using a single month's burn rate for runway**: one-off expenses (annual software renewals, tax payments) distort monthly burn. Always use a rolling 3-month average.
- **Double-counting inter-account transfers**: moving $50k from checking to savings shows up as a debit in one account and credit in another. If not netted out, total cash appears to increase artificially.
- **Ignoring payment processor float**: treating Stripe or PayPal balances as immediately available cash overstates liquidity. Funds in processors typically take 2–7 days to settle into the bank.
- **Alert fatigue from threshold-only monitoring**: flagging every transaction above a fixed dollar threshold without context (vendor, payment pattern, expected date) leads to ignored alerts. Anomaly detection must incorporate patterns, not just amounts.

## Verification

Can you answer "what is our total cash position right now?" from the snapshot? Can you answer "how many months of runway do we have?" Are anomalies clearly flagged with context and recommended actions? If not, the monitoring is incomplete.

## Example

**User prompt**: "What's our cash position today?"
**What should happen**: Gather current balances from all bank accounts and payment processors, calculate total cash on hand, compute the latest burn rate and runway, produce a daily cash snapshot dashboard, and flag any anomalies detected in the past 7 days.

**User prompt**: "Check for any unusual transactions this week."
**What should happen**: Pull the last 7 days of transactions across all accounts, run anomaly detection heuristics (off-hours, round amounts, new counterparties, duplicate payments), and return a prioritized flag list with transaction details and recommended actions.

**User prompt**: "Alert me if our cash drops below $500k and tell me how long we have."
**What should happen**: Monitor the cash position against the $500k threshold, compute the current runway in months based on trailing 3-month net burn, project the zero-cash date if burn remains constant, and provide a severity rating (green/yellow/orange/red) with specific recommendations.

## Linked Skills

- Forecast future cash → `cash-forecasting`
- Verify balances against bank → `bank-reconciliation`
- Optimize cash yield → `banking-relationship-management`
- Optimize payment timing → `working-capital-optimization`
