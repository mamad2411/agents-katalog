---
name: verification-load-interface-design
description: How the AI coding assistant interface (Inline, Chat, or Structured prompting) shapes verification load and fatigue, independent of the underlying model. Based on the ACM 2026 controlled study (N=60, single LLM fixed across conditions) isolating interface effects on verification burden. Covers the interface-dependent fatigue hypothesis, the experimental design that controls for model quality, and design implications for AI coding tools. Use when choosing or designing AI coding assistant interfaces, evaluating why one interface produces more fatigue than another, or researching interface-level fatigue determinants. NOT for general review fatigue mitigation (use ai-review-fatigue-mitigation) or the decision-density crisis (use coding-agent-decision-fatigue-mitigation).
---

# Verification Load Interface Design

## Overview
Not all AI coding fatigue comes from the model — some comes from the interface. A 2026 controlled study fixed a single LLM and varied only the interaction mode (Inline, Chat, Structured, or no-AI control) across 60 participants solving three Python tasks, isolating the interface's effect on verification load and fatigue. The interface you choose shapes how tired your users get.

## When to Use
- Choosing between AI coding assistant interfaces (inline completion, chat, structured prompting)
- Designing a new AI coding tool and deciding on the interaction paradigm
- Evaluating why one AI coding interface produces more user fatigue than another despite similar model quality
- Researching interface-level (not model-level) determinants of AI fatigue
- NOT for general review fatigue mitigation practices (use `ai-review-fatigue-mitigation`)
- NOT for the decision-density crisis in agentic coding (use `coding-agent-decision-fatigue-mitigation`)
- NOT for measuring AI fatigue across products (use `ai-fatigue-scale-design`)

## Core Process / Workflow

### 1. Understand the core question

Does the interface through which you interact with an AI coding assistant change how much verification load and fatigue you experience — independent of the model's quality?

This matters because most fatigue research varies the model or the task. This study holds both fixed and varies only the interface.

### 2. The experimental design

| Element | Detail |
|---|---|
| Participants | N = 60 |
| Tasks | 3 Python programming tasks |
| Conditions | Inline prompting, Chat prompting, Structured prompting, No-AI control |
| Model | Single LLM held fixed across all AI conditions |
| Isolation | Only the interface varies — model quality, task difficulty, and participant pool are controlled |
| Measures | Verification load, fatigue, task outcomes |

### 3. The interface conditions

| Interface | How it works | Verification implication |
|---|---|---|
| **Inline** | AI suggests code directly in the editor at the cursor | Verification happens inline, interleaved with writing; lower context switch but constant micro-interruptions |
| **Chat** | AI interaction happens in a separate chat panel | Verification requires switching between chat and code; higher context switch but more deliberate review |
| **Structured** | AI interaction follows a structured prompting protocol | Verification is guided by the structure; potentially lower cognitive load but more setup overhead |
| **No-AI control** | Participants solve tasks without AI assistance | Baseline for comparison — establishes the non-AI verification load |

### 4. Why interface matters for fatigue

The interface determines:
- **Where verification happens** (inline vs. separate panel)
- **When verification happens** (interleaved vs. batched)
- **How much context switching is required** (none vs. high)
- **How visible the AI's reasoning is** (implicit vs. explicit)
- **How much effort is required to request and evaluate output**

These are interface design choices, not model quality issues. Two tools using the same model can produce different fatigue levels depending on interface design.

### 5. Design implications

**For interface designers:**
- Measure verification load per interface, not just per model
- The interface is a fatigue determinant independent of model quality
- Inline suggestions minimize context switching but maximize micro-interruption frequency
- Chat interfaces maximize deliberate review but maximize context switching
- Structured prompting may reduce cognitive load but adds setup overhead
- The optimal interface depends on task type and user expertise

**For product teams choosing interfaces:**
- Don't assume "same model = same fatigue" — the interface is a variable
- A/B test interfaces on fatigue metrics, not just on task completion
- Consider hybrid interfaces that adapt to task context

### 6. The verification-load measurement approach

| Metric | What it captures |
|---|---|
| Time spent verifying vs. writing | The verification burden ratio |
| Number of verification actions per task | The verification frequency |
| Self-reported fatigue (post-task) | The subjective strain |
| Error detection rate | The verification effectiveness |
| Context switches per task | The switching cost |

### 7. Connection to the review fatigue framework

This study provides the **interface-level evidence** that complements the `ai-review-fatigue-mitigation` skill's human-factors framework:

- `ai-review-fatigue-mitigation` explains **why** review fatigue happens (vigilance decrement + automation complacency + context switching)
- This skill explains **how the interface modulates** that fatigue — the same mechanisms, but triggered differently by Inline vs. Chat vs. Structured interaction

## A-Tech Applications

| Product | Application |
|---|---|
| **A-Coder** | A/B test interface modes on fatigue metrics; default to the interface that minimizes verification load for the task type; allow users to switch modes based on their fatigue state |
| **Be Practical** | Module on "Choosing Your AI Interface" — teach learners that the interface is a fatigue variable, not just a preference; include the study design as a research-literacy example |
| **Builder's Club** | Open-source a verification-load measurement MCP tool; publish interface fatigue benchmarks as a community resource |

## References
- See [references/verification-load-study-evidence.md](references/verification-load-study-evidence.md) for the study details and cross-references.