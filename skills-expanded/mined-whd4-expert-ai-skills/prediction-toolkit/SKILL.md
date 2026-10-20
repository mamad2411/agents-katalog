---
name: prediction-toolkit
description: "Route prediction and forecasting problems to the right method. Covers 7 families: Monte Carlo simulation, statistical forecasting (ARIMA/exponential smoothing), machine learning, Bayesian inference, crowd aggregation, causal inference, and first-principles modeling. Use when you need to predict a future outcome, quantify uncertainty, forecast time-series, update a belief with evidence, infer a cause, or synthesize expert opinions. Combines Monte Carlo Predictor, bootstrap, Bayesian update, and exponential smoothing as callable tools; routes to external methods (ML, markets, causal, physics) when those are the right fit."
version: "1.0.0"
tags: ["prediction", "forecasting", "uncertainty", "bayesian", "simulation", "decision-making", "risk-analysis"]
---

# Prediction Toolkit

**Purpose:** When a user question involves **predicting the future, quantifying uncertainty, updating a belief with evidence, or inferring what would happen under a different decision**, this skill picks the right tool from seven families and runs it. It is a decision router + a set of runnable methods.

Without this skill, Claude defaults to linear prose reasoning and quietly skips quantitative methods. With this skill, Claude reaches for the method that actually fits the shape of the problem.

---

## When to use this skill

Load this skill when any of these apply:

- The question is about **the future** ("how long will...", "what's the chance...", "forecast X")
- The question asks for **uncertainty quantification** ("what's the range of likely outcomes", "what's the P95 worst case")
- The question involves **updating a belief** ("given this new data, should I change my estimate")
- The question involves **comparing decisions** under uncertainty ("should we do A or B")
- The question asks **why** something happened or what would happen **if we changed X** (causal)
- The question involves **small data and confidence bounds** ("5 out of 100 — how confident can I be")
- The question involves **aggregating expert opinions** or **market signals**

Do NOT load this skill for:
- Deterministic calculations (arithmetic, currency conversion, geometry) — just do the math
- Questions with explicit known answers (look them up)
- Tasks where there's no uncertainty at all

---

## The seven method families

Each family solves a different *shape* of prediction problem. The router below maps problem shape → method.

| # | Family | Implemented here? | Best for |
|---|--------|-------------------|----------|
| 1 | **Statistical forecasting** | ✅ `exponential_smoothing.py` (guide for ARIMA/Prophet) | Time-series with history, forecast next N periods |
| 2 | **Machine learning** | Guide in `methods/machine-learning.md` | High-dim features, lots of labeled data, nonlinear relationships |
| 3 | **Bayesian inference** | ✅ `bayesian_update.py` | Update a belief with new evidence; small-sample rate estimation |
| 4 | **Simulation (Monte Carlo + bootstrap)** | ✅ Monte Carlo via `monte-carlo-predictor` skill; ✅ `bootstrap.py` | Uncertain inputs + a model; CI on a sample statistic |
| 5 | **Crowd aggregation** | Guide in `methods/crowd-aggregation.md` | Multiple independent estimates or expert opinions to combine |
| 6 | **Causal inference** | Guide in `methods/causal-inference.md` | "What if we changed X?" — counterfactual / intervention questions |
| 7 | **First-principles / physics** | Guide in `methods/first-principles.md` | Known underlying laws; extrapolate beyond the data regime |

Where "guide" is listed, the toolkit tells you *when to reach for that family and what library/approach to use*, rather than duplicating production libraries. This is deliberate — bad implementations of these methods are worse than pointing at the right library.

---

## How to pick a method (decision tree)

