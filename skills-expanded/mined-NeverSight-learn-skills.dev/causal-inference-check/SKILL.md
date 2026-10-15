---
name: causal-inference-check
description: Use when a team makes a causal claim from observational data and the AI should assess counterfactual quality, alternative explanations, and next-step rigor.
source: perlytics-skill
version: 1.0.0
---

# Causal Inference Check

## Purpose

Assess whether a causal claim is justified by the available evidence, identify what alternative explanations exist, and recommend what method or evidence is needed to support the claim rigorously.

## When to use

Use this skill when:

- a team states or implies that X caused Y based on observational data ("we added feature X and retention went up")
- a `root-cause-analysis` or `hypothesis-tree` investigation arrives at a confident-sounding conclusion that lacks experimental backing
- a decision is being justified with a correlation rather than controlled evidence
- you need to evaluate whether non-experimental evidence is strong enough to act on

## When not to use

Do not use this skill when:

- the causal claim is already supported by a well-designed randomized experiment (use `experiment-readout` instead)
- the task is descriptive - "what happened" rather than "what caused it"

## Required thinking discipline

- Correlation is evidence, not proof. A correlation between X and Y is consistent with X causing Y, but also consistent with Y causing X, a common cause driving both, or coincidence.
- Always name the alternative explanation before accepting a causal claim. The job is not to disprove the claim, but to surface what else could explain the pattern.
- The counterfactual question is: what would have happened to Y if X had not occurred? If you cannot describe the counterfactual, you cannot assess the causal claim.
- Match the method to the question rigor required. Not every question needs an RCT - but every causal claim needs a credible counterfactual.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Confounders to check by default

Before accepting any causal claim, ask whether these alternatives were ruled out:

- **Selection bias:** did the people who received X differ systematically from those who did not, in ways that also affect Y?
- **Simultaneous change:** did something else change at the same time as X that could explain the change in Y?
- **Reverse causality:** could Y be causing X rather than the other way around?
- **Survivorship bias:** is the comparison population systematically different because some entities dropped out?
- **Regression to the mean:** was X applied to a group precisely because Y was unusually bad, making a natural rebound likely regardless of X?

## Workflow

1. **State the causal claim explicitly.** Convert the implicit claim into a testable statement: "We believe [intervention X] caused [outcome Y] to change by [amount]."

2. **Identify the counterfactual.** What would Y have looked like if X had not occurred? Is there a control group, a pre-period, a comparable geography, or a synthetic control?

3. **List plausible confounders.** Name at least two alternative explanations that are consistent with the observed pattern. Use the checklist above.

4. **Assess evidence type:**
   - **Randomized experiment:** strongest evidence. If well-designed and validated (see `experiment-readout`), the causal claim is well-supported.
   - **Quasi-experiment:** moderate strength. Evidence depends on the credibility of the identification assumption (parallel trends, sharp cutoff, etc.).
   - **Observational (pre/post, correlation):** weakest evidence. Can support a hypothesis but not confirm causality without ruling out confounders.

5. **Recommend the appropriate method or next step:**

| Situation | Recommended method |
|---|---|
| Observational correlation only | State as association, not cause. Run confound checks. |
| Pre/post with no control group | Consider difference-in-differences if a valid control group exists. Otherwise, treat as descriptive. |
| Geographic or cohort rollout | Synthetic control or matched comparison group. |
| Known eligibility cutoff (e.g., score threshold) | Regression discontinuity. |
| Randomized assignment | Standard experiment readout. |
| No clean identification possible | State explicitly what evidence would be needed and at what cost. |

6. **State the conclusion with honest confidence.** Use "associated with," "consistent with," or "suggests" rather than "caused" unless the evidence warrants it.

## Output format

- Causal claim (explicitly stated)
- Counterfactual identified (or noted as missing)
- Evidence type (RCT / quasi-experiment / observational)
- Confounder list (named, not just acknowledged)
- Causal claim confidence (supported / partially supported / unsupported)
- Recommended method or next step
- Language recommendation (how to state the claim honestly)

## Good example

Claim: "Email re-engagement caused a 12% lift in 30-day retention among lapsed users."

> Counterfactual: users who did not receive the email. However, email was sent only to users who had opened a prior email in the last 90 days - these users likely have higher baseline re-engagement intent.
> Evidence type: observational comparison. No randomization.
> Confounders: selection bias (email recipients are self-selected active users), simultaneous product change (a mobile notification was also added during this period).
> Assessment: the 12% difference is consistent with email having an effect, but cannot be separated from selection bias and the concurrent notification change.
> Confidence: unsupported as a causal claim.
> Recommended method: run an A/B test with random assignment among eligible lapsed users to isolate the email effect.
> Language recommendation: "Users who received re-engagement email showed 12% higher 30-day retention - this is consistent with an email effect but has not been causally validated."

## Bad example

> We sent the email and retention went up, so the email worked.

Why this is bad:

- no counterfactual - would retention have gone up anyway?
- no confounder check - who was selected to receive the email?
- no evidence type assessment - this is observational, not experimental
- treating post-hoc correlation as confirmed causality will lead to scaling an intervention that may not have worked

## Practical notes

- The most common causal claim error in business analytics is treating pre/post comparison as evidence of causality. Before-and-after comparisons have no control and cannot separate the intervention effect from concurrent changes or natural trends.
- "Regression to the mean" is underappreciated: if a team intervenes on the worst-performing users or markets, performance will likely improve somewhat on its own - this is not evidence the intervention worked.
- It is valid and useful to act on an association before causality is proven, as long as the uncertainty is stated explicitly and the decision is sized appropriately.

## Optional variants

- **Marketing attribution:** distinguish last-touch, multi-touch, and incremental lift - only incremental lift with a holdout group supports a causal claim about campaign effectiveness.
- **Product feature launch:** when a feature is launched to all users simultaneously, there is no control group - synthetic control or pre-period regression are the best available quasi-experimental approaches.
- **Operations intervention:** when applying a process change to a specific team or location, the comparison should be a matched comparable unit rather than company-wide average, which is affected by the intervention.
