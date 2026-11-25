---
name: open-source-neuromarketing-tooling
description: Deploy open-source, self-hostable neuromarketing tools that score ad creatives across brain regions using AI models (CLIP, Whisper, TRIBE v2). Use when evaluating ad creative before spending, comparing variants, applying creator playbooks, or building privacy-first in-silico neuromarketing platforms.
---

# Open-Source Neuromarketing Tooling Pattern

## Overview

A new generation of open-source, self-hostable neuromarketing tools has emerged that bring lab-grade consumer neuroscience to anyone with a CPU. These tools use AI foundation models — CLIP for visual-semantic similarity, Whisper for audio transcription, and Meta's TRIBE v2 for predicted fMRI BOLD responses — to score marketing creative across brain regions without requiring EEG, fMRI, or biometric hardware.

## When to Use

- Pre-flight checking ads before spending promotion budgets
- Comparing two creative variants and wanting a structured reason, not a coin flip
- Fast iteration on hooks, thumbnails, and opening frames
- Applying a specific creator's playbook (Hormozi, GaryVee, Brunson) to your creative
- Building privacy-first neuromarketing into your product (no third-party data calls)
- Evaluating ad copy for cognitive friction before sending sponsorship pitches

## The Tooling Landscape

### Tier 1: CLIP-Based Brain Region Scoring

**NeuroPulse (neurolens)** — MIT-licensed, CPU-only, self-hostable
- Scores any image, video, YouTube/TikTok/Instagram URL, PDF, or text across **8 brain regions**
- Uses CLIP ViT-L/14 cosine similarity against neuroscience-informed probe texts
- Whisper transcribes video audio so spoken copy feeds language/persuasion regions
- Single-line verdict identifies weakest spot (e.g., "Forgettable — this won't stick in memory five minutes after viewing")
- Per-region breakdowns with concrete recommendations
- Compare two pieces of content side-by-side
- Creator Personas: Apply Hormozi, GaryVee, Brunson, Yadegari tactical playbooks
- Generate personas from content (paste transcripts, LLM extracts tactical playbook into 8-region structure)
- Backend: FastAPI + SQLite | Frontend: Next.js + shadcn/ui + Recharts
- Deploy: Hugging Face Space (free, 16GB RAM) + Vercel (free)

**8 Brain Regions Scored:**

| Region | What It Captures |
|--------|-----------------|
| Visual Cortex | Whether the visual hook pulls attention |
| Face & Social | Human presence and trust signal |
| Amygdala | Emotional charge |
| Hippocampus | Memorability and narrative arc |
| Language Areas | Copy clarity and voice |
| Reward Circuit | Payoff signal — what's in it for them |
| Prefrontal Cortex | Logical proof and reasons to believe |
| Motor Action | Strength of the call to action |

**Honest limits**: Not a peer-reviewed neuroscience instrument. Scores are CLIP cosine similarity against probe texts, mapped to 0-100. Treat as a creative-review heuristic, not a clinical signal. If you have ROAS/CTR data, trust that first.

### Tier 2: fMRI Prediction via TRIBE v2

**NeuroCopy Engine (JashanLabs)** — Open-source, GPU required (T4+)
- Runs text through Meta's **TRIBE** (Text and aRticulation Implicit Brain Evaluation) foundation model
- Predicts actual fMRI BOLD responses across targeted brain regions
- **Alpha Score Algorithm**: Temporal dynamics layer that doesn't just average brain response:
  1. **Reward vs. Friction**: Isolates Default Mode Network (safety/appeal) minus Anterior Cingulate + Insula (risk/cognitive load)
  2. **CTA Momentum (Dopamine Derivative)**: Mathematical derivative of engagement during final 25% of copy
  3. Positive momentum at CTA heavily weights final Alpha Score
- Temporal heatmaps: Visualize exactly when a reader's brain spikes or flatlines
- Requires ~16GB RAM + NVIDIA GPU

