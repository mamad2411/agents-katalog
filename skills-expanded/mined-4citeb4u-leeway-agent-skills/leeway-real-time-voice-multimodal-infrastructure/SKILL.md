---
name: leeway-real-time-voice-multimodal-infrastructure
description: Governed production skill for full-duplex real-time voice and multimodal agents: DSP/audio framing, WebRTC/RTP transport, VAD/turn detection, streaming STT/LLM/TTS pacing, deterministic barge-in/cancellation, playout accounting, adaptive vision sampling, telemetry, latency budgets and provider-agnostic execution.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  class: CROSS_HOUSE_REALTIME_INFRASTRUCTURE
  use-priority: HIGH_FOR_LIVE_VOICE_MULTIMODAL
  formula-tunnel: ADAPTED_V1
---
# LeeWay Real-Time Voice & Multimodal Infrastructure

## Mission
Build and diagnose low-latency full-duplex conversational systems without coupling Agent Lee identity to any STT, LLM, TTS, transport or vision provider.

## Required orchestration
PERCEPTION → MEDIA TRANSPORT → DSP/VAD → STT → TURN STATE → LLM STREAM → SYNTACTIC/PROSODIC CHUNKER → TTS STREAM → PLAYOUT LEDGER → AUDIO SINK, with an INTERRUPT BUS capable of cancelling every downstream stage.

## 1. Audio/DSP
Understand PCM/sample rate/bit depth/channels, resampling, framing, clock domains, gain/noise suppression/AEC where applicable, Opus packetization, timestamping, jitter, packet loss concealment and FEC. Frame dimensions are computed from sample rate and frame duration, never guessed.

## 2. Transport
Prefer WebRTC media paths for interactive browser/device audio/video when their RTP/SRTP, congestion, jitter and NAT traversal properties fit the task. WebRTC commonly uses ICE with STUN/TURN and secure RTP media. WebSockets remain valid for signaling/control or workloads where reliable ordered streams are preferable; never impose transport by slogan.

## 3. Turn-taking
Maintain explicit states such as LISTENING, USER_SPEAKING, ENDPOINT_PENDING, AGENT_THINKING, AGENT_SPEAKING, INTERRUPTING, RECOVERING. VAD acoustic evidence and semantic end-of-turn evidence are separate inputs. Silence/VAD thresholds are calibrated profiles, not universal constants.

## 4. Streaming STT
Track interim/final transcript stability, timestamps, revisions and confidence/evidence where available. Never feed an unstable interim transcript into irreversible actions.

## 5. Token-to-speech pacing
Use clause/prosody-aware streaming. Punctuation is one cue; also handle abbreviations, decimals, URLs, quoted text, numbers, acronyms, language-specific segmentation and maximum latency/word fallback. Voice output may require a speech-normalization layer rather than changing canonical text content.

## 6. Barge-in / cancellation
On validated user speech start during agent playout: locally suppress/flush interruptible playout first; propagate cancellation upstream to TTS and LLM generation; invalidate queued-but-unheard content; preserve only content actually rendered/heard in conversational state. Cancellation must be idempotent and race-safe.

## 7. Playout ledger
Track GENERATED_TEXT, TTS_ACCEPTED_TEXT, AUDIO_SYNTHESIZED, AUDIO_QUEUED, AUDIO_RENDERED_ESTIMATE and INTERRUPTED_AT. Conversation history uses the best evidence of what the user could actually have heard, not the complete generated response.

## 8. Multimodal vision
Decouple audio and vision clocks. Use adaptive semantic keyframing: scene change, motion, OCR/UI change, task relevance, user pointing/gesture or explicit request can increase sampling; stable scenes can reduce it. Fixed 1–2 FPS is a profile, not a law.

## 9. Latency
Measure per-stage distributions, not only averages: ingest/network, jitter buffer, VAD/endpointer, STT first/final useful text, LLM TTFT/token rate, chunker dwell, TTS TTFB/RTF, playout queue, interruption spill, total response onset. Latency targets are product/device/network profiles and require empirical calibration.

## 10. Queueing/pacing invariants
Use critical-path DAG timing, Little's Law only where its stationarity assumptions are justified, and real-time-factor/audio-duration measurements for synthesis pacing. Smooth playout requires adequate production margin plus bounded jitter buffering; an average rate alone does not guarantee no underrun.

## 11. Provider abstraction
STT, LLM, TTS, VAD, transport, audio sink and vision sampler are capability interfaces. Providers are replaceable and cannot redefine LeeWay authority.

## 12. Formula/LFEA
All thresholds/equations must declare claim class, units, domains, assumptions and validation state. Candidate latency/VAD/pacing formulas route through Formula Factory/LFEA before canonical promotion.

