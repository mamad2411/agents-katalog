---
name: lemonslice-hosted
description: Create and manage Lemon Slice hosted sessions.
license: MIT
---

# Lemon Slice Hosted Pipeline

## Official docs
- https://lemonslice.com/docs/hosted/overview.md
- https://lemonslice.com/docs/api-reference/create-hosted-session

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
The developer wants Lemon Slice to handle the entire AI pipeline (STT, LLM, TTS, avatar), and the backend needs to create/manage these sessions.

## Do not use this skill when
- The developer is bringing their own STT/LLM/TTS (use `lemonslice-self-managed`, `lemonslice-livekit`, or `lemonslice-pipecat`).
- The developer only wants a simple web widget without a backend (use `lemonslice-widget`).
- You need to build the frontend Daily UI for the hosted session (use `lemonslice-hosted-daily`).

## Agent workflow
1. **Backend Session Creation:**
   - Call `POST /api/liveai/rooms` to create a hosted session.
   - Include `X-API-Key` in headers.
   - The creation body requires ONLY `agent_id` (unless official docs state otherwise). Do not pass unsupported fields like `agent_image_url`, `agent_prompt`, or `idle_timeout` unless explicitly verified.
2. **Handle Response:**
   - The response must include:
     - `room_url`
     - `token`
     - `image_url`
     - `session_id`
3. **Session Status:**
   - The statuses are:
     - `QUEUED`
     - `ACTIVE`
     - `COMPLETED`
     - `TIMED_OUT`
     - `FAILED`
4. **Handoff to Frontend:**
   - The backend must return the connection credentials to the frontend so it can join the Daily room.

## Common mistakes
- Using `/api/liveai/sessions` (Self-Managed) instead of `/api/liveai/rooms` (Hosted).
- Exposing the `X-API-Key` to the frontend to let the frontend create sessions. The backend must create the session.
- Sending unverified properties in the creation payload.

## Validation checklist
- [ ] Is the session created via `POST /api/liveai/rooms`?
- [ ] Is `agent_id` the primary required field used?
- [ ] Are all unsupported hosted fields removed from the payload?
