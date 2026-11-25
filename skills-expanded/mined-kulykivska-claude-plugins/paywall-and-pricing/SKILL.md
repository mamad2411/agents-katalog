---
name: paywall-and-pricing
description: >-
  Design paywalls, Pro gates and pricing pages that sell without annoying:
  partial or blurred previews instead of hard locks, anchoring and decoy
  tiers, the annual toggle, trial rules, upgrade moments tied to user
  success, copy patterns and what to measure. Honest by default, with an
  explicit list of forbidden dark patterns. Trigger on "design the paywall",
  "pricing page", "Pro gate", "how should we lock this feature", "upgrade
  screen", "trial or freemium", "annual vs monthly", "why is nobody buying
  Pro", or when reviewing any screen that asks for money.
---

# Paywall and pricing

**Product name.** `{{app}}` here and in the references stands for the user's product. Take its name from the project (README title, package.json, app.json, Info.plist) or ask once, then write every example with that name and the product's own screens.

A good gate shows the value, names the price, and lets the user say no
without punishment. People pay when they have just seen what they would get,
at a moment when they want more of it. Everything here serves that.

## Step 1: map the value before the gate

Write down, for the product, three lists. Nothing else in this skill works
without them.

- **Free forever**: what a free user gets. It must be good enough to come
  back for. ({{app}}: the race winner prediction and the public track
  record.)
- **Pro**: what paying adds, as outcomes. (Full finishing order, qualifying
  and sprint predictions, per-driver probabilities, alerts before lights
  out.)
- **Success moments**: when a user has just got value. (Their followed
  driver finished where the prediction said; they opened the app three race
  weekends in a row; they shared a prediction.)

## Step 2: choose the gate for each Pro surface

Decision rule, in order:

1. Can the user see the **shape** of the value without the value itself? Use
   a **partial preview**: show the top 3 of 20, the first row of the table,
   one driver of the grid, the chart without its axis values. Default choice.
2. Is the value a number or a list whose layout alone sells it? Use a
   **blurred preview** with the real layout and real length, blurred or
   replaced by placeholder bars. Never blur fake data that looks better than
   the real one.
3. Is it an action rather than content (alerts, export, API)? Show the
   control in place, enabled, and open the paywall sheet on tap, with the
   context of what they tried to do.
4. **Hard lock** (a padlock and nothing else) only when a preview would leak
   the value itself. Rare.

Gates live in one shared component per platform, never ad-hoc checks per
screen, and free content stays visible to crawlers (see the `seo` plugin for
gating and indexing).

## Step 3: the upgrade moment

Show the paywall **after** a success moment or **at** the moment of intent
(the user tapped a locked thing), never on cold launch, never in the middle
of a task, never twice in one session unprompted.

- Soft prompt (inline card, dismissible) after a success moment: "Your pick
  for Hamilton was right. Pro shows the full order for every session."
- Full paywall sheet only on intent: a tap on a gated control or on "Go Pro".
- Frequency cap: one unprompted upgrade prompt per user per week, zero during
  onboarding, zero in the first session.
- After "Not now", the same prompt stays away for at least 7 days.

## Step 4: the paywall and pricing page

Layout that works on a sheet and on a page:

1. Headline naming the outcome, tied to where they came from ("See the full
   grid for Sunday").
2. Three to five outcome bullets, no feature codes.
3. Plans: two or three tiers. Anchor with the highest first on the web or
   with the annual price shown against twelve monthly payments. A decoy tier
   is fine when it is a real, sellable plan; it is a dark pattern when it
   exists only to be bad.
4. **Annual toggle**: default to the plan most users should pick. Show the
   total charged ("$39.99 per year"), then the equivalent ("$3.33 a month,
   2 months free"). The saving is computed from the real monthly price.
5. One primary button that names the outcome and the terms: "Start 7-day free
   trial", with "then $39.99 per year, cancel any time" directly under it in
   readable size.
6. Proof: track record, rating, one quote.
7. "Restore purchases" (required on iOS), terms, privacy, and a clear close
   control of normal size in the usual corner.

Copy patterns and full examples are in `references/patterns.md`.

## Step 5: trial rules

- Trial length matches the product rhythm: a sports product with weekly
  events needs a trial that covers at least one full event (7 days minimum;
  a race weekend trial starts on Thursday, not Sunday night).
- Say at start what happens at the end: the date, the amount, how to cancel.
- Remind before the charge (24 to 48 hours ahead), on the channel the user
  chose, with a one-tap cancel path.
- One trial per person. Do not offer a trial to someone who just cancelled;
  offer to come back instead.
- On iOS, use the store's introductory offer mechanics and its trial
  eligibility, not a home-made trial.

## Forbidden: dark patterns

Never design, recommend or approve any of these, even when asked for "more
conversion". If an existing screen has one, it is a Blocker finding.

- **Fake scarcity or urgency**: countdowns that reset, "only 3 spots left"
  for a digital product, "price goes up tonight" that does not.
- **Confirm-shaming**: "No thanks, I like being wrong about races."
- **Hidden or hard cancellation**: cancel buried in support email, a phone
  call, or more steps than sign-up took. Cancel must be as easy as buying.
- **Silent trial conversion**: no reminder, no date, terms in grey 9 pt.
- **Disguised price**: only a per-week or per-day figure for an annual
  charge; the charged total missing or smaller than the equivalent.
- **Pre-checked add-ons** and anything sneaked into the basket.
- **Tiny or hidden close button**, a close that appears after a delay, or a
  paywall that cannot be dismissed on a free feature.
- **Nagging**: the same prompt after every action, prompts that ignore "Not
  now".
- **Bait and switch**: a free feature moved behind the paywall without
  notice for existing users; fake blurred data better than the real data.
- **Fake social proof**: invented counts, reviews or "people are viewing".
- **Guilt or fear copy** about losing data, streaks or accuracy if they do
  not pay.

## Step 6: what to measure

Instrument before launch. Every surface reports entry, success, failure and
drop-out.

- `paywall_view{surface, trigger, variant}` and `paywall_dismiss{surface}`
- `paywall_cta_tap{plan, period}`, `plan_toggle{period}`
- `checkout_start`, `purchase_success{plan, period, trial}`,
  `purchase_fail{reason}`, `purchase_cancel_in_sheet`
- `trial_start`, `trial_reminder_sent`, `trial_convert`, `trial_cancel`
- `restore_tap`, `restore_success`, `restore_fail`
- `subscription_cancel{reason}`, `refund`

Ratios: view to purchase per surface and trigger; trial to paid; 30 and 90
day retention of payers; ARPU per visitor. Guardrails that must not get
worse while conversion goes up: refund rate, cancellations within 48 hours,
store rating, support tickets about billing, free-user 7-day retention.

## Output

For a design request: the value map, a gate choice per surface, the paywall
layout with final copy (run it through the `ux-copy` skill), the trial rules,
the event list, and one A/B test to start with. For a review: findings in
the `conversion-review` table format, with dark patterns always first.
