---
name: bayesian-decision-analysis
description: Turn posterior distributions into optimal actions using loss functions, expected value of information, and the newsvendor framework. Use when the user has a Bayesian model and needs to make a decision under uncertainty — pricing, inventory, ship-or-wait, resource allocation. Covers EVPI, EVSI, custom loss functions, and asymmetric cost structures.
---

<!-- Bundled files (accessible via ${CLAUDE_SKILL_DIR}):
  - SKILL.md — this file
  - scripts/demo.py — runnable marimo notebook with worked example
-->

# Bayesian Decision Analysis

Every other Bayesian bundle gives you a posterior. This bundle shows
you what to **do** with it. Decision analysis is the framework for
choosing the action that minimizes expected cost (or maximizes expected
utility) given your uncertainty about the world.

## When to use this skill

- You have a posterior distribution (from any Bayesian model) and need
  to choose an action
- The cost of being wrong is asymmetric (overprediction costs
  differently than underprediction)
- You need to decide whether to collect more data or act now
- Stakeholders ask "what should we do?" not "what is the parameter?"
- You need to quantify the dollar value of additional information

## When NOT to use this skill

- You just need parameter estimates or predictions → use the
  inference bundles directly
- The decision is purely classification (binary output) → use
  threshold tuning from the `binary-classification` bundle
- You're comparing two specific variants → use `bayesian-ab-testing`
  (which already includes expected loss)

## The three-step framework

Every Bayesian decision problem follows the same pattern:

### Step 1: Posterior

Get $P(\theta \mid \text{data})$ from your Bayesian model. This is
what the other bundles produce — the posterior is the input to
decision analysis, not the output.

### Step 2: Loss function

Define $L(a, \theta)$ — the cost of taking action $a$ when the true
state of the world is $\theta$. **This is the business input.** It
comes from stakeholders, domain experts, or regulatory requirements,
not from the data.

### Step 3: Minimize expected loss

$$a^* = \arg\min_a \; \mathbb{E}_{\theta \sim \text{posterior}}[L(a, \theta)]$$

With posterior samples:

```python
theta_samples = idata.posterior["theta"].to_numpy().flatten()

actions = np.linspace(low, high, 1000)
expected_losses = np.array([
    np.mean(loss_fn(a, theta_samples))
    for a in actions
])
optimal_action = actions[np.argmin(expected_losses)]
```

## Loss functions and their optimal actions

| Loss function | Formula | Optimal action | Use when |
|---|---|---|---|
| Squared error | $(a - \theta)^2$ | Posterior **mean** | Symmetric cost, no outliers |
| Absolute error | $\lvert a - \theta \rvert$ | Posterior **median** | Robust to outliers |
| 0-1 loss | $\mathbb{1}[a \neq \theta]$ | Posterior **mode** (MAP) | Classification |
| Asymmetric linear | $c_u \max(\theta-a, 0) + c_o \max(a-\theta, 0)$ | Posterior **quantile** at $\frac{c_u}{c_u + c_o}$ | Over/under costs differ |
| Custom | $L(a, \theta)$ | Compute numerically | Always the right move |

**For real problems, always define a custom loss.** Squared error is
a modeling convenience, not a business objective. The ten minutes
spent defining the right loss function matters more than the ten
hours spent tuning the model.

## Expected Value of Perfect Information (EVPI)

EVPI answers: **what's the maximum I should spend on any
information?**

```python
# Current best action's expected loss
current_loss = np.mean(loss_fn(optimal_action, theta_samples))

# With perfect info: for each possible true theta, pick the best action
perfect_losses = np.array([
    np.min([loss_fn(a, theta) for a in actions])
    for theta in theta_samples
])
perfect_loss = np.mean(perfect_losses)

evpi = current_loss - perfect_loss
```

If EVPI = $500, then even an omniscient oracle is worth at most $500.
Any data collection, consulting, or research that costs more than
this is not worth it.

## Expected Value of Sample Information (EVSI)

EVSI answers: **how much is N more data points worth?**

