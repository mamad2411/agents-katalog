---
name: phf-hierarchical-user-modeling
description: Applies Bourdieu's Theory of Practice (Practice-Habitus-Field) to LLM personalization by building hierarchical user models that capture individual dispositions and collective behavioral regularities. Use when designing LLM personalization systems that go beyond flat behavioral histories, when building collaborative filtering for LLMs without shared item observations, when addressing cold-start personalization, or when modeling user behavior through sociological frameworks rather than pure interaction logs.
---

# PHF: Practice-Habitus-Field for LLM Personalization

## Overview

PHF (Practice-Habitus-Field) reconceptualizes LLM personalization through Pierre Bourdieu's Theory of Practice, organizing user behavior into three hierarchical levels that address the limitations of flat behavioral paradigms in existing personalization systems.

Based on Wang, Mou, Liu, Wang, Wang & Wei (arXiv:2606.02300, June 2026, Fudan University / Shanghai Innovation Institute / OPPO).

## The Core Problem

Existing LLM personalization methods adopt a **flat behavioral paradigm** — treating user behaviors as an unordered collection of observed instances. This produces two key limitations:

1. **Behavior fragmentation**: Within each user, behavioral histories lack internal structure. Behaviors are treated as isolated instances rather than consolidated into stable long-term patterns.
2. **User isolation**: Users are modeled independently without leveraging shared behavioral regularities across users with similar profiles, limiting generalization when history is sparse.

## The PHF Framework — Three Hierarchical Levels

### Level 1: Practice (Individual Behavior)
Individual user behaviors are abstracted as **practices** — denoised semantic representations that filter surface-level noise while preserving core behavioral semantics.

Implementation: Each interaction (query-response pair) is encoded and quantized into a discrete **Semantic ID** using residual vector quantization (RQ-VAE). Multi-level quantization decomposes each interaction into coarse-to-fine semantic components:
- Level 1: Dominant behavioral intent (e.g., "fantasy" vs "action" vs "romance")
- Level 2: Sub-genre or sub-intent refinement
- Level 3: Fine-grained residual distinctions

This discretization causes behaviors with different surface forms but similar underlying intent to converge toward shared prototypes — a behavioral abstraction process.

### Level 2: Habitus (Long-Term Dispositions)
Practices are **temporally aggregated** into habitus — stable behavioral dispositions that characterize each user's long-term tendencies.

Implementation: Temporally weighted aggregation using square-root recency scaling:
```
h_i = Σ(w_t * x̂_it), where w_t = exp(√t) / Σ exp(√τ)
```
The square-root scaling ensures recency effects grow sublinearly, preventing recent behaviors from dominating while preserving temporal sensitivity. The resulting habitus vector encodes a coherent representation of the user's long-term behavioral disposition.

Key insight: Habitus captures the *trajectory* of a user's preferences over time, not just their current state. A user who "used to like Harry Potter, now more interested in superhero stories" has a habitus that reflects this evolution.

### Level 3: Field (Collective Behavioral Structure)
Users with similar habitus are organized into **fields** — shared behavioral communities that encode collective regularities.

Implementation: K-Means clustering over habitus representations partitions users into K latent fields. Each field centroid becomes a field embedding that captures the shared behavioral disposition of users within that cluster. At inference, each user is assigned to their nearest field — requiring no access to other users' data.

Collaborative signal: Fields provide inductive bias similar to collaborative filtering, but without requiring overlapping observations across identical items. Users with similar long-term dispositions tend to exhibit similar preferences even in sparse-history settings.

## PHFCompass Implementation

PHFCompass is a lightweight, model-agnostic implementation:

### Architecture
- **Encoder**: Contriever (default) or RoBERTa-large for interaction encoding
- **Quantizer**: 3-level RQ-VAE with codebook sizes 32-32-16 (hybrid K-Means / balanced K-Means initialization)
- **Decoder**: Frozen LLM (Qwen2.5-7B-Instruct default; also tested with LLaMA-3-8B-Instruct)
- **Training**: Only lightweight projection layers trained; LLM remains frozen
- **Field count**: K=10 (optimal balance point; performance degrades beyond K=15 due to fragmentation)

### Key Results (LaMP Benchmark)
PHFCompass achieves best performance across all 6 LaMP tasks:

| Task | Type | PHFCompass | Best Flat Baseline | Improvement |
|------|------|-----------|-------------------|-------------|
| LaMP-1 (Citation) | Classification | 0.631 | 0.529 (ROPG) | +19.3% |
| LaMP-2 (Movie Tag) | Classification | 0.531 | 0.503 (OPPU) | +5.6% |
| LaMP-3 (Product Rating) | Regression | 0.260 MAE | 0.314 (T-H) | -17.2% |
| LaMP-4 (News Headline) | Generation | 0.193 R-1 | 0.192 (OPPU) | +0.5% |
| LaMP-5 (Scholarly Title) | Generation | 0.516 R-1 | 0.512 (T-H) | +0.8% |
| LaMP-7 (Tweet Paraphrase) | Generation | 0.535 R-1 | 0.524 (OPPU) | +2.1% |

