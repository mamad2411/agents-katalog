---
name: causal-inference
description: Estimate causal effects instead of correlations — randomised experiment and A/B test, geo holdout and geo experiment, difference-in-differences (DiD) with parallel-trends assumption, synthetic control, regression discontinuity design (RDD), instrumental variables (IV), confounding vs selection bias, pre-trend checks, placebo and null tests, counterfactual and lift measurement, why correlation-based lift claims fail.
---

# Causal Inference (experiments, DiD, synthetic control, quasi-experiments)

## The question is always about a counterfactual

Every causal claim compares the observed world to one that did not happen: what would this group's outcome
have been without the treatment? Method choice is only about how that counterfactual is built —
randomisation by design, quasi-experiments by assumption. State the assumption; show evidence for it.

```
randomised (A/B, geo holdout) → counterfactual = the control arm; assumption: valid randomisation
DiD                           → = treated group's own pre-trend continued; assumption: parallel trends
synthetic control             → = weighted mix of untreated units matching the treated pre-period
RDD                           → = units just the other side of a threshold; assumption: continuity
IV                            → = variation from an instrument; assumptions: relevance + exogeneity
```

## Randomisation first (the gold standard)

Randomise at the level the treatment is delivered: users for in-product changes, geos for media, markets
for pricing. Fix the unit, primary metric, analysis window and minimum detectable effect **before** launch,
with power computed from the metric's own variance. Geo holdouts are the marketing workhorse because ads
cannot be reliably withheld per individual: pair or stratify geos on pre-period level and trend, and hold
out enough population to be powered (a token 5% holdout rarely detects a real media effect).

## Difference-in-differences

```
effect = (Y_treated,post − Y_treated,pre) − (Y_control,post − Y_control,pre)
assumption: absent treatment, both groups' outcomes would have moved in parallel
```

DiD subtracts the control's change from the treated group's change, cancelling level differences and
shocks common to both. Parallel trends concerns an unobserved counterfactual: never provable, only
falsifiable. Check it — plot both series over many pre-periods (not two points) and run an event-study
specification with leads and lags, confirming every pre-treatment lead is ≈0. Breakages: the treated unit
was chosen *because* it was already moving (Ashenfelter's dip), a shock hit one group only, or timing is
staggered (needs a staggered-adoption estimator, not naive two-way fixed effects). Cluster errors at the
treatment unit; treating each user-day as independent shrinks the interval to fiction.

## Synthetic control, RDD, IV

- **Synthetic control**: weight untreated donors to reproduce the treated unit's pre-period path, then
  read the post-period gap. Fits one or few treated units; needs a long clean pre-period and spillover-free
  donors. Validate with placebo runs on donors — the real gap must be extreme against that distribution.
- **RDD**: exploits a hard threshold in a continuous assignment variable (score cutoff, spend tier); needs
  continuity at the cutoff and no score manipulation (check density bunching). The estimate is *local*.
- **IV**: variation from an instrument correlated with treatment but affecting the outcome only through it
  (relevance + exclusion). Weak instruments bias badly; exogeneity is arguable, never testable.

## Confounding vs selection bias

**Confounding** — a common cause moves both treatment and outcome (seasonality drives spend and sales; a
promo overlaps the test); fix by design (randomise, difference out) or by conditioning on the confounder.
**Selection bias** — who lands in each group is related to the outcome, and conditioning cannot fix
selection on unobservables. Never condition on a post-treatment variable or a collider: that manufactures
bias instead of removing it, and survivorship is selection bias with a friendly name.

## Failure modes — why correlation-based lift claims fail

- "Exposed users converted 3× more": exposure is caused by being active, targetable and high-intent, so
  the gap measures who was targeted, not what the campaign did.
- Before/after with no control, credited to the change — seasonality, launches, price moves ignored.
- "Engaged users retain better": reverse causality, since retention drives engagement too.
- Attribution-model output read as incremental lift; a credit split is not a counterfactual.
- "No effect" from an underpowered test — that shows nothing, not an absence of effect.

## Reviewer checklist

- [ ] The counterfactual and its identifying assumption are stated explicitly
- [ ] Randomisation used where feasible; unit, cells and analysis window pre-registered
- [ ] Minimum detectable effect and power computed before launch from the metric's own variance
- [ ] Pre-trend / event-study plot shown over multiple pre-periods, not two points
- [ ] Placebo or null test run (pre-treatment periods, untreated donors, alternate controls)
- [ ] Concurrent shocks, composition changes and staggered timing ruled out or modelled
- [ ] Errors clustered at the treatment unit; interval reported with the point estimate; no
      conditioning on post-treatment variables, colliders or survivors; RDD estimates kept local

## Provenance

Standard applied-econometrics and experimentation practice: DiD with parallel-trends and event-study
checks, synthetic control with placebo inference, RDD continuity and density checks, IV relevance and
exclusion conditions, randomisation as the identification benchmark. The 5% holdout figure is
**derived, unverified**; replace with the project's own measured values before treating as a target, via a
real power calculation. No statistic, effect size or vendor result is claimed here.
