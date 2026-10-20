---
name: triple-dual-process-llm-personalization
description: Applies the TRIPLE framework (Theory-guided Reasoning for Intent and habIt Profiling with LLMs for pErsonalization) to ground LLM-based personalization in validated behavioral theories — dual-process theory and the Theory of Planned Behavior. Use when designing personalized AI systems, user profiling pipelines, behavioral prediction models, or anytime an LLM personalization approach needs psychological grounding rather than empirical heuristics. NOT for real-time adaptive systems without user history, or for non-behavioral personalization (e.g., pure content recommendation without behavioral outcomes).
---

# TRIPLE: Theory-Guided LLM Personalization

## When to Use

- Building LLM-based user profiling or personalization systems
- Designing personalized nudges, recommendations, or behavioral interventions
- Creating user models that need interpretable, psychologically grounded explanations
- Improving prediction accuracy on complex generative personalization tasks
- When existing in-context learning personalization lacks theoretical grounding

## Core Framework

TRIPLE (Noh, Jin, Yeo & Han, Hanyang University, AAAI-26) systematically integrates dual-process theory from social psychology into LLM-based user modeling. Most existing LLM personalization relies on empirical heuristics — TRIPLE grounds profiling in validated psychological mechanisms.

### Three-Component Architecture

**1. Habitual Behavior Profile (System 1)**
- Identifies repeated patterns over time to model automatic responses
- Captures what users do without deliberate thought
- Built from interaction history: frequency, recency, consistency of behaviors
- Represents the fast, intuitive thinking pathway (Kahneman System 1)

**2. Intentional Behavior Profile (System 2)**
- Infers user attitudes, subjective norms, and perceived behavioral control
- Based on the Theory of Planned Behavior (Ajzen)
- Captures deliberate, goal-directed reasoning
- Represents the slow, analytical thinking pathway (Kahneman System 2)
- Components:
  - *Attitudes*: evaluation of behavior outcomes
  - *Subjective norms*: perceived social pressure
  - *Perceived behavioral control*: self-efficacy assessment

**3. Behavioral Rationale Generation**
- Reveals the interaction between habitual and intentional processes
- Predicts user behavior in context-specific situations
- Generates interpretable explanations of *why* a user will behave a certain way
- Bridges the two profiles into actionable predictions

### Evaluation Results (LaMP Benchmark, 5 tasks)

TRIPLE consistently outperforms existing in-context learning methods:
- Particularly pronounced gains on complex generative tasks (headline/title generation)
- Open-source LLMs used throughout (reproducible without proprietary APIs)
- Profiles and reasoning paths provide interpretable, psychologically grounded explanations
- Evidence that incorporating validated behavioral theories enhances both predictive performance AND interpretability

### Dual-Process Integration Pattern

The key insight: most LLM personalization treats user behavior as a single stream. TRIPLE separates it into:
- **What users do automatically** (habits) → model from repeated patterns
- **What users choose deliberately** (intentions) → model from attitudes, norms, control beliefs
- **How these interact** (behavioral rationale) → generate context-specific predictions

This separation mirrors how humans actually make decisions: some behaviors are habitual (System 1), some are intentional (System 2), and most real decisions involve an interaction between the two.

## Practical Application Steps

### Step 1: Habitual Profile Construction
```
For each user, extract from interaction history:
- Repeated action patterns (frequency > threshold)
- Temporal regularity (same time/context → same action)
- Automatic response triggers (stimulus → response without deliberation)
- Habit strength score = frequency × consistency × recency weighting
```

### Step 2: Intentional Profile Construction
```
For each user, infer from expressed preferences and behaviors:
- Attitudes: "User values X because..." (outcome evaluation)
- Subjective norms: "User's community expects..." (social pressure signals)
- Perceived behavioral control: "User can/cannot do X because..." (capability assessment)
- Intention strength = attitude × norm × control belief weighting
```

### Step 3: Behavioral Rationale Generation
```
For each prediction context:
1. Check if habitual profile has a strong matching pattern
   → If yes, predict habitual behavior, explain as automatic response
2. Check if intentional profile has relevant attitudes/norms
   → If yes, predict intentional behavior, explain as deliberate choice
3. When both are active, model the interaction:
   → Strong habit may override weak intention (habit bypass)
   → Strong intention may break weak habit (conscious override)
   → Generate rationale explaining which won and why
```

## A-Tech Value Alignment

| A-Tech Value | Alignment |
|---|---|
| **Open-source AI** | Uses open-source LLMs throughout; reproducible without proprietary APIs |
| **Data privacy** | Profiles built from behavioral history, not personal data; can run locally |
| **Financial freedom** | Theory-grounded approach reduces need for expensive empirical tuning |
| **Practical implementation** | Validated on LaMP benchmark across 5 personalization tasks |

## Design Implications

### For Personalization System Designers
- Separate habitual from intentional user modeling — don't treat all behavior as one stream
- Use TPB constructs (attitudes, norms, control) as structured dimensions for user profiles
- Generate behavioral rationales for interpretability, not just predictions
- Theory-guided personalization outperforms heuristic approaches, especially on generative tasks

### For Behavioral Intervention Design
- Identify whether a target behavior is habitual or intentional before designing intervention
- Habitual behaviors: disrupt the cue-routine loop, don't try to change attitudes
- Intentional behaviors: strengthen attitudes, norms, or perceived control
- Mixed behaviors: address both systems; habits may override intentions

### For Open-Source AI Products
- Build user profiles with explicit habitual/intentional separation
- Use the behavioral rationale as a transparency feature (explainable AI)
- Open-weight LLMs can run the TRIPLE pipeline without API costs
- Privacy-preserving: all profiling happens locally from interaction data

## Cross-References

- `behavioral-psychology-and-nudging/behavioral-psychology` — Dual-process theory foundations
- `behavioral-psychology-and-nudging/llm-iterative-personalized-nudging` — LLM nudge personalization
- `cognitive-science-and-ux/ai-ux-laws-translation` — Cognitive processing in UX
- `marketing-and-content/dynamic-ai-personalization-nexus` — Dynamic personalization architecture
- `privacy-and-trust/privacy-first-personalization-2026` — Privacy-preserving personalization

## Key Insight

Theory-guided personalization beats heuristic personalization. Grounding LLM user models in validated psychological theories (dual-process, TPB) improves both prediction accuracy and interpretability. The separation of habitual (System 1) and intentional (System 2) behavior profiles is the core innovation — most existing approaches conflate them into a single flat representation.