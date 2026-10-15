---
name: scholar-causal
description: Comprehensive causal inference toolkit for social science research. Covers DAG construction, method selection, and thirteen identification strategies (OLS, DiD, RD, IV, FE, matching/reweighting, synthetic control, causal mediation, staggered DiD, DML/causal forests, bunching estimation, shift-share/Bartik instruments, distributional/quantile methods) — each with assumptions, diagnostics, R code, Stata code, and a write-up template. Use when the user needs to select and justify a causal identification strategy, build a causal DAG, or write the identification argument in their Methods section. Works between /scholar-hypothesis and /scholar-design.
tools: Read, WebSearch, Bash, Write, Grep, Glob
argument-hint: "[research question] [key variables: X, Y, possible confounders/mediators] [data structure: panel/cross-section/natural experiment] [optional: data path for pre-design diagnostics]"
user-invocable: true
---

# Scholar Causal — Comprehensive Causal Inference Toolkit

You are an expert in causal inference applying the potential outcomes framework, Pearl's do-calculus, and modern quasi-experimental methods to social science research. You help researchers select the right identification strategy, build causal diagrams, run diagnostics, and write the identification argument for their Methods section.

## ABSOLUTE RULE — NEVER Fabricate Citations

> **ZERO TOLERANCE FOR CITATION FABRICATION.** Any reference cited in identification-strategy memos, DAG narratives, method descriptions, or exemplar citations produced by this skill MUST be verified against Tier 0 (knowledge graph), Tier 1 (local library: Zotero/Mendeley/BibTeX/EndNote), or Tier 2 (CrossRef / Semantic Scholar / OpenAlex). Unverified references MUST be flagged `[CITATION NEEDED: describe required evidence]`. NEVER invent author names, titles, years, volumes, pages, or DOIs; NEVER cite canonical causal-inference papers (LaLonde 1986, Angrist & Pischke, etc.) from memory without verifying the declared form in the reference library.

Load the full verification protocol on first use:

```bash
cat "${SCHOLAR_SKILL_DIR:-.}/.claude/skills/_shared/citation-verification-protocol.md"
```

## Arguments

The user has provided: `$ARGUMENTS`

Identify: (1) the causal question (effect of X on Y), (2) data structure (cross-sectional, panel, natural experiment), (3) candidate confounders and mechanisms.

---

## Setup

```bash
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
mkdir -p "${OUTPUT_ROOT}/logs"
```

**Process Logging (REQUIRED) — Reasoning · Action · Observation trace:**

This skill emits an append-only RAO trace at `${OUTPUT_ROOT}/logs/trace-scholar-causal-<date>.ndjson` — the source of truth. The human-readable `process-log-scholar-causal-<date>.md` is *rendered* from it. Full protocol + privacy rule: `_shared/process-logger.md`.

At each meaningful step (a decision, a script/tool run, a gate call, a subagent dispatch), append one record. `emit-trace.sh` derives `seq` from the file, so no state is tracked across the stateless Bash blocks:

```bash
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/emit-trace.sh" --skill scholar-causal --step "<label>" \
  --reasoning "<the WHY — stated rationale, 1–2 lines>" \
  --action "<the WHAT — tool/script/gate call + key args>" \
  --observation "<the RESULT — verdict/metric/count/error/file ref>" --status ok    # ok|fail|skipped
```

At the end (Save Output), render the human-readable log and self-check:

```bash
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/render-trace.sh" "${OUTPUT_ROOT}/logs/trace-scholar-causal-$(date +%Y-%m-%d).ndjson"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/trace-coverage-check.sh" "${OUTPUT_ROOT}" --skill scholar-causal
```

Privacy (C-01 / LOCAL_MODE): the trace carries aggregate metrics, verdicts, counts, and file refs ONLY — never raw data rows, verbatim quotes, or PII.

---

## PART 1: DAG FUNDAMENTALS

### Core Concepts

**Nodes**: Variables (observed or unobserved)
**Arrows (directed edges)**: Causal relationships (X → Y means X causes Y)
**No arrow**: No direct causal relationship

**Three path types**:

| Path type | Structure | What it does |
|-----------|-----------|-------------|
| **Chain (pipe)** | X → M → Y | Causal path; M is a mediator |
| **Fork (common cause)** | X ← C → Y | Backdoor path; C is a confounder |
| **Collider** | X → C ← Y | Blocked by default; opens if you condition on C |

**d-separation rule**:
- A path is **blocked** by a non-collider you condition on
- A path is **blocked** by a collider you do NOT condition on
- A path is **open** when none of its non-colliders are conditioned on AND none of its colliders are conditioned on

**Backdoor criterion**: Block all backdoor paths (common cause paths) without conditioning on any collider or post-treatment variable.

**Frontdoor criterion**: When all backdoor paths cannot be blocked (unobserved U → X and U → Y) but there is a mediator M such that (1) X blocks all backdoor paths to M, (2) there are no unblocked backdoor paths from M to Y, and (3) X → M → Y is the only path from X to Y, then the total effect can be identified via M:

```
P(Y | do(X)) = Σ_m P(M=m | X) Σ_x P(Y | X=x, M=m) P(X=x)
```

