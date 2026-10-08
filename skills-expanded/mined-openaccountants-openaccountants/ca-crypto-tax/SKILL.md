---
name: ca-crypto-tax
description: "> Use this skill whenever asked about Canadian cryptocurrency taxation. Trigger on phrases like \"crypto tax Canada\", \"CRA crypto\", \"Bitcoin capital gains Canada\", \"crypto business income CRA\", \"adjusted cost base crypto\", \"ACB crypto\", \"mining tax Canada\", \"staking tax Canada\", \"GST HST crypto\", \"crypto inclusion rate Canada\", or any question about how cryptocurrency is taxed by the CRA. This skill covers capital gains vs business income treatment, the 50% inclusion rate, ACB tracking, mining/staking as business income, GST/HST on crypto payments, and record-keeping requirements. ALWAYS read this skill before touching any Canadian crypto tax work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: CA
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ca-crypto-tax"
  tax_year: 2025
  obligation: CRYPTO
---

# Canada Crypto Tax -- Capital Gains & Business Income Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | Canada |
| Tax | Income Tax -- Cryptocurrency / Digital Assets |
| Currency | CAD (all gains/income reported in CAD) |
| Tax year | 1 January -- 31 December 2025 |
| Primary legislation | Income Tax Act (Canada), Sections 3, 9, 38, 39, 54 |
| Supporting guidance | CRA Guide T4037 (Capital Gains); IT-479R (archived -- Transactions in Securities); CRA crypto guidance page |
| Tax authority | Canada Revenue Agency (CRA) |
| Filing portal | CRA My Account / NETFILE / paper T1 |
| Filing deadline | 30 April 2026 (15 June 2026 if self-employed; balance due 30 April) |
| Skill version | 1.0 |

### Core Principle

The CRA treats cryptocurrency as a **commodity** (not currency). Dispositions result in either a capital gain or business income depending on the taxpayer's circumstances.

### Capital Gains Inclusion Rate (2025)

| Taxpayer | Inclusion Rate | Notes |
|---|---|---|
| Individuals -- first $250,000 of net capital gains | 50% | Standard inclusion |
| Individuals -- gains above $250,000 | 66.67% | Effective for dispositions after 24 June 2024 |
| Corporations and trusts | 66.67% on all gains | No $250K threshold |

**Important:** The increase to 66.67% above $250K was announced in Budget 2024 and received Royal Assent. Verify current enforcement status as implementation details evolved through 2024-2025.

### Federal Tax Rates (2025)

| Taxable Income (CAD) | Rate |
|---|---|
| 0 -- 57,375 | 15% |
| 57,376 -- 114,750 | 20.5% |
| 114,751 -- 158,468 | 26% |
| 158,469 -- 220,000 | 29% |
| 220,001+ | 33% |

### Conservative Defaults

| Ambiguity | Default |
|---|---|
| Unknown whether capital or business income | Treat as capital gains (lower inclusion) until evidence of business activity |
| Unknown ACB | $0 (maximum gain) -- obtain records |
| Unknown acquisition date | No holding period benefit claimed |
| Unknown fair market value at acquisition | Use reputable exchange rate at date/time |

---

## Section 2 -- Classification Rules

### 2.1 Capital Gains vs Business Income

| Factor | Capital (Investor) | Business Income (Trader) |
|---|---|---|
| Frequency of transactions | Occasional | High volume, systematic |
| Holding period | Extended (weeks/months/years) | Very short (minutes/hours/days) |
| Knowledge/expertise | General interest | Deep market knowledge, technical analysis |
| Time devoted | Part-time/casual | Significant daily commitment |
| Financing | Own capital | Leveraged/borrowed funds |
| Advertising/promotion | None | May promote activity |
| Nature of assets | Long-term hold for appreciation | Quick turnover for profit |
| Tax treatment | 50% (or 66.67%) inclusion | 100% income (fully taxable) |
| Loss treatment | Capital losses (only offset gains) | Business losses (offset all income) |

The CRA applies a holistic test. No single factor is determinative.

### 2.2 Disposition Events

A disposition occurs when:

