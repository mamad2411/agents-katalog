# rating-methodologies

Credit rating methodologies — S&P, Moody's, Fitch approaches.

## When to Activate

- Assessing a company's likely credit rating or rating trajectory
- Preparing for a rating agency engagement or annual review
- Understanding the impact of a transaction (M&A, debt issuance, recap) on credit ratings
- Analyzing the difference between ratings from multiple agencies (split ratings)
- Evaluating subordination and structural considerations for instrument-level ratings (notching)
- Benchmarking financial ratios against rating category medians
- Advising on actions to achieve or maintain a target rating

## Core Concepts

### Rating Scales

**Investment Grade vs. High Yield:**

```
Quality        S&P       Moody's     Fitch      Category
Highest        AAA       Aaa         AAA        Investment Grade
High           AA+/AA/AA- Aa1/Aa2/Aa3 AA+/AA/AA- Investment Grade
Upper Medium   A+/A/A-   A1/A2/A3    A+/A/A-   Investment Grade
Medium         BBB+/BBB/BBB- Baa1/Baa2/Baa3 BBB+/BBB/BBB- Investment Grade
---threshold---
Speculative    BB+/BB/BB- Ba1/Ba2/Ba3 BB+/BB/BB- High Yield
Highly Spec.   B+/B/B-   B1/B2/B3    B+/B/B-   High Yield
Substantial    CCC+/CCC  Caa1/Caa2   CCC       High Yield
Default        D/SD      Ca/C        D/RD      Default
```

- The BBB-/Baa3 to BB+/Ba1 boundary is the critical threshold — crossing it (fallen angel) triggers forced selling by investment-grade-only mandates
- Modifiers (+/-, 1/2/3) indicate relative standing within a category

### S&P Methodology

S&P's corporate rating framework combines business risk and financial risk:

**Business Risk Profile (BRP):**
1. **Industry risk**: Cyclicality, competitive dynamics, regulatory environment, growth prospects (scored 1-6)
2. **Country risk**: Sovereign rating, economic stability, institutional framework
3. **Competitive position**: Market share, scale, diversification, operating efficiency, profitability

BRP scale: Excellent, Strong, Satisfactory, Fair, Weak, Vulnerable

**Financial Risk Profile (FRP):**
- Core ratios: FFO/Debt, Debt/EBITDA, FFO/Interest, FOCF/Debt
- S&P adjusts reported figures for operating leases, pensions, hybrid instruments, receivables securitization
- FRP scale: Minimal, Modest, Intermediate, Significant, Aggressive, Highly Leveraged

**Anchor rating**: Combination of BRP and FRP on a matrix produces the anchor (starting point)

