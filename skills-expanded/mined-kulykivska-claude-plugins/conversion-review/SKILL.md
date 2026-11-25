---
name: conversion-review
description: >-
  Audit a page, screen, screenshot, artifact or URL against conversion
  heuristics: value proposition on the first screen, one primary action per
  screen, proof, sign-up and checkout friction, trust, pricing clarity and
  mobile. Returns prioritized findings, each with the fix, a severity and the
  metric or event that would prove it. Trigger on "conversion review", "why
  does nobody sign up", "audit this landing page", "review this pricing
  page", "will this page sell", "check the funnel on this screen", or before
  shipping any page whose job is to get a sign-up or a payment.
---

# Conversion review

**Product name.** `{{app}}` here and in the references stands for the user's product. Take its name from the project (README title, package.json, app.json, Info.plist) or ask once, then write every example with that name and the product's own screens.

A page that sells answers three questions in the first five seconds: what is
this, is it for me, what do I do next. Everything below checks whether the
page answers them, and then whether anything between "yes" and "paid" gets in
the way.

## Inputs

Accept any of: a live URL (fetch it, and fetch it again with a phone user
agent), a screenshot or several, a published artifact, or the source files of
the page. Ask one question if it is missing: **what is the one action this
page exists to get** (sign up, start trial, buy Pro, install the app). Without
it every finding is a guess.

If the project has analytics, read the event names before writing findings,
so the "prove it" column uses events that exist or names the one to add.

## The pass

Walk the page top to bottom once, then the path to payment once. Score each
heuristic; details and examples for each are in
`references/heuristics.md`.

1. **First screen (above the fold, at 390x844 and at 1440x900).** A headline
   that states the outcome in the visitor's words, a subline that says for
   whom, one visible primary action, one piece of proof. A logo, a slogan and
   a carousel is not a value proposition.
2. **One primary action per screen.** Exactly one filled button per viewport.
   Secondary actions are links or outlined. Two equal buttons split the click.
3. **Proof.** Specific, checkable, near the claim: a public track record
   ({{app}}: every past prediction next to the actual result, including the
   misses), numbers with a date, named users, press. Unverifiable superlatives
   count as zero proof.
4. **Friction to sign-up.** Count fields, screens and decisions between the
   primary action and value. Social sign-in offered, email verification not
   blocking the first use, no credit card for a free tier, no account wall in
   front of the thing the page promised.
5. **Friction to checkout.** Price visible before the checkout form, the
   store's native sheet on mobile (Apple Pay, StoreKit), no re-entry of data
   already known, errors inline and recoverable.
6. **Trust.** Who is behind it, how to cancel, refund terms, privacy in one
   sentence, working contact. Broken images, lorem ipsum, a stale copyright
   year and a 2019 changelog all cost trust.
7. **Pricing clarity.** What the free tier gets, what Pro adds, the total
   charged and the billing period in the same place. See the
   `paywall-and-pricing` skill for the full gate and pricing checks.
8. **Mobile.** Thumb-reachable primary action, 44pt targets, no horizontal
   scroll, text readable without zoom, the page loads its first screen fast
   on a mid-range phone (LCP under 2.5 s).
9. **Speed and stability.** Layout shift when fonts or images load, spinners
   in place of content, a hero that waits on JavaScript.
10. **Copy.** Jargon on a page for newcomers (see the `ux-copy` skill), a
    call to action that describes the click ("Continue") instead of the
    outcome ("See this weekend's prediction").

## Severity

- **Blocker**: stops a willing visitor from converting (broken checkout, no
  price anywhere, primary action off-screen on mobile, an account wall before
  any value).
- **Major**: measurably lowers conversion for most visitors (no proof, two
  competing primary actions, vague headline, card required for a free tier).
- **Minor**: polish that compounds (weak microcopy, one extra field, slow
  secondary image).

Rank by severity, then by how many visitors hit it (first screen beats
footer), then by effort (cheap fixes first within a tier).

## Output

One table, then the notes.

| # | Where | Finding | Fix | Severity | Proves it |
|---|-------|---------|-----|----------|-----------|
| 1 | Hero, mobile | Primary action below the fold at 390x844 | Move "See this weekend's prediction" above the hero image; image becomes background | Blocker | `landing_cta_tap / landing_view` up; scroll-depth before first tap down |

Rules for the table:

- **Fix** is concrete enough to implement without a meeting: the new copy,
  the element to move, the field to delete.
- **Proves it** names an event or ratio. Use the project's taxonomy; when an
  event does not exist, write it as `new: <event_name>` and say what fires
  it. Every event plan covers entry, success, failure and drop-out.
- Do not list more than 15 findings. If there are more, the page needs the
  `landing-builder` skill, not a review.

After the table: **Top three to ship first** (one line each), then **What
this review could not see** (logged-in states, real traffic mix, load under
real network), then **Open questions**.

## Rules

- Honest conversion only. Never recommend a pattern listed as forbidden in
  `paywall-and-pricing` (fake scarcity, confirm-shaming, hidden cancellation
  and the rest), even when it would move the number.
- Review what is on the page, not what the team meant. If a claim needs
  context to be true, the page needs the context.
- A hypothesis is not a finding. "Users might prefer a video" goes to the A/B
  plan in `landing-builder`, not into the table.
