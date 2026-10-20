---
name: dikw-agentic-behavioral-experiment-learning
description: Applies a tool-augmented, multi-agent DIKW (Data-Information-Knowledge-Wisdom) architecture to transform one-shot behavioral experiments into cumulative knowledge systems that learn from prior experimental data and generate superior interventions. Use when designing behavioral messaging at scale, building agentic A/B-test learning loops, extracting reusable design principles from megastudy data, or evaluating whether LLM reasoning alone (without experimental data) can predict intervention effectiveness. NOT for single-shot message optimization or when no prior experimental data exists.
---

# DIKW Agentic Behavioral Experiment Learning

## Overview

Tool-augmented agentic AI, structured as a four-level Data-Information-Knowledge-Wisdom (DIKW) hierarchy with code-execution agents at the Data/Information levels and reasoning agents at the Knowledge/Wisdom levels, can extract reusable behavioral design principles from completed field experiments and generate next-round interventions that outperform both expert-designed and frontier-LLM-designed baselines. The key finding: value comes from domain-specific experimental data processed through the learning infrastructure, not from the LLM's general reasoning ability — frontier LLMs operating without experimental data failed to predict which interventions would succeed (Spearman ρ = 0.27, n.s. for GPT-4o; ρ = −0.12 for Claude 3.5).

## When to Use