**Modifiers** (each can adjust up/down 1-2 notches):
- Diversification/portfolio effect
- Capital structure (debt maturity, currency, interest rate mix)
- Financial policy (management's stated leverage target, track record)
- Liquidity (adequate, strong, exceptional — or less than adequate)
- Management and governance
- Comparable rating analysis (final calibration versus peers)

**Group/parent influence**: Subsidiary ratings adjusted for group credit profile, strategic importance, and support likelihood

### Moody's Methodology

Moody's uses industry-specific scorecards combining quantitative and qualitative factors:

**Quantitative factors** (typically 60-70% weight):
- Scale (revenue)
- Profitability (EBITDA margin, operating margin)
- Leverage (Debt/EBITDA, FFO/Debt)
- Coverage (EBIT/Interest, FFO/Interest)
- Cash flow (RCF/Net Debt, FCF/Debt)

**Qualitative factors** (typically 30-40% weight):
- Business profile (market position, barriers to entry)
- Revenue diversity (geographic, product, customer)
- Regulatory/event risk
- Financial policy (tolerance for leverage, acquisition strategy, shareholder returns)

**Grid-indicated rating**: The scorecard output — a starting point subject to further judgment

**Adjustments from grid-indicated to actual rating:**
- Ownership structure (private equity ownership often weighs negatively — aggressive financial policy assumed)
- Event risk (pending M&A, litigation, regulatory action)
- Liquidity profile
- Structural considerations (priority of claims)

### Key Financial Ratios by Rating Level

Approximate medians for non-financial corporates (varies by industry):

```
Metric              AAA    AA     A      BBB    BB     B      CCC
FFO/Debt            >60%   45-60% 30-45% 20-30% 12-20% 5-12%  <5%
Debt/EBITDA         <1.0x  1.0-1.5x 1.5-2.5x 2.5-3.5x 3.5-5.0x 5.0-7.0x >7.0x
FFO/Interest        >15x   10-15x 6-10x  4-6x   2.5-4x 1.5-2.5x <1.5x
FOCF/Debt           >30%   20-30% 15-20% 10-15% 5-10%  0-5%   <0%
```

These are indicative — actual thresholds differ by industry (e.g., utilities tolerate higher leverage, tech companies are expected to have lower leverage).

### Notching (Subordination)

Instrument-level ratings are notched from the issuer rating based on priority of claims and recovery expectations:

- **Senior secured**: May be notched up 1-2 notches from the issuer rating (higher recovery)
- **Senior unsecured**: Typically equal to the issuer rating for investment-grade; may be notched down for high-yield issuers with significant secured debt
- **Subordinated debt**: Notched down 1-2 notches
- **Junior subordinated / hybrid**: Notched down 2-4 notches (including equity content adjustment)
- **Recovery ratings**: S&P assigns recovery ratings (1+ through 6) estimating recovery in a hypothetical default scenario

**Structural subordination**: Debt at a holding company is structurally subordinated to debt at operating subsidiaries — cash flows must service opco debt before reaching the holdco

### Outlook and CreditWatch

- **Outlook (Positive, Stable, Negative)**: Indicates the direction of a potential rating change over the medium term (typically 12-24 months). Not a certainty
- **CreditWatch / Review for Upgrade or Downgrade**: Indicates a near-term potential rating action, usually resolved within 90 days. Triggered by a specific event (M&A announcement, earnings miss, regulatory change)
- **Rating affirmation**: Rating confirmed after review — important data point that the agency considered new information and maintained the rating

### Split Ratings

When agencies assign different ratings to the same issuer:

- Common causes: Different methodological emphasis, different adjustment conventions, timing of review, qualitative judgment
- Market convention: Use the lower of two ratings, or the middle of three, for regulatory and index purposes
- Narrow split (one notch): Not unusual and typically not concerning
- Wide split (two+ notches): Investigate the specific factors driving divergence — may reveal a risk that one agency emphasizes more

## Methodology

1. **Identify the relevant methodology**: Each agency publishes sector-specific rating criteria. Download and reference the correct methodology for the industry
2. **Adjust financial statements**: Apply agency-specific adjustments (operating leases, pensions, hybrids, securitizations, captive finance)
3. **Calculate key ratios**: Compute the ratios used in the scoring grid, using the agency's definitions
4. **Assess qualitative factors**: Score business risk, competitive position, management, governance, financial policy
5. **Derive the grid-indicated or anchor rating**: Apply the scoring matrix
6. **Apply modifiers and notch adjustments**: Consider diversification, liquidity, financial policy, group support, structural subordination
7. **Benchmark against rated peers**: Compare the subject's profile to similarly rated companies in the same sector
8. **Sensitivity analysis**: Model how a rating would change under different financial scenarios (deleveraging plan, acquisition, dividend policy change)

## Templates

### Rating Assessment Summary

```
Company: [Name]               Sector: [Industry]
Current Rating: BBB / Baa2    Outlook: Stable / Stable

S&P Framework:
  Business Risk Profile: Satisfactory (Strong competitive position, moderate industry risk)
  Financial Risk Profile: Intermediate
  Anchor: bbb
  Modifiers:
    Diversification: 0 (neutral)
    Capital structure: 0
    Financial policy: -1 (acquisitive strategy, tolerance for temporary leverage spikes)
    Liquidity: +1 (strong — $500M undrawn RCF, no near-term maturities)
    Management/governance: 0
  Indicative Rating: BBB (stable)

Key Ratios vs. BBB Medians:
  Metric              Company   BBB Median   Position
  FFO/Debt            28%       25%          Above median
  Debt/EBITDA         3.1x      3.0x         At median
  FFO/Interest        5.5x      5.0x         Above median
  FOCF/Debt           12%       12%          At median
```

### Rating Impact Analysis (M&A Scenario)

```
Scenario: Acquisition of [Target] for $800M (60% debt funded)

                        Pre-Deal    Pro Forma   Recovery (Y2)
Revenue                 $2,500M     $3,200M     $3,400M
EBITDA                  $500M       $620M       $700M
Net Debt                $1,200M     $1,800M     $1,550M
Net Debt / EBITDA       2.4x        2.9x        2.2x
FFO / Debt              32%         24%         30%
FFO / Interest          6.0x        4.2x        5.0x

Current Rating:         BBB+
Expected Post-Close:    BBB- (negative outlook)
Expected Recovery:      BBB (stable) within 18-24 months

Mitigants: Synergies ($50M run-rate), asset disposals ($200M), no dividends during recovery
Risk: Rating downgrade to BB+ if integration delays or synergies underperform by >30%
```

### Notching Table

```
Instrument                      | Recovery | Notch from ICR | Instrument Rating
Senior Secured Term Loan A      | 1+ (95%) | +1             | BBB+
Senior Secured Term Loan B      | 1 (90%)  | +1             | BBB+
Senior Unsecured Notes          | 3 (55%)  | 0              | BBB
Subordinated Notes              | 5 (15%)  | -2             | BB+
Junior Subordinated / Hybrid    | 6 (5%)   | -3             | BB
```

## Quality Gate

- [ ] Correct agency methodology identified and applied for the sector
- [ ] Financial statements adjusted using agency conventions (leases, pensions, hybrids, off-balance-sheet)
- [ ] Key ratios calculated on the agency's definitions and compared to published medians
- [ ] Business risk / qualitative factors assessed with supporting evidence
- [ ] Grid-indicated or anchor rating derived and modifiers applied with justification
- [ ] Notching applied correctly for each instrument based on priority of claims and recovery analysis
- [ ] Peer comparison completed against similarly rated companies in the same sector
- [ ] Split rating analysis performed if multiple agency ratings differ
- [ ] Outlook and CreditWatch status incorporated into the assessment
- [ ] Sensitivity analysis models rating impact under at least two scenarios (upside, downside)
- [ ] Rating agency engagement timeline tracked (annual review date, expected actions)
