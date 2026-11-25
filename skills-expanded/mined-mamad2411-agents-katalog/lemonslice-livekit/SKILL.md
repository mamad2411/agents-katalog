---
name: lemonslice-livekit
description: Add Lemon Slice avatars to LiveKit Agents.
license: MIT
---

# Lemon Slice LiveKit Integration

## Official docs
- https://lemonslice.com/docs/livekit.md

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
The developer is building a voice AI agent using the LiveKit Agents framework and wants to add a Lemon Slice avatar video track.

## Do not use this skill when
- The project does not use LiveKit.
- The project uses Pipecat (use `lemonslice-pipecat`).
- The developer wants a hosted session (use `lemonslice-hosted`).

## Agent workflow
1. **Detect language:** Identify if the project is Python or Node.js.
2. **Install package:**
   - Python: `pip install "livekit-agents[lemonslice]"`
   - Node.js: `npm install @livekit/agents-plugin-lemonslice` (or `pnpm add` - exactly as documented in the LiveKit Node.js tab)
3. **Configure Avatar Session:**
   - Ensure the API key (`LEMONSLICE_API_KEY`) is kept server-side.
   - Initialize `lemonslice.AvatarSession` with `agent_image_url` or `agent_id`.
   - Configure optional parameters: `agent_prompt`, `agent_idle_prompt`, `idle_timeout`, `simulcast`.
   - **Important:** When using the Gemini Live S2S model for realtime interactions, set `response_done_timeout=0.8` to handle end of responses correctly.
4. **Start Session:**
   - Await the `start()` method on the avatar, passing the LiveKit session and room context (e.g., `await avatar.start(session, room=ctx.room)`).
5. **Handle lifecycle & Events:**
   - Participant join is not enough; wait for `bot_ready` as the explicit readiness signal over the data channel.
   - Listen for events over the data channel:
     - `bot_ready`
     - `idle_timeout`
     - `error`
     - `video_generation_error`
     - `metric`
   - Gracefully disconnect the room or send the `terminate` control action to shut down the avatar.

## Common mistakes
- Trying to manually call Lemon Slice REST APIs to create the session. The LiveKit plugin handles session creation internally.
- Putting the `LEMONSLICE_API_KEY` in the frontend client. It must remain in the backend/agent server environment variables.
- Treating standard participant join as readiness instead of waiting for `bot_ready`.

## Validation checklist
- [ ] Is the correct, officially documented LiveKit plugin installed?
- [ ] Is `LEMONSLICE_API_KEY` in the server environment?
- [ ] Is the code waiting for the `bot_ready` signal before assuming readiness?
- [ ] If using Gemini Live S2S, is `response_done_timeout=0.8` set?
