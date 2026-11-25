---
name: onboarding
description: "Post-signup onboarding, activation, first-run experience and time-to-value. Use when users sign up but do not activate, or for onboarding checklists and empty states."
metadata:
  version: 2.0.1
---

# Onboarding CRO

Get users to their aha moment fast and set up the habit behind retention. Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`) first when it exists. Ask only what is missing: product type (B2B or B2C) and core value, the activation event, what happens after signup, where users drop off.

## Principles

1. **Time-to-value.** Remove every step between signup and core value. Design the Minimum Path to Value, the fewest steps to enough value for a confident decision: [references/minimum-path-to-value.md](references/minimum-path-to-value.md) (inventory, remove, reconstruct; abandonment benchmarks; Stripe, Calendly, Notion patterns).
2. **One goal per session.** Hold advanced features for later.
3. **Do, don't show.** An interactive step beats a tutorial.
4. **Visible progress.** Start progress already begun (endowed progress), end each session on a win (peak-end), keep tasks at the edge of ability, and treat each stall as a missing motivation, ability or prompt (Fogg). Add boosters (pre-filled data, templates, quick wins) and remove blockers (required fields, dead ends, blank screens). Detail and the 10-component toolkit (welcome forms, drip emails, skippable tutorials, checklists, empty states and more): [references/psychology-and-toolkit.md](references/psychology-and-toolkit.md).

Use the fewest components that reach value.

## Define activation

Judge by lead-to-customer conversion and 90-day retention, not signup volume. Choose the activation model (freemium, free trial, paid trial, money-back, consultation) before designing the flow; it shapes the path: [references/activation-models.md](references/activation-models.md).

The aha moment is the action that correlates most with retention. Compare what retained users did that churned users did not, and find the earliest such signal. Examples: project tool (first project plus a teammate), analytics (tracking installed plus first report), design tool (first design plus export or share), marketplace (first transaction). Use the user's real behavioral data to confirm; name it as a hypothesis when none exists.

## Flow decisions

First 30 seconds, pick by product:
- **Product-first** for simple, B2C, mobile (risk: blank-slate overwhelm).
- **Guided setup** when personalization is needed (risk: friction before value).
- **Value-first** with demo data (risk: feels unreal).

Whichever: one clear next action, no dead ends, progress shown if multi-step.

- **Checklist** (multi-step setup, several features to discover, self-serve B2B): 3 to 7 items, highest value first, quick wins first, progress percentage, celebration at the end, dismissable.
- **Empty states** explain the area, show it with data, offer one primary action to add the first item, optionally with example data.
- **Tours** for complex UI only: 3 to 5 steps, dismissable any time, never repeated for returning users.
- **Email** reinforces in-app actions with a specific CTA, personalized by actions taken: welcome (immediate), incomplete onboarding (24h, 72h), activation achieved, feature discovery (days 3, 7, 14).
- **Stalled users**: define stalled (X days inactive, setup incomplete), then reminder email, in-app "pick up where you left off", personal outreach for high-value accounts.

More detail and key steps by product type (B2B SaaS, marketplace, mobile, content): [references/flow-patterns.md](references/flow-patterns.md).

## Measure

Activation rate, time to activation, steps to activation, onboarding completion, day 1/7/30 retention, activation by cohort and source. Track drop-off per step (signup, step 1, step 2, activation, retention) and fix the biggest drop first.

## Output

- **Audit**: finding, impact, recommendation, priority.
- **Flow design**: activation goal, step-by-step flow, checklist items, empty state copy, email triggers, metrics plan.

Experiment ideas (flow simplification, progress mechanics, personalization, help availability): [references/experiments.md](references/experiments.md).

Related: `signup` for the step before; `paywalls` for converting to paid during or after onboarding.
