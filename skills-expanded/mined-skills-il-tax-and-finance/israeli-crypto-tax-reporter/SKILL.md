---
name: israeli-crypto-tax-reporter
description: Calculate cryptocurrency capital gains tax per Israeli Tax Authority (Reshut HaMisim) rules and generate capital-gains reporting data and Form 1399י advance-payment data (within 30 days of each sale). Use when a user needs to compute crypto tax using FIFO cost basis, classify DeFi income (staking, liquidity mining, airdrops), prepare annual filing data, understand advance payment (mikdamot) and reporting duties, or handle unreported crypto from past years now that the Voluntary Disclosure Procedure (Nohal Gilui Mirtzon) has closed. Covers Section 88 of the Income Tax Ordinance, Circular 2018/05, the 25% capital gains ceiling for individuals, and the surtax (3% above NIS 721,560, plus 2% on capital income that itself exceeds it; frozen through 2027). Do NOT use for non-Israeli tax jurisdictions, general income tax calculations, or VAT (maam) on crypto business activities, which require separate professional consultation.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Python 3.8+ for calculator script
---

# Israeli Crypto Tax Reporter

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.

The Voluntary Disclosure Procedure is a process in which you hand the Tax Authority information about your own past reporting, and it concerns criminal exposure: while the procedure is open it may confer immunity from criminal proceedings, and once it has closed such an approach is an admission with no immunity. This tool does not test your eligibility for the procedure, does not examine the full extent of your years and documents, and does not decide whether you should apply. Whether to apply, on which track and at what time is a legal question, and legal advice and legal opinions are reserved by law to a licensed advocate. Consult a tax-specialist lawyer before lodging a voluntary-disclosure application or a corrected return under Section 131, even if the deadline is close.


## Instructions

### Step 1: Understand the Israeli Crypto Tax Framework

Before performing any calculations, ensure you understand the key regulatory principles:

**Core legal basis:**
- Cryptocurrency is classified as an **asset** (neches) under Section 88 of the Income Tax Ordinance (Pekudat Mas Hachnasa), not as currency.
- Gains from selling crypto are taxed as **capital gains** (revach hon) under Chapter E of the Ordinance.
- **Circular 05/2018**, "מיסוי פעילות באמצעי תשלום מבוזר", dated 17 January 2018, is the primary ITA guidance and remains in force.

**Tax rates:**
- **Individuals**: up to 25% on the real gain, under Section 91(b)(1). **25% is a ceiling, not a flat rate**: the gain is taxed under s.121 as the top layer of income, capped at 25%. From age 60 the s.121(b)(1) brackets (10%, 14%, 20%) can make it lower when total income is modest, and s.91(e)(1) lets the real gain be spread over up to four tax years (or the ownership period, if shorter) at the taxpayer's request. A lot acquired before 1.1.2012 (bitcoin bought 2009-2011) splits its real gain by days under s.91(b1): the part up to 31.12.2011 at no more than 20%.
- **The 30% rate almost certainly does NOT apply to ordinary tokens.** Section 91(b)(2) charges up to 30% on the sale of a **"נייר ערך בחבר-בני-אדם"**, a security in a body corporate, by a material shareholder. A fungible token is not one, and Circular 05/2018 never invokes 91(b)(2). Do not apply 30% just because the holder owns a large stake in a project; an equity-like token in an incorporated entity is a question for a CPA or a pre-ruling.
- **Business/traders**: If crypto activity constitutes a business (esek), gains are taxed as ordinary income at marginal rates (up to 47%, plus the surtax) instead of the 25% capital rate. This is the single highest-stakes determination in crypto tax. Circular 05/2018 does NOT enumerate the test: section 3.1.4 says only that classification "ייקבע בהתאם למבחני עסק כפי שנקבעו **בפסיקה**", delegating to the case law. Cite the badge-of-trade factors as case law, not as the circular, and walk the user through them rather than guessing: trade frequency and volume, holding period, time and attention devoted, use of leverage, the taxpayer's professional knowledge, financing method, and inventory-versus-investment intent. No single factor decides it. When it is genuinely borderline, recommend a pre-ruling (hachlatat misui) or CPA review. Business classification also pulls in National Insurance + health tax and a VAT consequence that is routinely got wrong: Circular 05/2018 registers a business-level trader as a **"מוסד כספי"** under Section 4 of the VAT Law (s.3.2.3.2.3), the **miner** as an osek (3.2.3.2.4), and leaves a non-business investor outside VAT (3.2.3.1). Never say "18% VAT plus osek registration"; details in `references/crypto-tax-regulations.md`.
- **Companies**: Standard corporate tax rate (**23%**, since 2018) applies to capital gains.
- **Surtax (mas yesafim)**: two limbs with two different tests. Section 121B(a) charges **3%** on TOTAL taxable income above **NIS 721,560**, salary included. Section 121B(a1) adds **2%** only on the part of **capital-source income that itself exceeds 721,560**. A crypto gain stacked on a salary does NOT attract the 2% unless the capital income alone crosses the threshold: the ITA's own example (execution instruction, הוראת ביצוע, 05/2025) taxes 400,000 salary plus 700,000 capital income at 3% on 378,440 and **no 2% at all**. Business-classified trading income is s.2(1) income, not capital-source, so it bears only the 3%. The Ordinance fixes 721,560 for **2024 through 2027**; do not apply CPI uplifts. Before 2025 only the 3% limb existed, and it already reached capital gains.

