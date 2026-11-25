# term-sheet-analysis

Term sheet analysis — economic and control terms for VC deals.

## When to Activate

- Reviewing a VC term sheet on behalf of founders or investors
- Negotiating economic terms (valuation, liquidation preference, anti-dilution)
- Evaluating control provisions (board composition, protective provisions, drag-along)
- Comparing multiple term sheets from different investors
- Advising on founder vesting and key employee equity terms
- Assessing the impact of terms on future fundraising flexibility
- Preparing for investor negotiations with data on market-standard terms

## Core Concepts

### Valuation Terms

The headline valuation determines ownership, but the details matter as much as the number:

- **Pre-money valuation**: Agreed value of the company before the investment. Determines existing shareholder dilution
- **Post-money valuation**: Pre-money + investment amount. Investor ownership = investment / post-money
- **Fully diluted basis**: Valuation per share is calculated on a fully diluted share count — includes all outstanding shares, options, warrants, and convertibles
- **Option pool**: Size and whether created pre-money or post-money is critical. A 20% pool on a pre-money basis at $20M pre-money means the operating company is effectively valued at $16M for existing shareholders
- **Price per share**: Post-money / fully diluted shares. Determines conversion ratios and sets the bar for future rounds

### Liquidation Preference

The most important economic term after valuation. Determines how proceeds are distributed before common shareholders receive anything:

- **1x non-participating**: Standard and founder-friendly. Investor gets 1x their investment back OR converts to common — whichever is higher. Aligns interests at higher exit values
- **1x participating**: Investor gets 1x back AND shares in remaining proceeds pro rata. Significantly more investor-favorable. Less common in top-tier VC deals
- **Participating with cap**: Participating up to a total return cap (e.g., 3x or 5x). Compromise position
- **Multiple preferences (2x, 3x)**: Investor gets 2x or 3x their money before common. Used in distressed or bridge rounds. Severely dilutes common shareholder returns at lower exit values
- **Stacking**: Later series typically have priority over earlier series (standard seniority) or may be pari passu

### Anti-Dilution Protection

Protects investors from future down rounds by adjusting the conversion price:

**Broad-Based Weighted Average (BBWA):**
```
New Conversion Price = Old CP * (A + B) / (A + C)
  A = Shares outstanding pre-round (fully diluted)
  B = Shares that would have been issued at Old CP for new round proceeds
  C = Shares actually issued in new round
```
- Standard market term. Adjusts proportionally based on the size and severity of the down round
- "Broad-based" means the denominator includes options and convertibles — more founder-friendly than narrow-based

**Narrow-Based Weighted Average:**
- Same formula but A includes only outstanding preferred shares (or outstanding preferred + common). More investor-favorable because the smaller denominator produces a larger adjustment

**Full Ratchet:**
- Conversion price drops to the lowest price at which new shares are issued in any subsequent round. No weighting for the number of shares issued
- Extremely punitive for founders and early investors. Rare outside distressed situations
- Even a small bridge at a lower price converts all protected shares at the new price

**Pay-to-play interaction**: Investors who do not participate in the down round may lose their anti-dilution protection

### Board Composition

The board of directors controls major corporate decisions. Composition is a critical control term:

- **Common structure at Series A**: 2 founders + 1 investor + 0 or 1 independent = 3-4 seats
- **Series B and beyond**: Boards grow; investor seats accumulate. Risk: founders lose board control even while holding majority economic ownership
- **Independent directors**: Mutually agreed by common and preferred. Serve as tiebreakers and governance anchors
- **Board observer rights**: Non-voting seat, typically for smaller investors or co-investors
- **Founder control principle**: Many top VCs support founder-controlled boards through Series B. Control flips to investors typically at later stages or upon underperformance

### Protective Provisions

Veto rights given to preferred shareholders over specific corporate actions, regardless of board composition:

- **Standard protections** (market norm — reasonable):
  - Amendment of charter/bylaws that adversely affect the preferred class
  - Issuance of senior or pari passu securities
  - Sale, merger, or dissolution of the company
  - Increase or decrease of authorized shares
  - Declaration of dividends
  - Incurrence of debt above a threshold
  - Change in the size of the board

- **Aggressive provisions** (less standard — push back):
  - Approval of annual budget or material deviations
  - Hiring/firing of CEO or key executives
  - Entry into new lines of business
  - Capital expenditure above a low threshold
  - Any contract above a specified value

### Drag-Along / Tag-Along

- **Drag-along**: If a specified majority (typically holders of majority of preferred and common, voting together) approve a sale, all shareholders must sell on the same terms. Prevents minority holdouts from blocking an exit
- **Tag-along (co-sale)**: If a founder or major shareholder sells shares, other shareholders have the right to sell a proportional amount on the same terms. Prevents founders from privately liquidating while investors remain locked in
- **Carve-outs from drag**: Typically, drag requires a minimum price or return threshold to protect against being dragged into a fire sale

### Redemption Rights

Right for preferred shareholders to require the company to repurchase their shares after a specified period (typically 5-7 years):

- **Purpose**: Provides a liquidity backstop if the company has not achieved an exit
- **Practical impact**: Most startups cannot fund redemption from cash flow. Creates leverage for investors to force a sale or recapitalization
- **Market practice**: Less common in early-stage VC. More common in growth equity and late-stage rounds
- **Accounting treatment**: Redeemable preferred may be classified as mezzanine equity or debt under GAAP — affects financial statements

### No-Shop / Exclusivity

