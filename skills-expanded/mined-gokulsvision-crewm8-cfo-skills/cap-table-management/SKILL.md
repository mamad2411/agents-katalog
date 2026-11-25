---
name: cap-table-management
description: Manage the capitalization table — track all equity holders, SAFEs and convertible notes, model dilution scenarios, and maintain a fully diluted view. Use when the user asks about updating the cap table, modeling dilution, converting SAFEs, managing the option pool, or understanding ownership percentages.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, fundraising, cap-table, equity, dilution]
related_skills:
  - fundraising-financials
  - fundraising-process-management
  - term-sheet-analysis
  - data-room-management
  - investor-relations
  - headcount-and-comp-planning
inputs_required:
  - current-cap-table-spreadsheet-or-carta-pulley-export
  - new-financing-terms-from-term-sheet-analysis
  - option-plan-current-pool-grants-outstanding-and-available
  - SAFE-convertible-note-register-with-terms
deliverables:
  - current-cap-table-issued-and-fully-diluted-views
  - SAFE-note-conversion-analysis-and-dilution-waterfall
  - pro-forma-cap-table-post-raise
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cap Table Management

Manage the company's capitalization table — the definitive record of who owns what. Track all equity holders, model dilution from future rounds, handle SAFE/convertible note conversions, manage the option pool, and maintain a fully diluted view.

## Purpose

The cap table is the ownership constitution of the company — every financing, every grant, every conversion changes who owns what. Mistakes here are irreversible and expensive. This skill ensures the cap table is always accurate, fully diluted, and ready for modeling any fundraise scenario so founders always know their true ownership.

## When to Use

- "Update the cap table for our new round"
- "Model dilution from this term sheet"
- "What does fully diluted ownership look like?"
- "Convert our SAFEs / notes for the Series A"
- "How big should our option pool be?"
- "Who owns what percentage?"

## Inputs Required

1. **Current cap table** — spreadsheet, Carta/Pulley/AngelList export, or manual listing of all securities.
2. **New financing terms** — from `term-sheet-analysis` or `fundraising-process-management`.
3. **Option plan** — current pool size, grants outstanding, available for grant.
4. **SAFE/convertible note register** — amount, valuation cap, discount rate, issue date.

## Quick Reference

| Security Type | Description | Tracking Notes |
|---|---|---|
| Common Stock | Founders, early employees, advisors | Track vesting schedules |
| Preferred Stock | Investors (Series Seed, A, B, etc.) | Track liquidation preferences |
| Stock Options (ISOs, NSOs) | Granted but unexercised | Include in fully diluted count |
| SAFEs | Simple Agreement for Future Equity | Most dilutive conversion = valuation cap only |
| Convertible Notes | Debt that converts to equity | Include accrued interest in conversion |
| **Fully diluted** | Issued + all options + warrants + convertible securities | This is the number VCs care about |

## Procedure

### 1. Cap Table Format

Build a table with these columns:

| Shareholder | Security Type | Shares | Ownership % (Issued) | Ownership % (Fully Diluted) | Issue Price | Total Invested | Liquidation Preference |
|---|---|---|---|---|---|---|---|

### 2. SAFE / Note Conversion

When a priced round triggers conversion:

**SAFE with valuation cap:**
```
Conversion price = min(valuation cap / fully diluted shares pre-money, round price × discount %)
Conversion shares = SAFE investment / conversion price
```

**Convertible note:**
```
Conversion price = min(cap / fully diluted, round price × discount)
Conversion shares = (principal + accrued interest) / conversion price
```

### 3. Dilution Modeling

Model the impact of a new round:

```
Step 1: Start with current fully diluted shares (FD0)
Step 2: Increase option pool if needed (add to FD0, dilutes existing)
Step 3: Calculate new investor shares = New investment / Price per share
Step 4: New fully diluted shares = FD0 + new investor shares
Step 5: Dilution per existing holder = 1 - (ownership before / ownership after)
```

### 4. Pro Forma Cap Table (Post-Raise)