**Cost basis method:**
- **FIFO** (First In, First Out) is the customary default. Circular 05/2018 prescribes **no** cost-basis method, so another may be used where applied consistently and documented. What the circular DOES prescribe, and agents routinely miss: section 3.1.5.1 makes the consideration in a barter trade the **same figure on both sides**, the seller's proceeds and the buyer's original cost, at the crypto's fair value in shekels **unless the asset bought carries a stated price (מחיר נקוב), which then fixes the crypto's disposal value**. The circular states no representative-rate requirement and no retention period either, so do not attribute those to it.

**Currency conversion:** convert every transaction to shekels at the rate on the transaction date, and determine the shekel value of **both** sides of a crypto-to-crypto trade at the time of the trade.

### Step 2: Collect Transaction Data

Gather the user's complete transaction history. The following data points are needed for each transaction:

1. **Date and time** of the transaction
2. **Transaction type**: buy, sell, trade, receive (airdrop, staking, mining), send, gift
3. **Asset**: Which cryptocurrency (BTC, ETH, etc.)
4. **Amount**: Quantity of the asset
5. **`price_nis`, the TOTAL shekel consideration for the row, never the per-unit price.** Two ETH bought at 8,000 each is `price_nis=16000`. Reversing it rescales every gain by the quantity and no gate can catch it. Convert foreign-fiat legs to shekels yourself; the calculator does not
6. **Exchange/platform**: where it occurred (Bits of Gold, Binance, Coinbase)
7. **Fees**: transaction, gas and exchange fees (deductible from gains)
8. **Wallet addresses** (optional, for verification)

Sources: exchange exports (Bits of Gold, Bit2C, Binance, Coinbase, Kraken), on-chain history (Etherscan, BscScan) and wallet exports (Ledger Live, Trezor Suite). Dates must be YYYY-MM-DD and numbers carry no thousands separator; the calculator stops on a row it cannot parse.

### Step 3: Calculate Capital Gains Using FIFO

