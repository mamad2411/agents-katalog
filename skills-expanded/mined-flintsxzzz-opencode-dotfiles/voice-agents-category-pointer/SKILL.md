---
name: voice-agents-category-pointer
description: "Pointer to a library of 5 specialized Voice Agents skills. Use when working on voice-agents-related tasks."
risk: none
---

# Voice Agents Capability Library 🎯

This is a **pointer skill**. The 5 specialized Voice Agents skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **audio-transcriber** — Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration
- **auri-core** — Auri: assistente de voz inteligente (Alexa + Claude claude-opus-4-20250805). Visao do produto, persona Vitoria Neural, stack AWS, modelo Free/Pro/Business/Enterprise, roadmap 4 fases, GTM, north star WAC e analise competitiva.
- **fal-audio** — Text-to-speech and speech-to-text using fal.ai audio models
- **pipecat-friday-agent** — Build a low-latency, Iron Man-inspired tactical voice assistant (F.R.I.D.A.Y.) using Pipecat, Gemini, and OpenAI.
- **voice-ai-development** — Expert in building voice AI applications - from real-time voice agents to voice-enabled apps. Covers OpenAI Realtime API, Vapi for voice agents, Deepgram for transcription, ElevenLabs for synthesis, LiveKit for real-time infrastructure, and WebRTC fundamentals.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/voice-agents/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/voice-agents`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
