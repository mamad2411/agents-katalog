---
name: lemonslice-control-actions
description: Control sessions, trigger custom actions (like waving), and terminate.
license: MIT
---

# Lemon Slice Control Actions

## Official docs
- https://lemonslice.com/docs/reference/actions.md
- https://lemonslice.com/docs/api-reference/control-self-managed-session.md

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
You need to programmatically control an active avatar session, such as triggering specific custom motion sequences (actions) or terminating the avatar without dropping the underlying transport connection.

## Do not use this skill when
- You are trying to handle mute/unmute/interrupt logic. That is handled at the orchestration layer (LiveKit/Pipecat SDKs).
- The session is not yet active/ready.

## Agent workflow
1. **Verify Readiness:**
   - Always wait for the avatar to join and emit `bot_ready` before sending controls or actions to avoid race conditions.
2. **Triggering Actions (REST):**
   - Actions like `wave` or `celebrate` can be triggered explicitly via the control endpoint.
   - Use `POST /api/liveai/sessions/{session_id}/control` with the `X-API-Key` header.
   - Body format:
     ```json
     {
       "event": "pose-trigger",
       "pose_trigger": { "name": "<ACTION_NAME>" }
     }
     ```
3. **Triggering Actions (LiveKit LLM Tool Calls):**
   - Use LLM function calling to let the agent trigger actions contextually.
   - Example: `await self.trigger_action("wave")`
4. **Session Termination (Self-Managed):**
   - Use the same `POST .../control` endpoint but with the documented control event: `terminate`.
   - This cleanly stops the avatar generation without tearing down the underlying LiveKit or Daily room.
5. **Hosted Daily Hang-up:**
   - Hosted Daily uses the `force-end` app message for user hang-up.

## Common mistakes
- Sending control actions or pose triggers before the session is fully ready (before `bot_ready`).
- Confusing the `terminate` action (which stops the video generation) with closing the underlying LiveKit/Daily connection.

## Validation checklist
- [ ] Does the code verify session readiness (`bot_ready`) before issuing commands?
- [ ] Are custom actions triggered using the `pose-trigger` event schema?
- [ ] Is the `terminate` event used correctly for self-managed control?
