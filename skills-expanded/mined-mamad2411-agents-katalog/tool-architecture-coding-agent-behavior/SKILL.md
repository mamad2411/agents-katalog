---
name: tool-architecture-coding-agent-behavior
description: Design coding agent tool interfaces that improve consistency, exploration, and efficiency by varying abstraction level and cognitive scaffolding rather than capability. Use when building coding agent tools, improving agent reliability, reducing token costs, or deciding between bash, atomic, semantic search, or code-execution interfaces.
---

# Tool Architecture Shapes Coding Agent Behavior

## Overview

When coding agents have similar underlying capabilities, how those capabilities are organized and exposed to the model (tool architecture) meaningfully changes agent behavior. Structured low-level interfaces improve consistency by up to 4.7x, natural-language search broadens repository exploration by 11%+, and code-execution interfaces achieve similar task performance with 41.6% fewer steps and 56.3% lower token usage. Lightweight text-based cognitive scaffolding has limited effect.

## When to Use

- Building or refining coding agent tool interfaces (bash, atomic tools, semantic search, code execution)
- Improving agent consistency across repeated attempts (pass^k)
- Reducing token cost and step count without sacrificing task performance
- Broadening repository exploration coverage in codebase navigation
- Deciding whether cognitive scaffolding tools (scratchpad, hypothesis tracking) are worth adding
- NOT for: single-shot code generation, non-agentic workflows, or when capability itself is the bottleneck

## Core Process / Workflow

### 1. Assess Your Current Tool Architecture

Identify which of six architectures your agent uses:
- **BashOnly**: General-purpose shell only (baseline)
- **Atomic**: Structured low-level operations (search, view, str_replace, create, bash)
- **NLSearch**: Natural-language search interface (sub-agent or embedding-based)
- **Python**: Code-execution blocks instead of individual tool calls
- **HypoTrack**: Hypothesis recording and tracking tool
- **Scratchpad**: Free-form intermediate reasoning tool

### 2. Apply the Four Findings

**Finding 1 — Atomic improves consistency (pass^k)**
- Atomic is the only setup that improves consistency for ALL actors (weakest to strongest)
- Largest gains for weakest actors (Qwen3Coder-30B: +0.059-0.074 pass^k)
- Mechanism: reduces low-level environment-interaction errors (mis-edit, wrong-syntax)
- Action: package recurring low-level actions into explicit, constrained primitives

**Finding 2 — NLSearch improves exploration**
- NLSearch consistently broadens repository coverage (+11%+ read diversity across actors)
- More diverse early search queries (Jaccard 0.85 vs 0.69, Levenshtein 0.58 vs 0.49)
- Improves recall of relevant files (+4.6% to +6.4%) but with lower precision
- Action: add a natural-language search interface alongside grep/find

**Finding 3 — Python/code-execution improves efficiency**
- Similar task performance with 41.6% fewer steps, 56.3% lower token cost
- Main gain from step reduction (77→46, 65→47, 80→55 across actors)
- Compound interaction: agent bundles multiple operations in a single block
- Action: expose a code-execution interface for complex multi-step workflows

**Finding 4 — Lightweight cognitive scaffolding has limited effect**
- Scratchpad: entries closely match reasoning already present in baseline (high BLEU)
- HypoTrack: rarely induces genuine multi-branch reasoning (mostly single-hypothesis)
- Action: do not rely on text-only scaffolding to change reasoning behavior; add retrieval, memory, or policy enforcement instead

### 3. Decision Framework

| Goal | Recommended Architecture | Trade-off |
|------|-------------------------|----------|
| Maximize consistency | Atomic | More turns for strong actors |
| Broaden exploration | NLSearch | Lower precision, more noise |
| Minimize cost/steps | Python code execution | Requires sandbox security |
| Weakest actors (small models) | Atomic + Python | Largest combined gains |
| Cognitive scaffolding | Skip lightweight text tools | Add retrieval or policy instead |

### 4. Capability-Matched Evaluation

When evaluating tool architecture changes:
- Hold underlying capability constant (same model, same information access)
- Measure pass^k (consistency), read diversity (Jaccard), solution diversity (CodeBLEU), and efficiency (tokens, steps)
- Run 10+ rollouts per instance to measure consistency reliably
- Validate findings on at least two task types (issue fixing, feature implementation, debugging)

## References

- See [references/evidence-base.md](references/evidence-base.md) for full statistical results, experimental design, and per-actor breakdowns.