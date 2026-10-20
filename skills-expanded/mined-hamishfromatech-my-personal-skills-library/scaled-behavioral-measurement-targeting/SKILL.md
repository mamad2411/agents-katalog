---
name: scaled-behavioral-measurement-targeting
description: Combines incentivized behavioral measurement with machine learning to create theory-guided treatment targeting rules at scale. Use when designing personalized interventions where latent behavioral moderators (loss aversion, time preferences, risk attitudes) drive heterogeneous treatment effects but cannot be observed at field scale. NOT for purely data-driven CATE estimation when large pilot RCT data is available and theory is unclear.
---

# Scaled Behavioral Measurement Targeting

## Overview

Scales individual-level behavioral preferences (e.g., loss aversion) from a small incentivized measurement sample to a large field population using machine learning on universally available digital footprints, enabling theory-guided treatment targeting that outperforms purely data-driven causal forest approaches — even without pilot treatment-effect data.

## When to Use

- Designing personalized interventions (messaging, pricing, nudges) where treatment effects are heterogeneous
- A latent behavioral construct (loss aversion, time preference, risk attitude) is theoretically identified as a moderator but not observable at field scale
- Large-scale RCT piloting is infeasible, costly, risky, or outcomes are noisy
- You want interpretable, theory-grounded targeting rules rather than black-box CATE estimates
- Cross-context portability matters (theory-anchored rules may transfer better than data-fit rules)

NOT for...
- Settings where the relevant moderator is directly observable (just target on it directly)
- Pure prediction problems with no causal treatment assignment
- Environments where large pilot RCT data with clean treatment variation is already available and theory offers no clear moderator

## Core Process / Workflow

### Step 1: Identify the Theory-Grounded Moderator

Identify which latent preference/causal moderator economic or behavioral theory predicts should drive heterogeneous treatment effects.

```
Example: Loss aversion (Kahneman & Tversky, 1979) predicts response to loss-framed messages.
Question: "Does theory tell us WHO should respond differently to this treatment?"
If no → use causal ML. If yes → continue.
```

### Step 2: Behavioral Measurement in a Small Sample

Design an incentivized behavioral measurement experiment (N ≈ 200-600) to elicit the latent construct at the individual level.

**Key design principles:**
- Must be incentivized (real stakes, not hypothetical)
- Can be coarse (partial ordering, not precise cardinal measure)
- Measure must be observable for each individual in the sample
- Keep it short for field/online settings (single-choice tasks acceptable)

**Loss aversion elicitation example (Bauer et al., 2026):**
1. Endow participant with a 15% voucher (establish reference point)
2. Offer a binary lottery: keep voucher vs. stake it (potential loss + larger potential gain)
3. Vary the potential gain across 3 between-subject conditions
4. Classify into 6 ordered categories based on accept/declade × condition

**Partial ordering derivation (Measurement 1):**
- Declining a more favorable gamble → higher loss aversion
- λ̄(1D) ≤ λ̄(2D) ≤ λ̄(3D)  [decliners ordered by gamble favorability]
- λ̄(VA) ≤ λ̄(VD) ∀V  [acceptors less loss-averse than decliners within version]

### Step 3: Link Measurement Sample to Field via Shared Observables

Identify "digital footprints" — variables observed in BOTH the measurement sample and the field sample at the moment targeting is needed.

**Universally available field data (no custom tracking):**
- Referral source (Google, newsletter, social)
- Entry page / category
- IP region (coarse geography)
- Device type (mobile/desktop)
- Operating system
- Browser type
- IP provider / ISP
- Time of week

**Key constraint:** These must be available at the targeting decision moment (e.g., website entry), not after behavioral engagement.

### Step 4: Train ML to Predict Latent Construct

Train a classifier to map digital footprints → behavioral construct categories.

```python
# XGBoost multiclass classification (Bauer et al., 2026)
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV

# Why classification not regression:
# The observed category is a LOWER BOUND (one-sided noisy measure),
# not a precise cardinal value. Regression would treat the bound as exact.
# Classification learns "most likely observed class given footprint."

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.7, 0.8, 0.9],
    'colsample_bytree': [0.7, 0.8, 0.9],
    'reg_alpha': [0, 0.1, 1.0],
    'reg_lambda': [1.0, 5.0, 10.0]
}

search = RandomizedSearchCV(
    xgb.XGBClassifier(objective='multi:softprob', eval_metric='mlogloss'),
    param_grid, n_iter=50, cv=5, scoring='f1_macro', n_jobs=-1
)
search.fit(X_train, y_train)  # y = 6 loss-aversion categories
model = search.best_estimator_
```

**Critical: exclude measurement-sample participants from field targeting evaluation** to prevent data leakage.

### Step 5: Validate Treatment-Effect Heterogeneity

Before deploying, confirm the predicted construct explains treatment-effect heterogeneity in the field sample.

1. Run the RCT at field scale (treatment vs. control, randomly assigned)
2. Predict latent construct for all field participants
3. Estimate Group Average Treatment Effects (GATE) per predicted category
4. Check: Do high-predicted-loss-aversion individuals respond more positively to loss framing?

