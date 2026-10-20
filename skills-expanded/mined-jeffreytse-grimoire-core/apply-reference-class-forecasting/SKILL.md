---
name: apply-reference-class-forecasting
description: Use when estimating the cost, duration, or probability of success of a project, initiative, or decision you are personally involved in — replace or check your case-specific intuitive estimate against the actual outcome distribution of a class of comparable past cases, because direct involvement systematically biases estimation toward optimism in a way outside data does not.
source: '新唐书·元行冲传 (New Book of Tang, Biography of Yuan Xingchong, compiled by Ouyang Xiu & Song Qi, 1060 AD) — 當局者迷，旁觀者清 (the one in the game is confused; the onlooker sees clearly); Kahneman & Tversky, "Intuitive Prediction: Biases and Corrective Procedures", TIMS Studies in Management Science (1979) — inside view/outside view distinction, planning fallacy; Flyvbjerg, Skamris Holm & Buhl, "Underestimating Costs in Public Works Projects", Journal of the American Planning Association (2002); HM Treasury, "The Green Book: Supplementary Guidance on Optimism Bias" (2003, updated)'
tags: [decision-making, estimation, planning-fallacy, forecasting, project-management, cognitive-bias]
related: [apply-monte-carlo-risk-simulation, apply-premortem, apply-devils-advocate-technique, apply-anchoring-defense, apply-halo-effect-mitigation, apply-availability-heuristic-correction, apply-statistical-prediction-preference, apply-small-sample-skepticism, apply-hindsight-bias-correction]
---

# Apply Reference Class Forecasting

Estimate a project's cost, duration, or odds of success from the actual outcome distribution of comparable past cases, not from the case-specific intuitive reasoning of whoever is directly involved — because involvement systematically biases the estimate toward optimism in a way that outside data corrects.

## Why This Is Best Practice

新唐书·元行冲传 (New Book of Tang, 1060 AD, attributed to Yuan Xingchong, Tang dynasty official, ~8th century AD):

> 當局者迷，旁觀者清。

"The one positioned within the game is confused; the one watching from outside sees clearly." The idiom names a specific, checkable asymmetry: the person with a stake in a specific case reasons from that case's unique-seeming plan, momentum, and hoped-for outcome (the "inside view"); a person with no stake reasons from what has actually happened in similar cases before (the "outside view") — and the outside view is the one that is empirically better calibrated.