**Adneural (OmarMusayev)** — MIT-licensed, three-engine platform
- **Brain Encoding**: Meta TRIBE v2 (trained on 450h fMRI data) predicts cortical response
- **Video Summarizer**: LLM with frame extraction generates scene-by-scene description
- **Social Simulation**: 200 personality-diverse AI agents react and interact (MiroFish/OASIS framework)
- **Diagnostic Agents**: LangGraph + Neo4j GraphRAG over 22 neuroscience papers
- **Seeding Bridge**: Translates brain activation → 9D emotional state → Big Five personality modulation → individualized agent responses
- Generates 4 audience-specific reports: Executive (go/no-go), Marketing (edit recommendations), Compliance (mental health impact), Full Research

### Tier 3: In-Silico SaaS Platform

**IZRI (Ikramik)** — B2B SaaS, open-weights models
- "Replacing the MRI machine with AI"
- Upload video campaigns → simulated neural response → 3D WebGL brain visualization
- Uses open-weights TRIBE v2 + RunPod GPU pipeline
- Pay-per-analysis ($99/video) to enterprise API ($2,000+/month)
- 85%+ gross margin (cloud GPU inference <$1.50/video)

## Implementation Pattern

### For Individual Creators (NeuroPulse)
```bash
git clone https://github.com/nikolas-sapa/neurolens
cd neurolens
bash start.sh
# Open http://localhost:3000
# First run downloads ~600MB model weights (cached after)
```

### For Teams (NeuroCopy Engine)
```bash
git clone https://github.com/jashanlabs/neurocopy-engine
pip install -r requirements.txt
# Open neuro_optimizer.ipynb in Kaggle/Colab with GPU
# Input ad variations, execute pipeline
```

### For Platforms (Adneural architecture)
1. TRIBE v2 brain encoding integration
2. LLM video summarizer (frame extraction + vision-capable model)
3. Multi-agent social simulation (200 agents across 6 archetypes)
4. LangGraph diagnostic pipeline with Neo4j GraphRAG
5. Generate audience-specific reports (executive, marketing, compliance, research)

## Decision Framework

| Need | Tool | Setup | Cost | Privacy |
|------|------|-------|------|---------|
| Quick creative check | NeuroPulse | Self-host, CPU | Free | Full (no third-party calls) |
| Copy A/B testing | NeuroCopy Engine | Colab/Kaggle, GPU | Free | Your compute environment |
| Full campaign analysis | Adneural | Docker + Neo4j + GPU | Infra cost | Self-hosted |
| Agency SaaS | IZRI pattern | Cloud GPU pipeline | $1.50/video | Customer data on your infra |

## Key Insight: Open-Source Democratizes Neuromarketing

Traditional neuromarketing (fMRI/EEG studies) costs $50,000-$200,000 per campaign and takes months. These open-source tools bring the analytical layer to anyone:
- **Cost**: $0 (self-hosted) vs $50K-$200K (lab studies)
- **Speed**: Seconds vs. months
- **Privacy**: Runs locally, no third-party calls vs. data sent to vendor
- **What you get**: Creative-review heuristic, not clinical signal

The honest framing matters: these are structured creative-review heuristics using CLIP/fMRI-prediction models, not peer-reviewed neuroscience instruments. Use them to identify weak spots before spending, not as a replacement for real performance data.

## Ethics Guardrails

- These tools measure *predicted* neural engagement, not actual brain responses
- Don't use for manipulation — use for clarity (presenting real offers in ways the brain best evaluates them)
- Transparent about limitations: "creative-review heuristic" not "neuroscience signal"
- Privacy-first: self-hosting means no consumer data leaves your infrastructure
- If you have ROAS/CTR data, trust that first — these tools are for the stage before you spend

## Sources

- NeuroPulse: github.com/nikolas-sapa/neurolens (MIT License)
- NeuroCopy Engine: github.com/jashanlabs/neurocopy-engine
- Adneural: github.com/OmarMusayev/Adneural (MIT License)
- IZRI: github.com/Ikramik/Izri
- TRIBE v2: github.com/facebookresearch/tribev2 (Meta FAIR)
- Neuromarketing Claude Skill: github.com/Claudefarid/neuromarketing-claude-skill