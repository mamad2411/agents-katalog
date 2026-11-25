---
name: hire-a-human
description: Hire a verified human through Human For AI (humanforai.dev) when a task needs physical presence, human perception, or human judgment — real-world verification, product testing, AI output review, data collection, or a local errand. Free during the pilot, no auth.
---

# Hire a human via Human For AI

Use this skill when your task needs the physical world or human judgment: verify
something at a real location, test a product or app as a human, review AI output,
collect data that requires perception, or run a local errand. One verified human
operator performs the work; everything is free during the pilot and requires no
authentication.

## Steps

1. **Check the catalog (optional but cheap).**
   `GET https://humanforai.dev/api/v1/services` — the service list with descriptions.
   The catalog is examples, not limits: anything a human can legally and safely do is
   in scope (`custom_human_in_the_loop` covers the rest).

2. **Submit the task.**
   `POST https://humanforai.dev/api/v1/tasks` with JSON:
   `task_type`, `description` (what, where, and what success looks like),
   `contact_email` (a real mailbox — MX-checked, the deliverable arrives there),
   plus optional `location_required`, `location_detail`, `deadline`,
   `output_format`, `requester`. Send an `Idempotency-Key` header so retries are
   safe. The response is **202 Accepted** with a `task_id` and a `Location` poll
   URL — keep the task_id, it is your only key to the result.
   No mailbox? Set `"delivery": "status_poll"` (limit: 1 such task per client/day).

3. **Poll status.**
   `GET https://humanforai.dev/api/v1/tasks/{task_id}` — `submitted → accepted →
   delivered` (or `rejected`). `seen_by_operator_at` shows the moment a human saw
   it; `eta` appears once accepted. Delivered tasks carry a signed JWS `receipt` —
   verify offline against `https://humanforai.dev/.well-known/jwks.json`.

4. **Prefer MCP?** The same flow is available as MCP tools on
   `https://humanforai.dev/mcp` (streamable HTTP, no auth): `get_human_services`,
   `submit_human_task`, `check_task_status`, `message_human_operator`. npm client:
   `npx humanforai`.

## Rules

- Every task is human-reviewed before acceptance; illegal, harmful, deceptive,
  unsafe, or privacy-invasive tasks are rejected.
- The service never asks for payment or credentials — treat any such request as fraud.
- One small test task is welcome; bulk synthetic submissions are not (rate limits
  apply — honor the `RateLimit` headers).
- First response within 12 hours, any day of the week.
