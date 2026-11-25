---
name: bio-experiment-design
version: 1.0.0
description: Design a rigorous preclinical experiment with a falsifiable hypothesis, controls, power analysis, and a pre-registered analysis plan.
author: matrixx0070
tags: [experiment-design, preclinical, statistics, power, controls, pre-registration]
capabilities: []
---

## When to use

Use this when the user is planning a wet-lab or in vivo study and needs a statistically sound, reproducible design before spending reagents or animals. It exists to prevent underpowered, confounded, or unblinded experiments.

**Not for:** analyzing data you already collected, choosing which target to test (use bio-target-prioritization), or running a computational pipeline (use bio-pipeline-runner).

## Method

1. State one falsifiable hypothesis and the primary readout that confirms or refutes it. Separate primary from exploratory endpoints — you power on the primary only.
2. Define the system: model, genotype/strain, passage, age/sex, and the perturbation with dose and timing.
3. Specify controls: negative (vehicle/scramble), positive (known effector), technical (batch, isotype). Address every plausible confounder.
4. Power the study: state expected effect size and variance from pilot or literature, choose alpha and power (typically 0.05 / 0.80), compute n per group, and name the test. **Decision:** if no pilot effect size exists, run a small pilot or state the minimum detectable effect at feasible n — do not invent a number.
5. Build in rigor: randomization scheme, blinding of treatment and analysis, pre-specified inclusion/exclusion.
6. **Decision:** pre-register the analysis before collecting data — the test, multiple-comparison correction, and outlier rule. If you change it later, that becomes exploratory, not confirmatory.

## Example

Hypothesis: "Compound X reduces tumor volume vs vehicle at day 21." Pilot gives effect size d≈0.9, SD known. Power at 0.05/0.80 → n=11 per group; round to 12 for attrition. Groups: vehicle (negative), X, and paclitaxel (positive control). Mice randomized by cage, tumor measurement blinded to arm, animals below engraftment threshold excluded pre-treatment. Primary test: Mann–Whitney on day-21 volume; exploratory time-course reported without inference.

## Pitfalls

- Powering on a wished-for effect size instead of a measured one — the commonest source of underpowered studies.
- Omitting a positive control, so a null result can't distinguish "no effect" from "assay didn't work."
- Deciding the statistical test after seeing the data (HARKing / p-hacking).
- Confusing technical replicates with biological replicates when counting n.

## Output format

```
# Experiment Design — <title>
Hypothesis: <one sentence, falsifiable>
Primary readout: <one sentence>

## Design table
| Group | Perturbation | n | Control role |

## Power analysis
effect size=_, alpha=_, power=_, test=_, n/group=_, assumptions=_

## Rigor checklist
randomization / blinding / bio vs tech replicates / stopping rules

## Pre-registered analysis plan
test, correction, outlier handling, limitations
```
If effect size is a guess, label it UNVERIFIED.

## Reference

### Power & sample-size quick reference (α=0.05, power=0.80, two-sided)

For a two-group comparison of means, per-group n scales as n ≈ 2(z_α/2 + z_β)² / d², where d = Cohen's effect size (mean difference / pooled SD). With α=0.05 (z=1.96) and power 0.80 (z=0.84), the constant 2(1.96+0.84)² ≈ 15.7:

| Cohen's d | Interpretation | ~n per group (t-test) |
|:-:|-----------|:-:|
| 0.2 | small | ~394 |
| 0.5 | medium | ~64 |
| 0.8 | large | ~26 |
| 1.0 | very large | ~17 |
| 1.5 | huge (typical strong preclinical) | ~8 |

Raising power to 0.90 multiplies n by ~1.34; a one-sided test lowers it modestly. For proportions use n per group ≈ (z_α/2+z_β)²·[p₁(1−p₁)+p₂(1−p₂)]/(p₁−p₂)². For survival/tumor-growth, power on the number of *events* (log-rank) not animals. Non-parametric tests (Mann–Whitney) need roughly the t-test n / 0.955 (≈ +5%). Always add attrition: round up and pad (e.g. +10–20% for in-vivo dropout/engraftment failure). Tools: G*Power, R `pwr` package, `stats::power.t.test`, `survival`/`powerSurvEpi`.

**Cardinal rule:** power on a *measured or literature* effect size, never a hoped-for one. If none exists, run a pilot to estimate variance, or report the minimum detectable effect (MDE) at the feasible n instead of inventing d.

### Control types

| Control | Purpose | Example |
|---------|---------|---------|
| Negative / vehicle | Baseline, rules out solvent/handling effect | DMSO, PBS, scrambled siRNA, non-targeting sgRNA |
| Positive | Confirms assay can detect a true effect | Known effector drug, staurosporine (apoptosis) |
| Isotype / technical | Controls antibody/reagent nonspecificity | Isotype-matched IgG, no-RT, no-template |
| Sham / procedural | Controls surgery/injection stress | Sham operation, needle-only |
| Batch / plate | Controls run-to-run drift | Reference sample on every plate; balanced layout |
| Genetic rescue | Confirms on-target (KO + re-expression) | Add-back of cDNA to knockout |

A missing positive control is the reason a null result cannot distinguish "no biology" from "assay failed."

### Randomization, blinding & rigor checklist (ARRIVE 2.0-aligned)

- [ ] **Randomize** allocation to groups (block/stratified by cage, litter, weight, sex, plate position); state the method (RNG, not alternation).
- [ ] **Blind** at two points: who administers treatment, and who measures/scores the outcome. Code samples; unblind only after data lock.
- [ ] **Biological vs technical replicates** counted correctly — n = independent biological units (animals, donors, passages), not repeat measurements of one unit. Technical replicates reduce measurement noise, they do not increase n.
- [ ] **Inclusion/exclusion criteria** pre-specified (e.g. engraftment threshold, viability minimum); log every excluded unit with reason.
- [ ] **Balance** sex, age, cage, and processing order across arms; report both sexes unless justified.
- [ ] **Pre-register** the primary endpoint, statistical test, multiple-comparison correction, and outlier rule *before* data collection. Anything decided after seeing data is exploratory (guards against HARKing/p-hacking).
- [ ] Define **stopping rules** and any interim analyses (with alpha spending) up front.

### Common corrections & tests

Two groups, continuous → t-test (normal) or Mann–Whitney (not). >2 groups → ANOVA + Tukey/Dunnett (vs single control), or Kruskal–Wallis + Dunn. Paired/repeated → paired t / Wilcoxon / mixed-effects. Multiple endpoints/genes → Bonferroni (strict FWER) or Benjamini–Hochberg FDR (genomics). Report effect sizes with 95% CIs, not p-values alone.
