---
name: behavioral-intervention-choice-tailoring
description: Applies Lipman, Alvarez Colic, Sukurica, Tholen (RIVM/Leiden/Erasmus, Behavioural Public Policy, Mar 27 2026; doubly randomized field trial, N=839 university students) — letting people CHOOSE their behavior-change intervention (financial incentive vs calorie labelling vs social-norm nudge) produced (marginally) significant increases in healthy snack choice vs no intervention, while randomly assigned versions of the same interventions did not; control-regressions suggest the benefit is driven by choice of calorie labelling and social norms, not by the act of choosing itself. Use when [designing user-selected intervention or preference layers in behavior-change products, choosing between assigned vs chosen personalization in nudging, evaluating self-selection effects in experiments, or designing onboarding that lets users pick their own intervention style]. NOT for [individual choice-architecture mechanics — use nudge-theory-choice-architecture — or belief-targeting via prediction — use belief-profile-targeting-rct].
---

# Tailoring Through Choice: Self-Selected Interventions Work; Assigned Ones Don't

## The experiment

One-size-fits-all interventions don't exist — effects vary across individuals. The standard fix is tailoring via measurement or machine learning, which carries practical (measurement error) and ethical (who decides what's best for whom) problems. A more feasible alternative: **let individuals choose their own intervention** ("tailoring through choice").

Lipman et al. ran a doubly randomized control trial: 839 Dutch university students choosing between a healthier and less healthy snack under three interventions — (i) small financial incentive (€0.10 attached to the healthy option), (ii) calorie information, (iii) social-norm nudge ("in a similar experiment, 60% chose healthily"). Half the respondents were **randomly assigned** an intervention (or a no-intervention control); the rest **selected** their own from the same menu.

## The four findings

1. **Choice works; assignment doesn't.** Self-selected interventions (marginally) significantly increased healthy snack choice compared to no-intervention control; randomly assigned interventions did not significantly affect choice (individual point estimates positive: +11pp incentives, +7pp labelling, +4pp norms — none individually significant).
2. **The menu itself reveals preferences.** Among those given a choice: 51% chose financial incentives, 41% calorie labelling, 8% social norms — most respondents picked the *most intrusive* option when it was their decision.
3. **The mechanism is conditional selection, not the act of choosing.** After controlling for demographics and selection-predicting characteristics, chosen **calorie labelling** and **social-norm** interventions significantly increased healthy choice; chosen financial incentives did not. When compared head-to-head, chosen vs assigned interventions showed no significant effectiveness difference (the ~3% edge was underpowered).
4. **Self-selection has a signature.** Respondents selecting incentives had lower BMI; those selecting calorie labelling had higher BMI and higher self-rated label susceptibility; the small social-norm group had lower diet quality, lowest demand for commitment, and lowest need for autonomy. Selection characteristics did *not* fully explain the effectiveness edge.

## The design rules

1. **Offer the menu before assuming the assignment.** Wherever heterogeneous interventions exist, a choice layer is the cheap first personalization — no measurement infrastructure required.
2. **Expect preference to diverge from effectiveness.** The most popular option (incentives, 51%) showed no significant effect when chosen; less popular options (labelling, norms) carried the effect. Don't infer effectiveness from popularity.
3. **Control for the selection signature when evaluating choice-based designs** — otherwise you can't tell autonomy effects from self-selection.
4. **One-shot choice is the lower bound.** Real deployments allow repeated choice, bundles, and experimentation before settling; a single-snack field experiment understates long-tail benefits of choice.
5. **Watch attrition symmetry.** This study found *more* dropout in the choice condition — the general finding that choice reduces dropout doesn't automatically transfer to short-horizon, low-stakes decisions.

## Applications

- **Behavior-change products:** onboarding flows should offer intervention-style menus (e.g., reminders vs streaks vs social feeds vs information) rather than assigning a design philosophy.
- **AI assistants:** a user-chosen intervention register ("how would you like to be nudged?") both improves effectiveness and answers the autonomy critique the disclosure literature documents — a choice is an autonomy-preserving design element that disclosure labels are not.
- **Workplace/public programs:** letting participants pick incentive type (cash vs competition vs social) is cheaper and possibly more effective than algorithmic assignment — and more defensible ethically.
- **Experiment design:** if you run choice-based personalization, pre-register whether you're estimating the *act of choosing* or the *conditional assignment*; they are different estimands.

## Honest caveats

- Convenience sample (university students, ~58% female, mean age ~22) limits external validity; students' social-norm susceptibility differs from older adults.
- Underpowered for small effects (minimum detectable effect sizes in appendix; the ~3% choice-vs-random edge was below power).
- One-shot, single-domain (snack choice); €0.10 incentives are small in absolute terms.
- Possible order effects (intervention menu order not randomized), though the modal choice differed between pilot and main experiment.
- Mechanism exploration is exploratory; alignment-with-prediction analysis suggests the act of choosing is *not* the whole driver.

## Pairs with

`belief-profile-targeting-rct` (algorithmic tailoring — the measurement-based complement to choice-based tailoring; both move past one-size-fits-all), `nudge-disclosure-autonomy-decoupling` (disclosure doesn't restore autonomy; choice plausibly does), `co-designed-digital-nudging` (the co-design lineage), `nudge-effectiveness-reality-check` (heterogeneity is a central explanation for modest average effects), `llm-iterative-nudge-personalization` (LLM-personalized assignment vs user-chosen assignment — an open design question).

## A-Tech alignment

- **Open source:** the doubly-randomized design and three-intervention menu are replicable patterns for open behavior-change tooling; no proprietary instruments required.
- **Privacy:** choice-based tailoring needs no profiling data — the privacy-preserving personalization option; contrast with belief/inference-based targeting which requires data collection.
- **Financial freedom:** for product builders, a preference menu is a zero-infrastructure personalization layer that measurably moves behavior — a free edge over assigned-design competitors.
- **Practical:** one design rule ("offer the menu"), one evaluation rule ("pre-register which estimand"), one caution ("popularity ≠ effectiveness") — directly usable in product reviews.