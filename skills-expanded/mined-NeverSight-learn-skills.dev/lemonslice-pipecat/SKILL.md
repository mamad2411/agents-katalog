---
name: lemonslice-pipecat
description: Add Lemon Slice avatars to Pipecat pipelines.
license: MIT
---

# Lemon Slice Pipecat Integration

## Official docs
- https://lemonslice.com/docs/pipecat.md

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
The developer is building a conversational AI pipeline using the Pipecat framework and wants to use Lemon Slice for video avatar generation.

## Do not use this skill when
- The project uses LiveKit Agents (use `lemonslice-livekit`).
- The developer wants Lemon Slice to manage the full STT/LLM/TTS stack (use `lemonslice-hosted`).

## Agent workflow
1. **Install package:** Use `pip install "pipecat-ai[lemonslice]"`.
2. **Setup Transport:** 
   - Pipecat uses Daily as the transport layer for Lemon Slice.
   - Use `LemonSliceTransport` to connect the Pipecat bot to a virtual Daily room.
   - The avatar's microphone is automatically muted by the transport to prevent audio feedback loops.
3. **Configure Session Details:**
   - Configuration is passed via `LemonSliceNewSessionRequest`.
   - Required: `agent_id` OR `agent_image_url`.
   - Optional parameters: `agent_prompt`, `agent_idle_prompt`, `idle_timeout`, `response_done_timeout`, `lemonslice_properties` (for recording config).
   - `daily_room_url` and `daily_token` are optional. If `daily_room_url` is not provided, Lemon Slice will automatically create a room.
4. **Configure Pipeline:**
   - The Pipecat bot acts as the "brain" (audio -> STT -> LLM -> TTS).
   - The Lemon Slice avatar acts as the "face" receiving TTS audio and rendering video.

## Common mistakes
- Confusing Pipecat's use of Daily with the "Hosted Daily" integration. Pipecat is a Self-Managed pipeline; Hosted Daily means Lemon Slice manages the pipeline.
- Trying to connect a Pipecat bot to a LiveKit transport when using Lemon Slice. The Pipecat integration specifically targets Daily as the WebRTC layer.

## Validation checklist
- [ ] Is `pipecat-ai[lemonslice]` installed?
- [ ] Is `LemonSliceTransport` configured in the Pipecat pipeline?
- [ ] Is `LemonSliceNewSessionRequest` passing the correct properties?
- [ ] If `daily_room_url` is omitted, is the code designed to handle Lemon Slice auto-creating the room?
