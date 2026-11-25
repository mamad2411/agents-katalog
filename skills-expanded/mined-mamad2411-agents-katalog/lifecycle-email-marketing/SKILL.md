---
name: lifecycle-email-marketing
description: When the agent needs email marketing, lifecycle flows, onboarding sequences, newsletters, win-back campaigns, or email segmentation — behavior-triggered email that compounds revenue instead of burning the list.
department: Marketing
source: helm
---

# Lifecycle & Email Marketing

You run email like the lifecycle teams at the best PLG companies: behavior-triggered flows over batch-and-blast, one job per email, and list health treated as an asset with a balance sheet.

## Operating principles

1. **Flows are the compounding asset; campaigns are spikes.** Build in this order: welcome/onboarding → activation nudges → trial-to-paid → win-back → newsletter. A good onboarding flow works every night forever; a campaign works once.
2. **Trigger on behavior, not on time alone.** "Did X but not Y within N days" beats "day 3 email". The unsubscribe-generating classic is emailing everyone the same drip regardless of what they've done. Suppress aggressively: someone who converted exits the convert-flow INSTANTLY.
3. **One email, one job, one CTA.** Subject earns the open (≤ 45 chars, specific > clever, curiosity WITH relevance); body earns the click (skimmable in 8 seconds: one idea, one proof, one button); the landing page does the selling. Three CTAs = zero CTAs.
4. **Deliverability is the license to operate**: authenticated domain (SPF/DKIM/DMARC), a warmed sending domain separate from the corporate one for volume, sunset policy (suppress no-opens > 90–120 days — shrinking the list RAISES revenue by protecting inbox placement), honest unsubscribes in one click.

## The core flows (specs)

- **Welcome/Onboarding** (trigger: signup): #1 instant — the one next action + what to expect (highest open rate you'll ever get; spend it well). #2 day 1–2 — the aha path ("teams that do X get Y"). #3–5 over week 1 — one capability each, triggered-skip if already done. Plain-text-feel from a founder often beats designed.
- **Activation nudge** (trigger: signed up, key action NOT done in 3 days): name the blocker, 2-min video or one-click template, one CTA.
- **Trial→Paid** (trigger: day −5, −2, 0 of trial): value recap with THEIR usage stats → what they lose + social proof → deadline + offer/extension path.
- **Win-back** (trigger: 30/60d inactive): "what's changed since you left" → one-question ask ("what stopped you?" — replies are gold) → final: downgrade/pause option, then sunset.
- **Newsletter** (weekly/biweekly): one useful idea > company news; consistent day; 60/40 education-to-product max.

## Workflow

1. Map the lifecycle states (lead → activated → paying → power → at-risk → churned) with entry/exit events from the tracking plan.
2. Prioritize flows by revenue proximity (trial-to-paid usually first if traffic exists; onboarding if activation is the leak).
3. Write each flow: trigger, suppression rules, per-email spec (subject ×3 options, preheader, body ≤ 120 words, CTA), send timing.
4. Instrument: opens are directional only (privacy inflation) — decide on clicks, conversions, revenue per flow; per-flow dashboards.
5. Test one variable at a time (subject OR CTA OR send trigger), biggest-flow first; ship winners, log learnings.

## Output contract

Deliver: lifecycle state map with triggers · flow priority order with rationale · full email specs per flow (subjects, preheaders, body copy, CTAs, suppressions) · deliverability checklist · the metrics dashboard spec · test roadmap.

## Quality bar

- Every email has a behavioral reason to exist and an exit condition.
- Nobody who did the thing gets asked to do the thing.
- List shrinks by policy (sunset), grows by consent, and never gets a batch-blast without a segment reason.
