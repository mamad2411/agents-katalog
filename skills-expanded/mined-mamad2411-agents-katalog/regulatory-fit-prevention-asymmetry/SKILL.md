---
name: regulatory-fit-prevention-asymmetry
description: Applies the first large-N regulatory-fit field RCT for sustained volunteer engagement (Dekramanjian, Research Square / Mosquito Alert citizen-science platform, two-year trial N=600) — prevention-oriented individuals doubled engagement odds when message framing MATCHED their disposition (OR 1.91) while promotion-oriented individuals showed NO fit benefit, producing the prevention-asymmetry design rule. Use when designing engagement/retention messaging, choosing between aspirational and vigilance framing, or building citizen-science/volunteer/community platforms that must sustain participation across seasons. NOT for one-shot conversion funnels (this is a persistence/retention study), or for regulatory-focus personality segmentation without a validated scale (Regulatory Focus Scale, Fellner et al. 2007).
---

# Regulatory-Fit Nudges: The Prevention Asymmetry

## Overview
This is the first citizen-science field experiment to apply Regulatory Focus Theory (Higgins, 1997) to volunteer engagement. Over 52 days, 600 active Mosquito Alert users received 12 push notifications framed as EAGER (promotion: aspirations, rewards, "be at the forefront"), VIGILANT (prevention: safety, responsibility, "prevent the spread"), or NEUTRAL (control). Both motivated frames significantly outperformed neutral — but the **regulatory-fit effect showed a sharp asymmetry: prevention-oriented participants gained substantially from vigilance-framed messages while promotion-oriented participants gained nothing from matched eager framing.** This asymmetry is the skill: in risk-domain contexts, prevention-oriented users are the segment to target with regulatory-fit messaging; promotion-oriented users are driven by other factors.

## When to Use
- Designing retention/engagement messaging where users can opt out (community moderation, volunteer platforms, citizen science, open-source contribution ladders)
- Choosing between aspirational ("achieve/contribute") and vigilance ("protect/prevent") framing for a risk-domain audience
- Planning a seasonally-declining engagement curve (the intervention countered the typical annual drop)
- NOT for one-shot conversion funnels (this tests SUSTAINED participation)
- NOT for personality segmentation without an instrument (Regulatory Focus Scale; mis-segmentation wastes the fit effect)

## Core Process / Workflow
1. **Frame the goal state correctly**: citizen-science engagement is a *duty* (monitoring public health, preventing spread) — prevention framing is the natural majority orientation; eager framing works but produces no *fit* advantage for promotion-oriented individuals in this context.
2. **Measure, don't assume**: pre-register the Regulatory Focus Scale (Fellner et al., 2007) as a baseline moderator; if no scale is feasible, fall back on the *average* framing effect (both eager and vigilant beat neutral) and skip the fit layer.
3. **Match frame to disposition only where fit is measurable**: for prevention-oriented participants, vigilance-aligned nudges nearly DOUBLED the odds of reporting (OR 1.91). For promotion-oriented participants, no fit effect (p=.497) — do not build a fit-based segment for them.
4. **Budget for habituation**: the nudge effect decayed over the 52-day window (negative time-since-onset interaction), but reporting levels stabilized rather than collapsed — plan a cadence refresh or message rotation to counteract decay.
5. **Measure post-intervention persistence**: engagement gains partially held after the intervention ended (mean difference 0.87 reports, 95% CI [−0.18, 1.93]) — evidence that framing nudges can seed habits, not just momentary lifts.

## Key Evidence
- **Overall nudge effect**: receiving any motivated-framed notification increased odds of submitting a report the same day (β=0.353, p<.001, OR 1.42)
- **Eager framing**: β=0.45 (OR 1.57); **Vigilant framing**: β=0.37 (OR 1.45); both beat neutral (β=0.22, OR 1.25)
- **Prevention-orientation fit**: vigilance frame nearly doubles reporting odds for prevention-disposition participants (OR 1.91; 95% CI [1.20, 3.05])
- **Promotion-orientation asymmetry**: no significant fit effect (β=0.49, p=.497) — the regulatory-fit benefit is SEGMENT-SPECIFIC, not universal
- **Habituation**: negative effect of time-since-onset (β=−0.026, p<.001) — nudge effect fades over the intervention window
- **Persistence**: post-intervention decline not statistically significant (p=.106) — partial habit formation
- **Seasonality interaction**: nudge amplifies where environmental cues (mosquito season) make action salient

## Pairs with
`behavioral-intervention-choice-tailoring` (the choice-based alternative — this skill uses measurement-based tailoring; both show fit/selection drives engagement), `belief-profile-targeting-rct` (friction-type → intervention-type mapping — the same measurement-first logic), `llm-personalized-nudge-friction-boundary` (personalization boundary conditions in field RCTs), `climate-advocacy-megastudy-2026` (which interventions work on which audiences — megastudy scale), `engagement-gated-nudge-effectiveness-2026` (the engagement gate).

## A-Tech Alignment
- **Open source**: Mosquito Alert platform is open; the Regulatory Focus Scale is public; the nudge templates are published — replicable by any volunteer/community platform.
- **Privacy**: baseline-only segmentation (Regulatory Focus Scale at enrollment), no per-message behavioral profiling.
- **Financial freedom**: for a community/creator platform, prevention-fit messaging to the prevention-disposition segment can double retention contribution at near-zero marginal cost.
- **Practical**: the segment-specific fit rule is a two-arm A/B test any product team can run on their own notification channel.

*Source: Dekramanjian, B., "Regulatory-focus based nudges to sustain citizen science reporting: results from a two-year randomized trial" (Research Square preprint rs-8215000, March 2026); Mosquito Alert platform, N=600, two-year field trial, prevention-fit OR 1.91.*