| Event | Disposition? |
|---|---|
| Sell crypto for CAD (or fiat) | Yes |
| Trade crypto for another crypto | Yes -- barter transaction |
| Use crypto to purchase goods/services | Yes -- at FMV |
| Gift crypto | Yes -- deemed disposition at FMV |
| Donate crypto to registered charity | Yes -- but donation receipt at FMV; no capital gain if donated to qualified donee (proposed) |
| Transfer between own wallets | No -- same beneficial owner |
| Death of taxpayer | Yes -- deemed disposition at FMV |

### 2.3 Adjusted Cost Base (ACB) Tracking

The ACB is calculated using the **weighted average cost method** (mandatory for identical properties under ITA s. 47):

ACB per unit = Total cost of all units acquired ÷ Total units held

| Element Included in ACB | Example |
|---|---|
| Purchase price in CAD | Amount paid on exchange |
| Transaction/exchange fees on purchase | Coinbase fee, spread cost |
| Transfer fees (incoming) | Network/gas fees to acquire |

When a partial disposition occurs:
- Proceeds of disposition = FMV in CAD at time of sale
- ACB of disposed units = (Total ACB ÷ total units) × units sold
- Capital gain/loss = Proceeds − ACB of disposed units − disposition costs

### 2.4 Superficial Loss Rule (ITA s. 40(2)(g)(i))

If you sell crypto at a loss and repurchase the same crypto (or identical property) within 30 days before or after the sale (or your affiliated person acquires it), the loss is **denied**. The denied loss is added to the ACB of the repurchased property.

### 2.5 Staking Rewards

| Treatment | Detail |
|---|---|
| CRA position | Business income or property income (assessable when received) |
| Amount | FMV in CAD at date/time of receipt |
| ACB of received tokens | FMV at receipt (becomes cost base for future disposition) |
| If part of active business | Report on T2125 (business income) |
| If passive/property income | Report as other income (Line 13000) |

### 2.6 Mining

| Scenario | Treatment |
|---|---|
| Hobby mining (small-scale, no profit intent) | Acquired at $0 ACB; CGT on disposition |
| Business mining (significant operations) | Business income at FMV when mined; expenses deductible; GST/HST registrant obligations |

### 2.7 Airdrops and Hard Forks

| Type | Treatment |
|---|---|
| Airdrop (no consideration given) | CRA: income at FMV if received for services or as reward; otherwise $0 ACB |
| Hard fork (new token from existing chain) | $0 ACB; taxable on disposition |
| Airdrop requiring action (governance, claim) | Income at FMV if value exists |

### 2.8 GST/HST on Crypto

| Transaction | GST/HST Implication |
|---|---|
| Purchasing crypto with fiat | No GST/HST (financial instrument) |
| Selling crypto for fiat | No GST/HST |
| Using crypto to purchase taxable goods/services | GST/HST applies to the goods/services (crypto is consideration) |
| Mining/staking as business -- selling mined crypto | Exempt financial service (no GST/HST on sale of crypto itself) |
| Mining/staking as business -- input costs | ITC may be restricted (financial services supplier rules) |
| Crypto exchange services (platform fees) | Subject to GST/HST as a taxable supply |

---

## Section 3 -- Transaction Pattern Library

### 3.1 Common Exchange Patterns (Canadian Exchanges)

| Pattern | Treatment | Notes |
|---|---|---|
| NEWTON BUY / SHAKEPAY BUY | Acquisition | ACB = CAD paid + spread (no explicit fee on some platforms) |
| BITBUY PURCHASE / COINSMART BUY | Acquisition | ACB = CAD paid + any trading fee |
| KRAKEN BUY (CAD pair) | Acquisition | ACB = CAD equivalent + fee |
| WEALTHSIMPLE CRYPTO BUY | Acquisition | ACB = CAD paid + spread |
| SELL ORDER (any exchange) | Disposition | Proceeds = CAD received |
| CONVERT / SWAP / TRADE | Disposition + acquisition | Two legs: dispose of A, acquire B |
| CAD WITHDRAWAL | Not taxable | Already sold |
| CAD DEPOSIT | Not taxable | Funding account |

### 3.2 Income Events

