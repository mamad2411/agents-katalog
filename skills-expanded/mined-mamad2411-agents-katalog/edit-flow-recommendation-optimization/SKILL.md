---
name: Edit Flow Recommendation Optimization
description: Applies the EditFlow framework for flow-aligned code edit recommendations that preserve developer mental flow continuity. Use when designing or optimizing AI code editing assistants, benchmarking edit recommendation systems, or evaluating flow-awareness in coding tools. NOT for one-shot code generation (different interaction pattern).
---

# Edit Flow Recommendation Optimization

## Overview

Based on Liu et al. (OOPSLA, April 2026). First framework for benchmarking and optimizing code edit recommendation systems from the perspective of developers' mental flow.

## Key Finding

**68.81% of model recommendations disrupt developers' ongoing mental flow**, including 8.83% that are technically correct but ill-timed. EditFlow reduces flow violations by 75% and improves recommendation precision by 66.99%.

## Flow Categories

| Category | Definition | Impact |
|----------|------------|--------|
| **Keep** | Follows an edge in the mental flow graph | Flow-preserving |
| **Jump** | Valid edit but skips intermediate steps | Flow-breaking |
| **Revert** | Suggests discarding an applied change | Flow-breaking |
| **Break** | Hallucinates content not in ground truth | Flow-breaking |

## Edit Order Recovery

### Pairwise Edit Order Labels
$$L = \{\prec, \succ, \sim, \bot\}$$

- $\prec$: After completing $h_i$, developer can naturally infer $h_j$
- $\succ$: Reverse of $\prec$
- $\sim$: Either direction preserves flow (symmetric)
- $\bot$: No cognitive connection

### Auto-Tuned Prompt Performance
| Method | Accuracy (%) |
|--------|-------------|
| Zero-shot | 50.63 |
| Few-shot | 47.42 |
| Hand-crafted | 53.27 |
| DSPy | 53.39 |
| **Auto-tuned** | **87.26** |

**63.81% relative improvement** over best baseline.

## EditFlow Pipeline

1. **Edit order recovery** — auto-tuned prompt infers pairwise cognitive order
2. **Digital twin** — simulates editing trajectories guided by recovered flow
3. **Flow-aware optimization** — filters and re-ranks recommendations:
   - Predict order label via LLM: $\text{LLM}(h_i, h_j, \pi^*)$
   - Retain only $\prec$ or $\sim$ (flow-keeping)
   - Defer $\succ$ or $\bot$ (flow-breaking)
   - Re-rank by average log probability

## Resource Overhead
- **Latency:** +1.71 seconds per query
- **Tokens:** +6.58k tokens per query
- **Cost:** +$0.03 per query
- **Trade-off:** 66.99% precision improvement for <2s latency cost

## User Study Results (N=32)

| Task | Without EditFlow | With EditFlow | Improvement |
|------|-----------------|-------------|-------------|
| Task 1 (easy) | 7.51 min | 6.88 min | 8.4% |
| Task 2 (hard) | 12.41 min | 8.00 min | **35.5%** |
| Task 3 (refactor) | 4.14 min | 3.53 min | 14.7% |

**Hard tasks benefit most** — EditFlow prevents flow-violating recommendations on complex, multi-file edits.

## A-Tech Applications

### For A-Coder
- **Flow-aware edit recommendations** — filter agent suggestions by mental flow continuity
- **Edit order recovery** — reconstruct developer's cognitive editing sequence
- **Digital twin evaluation** — simulate editing trajectories for A-Coder benchmarking

### For Be Practical
- **Flow theory in practice** — mental flow as measurable developer productivity construct
- **EditFlow curriculum** — teaching flow-aware AI tool usage
- **User study methodology** — controlled task evaluation with flow metrics

### For Builder's Club
- **Flow-aware tool design** — EditFlow as open-source contribution
- **Digital twin framework** — reproducible evaluation for AI coding tools
- **Mental flow metrics** — quantifying cognitive continuity

## Cross-References
- `agentic-flow-aligned-edit-recommendation` — prior flow work (builds on this)
- `vibe-coding-phenomenological-flow` — phenomenological analysis
- `developer-ai-cognitive-engagement-decline` — engagement decline pattern
- `developer-ai-ambidexterity-shift` — ambidexterity framework

## Source
Liu, C., Lin, Y., Chang, J., Liu, J., Qi, B., Jiang, B., Huang, Z. & Dong, J.S. (OOPSLA, April 2026). "EditFlow: Benchmarking and Optimizing Code Edit Recommendation Systems via Reconstruction of Developer Flows."
