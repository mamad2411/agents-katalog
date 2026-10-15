---
name: lemonslice-hosted-daily
description: Build a Daily frontend for hosted Lemon Slice sessions.
license: MIT
---

# Lemon Slice Hosted Daily Frontend

## Official docs
- https://lemonslice.com/docs/hosted/integrations/daily-room-integration

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
You are building the frontend user interface for a Hosted Lemon Slice session, and the backend has already created the session and returned the Daily room credentials.

## Do not use this skill when
- You are trying to use Pipecat (use `lemonslice-pipecat`).
- You are writing the backend code to create the session (use `lemonslice-hosted`).
- You just want a simple drop-in website widget (use `lemonslice-widget`).

## Agent workflow
1. **Receive Credentials:** 
   - The frontend must request session credentials from the developer's backend.
   - It will receive `room_url` and `token`.
   - The frontend MUST NOT call the Lemon Slice API directly.
2. **Connect to Daily:**
   - Use Daily docs/patterns only where Lemon Slice docs explicitly support them.
3. **Event & State Management:**
   - Use `app-message` to listen for Lemon Slice events.
   - Treat `bot_ready` as the main active-call readiness signal.
   - Handle the following events/states:
     - `idle_timeout`
     - `daily_error`
     - `video_generation_error`
     - `participant-left`
4. **Startup Timeout Behavior:**
   - Implement logic so that if `bot_ready` does not fire within a threshold, the app leaves the room and shows a retry UI.

## Common mistakes
- Attempting to call Lemon Slice REST APIs directly from the React/frontend code to create the session.
- Treating participant-join as the readiness signal instead of listening for `bot_ready` via `app-message`.

## Validation checklist
- [ ] Does the frontend rely entirely on the backend for `room_url` and `token`?
- [ ] Is `bot_ready` used as the signal to transition to active?
- [ ] Is there a startup timeout implemented to show retry UI if `bot_ready` is delayed?