| Pattern | Treatment | Notes |
|---|---|---|
| STAKING REWARD | Income (business or property) | FMV at receipt |
| MINING PAYOUT | Income (if business) or $0 ACB (if hobby) | Determine mining scale |
| REFERRAL BONUS (crypto) | Income | FMV at receipt |
| EARN / LENDING INTEREST | Income (property income) | FMV at receipt |
| CASHBACK REWARD (crypto) | Income | FMV at receipt |

### 3.3 Non-Taxable Movements

| Pattern | Treatment | Notes |
|---|---|---|
| TRANSFER TO COLD WALLET | No tax event | Same beneficial owner |
| TRANSFER BETWEEN EXCHANGES | No tax event | Network fees add to ACB or deductible expense |
| FIAT DEPOSIT / WITHDRAWAL | No tax event | Cash movement |

---

## Section 4 -- Computation Method

### Step 1: Classify Activity
Determine if taxpayer is investor (capital gains) or trader (business income).

### Step 2: Build ACB Ledger
Track every acquisition: weighted average cost across all units of each crypto.

### Step 3: Calculate Gain/Loss per Disposition
Proceeds (CAD FMV) − ACB of disposed units − selling costs = gain or loss.

### Step 4: Check Superficial Loss Rule
Deny any loss where same crypto was reacquired within 30-day window.

### Step 5: Apply Inclusion Rate
- Capital gains: 50% on first $250K; 66.67% on excess (individuals)
- Business income: 100% taxable

### Step 6: Report Staking/Mining/Airdrop Income
Separately from capital gains -- as business or property income.

### Step 7: File
- Capital gains: Schedule 3
- Business income: T2125 (Statement of Business Activities)
- Other income: Line 13000

---

## Section 5 -- Record-Keeping Requirements

CRA requires:

| Record | Mandatory |
|---|---|
| Date and time of each transaction | Yes |
| Type of transaction (buy/sell/trade/transfer) | Yes |
| Amount of crypto involved | Yes |
| FMV in CAD at time of transaction | Yes |
| Exchange or platform used | Yes |
| Wallet addresses involved | Yes |
| Running ACB calculation | Yes |
| Purpose of transaction | Yes |

Retention: 6 years from the end of the tax year to which they relate.

---

## Section 6 -- Edge Cases

### 6.1 Crypto-to-Crypto Swaps
Each swap is a barter transaction. The disposition of crypto A is at the FMV of crypto B received (or FMV of A given up, whichever is more readily determinable). Must calculate gain/loss on A and establish ACB for B.

### 6.2 DeFi Lending
Lending crypto to a DeFi protocol may be a disposition (if legal ownership transfers to the protocol). Conservative treatment: disposition at FMV when deposited, reacquisition when withdrawn. Interest/yield received is property income.

### 6.3 NFTs
Treated the same as other crypto assets. Acquisition = ACB. Sale = disposition. If creating NFTs as a business, profits are business income.

### 6.4 Wrapped Tokens
Wrapping (e.g., ETH → WETH) is a grey area. Conservative treatment: disposition of ETH, acquisition of WETH at same FMV. No gain/loss but must track separately.

### 6.5 Emigration from Canada
Deemed disposition of all crypto at FMV on departure date (ITA s. 128.1). Capital gains tax applies on departure.

### 6.6 Death
Deemed disposition at FMV immediately before death. Capital gains included in terminal return. Beneficiary acquires at FMV as their ACB.

---

## Section 7 -- Prohibitions

- NEVER apply the 50% inclusion rate to all gains without checking the $250,000 threshold
- NEVER use specific identification method for identical properties -- CRA requires weighted average (ITA s. 47)
- NEVER ignore the superficial loss rule for repurchases within 30 days
- NEVER treat crypto-to-crypto swaps as non-events -- each swap is a disposition
- NEVER claim business losses without substantiating that the activity is a business (not capital)
- NEVER ignore GST/HST obligations for crypto businesses
- NEVER assume airdrops are always tax-free -- determine if income character exists
- NEVER omit staking/mining income -- it is taxable when received
- NEVER present tax calculations as definitive -- always label as estimated

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, CGA, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ca-crypto-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
