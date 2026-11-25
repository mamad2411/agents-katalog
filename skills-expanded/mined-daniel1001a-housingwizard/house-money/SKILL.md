---
name: house-money
description: Home-purchase money math - cash to close (down payment plus closing costs), monthly payment with taxes, insurance and PMI, the highest price that fits cash, monthly and reserve limits at the same time, down payment trade-offs, gift funds, comparing Loan Estimates, rate locks, and seller credits vs price cuts. Use when a buyer asks "can we afford this", "how much cash do we need", "what should our max offer be", "20% or less down", "which lender", "when to lock", or whenever a price, rate or loan amount changes. Includes a script with a New York City preset and a generic US preset.
---

# House money

Most affordability mistakes come from solving limits one at a time: pick a down payment, then check the monthly payment, then notice the reserve is gone. Solved in sequence, the same numbers can say "yes" in one session and "no" in the next. Solve them together.

<!-- shared:rules -->
## Ground rules (shared by every HousingWizard skill)

Each one guards against a common, expensive mistake. They apply to every answer.

1. **Tag where each fact came from.** Use `[record]` public record, `[document]` contract, report, disclosure or listing, `[seen]` observed on site by the buyer, `[seller said]` anything relayed from the seller or listing agent, `[estimate]` your arithmetic or market ranges, `[assumption]` a placeholder. Never promote a seller statement or an estimate to a fact.
2. **Zero rows is not clean.** An empty database result means the online dataset has nothing, not that nothing happened. Compare with neighbors before calling anything unusual.
3. **Give the honest counter-case.** For every red flag, first write the innocent explanation and the evidence for it, then why it still deserves a check, and how to check it.
4. **End with a human check.** Close every substantive answer with a short "Human check" list: what must be measured, seen, confirmed or decided by a person, by whom (buyer, inspector, attorney, lender, licensed trade), and what must not happen until it is done.
5. **You are not the buyer's lawyer, agent, inspector or lender.** Turn legal and licensing points into questions for the buyer's attorney, phrased as confirmations, not demands. Cost figures are ranges with a source, never quotes.
6. **Name the jurisdiction.** Say which state and city rules you are applying. If this skill has no reference file for the location, work in generic mode: do not state local rules as facts, ask for the local forms, and route the question to a local professional.
7. **Draft, never act.** Write messages, letters and checklists for the buyer to send or use. Do not send, sign, pay, accept terms, or fill forms on their behalf.
8. **Stop at walls.** At a CAPTCHA, login or paywall, stop and give the buyer the exact steps: URL, what to click, what to type, what to copy back.
9. **Keep the case file true.** Write new facts into the buyer's case file (see house-case-file). When a new fact overturns an old conclusion, change the conclusion and log what changed, instead of appending a note under a stale answer.
10. **Re-check anything time-sensitive.** Rates, taxes, fees, tariffs and code section numbers change. Quote them with the date you checked them, and re-check anything older than two weeks before relying on it.
<!-- /shared:rules -->

## Inputs to collect

Ask only for what is missing from the case file:

- Cash available now and when any gifts arrive (gifts need lender paperwork; ask the lender before moving money).
- Monthly ceiling. If the buyer has a conservative rule and a real maximum, keep both and show both. Do not rewrite either one.
- Reserve that must stay untouched after closing, and cash needed for work right after closing.
- Rate to use (a real quote if they have one; otherwise two or three scenarios, dated).
- Property tax: the actual bill if possible. Estimates from assessed value are often wrong, and many places reassess after a sale or after improvements.
- Insurance: a quote if possible; otherwise a placeholder labeled as one.
- Location, for closing costs and transfer taxes.

## Run the numbers

`scripts/cash_to_close.py` (Python 3, no packages):

```bash
# One price: cash to close and monthly payment across rates
python3 scripts/cash_to_close.py scenario --price 850000 --down-pct 20 --rates 6.25 6.75 7.25 --tax-monthly 900 --insurance 180 --cash 250000 --reserve 30000

# New York City preset (mansion tax brackets, mortgage recording tax buyer share)
python3 scripts/cash_to_close.py scenario --preset nyc --price 1250000 --ltv 75 --tax-monthly 1000

# NYC co-op: no mortgage recording tax on a share loan; mansion tax still applies at $1M+
python3 scripts/cash_to_close.py scenario --preset nyc --property coop --price 1250000 --ltv 75

# Highest price that fits every limit at once, and which limit binds
python3 scripts/cash_to_close.py max-price --cash 250000 --reserve 30000 --renovation 40000 --monthly-cap 6500 --rate 6.75 --tax-rate 1.2 --insurance 180
```

The output labels each number `[you]`, `[assumed]` or as a checked rule. Carry those labels into your answer. If the script warns that the NYC rates are old, say so and re-check the official pages before relying on them. For a co-op, pass the monthly maintenance as `--hoa`, and add the flip tax and lien search to `--misc` when the buyer pays them. If the script cannot run here, do the same arithmetic by hand and show it.

## Say what the numbers mean

- **Which limit binds.** Cash, monthly payment, or both. When both bind, a bigger loan eases cash but raises the payment; say so, because that is the real trade-off the buyer is choosing.
- **Down payment is a range, not a rule.** 20 percent avoids PMI but can drain the reserve. Show two or three down payment choices with their monthly payment and leftover cash.
- **Cliffs.** Some taxes apply to the full price once a threshold is crossed (New York's mansion tax starts at $1,000,000). If the price is near a threshold, show both sides.
- **Tax surprises.** Improvements and additions can raise property tax immediately even where annual increases are capped (New York City's class 1 caps do not cover physical improvements).

## Loans, locks and credits

Read `references/loans.md` for lender comparison, rate lock timing, seller credit limits, and what not to do during underwriting.

## Output

1. The answer in one line (for example: "Up to about $X fits; cash is the limit, not the monthly payment").
2. The table the script produced, with labels.
3. Which assumptions move the answer most, and how to replace them with real numbers (tax bill, insurance quote, Loan Estimates).
4. Human check.

Update the case file with the figures and their dates.
