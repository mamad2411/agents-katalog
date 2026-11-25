---
name: dsct-reconfiguration-reengagement-study
description: Applies the Detox nudge-reconfiguration quasi-experiment (Peña-Albert et al., JMIR Formative Research 2026;10:e85349; N=252 passive users) — a single reconfiguration prompt to users who had disabled nudges was accepted by 46%, lifting user-nudge interaction from 29.7% to 58.5% (DiD +36.3pp, P<.001) for ~2 weeks before converging with control; pre-existing configuration behaviors (21.5% shorter thresholds, fewer leisure goals) predicted acceptance while self-reports did not. Use when [designing re-engagement flows for lapsed users, evaluating behavioral-vs-self-report readiness signals, advising on digital self-control tool retention, or explaining the intention-behavior gap in app data]. NOT for [initial nudge design — use wellspent-customizable-screen-time-rct — or habit formation theory — use ai-nudging-habit-formation].
---

# Restoring Engagement: Nudge Reconfiguration Prompts in Digital Self-Control Tools

## Overview
Peña-Albert, Ingram, Khazaal, Litrico, Farah & Gillet (EPFL + HES-SO + Lausanne University Hospital; *JMIR Formative Research* 2026;10:e85349; published Apr 28, 2026) solve the retention problem that kills digital self-control tools (DSCTs): users who installed the tool, then **disabled their nudges**. In a device-level randomized quasi-experiment inside the Detox iOS app (N=252 passive users), the experimental group (n=138) received **one prompt during their daily check-in** inviting them to reconfigure nudge settings (suggested default: 10-minute consecutive-usage threshold + 1-minute cooldown). Control (n=114) got nothing.

**Results:**
- **46% (63/138) accepted.** The acceptance subgroup's 7-day user-nudge interaction ratio rose **29.7% → 58.5%** (peak 65% day 1); **DiD = +36.3 percentage points vs control, P<.001**. The rejection subgroup's decline was statistically indistinguishable from control (P=.82) — the prompt was not counterproductive.
- **Durability:** elevated engagement persisted ~2 weeks, converging with control by ~1 month. Single prompts start behavior; they don't sustain it.
- **Behavioral divergence predated the prompt:** accepters had preconfigured **21.5% shorter consecutive-usage thresholds** (P=.03; Cohen d widened −0.47 → −0.67 post-intervention) and were far less likely to select leisure-oriented daily goals (15.6% vs 26.2%, P=.001). Spillover to manual app blocking grew (d 0.39 → 0.49).

## The headline finding: behavioral indicators beat self-reports
No self-reported measure — screen-time goals, scrolling-regret frequency, emotional responses, even the post-prompt rationale survey — differed between accepters and rejecters (all P>.1). **Observable in-app behavior predicted intervention receptiveness; stated intentions did not.** This is the intention–behavior gap operationalized: DSCT configuration logs are free, continuous proxies for readiness-to-change that no survey can match.

## Design implications (the authors' implications, distilled)
1. **Engagement is a continuum, not a binary.** Nearly half of "passive" users were latent re-engagers. Proactive reconfiguration prompts beat accepting attrition as inevitable.
2. **Adaptive cadence beats single prompts.** The 1-month convergence argues for empirically-timed periodic re-engagement — and for readiness-based *predictive modeling* (configuration logs + temporal patterns → personalized prompt timing) rather than static threshold rules.
3. **Autonomy stays the floor.** SDT-grounded design: opt-in framing, adjustable parameters, transparent rationale. Extrinsic prompts cannot sustain what intrinsic motivation hasn't adopted.

## Key talking points
- The DiD design with device-level randomization and permutation tests — methodological rigor unusual in app-based behavioral research.
- The spillover effect: re-engaging one feature catalyzed broader self-regulatory behavior (manual blocking).
- The design implication for any nudge product: log configuration behavior; treat it as the readiness signal; follow up on short, vague intentions (intention entries under ~25 words rarely convert).

## Pairs with
`wellspent-customizable-screen-time-rct` (the initial-engagement companion — Wellspent starts the nudge, this skill restores it), `choice-closure-effect`, `co-designed-digital-nudging`, `consent-fatigue-progressive-permissioning` (privacy-side of re-engagement prompts).

## A-Tech alignment
- **Behavioral nudging + practical implementation:** a concrete, measurable re-engagement pattern any solo builder can implement (one prompt, one default, one log).
- **Data privacy:** behavioral indicators are first-party telemetry — usable without third-party trackers; the study's own data handling (tokenized, non-identifiable) models the compliant version.
- **Financial freedom:** retention flows directly to MRR for wellbeing-tool builders; the 46% acceptance rate quantifies the recoverable churn.

*Source: Peña-Albert, Ingram, Khazaal, Litrico, Farah & Gillet, "Restoring Engagement in Digital Self-Control Tools Using Nudge Reconfiguration Prompts: Quasi-Experimental Study," JMIR Form Res 2026;10:e85349. doi:10.2196/85349.*