```python
evsi_values = []
for n_extra in [100, 500, 1000, 5000]:
    future_losses = []
    for s in range(n_mc):
        # Draw a "true" state from current posterior
        theta_true = theta_samples[s]

        # Simulate future data under this true state
        future_data = simulate(theta_true, n_extra)

        # Update posterior with future data
        updated_posterior = update(current_posterior, future_data)

        # Find optimal action under updated posterior
        optimal_loss = min_expected_loss(updated_posterior, actions)
        future_losses.append(optimal_loss)

    evsi = current_min_loss - np.mean(future_losses)
    evsi_values.append(evsi)
```

**When to stop collecting data:** if EVSI(n) * business_value < cost
of collecting n samples, stop and decide now.

## Common decision scenarios

### Pricing under demand uncertainty

- **Action:** price $p$
- **Uncertain:** demand curve parameters $(\alpha, \beta)$
- **Loss:** negative expected revenue = $-p \cdot \text{demand}(p; \alpha, \beta)$
- **Optimal:** sweep prices, pick the one with highest expected revenue

### Inventory (newsvendor problem)

- **Action:** order quantity $q$
- **Uncertain:** demand $d$
- **Loss:** $c_o \max(q - d, 0) + c_u \max(d - q, 0)$
  (overage cost + underage cost)
- **Optimal:** order at the $\frac{c_u}{c_u + c_o}$ quantile of the
  posterior predictive demand distribution

### Ship-or-wait (A/B test stopping)

- **Action:** ship treatment (B) now, keep control (A), or continue
  testing
- **Uncertain:** true conversion rates $p_A, p_B$
- **Loss:** expected regret of shipping the wrong variant
- **Optimal:** ship when expected loss < cost of continued testing

### Resource allocation

- **Action:** allocate budget across K options
- **Uncertain:** return rate of each option
- **Loss:** negative expected total return
- **Optimal:** portfolio optimization over posterior samples

## MLflow logging

| Kind | What |
|---|---|
| `params` | scenario, loss_function, action_space, n_mc, prior_spec |
| `metrics` | optimal_action, expected_loss, evpi, evsi_at_n |
| `tags` | decision_type, data_hash |
| `artifacts` | posterior/idata.nc, plots/{loss_curve.png, evpi.png, evsi_curve.png} |

## Common pitfalls

1. **Using squared error loss by default.** Squared error is a
   mathematical convenience, not a business objective. If
   underprediction costs 10x more than overprediction, use
   asymmetric loss.
2. **Ignoring EVPI.** If the maximum value of perfect information is
   $200, don't spend $5000 on a better model or more data.
3. **Confusing posterior summaries with decisions.** The posterior
   mean is only the optimal action under squared loss. For asymmetric
   costs, the optimal action is a quantile, not the mean.
4. **Not involving stakeholders in loss function design.** The loss
   function encodes business priorities. Data scientists can't define
   it alone — it needs input from the people who bear the costs.
5. **Computing EVSI without accounting for experimentation cost.**
   EVSI of $100 doesn't mean "collect more data." It means "more
   data is worth $100." If collection costs $150, stop.
6. **Point-estimate decisions when you have a posterior.** If you
   have a posterior and only use the mean to make decisions, you're
   throwing away uncertainty information. Use the full posterior.
7. **Optimizing the wrong metric.** Revenue maximization, profit
   maximization, and regret minimization give different optimal
   actions. Make sure you're optimizing what the business actually
   cares about.

## Worked example

See `demo.py` (marimo notebook). It works three scenarios end-to-end:
optimal pricing under demand uncertainty, inventory ordering
(newsvendor), and ship-or-wait with EVSI. Also demonstrates how
different loss functions change the optimal point estimate for a
skewed posterior. Run it with:

```
marimo edit --sandbox demo.py
```

## References

- Raiffa & Schlaifer (1961), *Applied Statistical Decision Theory*
- Berger (1985), *Statistical Decision Theory and Bayesian Analysis*
- Bayesian Methods for Hackers, Chapter 5 (Loss Functions)