Use the crypto gains calculator script to process transactions:

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2026 --other-income 300000
```

The calculator applies FIFO methodology:

1. **Queue all purchases** by date (oldest first)
2. **For each sale**, match against the oldest available purchase lots
3. **Calculate gain/loss** for each matched lot: net proceeds minus cost, fees included on both sides
4. **Sum all gains and losses** for the tax year

It performs **no currency conversion**. A Binance or Coinbase export in USD or USDT must be converted to shekels row by row BEFORE it reaches `price_nis`; a USD figure pasted in as-is understates every gain by the exchange rate, and nothing in the data reveals it. Merge the exports of every exchange and wallet into ONE file, since FIFO runs per asset across all of them and a transfer between platforms carries its basis with it.

A crypto-to-crypto trade is a disposal of one asset and an acquisition of the other, at one shekel value for both.

### Step 4: Classify DeFi and Special Income

Different crypto activities have different tax treatments in Israel:

| Activity | Classification | Tax Rate | Reporting |
|----------|---------------|----------|-----------|
| Buy and hold, then sell | Capital gain | 25% | Form 1399י |
| Crypto-to-crypto swap | Capital gain (disposal + acquisition) | 25% | Form 1399י |
| Staking rewards | Ordinary income at receipt, then capital gain on sale | Marginal (s.121), see note | 1301 for the receipt; 1399י only on the later sale |
| Liquidity mining/yield farming | Ordinary income | Marginal rates | Form 1301 |
| Airdrops (free tokens) | Income at receipt, capital gain on sale | Marginal + 25% | 1301 for the receipt; 1399י on the sale |
| Mining | Business income, categorically | Marginal rates | Form 1301 |
| NFT sales (creator) | Business income | Marginal rates | Form 1301 |
| NFT sales (collector) | Capital gain | 25% | Form 1399י |
| Hard fork tokens | Zero cost basis (a conservative choice), capital gain on sale | 25% | Form 1399י |
| Lending interest (CeFi/DeFi) | Interest income | 15%, 25% or marginal (s.125C, see note) | Form 1301 |

**Classification notes:**
- **Mining is not a scale question.** Circular 05/2018 s.3.1.4 treats mined crypto as business income categorically; offer no hobby-versus-business test for it.
- **Staking** has no definitive ITA guidance. Conservative treatment: income at receipt at market value, then gain or loss on sale. **There is no general 25% "passive" rate for it.** Unless the reward is characterised as interest (s.125C), it is taxed under s.121, where income not from personal exertion starts at **31%** for an individual under 60 (s.121(a)(1)); the lower brackets of s.121(b)(1) apply only from age 60. Ask the user's age and other income before quoting a figure.
- **Airdrops**: income at market value on receipt, which becomes the basis.
- **Hard forks**: zero cost basis here is a conservative CHOICE, not a sourced rule, and it sits oddly beside the airdrop treatment (income at receipt, becoming basis). State the position you take.
- **Business rows also carry National Insurance and health tax**, which the rate column does not show. Combined rates: see the reference file.
- **Lending interest is not automatically 25%.** Section 2(4) fixes no rate. 125C(b) sets 25%, **125C(c)(1) charges 15%** on a NON-index-linked asset (arguably crypto lending; a USD-stablecoin loan may be argued to be currency-linked, which would put it at 25%), and **125C(d) pushes it to the full marginal rate** where the interest is business income or in the books, or the recipient is a material shareholder, employee or supplier of the payer. See the reference file.
- **DeFi yields** (liquidity provision, farming): ordinary income at marginal rates.

See `references/crypto-tax-regulations.md` and `references/crypto-tax-scenarios.md`.

### Step 5: Choose the Right Reporting Form



Form **1399י** is "הודעה על מכירת נכס", the notice of an **asset** sale that Section 91(d)(1) requires within 30 days. Forms **1322, 1325 and 1326** are **ניירות ערך** forms (1322 for securities **הנסחרים בבורסה**), and the 1301's **נספח ג** is the traded-securities appendix; crypto is a נכס, so none of them carries it. Full titles are in `references/crypto-tax-regulations.md`.

**Many trades in a month:** the 1399י instructions let virtual-currency trades of one month be reported as ONE transaction, with a weighted-average acquisition date (or the real gain entered as a forced transaction, code 51 with code 71). Each trade is still computed separately, and a working paper showing the computation is attached.

Generate the required data:

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2026 --schedule
```

For each disposal the form takes the asset, the FIFO acquisition date, the sale date, the cost and the proceeds in NIS (fees included) and the gain or loss.
The **holding period** earns no US-style long-term preference; it matters for the inflationary-amount split (Sections 88 and 91(c), not 91(b)(3)) and for pre-2012 lots.

**Loss offsetting rules:**
- Capital losses from crypto offset capital gains from crypto and from other assets (stocks, and land betterment, which s.92(a)(1) treats as a capital gain) in the same tax year
- A loss on an asset **outside Israel** is offset first against capital gains outside Israel (s.92(a)(3)); whether crypto held on a foreign exchange is such an asset is unsettled, so flag it
- Unused capital losses carry forward against capital gains only, under Section 92(b) (never against ordinary income)
- A same-year **business** loss (mining, a trader) offsets total taxable income from other sources, capital gains included (s.28(a)); carried forward, it offsets only business income (or s.2(2) income on the s.28(b) conditions)

### Step 6: Calculate Advance Tax Payments (Mikdamot)

If the user has crypto gains during the year, they generally need to file and pay advance tax (mikdama) ahead of the annual return:

