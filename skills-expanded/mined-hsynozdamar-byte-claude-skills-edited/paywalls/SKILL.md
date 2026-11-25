---
name: paywalls
description: "In-app paywalls, upgrade screens, upsell modals and feature gates. Use when asking users to upgrade inside the product. Not for public pricing pages."
metadata:
  version: 2.0.0
---

# Paywall and Upgrade Screen CRO

Convert free users to paid, or paid to higher tiers, at the moment they have felt enough value. Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`) first when it exists. Ask only what is missing: upgrade type (freemium to paid, trial to paid, tier upgrade, feature upsell, usage limit), what is free vs gated, current conversion, what triggers prompts, the user's aha moment, pricing model (seat, usage, flat), and mobile, web or both.

iOS and Android paywalls and IAP follow store rules.

## Principles

- **Value before ask.** Show it after the aha moment, as the natural next step.
- **Show, don't tell.** Preview the paid feature so the upgrade feels tangible.
- **Frictionless path.** Pricing is one tap away when they are ready.
- **Respect the no.** Continuing free stays easy, which keeps trust for a later conversion.

## Trigger points

- **Feature gate** (paid-only click): say why it is paid, show what it does, quick unlock, option to continue without.
- **Usage limit**: state the limit reached, show what upgrading provides, never block abruptly.
- **Trial expiry**: warn at 7, 3 and 1 days, say what happens on expiry, summarize value received.
- **Time-based**: a gentle reminder after X days of free use that highlights unused paid features and dismisses easily.

## Screen anatomy

Headline on what they get ("Unlock [Feature] to [Benefit]"), a value demonstration (preview, before/after), key plan differences with the current plan marked, simple pricing with annual vs monthly, social proof from real customers, a specific CTA ("Start Getting [Benefit]"), and a clear escape ("Not now" or "Continue with Free"). Text wireframes for feature-lock, usage-limit and trial-expiry screens: [references/layouts.md](references/layouts.md).

## Timing and frequency

- Show: after the value moment and before frustration, after activation, at genuine limits.
- Hold back: during onboarding, mid-flow, and repeatedly after a dismissal.
- Cap prompts per session, cool down for days (not hours) after a dismiss, and watch annoyance signals.

## Upgrade flow

Minimize steps from paywall to payment, stay in context, pre-fill known data. After upgrade: immediate access, confirmation and receipt, a guide to the newly unlocked features.

## Guardrails

Keep the close button visible, plan choice clear and copy free of guilt, since dark patterns erode trust and break store rules. Do not ask before value is delivered, prompt too often, block critical flows, or make upgrading complicated.

## Test and measure

Test trigger timing, headline and copy, price presentation, trial length, feature emphasis, layout. Track impression rate, click-through to upgrade, completion rate, revenue per user, and churn after upgrade. Ideas: [references/experiments.md](references/experiments.md).

Related: `onboarding` to reach the aha moment first; `cro` for public pricing pages.
