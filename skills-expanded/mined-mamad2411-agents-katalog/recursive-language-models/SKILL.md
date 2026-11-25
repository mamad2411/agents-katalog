---
name: recursive-language-models
description: Apply Recursive Language Models (RLMs) — models that treat long prompts as external environments they can programmatically examine, decompose, and recursively call themselves over — to break context window limits without hitting context rot. Covers the MIT RLM-Qwen3-8B breakthrough (28.3% average improvement over base model, approaches GPT-5 quality on three tasks despite being 50x smaller), the recursive decomposition pattern, context navigation vs. context dumping, and the practical architecture for agents that process entire codebases or long documents. Use when building agents that must process inputs exceeding context windows, analyzing entire codebases, reasoning over long legal/research documents, or decomposing multi-stage problems recursively. NOT for standard short-context tasks where conventional models suffice.
---

# Recursive Language Models

## Overview

The biggest constraint in building agents has been context windows. Even with million-token limits, models suffer from "lost in the middle" — information buried mid-context gets ignored, and performance degrades as context grows (Databricks: correctness drops around 32K tokens). Recursive Language Models (RLMs) solve this by treating long prompts as external environments that models can programmatically examine, decompose, and recursively call themselves over.

The breakthrough: MIT researchers built RLM-Qwen3-8B, the first natively recursive language model, which outperforms the underlying Qwen3-8B by 28.3% on average across long-context tasks. Even more striking: it approaches GPT-5 quality on three tasks despite being 50x smaller.

## When to Use

- Building agents that process entire codebases (thousands of files, dependency analysis)
- Long-document reasoning (legal contracts, research papers, technical specifications)
- Multi-stage problem decomposition where each stage requires deep reasoning
- Tasks where context exceeds the model's window and naive chunking loses cross-section connections
- When you need a smaller model to perform like a frontier model on long-context tasks

**NOT for:**
- Standard short-context tasks (use conventional models directly)
- Tasks where the entire input fits comfortably in context (<32K tokens)
- Real-time latency-sensitive applications (recursion adds round-trips)

## The Core Problem RLMs Solve

### The Context Window Trap

| Approach | Problem |
|----------|---------|
| Bigger context windows | Context rot: performance degrades as context grows, even on simple tasks |
| Naive chunking | Loses cross-section connections; can't reference findings from chunk A while processing chunk B |
| Retrieval-augmented generation | Only retrieves what the embedding model matches; misses structural relationships |
| Million-token dumping | "Lost in the middle": mid-context information ignored regardless of relevance |

### The RLM Solution

Instead of processing the entire prompt at once, RLMs:
1. **Break** the long input into snippets
2. **Process** each piece recursively — the model calls itself like a function
3. **Navigate** to relevant information as needed (active, not passive)
4. **Synthesize** findings across recursive calls

This enables processing inputs up to **two orders of magnitude beyond context windows** — without the context rot issues that plague traditional long-context models.

## The Recursive Decomposition Pattern

```
RLM.process(input: str, depth: int = 0) -> str:
    if fits_in_context(input):
        return base_model.generate(input)
    
    snippets = decompose(input)
    partial_results = []
    
    for snippet in snippets:
        if needs_deeper_analysis(snippet):
            # Recursive call — the model calls itself
            result = RLM.process(snippet, depth + 1)
        else:
            result = base_model.generate(snippet)
        partial_results.append(result)
    
    return synthesize(partial_results, context=input)
```

**Key difference from naive chunking:** The model can navigate back to the original input during synthesis. It examines different parts as needed, more like how humans work through complex documents — reading the summary, jumping to a relevant section, cross-referencing, then building a conclusion.

## RLM-Qwen3-8B Performance Data

| Metric | Result |
|--------|--------|
| Average improvement over base Qwen3-8B | +28.3% across long-context tasks |
| vs. GPT-5 quality on 3 tasks | Approaches parity despite being 50x smaller |
| Short-prompt performance | Dramatically outperforms vanilla frontier models at comparable cost |
| Context handling | Active navigation, not passive dumping |
| "Lost in the middle" | Eliminated — RLMs navigate to relevant information |

### What This Enables

| Use Case | Conventional Limit | RLM Capability |
|----------|--------------------|----|
| Entire codebase analysis | Can't fit in context; naive chunking misses dependencies | Systematic analysis of dependencies across thousands of files |
| Long-document reasoning | Legal contracts, research papers exceed limits | Recursive processing with cross-reference synthesis |
| Multi-stage problem decomposition | Single-pass reasoning degrades on complex problems | Recursive sub-problem decomposition |
| Context utilization | Passive — middle context ignored | Active — model navigates to relevant sections |

## The Context Navigation vs. Context Dumping Distinction

| Dimension | Context Dumping (Traditional) | Context Navigation (RLM) |
|-----------|-------------------------------|--------------------------|
| Strategy | Load everything, hope the model finds it | Model actively decides what to examine |
| Efficiency | Low — pays attention to everything equally | High — focuses compute on relevant sections |
| Cross-references | Lost when chunked | Preserved through recursive synthesis |
| Context rot | Sets in as context grows | Avoided — each recursive call has focused context |
| Scalability | Limited by window size | Scales two orders of magnitude beyond window |

## Practical Architecture for Agent Systems

### Pattern 1: Codebase Analysis Agent

```
Task: "Analyze the authentication flow across this 12M-line codebase"

RLM Execution:
├── Decompose codebase into module groups
│   ├── Group A: auth/ directory
│   ├── Group B: middleware/ directory  
│   └── Group C: API routes
├── For each group (recursive):
│   ├── Decompose into files
│   │   ├── For each file (recursive):
│   │   │   ├── Extract auth-related functions
│   │   │   └── Map function call graph
│   │   └── Synthesize module-level flow
│   └── Map inter-module dependencies
└── Final synthesis: Complete auth flow with dependency map
```

