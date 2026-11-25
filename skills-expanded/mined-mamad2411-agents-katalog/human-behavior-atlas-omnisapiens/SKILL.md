---
name: human-behavior-atlas-omnisapiens
description: Applies the Human Behavior Atlas benchmark and OmniSapiens 2.0 foundation model for unified social behavior processing. Use when evaluating multimodal behavioral AI, building emotion recognition systems, detecting sarcasm or humor, or developing socially intelligent agents.
---

# Human Behavior Atlas & OmniSapiens 2.0: Unified Social Behavior Processing

## Overview
The **Human Behavior Atlas (HBA)** is a large-scale benchmark for unified psychological and social behavior understanding, introduced at ICLR 2026 (Ong, Dai, Li et al., MIT). It spans diverse behavioral domains — emotion recognition, sentiment understanding, humor/sarcasm detection, intent recognition, non-verbal communication, and mental health indicators — under a single evaluation framework with multimodal inputs (text, audio, video, images).

**OmniSapiens 2.0** (ICML 2026) is the first-of-its-kind foundation model for general social behavior processing. Built on Qwen2.5-Omni-7B and trained with a novel reasoning-RL algorithm called **Heterogeneity-Aware Relative Policy Optimization (HARPO)**, it achieves state-of-the-art across the HBA benchmark. All models, benchmark data, and code are openly released (Apache 2.0 models, public benchmark on HuggingFace, code on GitHub at MIT-MI/human_behavior_atlas).

## When to Use
- Building emotion-aware AI or affective computing systems that need multimodal input
- Evaluating multimodal behavioral AI models against a standardized benchmark
- Developing socially intelligent agents that must read sarcasm, humor, intent, or non-verbal cues
- Benchmarking behavioral AI systems across diverse psychological domains
- Researching on-device / privacy-preserving behavioral processing (open-weight models enable local inference)
- Designing conversational agents that need social intelligence beyond text

- NOT for clinical diagnosis of mental health conditions (research-grade, population-level signals)
- NOT as a replacement for human judgment in high-stakes emotional assessment
- NOT for real-time surveillance applications (ethical use required; see limitations)

## Core Concepts

### Human Behavior Atlas (HBA) Benchmark
A unified evaluation framework covering six behavioral domains:
1. **Emotion recognition** — identifying emotional states from multimodal signals
2. **Sentiment understanding** — polarity and nuance beyond positive/negative
3. **Humor/sarcasm detection** — the hardest social signal for AI; includes cross-modal cues
4. **Intent recognition** — inferring what a speaker/actor aims to achieve
5. **Non-verbal communication** — pose, gesture, facial expression, prosody
6. **Mental health indicators** — behavioral markers relevant to wellbeing

**Benchmark structure:** JSONL splits with fields `problem` / `answer` / `images` / `videos` / `audios` / `texts`. Each sample carries a **modality signature** (e.g., `text_audio`, `video`, `text_video`) indicating which modalities are present. Pre-extracted features include pose estimates and OpenSMILE audio features, enabling reproducible evaluation without re-running feature extractors.

### OmniSapiens 2.0 Foundation Model
The first foundation model designed for **general social behavior processing** — unifying the HBA domains under a single model rather than training per-task specialists.

- **Base architecture:** Qwen2.5-Omni-7B (natively multimodal: text + audio + image + video)
- **Training framework:** VERL (Volcano Engine Reinforcement Learning)
- **Reasoning-RL algorithm:** HARPO (Heterogeneity-Aware Relative Policy Optimization) — a novel RL method that accounts for the heterogeneity of behavioral tasks during reward shaping
- **Release:** 6 models on HuggingFace (see references/evidence-base.md for the full comparison table)

### Three-Stage SFT Pipeline
OmniSapiens 2.0 is trained in three sequential supervised fine-tuning stages:

1. **Classification training** — per-task classification heads attached to the backbone; teaches domain-specific behavioral discrimination
2. **QA training** — backbone frozen, only `lm_head` trained; converts classification knowledge into natural-language reasoning
3. **BAM (Behavioral Adapter Module)** — lightweight per-dataset residual adapters; enables efficient specialization without full retraining

### HARPO Algorithm
Heterogeneity-Aware Relative Policy Optimization is the reasoning-RL algorithm used to refine OmniSapiens 2.0. Unlike standard RLHF, HARPO explicitly accounts for the fact that behavioral tasks differ widely in difficulty, label structure, and modality availability — it shapes relative rewards in a heterogeneity-aware manner so the model doesn't over-optimize easy tasks at the expense of hard ones (e.g., sarcasm detection).

## Released Models (HuggingFace)

