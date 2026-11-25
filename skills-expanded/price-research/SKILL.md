---
name: price-research
description: Use when someone needs to find out how much customers will actually pay before setting or changing a price — e.g. "what's the most profitable price for this", "should I survey my list about pricing", "how do I test willingness to pay", "is Van Westendorp the right method", "we're just copying competitor prices".
---

# Price research

Find the profit-maximizing price with two one-question surveys and a correction step, instead of guessing, copying competitors, or averaging "what would you pay?" answers. The method combines an open question (which people overstate) with a randomized yes/no question (which is unbiased but coarse) to get an accurate demand curve cheaply.

## When to use

- Pricing a new product, plan, or course before launch
- Deciding whether to raise or lower an existing price
- The user proposes a "how much would you pay?" survey, Van Westendorp, or competitor matching

## When not to use

- Choosing the digits or presentation of a price already decided → the `pricing` skill
- Unable to get ~500 completed responses (30 per closed price × 7, the same again for the open survey, plus drop-off): the method needs volume; suggest a price A/B test instead

## Inputs

- Product description, images, or a demo (realism matters)
- Unit cost, reachable audience size, currency
- The lowest and highest price you can imagine charging
- Channels to recruit respondents (site, newsletter, customers, panel)
- Strategy: maximize profit now, volume/reach, or premium positioning

## Procedure

1. **Why not the usual methods.** Averaging open "how much would you pay?" answers overstates by a large margin (often ~50%). Asking "would you buy at $X?" alone is biased by the price acting as a quality cue. Competitor matching ignores your own demand. Van Westendorp gives an "acceptable range", not the profit-maximizing point. The lab-standard auction method (BDM) is accurate but requires selling the real product and is too costly for most teams.
2. **Build the price ladder.** Pick 7 prices with equal steps from the lowest to the highest plausible price ($20, $40 … $140). More steps need more respondents. †
3. **Write two surveys with identical product descriptions.** Survey A (open): "What is the most you would pay for [product]? (in $)". Survey B (closed): "Would you buy [product] for $X? Yes / No", where X is one ladder price chosen at random per respondent. Use a tool that supports random-subset questions (Qualtrics does) and a random link splitter to send 50% to each survey.
4. **Sample size.** At least 30 answers per closed price → 210 for B, the same for A, plus ~80 for drop-off ≈ 500 total. † Work back from your expected response rate: at 5%, a list of 10,000 yields ~500. Recruit existing or prospective customers first; panels are a fallback. Say "one quick question" and offer a reward (coupon, prize draw). Keep it open 2–3 weeks.
5. **Test before launch.** Preview both surveys, open the split link in incognito several times, confirm prices randomize, delete test answers.
6. **Check, then clean.** Stop and ask before computing if the closed survey has fewer than 4 distinct prices, if the ladder steps are not equal, or if any closed answer is not a clear yes/no (yes/no, y/n, true/false, 1/0); fix the data, don't guess. Then drop every Survey A answer at or below $0 and every answer above 5× the median of the positive answers; if you use another multiple, say so. †
7. **Correct.** `corrected = open_answer − mean(open) + mean(closed)`, where `mean(closed)` is the area under the yes-share curve across the ladder. Use the trapezoid rule: add the points 100% yes at $0 and 0% yes one step above the top price, then sum `(share_a + share_b) / 2 × step` over each pair of neighbouring points. Each corrected value is an estimate of that respondent's willingness to pay; the distribution, not any single value, is what you use.
8. **Demand and profit.** For each ladder price: share of corrected values ≥ price; buyers = share × audience; profit = (price − unit cost) × buyers. Pick the maximum and list near-ties (within 10% of the best profit). Do not recommend a price if no price is profitable at the given cost, if any closed price has fewer than 30 answers, or if the cleaned open survey has fewer than 30 × the number of prices; show the table as indicative only and say what data is missing. *Audience* is the number of people who will actually see the offer (expected launch reach), not the size of the survey list. *Unit cost* is the marginal cost per sale; for digital products that is near $0 plus any per-sale fees, and the profit-maximizing price then equals the revenue-maximizing one. If two adjacent prices are within ~10% on profit, treat them as a tie and let strategy (step 9) or a live A/B test decide.
9. **Override by strategy.** A premium brand may choose a higher price at lower profit to attract future buyers; a reach-first launch may go lower. Say which you chose and why. †

Do the calculation yourself on the raw answers (open: one amount per respondent; closed: price and yes/no per respondent), with code or a spreadsheet if the environment has one, and show the working in this layout. Worked example on synthetic data (230 open answers, 30 per price on a 7-step ladder, cost 5, audience 8000):

```
Open survey: 230 answers, 3 dropped (<=0 or >5x median)
Closed survey: 210 answers across 7 prices
       30.00  yes  96.7%  n=30
       60.00  yes  86.7%  n=30
       90.00  yes  40.0%  n=30
      120.00  yes  23.3%  n=30
      150.00  yes  13.3%  n=30
      180.00  yes   3.3%  n=30
      210.00  yes   0.0%  n=30

mean_open   = 125.59
mean_closed = 94.00
correction  = mean_closed - mean_open = -31.59  (applied to every open answer)
corrected mean WTP = 94.00

     price  share willing     buyers       profit
     30.00          83.7%       6696       167401
     60.00          63.0%       5040       277181
     90.00          42.3%       3383       287577
    120.00          26.9%       2150       247225
    150.00          17.2%       1374       199295
    180.00          11.9%        952       166520
    210.00           7.5%        599       122819

Profit-maximizing price: 90.00  (profit 287577 at cost 5, audience 8000)
Near-ties (within 10% of the best profit): 60.00 — treat as tied; decide by strategy or a live A/B test.
Override for strategy: a premium brand may pick a higher price; a reach-first launch a lower one.
```

## Output

| Item | Value |
|---|---|
| Price ladder | 7 prices, equal steps, range stated |
| Survey A / B wording | exact text |
| Sample plan | ≥30 per price; target ~500; channels; incentive; duration |
| Correction constants | mean_open, mean_closed, shift |
| Demand & profit table | per ladder price |
| Recommended price | with the strategy override, if any |

## Common mistakes

- Averaging "what would you pay?" answers — overstated; needs the closed-survey correction.
- Reaching for Van Westendorp — gives a range, not the profit-maximizing point.
- Uneven ladders ($20, $50, $100) — steps must be equal for the correction to hold.
- Too many prices for the sample (10 prices with 276 answers) — under 30 per price; use 7 and run longer.
- Thin product description — respondents price what they imagine; show images or a demo.
- Picking the top-profit price blindly when the brand is premium — state the strategic override.

## Quick reference

| Step | Rule |
|---|---|
| Ladder | 7 prices, equal steps, generous range |
| Split | 50/50 random to open vs closed; random price within closed |
| Sample | ≥30 per closed price, ~500 total |
| Clean | Drop 0 and outliers (>5× median) |
| Correct | open − mean(open) + mean(closed) |
| Choose | max (price − cost) × audience × share ≥ price, then apply strategy |

† No primary citation on file for this rule — a practitioner tip, not a measured finding.

Evidence and effect sizes: see [reference.md](reference.md).
