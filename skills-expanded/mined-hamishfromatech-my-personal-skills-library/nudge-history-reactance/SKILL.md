---
name: nudge-history-reactance
description: Applies the Peking University online randomized trial (Yang et al., npj Digital Medicine, Aug 18 2026; N=2,167 older adults, 7 nudge arms) showing nudges are HISTORY-DEPENDENT — video nudges raised influenza-vaccination willingness among the unvaccinated (especially side-effect-worried) while most nudge types NEGATIVELY associated with willingness among the previously vaccinated, read as psychological reactance — as the design rule for history-aware nudge gating. Use when [designing notification/nudge systems where users have prior exposure to the target behavior, deciding whether to suppress nudges for converted users, diagnosing why a nudge backfired for a user segment, or designing re-engagement vs anti-annoyance policies in AI products]. NOT for [clinical vaccination advice or dosing, one-time first-exposure nudges where no history exists, or claims that survey willingness equals actual vaccination uptake].
---

# Nudge History Reactance: When Conversion Makes Nudges Backfire

## Overview
A community/web-based randomized trial in Lanzhou New Area, China (March 2025; published npj Digital Medicine, Aug 18 2026; N=2,167 adults 60+, eight parallel arms, 80 family-doctor teams, ≥20 household surveys each) tested seven nudge methods vs control for influenza-vaccination willingness. Headline: overall willingness was low (19.20%), and the same nudges produced OPPOSITE effects by vaccination history — video nudges significantly increased willingness among the UNVACCINATED (strongest among those worried about side effects), while for PREVIOUSLY VACCINATED participants most nudge methods were NEGATIVELY associated with willingness, with the effect strongest in those without prior influenza experience. The authors' interpretation: indiscriminate application to previously vaccinated individuals may paradoxically REDUCE willingness through psychological reactance.

## The Evidence Base
- **Yang, Hu, Huang, Wang, Zhang, Jiang, Pang, Fu, Chen & Guo** — "An online randomized trial of electronic nudges for influenza vaccination willingness among older Chinese adults," *npj Digital Medicine*, published Aug 18 2026 (DOI 10.1038/s41746-026-03128-w), open access.
- **Design:** eight parallel arms (7 nudge methods + 1 control), online randomization via community health centers, older-adult sample (60+), Beijing Natural Science Foundation funded.
- **Key facts:** overall willingness 19.20%; no-prior-influenza-experience participants less willing to vaccinate; video nudge significant and positive for the unvaccinated, particularly those worried about side effects; previously vaccinated participants showed negative associations with most nudges.
- **Outcome caveat (name it every time):** this measures WILLINGNESS, not actual uptake. Willingness is an intermediate outcome — cite it as such, never as vaccination behavior.
- **Mechanism:** reactance is the leading candidate for the negative arm among the converted — nudging people who have already done the thing implies their past choice needs correction, inviting pushback. This is the mirror image of the reminder-WTP finding (simple reminders create their own demand): reminders aimed at people who no longer need the reminder destroy value.

## Core Findings (the three laws)
1. **Nudge effects are history-dependent.** The same message helps the unconverted and repels the converted. A nudge policy without a user-history dimension is half-designed; segment by prior action BEFORE choosing the nudge.
2. **Suppress, don't nudge, the converted.** For users who already performed the target behavior, the highest-value intervention is usually silence or a different goal — the default is DO NOT nudge, with opt-in reinforcement as the exception.
3. **History interacts with concern.** The video nudge worked best for the worried unvaccinated — concern is the engagement gate, prior action is the reactance gate. Diagnose both before selecting the intervention class.

## When to Use
- Notification and reminder systems for apps with long user histories (AI assistants included).
- Retention campaigns: deciding which cohorts get re-engagement nudges vs suppression.
- Diagnosing a nudge that "backfired": check whether the segment it repelled was the converted one.
- Anti-annoyance policy design (frequency capping by history, not just by volume).

## NOT For
- Clinical recommendations (this is willingness, not clinical uptake; and it's a single older-adult population).
- First-touch nudges for brand-new users (no history to gate on).
- Generalizing reactance to all reminder contexts — the reminder-WTP evidence shows simple reminders can compound; the difference here is the converted-audience posture.

## Core Process / Workflow
1. **Add a history dimension to the nudge policy.** For every nudge type, define: who is eligible (never-done vs done-before), and what the default is for the done-before group (usually: none).
2. **Gate by prior action, then by concern.** History gate first (reactance risk), then barrier/concern diagnosis (which nudge class fits the unconverted).
3. **Pre-register the backfire test.** Include the previously-converted cohort in every nudge experiment and test for negative effects — most teams only measure the unconverted and miss the harm.
4. **Design the exit, not just the entry.** For converted users, replace nudges with quiet reinforcement (receipts, status pages, thank-you states) — communication that doesn't ask for re-decision.
5. **Watch for the timing shift.** If nudge-induced uptake merely shifts WHEN people act (the youth-financial-education RCT pattern), suppress re-nudging after the action to avoid pure annoyance.

## A-Tech Alignment
- **Open source:** replicable A/B pattern; the eight-arm randomized design is directly reusable in open analytics stacks.
- **Privacy:** history-gating requires user-state tracking — keep it first-party and purpose-limited; the gating signal (prior action) is minimal data, not profiling.
- **Financial freedom:** unnecessary nudges to converted users burn trust that costs retention revenue; suppressing them is a free policy change.
- **Practical:** the history-gate table (nudge type × user state × default action) is a one-page addition to any notification design system.

## References
- Pairs with: `nudge-complementarity-benefit-cost` (this cycle — pair the right components AND the right audience), `reminder-wtp-information-penalty` (the compounding-reminder result among NEEDERS — this is the reactance result among the CONVERTED; together they define when reminders help vs hurt), `engagement-gated-nudge-effectiveness-2026` (engagement as the gate), `belief-profile-targeting-rct` (friction diagnosis before intervention choice), `nudge-effectiveness-reality-check` (small-effects calibration), `cross-cultural-llm-personalized-nudge-design` (personalized nudge design).