- **Form**: **Form 1399י** (1399-yod) for individuals. Virtual currency: transaction code **77** ("all other transactions, including virtual currency") with code **71** ("realisation or conversion of virtual currency"). Form 1399ח is the company equivalent.
- **Reporting deadline**: within **30 days** of EVERY sale, including a sale at a **loss**: s.91(d)(1) requires the notice to set out "רווח ההון או הפסד ההון". It is filed to the assessing officer (pakid shuma). For sales made earlier this year whose 30 days have lapsed, the default advice is to file now; interest and linkage run from day 30.
- **Payment**: 25% of the real gain, after offsetting capital losses **brought forward** (Form 1344) and losses realised **earlier in the same year**; the 1399י loss line counts both.
- **Tax withheld at source by an Israeli platform**: ask first. Bits of Gold announced in April 2022 an arrangement with the ITA (25% of the profit withheld, same-year losses offset, no separate 30-day notice for withheld sales); whether it still runs, and on what terms, is unverified, and the December 2024 draft withholding regulations for digital-asset platforms are not in force. Get the platform's annual withholding confirmation, credit it in the return, and enter it in the calculator's optional `tax_withheld_nis` column so no second advance is demanded. **The surtax is NOT part of this advance.** Section 121B(b) says expressly that Section 91(d)'s advance-payment rules "לא יחולו" to income chargeable to the surtax, so the 3% and 2% are settled annually in the return, not in the 30-day mikdama. A user who adds 5% to the advance overpays it.
- **If the deadline is missed**, Section 91(d)(2e) lets the assessing officer extend the date or reduce the advance on reasonable grounds. Conversely, under 91(d)(2a) he may **increase** an advance he reasonably thinks is understated by 20% or more.
- **Annual reconciliation**: advance payments are credited against the final annual tax liability when filing the annual return.
- **Penalties for non-payment**: interest (ribit) and linkage differences (hafreshei hatzmada) accrue from the 30-day deadline.

```bash
python scripts/crypto-gains-calculator.py --input transactions.csv --year 2026 --advance-payments --loss-carryforward 0
```

### Step 7: Provide Filing Guidance

Guide the user through the tax filing process:

1. **Compile the disposal schedule**: every disposal with acquisition date, cost, proceeds and real gain, in the 1399י columns. There is no ITA crypto appendix (see Step 5); this is your working paper.
2. **File the annual tax return**: submit Form 1301 with the appendices the ITA requires. **There is no crypto appendix**: attach the filed 1399י notices (field **054** counts them, field **056** totals the sale proceeds outside traded securities), with your disposal schedule; their tax is credited against the advance. `references/crypto-tax-regulations.md` sets out the packaging. **Form 1344** is the appendix for losses carried forward from an earlier year, which matters here because Section 92 allows an unused capital loss to be carried forward indefinitely. A crypto disposal generally creates a filing obligation. The January 2025 **draft** salaried-filer exemption for digital assets (Section 134A, conditioned on full withholding by a supervised Israeli platform) is **not in force**: Nevo's consolidated text of the exemption regulations, current to 16.02.2026, contains no digital-asset provision. Quote no ceiling for it; see `references/crypto-tax-regulations.md`. Paying an advance (mikdama) does NOT by itself remove the annual-return obligation.
3. **Filing deadline**: sales made in 2026 go on the **TY2026 return, filed in 2027**, whose deadline the ITA has not yet published; verify on gov.il. For TY2025 the ITA set **30 June 2026 online** and, after an extension, **31 May 2026 on paper**; both have passed, and representing accountants get a separate extension arrangement.
4. **Self-assessment of surtax**: 3% under Section 121B(a) on total taxable income above NIS 721,560, plus 2% under 121B(a1) on the part of capital-source income that itself exceeds 721,560 (see Step 1). No CPI uplift through 2027. 121B(e) excludes the inflationary amount from the base, and 121B(b) keeps the surtax out of the 30-day advance.
5. **Voluntary Disclosure: CLOSED.** The procedure declared on 25 August 2025 ended on **31 August 2026**. As of 12 October 2026 no extension or successor had been announced; check gov.il for one rather than assuming either way. There is no immunity to obtain and you must not imply otherwise. The route for unreported past years is an ordinary corrected return through the assessing officer under Section 131, with the deficiency and offence exposure that attaches to a late or amended return, and the taxpayer should take advice from a tax-specialist lawyer before filing. The procedure's former tracks and limits are in `references/crypto-tax-regulations.md`, for a user asking about an application already lodged.
6. **Bank refuses the funds (Form 909)**: where a bank refuses in writing to accept crypto-derived deposits, an **individual** (not a company) files **Form 909** and pays in shekels directly into the ITA's Bank of Israel account, under ITA Instruction 06/2024. The procedure is temporary and was extended to **31 December 2027**. **Tax paid under it is not refunded**, even where losses, deductions or credits that the assessment did not reflect would have produced a refund, so put every loss and credit into the computation before paying. Attachments and the AML review: see `references/crypto-tax-regulations.md`.
7. **Record keeping**: keep all records, exports and wallet data. Circular 05/2018 s.3.1.3 fixes no retention period; the seven-year figure comes from the bookkeeping directives.

