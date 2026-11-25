---
name: lemonslice-production-patterns
description: Make Lemon Slice integrations production-ready.
license: MIT
---

# Lemon Slice Production Patterns

## Official docs
- https://lemonslice.com/docs/reference/best-practices.md

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
You are reviewing, auditing, or finalizing a Lemon Slice integration and need to ensure it is secure, performant, and stable for production use.

## Do not use this skill when
You are just starting to build a prototype. Establish the core functionality using the specific integration skill first.

## Agent workflow
1. **Security Audit:**
   - Verify `LEMONSLICE_API_KEY` is completely absent from all client-side code (frontend frameworks, widget embeds in production).
   - Keep cleanup/termination guidance secure.
2. **Production Guidance from Docs:**
   - Budget latency carefully across your entire stack.
   - Optimize the STT/LLM/TTS pipeline.
   - Use Voice Activity Detection (VAD) effectively.
   - Always listen for `bot_ready` before interacting.
   - Handle avatar disconnect scenarios gracefully.
   - Handle room errors and catch pipeline errors.
   - Handle startup failures explicitly.
   - Set client-side startup timeouts (if `bot_ready` does not fire, fallback/retry).
   - Check idle timeout and GPU timeout configurations.
3. **Session Lifecycle Management:**
   - Timeouts vary by path. Best Practices lists idle timeout default 60s and GPU timeout default 30min; LiveKit docs also mention a 1-hour maximum session duration. Do not assume one timeout applies to every integration path.
   - Implement cleanup logic to terminate sessions.

## Common mistakes
- Exposing API keys in `.env.local` files that get bundled into Next.js/React frontend builds.
- Failing to issue cleanup/termination commands.
- Assuming arbitrary performance metrics (like 25 FPS or <3s response) instead of following latency budgeting guidelines.

## Validation checklist
- [ ] Is the API key perfectly secure and isolated?
- [ ] Are startup timeouts and `bot_ready` listeners implemented?
- [ ] Are error boundaries and disconnect handlers in place?
- [ ] Are idle/GPU timeouts explicitly configured?
