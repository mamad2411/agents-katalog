---
name: leeway-acoustic-coprocessor-fabric
description: Formula-governed model/device/system-agnostic voice coprocessor architecture using capability-negotiated universal voice events, replaceable acoustic engines, portable interruption/control, AEC/double-talk handling, platform adapters and evidence.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  class: CROSS_PLATFORM_ACOUSTIC_COPROCESSOR
  formula-funnel: ASC_V1_ADAPTED
---
# LeeWay Acoustic Coprocessor Fabric

## Core law
Agnosticism is achieved by stable external contracts and capability negotiation, not by assuming arbitrary model hidden states, token vocabularies, probability vectors or embeddings are interchangeable.

## Universal Voice Bus — minimum and optional surfaces
Minimum portable event: TEXT_DELTA with monotonic/session timestamp, generation epoch, provider/model provenance and cancellation identity.
Optional negotiated events: TOKEN_LOGPROBS, SEMANTIC_EVENT, TOOL_EVENT, PHONEME_EVENT, PROSODY_EVENT, AUDIO_EMBEDDING, AUDIO_CODEC_UNIT, NATIVE_AUDIO_CHUNK, VISION_EVENT, CONFIDENCE_EVENT.

A provider adapter advertises exactly what it can emit/accept. Missing optional capability remains missing; never synthesize evidence.

## Model paths
Text-only/closed models use speech normalization + phoneme/prosody planning + selected TTS engine.
Native speech models may preserve their native acoustic path while still publishing control/evidence/tool side channels.
Continuous/flow-matching engines are selectable only when qualified by Formula Factory.

## Semantic alignment
Unit normalization does not create cross-model semantic invariance. If a shared semantic space is required, use a single shared encoder or explicitly calibrated alignment with anchors and measured retrieval/alignment error.

## Acoustic coprocessor
Owns portable audio framing, resampling contracts, AEC/double-talk subsystem, bounded ring buffers, playout ledger, interrupt epochs, backpressure, speech engine interface and platform source/sink adapters. It does not own Creator authority, conversation truth, tool authorization or privacy policy.

## Barge-in
Do not use instantaneous mic-vs-speaker cosine divergence as the sole detector. Use delay-aware AEC residual and calibrated double-talk evidence (e.g. coherence/correlation and/or neural near-end detector) plus conversational/VAD evidence. Invalidate generation epoch before attempting provider cancellation and local sink flush.

## Platform agnosticism
Portable core + adapters. Web/browser, Windows, Linux, Android, Apple and telephony surfaces have different audio APIs, permissions, scheduling and buffer semantics. No Python-only implementation is called universally device-agnostic.

## Flow/continuous engine
Hyperspherical conditioning, splines, OT-CFM, continuous latent audio and few-step solvers remain pluggable Formula Factory candidates. Qualification must measure NFE-quality, latency, power, memory, speaker/prosody fidelity and causal streaming behavior against cascaded/native baselines.

## Capability graduation
Persist verified provider/device/network/acoustic profiles by identity/version. Reuse only when compatibility evidence matches.

## Funnel questions
Before architecture or repair ask all mandatory Formula Funnel discovery questions in config/formula-lab/asc-formula-funnel-v1.json.