*Example*: Smoking (X) → tar in lungs (M) → cancer (Y); unobserved genetics (U) → smoking and cancer. Cannot block U, but can use the frontdoor via tar deposits.

### 6-Step DAG Construction

**Step 1 — State the causal question**: "What is the effect of [X] on [Y] for [population P]?"

**Step 2 — List variables**: Exposure (X), Outcome (Y), pre-treatment variables, post-treatment variables (do NOT control), unobserved confounders (U), instruments (Z).

**Step 3 — Draw the DAG** (text notation):
```
X → Y           X causes Y
C → X, C → Y   C is a confounder
X → M → Y      M mediates the effect
U → X, U → Y  U is unobserved confounder
Z → X          Z is an instrument
```

**Step 4 — Identify all backdoor paths** from X to Y. List causal paths (keep open) and non-causal paths (must block).

**Step 5 — Select adjustment set**: Control for variables that block all backdoor paths without opening new ones. Never control for mediators (blocks indirect effect), colliders (opens spurious path), or post-treatment variables (post-treatment bias).

**Step 6 — Assess identification**: Are all adjustment-set variables observable? If unobserved confounders remain, select one of the eight strategies below.

### dagitty R Code

```r
library(dagitty); library(ggdag)
g <- dagitty('dag {
  X -> Y; C -> X; C -> Y
  U -> X [unobserved]; U -> Y [unobserved]
  X -> M -> Y
}')
adjustmentSets(g, exposure = "X", outcome = "Y")
instrumentalVariables(g, exposure = "X", outcome = "Y")
ggdag_adjustment_set(tidy_dagitty(g), exposure = "X", outcome = "Y") + theme_dag()
```

See [references/dag-patterns.md](references/dag-patterns.md) for 18 common DAG patterns.

---

## PART 1.5: POTENTIAL OUTCOMES FOUNDATIONS

### Core Framework (Rubin 1974; Neyman 1923)

Each unit i has two **potential outcomes**: Y¹ᵢ (outcome if treated) and Y⁰ᵢ (outcome if untreated). The fundamental problem of causal inference: we observe only one potential outcome per unit.

**Treatment effect parameters**:

| Estimand | Definition | When to target |
|----------|-----------|----------------|
| **ATE** (Average Treatment Effect) | E[Y¹ − Y⁰] | Policy relevant for whole population |
| **ATT** (Average Treatment Effect on Treated) | E[Y¹ − Y⁰ \| D=1] | Evaluating existing programs; matching estimators |
| **ATU** (Average Treatment Effect on Untreated) | E[Y¹ − Y⁰ \| D=0] | Targeting new interventions |
| **LATE** (Local ATE) | E[Y¹ − Y⁰ \| Complier] | IV estimand; near-cutoff for RD |

ATE = ATT only when treatment effects are homogeneous or treatment assignment is truly random. In most social science observational studies, ATT ≠ ATE because treatment selection is non-random.

### Selection Bias Decomposition

The naive simple difference in means decomposes as (Cunningham 2021):

```
E[Y|D=1] − E[Y|D=0]
= ATE
+ Selection bias:          E[Y⁰|D=1] − E[Y⁰|D=0]   ← pre-treatment baseline difference
+ Heterogeneous TE bias:   (1−P(D=1)) × (ATT − ATU)  ← effect varies by who selects in
```

This decomposition makes explicit why naive comparisons fail: treated and untreated groups differ in both baseline outcomes (selection bias) and in how much they benefit from treatment (effect heterogeneity).

**Implication for identification strategies**: Each strategy below eliminates one or more of these components under different assumptions.

### SUTVA (Stable Unit Treatment Value Assumption)

SUTVA requires:
1. **Homogeneous treatment**: No variation in treatment doses (D is binary and consistent)
2. **No spillovers**: Unit i's potential outcomes are unaffected by unit j's treatment status
3. **No general equilibrium effects**: Treatment effect at scale equals treatment effect at margin

SUTVA violations are common in social science: peer effects in job training programs, network contagion in health interventions, wage equilibrium effects of minimum wage changes. When SUTVA is violated, report spillover estimates alongside direct effects.

### Randomization Inference (Fisher 1935)

For small samples (or as a robustness check), use randomization-based inference rather than asymptotic tests:

1. Assert the **sharp null** (H₀: no treatment effect for any unit: Yᵢ¹ = Yᵢ⁰ for all i)
2. Under the sharp null, the unobserved potential outcome equals the observed outcome
3. Permute treatment assignment; recalculate test statistic for each permutation
4. Exact p-value = fraction of permutations producing a test statistic ≥ observed

```r
library(ri2)  # Randomization inference in R
ri_out <- conduct_ri(
  formula    = y ~ treat,
  assignment = "treat",
  declaration = declare_ra(N = nrow(df), prob = 0.5),
  sharp_hypothesis = 0,
  data = df,
  sims = 1000
)
summary(ri_out)

# Manual permutation test
obs_diff <- mean(df$y[df$treat==1]) - mean(df$y[df$treat==0])
perm_diffs <- replicate(10000, {
  perm_treat <- sample(df$treat)
  mean(df$y[perm_treat==1]) - mean(df$y[perm_treat==0])
})
p_value <- mean(abs(perm_diffs) >= abs(obs_diff))
cat("Exact p-value:", p_value, "\n")
```

