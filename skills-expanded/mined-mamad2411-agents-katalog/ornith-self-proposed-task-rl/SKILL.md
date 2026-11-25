---
name: ornith-self-proposed-task-rl
description: Applies Ornith-1.5's self-proposed task reinforcement learning method — where the model generates its own training tasks (scaffold + solution rollouts) rather than relying on human-written tasks — to design scalable post-training pipelines. Use when designing RL post-training for coding/agentic models, addressing environment-scaling bottlenecks, or evaluating the tradeoff between self-generated and human-curated training environments.
---

# Ornith Self-Proposed Task Reinforcement Learning

## Overview
Ornith-1.5 (DeepReinforce, August 2026) introduces a post-training method where the model proposes its own training tasks, builds a scaffold for each, and generates the solution rollouts that become the RL signal — eliminating the human-written task bottleneck that limits how far RL post-training can scale.

## When to Use
- Designing RL post-training pipelines for coding or agentic models
- Hitting the environment-scaling bottleneck (not enough human-written task environments)
- Evaluating whether self-generated training tasks can replace curated environments
- Building synthetic task-generation pipelines for RL reward signals
- Comparing self-proposed-task RL vs human-curated RL approaches
- NOT for supervised fine-tuning (SFT) — this is specifically an RL post-training method
- NOT for models without strong base capabilities (self-proposed tasks require the model to already generate plausible task structures)

## Core Process / Workflow

### 1. The Core Insight: Environment Scaling, Not Model Scaling

The dominant 2026 pattern for post-training (GLM-5.3, Qwen3.8, Kimi K3) is scaling RL on long-horizon task environments. But the bottleneck is not compute — it is the **number and quality of task environments**.

> "As agent capability improves, much of the difficulty in scaling post-training moves from the model to the environment. A useful task environment has to be executable, verifiable, and close to real professional work — and we need many of them, not a handful of hand-built ones."

Ornith's solution: let the model generate its own environments.

### 2. The Self-Proposed Task RL Pipeline

```
┌─────────────────────────────────────────────────────┐
│  1. Model PROPOSES a task                           │
│     (drawn from learned task distribution)          │
├─────────────────────────────────────────────────────┤
│  2. Model BUILDS a scaffold for the task            │
│     (runnable environment, dependencies, test setup) │
├─────────────────────────────────────────────────────┤
│  3. Model GENERATES solution rollouts               │
│     (attempt to solve its own task)                 │
├─────────────────────────────────────────────────────┤
│  4. Task reward = validity × novelty × difficulty   │
│     - validity: is the task solvable?               │
│     - novelty: is it different from prior tasks?     │
│     - difficulty: targets 0.2 success rate          │
├─────────────────────────────────────────────────────┤
│  5. RL signal from solution rollouts                │
│     (reward from successful completions)            │
└─────────────────────────────────────────────────────┘
```

### 3. The Reward Decomposition

The task reward multiplies three components:

```python
task_reward = validity_score * novelty_score * difficulty_score

# validity: Is the task actually solvable?
#   - A judge agent attempts the task to verify solvability
#   - Verifiers synthesized WITHOUT access to the reference solution
#   - Must pass oracle, no-op, and unsolved-state checks

# novelty: Is this task different from previously generated tasks?
#   - Prevents the model from repeatedly proposing the same easy task
#   - Measured against the growing task distribution

# difficulty: Is this task at the right challenge level?
#   - Targets a 0.2 success rate (80% failure = optimal challenge)
#   - Too easy (high success) = low learning signal
#   - Too hard (0% success) = no successful rollouts to learn from
```

### 4. Why 0.2 Success Rate?

The 0.2 target is not arbitrary. At 20% success:
- Enough rollouts succeed to provide a positive RL signal (1 in 5)
- The task is hard enough that the model must actually improve to solve it
- The reward gradient is steep — small improvements yield large reward changes
- This mirrors the curriculum-learning principle of "desirable difficulty"

### 5. Reward Hacking Defense

Ornith explicitly carries reward-hacking defense into task generation:
- **Verifiers are synthesized without access to the reference solution** — prevents the verifier from being gamed
- **Solver trajectories are used to discover and close reward shortcuts** — if a solver finds a shortcut, the task is patched
- **Three check types:** oracle (does the correct solution pass?), no-op (does doing nothing incorrectly pass?), unsolved-state (does an unsolved state incorrectly pass?)
- A verifier that passes all three checks produces a binary reward reliable enough to train on directly

### 6. Ornith-1.5 Benchmark Evidence

| Benchmark | Ornith-1.5 397B | Claude Opus 4.8 | Kimi K3 |
|-----------|-----------------|-----------------|---------|
| Terminal-Bench 2.1 | 86.1 | 85.0 | 88.3 |
| SWE-bench Verified | 86.0 | — | — |
| GPQA Diamond | 92.8 | — | — |
| BrowseComp | 86.6 | — | — |
| Context window | 262,144 (→1M YaRN) | — | — |
| License | MIT (all sizes) | Proprietary | Open-weight |

**Key caveat:** Ornith-1.5 leads on Terminal-Bench and SWE-bench but trails on harder agentic rows (Frontier-Bench v0.1: 13.5 vs Opus 21.1; NL2Repo: 59.5 vs 69.7). A model trained on tasks it wrote itself has an obvious failure mode: it optimizes for the kind of task it can solve, not the kind of task that matters. The gap on Frontier-Bench and NL2Repo reflects this.

### 7. Self-Proposed vs Human-Curated Task Tradeoffs

| Dimension | Human-Curated Tasks | Self-Proposed Tasks (Ornith) |
|-----------|-------------------|------------------------------|
| Scalability | Limited by human effort | Scales with compute |
| Task diversity | Bounded by human imagination | Can discover novel task patterns |
| Quality control | High (human-reviewed) | Requires automated verification |
| Reward hacking risk | Lower (human-designed) | Higher (model may propose easy tasks) |
| Coverage of edge cases | Low (humans miss edge cases) | Higher (can probe failure modes) |
| Alignment with real work | High (humans design realistic tasks) | Uncertain (model may optimize for solvability) |
| Compute cost per task | High (human time) | Low (inference cost) |
| Difficulty calibration | Manual | Automated (0.2 success target) |

### 8. Implementation Checklist

```markdown
## Self-Proposed Task RL Pipeline

1. [ ] Base model: Start with a capable base/post-trained model
2. [ ] Task proposer: Fine-tune or prompt the model to propose tasks
3. [ ] Scaffold builder: Generate runnable environments for proposed tasks
4. [ ] Verifier synthesis: Generate verifiers WITHOUT reference solutions
5. [ ] Three-check validation: oracle / no-op / unsolved-state
6. [ ] Difficulty targeting: Filter to ~0.2 success rate tasks
7. [ ] Novelty scoring: Compare against prior task distribution
8. [ ] Solution rollouts: Generate multiple attempts per task
9. [ ] RL training: Use binary reward from validated verifiers
10. [ ] Iterate: Expand task distribution; close discovered shortcuts
```

## References
- See [references/ornith-evidence-base.md](references/ornith-evidence-base.md) for full evidence: Ornith-1.5 architecture and training method, benchmark tables, reward decomposition analysis, reward-hacking defense mechanisms, comparison with GLM-5.3 environment-scaling approach, and the self-proposed-task failure mode analysis.