---
name: lemonslice-overview
description: Understand Lemon Slice and the available integration paths. Use this first to learn what Lemon Slice is.
license: MIT
---

# Lemon Slice Overview

## Official docs
- https://lemonslice.com/docs/introduction.md

## Use this skill when
You need to understand what Lemon Slice is, how it works, and what integration options are available before deciding how to build with it.

## Do not use this skill when
You have already selected an integration path and need specific implementation details. If you already know your path, use the specific skill for that integration (e.g., `lemonslice-livekit`, `lemonslice-hosted`). If you need help choosing, use `lemonslice-integration-choice`.

## Agent workflow
1. Understand the core product: Lemon Slice is a real-time avatar video platform powered by the LemonSlice-2 model. It provides AI-powered digital avatars that can engage in real-time video conversations.
2. Understand the three main tiers of integration:
   - **Widget**: A prebuilt embeddable web component. The easiest way to add an avatar to a website.
   - **Hosted Pipeline**: Lemon Slice manages the agent backend (STT, LLM, TTS). The developer builds the frontend UI and controls the call lifecycle.
   - **Self-Managed Pipeline**: The developer owns and manages the entire agent stack (STT, LLM, TTS). Lemon Slice is used purely as a real-time video generation layer.
3. Understand the supported frameworks:
   - LiveKit (Self-Managed)
   - Pipecat (Self-Managed)
   - REST API (Hosted or Self-Managed)
4. Read the `lemonslice-integration-choice` skill next. This is the mandatory router for the repository and MUST be used to select the correct technical path before any code is written.

## Common mistakes
- Confusing Hosted Pipeline with Self-Managed Pipeline. Hosted means Lemon Slice runs the AI; Self-Managed means you run the AI.
- Starting to code before choosing a clear integration path. The APIs and packages are entirely different for each path.

## Validation checklist
- [ ] Do I understand the difference between Hosted and Self-Managed?
- [ ] Have I identified whether this project uses LiveKit, Pipecat, or a custom stack?
- [ ] Have I routed to `lemonslice-integration-choice` to finalize the path?
