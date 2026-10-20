---
name: 402pilot-buyer-side-payment-decision
description: Applies the 402Pilot buyer-side decision layer for autonomous agent micropayments to design spending policies that learn service value and adapt purchasing decisions under wallet pressure. Use when building autonomous agents that pay for API calls, designing budget-constrained provider selection policies, implementing pay-per-inference routing, or developing buyer-side decision-making for x402/AP2 payment protocols.
---

# 402Pilot: Buyer-Side Payment Decision Layer for Autonomous Agent Micropayments

## Overview
A protocol-agnostic buyer-side decision layer between autonomous agents and payment execution that implements purchasing policies for selecting among payable providers — solving the problem that programmable payment protocols (x402, AP2) handle execution but do not determine which payable service an agent should buy under a finite wallet.

## When to Use
- Building autonomous agents that pay for API calls, MCP tools, or inference endpoints
- Designing budget-constrained provider selection policies
- Implementing pay-per-inference routing across multiple model providers
- Developing buyer-side decision-making for x402, AP2, or ACP payment protocols
- Managing agent spending under finite wallet constraints with changing market conditions
- Building cost-aware LLM routing with post-payment feedback learning
- NOT for: payment execution infrastructure (use x402/AP2/ACP directly); human-operated purchasing decisions

## Core Process / Workflow

### The Agent-Native Payment Decision Problem

An autonomous buyer interacts with K payable providers over T rounds, starting with wallet balance B₀ = B:

```
Task arrives (context x_t) → Derive affordable set A_t → Select provider → Pay → Observe outcome → Update posteriors → Repeat
```

**Key constraints:**
- Can only select from affordable providers (price ≤ remaining wallet)
- Observe outcomes only for selected provider (chosen-only paid feedback)
- Provider reliability and prices may change without announcement
- Must run continuously without human resetting or retuning

### The 402Pilot Decision Layer Architecture

```
Upstream: Task request + candidate payment requirements Q_t
    ↓
Context Encoder → task context x_t
Wallet → affordable set A_t + wallet pressure λ_t
    ↓
Buyer Policy (PA-DCT) → select provider a_t
    ↓
Payment Substrate (x402/AP2/etc.) → execute transaction
    ↓
Outcome Scorer → realized utility u_t + charge c_t
    ↓
Wallet records c_t; Policy updates with (x_t, a_t, u_t, c_t)
```

### PA-DCT: Payment-Aware Discounted Contextual Thompson Sampling

**Three core mechanisms:**

1. **Discounted Utility and Cost Posteriors**
   - Maintains Bayesian posteriors over provider utility (Q-posterior) and cost (C-posterior) per provider-context pair
   - Common discount factor γ applies to all cells each round (forgets stale evidence)
   - Normal-Normal conjugate model with configurable priors

2. **Payment-Aware Selection Rule**
   - Thompson sample utility and cost from posteriors
   - Combine into payment-aware reward: `r̂ = (1 - λ_norm) × û - λ_norm × ĉ_normalized`
   - As wallet pressure increases, selection shifts from quality-focused to cost-focused
   - Select provider with highest sampled reward from affordable set

3. **Post-Payment Learning**
   - After transaction: observe realized utility (quality - failure penalty) and receipt cost
   - Update only the selected provider-context cell's posteriors
   - All cells discounted each round (non-stationary adaptation)

### Wallet Pressure Formula

```
λ_t = λ₀ × exp[α × (spending_deviation_from_plan)]

where spending_deviation = (cumulative_spent / B) / (t / T) - 1

λ_norm = λ_t / (1 + λ_t) ∈ (0, 1)
```

- Rises when spending runs ahead of plan
- Falls when spending runs behind
- Exponential form keeps pressure positive and smooth

### Key Hyperparameters

| Parameter | Value | Role |
|-----------|-------|------|
| γ (discount) | 0.999 | Effective memory ~1000 rounds; balances responsiveness with stability |
| ν (failure penalty) | 0.5 | Makes billed failures materially worse without overwhelming utility signal |
| c_max (cost normalizer) | $0.01 | Maps highest listed price to 1.0 |
| α (pressure sensitivity) | 2.0 | Controls how aggressively spending deviations increase pressure |
| λ₀ (baseline pressure) | 1.0 | Initial pressure when spending is on plan |

### Performance Evidence (402Pilot-Bench: 823 tasks, 5 providers, 3 scenarios, 30 seeds)

| Scenario | PA-DCT Quality | Budget Used | PA-gap/T | Best Baseline PA-gap/T |
|----------|---------------|-------------|----------|------------------------|
| S1 Stationary | 0.797 | 42% | 0.133 | 0.101 (Always-P-mid) |
| S2 Reliability shock | 0.761 | 43% | 0.166 | 0.164 (Always-P-cheap) |
| S3 Price shock | 0.831 | 39% | **0.121** | 0.195 (LinCBwK-Adapt) |

**Key finding:** PA-DCT maintains competitive quality while using only 39-43% of wallet, and achieves best non-oracle PA-gap/T in price-shock scenario. None of the baselines simultaneously maintains budget discipline AND adapts across reliability and price changes.

### Ablation: Component Roles

| Component Removed | Effect |
|-------------------|--------|
| Payment-aware ranking (-P) | Exhausts wallet in S1/S2; PA-gap/T jumps from 0.166 to 0.878 in S2 |
| Discounting (-D) | Slows S2 recovery by 53% (1,467→2,249 rounds) |
| Contextual bucketing (-C) | Delays S3 adaptation from 200 to 398 rounds |
| Thompson sampling (-TS) | Increases S1 PA-gap/T std from 0.004 to 0.046; delays S3 adaptation to 2,232 rounds |
| Learned realized costs (-C_post) | Eliminates price adaptation; P-premium selection drops from 66.1% to 3.6% |

### Decision Framework: When to Use PA-DCT vs Alternatives

| Situation | Recommended Policy | Why |
|-----------|-------------------|-----|
| Stable market, known good provider | Fixed-arm (Always-P-mid) | No exploration cost; best when market matches |
| Reliability shocks expected | PA-DCT | Discounting enables adaptation; payment-aware preserves solvency |
| Price changes expected | PA-DCT | Learned realized costs enable reallocation; best PA-gap/T |
| Strict budget, no adaptation needed | Contextual BTS | Preserves wallet but doesn't adapt to market changes |
| Quality maximization, unlimited budget | LinCBwK-Adapt | Higher quality but consumes 93-100% of wallet |
| Simple cost-aware routing | PM-Greedy | Uses listed prices; doesn't learn realized costs |

## References
- See [references/evidence-base.md](references/evidence-base.md) for full evidence: problem formulation, 402Pilot architecture, PA-DCT algorithm details, 402Pilot-Bench benchmark design, provider set, scenario design, complete results tables, ablation study, sensitivity analysis, theoretical analysis (regret bounds, adaptation rate), x402 integration witness, A-Tech applications.