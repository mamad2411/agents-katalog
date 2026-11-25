---
name: stress-test-unit-economics
description: >-
  Builds a business plan's per-unit model with the arithmetic shown, dates the cash low point, and
  finds the one input that kills the business, called by ceh-business-plan:develop-business-plan.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Stress-test unit economics

Prove or disprove that one unit of this business makes money and that cash lasts until enough units
are sold. Done is a unit model, a cash timeline, and a sensitivity table in §08 and §11 of
`BUSINESS_PLAN.md`, with the single input that kills the business named in §12.

## Procedure

1. Read the plan, schema in `${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`. Collect
   every number already stated and where it came from.
2. Define the unit: one customer, one order, one seat, one job. Pick the thing the customer pays
   for. A wrong unit hides the loss, so state it before any arithmetic.
3. Build the unit model in the Output table. Every input carries a confidence tag and a source.
   Where the plan has no number, write your best estimate as a range and tag it `[assumption]`.
4. Find the cost floor. Break the largest cost into its components and ask what each must cost at
   minimum (Elon Musk's first-principles pass on battery and rocket costs). Then run it the other
   way: start from the price the customer will pay and state what the cost must come down to
   (Ingvar Kamprad designed IKEA products from the price tag backward).
5. Lay out cash timing month by month for 18 months: when cash is paid out, when it is collected.
   Record the cash conversion cycle, the lowest cash balance, and the month it falls in. Michael
   Dell collected from customers before paying suppliers, so growth funded itself. Most plans have
   the reverse, where growth consumes cash.
6. Answer the default-alive question: at the current cost base and a growth rate already observed
   or conservatively assumed, does the business reach break-even before the cash runs out? (Paul
   Graham's test.) State yes or no with the month.
7. Run the sensitivity table. Flex each input to its own plausible bad case, not a uniform 10%,
   because a uniform flex hides which input actually kills the business.
   The input whose bad case flips the unit to a loss, or moves the cash-out month before
   break-even, is the kill input.
8. Apply the margin of safety: the plan must still work with the two weakest inputs at their bad
   case together. (Benjamin Graham's principle, Buffett's first rule: do not lose the money.)
9. Write §08 and §11 now, and add the kill input to §12 as one line with its cheapest test, ending
   `(stress-test-unit-economics)`. Writing before asking keeps the model if the session is
   interrupted.
10. Show the user the three tables and ask about the kill input first, one question per turn,
    three questions at most. Revise the tables in place after each answer. An input still open
    stays tagged `[assumption]`. Then re-score criteria 5 and 6 of the PMF gate.

## Checks on the model

| Check           | Ask                                                                                                                    | Warning sign                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Price basis     | Is the price tied to what the customer spends on the alternative today?                                                | The price is cost plus a margin, or a guess                           |
| Contribution    | Does one unit cover its own variable costs, including support, payment fees, returns, and delivery?                    | Margin is quoted before those costs                                   |
| Acquisition     | Is the cost to win a customer measured, or borrowed from a blog post?                                                  | It rests on free channels that have not been tried                    |
| Payback         | How many months until a customer returns what it cost to win them?                                                     | Payback is longer than the cash on hand allows                        |
| Retention       | How long does a customer stay, and what is that based on?                                                              | Lifetime value assumes a retention figure nobody has observed         |
| Scale direction | Does unit cost fall as volume grows, and by how much? (Henry Ford and Sam Walton cut prices as scale cut their costs.) | Costs rise with volume: people, support, or compute scale one for one |
| Fixed cost      | What must be paid whether or not anything sells?                                                                       | Fixed cost is committed before the first sale                         |
| Founder pay     | Does the model include a wage for the founders?                                                                        | Profit exists only because the founders work for nothing              |

Common rules of thumb for subscription software are lifetime value at least three times
acquisition cost and payback within twelve months. Treat them as conventions to state and compare
against. Other business types have their own, so ask what the norm is in the user's industry
before applying one.

## Rules

- No number without its arithmetic. Write `40 customers x $49 x 12 = $23,520`, never `$23.5k ARR`.
  Only a visible input can be checked or replaced.
- Never invent the user's figures. An estimate is a range with an `[assumption]` tag and a named
  way to replace it with a real number.
- Bottom-up only. Revenue is customers times price. A percentage of a large market is not a
  forecast.
- Three numbers decide viability: contribution per unit, payback period, cash low point. Lead with
  those. A five-year projection adds false precision and is out of scope.
- State bad news in the first line. If the unit loses money, say so before showing the tables,
  because it changes every decision downstream and is easy to skim past below them.
- Re-tag as numbers firm up. An input the user confirms from a real invoice or a real sale becomes
  `[evidence]`.

## Output

`### Unit model` goes into §08 and `### Cash and sensitivity` into §11. A re-run replaces both:

```markdown
### Unit model

Unit: <one customer per month>

| Line                  | Value | Arithmetic or source    | Tag |
| --------------------- | ----- | ----------------------- | --- |
| Price                 |       |                         |     |
| Variable cost         |       |                         |     |
| Contribution per unit |       | price - variable        |     |
| Cost to acquire       |       |                         |     |
| Payback (months)      |       | acquire / contribution  |     |
| Expected lifetime     |       |                         |     |
| Lifetime value        |       | contribution x lifetime |     |

### Cash and sensitivity

#### Cash

- Cash conversion cycle: <days>, <collect before or after paying>
- Lowest balance: <amount> in <month>
- Default alive: <yes | no>, break-even in <month> against cash-out in <month>

#### Sensitivity

| Input | Base | Bad case | Why that bad case | Unit result | Cash-out month |
| ----- | ---- | -------- | ----------------- | ----------- | -------------- |

**Kill input:** <input> — <the cheapest test that would replace the estimate with a number>
```

## Stop conditions

- The unit loses money at the base case and no price or cost change the user accepts fixes it →
  report that the business does not work as planned, with the gap in money per unit.
- There is no price and no customer signal to anchor one → stop and name
  `ceh-business-plan:find-product-market-fit`. A model on a guessed price tests nothing.
- **No human to answer** (a headless run, or called by another agent): ask nothing. Draft and
  revise from what the plan holds, tag every gap `[assumption]`, and end with the questions you
  would have asked, in order, each with the assumption you used instead.

## Hands off to

- When the kill input is acquisition cost or conversion, suggest
  `ceh-business-plan:plan-go-to-market` to test the channel.
- When the model only works at a price the customer has not signaled, suggest
  `ceh-business-plan:sharpen-strategy` for the pricing-power test.
