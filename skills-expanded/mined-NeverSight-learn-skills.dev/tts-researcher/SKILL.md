---
name: tts-researcher
description: Methodical research and implementation workflow for Text-to-Speech (TTS) models. Use when gathering academic resources, locating official and community repos, adapting architectures to new languages, training, or evaluating TTS systems.
---

# TTS Researcher

A specialized workflow for gathering resources, adapting architectures, and evaluating Text-to-Speech AI models.

## Methodical Research Workflow

When tasked with researching a TTS architecture or language adaptation, follow this sequence:

### 1. Architectural Deep-Dive
- **Identify Core Papers**: Find the foundational paper(s), any follow-ups, and the official repository.
- **Analyze Model Paradigm**: Determine if it is Autoregressive (AR), Non-Autoregressive (NAR), Diffusion-based, or Flow-matching.
- **Reference**: See [references/tts-landscape.md](references/tts-landscape.md) for a guide on major paradigms.

### 2. Resource Gathering (Academic + Implementation)
- **Primary Sources**: Collect papers, surveys, and benchmark reports that define the architecture and its evaluation.
- **Official Repos**: Locate the original or organization-owned GitHub repo and note license, last update, and reproducibility status.
- **Community Repos**: Search for forks and third-party implementations, especially ones adapted to new languages.
- **Report Findings**: Provide a short list of the most credible and relevant sources before moving on.

### 3. Community & Adaptation Research
- **Locate Custom Implementations**: Search GitHub for forks or unofficial implementations, specifically those targeting different languages (e.g., "MeloTTS-German", "VITS-Spanish").
- **Technical Hurdles**: Note any language-specific challenges mentioned in community discussions (e.g., pitch accent, tonal languages, specific phonemizers).

### 4. Training & Adaptation Requirements
- **Data Preparation**: Identify the required dataset format (e.g., LJSpeech, LibriTTS) and transcription needs.
- **Phonemization**: Verify the availability of phonemizers (e.g., `espeak-ng`, `gruut`) for the target language.
- **Hardware**: Estimate VRAM requirements for training and inference.
- **Reference**: Use [references/adaptation-checklist.md](references/adaptation-checklist.md) to verify readiness.

### 5. Evaluation Strategy
- **Objective Metrics**: Plan for MCD (Mel Cepstral Distortion), WER (Word Error Rate), and F0 Correlation.
- **Subjective Metrics**: Design a MOS (Mean Opinion Score) test or MUSHRA test if applicable.
- **Reference**: See [references/evaluation-guide.md](references/evaluation-guide.md) for metric definitions and tools.

## Recommended Tools
- `google_web_search`: For finding recent papers and repos.
- `paper_search`: For deep academic research on Hugging Face Hub.
- `hub_repo_search`: For finding models and datasets on Hugging Face.
- `query-docs`: For technical implementation details of libraries (e.g., `torch`, `transformers`).