- **No-shop clause**: Company agrees not to solicit or engage with other potential investors for a specified period (typically 30-60 days) after signing the term sheet
- **Break-up fee**: Rare in VC but occasionally included — company pays a fee if it accepts a competing offer
- **Fiduciary out**: Board retains the fiduciary duty to consider superior offers — no-shop cannot override this, but creates a practical barrier

### Founder Vesting

- **Reverse vesting**: Founders' existing shares become subject to vesting. If a founder leaves, unvested shares are repurchased at cost
- **Standard schedule**: 4 years with a 1-year cliff. Some deals credit time already served (e.g., 1 year of credit for founders who have been building for 12+ months pre-funding)
- **Acceleration**: Single trigger (100% vesting upon change of control) or double trigger (change of control + termination). Double trigger is market standard; single trigger is founder-favorable
- **Rationale**: Protects the company and investors if a founder departs early. Without vesting, a departing founder retains their full stake with no ongoing contribution

## Methodology

1. **Term extraction**: Read the term sheet line by line. Extract every economic and control term into a structured summary
2. **Market comparison**: Compare each term to market standards (NVCA model documents, recent benchmark data). Flag terms that are more aggressive or more favorable than standard
3. **Economic modeling**: Build a cap table and waterfall model reflecting the proposed terms. Compute founder and investor ownership, dilution, and proceeds at various exit values
4. **Scenario analysis**: Model downside (down round, fire sale), base case, and upside exits to understand how terms affect each stakeholder
5. **Anti-dilution impact**: Simulate a future down round — quantify the additional dilution to founders under BBWA vs. full ratchet
6. **Control analysis**: Map board composition and protective provisions. Identify which decisions the founders can make unilaterally vs. those requiring investor consent
7. **Negotiation priorities**: Rank terms by economic and strategic impact. Identify the 3-5 terms most worth negotiating and propose specific counter-offers

## Templates

### Term Sheet Comparison Matrix

```
Term                    | Investor A (Lead)    | Investor B           | Market Standard
------------------------|----------------------|----------------------|-------------------
Pre-money valuation     | $30M                 | $35M                 | N/A (deal-specific)
Investment amount       | $8M                  | $8M                  | N/A
Post-money              | $38M                 | $43M                 | N/A
Option pool (pre-money) | 15%                  | 20%                  | 10-15%
Liquidation pref        | 1x non-participating | 1x participating     | 1x non-participating
Anti-dilution           | BBWA                 | BBWA                 | BBWA
Board seats             | 2 founder, 1 inv, 1 ind | 2 founder, 2 inv  | 2F + 1I + 1 ind
Protective provisions   | Standard NVCA        | Standard + budget    | Standard NVCA
Founder vesting         | 4yr, 1yr cliff, 1yr credit | 4yr, 1yr cliff, no credit | 4yr, 1yr cliff
Pro rata rights         | Major investors      | All investors        | Major investors
No-shop                 | 45 days              | 60 days              | 30-45 days
Drag-along              | Majority preferred + common | Majority preferred | Common + preferred
```

### Anti-Dilution Simulation

```
Current Round: Series A at $5.00/share, 2M shares
Down Round: Series B at $3.00/share, 1.5M shares

Broad-Based Weighted Average:
  Pre-round fully diluted shares:    10,000,000
  Shares at old price ($5):          1,500,000 * $3 / $5 = 900,000
  Shares actually issued:            1,500,000

  New CP = $5.00 * (10M + 900K) / (10M + 1.5M) = $5.00 * 0.948 = $4.74
  Additional shares to Series A:     (2M * $5 / $4.74) - 2M = 109,705 shares
  Dilution to common:                ~1.0% additional

Full Ratchet:
  New CP = $3.00 (drops to new round price)
  Additional shares to Series A:     (2M * $5 / $3) - 2M = 1,333,333 shares
  Dilution to common:                ~11.5% additional

Impact: Full ratchet creates 12x more dilution than BBWA in this scenario.
```

### Founder Proceeds at Various Exit Values

```
Assumptions: $8M Series A, 1x NP preferred, 21% investor ownership, 2 founders at 30% each

Exit ($M)  | Series A    | Founder 1   | Founder 2   | Others/Pool
-----------|-------------|-------------|-------------|------------
$10M       | $8.0M (pref)| $0.6M       | $0.6M       | $0.8M
$25M       | $5.3M (conv)| $7.5M       | $7.5M       | $4.8M
$50M       | $10.5M(conv)| $15.0M      | $15.0M      | $9.5M
$100M      | $21.0M(conv)| $30.0M      | $30.0M      | $19.0M
$250M      | $52.5M(conv)| $75.0M      | $75.0M      | $47.5M

Conversion threshold: $38.1M ($8M / 21%)
Below $38.1M: Series A takes preference, founders get residual
Above $38.1M: Series A converts, everyone shares pro rata
```

## Quality Gate

- [ ] Every economic term extracted and compared to market standards
- [ ] Pre-money / post-money arithmetic verified, including option pool impact on effective valuation
- [ ] Liquidation preference structure modeled in waterfall at 5+ exit values
- [ ] Anti-dilution type identified and simulated for a hypothetical down round
- [ ] Board composition analyzed — identify at which point founders lose control
- [ ] Protective provisions reviewed against NVCA standard; aggressive provisions flagged
- [ ] Drag-along and tag-along provisions checked for minimum price thresholds
- [ ] Founder vesting terms reviewed: schedule, cliff, credit for past service, acceleration triggers
- [ ] Pro rata rights and information rights documented
- [ ] No-shop period and exclusivity terms assessed for reasonableness
- [ ] Redemption rights (if present) analyzed for financial feasibility and accounting impact
- [ ] Negotiation priorities ranked by economic impact with specific counter-proposals drafted
