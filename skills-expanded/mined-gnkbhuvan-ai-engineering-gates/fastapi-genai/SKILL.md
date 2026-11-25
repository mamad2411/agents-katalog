---
name: fastapi-genai
description: |
  FastAPI implementation for generative AI services — the code/Python layer beneath
  `production-rag` and `agentic-ai`. Fires regardless of which LLM provider is involved
  (OpenAI, Anthropic, a self-hosted model, or any other) — the FastAPI/Python patterns are
  the same either way. Branches: build or serve a model-calling endpoint, stream a response
  token-by-token (SSE/WebSocket), define a type-safe request/response contract, persist
  conversation or usage data, add auth or AI-specific security (rate limiting,
  prompt-injection guardrails), cache or batch for cost/latency, test a non-deterministic
  endpoint, or containerize and deploy the service.
---

# FastAPI for GenAI Services

Implementation reference — this skill IS code-heavy and Python-specific, unlike
`production-rag` and `agentic-ai` which stay at the architecture level. Use those two to
decide *what* to build; use this one for *how* to build it in FastAPI.

## First-Principles Foundation

1. **Load once, reuse always**: load models/clients in a `lifespan` handler at startup, not
   per-request. Per-request loading is the single most common cause of needless latency in
   AI services.
2. **Async only end-to-end, or not at all**: declaring `async def` while calling a *sync*
   client inside it blocks the whole event loop — worse than just writing a sync `def` and
   letting FastAPI's thread pool handle it. Either use the provider's async client with
   `await` throughout, or stay synchronous.
3. **Stream anything large or slow**: token-by-token text, audio, video, big binaries. Use
   `StreamingResponse` (SSE) or a `WebSocket` rather than buffering a full response in
   memory and returning it all at once.
4. **Type everything with Pydantic**: request/response contracts, environment config, and —
   critically — the shape you're willing to accept *from* the LLM. A Pydantic model is a
   validation layer, an OpenAPI doc, and a contract enforcement mechanism in one.
5. **Treat the model as an untrusted, non-deterministic dependency**: gate any consequential
   action at the application layer, not in a prompt instruction; test behaviorally, not for
   exact output match; never let the model be the sole judge of its own output.
6. **Don't add infrastructure before you've measured you need it**: `BackgroundTasks` before
   a task queue, FastAPI's thread pool before a separate worker fleet, an in-memory or
   keyword cache before a semantic cache, the Postgres you already run before a new
   specialized store. Escalate only when a specific, measured bottleneck demands it.

## Trigger Decision Tree

1. **What's the request shape?** Single request/response, streaming, or a background job?
   → shapes everything else.
2. **Sync or async dependencies?** Decide before writing the route signature — mixing them
   wrongly is the most common bug class here (see axiom 2).
3. **Confirm missing details**—gate below; do not start implementing until it passes.
4. **Set up serving**: routing, Pydantic contracts, model/client loading →
   `references/project-setup-and-serving.md`, `references/type-safety.md`
5. **Streaming or background work needed?** → `references/concurrency-and-streaming.md`
6. **Needs persistence** (conversation history, usage tracking)? →
   `references/databases.md`
7. **Needs auth, or AI-specific hardening** (prompt injection, rate limiting)? →
   `references/auth-and-security.md`
8. **Expensive or high-volume enough to need caching/batching?** →
   `references/optimization-caching.md`
9. **Write the test plan alongside the implementation, not after** →
   `references/testing.md`
10. **Ship it** → `references/deployment.md`

### When Information Is Missing—Ask Before Building

| Missing? | Ask |
|---|---|
| Provider/model | "Which model/provider — OpenAI, Anthropic, a self-hosted model? Sync or streaming response?" |
| Persistence | "Does this need to remember anything across requests (conversation history, usage)?" |
| Auth | "Who's allowed to call this, and how should they authenticate?" |
| Load profile | "Roughly how many requests per minute, and is cost per request a concern?" |
| Deployment target | "Where does this run — a container platform, serverless, a VM with a GPU?" |

**Gate**: this step is done only when every row above that's actually unclear from context has either been answered by the user or stated out loud as an explicit assumption with no objection. Silently assuming and continuing does not satisfy this — stop and ask instead.

## Core Patterns Quick Reference

| Need | Pattern |
|---|---|
| Load a model/client once | `@asynccontextmanager` `lifespan` handler, store in a dict on `app.state` or module scope |
| Validate LLM output shape | Pydantic `BaseModel` + `Field` constraints; native structured-output mode if the provider supports it, prefill fallback otherwise |
| Stream text tokens to a browser | `StreamingResponse` with `media_type="text/event-stream"`, `data: ` prefix per chunk |
| Bidirectional chat | `WebSocket` with a connection manager; reconnect with exponential backoff client-side |
| Persist a streamed response | `BackgroundTasks.add_task` after the stream completes — don't hold a DB transaction open during streaming |
| Block a malicious/off-topic prompt | A guardrail check run concurrently with the main LLM call via `asyncio.wait(..., return_when=FIRST_COMPLETED)`, cancel the main call if it fails |
| Rate-limit by user, not just IP | Per-user key function on the limiter; IP-based alone is defeated by proxies/VPNs |
| Cache repeated/similar prompts | Keyword/exact-match cache first; escalate to semantic (embedding-similarity) cache only if hit rate on exact-match is low |
| Test a non-deterministic endpoint | Behavioral tests (readability/toxicity/length properties), not exact-string assertions |

## Deliverables

When delivering a FastAPI implementation, provide:

1. **The endpoint(s)** with Pydantic request/response models
2. **Model/client lifecycle** (how and when it's loaded, sync vs. async)
3. **Test coverage** appropriate to non-determinism (behavioral + integration, not just unit)
4. **Auth/rate-limiting** applied if the endpoint is exposed beyond local development
5. **A Dockerfile** (or note that one already exists and what changed)
6. **Known cost/latency characteristics** (which calls are cached, batched, or streamed, and why)

## References

| File | Topic | Load When |
|------|-------|-----------|
| `references/project-setup-and-serving.md` | Routing, dependency injection, lifespan model loading, middleware, model-serving strategies | Setting up a new service or endpoint |
| `references/type-safety.md` | Pydantic request/response contracts, validators, computed fields, structured LLM outputs | Designing the I/O contract for an AI endpoint |
| `references/concurrency-and-streaming.md` | Async rules, SSE, WebSocket, background tasks | Streaming responses or running anything concurrently |
| `references/databases.md` | Async SQLAlchemy, repository pattern, schema for conversations/usage, migrations | Persisting conversation history or usage data |
| `references/auth-and-security.md` | Basic/JWT/OAuth2 auth, RBAC/ABAC/ReBAC, prompt-injection guardrails, rate limiting | Exposing the service beyond local dev, or hardening against abuse |
| `references/optimization-caching.md` | Batch APIs, caching (keyword/semantic/context), quantization, fine-tuning trade-off | Cost or latency is a measured problem, not a guess |
| `references/testing.md` | Test strategy for non-deterministic endpoints, pytest patterns, test doubles, behavioral/integration/E2E tests | Writing or reviewing tests for an AI endpoint |
| `references/deployment.md` | Dockerfile patterns, image optimization, networking, Compose, GPU support, deployment-target comparison | Shipping the service |
