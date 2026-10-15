---
name: lemonslice-self-managed
description: Build with Lemon Slice as the avatar layer in a custom agent stack.
license: MIT
---

# Lemon Slice Self-Managed Pipeline

## Official docs
- https://lemonslice.com/docs/api-reference/create-self-managed-session
- https://lemonslice.com/docs/api-reference/get-self-managed-session

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
The developer owns the entire AI stack (STT, LLM, TTS) and wants to use Lemon Slice exclusively as the video generation layer.

## Do not use this skill when
- The developer wants Lemon Slice to handle the STT/LLM/TTS (use `lemonslice-hosted`).
- The developer is using LiveKit (use `lemonslice-livekit`).
- The developer is using Pipecat (use `lemonslice-pipecat`).

## Agent workflow
1. Ensure the API key (`LEMONSLICE_API_KEY`) is kept server-side.
2. Create a session using `POST /api/liveai/sessions`.
   - Provide `transport_type`. Allowed values: `livekit` or `daily`.
   - Provide avatar identity via EXACTLY ONE of `agent_id` or `agent_image_url`. Do not provide both.
   - You may include optional documented fields: `agent_prompt`, `agent_idle_prompt`, `idle_timeout`, `response_done_timeout`, `simulcast`.
3. Understand the session lifecycle statuses:
   - `QUEUED`
   - `ACTIVE`
   - `COMPLETED`
   - `TIMED_OUT`
   - `FAILED`
4. The backend should poll `GET /api/liveai/sessions/{session_id}` to check status if necessary.

## Common mistakes
- Using `/api/liveai/rooms/{session_id}` to check status instead of `/api/liveai/sessions/{session_id}`.
- Exposing the `LEMONSLICE_API_KEY` in frontend code.
- Providing both `agent_image_url` and `agent_id`. They are mutually exclusive.
- Using an undocumented `transport_type`.

## Validation checklist
- [ ] Is the session created using `POST /api/liveai/sessions`?
- [ ] Is `LEMONSLICE_API_KEY` only used securely on the backend?
- [ ] Is exactly ONE of `agent_image_url` or `agent_id` provided?
- [ ] Is the `transport_type` either `livekit` or `daily`?