### Ablation Insights
- **Removing habitus** causes largest degradation → individual behavioral representations are fundamental
- **Removing field** causes moderate declines, especially on classification tasks → collaborative signals beneficial for reasoning-heavy personalization
- **Classification tasks** depend more on field (behavioral logic); **generation tasks** depend more on habitus (stylistic consistency)
- **RAG integration degrades performance** — latent habitus/field embeddings already capture essential user characteristics; raw retrieved text adds noise

## When to Use This Skill

### Triggers
- Designing LLM personalization beyond retrieval-augmented prompting
- Addressing cold-start or sparse-history personalization
- Building collaborative filtering without shared item observations
- Modeling user preference evolution over time
- Applying sociological frameworks to AI personalization
- Designing user embeddings that capture both individual and collective patterns

### NOT For
- Single-turn, context-free generation (no personalization needed)
- Systems where users have identical, dense interaction histories
- Applications where raw retrieval text is required (RAG may be better)
- Real-time streaming personalization (PHF evaluated on static histories only)

## Practical Application Guide

### Step 1: Map Your Personalization Problem to PHF Levels
Ask: Does your problem suffer from behavior fragmentation (need habitus) or user isolation (need field)?
- Fragmentation only → implement habitus (temporal aggregation)
- Isolation only → implement field (clustering)
- Both → implement full PHF

### Step 2: Choose Your Feature Abstraction
- Dense embedding + RQ-VAE quantization (PHFCompass default)
- Text-based persona summarization (T-H variant: cheaper but less effective)
- Direct embedding aggregation (simplest, no quantization)

### Step 3: Determine Field Granularity
- K=10 is a robust default
- Small K: coarser fields, more users per cluster, stronger collaborative signal but risk of dilution
- Large K: finer fields, higher internal homogeneity but weaker collaborative signal due to sparsity
- Monitor t-SNE visualization for cluster separation quality

### Step 4: Architectural Integration
```
Input = [ϕh(habitus), ϕf(field), Emb(query)]
→ Frozen LLM → Personalized response
```
Only projection layers (ϕh, ϕf) are trained. The LLM stays frozen, making this compatible with any backbone.

## Interpretability

PHFCompass produces interpretable Semantic IDs:
- Same semantic ID → strong thematic coherence (e.g., 0-14-2 groups "romance in fantastical worlds": Wonder Woman, Howl's Moving Castle)
- Level-1 codes reveal fine-grained distinctions within broad categories
- Same movie with different tags yields different IDs (e.g., Inception as action: 8-21-12; as psychology: 15-21-12) — user-specific intent disentangled from shared semantic structure

## A-Tech Value Alignment

| A-Tech Value | Alignment |
|-------------|-----------|
| **Open-source AI** | Compatible with any frozen open-weight LLM (Qwen2.5, LLaMA-3 tested); MIT-licensed code release planned |
| **Data privacy** | Field embeddings derived from cluster centroids; no cross-user data sharing at inference; user-level data never leaves device |
| **Financial freedom** | Lightweight (only projection layers trained); no fine-tuning of base LLM; reduces compute cost vs full personalization |
| **Practical implementation** | Validated on 6 LaMP tasks; model-agnostic; reproducible with open benchmarks |

## Cross-References

- `ai-nudging-habit-formation` — habitus concept parallels habit formation theory
- `parasocial-ai-relationship-design` — field concept enables community-level modeling
- `dynamic-ai-personalization-nexus` — PHF as structural alternative to flat personalization
- `ai-user-personality-adoption-edger` — personality traits as habitus components
- `ai-agent-behavioral-science` — Bourdieu's framework as behavioral science foundation

## Limitations

- Evaluated only on LaMP benchmark (English text, static histories)
- No evaluation of streaming/dynamic habitus updates or field re-clustering
- LaMP lacks continuously evolving interactions — real-world deployment needs adaptive field management
- Standard classification/generation metrics may not capture personalization quality nuances (user satisfaction, perceived relevance, behavioral consistency)
- Alternative implementations of each level (recurrent attention for habitus, graph-based community detection for field) unexplored

## Future Directions

1. **Streaming PHF**: Implement dynamic habitus updates and periodic field re-clustering
2. **Multimodal PHF**: Extend beyond text to image, audio, video interactions
3. **Fairness-aware fields**: Investigate whether field clustering reinforces existing biases
4. **Graph-based fields**: Replace K-Means with community detection for richer topological structure
5. **Attention-based habitus**: Replace weighted averaging with recurrent/attention temporal architectures