**When to recommend professional help:** over 100 trades a year, complex DeFi (multi-chain, bridging, wrapping), an unclear business-versus-investment call, gains over 500,000 NIS, tokens from an ICO or IEO, any cross-border position, or **derivatives** (futures, perpetuals, options on Binance or Bybit), which this skill and its calculator do not cover at all.

## Examples

### Example 1: Simple Bitcoin Buy and Sell

User says: "I bought 0.5 BTC in January 2025 for 80,000 NIS and sold it in August 2025 for 120,000 NIS. What's my tax?"

Actions:
1. Identify the transaction: single buy, single sell.
2. Calculate capital gain: 120,000 - 80,000 = 40,000 NIS.
3. Apply the 25% ceiling (lower possible from age 60): 40,000 x 0.25 = 10,000 NIS.
4. Check surtax threshold: a 40,000 NIS gain is well below NIS 721,560, so no surtax (assuming no other income above the threshold).
5. Note the holding period: 7 months. The holding period does not change the rate, but the inflation-component split (sechum hatzmada) is negligible for such a short hold.

Result: capital gain 40,000 NIS, tax liability 10,000 NIS. The user should have filed Form 1399י (transaction codes 77/71) within 30 days of the August sale and paid the 10,000 NIS as a mikdama. If the deadline is missed, the user should still file and pay as soon as possible to minimise interest and linkage penalties. The gain is then carried into the **2025 annual tax return**, which was due **30 June 2026 (online) or 31 May 2026 (paper)**.

### Example 2: Crypto-to-Crypto Trade with FIFO

User says: "I bought 2 ETH at 5,000 NIS each in March 2024, then 3 ETH at 7,000 NIS each in June 2024. In October I traded 3 ETH for 0.5 BTC when ETH was worth 9,000 NIS each. What's my tax situation?"

Actions:
1. Build the FIFO queue: Lot 1: 2 ETH @ 5,000 NIS (March), Lot 2: 3 ETH @ 7,000 NIS (June)
2. Process the disposal: 3 ETH traded in October (crypto-to-crypto = taxable disposal)
3. Apply FIFO: First consume Lot 1 (2 ETH @ 5,000), then 1 ETH from Lot 2 (@ 7,000)
4. Calculate gains:
   - Lot 1: 2 ETH x (9,000 - 5,000) = 8,000 NIS gain
   - Lot 2 partial: 1 ETH x (9,000 - 7,000) = 2,000 NIS gain
   - Total gain: 10,000 NIS
5. Tax at 25%: 10,000 x 0.25 = 2,500 NIS
6. Note remaining position: 2 ETH from Lot 2 (@ 7,000 NIS cost) + 0.5 BTC (@ 27,000 NIS total cost, which is 3 x 9,000 NIS)

Result: The crypto-to-crypto trade triggers a taxable event of 10,000 NIS capital gain (2,500 NIS tax). The new BTC position has a cost basis of 27,000 NIS (the NIS value of 3 ETH at the time of trade). The remaining 2 ETH retain their original cost basis of 7,000 NIS each. The agent generates a disposal entry for the 30-day Form 1399י notice.

## Bundled Resources