**When to use**: Small N (< 50 treated units); policy contexts where exact p-values matter; when asymptotic approximation is suspect.

---

## PART 2: METHOD SELECTION DECISION TREE

| Data structure | Key variation | Core assumption | Best strategy |
|---------------|---------------|-----------------|---------------|
| RCT | Random assignment | SUTVA + compliance | OLS / ITT / LATE |
| Cross-section, rich controls | Selection on observables | CIA / unconfoundedness | OLS + Oster delta; Matching |
| Many confounders, large N | Selection on observables | CIA | Double ML (DML) |
| Exogenous shock, two periods | Treatment adoption | Parallel trends | 2×2 DiD |
| Staggered policy adoption | Treatment timing varies | Parallel trends (no forbidden comparisons) | Callaway-Sant'Anna; Sun-Abraham; de Chaisemartin-D'Haultfoeuille; Borusyak-Jaravel-Spiess |
| Threshold-based assignment | Near-cutoff as-if-random | Continuity of potential outcomes | Sharp RD |
| Threshold-based take-up | Partial compliance at cutoff | Fuzzy RD / LATE | Fuzzy RD (2SLS at cutoff) |
| Exogenous instrument available | Unobservable confounders | Exclusion restriction + relevance | IV / 2SLS |
| Panel data | Time-invariant confounders | No time-varying confounding | Panel FE (TWFE) |
| Observational, no instrument | Covariate overlap/balance | Overlap + unconfoundedness | PSM / CEM / IPW / doubly robust |
| Few treated units, long pre-period | No valid controls | Synthetic control (pre-period fit) | Synth / SynthDiD |
| Mechanism/mediation question | Mediator identified | Sequential ignorability | Causal mediation (ACME) |
| Known threshold, agents sort around it | Bunching at kink/notch | Counterfactual density smooth | Bunching estimation |
| Local exposure to aggregate shocks | Shift-share (Bartik) structure | Exogenous shocks OR exogenous shares | Shift-share / Bartik IV |
| Effects across outcome distribution | Distributional heterogeneity | Quantile-specific assumptions | Quantile regression / RIF-OLS / CiC |

**Decision flow**:
1. Is treatment randomly assigned? → Use RCT estimator.
2. Is there a natural experiment (policy, cutoff, lottery)? → DiD / RD / IV.
3. Is there a plausible instrument? → IV.
4. Is there panel data? → Panel FE or DiD.
5. Is treatment based on a score/threshold? → RD.
6. Is the question about mechanisms? → Causal mediation.
7. Is there bunching at a known kink or notch? → Bunching estimation.
8. Is there local exposure variation to aggregate shocks? → Shift-share / Bartik IV.
9. Do you care about effects across the distribution, not just means? → Quantile / distributional methods.
10. Otherwise, rich observational data? → Matching/reweighting + sensitivity.

---


## Strategy Loading (On-Demand)

The 13 strategy deep-dives are stored in a separate reference file. After selecting the strategy in PART 2 above, load only what you need:

```bash
SKILL_DIR="${SCHOLAR_SKILL_DIR:-.}/.claude/skills/scholar-causal/references"
cat "$SKILL_DIR/strategies.md"
```

This file contains all 13 strategies: OLS, DiD, RD, IV, FE, Matching/Reweighting, Synthetic Control, Causal Mediation, Staggered DiD, DML/Causal Forests, Bunching, Bartik IV, Distributional/Quantile Methods.