| Model | Description |
|---|---|
| OmniSapiens-7B-RL | RL-refined model with HARPO |
| OmniSapiens SFT | Supervised fine-tuned base (post 3-stage SFT) |
| BAM — humour adapter | Lightweight residual adapter for humor detection |
| BAM — sentiment adapter | Lightweight residual adapter for sentiment understanding |
| BAM — sarcasm adapter | Lightweight residual adapter for sarcasm detection |
| OmniSapiens 2.0 | Full SOTA model (SFT + BAM + HARPO RL) |

See [references/evidence-base.md](references/evidence-base.md) for HuggingFace links, training pipeline details, and the BAM architecture.

## Core Process / Workflow

### 1. Task Identification
Determine which HBA behavioral domain(s) your use case maps to:
```
domain: emotion_recognition | sentiment | humor_sarcasm | intent | non_verbal | mental_health
modalities: text | audio | video | image | text_audio | text_video | ...
```

### 2. Model Selection
- **Full SOTA:** Load `OmniSapiens 2.0` for best cross-domain performance
- **Lightweight / specialized:** Load `OmniSapiens SFT` + the relevant BAM adapter (humour/sentiment/sarcasm)
- **Research / RL ablation:** Use `OmniSapiens-7B-RL` to study HARPO effects

### 3. Benchmark Evaluation
Use the HBA JSONL splits to evaluate. Each sample includes a modality signature so you can subset by available modalities:
```python
# Pseudocode
sample = {"problem": "...", "answer": "...", "images": [...], "audios": [...],
          "modality": "text_audio"}
prediction = omnisapiens.generate(sample)
```

### 4. On-Device / Privacy-Preserving Deployment
Because OmniSapiens 2.0 is open-weight (Apache 2.0) and built on Qwen2.5-Omni-7B (7B parameters), it is feasible to run behavioral inference on-device — enabling privacy-preserving social intelligence without sending behavioral data (audio, video, text) to a cloud server.

### 5. Custom Domain Adaptation
For new behavioral domains not in HBA, train a new BAM adapter (Stage 3 of the SFT pipeline) on your dataset. The backbone remains frozen; only the lightweight residual adapter is trained — making adaptation cheap and fast.

## Key Findings (Ong, Dai, Li et al., 2026)

- HBA is the first benchmark unifying psychological and social behavior understanding across six domains under a single multimodal framework
- OmniSapiens 2.0 is the first foundation model for general social behavior processing — a single model handles all HBA domains
- HARPO reasoning-RL outperforms standard RLHF on heterogeneous behavioral tasks, especially hard ones like sarcasm/humor
- The three-stage SFT pipeline (classification → QA → BAM) decouples broad behavioral knowledge from cheap per-dataset specialization
- All resources are open: benchmark data (parquet + tar on HuggingFace), code (GitHub MIT-MI/human_behavior_atlas), models (Apache 2.0 on HuggingFace)

## Applications

### A-Coder (A-Tech Coding Assistant)
- Detect frustration or confusion in developer voice/text for adaptive assistance
- Sarcasm detection in code review comments to avoid misinterpreting tone
- Intent recognition for natural-language code requests

### Be Practical (A-Tech Learning Platform)
- Emotion-aware learning content adaptation (detect engagement vs. frustration)
- Sentiment analysis of learner feedback across modalities
- Mental health indicator monitoring for at-risk learner support (ethical, opt-in)

### Builder's Club (A-Tech Community)
- Social intelligence for community moderation agents (detect hostility, humor, intent)
- Multimodal sentiment analysis of community content
- Non-verbal communication analysis for video-based community events

## A-Tech Value Alignment

| A-Tech Value | Alignment |
|---|---|
| **Open-source AI** | Apache 2.0 models, public benchmark on HuggingFace, MIT-licensed code on GitHub |
| **Data privacy** | On-device behavioral processing possible (7B open-weight model); no cloud dependency for sensitive behavioral data |
| **Practical implementation** | VERL framework integration, HuggingFace deployment, BAM adapters for cheap customization |

## Practical Triggers
Use this skill when:
- Building emotion-aware AI that needs multimodal input (text + audio + video)
- Evaluating multimodal behavioral models against a standardized benchmark
- Developing social intelligence in agents (sarcasm, humor, intent, non-verbal cues)
- Benchmarking behavioral AI systems across diverse psychological domains
- Needing privacy-preserving on-device behavioral inference
- Adapting a foundation model to a new behavioral domain via lightweight adapters

## Limitations
- Research-grade models; not validated for clinical mental health diagnosis
- Behavioral domains in HBA are a subset of human social behavior — not exhaustive
- Sarcasm/humor detection remains the hardest domain; performance varies by cultural context
- Pre-extracted features (pose, OpenSMILE) are dataset-specific; new data requires re-extraction
- HARPO is novel; limited independent replication at time of writing
- Ethical use required — social behavior models can be misused for surveillance or manipulation

## References
- See [references/evidence-base.md](references/evidence-base.md) for model comparison table, training pipeline details, benchmark dataset structure, BAM adapter architecture, and HARPO algorithm description.