**Why best:** Kahneman & Tversky's original finding is that inside-view estimation is not just occasionally wrong but systematically and predictably optimistic — every planner reasons from their own case's specific, distinguishing details, which crowds out the base-rate information that similar past cases usually run over budget and over schedule. The outside view — built from a reference class of genuinely comparable past cases — is not a different opinion to weigh against the inside view; it is a bias-correction with a demonstrated, checkable track record. This is a distinct, falsifiable claim (Flyvbjerg's decades-spanning project database shows the actual overrun distribution), not a generic warning to "be less optimistic."

**Kahneman & Tversky (1979):** Identified the "planning fallacy" — when people estimate a future task, they focus on the specific plan for that case (the inside view) rather than the outcome statistics of similar cases (the outside view), producing predictable, direction-consistent optimism regardless of the planner's expertise or good faith. Foundational to behavioral economics; Kahneman was awarded the 2002 Nobel Memorial Prize in Economic Sciences substantially for this and related work.

**Flyvbjerg, Skamris Holm & Buhl (2002):** Analyzed 258 transportation infrastructure projects (rail, bridges, tunnels, roads) across 20 countries over 70 years — actual costs exceeded estimated costs in 90% of projects, with rail projects overrunning by an average of 44.7% and averaging cost escalation had not improved over the 70-year study period despite improving forecasting technology, evidence that the error is systemic (motivational/cognitive) rather than technical. This database is the empirical foundation of reference class forecasting as a corrective method.

**HM Treasury Green Book, "Supplementary Guidance on Optimism Bias" (2003, updated):** The UK government mandated reference-class-based optimism-bias uplift percentages for all public-sector project appraisals, derived directly from Flyvbjerg's empirical distributions by project type (e.g., specific uplift ranges for standard buildings, non-standard buildings, and infrastructure projects) — a recognized standards-body codification of this exact practice, in mandatory use across UK government project appraisal since 2003.

**Adopted by:** UK HM Treasury (mandatory optimism-bias uplift on all public project business cases since 2003); Danish Ministry of Transport (adopted reference class forecasting for infrastructure appraisal following Flyvbjerg's recommendations); Flyvbjerg's methodology is used by the World Bank and in infrastructure planning practice internationally.
**Impact:** Flyvbjerg's 258-project database found actual-to-estimated cost ratios averaging 1.45 for rail and 1.20 for roads, with the degree of underestimation showing no improvement over 70 years of inside-view forecasting — establishing that outside-view correction, not better inside-view technique, is what closes the gap; UK Treasury's mandated optimism-bias uplifts are calibrated directly to this distributional evidence rather than to expert judgment.

## Steps

1. **Recognize the inside-view symptom.** If your estimate for cost, duration, or success probability is built from this specific project's plan, team, and current momentum — "we're different because X, Y, Z" — that is the inside view Kahneman and Tversky identified as the systematically optimistic default. This is the trigger to apply the outside view as a check, not a replacement made only when convenient.

2. **Define the reference class.** Identify a set of past projects genuinely comparable in type, scale, and sector — narrow enough to be truly comparable, wide enough to have enough cases for a distribution (Flyvbjerg's own work typically uses 20+ comparable cases). A reference class of one or two cherry-picked "similar" projects is not sufficient.

3. **Gather actual outcomes, not original estimates, for the reference class.** Collect what those past projects actually cost, actually took, or actually achieved — not what they were originally projected to cost or take. The gap between the reference class's own original estimates and its actual outcomes is itself the calibration data.

4. **Anchor the estimate to the reference class distribution.** Start from the reference class's actual-outcome distribution (median and spread), not from zero or from the inside-view number. Adjust from that anchor only for specific, verifiable differences between the current case and the reference class — not for generic optimism ("we've learned from others' mistakes," "our team is stronger").

5. **Compare the adjusted outside-view number against the inside-view number.** A large gap between the two is itself a warning signal, not a tie-breaker to average away — investigate what the inside-view estimate is failing to account for before finalizing.

6. **Where feasible, have someone with no stake in the project perform the outside-view estimate independently.** A truly disinterested estimator, working only from the reference class data, structurally cannot fall into the inside view's optimism — this is the direct, literal application of "the onlooker sees clearly."

## Rules

- Never rely on the inside view alone for a consequential estimate — pair it with a reference-class-based outside-view check as a matter of process, not only when the inside-view number already looks doubtful.
- A reference class must be genuinely comparable in type, scale, and sector — a mismatched reference class (wrong project type, wrong order of magnitude) produces a misleading anchor that is worse than no outside view at all.
- Use actual outcomes of the reference class, never its original estimates — using other projects' original (also-optimistic) estimates reintroduces the same bias this method exists to correct.
- Blend by adjusting for verified case-specific differences, not by simple averaging of the inside and outside numbers — averaging a biased and unbiased estimate still leaves a biased result.

## Examples

**Infrastructure:** A transit agency's internal team estimates a new rail line at $2B based on the specific engineering plan. Applying reference class forecasting: 30 comparable rail projects worldwide averaged a 44.7% cost overrun against original estimate. Outside-view-adjusted estimate: ~$2.9B. The agency budgets and seeks approval for the higher figure; the project comes in at $2.85B — within the outside-view range, well outside the inside-view number.

**Software:** An engineering team estimates a migration project at 6 weeks based on the specific technical plan. Reference class: the last 12 migrations of similar scope at the company averaged 11 weeks, with none finishing under 8. Outside-view estimate: 10–12 weeks. Leadership plans around 11 weeks; the inside-view 6-week estimate is flagged as a planning-fallacy signal and investigated for missing scope rather than accepted at face value.

**Startup fundraising timeline:** A founder estimates closing a seed round in 6 weeks based on current investor conversations. Reference class: the accelerator's outcome data on 40 prior portfolio companies' seed rounds averages 4.5 months from first pitch to close. Founder revises runway planning around the reference-class estimate rather than the inside-view number, avoiding a cash crunch.

## Common Mistakes

- **Cherry-picking a favorable reference class.** Selecting past cases that happen to support the desired inside-view number defeats the method — the reference class must be selected by objective type/scale/sector criteria before outcomes are examined, not after.
- **Using the reference class's original estimates instead of actual outcomes.** This silently reintroduces the same optimism bias the outside view is meant to correct.
- **Treating the outside view as infallible and ignoring genuine, verifiable case-specific differences.** The method is anchor-then-adjust, not blind base-rate substitution — real, evidenced differences from the reference class should still shift the estimate.
- **Applying this only after the inside-view estimate has already been committed to stakeholders.** The correction has to happen at initial appraisal, before public or internal commitment, to actually change the decision rather than just explain the overrun after the fact.

## When NOT to Use

- When no genuinely comparable reference class exists (a truly novel undertaking with no analogous past cases) — the outside view degrades into a poorly-matched, misleading anchor; use structured elicitation instead (`apply-premortem`, `apply-devils-advocate-technique`).
- For low-stakes estimates where the cost of a planning-fallacy-driven overrun is trivial — the overhead of building a reference class isn't justified.
- As a substitute for probabilistic modeling of a single project's internal risk factors — see `apply-monte-carlo-risk-simulation` for that distinct, complementary technique.