## 13. Veritas acceptance
At minimum test: first-response latency distribution; sustained playout underruns; packet loss/jitter scenarios; barge-in spill; cancellation races; duplicate/late events; transcript revision; TTS failure/recovery; network handoff/TURN fallback where relevant; AEC/feedback; provider timeout; visual sampling load; context correctness after interruption.

## Heavy-use routing
For local Windows playback of prepared assistant replies, use the bounded [Read Aloud adapter](../read-aloud/SKILL.md). It includes executable voice selection, rate control, cancellation and WAV output. Persistent accessibility preferences belong in the host's startup instructions. The adapter does not inherit untested streaming, microphone, or acoustic guarantees from this architecture skill.

Use this skill by default for: Agent Lee live voice, phone receptionist, receptionist/front counter agents, avatar employees, accessibility/read-aloud, live phone calls, Device Bridge voice, two-way audio, live screen/camera assistants, streaming TTS/STT, barge-in, WebRTC diagnostics and multimodal low-latency systems.

## Evidence law
Configured != proven; streaming != low latency; cancellation requested != downstream silence; audio generated != audio heard; transport connected != healthy; model output != proof.


## 14. Formula Tunnel four-plane architecture

### Media Plane
Capture, DSP, AEC/noise suppression/gain control when applicable, resampling, codec/packetization, media transport, STT/TTS media streams and playout. Media timestamps must preserve clock-domain identity.

### Control Plane
Session/signaling, connectivity state, provider capability negotiation, state transitions, interrupt epochs, cancellation propagation, bounded queues/backpressure, reconnect, codec/provider changes and stale-event rejection.

### Cognitive Plane
Semantic endpointing, context construction, LLM streaming, speech normalization, prosody/chunk planning, adaptive visual relevance and conversation-state reconciliation.

### Evidence Plane
Monotonic timestamps, stage spans, queue occupancy, packet/jitter/loss evidence, playout ledger, interruption trace, provider identity/version, Formula/LFEA state, privacy/authority state and receipt references.

## 15. Interrupt epochs and stale work
Every response generation receives a monotonically increasing generation/interrupt epoch. Barge-in invalidates the current epoch before upstream cancellation. Audio/text/events arriving from an invalid epoch are dropped even if a provider ignores or races cancellation. Cancellation requested != cancellation completed.

## 16. Backpressure and bounded buffers
Every queue has an explicit capacity, age limit and overflow policy. Never allow latency to grow silently by accumulating audio/text/video. Under overload, degrade deliberately: reduce vision sampling, shorten context, change chunking/provider profile, shed nonessential work or fail visibly according to authority.

## 17. Clock, device and acoustic state
Track capture clock, server monotonic clock and playout/device clock where observable. Measure drift rather than assuming synchronized clocks. Account for audio-route changes, focus/permission loss, Bluetooth/telephony path changes, device thermal/power throttling and codec renegotiation.

Echo cancellation/feedback behavior is part of duplex qualification. VAD confidence is not trusted as user speech evidence when playback echo is unresolved.

## 18. Session continuity and recovery
Model CONNECTING, CONNECTED, DEGRADED, RECONNECTING and CLOSED session states independently from conversational turn state. Reconnect must preserve only evidence-backed conversational state and reject stale packets/generations from the prior transport epoch.

## 19. Privacy, consent and authority
Microphone/camera capture, recording, retention, speaker identification/voice cloning and telephony actions require applicable user/platform authorization. Privacy/authority violations are hard gates and cannot be traded against latency or quality.

## 20. Rendered vs heard truth
AUDIO_RENDERED_ESTIMATE means evidence that samples reached the observable playout boundary. It does not prove the human heard them. Use acoustic loopback/return evidence when available; otherwise preserve the distinction as uncertainty.

## 21. Adaptive Formula policy
VAD/endpointer thresholds, jitter buffer, chunk size, vision sampling, provider choice and degradation policy may adapt to measured device/network/speaker conditions. Adaptation is bounded by Formula/LFEA profiles and must preserve the selected profile/version/evidence.

## 22. Capability graduation
Verified device, network, speaker and provider profiles may seed future sessions. Reuse is conditional on matching identity/context/version evidence; do not blindly transfer calibration across devices, microphones, networks, languages or providers.

## 23. Formula Tunnel questions
For every significant voice/multimodal design or failure ask: What are we not discovering? What needs enhancement? What can become deterministic? What requires physical measurement? What existing Skill Houses/tools should compose? What failure state has not been simulated? What knowledge can be graduated so the next execution starts above zero?
