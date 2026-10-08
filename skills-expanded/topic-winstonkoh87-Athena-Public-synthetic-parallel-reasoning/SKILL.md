---
name: synthetic-parallel-reasoning
description: Automates Protocol 75 v4.0, forcing 4 parallel external API calls (Domain Expert, Adversarial Skeptic, Cross-Domain Pattern Matcher, Zero-Point First Principles) with an Adversarial Convergence Gate. The 'Einstein Protocol' application.
argument-hint: "evaluate <complex-problem>"
allowed-tools:
  - Bash
  - Read
auto-invoke: false
model: default
context_trigger: "difficult problem, complex analysis, ultrathink, parallel reasoning, Einstein protocol, multi-perspective, deep evaluation"
---

# Parallel Synthetic Architect (Protocol 75 Engine v4.0)

Deploys true parallel reasoning via `parallel_orchestrator.py` to evaluate a strategic bottleneck. Refuses single-shot answers to complex problems.

## Triggers

"difficult problem", "what's the best strategy", "how should I handle this", "analyze this", `/ultrathink`

## Core Mechanics (v4.0)

1. **Phase 1 (Prime)**: Run semantic search, build internal CoT hypothesis, write context file.
2. **Phase 2 (Execute)**: Run `parallel_orchestrator.py` — this dispatches 4 parallel Gemini API calls:
   - Track A: Domain Expert (applies user's frameworks)
   - Track B: Adversarial Skeptic (attacks premises, checks Law #1)
   - Track C: Cross-Domain Pattern Matcher (finds isomorphic patterns)
   - Track D: Zero-Point First Principles (inversion, RETO lens)
3. **Phase 3 (Deposit)**: Read output, present synthesis, quicksave.

## Enforcement

> [!CAUTION]
> The script execution is **MANDATORY**. If the LLM writes a single-pass essay instead of running the script, it has violated this protocol. A single LLM checking its own homework hits a quality ceiling (Trilateral Feedback Loop principle).

## Execution

```bash
python3 .agent/scripts/parallel_orchestrator.py "<query>" \
  --context-file /tmp/ultrathink_context.md \
  --output .context/state/ultrathink/ultrathink_$(date +%Y%m%d_%H%M%S).md
```

## Reference Paths

- `.agent/workflows/ultrathink.md` (v4.0)
- `.agent/scripts/parallel_orchestrator.py` (v4.0)
- `Athena-Public/examples/protocols/decision/75-synthetic-parallel-reasoning.md`