**Bauer et al. (2026) validation results:**
- Above-median predicted loss aversion: +1.5% to +6.5% purchase volume from loss framing
- Below-median: -2.2% to -6.3% (treatment backfires)
- Overall ATE: insignificant (opposing effects cancel)

### Step 6: Define Targeting Policy & Off-Policy Evaluation

Define a treatment rule: treat only individuals whose predicted construct falls in the responsive range.

```
Policy: Treat if predicted_loss_aversion ∈ {Categories 4, 5, 6}
        (above-median; ≈43% of population)
```

**Off-policy evaluation** (estimate counterfactual using existing RCT data):
```python
# R_obs[j] = observed avg revenue for group j
# j ∈ {(TT,T), (TT,C), (NT,T), (NT,C)}
# TT = targeted-for-treatment, NT = non-targeted, T = actually treated, C = control

# Counterfactual revenue under targeting policy:
# R_hat = α * R_TT,T + (1 - α) * R_NT,C
# where α = share targeted

policy_effect = R_hat - R_control_avg
```

Bootstrap with 100 Monte Carlo iterations (50/50 train-test splits) for confidence intervals.

### Step 7: Benchmark Against Causal Forest

Compare theory-guided targeting vs. data-driven causal forest:

```python
from econml.dml import CausalForestDML
# Train on 70% of RCT, evaluate on 30%
# Hurdle model for zero-inflated outcomes (purchase/no-purchase)

cf = CausalForestDML(
    model_y=HurdleRegressor(),  # handles zero-inflation
    discrete_treatment=True,
    n_estimators=1000
)
cf.fit(Y_train, T_train, X_train)
ites = cf.effect(X_eval)
```

**Bauer et al. (2026) benchmark results:**
| Approach | Revenue Lift | CI | Significance |
|---|---|---|---|
| Scaled behavioral measurement | +1.9% | [1.66%, 2.21%] | p < 0.01 |
| Causal Forest (with 250K pilot) | +0.16% | [-0.01%, 0.4%] | n.s. |
| Random targeting (placebo) | -0.05% | [-0.23%, 0.12%] | n.s. |

## Why Theory-Guided Can Beat Data-Driven

**Signal-to-noise ratio:** Direct estimation of heterogeneous treatment effects from noisy outcomes is statistically demanding. The behavioral measurement provides an individual-level moderator observed for every subject (high signal), whereas treatment effects are only observed between-subjects (low signal, high noise).

**Proxy-based targeting theorem (Fernández-Loría & Provost, 2022):** When a proxy captures an important moderator of treatment response, proxy-based targeting can outperform direct CATE estimation.

**Interpretability:** Treatment assignment is explainable ("we treat you because you're predicted loss-averse and loss framing works for loss-averse people"). This matters for GDPR right-to-explanation, anti-discrimination compliance, and consumer trust.

**Portability:** Theory-anchored rules may transfer across populations/platforms better than sample-fit black-box models (economic theory as regularization).

## Deployment Guardrails

- **Measurement cost vs. pilot cost:** If running a behavioral measurement (N≈500) is cheaper than a pilot RCT (N≈250K), use scaled measurement. If pilots are cheap and clean, causal ML may suffice.
- **Coarse measurement is conservative:** A single-choice elicitation introduces noise; more elaborate protocols should improve targeting further (results are a lower bound on the method's potential).
- **No-cardinal-assumption:** Don't treat the predicted category as a precise number; use it as an ordinal ranking for thresholding.
- **Exclude measurement participants from field evaluation** to avoid leakage.
- **Monitor for distribution shift:** Digital footprints may change across seasons/platforms; re-validate the measurement-to-field link periodically.
- **Ethical targeting:** Theory-guided is not automatically ethical. Loss-aversion targeting could exploit a vulnerability. Consider whether targeting benefits the consumer, not just the firm.

## A-Tech Alignment

| A-Tech Value | Alignment |
|---|---|
| **Open-source AI** | XGBoost, scikit-learn, EconML are all open-source; method is reproducible with open tools |
| **Data privacy** | Digital footprints are universally available (no tracking required); measurement is incentivized and consented; no biometric/sensitive data |
| **Financial freedom** | Enables SMEs to target effectively without large-scale RCT infrastructure; reduces marketing waste on non-responsive segments |
| **Practical implementation** | Validated at N≈500,000 field scale with 582 measurement participants; 50+50 bootstrap protocol; EconML benchmark |

## Cross-References

- `behavioral-design-practical-playbooks` — behavioral design patterns this method can target
- `digital-nudging-ethical-persuasion` — ethical framing for targeting vulnerable segments
- `nudge-effectiveness-reality-check` — evidence on nudge heterogeneity this method exploits
- `hyperbolic-discounting-reversal` — another latent preference that could be scaled via this method
- `ai-pricing-model-taxonomy-2026` — pricing personalization application of the method
- `friction-based-pricing-discovery` — complementary approach to discovering willingness-to-pay heterogeneity

## References

- See [references/scaled-behavioral-measurement-evidence-base.md](references/scaled-behavioral-measurement-evidence-base.md) for the full evidence base, mathematical derivations, experimental design, off-policy evaluation details, and benchmark comparisons.