### Scripts
- `scripts/crypto-gains-calculator.py` -- FIFO capital-gains calculator over a transaction CSV. It refuses to compute on impossible or unparseable data (negative or zero quantities, impossible dates, non-ILS currency, rows it cannot parse) rather than returning a silent zero, and a disposal with no matching purchase lot is reported as UNPRICED and excluded from the totals rather than being given a zero cost basis. Exit code 3 means the report is incomplete. It performs NO currency conversion: convert foreign-currency legs to shekels before the file reaches it. Run: `python scripts/crypto-gains-calculator.py --help`

### References
- `references/crypto-tax-regulations.md` -- ITA circulars, the Ordinance sections with their verbatim text (including the Section 100A formula), the ITA's own published form titles, classification rules and deadlines.
- `references/crypto-tax-scenarios.md` -- worked examples: simple trades, crypto-to-crypto swaps, DeFi staking, NFT sales, mining, airdrops, hard forks.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [BOI Exchange Rates](https://agentskills.co.il/he/mcp/boi-exchange) | The Bank of Israel daily representative rate, for converting foreign-currency legs to shekels **before** they reach the calculator. A defensible documented choice, not one Circular 05/2018 mandates. |

## Gotchas
- Israel taxes crypto as property (capital gains), not as currency; currency-exchange rules do not apply.
- The Israeli individual rate is up to 25% (a ceiling), not the US 15%/20%. Agents trained on US data will use the wrong one.
- Israeli practice defaults to FIFO. Agents may default to average cost or LIFO, which are not standard here.
- Crypto-to-crypto swaps are taxable events in Israel. Agents may treat them as non-taxable exchanges (the old US rule), which has never been the Israeli position. Circular 05/2018 section 3.1.5.1 also requires the SAME shekel figure to serve as the seller's proceeds and the buyer's original cost, so the two CSV legs of a swap must carry identical values.
- **Stablecoins are still an "asset" under Section 88**, not foreign currency. Every USDT-to-USDC swap, every conversion leg of a DeFi trade and every off-ramp is a taxable disposal in shekels. Users treat them as cash equivalents and skip them, missing most of an active DeFi participant's taxable events.
- **Inflation indexation (sechum hatzmada) is not applied by the calculator, and the rate is not 0%.** Section 91(c) taxes the **chargeable** inflationary amount at **10%**, which is nil for crypto only because Section 88 confines it to gain accrued by 31.12.1993; do not state a "0% rate". The calculator applies 25% to the whole gain with no CPI step, so it overstates tax on long-held lots in inflationary years. The 1399י itself carries the real-gain and inflationary-amount lines; recommend a manual indexation pass or CPA review before filing.
- **Israel has no wash-sale rule.** A taxpayer may realise a December loss and re-buy in January with the loss fully recognised. Agents trained on US tools may wrongly disallow it.
- **Gift and inheritance basis runs through Section 88's מחיר מקורי and יום הרכישה.** Inheritance carries the deceased's basis and date. A gift carries the donor's basis only if it was EXEMPT under s.97(a)(4) or (5); a non-exempt gift from a non-relative takes its value on the day of the gift. Zero basis is always wrong.
- **Crypto lost to insolvency, theft or lost keys** is a capital loss only once the loss is final and documented (bankruptcy order, police report). Do not write off frozen-but-solvent balances or undocumented key loss.
- **A capital loss offsets more than the real gain, and the carry-forward has a condition.** Section 92(a)(1) offsets the loss against the real gain first, then each remaining shekel offsets **three and a half shekels** of chargeable inflationary amount. Section 92(b) carries the unused amount forward against capital gains in the following years, **but only if a return was filed for the year the loss arose**, so a client who skipped that year has lost the carry-forward. The calculator performs neither offset nor carry-forward; Form 1344 is the appendix for the brought-forward figure.
- **Leaving Israel triggers an exit tax (deemed sale, Section 100A), and the deferral is NOT an election.** s.100A(b) deems anyone who does not pay on leaving to have **requested** deferral to realization; the chargeable portion is measured at realization, apportioned by elapsed time, and **no interest or linkage accrues during the deferral**. Formula and text: `references/crypto-tax-regulations.md`. The calculator does NOT model this; route relocation to a CPA and the aliyah skills.
- **An oleh or toshav chozer vatik may hold a 10-year exemption**: Section 14(a) for income, **Section 97(b)(1)** for a capital gain on an asset **held outside Israel** (where crypto is located is unsettled; flag it). From 2026 the s.134B **reporting** exemption is cancelled for new residents, so the exempt income must still be reported. The calculator does not model the exemption and will overstate tax.

## Troubleshooting

### Problem: no NIS rate available for a transaction date
Cause: the Bank of Israel publishes no rate on Shabbat and holidays.
Solution: use the rate from the most recent prior business day, and **do it in the CSV, not in the tool**. The calculator performs no rate lookup and has no `--manual-rate` flag; it consumes `price_nis` exactly as given.

### Error: "FIFO queue exhausted - more sold than purchased"
Cause: the history sells more than it bought, usually because purchases are missing (deposits from another exchange or wallet, or a partial export).
Solution: review the history for completeness; a transfer in from another exchange or wallet is not a taxable event but must be recorded to carry the cost basis. Add the missing purchases. Where the original records are genuinely unavailable, establish a basis from the earliest available market price, document it, and disclose it. The calculator will not do this for you: it marks such disposals UNPRICED and excludes them, so the printed totals UNDERSTATE the gain until you supply a basis.

### Error: "Transaction type not recognized for tax classification"
Cause: The calculator encountered a transaction type it cannot automatically classify for tax purposes (e.g., a complex DeFi interaction, bridge transaction, or wrapped token conversion).
Solution: map the row to a recognised type by hand. Wrapping (ETH to WETH) is generally not a taxable event; a bridge may be one if it involves a swap; a liquidity deposit is contested (see Scenario 9 in `references/crypto-tax-scenarios.md`).

### Error: the report says UNPRICED, or exits with code 3
Cause: one or more disposals have no matching purchase lot in the file, so their cost basis is unknown. The calculator deliberately does NOT assume a zero basis, because that overstates the gain and manufactures an acquisition fact for the return.
Solution: Review the error output which lists the specific transactions with missing data. For each, provide the acquisition date (FIFO-determined) and the NIS value at that date. For a gift or inheritance, see the Section 88 basis rules in the Gotchas; airdrops use the market value at receipt. Update the transaction CSV with the corrected data and re-run.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israeli Tax Authority - annual return service (Form 1301) | https://www.gov.il/he/service/reporting-and-payment-2025-annual-tax-report-for-individuals | TY2025 forms (1301, 1399י, 1344) and the online filing portal. Look for the TY2026 page in 2027 |
| ITA execution instruction (הוראת ביצוע) 05/2025, the 2% capital-source surtax | https://www.gov.il/BlobFolder/policy/inst-05-2025/he/IncomeTax_inst-05-2025.pdf | Worked examples showing the 2% applies only to capital income that itself exceeds the threshold |
| Bank of Israel - representative rates (sha'ar yatzig) | https://www.boi.org.il/roles/markets/exchangerates/ | Daily NIS reference rates for currency conversion of foreign-fiat legs of crypto trades |
| ITA Circular 05/2018 (crypto classification; prescribes no cost-basis method) | https://www.gov.il/BlobFolder/policy/income-tax-professional-inst-5-2018/he/Policy_ProfessionalInstIncomeTax_hor_acc%2015.2.18.pdf | Foundational tax-treatment guidance for virtual currencies |
| Voluntary Disclosure Procedure, ITA announcement | https://www.gov.il/he/pages/sa250825-1 | The declaration of 25 Aug 2025 and its 31 Aug 2026 end date. The procedure has CLOSED; check here for any successor |
| Form 909 - paying crypto tax when a bank refuses the funds | https://www.gov.il/he/service/reporting-cryptocurrency-activity | Bank-refusal payment procedure, required attachments, individuals only. Extension to 31.12.2027 and the no-refund rule: https://www.gov.il/he/pages/pa310826-1 |
| Bituach Leumi self-employed rates (2026) | https://www.btl.gov.il/Insurance/National%20Insurance/type_list/Self_Employed/Pages/rates.aspx | Current National Insurance + health-tax rates for business-classified crypto traders |
| OECD Crypto-Asset Reporting Framework (CARF) - committed jurisdictions | https://www.oecd.org/content/dam/oecd/en/networks/global-forum-tax-transparency/commitments-carf.pdf | Israel is listed under "Jurisdictions undertaking first exchanges by **2028**" (list updated 14 Sep 2026). Israeli implementing legislation has not been enacted, so assert no data-collection start date. Re-check the list, which the Global Forum revises |