```
Is this about predicting a FUTURE outcome?
├── YES
│   ├── Do you have historical time-series data?
│   │   ├── YES → statistical forecasting
│   │   │         • short series, want simple forecast → exponential_smoothing
│   │   │         • long series, need confidence bands → ARIMA (external / scipy)
│   │   │         • many features, nonlinear → machine learning
│   │   └── NO  → do you have a model + uncertain inputs?
│   │             ├── YES → Monte Carlo (use monte-carlo-predictor skill)
│   │             └── NO  → crowd aggregation / expert elicitation
│   │
│   └── Need to combine multiple methods?
│       → Monte Carlo for uncertainty + ML point forecast as an input
│
└── NO — this is about explaining the past or updating a belief
    ├── Updating a probability with new evidence?
    │   → bayesian_update
    │
    ├── Small sample, need CI on a mean/median/etc.?
    │   → bootstrap
    │
    ├── "Would X have changed the outcome?" (counterfactual)
    │   → causal inference (read methods/causal-inference.md)
    │
    └── Need the underlying physics to extrapolate?
        → first-principles (read methods/first-principles.md)
```

Use `python -m engine.router recommend "<problem description>"` to get an automated recommendation.

---

## Workflow

When a user asks a prediction/forecasting question:

1. **Classify the shape** of the problem using the decision tree above (or run `router.py recommend`).
2. **Reach for the matching method**:
   - Monte Carlo: invoke the `monte-carlo-predictor` skill
   - Bootstrap: `from engine.bootstrap import bootstrap_ci`
   - Bayesian: `from engine.bayesian_update import beta_binomial_update`
   - Exponential smoothing: `from engine.exponential_smoothing import forecast`
   - For ML/crowd/causal/first-principles: read the corresponding `methods/*.md` guide — they document when to escalate to external tooling or specific libraries
3. **Combine when needed**:
   - Bayesian prior + Monte Carlo forward simulation
   - Bootstrap CI on a ML model's predictions
   - Exponential smoothing forecast as a Monte Carlo input
4. **Report honestly**:
   - State which method was used and why
   - Name the key assumptions (distributions, priors, smoothing params)
   - Quote uncertainty ranges, not just point estimates
   - Flag when the method might be wrong (tiny sample, untested prior, structural break risk)

---

## Interfaces

All four integration paths, same as monte-carlo-predictor:

```bash
# Python API
from engine import bootstrap_ci, bayesian_update, forecast, recommend_method

# CLI
python -m engine router recommend "forecast next quarter's revenue"
python -m engine bootstrap --data data.csv --stat mean --ci 0.95
python -m engine bayes --prior "beta(2,8)" --successes 5 --trials 20
python -m engine forecast --series data.csv --periods 4

# JSON stdin/stdout
echo '{"method":"bootstrap","data":[1,2,3,4,5],"stat":"mean"}' | python -m engine run -

# MCP server
python -m engine.mcp_server
```

See `engine/agent_contract.md` for the stable interface spec.

---

## Design rules

1. **No raw `eval`.** All user-supplied expressions go through the safe evaluator from `monte-carlo-predictor` (or equivalent AST whitelist).
2. **Pure data in, pure data out.** Specs are JSON/YAML; outputs are JSON. Safe for LLM agents to generate.
3. **Pure Python fallbacks.** Methods work without numpy/scipy; they use optimized libraries when available.
4. **Each method is independently callable.** No "god-mode" function — the agent composes methods.
5. **Honest uncertainty.** Every output includes confidence bounds and caveats. No false precision.

---

## Working examples

- `examples/ab-test-bayesian/` — Bayesian A/B test update
- `examples/sales-forecast-smoothing/` — Time-series forecast with exponential smoothing
- `examples/bootstrap-ci/` — Confidence intervals from a tiny sample

---

## Tests

```bash
cd skills/prediction-toolkit && python3 -m engine.tests.test_toolkit
```

All tests must pass before shipping any changes.

---

## Related skills

- **`monte-carlo-predictor`** — The Monte Carlo family lives there. This skill routes to it for simulation problems. Do not duplicate.

---

## Honest limits

- The router is a heuristic. It suggests, it doesn't decide. Override when you have context.
- ML/crowd/causal/first-principles are **guides, not implementations** in this skill. They tell you *when and how* to reach for external tooling. Building them in Python without scipy/sklearn/pyro would be dishonest about quality.
- The value of the toolkit is 80% **knowing which tool to reach for** and 20% the specific implementation. Treat the router as the main product.
