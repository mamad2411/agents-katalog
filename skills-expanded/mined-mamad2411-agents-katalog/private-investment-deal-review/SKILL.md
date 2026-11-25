---
name: private-investment-deal-review
description: >
  Review private early-stage investment deals and offering docs (Echo.xyz group
  SPVs, angel/SAFE/preferred rounds, Dropbox/transfer zip packages). Use when
  Cooper asks how/when stock is delivered, what he actually owns, broker transfer
  questions, carry/fees, liquidity, or pastes an Echo/offering-docs link.
version: 1.0.0
---

# Private investment deal review

## When to use
- Echo.xyz (or similar onchain group-invest) equity/token deals
- "When do I get the stock?" / "transfer to broker?"
- Offering memorandum, subscription agreement, M&AA, Dropbox transfer of deal docs
- SPV / Participating Shares / SAFE / preferred structure questions

## Default mental model (Echo equity)
Do **not** assume broker street-name shares.

Typical stack:
```
Investor → Participating Shares in deal SPV (often BVI) → SPV holds company Preferred/SAFE/token warrant
```

- Cap table at the **company** shows **one line** (the SPV), not each Echo angel.
- Investor proof = offering docs + SPV register / Echo Account → Documents — **not** DTC to Fidelity.
- Tokens (when the deal is tokens) are different: more wallet-direct; investor often controls sell timing. Equity is SPV paper.

Platform facts (Echo public support — confirm against current deal docs):
- Fund in **USDC** onchain; participants rolled into a single vehicle
- Echo fee model (platform): **~5% of profits** only when user profits; deal ops costs (SPV filings, etc.) shared among SPV investors
- Lead never custodied follower USDC; Manager/legal entity (e.g. Gm Echo Manager Ltd) runs vehicle
- Liquidity: illiquid until exit / compulsory redemption / distribution; no optional shareholder redemption on many vehicles

## Workflow
1. **Identify asset type** from Schedule 1 / deal card: Preferred / SAFE / token / warrant.
2. **Get the docs** (prefer local over fighting Dropbox Transfer JS):
   - Check `~/Downloads/*offering*`, `~/Downloads/*<issuer>*`, unzipped sibling folders first
   - Dropbox Transfer short links often need a browser session; `?dl=1` may return HTML. If zip already landed in Downloads, use it.
   - Extract: `unzip -o "...zip" -d /tmp/deal-docs`
3. **Text-extract**:
   - `.docx` → `textutil -convert txt` (macOS) or python-docx
   - `.pdf` → `pdftotext` if present; else note limitation and use Preview/computer_use only if needed
4. **Mine these fields** (table for Cooper):
   | Field | Where |
   |---|---|
   | Vehicle legal name / jurisdiction | OM cover, Articles |
   | What investor receives | Participating Shares vs LP interest |
   | Underlying Investment | Schedule 1 |
   | Valuation / instrument | Schedule 1 |
   | Investment Allocation vs Expense Allotment | Definitions / Summary of Terms |
   | Subscription Date / Term | Definitions |
   | Carry / Performance Fee | OM economics |
   | Voting (investor vs Manager Management Shares) | Rights of Management Shares |
   | Redemption / transfer | OM + Subscription reps |
   | Distribution path | same wallet/bank as funding |
5. **Answer delivery questions in plain English**:
   - When SPV shares issue (funds + KYC + acceptance → Subscription Date)
   - When underlying closes (Definitive Documents with company — often after vehicle close)
   - Broker? Almost never for private preferred via Echo SPV
6. **Flag risks briefly** (don't dump full OM): no optional redemption, transfer only with Director consent, Manager voting control, carry, expense haircut, competitor transfer blocks, side letters, illiquidity/term.

## Response shape
- Lead with the stack diagram and "not a broker transfer"
- Timeline table (fund → SPV share issue → company securities in SPV → exit/distribution)
- Deal-specific numbers from Schedule 1
- Optional next: share-count math after pro-rata expense, or risk deep-dive
- Cooper often wants **short sequential answers** (liquidity → currency → secondary → marks). Prefer tight tables + one-line bottom lines over long preambles once the stack is established.

## Liquidity / secondary / returns (ask these early)
| Question | Default Echo equity SPV answer |
|---|---|
| Secondary market? | **No free secondary.** Transfer only w/ Director consent; no listing; not redeemable at investor option. Underlying preferred is sold (if ever) by Manager/SPV, not by Cooper personally. |
| How do I get paid? | **M&A / IPO-type company exit**, SPV distribution, rare consented transfer, or end-of-term wind-down (may still be illiquid paper). |
| Currency of return? | **USD or USDC** back to the **same wallet/bank funded from** (USDC in → expect USDC out). Not brokered company shares by default. In-kind is theoretically possible but not the standard path. |
| Green P&L in portfolio? | **Unrealized mark**, not cash. Usually last preferred round / Manager Valuation Policy — **not** "someone bought my SPV shares." |

## Portfolio marks vs real rounds
When Cooper asks "how can it be up?" or "round or 409A?":
1. Restate: **paper NAV**, illiquid, not sellable at mark.
2. Pull **entry post-money** from Schedule 1 / deal card.
3. Search public funding timeline **after Subscription Date** (company press, CB Insights, Caplight, Tracxn). Prefer **priced/extension equity rounds** over 409A language.
4. **409A** is option FMV and often **below** last preferred — Echo-style upside marks are usually **last round preferred**, not 409A.
5. If he gives cost → mark (e.g. $10k → $22.6k), reverse multiple:
   - `implied_PM ≈ entry_PM × (mark / cost)` **only if** platform marks 1:1 to new preferred price with no discount/carry reserve.
   - Label as **inference**, not disclosed valuation. Form D rarely states post-money; press often omits it.
6. Flat extensions at the **same** price would **not** explain a large mark-up by themselves.

## Pitfalls
- Do **not** say "you'll get Exowatt stock in your brokerage" for Echo SPV equity deals
- Do **not** confuse Echo platform 5% profit fee with Vehicle **carried interest** (often 20% in memo) — both can apply; label sources
- Subscription signatures may sit **in escrow** until Vehicle close — "I clicked invest" ≠ shares issued yet
- Expense allotment is often **deducted pro-rata** from Aggregate Investment Amount before Subscription Amount / share count
- Company Definitive Documents may **not** be drafted by Vehicle counsel — rights "expected" not guaranteed until signed
- Confidentiality: don't republish deal terms publicly; keep analysis in-session / Cooper-private
- Do **not** treat portfolio appreciation as realized return or secondary bid
- Do **not** claim a precise new post-money from a dashboard multiple without stating assumptions (1:1 mark, no illiquidity discount, carry not reserved in NAV)
- SEC EDGAR bots often block undeclared UAs; use a proper User-Agent or browser if Form D is needed — don't invent filing contents

## References
- `references/echo-spv-pattern.md` — Echo vehicle pattern + Exowatt CC Ltd worked example (incl. Nov-2025 mark inference)
