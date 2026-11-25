---
name: leeway-frontier-voice-architecture-selector
description: Formula-governed selector for cascaded streaming, native speech-to-speech/Thinker-Talker, and experimental continuous-latent voice architectures using evidence, hardware, latency, quality, control, privacy and tool requirements.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  class: VOICE_ARCHITECTURE_SELECTOR
---
# LeeWay Frontier Voice Architecture Selector

## Mission
Never force one voice architecture onto every workload. Select the best verified architecture for the task and preserve a common full-duplex control/evidence fabric.

## Architecture A — Cascaded Streaming
Audio → VAD/endpointing → streaming STT → LLM/tool loop → streaming TTS → playout.
Prefer when explicit transcripts, deterministic tool workflows, provider modularity, auditability, accessibility, constrained hardware or independent component replacement dominate.

## Architecture B — Native Speech-to-Speech
Audio encoder/representation → multimodal Thinker/reasoner → streaming speech Talker/decoder → audio.
Prefer when the selected provider/model has verified native speech capability and prosody/acoustic context/low interaction latency materially matter. Native primary speech paths may still emit/maintain text or semantic side channels for tools, audit, accessibility and recovery.

## Architecture C — Continuous Geometric State-Space Research
Continuous acoustic representations, continuous-time/state-space coupling and flow/diffusion acoustic decoding are Formula Factory research candidates. Hyperbolic latent geometry, Neural SDE coupling, one/few-step OT flow synthesis, differential-geometric interruption and low-rank continuous memory require independent mathematical and empirical qualification before production authority.

## Selection vector
Evaluate latency, semantic/task correctness, acoustic/prosody fidelity, tool reliability, memory/compute, concurrency, interruption quality, auditability, privacy, accessibility, provider availability and device/network constraints. Hard gates outrank weighted optimization.

## MLA / MTP law
MLA is architecture-specific; never prescribe it to a model that does not implement a compatible attention/cache architecture. MTP/speculative decoding is capability-specific and must be discovered/benchmarked. Neither is a generic server flag that automatically upgrades arbitrary models.

## Representation law
Text tokens, continuous embeddings, discrete acoustic codec units and continuous acoustic latents are representations with different tradeoffs. No representation is banned by ideology. Select and measure.

## Common fabric
All architectures remain subordinate to leeway-real-time-voice-multimodal-infrastructure: Media/Control/Cognitive/Evidence planes, generation epochs, bounded queues, playout ledger, privacy/authority gates, session recovery, adaptive profiles and Veritas.

## Anti-hallucination law
Published architecture examples are evidence for those systems, not proof that every provider or future model has the same internals.
