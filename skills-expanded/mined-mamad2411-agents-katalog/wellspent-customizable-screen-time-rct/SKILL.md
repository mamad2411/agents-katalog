---
name: wellspent-customizable-screen-time-rct
description: Applies the Wellspent app randomized controlled trial (Mertens et al., JMIR mHealth 2026;14:e56824; 70 iPhone users, 3-week RCT) — customizable, autonomy-supportive digital self-control nudges cut screen time on the most problematic app by ~29 min/day (P<.001) and reduced perceived problematic smartphone use, while problematic social media use and self-efficacy did not move. Use when [designing screen-time or digital-wellbeing features, advising on autonomy-supportive behavior-change UX, evaluating self-nudge app designs, or explaining why behavioral outcomes move faster than cognitive ones]. NOT for [platform dark-pattern analysis — use digital-addiction-economics-2026 — or AI-driven personalization nudges — use ai-self-modeling-longitudinal-nudge].
---

# Wellspent: Customizable, Autonomy-Supportive Screen-Time Nudges (RCT Evidence)

## Overview
The most rigorous 2026 test of the self-nudge pattern the library has been tracking since the `one Sec` / Goldilocks-era skills. **Wellspent** (Mertens, Brockmeier, Roitzheim, Radtke, Dingler & Keller, *JMIR mHealth and uHealth* 2026;14:e56824; published Apr 8, 2026; trial DRKS00031767) is a customizable mobile intervention: users pick their problematic apps, set daily time limits and nudge intervals, and personalize the full-screen reminder's frequency, tone, and alternative activity. The design is explicitly **autonomy-supportive** (self-determination theory): reminders require active dismissal but **never block access** — the user decides whether to continue.

**Results (3-week RCT, N=70, preregistered):** daily screen time on the most problematic app fell ~**29 minutes/day** (estimate −29.35, 95% CI −42.79 to −15.99, P<.001); perceived problematic smartphone use decreased (P=.01). **No significant effect** on problematic social media use or self-efficacy. Behavioral change can move in days; cognitive/self-perception outcomes need longer, more reflective processes.

## The three design takeaways the authors name
1. **Moderate enforcement works.** Full-screen reminders that *offer a choice* reduce screen time without triggering reactance — friction at the moment of temptation beats restriction.
2. **Customization enhances acceptance.** Users who select target apps, limits, and reminder tone feel ownership; 78% voluntarily continued using the app in week 3. Configurability is the retention mechanism.
3. **Friction alone is not enough.** Self-efficacy and problem-use scores need reflective components (journaling, progress feedback, social accountability) — friction moves behavior faster than it moves minds.

## Honest caveats
- Small sample (70; primary-outcome analysis N=46), iOS-only, 26% attrition; the problematic-social-media-use effect reached significance only in adjusted models (fragile).
- Self-efficacy rose in *both* groups — in-the-moment friction lacks visible progress tracking, so mastery experiences don't accumulate.
- Reminder acceptance ≈ one-third of prompts; users raise nudge intervals when they want longer sessions — autonomy works both ways.

## Key talking points
- The dual-process frame: full-screen pause interrupts habitual System-1 scrolling; the quit-or-continue choice keeps System 2 in charge.
- BCT grounding (goal setting, prompts/cues, behavioral feedback, self-monitoring, substitution) — a template for evidence-based nudge design.
- Contrast with one-size-fits-all blockers: customization without coercion is the design space that clears an RCT.

## Pairs with
`digital-addiction-economics-2026`, `ai-nudging-habit-formation`, `behavioral-design-practical-playbooks`, `boosting-empowering-behavior-change` (boosts vs nudges framing — Wellspent is a boost delivered as a nudge).

## A-Tech alignment
- **Practical implementation:** a complete, replicable intervention pattern (defaults, thresholds, tone options) for privacy-respecting wellbeing tools.
- **Behavioral nudging:** the cleanest 2026 evidence that user-defined nudges beat imposed ones.
- **Open source ethos:** the R code is published on OSF — replicable by construction.

*Source: Mertens et al., "Promoting Self-Regulated Social Media Use on Smartphones With a Mobile Intervention App (Wellspent): Randomized Controlled Trial," JMIR Mhealth Uhealth 2026;14:e56824. doi:10.2196/56824.*