---
name: capital-gains
description: "Use when you are thinking about selling an investment property and want an indicative picture of the capital gain, the likely CGT, and your net proceeds — ready to take to a registered tax agent."
---

# Skill — Capital Gains / Sale Planner

**Stage:** 3 — Stress-Test (or Decide)
**Hook:** Before you sell, model the tax. The headline sale price is not what you keep.
**Use when:** You are thinking about selling an investment property and want an indicative picture of the capital gain, the likely CGT, and your net proceeds — ready to take to a registered tax agent.

---

## Purpose

This skill models the indicative tax position of selling an Australian investment property. It builds the cost base, works out the gross capital gain, tests CGT discount eligibility, estimates CGT per owner at each owner's marginal rate, and lands on an estimated net-proceeds figure after selling costs and tax.

All outputs are assumptions and estimates. This is preparation for a conversation with your registered tax agent — not a tax calculation you can rely on, and not a determination of any exemption.

---

## Reads from

- Property File: SNAPSHOT, PURCHASE DETAILS (price, date, buying costs)
- Property File: CAPITAL IMPROVEMENTS log (if maintained)
- Investor Profile: ownership structure, each owner's marginal tax rate, main-residence history

## Writes to

- Property File: SALE PLAN (cost base, estimated gain, estimated CGT, net proceeds estimate)

