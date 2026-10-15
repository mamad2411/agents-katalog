---
name: lemonslice-api-reference
description: Use Lemon Slice REST APIs correctly.
license: MIT
---

# Lemon Slice API Reference

## Official docs
- https://lemonslice.com/docs/reference/overview.md

## Use this skill when
> **Guardrail:** Use only after `lemonslice-integration-choice` has explicitly selected this path.
You need to call raw Lemon Slice REST endpoints for session creation, status polling, or metadata retrieval from a backend environment.

## Do not use this skill when
- You are trying to make API calls from a frontend browser environment (never expose the API key).
- You are using the LiveKit plugin or Pipecat, which abstract most of these API calls internally.

## Agent workflow
1. **Base Configuration:**
   - Base URL: `https://lemonslice.com/api`
   - Authentication: Add the `X-API-Key` header to all requests.
2. **Identify the correct endpoint family:**
   - **Self-Managed:** strictly uses `/liveai/sessions`
   - **Hosted/Widget rooms:** strictly uses `/liveai/rooms`
   - Do NOT mix these endpoint families.
3. **Creation Endpoints:**
   - **Hosted:** `POST /api/liveai/rooms`
     - Response exact fields: `room_url`, `token`, `image_url`, `session_id`
   - **Self-Managed:** `POST /api/liveai/sessions`
     - Response exact fields: `session_id`
4. **Other Documented Endpoints:**
   - Include `GET` (status/metadata), `LIST` (if documented without generic pagination limits), and `POST .../control` (control) endpoints.

## Common mistakes
- Sending both `agent_id` and `agent_image_url`.
- Mixing up `/liveai/sessions` and `/liveai/rooms`.

## Validation checklist
- [ ] Are requests hitting the correct base URL (`https://lemonslice.com/api`)?
- [ ] Is the `X-API-Key` header present?
- [ ] Are Self-managed and Hosted endpoints strictly segregated?
- [ ] Do the creation responses match the exact documented fields?
