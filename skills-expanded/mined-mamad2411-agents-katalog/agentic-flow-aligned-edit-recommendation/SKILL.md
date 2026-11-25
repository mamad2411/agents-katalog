---
name: agentic-flow-aligned-edit-recommendation
description: Framework for evaluating and optimizing AI code-edit recommendation systems to preserve developer mental flow rather than disrupt it. Use when designing or evaluating AI coding assistants (Cursor, Claude Code, CoEdPilot), benchmarking edit recommendation quality beyond accuracy, or building flow-aware post-processing wrappers for existing assistants. NOT for single-shot code completion, or for evaluating assistants where flow continuity is irrelevant.
---

# Agentic Flow-Aligned Edit Recommendation

## Overview
EditFlow (Liu et al., 2026, OOPSLA) is the first framework for benchmarking and optimizing code-edit recommendation systems from the perspective of developer mental flow. It reveals that 68.81% of model recommendations from Cursor and Claude Code disrupt developers' ongoing mental flow — including 8.83% of suggestions that are technically correct but ill-timed. A flow-aware post-processing wrapper reduces flow violations by over 75% and improves task completion speed by 25.11%.

## When to Use
- Designing or evaluating AI coding assistants (Cursor, Claude Code, Copilot, CoEdPilot)
- Benchmarking edit recommendation quality beyond code-accuracy metrics
- Building flow-aware post-processing wrappers for existing assistants
- Diagnosing why a high-accuracy assistant still reduces developer productivity
- Designing multi-file edit recommendation systems where temporal ordering matters
- NOT for single-shot code completion (no flow dimension)
- NOT for evaluating assistants where flow continuity is irrelevant

## Core Process / Workflow

### 1. Flow-Aware Evaluation Taxonomy
Classify every predicted edit recommendation into one of four mutually exclusive categories:

| Category | Definition | Impact on Flow |
|---|---|---|
| **Keep** | Valid edit that is a one-hop successor of completed edits in the mental flow graph | Preserves flow continuity |
| **Jump** | Valid edit but skips intermediate logical steps (not a one-hop successor) | Disrupts flow — cognitive gap |
| **Revert** | Suggests discarding an already-applied change | Creates cognitive dissonance |
| **Break** | Hallucinated content not present in the ground-truth commit | Breaks flow entirely |

**Key finding:** In Cursor and Claude Code, the majority of recommendations are Break (51–55%), not Keep (28–34%).

### 2. Mental Flow Graph Construction
1. Extract edit hunks from a commit (each hunk = file path + line range + pre/post content)
2. Annotate pairwise order relations between hunks: `≺` (h_a naturally precedes h_b), `≻` (reverse), `∼` (either order preserves flow), `⊥` (no cognitive connection)
3. Build a directed mental flow graph where edges represent cognitive continuity
4. One-hop successors of completed edits = valid next steps that preserve flow

### 3. Prompt Auto-Tuning for Edit Order Recovery
EditFlow learns an optimized prompt that infers pairwise cognitive order between edits:
- Auto-tuned prompt achieves 87.26% accuracy (vs 50–53% for zero/few-shot/hand-crafted baselines)
- 63.81% relative improvement over the best baseline
- On real-world industrial data (500 commits, 3,059 hunks): only 30 violations vs 121 for hand-crafted baseline (75%+ reduction)

### 4. Flow-Aware Post-Processing (EditFlow Wrapper)
EditFlow wraps existing recommendation systems (Cursor, Claude Code, CoEdPilot):
1. Query the recommendation system for candidate edits
2. Infer pairwise order label between each candidate and the last completed edit via the auto-tuned prompt
3. Keep only candidates with `≺` or `∼` relations (flow-continuous)
4. Defer `≻` and `⊥` candidates for future iterations (not discarded permanently)
5. Re-rank remaining candidates by average log probability of the order label

### 5. Measured Impact

| Metric | Cursor (Original) | Cursor (w/ EditFlow) | Claude Code (Original) | Claude Code (w/ EditFlow) |
|---|---|---|---|---|
| Keep (%) | 24.00 | 38.49 | 30.76 | 46.89 |
| Break (%) | 60.15 | 51.13 | 53.49 | 45.52 |
| Precision (%) | 33.02 | 42.42 | 40.54 | 50.45 |
| F0.5 | 34.22 | 41.45 | 40.32 | 46.75 |

- **66.99% average precision improvement** across systems
- **25.11% faster task completion** in controlled user study (32 participants, 3 tasks)
- **87.42% average boost** to flow-keeping edits
- **22.42% average drop** in flow-breaking edits
- Additional overhead: 1.71s latency, 6.58K tokens, $0.03/query (below the ~2s flow-disruption threshold)

### 6. Known Failure Modes
1. **False rejection (1-context sensitivity):** EditFlow evaluates flow only against the most recent edit; a valid edit with flow continuity to an earlier edit may be incorrectly rejected
2. **False acceptance (intent ambiguity):** A locally coherent but globally incorrect edit (e.g., deleting instead of renaming) may be accepted because the local flow is continuous

## References
- See [references/editflow-evidence-base.md](references/editflow-evidence-base.md) for the full evidence base, including the digital twin evaluation framework, the user study design, and the failure analysis.