---
name: ui-part-pricing
description: "Pricing sections and pages: real prices or placeholders, the shape by what is sold, one plan's anatomy, recommending a plan honestly, billing period, currency and tax, comparison tables, price lists for services, phones, and what is dishonest or unlawful. Read before building or reworking any pricing section, plan comparison or price list."
---

# Pricing

The generated version: three cards called Starter, Pro and Enterprise, the
middle one raised with a glow and a "Most popular" ribbon nobody measured,
a monthly and yearly switch promising "Save 20%", crossed-out prices that
were never charged, and twelve features with a check on every line.
Pricing is where people decide whether to pay, so every number on it is a
promise the business has to keep. The principles are in the `ui` skill,
the measures in `ui-layout`, the words in `writing`.

## 1. What it is for, and its shape

- Use it for letting a user choose a plan and know what they pay.
- Real prices only, from the business, or visible placeholders (`[Price]`,
  `[Plan name]`) listed in your report. Never a plausible guess.
- As many plans as are real, not three columns by default. Features in the
  same order in every plan so they can be compared.

| What is sold | Shape |
|---|---|
| One plan or one product | a single statement: the price, what it includes, the button; not a lone card |
| Two to four plans | the plans side by side on wide screens |
| Five or more plans, or many differences | a short summary of the plans, then a comparison table |
| Services at set prices (a clinic, a salon, a workshop) | a price list: the service, its length or unit, its price, in aligned columns |
| Prices that depend on the job | what the price depends on, a real example if the business gives one, how to get a quote |

- A landing page carries a short pricing section; a pricing page holds the
  comparison and the billing questions.

## 2. One plan

