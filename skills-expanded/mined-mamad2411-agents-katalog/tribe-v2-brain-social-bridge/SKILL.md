---
name: tribe-v2-brain-social-bridge
description: Bridges Meta's open-source TRIBE v2 brain-encoding model (predicts cortical fMRI-like responses to any video/audio/image from 450h of training data) with multi-agent social simulation (200 personality-diverse AI agents) via a novel seeding bridge that translates predicted cortical activation into personality-modulated emotional states, enabling pre-launch advertising analysis that predicts both neurological response and social-media cascade dynamics before a campaign airs. Use when testing ads before launch (go/no-go decision), when you need both neural and social predictions, or when building a brain-grounded campaign intelligence platform. NOT for post-launch sentiment analysis, for EEG-only neuromarketing (use multimodal-eeg-eye-tracking-consumer-choice), or for manipulating social cascades (guardrail: no manipulation).
---

# TRIBE v2 Brain–Social Bridge for Pre-Launch Campaign Intelligence

## Overview

Adneural (open-source, MIT-licensed, built at Purdue Catapult Hackathon 2026) is the first platform to connect computational neuroscience to social simulation for pre-launch advertising analysis. It uses Meta's open-source TRIBE v2 to predict cortical brain responses to any media stimulus, then translates those predictions into 9-dimensional emotional states, modulates them by Big Five personality traits, seeds 200 AI agents, and simulates social-media reactions — producing a go/no-go launch recommendation with neural + social rationale. The Jaguar "Copy Nothing" case study demonstrated retrospective prediction of the campaign's real-world failure before knowing the outcome.

## When to Use

- Making a go/no-go launch decision on an advertising campaign before it airs
- Predicting both neurological response (cortical activation) and social-media cascade dynamics
- Building a brain-grounded campaign intelligence platform that integrates neuroscience literature (GraphRAG over 22 papers)
- Translating predicted brain activation into personality-diverse emotional reactions
- Extending in-silico-neuromarketing-platform-pattern with a social-simulation layer
- NOT for post-launch sentiment analysis (social listening tools are sufficient)
- NOT for EEG-only neuromarketing — use multimodal-eeg-eye-tracking-consumer-choice
- NOT for manipulating social cascades (guardrail: no manipulation; diagnostic only)

## Core Process / Workflow

### 1. Brain encoding (TRIBE v2)

- Input: video/audio/image ad creative.
- Model: Meta TRIBE v2 (trained on 450h of fMRI data; open-source via facebookresearch/tribev2).
- Output: predicted cortical activation across 148 parcels, second-by-second.

### 2. Video summarisation

- LLM with frame extraction generates scene-by-scene description.
- This context is added to every downstream analysis step.

### 3. The seeding bridge (novel contribution)

Translate brain activation → agent emotional states:
1. **Network aggregation**: 148 cortical parcels → 8 functional brain networks.
2. **Emotional computation**: network activations → 9D emotional state vector (anxiety, trust, excitement, discomfort, memorability, etc.).
3. **Personality modulation**: base emotional state × Big Five traits → individualised response. (A neurotic viewer gets anxiety; an extraverted viewer gets curiosity — same brain data, different reactions.)
4. **Population distribution**: 200 agents across 6 archetypes (enthusiastic sharer, empathetic worrier, skeptical analyst, hostile critic, average viewer, emotional storyteller).

### 4. Social simulation

- Framework: MiroFish/OASIS multi-agent.
- Simulate Reddit-style social-media reactions.
- Detect cascades, analyse sentiment dynamics.

### 5. Neuro-translator (GraphRAG)

- Neo4j knowledge graph over 22 neuroscience papers (2,684 findings, 9,921 relationships).
- Translates neural findings into actionable insights via LangGraph.

### 6. Diagnostic agents and reports

Three-agent LangGraph pipeline produces four audience-specific reports:
- **Executive**: go/no-go recommendation with risk dashboard.
- **Marketing**: timestamped edit recommendations with neural rationale.
- **Compliance**: mental health impact assessment, regulatory flags.
- **Full Research**: complete neural-social bridge analysis with paper citations.

### 7. Guardrail check

- No manipulation: the platform is diagnostic, not persuasive.
- Subcortical structures (amygdala, hippocampus, nucleus accumbens) are inferred from cortical proxy patterns with explicit confidence tagging, not directly measured.

## Case Study: Jaguar "Copy Nothing" (Retrospective Validation)

| Adneural predicted (blind) | What actually happened |
|---|---|
| Weak emotional tagging, low memorability | Positive sentiment collapsed from 23% to 8% |
| No narrative processing (pure visual stimulus) | "Where are the cars?" became the meme |
| Narrative vacuum vulnerable to hostile reframing | The void got filled with ridicule |
| Minimal trust formation | No brand equity built; CEO resigned |

**Launch recommendation: NO GO** (predicted before knowing the outcome).

## A-Tech Application Matrix

### A-Coder (developer tool)
- Developer-ad brain bridge: test A-Coder launch trailers for neural + social response before release.

### Be Practical (education)
- Curriculum: "Brain-Grounded Campaign Intelligence" — from TRIBE v2 to social simulation.

### Builder's Club (community)
- Open-source Adneural fork for A-Tech community; hackathon to extend the seeding bridge.

## References

- See [references/tribe-v2-brain-social-bridge-evidence-base.md](references/tribe-v2-brain-social-bridge-evidence-base.md) for the full evidence base.