- Building a cumulative learning system that extracts design knowledge from each completed A/B test or megastudy to inform the next round
- Designing healthcare, policy, or marketing messaging where general behavioral theory is insufficient and domain-specific patterns must be discovered empirically
- Evaluating whether to invest in experimental-data infrastructure versus relying on LLM reasoning for intervention design
- Creating an auditable, transparent pipeline where every design decision traces back to specific statistical observations
- NOT for one-shot message generation without prior experimental data
- NOT for domains where behavioral theory already transfers cleanly (the method's value is in discovering where theory breaks)

## Core Process / Workflow

### 1. Stage 1 — Human + Chatbot design (baseline generation)

Follow the current state of practice: behavioral science experts collaborate with a conversational LLM (Level 1 AI — chatbots) to generate theory-driven message variants. Select psychological principles (Cialdini authority, prospect theory gain-loss framing, temporal salience, commitment devices, progress feedback, emotional appeals). Generate 3 candidates per principle, evaluate by majority vote, deploy in a randomized controlled trial. This generates the experimental dataset that feeds Stage 2.

### 2. Stage 2 — DIKW agentic learning (knowledge extraction)

#### Architecture (4 specialized agents + orchestrator, built on LangGraph)

```
Orchestrator → generates analytical topic plan at each DIKW level
  ↓
D-Agent (Data level) — code execution
  • Validates dataset integrity, randomization balance, schema
  • Documents experimental design parameters, message variants, features
  • Produces: executable Python scripts + CSV statistical tables + structured reports
  
I-Agent (Information level) — code execution  
  • Extracts individual statistical findings: engagement metrics stratified by subgroup
  • Analyzes message-performance variation, demographic patterns, temporal dynamics
  • Cross-dataset consistency checks
  • Produces: reproducible statistical reports with embedded figures
  
K-Agent (Knowledge level) — LLM reasoning (no code)
  • Synthesizes multiple I-level findings into integrated principle assessments
  • Requires multi-finding convergence (cross-subgroup consistency)
  • Assigns confidence scores weighted by statistical significance, sample size, cross-context robustness
  • Can pause and request additional D/I analyses (bidirectional flow)
  
W-Agent (Wisdom level) — LLM reasoning (no code)
  • Translates K-level assessments into concrete intervention designs
  • Each design accompanied by rationale tracing back to K-level → I-level → raw data
  • Operates under operational constraints (character limits, attribution, no misleading claims)
```

#### Critical separation principle

D and I agents use **autonomous code execution** (pandas, scipy, matplotlib, 150-300 lines per task) producing verified statistical facts. K and W agents use **LLM reasoning** over those verified facts. The system cannot assert a behavioral pattern unless I-level code execution has already produced numerical evidence. This prevents hallucination of behavioral patterns that unaided LLMs generate from training data.

#### Evidence-chain transparency

Every design decision traces back through: Wisdom (design rationale) → Knowledge (principle assessment + confidence) → Information (statistical finding) → Data (raw observation). This creates an auditable reasoning chain for post-hoc verification.

### 3. Validate in a second field experiment

Test AI-generated interventions against:
- The existing standard-of-care baseline (default message)
- The best-performing human+LLM-designed messages from Stage 1

Use stratified randomization by key covariates identified as moderators in Stage 1. Apply Holm-Bonferroni correction for multiple comparisons.

### 4. Compare against frontier LLMs without experimental data

Run frontier LLMs (GPT-4o, Claude) in pairwise comparison mode (380 comparisons for 20 messages → Elo ratings) without access to experimental data. Expect near-zero or negative correlation with actual effectiveness. This validates that the learning advantage comes from the data-processing infrastructure, not model capability.

## Key Empirical Findings

| Metric | Value | Context |
|---|---|---|
| Best AI-generated message CTR | 69.8% | +6.5pp over default baseline (10.3% relative) |
| Outperformance vs best human+LLM | +3.1pp | vs salience (66.7%), the top Stage 1 performer |
| Frontier LLM prediction accuracy | ρ = 0.27 (n.s.) | GPT-4o; Claude ρ = −0.12 (worse than random) |
| Messages significantly outperforming baseline | 4 of 17 | After Holm-Bonferroni correction (p ≤ 0.0031) |
| Total patient visits | 693,139 | Stage 1: 444,691; Stage 2: 248,448 |

### Domain-specific principles discovered (where general theory failed)

| Principle | Theory prediction | Actual finding |
|---|---|---|
| Efficiency framing | Not in standard frameworks | **#1 performer** — brevity + novelty cue + action verb |
| Completion framing | Moderate | #2 — "final step from your visit" |
| Professional authority | Strong (Cialdini) | #3 — works; casual personalization backfires |
| Social proof | Strong (Cialdini) | **Backfires** — underperforms baseline across all subgroups |
| Reciprocity | Moderate | **Backfires** — premature gratitude triggers persuasion knowledge |
| Direct commands | Moderate | **Underperforms** — triggers reactance (autonomy preservation) |

### Why domain-specific knowledge emerges (3 factors)

1. **Autonomy preservation**: patients resist directive language in medical contexts (reactance theory); efficiency framing conveys urgency implicitly without triggering resistance
2. **Professional norm governance**: casual tone undermines credibility where competence signaling matters; professional authority succeeds while casual personalization backfires
3. **Cognitive load sensitivity**: patients facing competing medical demands reward brevity and clarity over persuasive elaboration; completion framing succeeds by positioning action as finishing an existing process (Zeigarnik) rather than starting a new task

## Deployment Guardrails

- **Medical/legal/operational review**: all generated messages reviewed by platform leadership before deployment (3 of 20 excluded: too passive, ambiguous format, redundant)
- **Computational grounding**: K/W agents cannot assert patterns not verified by I-level code execution
- **Multi-finding convergence**: Knowledge-level confidence requires cross-subgroup consistency, not just aggregate significance
- **Bidirectional flow**: K-agent can request additional D/I analyses when evidence is insufficient
- **Version control**: all scripts, reports, and generated messages persisted for reproducibility

## A-Tech Applications

- **A-Coder**: Apply DIKW to developer-productivity experiments; extract design principles from A/B tests of nudge messages, UI interventions, and feature announcements
- **Be Practical**: Curriculum on cumulative experimental learning; teach that one-shot evaluation is obsolete when paired with agentic knowledge extraction
- **Builder's Club**: Open-source DIKW toolkit for behavioral experiment learning; the architecture is domain-independent (validated in healthcare, applicable to education, sustainability, productivity)

## Cross-References

- `llm-iterative-personalized-nudging` — LLM nudges with cross-round updating; DIKW extends this to multi-stage experimental learning
- `ai-agent-behavioral-science` — foundational behavioral science for AI agents
- `agent-experience-design-2026` — agent UX design patterns
- `nudge-transparency-disclosure-effectiveness` — transparency framework for behavioral interventions

## References

- See [references/dikw-evidence-base.md](references/dikw-evidence-base.md) for the full study extraction.