---

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PURCHASE PRICE: $[amount]
PURCHASE DATE: [DD/MM/YYYY] (determines the > 12-month CGT discount test)
SALE PRICE: $[amount or indicative estimate] (label unverified if it is an estimate, not a signed contract)
BUYING COSTS: $[stamp duty + legal/conveyancing + other acquisition costs]
CAPITAL IMPROVEMENTS: $[cost of capital improvements made — cost-base additions, not repairs]
SELLING COSTS: $[agent commission + marketing + legal/conveyancing on sale]
OWNERSHIP STRUCTURE + SPLIT: [e.g. 50/50 tenants in common / sole owner / company / trust]
MAIN RESIDENCE?: [never / yes — which periods it was your main residence]
HELD > 12 MONTHS?: [yes / no] (from purchase date to sale contract date)
EACH OWNER'S MARGINAL TAX RATE: [e.g. Owner A 37%, Owner B 32.5%]
```

---

## How the numbers are worked out

Use these explicit formulas so two people modelling the same sale get the same result:

```
cost base            = purchase price + buying costs + capital improvements + selling costs
gross capital gain   = sale price − cost base
discounted gain      = gross gain × 50%        (only if the individual held the asset > 12 months)
taxable gain (owner) = discounted gain × ownership share
estimated CGT (owner)= taxable gain (owner) × that owner's marginal rate  (+ optional 2% Medicare levy)
```

- **CGT discount:** the CGT discount rate, the holding-period test, and which owner types qualify are set by legislation and **have been subject to reform — do not assume the historical "50% after 12 months" rule still applies.** Do NOT hard-code a discount percentage. Instead: state the owner type (individual / trust / company / SMSF) and the purchase-to-sale holding period, then flag that the **current-year CGT discount treatment must be confirmed with a registered tax agent**. Model and clearly label the **no-discount (full gross gain)** case as the conservative baseline, and note the discounted case only as "subject to the current discount rules — verify".
- **2026 reform (verify current-year rules):** Australia's 2026 Budget legislated that from **1 July 2027** the 50% CGT discount for individuals and trusts is **replaced by cost-base indexation** plus a **30% minimum tax** on gains, and only applies to gains arising after that date (companies/super funds excluded; new residential dwellings may choose). Until **30 June 2027** the existing 50%/12-month rule still applies. State which regime is in play for the disposal date and send the taxpayer to a registered tax agent — do not hard-code either. **Check it live:** if you have web access at run time, confirm the current-year CGT discount treatment at ato.gov.au (and budget.gov.au / Treasury for announced changes) before quoting any rate — do not rely on training-data recall for tax law.
- **Capital improvements vs repairs:** only genuine capital improvements add to the cost base. Repairs and maintenance already claimed as deductions do not. Flag anything ambiguous for the tax agent.
- **Main-residence exemption:** if the property was ever your main residence, the gain may be reduced or fully exempt. A partial/pro-rata exemption can apply when it was rented for part of the ownership period, and the **"6-year rule"** may let it stay exempt for up to six years of renting after you move out. **Do not compute the exemption here** — flag it as verify-with-tax-agent. Model the non-exempt case and clearly label it.
- **Medicare levy:** add the 2% Medicare levy to the marginal rate as an optional extra if relevant. Note it is an estimate, not tax advice.

**Benchmark ranges** (typical AU estimate — verify with your agent, conveyancer, and tax agent; do not treat as fact):

| Cost item | Typical range | Note |
|---|---|---|
| Agent commission | ~1.5%–2.5% of sale price | Varies by state and agent — verify |
| Marketing / campaign | ~$3,000–$10,000+ | Varies by campaign and price point — verify |
| Selling costs combined | ~2%–3.5% of sale price | Commission + marketing rule of thumb — verify |
| Legal / conveyancing (sale) | ~a few hundred–low thousands | Varies by state and firm — verify |

**Worked example:** Bought for $600,000 with $30,000 buying costs, added $20,000 in capital improvements, selling for $800,000 with $24,000 selling costs. Cost base = 600,000 + 30,000 + 20,000 + 24,000 = **$674,000**. Gross gain = 800,000 − 674,000 = **$126,000**. Held > 12 months, individual, so discounted gain = 126,000 × 50% = **$63,000**. Sole owner at 37% → estimated CGT ≈ 63,000 × 0.37 ≈ **$23,310**. (illustration only — verify every input)

---

## Output contract

Return exactly these 6 sections. Every number is labelled an estimate to verify.

### 1. COST BASE BUILD-UP
Show the cost base as a table so each component is visible and checkable.

| Component | Amount | Source |
|---|---|---|
| Purchase price | $X | User input |
| Buying costs (stamp duty, legal) | $X | User input — verify |
| Capital improvements | $X | User input — verify capital vs repair with tax agent |
| Selling costs (commission, marketing, legal) | $X | Estimate — verify |
| **Cost base (total)** | **$X** | Calculated |

### 2. GROSS CAPITAL GAIN
- Sale price (label as estimate if not a signed contract)
- Less: cost base (from section 1)
- = **Gross capital gain (estimate)**
- Note if this is a capital loss instead (gain is negative) — a loss cannot be discounted and may be carried forward; verify with your tax agent.

### 3. CGT DISCOUNT ELIGIBILITY
- Held > 12 months? [yes/no] — and what that means here
- Owner type: individual / trust (may get 50% discount) vs company (no 50% discount)
- Discounted gain = gross gain × 50% (if eligible), otherwise full gross gain
- State clearly: this is an eligibility estimate, not a determination — confirm with your tax agent.

### 4. ESTIMATED CGT BY OWNER
One row per owner, using their ownership share and marginal rate.

| Owner | Share | Taxable gain (share of discounted gain) | Marginal rate | Estimated CGT | + 2% Medicare (optional) |
|---|---|---|---|---|---|
| Owner A | X% | $X | X% | $X | $X |
| Owner B | X% | $X | X% | $X | $X |
| **Total** | 100% | $X | — | **$X** | **$X** |

All figures are estimates to verify with a registered tax agent.

### 5. NET PROCEEDS AFTER SELLING COSTS & CGT
- Sale price (estimate)
- Less: loan payout (if supplied — otherwise flag as a figure to confirm with your lender)
- Less: selling costs (commission, marketing, legal)
- Less: estimated CGT (total from section 4)
- = **Estimated net proceeds (before any main-residence exemption)**
- Reminder: a main-residence exemption, if it applies, could materially increase this — your tax agent determines that.

### 6. TIMING & QUESTIONS FOR YOUR TAX AGENT
- **Timing:** the CGT event is generally the **contract date**, not settlement — this can change which financial year the gain falls in. Note whether selling before/after 30 June, or holding just past the 12-month mark, could change the position. Flag as a question, not advice.
- Questions to ask:
  - "Do I qualify for the main-residence exemption for any period, and does the 6-year rule apply to me?"
  - "Which of my improvement costs count toward the cost base, and which were already deducted?"
  - "How does the contract date affect which financial year this gain is taxed in?"
  - "Do I have any carried-forward capital losses that offset this gain?"
  - "How does my ownership structure change the CGT outcome?"

---

## Safety boundaries

- Never present CGT as a definitive figure — it is always an estimate to verify with a registered tax agent
- Never determine the main-residence exemption yourself — flag it for the tax agent and model the non-exempt case
- Never assume a sale price — if it is not a signed contract, label it an estimate and say so in the output
- Never treat repairs as cost-base additions — only genuine capital improvements, and flag ambiguous items
- CGT law and rates change — always verify current rules with the ATO or a registered tax agent
- Never suggest this output replaces professional tax advice

---

## Pairs with

- [Tax Year Prep](tax-year-prep.md) — get your records CGT-ready before you sell
- [Accountant Prep](accountant-prep.md) — take this estimate to a registered tax agent
- [Property Appraisal](property-appraisal.md) — pressure-test the sale-price estimate
- [Portfolio Review](portfolio-review.md) — how does selling affect the whole portfolio?

---

## Disclaimer

> **NOT TAX ADVICE.** This output is general information and educational preparation only. Every capital gain, CGT figure, and net-proceeds number here is an assumption or estimate — not a tax calculation you can rely on. This skill does not determine the main-residence exemption, the 6-year rule, or any other exemption or concession — only a registered tax agent can. CGT law, rates, and thresholds change; verify current rules with the ATO and a registered tax agent before acting. See [disclaimers/not-tax-advice.md](../disclaimers/not-tax-advice.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