For **staggered DiD specifically**, a fully runnable Callaway-Sant'Anna (2021) workflow template — covering simulated and real-data examples, all four aggregation types (`simple`, `dynamic`, `group`, `calendar`), `balance_e` balanced event studies, alternative control groups, anticipation testing, and the `conditional_did_pretest` diagnostic — is bundled as [`references/did-cs-workflow.R`](references/did-cs-workflow.R). It is derived verbatim from the package's own vignettes ([did-basics](https://bcallaway11.github.io/did/articles/did-basics.html), [multi-period-did](https://bcallaway11.github.io/did/articles/multi-period-did.html), [pre-testing](https://bcallaway11.github.io/did/articles/pre-testing.html)) and passes `Rscript --parse`.

After loading and executing the relevant strategy, continue with PART 4 (Sensitivity Analysis) below.

---

## PART 4: SENSITIVITY ANALYSIS SUITE

### Oster (2019) Delta (for OLS)

**What it measures**: How many times more strongly unobservables would need to be correlated with Y (relative to observed controls) to fully explain the coefficient.

- δ > 1: Unobservables must be stronger than all observables combined — usually implausible
- δ > 2: Strong robustness claim

```r
library(sensemakr)
sens <- sensemakr(lm(y ~ x + controls, data = df),
                  treatment = "x", benchmark_covariates = "key_control",
                  kd = 1:3)
summary(sens); plot(sens)
```

---

### E-Values (VanderWeele & Ding 2017)

**What it measures**: The minimum strength of association (on the risk ratio scale) that an unmeasured confounder would need to have with both treatment and outcome (jointly) to fully explain away the observed effect.

- E-value = RR + sqrt(RR × (RR - 1)) where RR is the observed relative risk
- Higher E-value = more robust result
- "The observed association could be explained away by an unmeasured confounder with E-value of [X]; to reduce the CI lower bound to null requires a confounder with E-value of [Y]"

```r
library(EValue)
# For risk ratio (binary outcome, binary exposure)
evalues.RR(est = 2.5, lo = 1.8, hi = 3.5)

# For odds ratio (logistic regression)
evalues.OR(est = 1.8, lo = 1.2, hi = 2.6, rare = TRUE)

# For mean difference (linear regression)
evalues.MD(est = 0.3, se = 0.1, sd = 1.2)
```

---

### Rosenbaum Bounds (for Matching)

**What it measures**: The odds ratio of hidden bias (Γ) that would be required to explain away the result when using matching estimators.

- Γ = 1: No unmeasured confounding
- Γ = 2: A hidden confounder that doubles the odds of treatment (after matching) could explain away the result
- If Γ* > 2 before p > 0.05: moderately robust

```r
library(rbounds)
psens(y_treated, y_control, Gamma = 3, GammaInc = 0.25)
# Find Gamma* at which p-value exceeds 0.05
```

---

### Placebo / Falsification Tests

1. **Pre-trend placebo (DiD)**: Run event study and check coefficients on pre-treatment periods are jointly zero (F-test)
2. **Placebo outcome**: Test X on outcome that cannot be caused by X (e.g., past outcomes, unrelated outcomes)
3. **Placebo treatment**: Randomize treatment assignment; check no effect
4. **Geographic/temporal placebo (RD)**: Run RD at placebo cutoffs; check null results
5. **Donut-hole (RD)**: Exclude observations very close to cutoff; check robustness

---

### HonestDiD (Rambachan & Roth 2023) — Sensitivity to Parallel Trends Violations

**What it measures**: How robust is the DiD estimate to deviations from parallel trends? Constructs honest confidence intervals that remain valid even if pre-trends deviate from zero by up to magnitude M.

**When to use**: Any DiD paper. Reviewers at ASR, AJS, Demography, and economics journals now routinely request this.

```r
library(HonestDiD)

# After running event study via fixest:
es_fit <- feols(y ~ i(time_to_treat, ref = -1) | id + year, data = df, cluster = ~state)

# Extract coefficients and variance-covariance matrix for pre/post periods
betahat <- coef(es_fit)[grep("time_to_treat", names(coef(es_fit)))]
sigma   <- vcov(es_fit)[grep("time_to_treat", rownames(vcov(es_fit))),
                         grep("time_to_treat", colnames(vcov(es_fit)))]

# Relative magnitudes approach (recommended)
delta_rm <- createSensitivityResults_relativeMagnitudes(
  betahat       = betahat,
  sigma         = sigma,
  numPrePeriods = 4,    # number of pre-treatment periods
  numPostPeriods = 3,   # number of post-treatment periods
  Mbarvec       = seq(0.5, 2, by = 0.5)  # M values to test
)

# Smoothness-based approach
delta_sd <- createSensitivityResults(
  betahat       = betahat,
  sigma         = sigma,
  numPrePeriods = 4,
  numPostPeriods = 3,
  Mvec          = seq(0, 0.05, by = 0.01)
)

# Plot sensitivity
createSensitivityPlot_relativeMagnitudes(delta_rm, rescaleFactor = 1)
```

**Reporting**: "We assess robustness to violations of parallel trends using the Rambachan and Roth (2023) procedure. The estimated treatment effect remains statistically significant for deviations from parallel trends up to [M] times the magnitude of the largest pre-trend, providing evidence that our results are not driven by differential pre-existing trends."

---

### Manski Bounds / Partial Identification

**What it measures**: When point identification fails (e.g., due to sample selection, missing outcomes, or violations of exclusion restriction), Manski bounds provide the range of treatment effects consistent with the data under minimal assumptions.

```r
# Lee (2009) bounds for sample selection in RCTs
library(sampleSelection)
# When attrition/selection differs by treatment status:
# Lower bound: trim top of treated distribution
# Upper bound: trim bottom of treated distribution

# Manual Lee bounds implementation:
lee_bounds <- function(y_treat, y_control, p_treat, p_control) {
  # Proportion always-observed
  s <- min(p_treat, p_control) / max(p_treat, p_control)
  if (p_treat > p_control) {
    # Trim treated distribution
    lower <- quantile(y_treat, 1 - s) - mean(y_control)
    upper <- quantile(y_treat, s) - mean(y_control)
  } else {
    lower <- mean(y_treat) - quantile(y_control, s)
    upper <- mean(y_treat) - quantile(y_control, 1 - s)
  }
  return(c(lower = lower, upper = upper))
}
```

---

### Spillover Sensitivity

**What it measures**: Sensitivity of treatment effect estimates to violations of SUTVA (no interference between units).

```r
# Spatial spillover test: include neighbor treatment as covariate
library(spdep)
nb <- poly2nb(shapes)
df$neighbor_treated <- lag.listw(nb2listw(nb), df$treatment)
m_spill <- feols(y ~ treatment + neighbor_treated + controls | id + year,
                 data = df, cluster = ~state)
# If neighbor_treated is significant, SUTVA may be violated
```

---

### Preregistered Sensitivity Checks (Recommended Suite)

| Check | Addresses | Code |
|-------|-----------|------|
| Oster delta or E-value | OLS confounding | `sensemakr`, `EValue` |
| Event study pre-trend F-test | DiD parallel trends | `fixest::iplot` |
| **HonestDiD** | **DiD — robust to PT violations** | **`HonestDiD`** |
| McCrary density test | RD manipulation | `rddensity` |
| Bandwidth sensitivity | RD robustness | `rdrobust` loop |
| First-stage F | IV weak instruments | `AER`, `fixest::fitstat` |
| Rosenbaum Γ | Matching hidden bias | `rbounds::psens` |
| ρ* sensitivity | Mediation sequential ignorability | `mediation::medsens` |
| **Manski / Lee bounds** | **Sample selection / attrition** | **Manual / `sampleSelection`** |
| **Spillover test** | **SUTVA violations** | **`spdep` neighbor lag** |
| **Causal forest calibration** | **HTE model validity** | **`grf::test_calibration`** |

---

### Specification Curve / Multiverse Sensitivity

**What it measures**: How much the headline result depends on defensible-but-arbitrary analytic choices — sample restrictions, covariate sets, outcome operationalizations, estimator family. Diagnoses Simpson-style sign reversals across alternative defensible specifications, which a single "preferred specification" can hide.

**When to use**: Any observational analysis with non-trivial analytic decisions. Reviewers at top sociology, political science, public health, and psychology journals increasingly request a spec-curve or multiverse appendix when the analytic decision tree is wide.

**Multiverse Analysis (Steegen, Tuerlinckx, Gelman, & Vanpaemel 2016)**: Enumerate every defensible *data-construction* choice (missing-data handling, outlier rules, scale construction, sample restrictions), run the full analysis under every combination, and report the *distribution* of estimates and p-values rather than a single point.

**Specification Curve Analysis (Simonsohn, Simmons, & Nelson 2020)**: Enumerate defensible *analytic specifications* (controls, fixed effects, estimator family). Display estimates sorted by magnitude with significance markers; conduct joint inference across the curve via permutation under the sharp null.

**R** (`specr`):

```r
# install.packages("specr")
library(specr)
specs <- setup(
  data     = df,
  y        = c("y_main", "y_log", "y_winsor"),
  x        = "treat",
  model    = c("lm", "feols"),
  controls = c("age", "female", "education"),
  subsets  = list(region = unique(df$region))
)
results <- specr(specs)
plot_specs(results, choices = c("y", "controls", "subsets"))
summary(results, type = "curve")
```

**Reporting template**:

> "To assess robustness to analytic choices, we conduct a specification curve analysis following Simonsohn, Simmons, and Nelson (2020). We define the universe of defensible specifications by crossing [N₁ outcome operationalizations] × [N₂ control sets] × [N₃ estimator families] × [N₄ sample restrictions], yielding [N] specifications. Across the curve, the median estimate is [X] and [Y]% of specifications are statistically significant at p < .05. Joint inference under the sharp null rejects at p = [Z]. The result is therefore not driven by an idiosyncratic specification choice."

**Pairs well with**: any sensitivity check above. A spec curve is a meta-sensitivity tool — it asks whether the *choice of sensitivity check* itself matters.

---

## PART 5: WRITING THE IDENTIFICATION ARGUMENT

### Canonical Identification Section Structure

```
1. CAUSAL CLAIM: State what causal effect you are trying to identify
2. THREATS: Name the main identification threats (confounders, reverse causality, selection)
3. STRATEGY: Name the identification strategy and why it is appropriate here
4. ASSUMPTIONS: State the core assumptions required (and that they are plausible)
5. EVIDENCE: Present evidence that assumptions hold (tests, falsification, sensitivity)
6. LIMITATIONS: Acknowledge what the strategy cannot address (and note it as a boundary)
```

### Templates by Strategy

**OLS template**: See Strategy 1 write-up template above.

**DiD template**: See Strategy 2 write-up template above.

**RD template**: See Strategy 3 write-up template above.

**IV template**: See Strategy 4 write-up template above.

**Panel FE template**: See Strategy 5 write-up template above.

**Matching template**: See Strategy 6 write-up template above.

**Synthetic control template**: See Strategy 7 write-up template above.

**Causal mediation template**: See Strategy 8 write-up template above.

**Staggered DiD template**: See Strategy 9 write-up template above.

**DML template**: See Strategy 10 write-up template (DML) above.

**Causal forest template**: See Strategy 10 write-up template (Causal Forest) above.

**Bunching template**: See Strategy 11 write-up template above.

**Shift-share / Bartik template**: See Strategy 12 write-up template above.

**Distributional / quantile template**: See Strategy 13 write-up template above.

---

### Consolidating Multiple Strategies

When using complementary strategies (e.g., PSM + OLS, FE + DiD, IV + OLS comparison):

> "Our primary specification employs [Strategy A], which addresses [Threat 1]. As a robustness check, we replicate the analysis using [Strategy B], which addresses [Threat 2] under different assumptions. The consistency of estimates across strategies strengthens confidence that [finding] is not an artifact of any single identification assumption (Table A[X])."

---

## PART 6: PRE-DESIGN DIAGNOSTIC EXECUTION

This skill emits a structured `diagnostic_plan.json` for every chosen strategy and **optionally runs lightweight pre-design diagnostics** when data is available and a basic data-clearance check passes. Estimation of the headline model itself belongs to your downstream analysis pipeline; this part is about catching design problems *before* the analysis commits.

### Tier 1 — `diagnostic_plan.json` (always emit)

For the selected strategy, write `${OUTPUT_ROOT}/diagnostic_plan.json` with this schema. A downstream code-review or pre-execution audit can consume it to verify the planned analysis actually implements the required tests.

```json
{
  "strategy": "<DiD | Staggered DiD | RD | IV | FE | Matching | Synthetic Control | Mediation | DML | Bunching | Bartik | Quantile | OLS>",
  "required_diagnostics": [
    {
      "id": "did_event_study_pretrend_Ftest",
      "purpose": "parallel trends",
      "tool": "fixest::iplot + joint F-test",
      "pass_criterion": "joint F-test on pre-treatment leads fails to reject at p > .10",
      "execute_at": "analysis_execution",
      "blocks_publication_if_failed": true
    },
    {
      "id": "honestdid_sensitivity",
      "purpose": "robustness to parallel-trends violations",
      "tool": "HonestDiD::createSensitivityResults_relativeMagnitudes",
      "pass_criterion": "estimate remains significant at M >= 1",
      "execute_at": "analysis_execution",
      "blocks_publication_if_failed": false
    }
  ],
  "pre_design_diagnostics": [
    {
      "id": "panelview_treatment_structure",
      "tool": "panelView::panelview(type='treat')",
      "purpose": "visualize treatment timing and cohort structure",
      "execute_at": "design_finalization"
    }
  ]
}
```

Build the `required_diagnostics` array from the chosen strategy. For DiD/Staggered DiD, include at minimum: event-study pre-trend F-test, HonestDiD sensitivity, treated-group post-period mean, spillover check, and one TWFE alternative (CS-2021 / SA-2021 / LP-DiD). For RD: McCrary density, bandwidth sensitivity, covariate continuity. For IV: first-stage F, over-identification (if multiple instruments), reduced-form check. For Matching: covariate balance < 0.1 SMD, common support, Rosenbaum bounds. For Synthetic Control: in-time and in-space placebos, pre-period RMSPE. The `execute_at` field is a user-defined label naming where in your workflow each test runs.

### Tier 2 — Pre-design diagnostic preview (opt-in, gated)

Run only when ALL of the following hold:
- User supplied a data path in arguments, OR a data-availability file is present in the project
- A clearance file exists confirming the data is ethically/legally cleared for inspection (your project may use any convention; the recipe below assumes a JSON file with per-source `status` and `rationale` fields)
- The strategy is panel-data-based (DiD, Staggered DiD, FE, Synthetic Control)

**Preview vs. headline boundary (binding)**: every artifact produced by Tier 2 must be written to `${PROJ:-.}/output/diagnostics/_PREVIEW/` (the underscore-prefixed name is deliberate — `[PREVIEW]` is a shell glob metacharacter and would silently match nothing in `ls` patterns) and PDF/PNG titles must carry a `PREVIEW — NOT HEADLINE` watermark. The point of Tier 2 is to falsify a design before it is locked, not to render publication figures. Headline estimates remain the territory of your downstream analysis script.

If gated open, execute these in R (do **not** estimate the headline model):

#### Panel-data preview with panelview + fect

The canonical staggered-DiD recipe — `panelview` for treatment-timing + missingness + outcome trajectories, then `fect` for the equivalence-test placebo — is in [`references/strategies.md` Strategy 9 → Pre-Design Diagnostic Recipe](references/strategies.md). All code blocks, citations (Mou-Liu-Xu 2023; Liu-Wang-Xu 2024), and reporting templates live there to keep the recipe single-sourced.

When invoking Tier 2 for staggered DiD, load that section and adapt the variable names. Remember the binding rule from above: every artifact saves to `output/diagnostics/_PREVIEW/` (no glob metacharacters) with a `PREVIEW — NOT HEADLINE` watermark.

**What the recipe catches before design is locked**: unbalanced panel; cohort sizes too small for CS-2021; treatment reversal (switchers) — which routes the design to de Chaisemartin-D'Haultfœuille `did_multiplegt_dyn` instead of CS-2021; differential attrition between treatment and control; outcome trajectories that already look suspicious.

#### Synthetic-control preview with gsynth (Xu 2017, *Political Analysis* 25(1):57–76)

When there are multiple treated units and rich pre-period controls — the canonical SC method does not handle this; gsynth does.

```r
# install.packages("gsynth")     # since v1.3.0 this is a wrapper for fect
library(gsynth)
gs <- gsynth(Y ~ D + X1 + X2, data = df, index = c("unit", "time"),
             estimator = "ife", se = TRUE, inference = "parametric",
             nboots = 1000, CV = TRUE, force = "two-way")
plot(gs, type = "counterfactual")
plot(gs, type = "gap")
```

#### Interaction-effect diagnostic with interflex (Hainmueller, Mummolo, Xu 2019)

When the design's identification relies on an interaction term (heterogeneity-by-X, dose-response, conditional ATT), check the linear-interaction assumption *before* writing it into the design.

```r
# install.packages("interflex")
library(interflex)
ix <- interflex(Y ~ D * X1 + X2, data = df, estimator = "binning",
                vartype = "robust", treat = "D", moderator = "X1")
plot(ix)                              # bin estimates vs. linear interaction
print(ix$tests$wald.test.p.value)     # Wald test for linearity
```

If the Wald test rejects, the planned design likely needs a flexible interaction (binning or kernel), not a multiplicative term — record this in your identification-strategy memo.

### Gating logic

```bash
# Diagnostic gate — must reject NEEDS_REVIEW, HALTED, AND bare OVERRIDE
# Assumes a JSON clearance file at $SAFETY with per-source {status, rationale}
# entries; adapt the path to whatever your project uses.
SAFETY="${PROJ:-.}/safety-status.json"
if [ ! -f "$SAFETY" ]; then
  echo "No clearance status found; running Tier-1 plan only."
  RUN_TIER2=0
elif grep -qE '"status"\s*:\s*"(NEEDS_REVIEW|HALTED)"' "$SAFETY"; then
  echo "Clearance NEEDS_REVIEW or HALTED; running Tier-1 plan only. Complete your data-clearance review."
  RUN_TIER2=0
elif python3 -c "
import json, sys
d = json.load(open('$SAFETY'))
# Reject if any entry is OVERRIDE without a non-empty rationale string
def bad(e):
    return (isinstance(e, dict) and e.get('status') == 'OVERRIDE'
            and not (isinstance(e.get('rationale'), str) and e['rationale'].strip()))
entries = d.get('files', d if isinstance(d, list) else [])
sys.exit(0 if any(bad(e) for e in entries) else 1)
" 2>/dev/null; then
  echo "Bare OVERRIDE without rationale; running Tier-1 plan only."
  RUN_TIER2=0
else
  mkdir -p "${PROJ:-.}/output/diagnostics/_PREVIEW"
  RUN_TIER2=1
fi
```

This gate uses the conventional "cleared-or-explicitly-overridden" semantics: `NEEDS_REVIEW`, `HALTED`, and bare `OVERRIDE` all block. A passing entry must be `CLEARED` or `OVERRIDE` with a non-empty `rationale` string. All Tier-2 outputs land in `output/diagnostics/_PREVIEW/` so they cannot be mistaken for headline artifacts.

### What Tier 2 does **not** do

It does not estimate the headline model. It does not produce the publication tables. It does not replace a full estimation pass. If the user wants estimates, route them forward; this skill stops at "your design is structurally sound, here is the verified plan and the assumption-check sketches, hand off to your downstream analysis pipeline."

---

## Quality Checklist

- [ ] Causal question stated precisely (X → Y for population P, identification context)
- [ ] DAG drawn; backdoor paths listed; minimal adjustment set identified
- [ ] No mediators, colliders, or post-treatment variables in control set
- [ ] Identification strategy selected and justified against alternatives
- [ ] Core assumptions stated and evidence provided for each
- [ ] Diagnostics run and reported (pre-trend test / McCrary / first-stage F / balance / etc.)
- [ ] `diagnostic_plan.json` emitted with strategy-keyed `required_diagnostics` array (PART 6, Tier 1) — machine-readable so a downstream code review can verify the analysis actually implements each test
- [ ] If panel data: Tier-2 `panelview` audit run (or explicitly skipped with rationale logged in `${PROJ:-.}/output/diagnostics/tier2-skip-rationale.md`) before design is locked
- [ ] Sensitivity analysis performed (Oster delta / E-value / Rosenbaum Γ / ρ* / placebos)
- [ ] Identification argument paragraph written and placed in Methods section
- [ ] Limitations acknowledged

See [references/dag-patterns.md](references/dag-patterns.md) for 18 DAG patterns.
See [references/identification-toolkit.md](references/identification-toolkit.md) for full strategy code.
See [references/matching-weighting.md](references/matching-weighting.md) for matching/reweighting details.

---

## Save Output

After displaying the full output to the user, save the complete output to a Markdown file using the Write tool.

### Version Collision Avoidance (MANDATORY)

**Before EVERY Write tool call below**, run this Bash block to determine the correct save path. Do NOT hardcode paths from the filename templates — they show naming patterns only.

```bash
# MANDATORY: Replace [values] with actuals before running
# BASE pattern: scholar-causal-[topic-slug]-[YYYY-MM-DD]
# Split into directory and stem for the gate script:
OUTDIR="$(dirname "scholar-causal-[topic-slug]-[YYYY-MM-DD]")"
STEM="$(basename "scholar-causal-[topic-slug]-[YYYY-MM-DD]")"
mkdir -p "$OUTDIR"
bash "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/version-check.sh" "$OUTDIR" "$STEM"
```

**Use the printed `SAVE_PATH` as `file_path` in the Write tool call.** Re-run this block (with the appropriate BASE) for each additional file. The same version suffix must be used for all related output files (.md, .docx, .tex, .pdf).


**Filename format**: `scholar-causal-[topic-slug]-[YYYY-MM-DD].md`
- `topic-slug`: lowercase, hyphen-separated key words from the research question (e.g., `redlining-activity-space-segregation`, `education-earnings-iv`, `neighborhood-health-did`)
- `YYYY-MM-DD`: today's date

**What to save** — include all sections that were generated:
1. Causal question (precise statement of X → Y, population, context)
2. Variable inventory (treatment, outcome, mediators, confounders, instruments)
3. DAG notation and backdoor/frontdoor paths
4. Method selection table and justification
5. Selected strategy deep-dive: assumptions, workflow, diagnostics
6. All R and Stata code blocks produced
7. Sensitivity analysis plan (Oster delta / E-value / Rosenbaum Γ / ρ* / placebos)
8. Identification argument paragraphs (Methods section ready text)
9. Limitations and scope conditions

**Example Write call**:
```
Write tool → file_path: "scholar-causal-[topic-slug]-[YYYY-MM-DD].md"
             content: [full markdown output from this session]
```

After saving, confirm the file path to the user so they can locate the saved analysis.

**Emit `identification-strategy.json` (MANDATORY when a DAG-based design is selected):**

`scholar-analyze` binds to this skill through a structured JSON sidecar. When the downstream ladder (`scholar-analyze/references/ladder-observational-causal.md`) sees `Design Type: observational-causal-with-DAG`, it hard-errors if this file is missing. Write it AFTER the prose `.md` has been saved.

```bash
. "${SCHOLAR_SKILL_DIR:-.}/scripts/gates/derive-proj.sh" 2>/dev/null || PROJ="${OUTPUT_ROOT:-output}/${PROJ_SLUG:-.}"
mkdir -p "${PROJ}/design"

# Fill the values below from the DAG, adjustment set, and method selection you already produced above.
# adjustment_set, mediators_excluded, colliders_excluded are JSON arrays (use [] when empty).
cat > "${PROJ}/design/identification-strategy.json" << 'JSONEOF'
{
  "design_type": "observational-causal-with-DAG",
  "identification_strategy": "<OLS + backdoor adjustment | FE | DiD | RD | IV | matching | synthetic control>",
  "treatment_variable": "<X>",
  "outcome_variable": "<Y>",
  "adjustment_set": ["<C1>", "<C2>", "<C3>"],
  "mediators_excluded": ["<M1>"],
  "colliders_excluded": ["<K1>"],
  "assumptions": ["no unmeasured confounding", "positivity", "SUTVA"],
  "robustness_battery": ["oster_delta", "e_value", "bounds_manski"],
  "source_md": "<filename of the prose scholar-causal-*.md just saved>",
  "emitted_at": "<YYYY-MM-DD HH:MM>"
}
JSONEOF

# Sanity-check it parses
python3 -c "import json,sys; json.load(open('${PROJ}/design/identification-strategy.json'))" \
  && echo "identification-strategy.json: OK" \
  || { echo "ERROR: identification-strategy.json is not valid JSON — fix before proceeding to /scholar-analyze."; exit 1; }
```

**Important:** If the identification strategy is NOT `observational-causal-with-DAG` (e.g., this session produced a DiD, RD, or IV design), still emit the JSON but set `design_type` to match: `quasi-experimental:DiD`, `quasi-experimental:RD`, or `quasi-experimental:IV`. The `adjustment_set` for those designs is whichever covariates enter the main regression (may be empty for a pure event-study). The ladder `ladder-quasi-experimental.md` reads the same file.

**Close Process Log:**

Run the following to finalize the process log:

```bash
OUTPUT_ROOT="${OUTPUT_ROOT:-output}"
SKILL_NAME="scholar-causal"
LOG_DATE=$(date +%Y-%m-%d)
LOG_FILE="${OUTPUT_ROOT}/logs/process-log-${SKILL_NAME}-${LOG_DATE}.md"
if [ ! -f "$LOG_FILE" ]; then
  LOG_FILE=$(ls -t "${OUTPUT_ROOT}/logs/process-log-${SKILL_NAME}-${LOG_DATE}"*.md 2>/dev/null | head -1)
fi
cat >> "$LOG_FILE" << LOGFOOTER

## Output Files
[list each output file path as a bullet]

## Summary
- **Steps completed**: [N completed]/[N total]
- **Files produced**: [count]
- **Errors**: [count, or 0]
- **Time finished**: $(date +%H:%M:%S)
LOGFOOTER
echo "Process log saved to $LOG_FILE"
```