- **The name** (18 to 20px, weight 600): the business's own plan names.
- **Who it is for**, in one line ("For a practice with one to three
  therapists").
- **The price**: the largest figure on the card (31 to 39px, `tabular-nums`,
  never wrapping), with its currency and period ("per month", "per user
  per month"), and the billing note under it ("Billed yearly", "Excl.
  VAT").
- **One button** that says what happens next: "Start with Team", "Book a
  call"; "Start a 14-day trial" only when the trial exists and is that
  long. The next page asks for nothing the button did not warn about (a
  card number).
- **The features**: a short list of 5 to 8 lines, the differences first
  ("Everything in Solo, plus:"), limits as numbers ("3 projects", "10
  GB"), each feature named the same way in every plan.
- **Measures**: plans 16 to 24px apart, 24 to 32px of padding, the card
  radius. Name, audience, price, button and features line up across the
  plans (`grid-template-rows: subgrid`), so prices and buttons sit on one
  line.

## 3. Recommending a plan

- One plan highlighted only when there is a reason to recommend it, with
  the reason in words: "Recommended for teams of five or more". A border in
  the accent and that label; the page's one filled button on that plan, the
  others outlined.
- No recommendation: every plan the same, every button the same style.
- Not "Most popular" on the middle plan with no basis, not a card scaled up
  with a glow.

## 4. Billing period, currency and tax

- A monthly and yearly switch only when both exist, as a segmented control
  (native radios in a `fieldset`, moved with the arrow keys), stating the
  true difference: "2 months free" when that is the discount. It changes
  every price, period and note together, and says both the monthly figure
  and what is billed ("[Price] a month, billed yearly as [Total]").
- The currency is plain to the audience: a symbol that cannot be mistaken
  ("US$", "A$", "Rp") or the ISO code. Format with
  `Intl.NumberFormat(locale, { style: "currency", currency })`; rupiah
  prices usually without decimals (`maximumFractionDigits: 0`), since the
  default shows two. A currency switcher only when the business sells in
  several; never a silent conversion.
- Say whether tax is included. Consumer prices in the EU and the UK include
  VAT; business plans may say "Excl. VAT"; in Indonesia say whether PPN is
  included. The total at checkout matches the page.
- Per-seat prices show the price per seat and a seat count that works out
  the total.

## 5. Comparison table

- For detailed differences: features in groups (Projects, Collaboration,
  Security, Support), each group a header row, each feature a row header
  (`th scope="row"`); the plan names with their price and button as a
  sticky header row (`ui-part-tables`).
- Cells: a check icon with visually hidden "Included", a dash with "Not
  included", or the value itself ("10 GB", "Email, next working day").
  Never colour alone.
- On phones: a switch choosing which plan to show beside the features, or
  one list per plan; the first column sticky if the table scrolls sideways.

## 6. Honesty

- No fake strike-through prices or countdowns. Crossed-out prices that were
  never charged are unlawful in many places; in the EU a price reduction
  must state the lowest price of the previous 30 days.
- No "Only 3 spots left", no timers, no add-ons ticked in advance. "Free"
  only when it costs nothing, with its limits said. A trial's length and
  whether it needs a card, only when true.
- An enterprise or "Contact sales" option only when the business really
  sells one; what happens after the form ("A reply within one working
  day") only when true.
- A billing FAQ with real answers: changing plans, cancelling, refunds,
  invoices, payment methods, tax (`ui-part-faq`).
- `Product` and `Offer` structured data only with the real values shown on
  the page (`frontend-seo`).

## 7. Phones, themes and motion

- Plans stack in one column with the recommended plan first, or sit in a
  row with scroll snap where the next card visibly peeks. Prices never
  wrap; buttons are 44px tall and full width.
- Themes: the recommended border and the check icons reach 3:1 in both
  themes (`ui-themes`).
- Motion: none needed. Prices change at once when the period switches (a
  100ms fade at most) and never count up; cards do not lift on hover
  (`motion-interface`).

## 8. A sketch

```html
<fieldset class="period">
  <legend class="visually-hidden">Billing period</legend>
  <label><input type="radio" name="period" value="month" checked> Monthly</label>
  <label><input type="radio" name="period" value="year"> Yearly, [true discount]</label>
</fieldset>

<ul class="plans" role="list">
  <li class="plan" data-recommended>
    <h3>[Plan name] <span class="plan-flag">Recommended for [reason]</span></h3>
    <p class="plan-for">[Who it is for, in one line]</p>
    <p class="plan-price">
      <span class="amount">[Price]</span> per month
      <small>[Billing note, tax]</small>
    </p>
    <a class="button button-primary" href="/signup?plan=[id]">Start with [Plan name]</a>
    <ul class="plan-features" role="list">
      <li>[Feature, with its limit]</li>
    </ul>
  </li>
</ul>
```

```css
.plans {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
  gap: var(--space-5);
}
.plan {
  display: grid;
  grid-row: span 5;
  grid-template-rows: subgrid; /* name, audience, price, button, features line up */
  gap: var(--space-3);
  padding: var(--space-6);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}
.plan[data-recommended] { border-color: var(--accent); }
.amount { font-size: var(--font-3xl); font-variant-numeric: tabular-nums; white-space: nowrap; }
```

## Check it

- Trace every price, plan name, limit and discount to the brief or the
  business; list each placeholder in your report.
- `ui_check`: `invented-figure` ("10,000+ customers", "99.9%"),
  `generic-action` ("Get Started").
- `preview` at 360, 768 and 1440px: prices do not wrap or overflow, the
  comparison table scrolls in its own container, one filled button per view
  (it reports a primary repeated across the plans), muted notes and check
  icons pass contrast in both themes.
- Keyboard: the period switch moves with the arrow keys and every price,
  period and note changes with it; a screen reader reads each plan's name,
  price and period in order.

## Avoid

Three columns by default; "Most popular" on the middle plan with no basis;
crossed-out prices that were never charged; countdowns and invented
scarcity; "Save 20%" that is not the real difference; prices without a
currency, a period or a word on tax; a lone card for a single plan;
features in a different order in each plan; a check on every line; a
glowing, scaled-up middle card; an enterprise tier that does not exist;
invented prices where `[Price]` belongs.
