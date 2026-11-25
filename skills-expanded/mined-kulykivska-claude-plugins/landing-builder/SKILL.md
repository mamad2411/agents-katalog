---
name: landing-builder
description: >-
  Write the structure and copy for a selling landing page: hero, proof,
  features as outcomes, pricing, FAQ and a final call to action, with
  variants per audience and an A/B test plan. Trigger on "write a landing
  page", "landing for", "homepage copy", "page for teams", "page for
  bookmakers", "B2B landing", "rewrite the hero", "A/B test the landing", or
  when a product or feature needs a page whose job is to sell.
---

# Landing builder

**Product name.** `{{app}}` here and in the references stands for the user's product. Take its name from the project (README title, package.json, app.json, Info.plist) or ask once, then write every example with that name and the product's own screens.

A landing page is an argument with one conclusion: the primary action. Each
section answers the next objection a visitor would raise. Write it in that
order, not in the order the product was built.

## Step 1: brief (ask, max four questions)

1. **Audience**: who lands here and from where (search, a social post, an ad,
   a partner link). One page per audience that differs in need, not per
   channel.
2. **Primary action**: one (start free, start trial, book a demo, install).
3. **Proof available**: what can be shown and checked today.
4. **Constraints**: brand voice, legal claims that are off-limits (for a
   betting-adjacent product: no promises of winnings, age and jurisdiction
   notices where required).

## Step 2: the section order

| # | Section | Job | Rule |
|---|---------|-----|------|
| 1 | Hero | What, for whom, what next | Outcome headline under 10 words, subline naming the audience, one primary button, one proof point, a real product visual |
| 2 | Proof strip | Believe it | The strongest checkable proof (public track record, numbers with dates, logos with permission) |
| 3 | How it works | Understand it | Three steps, each an action the user takes |
| 4 | Outcomes | Want it | Features written as results: "Know the grid before qualifying" not "Qualifying model v3" |
| 5 | Deep proof | Trust it | A real example: last race's prediction next to the result, misses included |
| 6 | Pricing | Afford it | Free and paid side by side; follow `paywall-and-pricing` |
| 7 | FAQ | Remove the last objection | Five to eight real questions from support, sales or reviews |
| 8 | Final call to action | Act | Repeat the primary action with the objection it answers ("Free, no card") |

Drop a section only with a reason. Add none that does not answer an
objection.

## Step 3: variants per audience

Same product, different job to be done. Change the headline, proof, outcomes
and primary action; keep the design system and pricing logic.

{{app}} example (full copy in `references/section-templates.md`):

| | Fans | Teams and analysts | Bookmakers and media |
|---|------|--------------------|----------------------|
| Job | Know what will happen, enjoy the weekend more | Faster, checkable pace and strategy reads | Reliable probabilities to publish or price against |
| Hero | "Know the result before the lights go out" | "Race predictions your engineers can audit" | "Calibrated F1 probabilities, delivered by API" |
| Proof | Public track record, app rating | Methodology page, per-session error, backtests | Calibration chart, uptime, latency, data licence |
| Primary action | Get the free prediction | Book a 20-minute walkthrough | Request API access |
| Pricing | Free and Pro | Team plan | Contact, volume based |

Rules for variants:

- Separate URLs per audience with their own title and meta description (so
  search and ads can land each audience on its page), shared components.
- Never claim to a B2B audience what the product cannot deliver today;
  "coming soon" goes into a waitlist action, not into the outcomes list.
- Regulated audiences get the compliance lines they expect (responsible
  gambling link, licensing questions answered in the FAQ).

## Step 4: copy rules

- Headlines state the outcome; sublines say who it is for and how.
- Numbers beat adjectives; every number has a date and a source link.
- Jargon only on the audience page that uses it (MAE is fine for analysts,
  not for fans); run all copy through the `ux-copy` skill, which also hands
  it to the `humanizer`.
- No em dashes, no emojis, no exclamation marks in headlines.
- Buttons name the result of the click.

## Step 5: A/B test plan

One hypothesis per test, written before building it:

```
Because <evidence>, we believe <change> for <audience>
will increase <primary metric>, without hurting <guardrail>.
```

- **Primary metric**: the page's goal event per unique visitor (for example
  `signup_success / landing_view`), not clicks.
- **Guardrails**: bounce rate, downstream activation (the free prediction
  actually viewed), refund or cancel rate for paid actions.
- **Sample size**: for a baseline rate p and the smallest lift worth
  detecting d (absolute), each arm needs about `16 * p * (1 - p) / d^2`
  visitors for 80% power at 5% significance. At p = 4% and d = 1 point that
  is about 6,100 per arm. If traffic cannot reach it in four weeks, test a
  bigger change or skip the test and ship the better-argued version.
- **Duration**: whole cycles. For a weekly-event product, at least two full
  event cycles, because race-weekend visitors behave unlike weekday ones.
- **No peeking**: decide the stopping point in advance; do not stop on the
  first significant day.
- **Order of tests**: hero headline, then proof block position, then primary
  action wording, then pricing presentation. Big levers first.

Events: `landing_view{variant, audience, source}`,
`landing_cta_tap{variant, position}`, `landing_section_view{section}`, and
the goal event with `variant` as a property. Assignment is sticky per
visitor and logged once as `experiment_exposure{experiment, variant}`.

## Output

1. Brief (the four answers).
2. The page per audience: every section with final copy, the visual for the
   hero, and notes for the designer.
3. Meta title and description per variant.
4. The A/B plan: hypotheses in priority order, metrics, sample size,
   duration.
5. **Open questions**: proof that does not exist yet, legal lines to confirm.

For the visual design of the page, hand the copy to the `redesign` flow in
the `ux-craft` plugin; the page is designed and approved before it is built.
