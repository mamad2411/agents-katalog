---
name: gander-open-voice-agent-architecture
description: Applies Tencent Hunyuan's Gander (Sept 9, 2026) — an open 9B Apache-2.0 omni-interaction model whose "Cerebellum-Brain" split decouples a fast streaming speech front-end (interruptible thinker-talker on MiniCPM-o 4.5) from a pluggable slow reasoning back-end (default Codex) so voice conversations keep flowing while long-horizon agent tasks run underneath. Use when [designing voice interfaces for coding agents, architecting split fast-interaction/slow-reasoning agent systems, evaluating open voice-agent stacks for local deployment, or building interruptible speech UX]. NOT for [text-only agent harness design (see nvidia-sol-pi-harness-self-optimization), agent payment flows (see ant-amp-kya-interoperability), or on-device model quantization (see bitnet-on-device-training-framework)].
---

# Gander: The Cerebellum-Brain Split for Voice-Native Agents

## Overview
Gander is the first open, fully local, Apache-2.0 artifact of the pattern most voice assistants bolt on badly: a fast streaming front half (speech + video + text in one-second chunks, interruptible mid-sentence via a detached Talker) paired with a pluggable orchestration runtime routing long-horizon tasks to a slower back brain (Codex by default). The split is the point — "most voice assistants that also run tasks bolt an agent onto a speech pipeline, which is why they go silent while they work."

## When to Use
- Adding voice/speech UX to coding or task agents without blocking the conversation loop
- Designing interruptible real-time interaction where background reasoning continues
- Choosing the pluggable back-brain boundary: which decisions stream vs which get routed to a reasoning agent
- Deploying a fully local voice-agent stack (clone → conda env → HF checkpoints → serve.sh → localhost:8000)

- NOT for harness token-efficiency optimization — see `nvidia-sol-pi-harness-self-optimization`

## Core Process / Workflow
1. **Split the interaction plane from the reasoning plane.** Front half: Thinker decides conversation flow; detached Talker renders speech so interruption mid-sentence loses no place. Back half: pluggable provider handles long-horizon work asynchronously and reports back. Route state through the orchestration runtime, never through the speech model.
2. **Make the back brain swappable.** Default Codex; the runtime connects streaming front-end to any agent handling long-horizon work. Design your integration at the runtime boundary, not the model boundary.
3. **Serve locally, fully.** Stack: faster-whisper-large-v3 (transcription) + Thinker/Talker checkpoints + pluggable back brain. One-second chunk streaming for video+speech+text.
4. **Check the license stack before shipping.** Gander is Apache-2.0, but derived from MiniCPM-o 4.5 and relies on faster-whisper-large-v3 — verify upstream components' terms for commercial shipping.
5. **Benchmark against the interaction metrics, not chat metrics.** Full-Duplex-Bench v3 turn-taking accuracy (100%, 8% premature interruptions), SpokenQA, Daily-Omni multimodal understanding (78.53%) — the interruptibility numbers are the design target for any voice-agent UX.

## Key Evidence
- **Source:** Tencent Hunyuan Speech Team with ZJU/SJTU/CUHK/NTU (Sept 9, 2026); 9B params; weights/code/data all released under Apache-2.0 on Hugging Face (Gander-Omni/Gander); base MiniCPM-o 4.5.
- **Interaction results:** SpokenQA 75.60% (Llama Questions) / 59.30% (Web Questions); Full-Duplex-Bench v3 100% turn-taking accuracy with 8% premature interruptions; Daily-Omni 78.53%.
- **Architecture lineage:** thinker-talker streaming design + detached orchestration — the first open artifact pairing real-time omni-interaction with pluggable long-horizon reasoning.

## Pairs-with
- `aws-pizza-bot-agent-inbox` (the ambient/inbox counterpart — Gander is the voice lane, Pizza Bot the inbox lane; both assume the human is not watching/listening continuously)
- `nvidia-sol-pi-harness-self-optimization` (harness efficiency layer — composes: run Gander's back brain on an efficiency-optimized harness)
- `hyperlayered-hypertext-agentic-reading` (interaction-layer design discipline)
- `recalibrategpt-ai-fatigue-operators-2026` (chat-surface cognitive load caution)
- `privacy-preserving-local-ai` (local-first deployment posture)

## A-Tech Alignment
- **Open source:** weights + code + training data, Apache-2.0, fully local-serving — anyone building a voice interface can study or change the split rather than accept a vendor's version of it.
- **Privacy:** fully local serving path (localhost) keeps speech and screen context off third-party endpoints; the back-brain choice (e.g. Ollama-hosted local models) can keep the reasoning plane local too.
- **Financial freedom:** a 9B model + pluggable cheap back brain = voice-agent capability at commodity-hardware cost; interruption-tolerant UX removes the latency tax that gates voice products.
- **Practical:** the Cerebellum-Brain boundary is directly portable — any agent product can adopt the two-plane split without the speech stack.

## Honesty Caveats
- Benchmark numbers are vendor-reported in the arXiv technical report; no independent replication found in the window.
- The default back brain (Codex) is a proprietary cloud provider — the "fully local" claim applies to the front half; back-brain choice determines the privacy boundary.
- 9B parameters bound front-half capability; complex multimodal reasoning quality unbenchmarked against frontier voice agents.
- Commercial shipping requires checking MiniCPM-o 4.5 and faster-whisper licenses upstream of the Apache-2.0 grant.

*Sources: Tencent Hunyuan Speech Team release (Sept 9, 2026) via AI/TLDR; Gander-Omni/Gander Hugging Face repo; arXiv technical report.*