### Pattern 2: Long-Document Reasoning Agent

```
Task: "Review this 500-page legal contract for risk clauses"

RLM Execution:
├── Decompose contract into sections
├── For each section (recursive):
│   ├── Extract obligations, conditions, termination triggers
│   ├── Cross-reference with definitions section (navigate back)
│   └── Flag risk-level per clause
├── Synthesize risk profile
└── Generate human-readable summary with clause references
```

### Pattern 3: Multi-Stage Problem Solver

```
Task: "Design a data pipeline architecture for this enterprise"

RLM Execution:
├── Stage 1: Gather requirements (recursive analysis of spec doc)
├── Stage 2: Research patterns (recursive analysis of architecture docs)
├── Stage 3: Design (synthesis with cross-references to stages 1-2)
├── Stage 4: Validate (recursive check against requirements)
└── Stage 5: Document (synthesize all stages)
```

## Connection to Context Engineering

RLMs are the architectural solution to the context failures documented in the `context-engineering` skill:

| Context Failure | How RLMs Address It |
|-----------------|---------------------|
| Poisoning | Each recursive call validates its input; hallucinations don't propagate across calls |
| Distraction | Focused context per call — model isn't trapped in its own history |
| Confusion | Only relevant snippets loaded per recursive call |
| Clash | Contradictions surfaced during synthesis; model can rank sources by examining each independently |
| Lost in the middle | Eliminated — active navigation replaces passive dumping |

## Privacy-First Advantage

RLMs have a natural privacy advantage for A-Tech's values:

- **Local processing:** Recursive calls can run on local SLMs, keeping data on-device
- **No data exfiltration:** Codebases and documents processed locally, not shipped to cloud APIs
- **Selective cloud escalation:** Only the synthesis step (which needs frontier reasoning) might use cloud models, and even then, only summaries are sent

```
Local SLM (recursive decomposition + per-snippet processing)
    ↓ summaries only
Cloud frontier model (final synthesis)
    ↓ result
Local display
```

This means the vast majority of sensitive data never leaves the user's machine.

## A-Tech Applications

### A-Coder (IDE)
- **Whole-codebase understanding:** RLM-powered agent that can analyze the entire project for refactoring, dependency mapping, and architecture review without shipping the codebase to a cloud API
- **Context-aware completions:** Recursive analysis of relevant files provides deeper context than simple retrieval
- **Local-first RLM:** Run RLM-Qwen3-8B locally for privacy-preserving codebase analysis

### Be Practical (Playbooks)
- **"Recursive Reasoning for Agent Builders" playbook:** Teaching module on RLM architecture, when to use recursion vs. conventional models, and implementation patterns
- **Long-document processing templates:** Pre-built recursive decomposition patterns for contracts, research papers, technical specs

### Builder's Club
- **Open-source RLM toolkit:** Community-maintained recursive decomposition library
- **RLM benchmark suite:** Community benchmarks comparing RLM implementations across model sizes and task types
- **Recursive pattern library:** Open-source decomposition templates for common agent workflows

## When to Choose RLM vs. Conventional Models

| Condition | Recommendation |
|-----------|---------------|
| Input fits in <32K tokens | Conventional model — RLM overhead not justified |
| Input is 32K–200K tokens | Consider RLM if cross-referencing is critical |
| Input exceeds 200K tokens | RLM — conventional models degrade regardless of window size |
| Latency is critical | Conventional — RLM adds recursive round-trips |
| Accuracy on long context is critical | RLM — 28.3% average improvement |
| Privacy requires local processing | RLM with local SLM — most processing stays on-device |
| Cost is critical | RLM with SLM — approaches frontier quality at 50x lower cost |

## Measurement Framework

| Metric | Target | Measurement |
|--------|--------|-------------|
| Long-context task accuracy | ≥ frontier model baseline | Controlled test on standard long-context benchmarks |
| Recursive depth efficiency | ≤3 levels for typical tasks | Depth tracking per task |
| Token cost vs. frontier | <20% of equivalent frontier model | Cost comparison per task |
| Cross-reference accuracy | ≥90% of references correctly linked | Reference validation |
| Local processing percentage | >90% of tokens processed locally | Token routing audit |
| Context rot incidents | 0 (by design) | Quality at maximum input size |

## Cross-References

- `context-engineering` — The four context failures that RLMs architecturally solve
- `agentic-coding-trends-2026` — Context engineering as a core skill shift; context rot data
- `slm-enterprise-deployment` — SLM architecture that RLMs build on for local-first processing
- `harness-engineering-ai-agents-2026` — Agent harness architecture for long-context tasks
- `verifiability-driven-automation` — RLMs improve verifiability by decomposing into checkable sub-tasks
- `ai-agent-finfops-cost-optimization` — RLMs as a cost optimization strategy (50x smaller model, frontier quality)

## Sources

- MIT — RLM-Qwen3-8B: First natively recursive language model, +28.3% over base Qwen3-8B on long-context tasks, approaches GPT-5 on 3 tasks at 50x smaller
- Firecrawl — "Top 13 Agentic AI Trends to Watch in 2026" (June 2026): RLMs as trend #10, breaking context limits, recursive decomposition pattern, context navigation vs. context dumping
- Databricks — "Context Rot in Long-Context Models" (2026): Performance degradation at 32K tokens — the problem RLMs solve
- See [references/rlm-architecture-patterns.md](references/rlm-architecture-patterns.md) for detailed implementation templates.