| Shareholder | Before ($) | Before (%) | After ($) | After (%) | Dilution |
|---|---|---|---|---|---|
| Founders | 6,000,000 | 60% | 6,000,000 | 42% | 30% |
| Employee Pool | 1,500,000 | 15% | 2,500,000 | 17.5% | — |
| Seed Investors | 2,000,000 | 20% | 2,000,000 | 14% | 30% |
| SAFE Holders | 500,000 | 5% | 800,000 | 5.6% | — |
| New Series A | — | — | 3,000,000 | 20.9% | — |
| **Total** | **10,000,000** | **100%** | **14,300,000** | **100%** | |

### 5. Common Calculations

- **Price per share**: Pre-money valuation / fully diluted shares pre-money.
- **Ownership %**: Shares held / total fully diluted shares.
- **Investment multiple**: Current value (per latest round price) / total invested.
- **Founder vesting status**: how much is vested vs unvested.

### 6. Cap Table Hygiene Checklist

- [ ] All grants have board approval documented
- [ ] 83(b) elections filed for all restricted stock grants
- [ ] No "missing" shares (issued - outstanding doesn't reconcile)
- [ ] Option plan has enough shares for planned hiring for next 12 months
- [ ] Advisor grants have vesting schedules
- [ ] No oral promises of equity that aren't documented
- [ ] 409A valuation is current (within 12 months)

## Output Format

- Current cap table (issued & fully diluted views)
- SAFE/note conversion analysis
- Dilution waterfall from proposed round
- Pro forma cap table post-raise
- Option pool analysis (grants outstanding, burn rate, months until depletion)

## Done Criteria

The skill is complete when:
1. Current cap table is populated with both issued and fully diluted views
2. SAFE/note conversion is modeled for the most dilutive scenario
3. Dilution waterfall shows the impact of the proposed round on each holder class
4. Pro forma cap table post-raise is produced
5. Option pool analysis shows burn rate and months until depletion
6. Cap table hygiene checklist is reviewed and gaps are flagged

## Pitfalls

- **Tracking only issued shares instead of fully diluted**: VCs negotiate on fully diluted ownership. A founder's 25% of "issued" could be 15% fully diluted. Always maintain both views.
- **Ignoring SAFE overhang**: multiple SAFEs with different caps and discounts can produce a nasty surprise at conversion. Always model the most dilutive conversion scenario.
- **Pre-money vs post-money option pool confusion**: a pre-money pool increase hits existing holders harder than a post-money increase. Model both to understand the true impact.
- **Missing MFN and pro-rata rights**: Most Favored Nation clauses and pro-rata rights can change conversion math significantly. Track these in the shareholder register.
- **Letting the 409A go stale**: options granted below fair market value can trigger IRS penalties. Refresh the 409A every 12 months or after a material event.

## Verification

Can you answer "what is the fully diluted ownership breakdown before and after this round?" from the cap table? Are SAFE/note conversions modeled with clear conversion prices? Is the option pool burn rate tracked? If the cap table doesn't reconcile (issued vs outstanding), is the gap flagged? If not, the cap table is incomplete.

## Example

**User prompt**: "Model dilution from this term sheet."
**What should happen**: Take the current cap table, apply the term sheet terms (valuation, amount raised, option pool increase), convert SAFEs and notes based on the round price, produce a pro forma cap table showing ownership before vs after for each holder class, and calculate dilution percentages for founders, employees, and existing investors.

**User prompt**: "Convert our SAFEs / notes for the Series A."
**What should happen**: For each SAFE and convertible note, calculate the conversion price using the valuation cap, discount rate, and Series A round price, compute the number of shares each converts into, add them to the pro forma cap table, and show the impact on existing holder dilution.

## Linked Skills

- Fundraising model & valuation → `fundraising-financials`
- Term sheet terms → `term-sheet-analysis`
- Round timing & structure → `fundraising-process-management`
- Data room document storage → `data-room-management`
- Investor reporting → `investor-relations`
- Option pool + hiring plan → `headcount-and-comp-planning`
