---
name: harden-llm-app-reliability
description: Hardens LLM API calls for production with per-call timeouts and cancellation, exponential-backoff-plus-full-jitter retries on 429/500/529 that honor Retry-After, model fallback, one-round structured-output repair, refusal/stop_reason handling, and a circuit-breaker degraded mode so a flaky provider never breaks the feature.
when_to_use: Shipping an LLM feature where provider errors, timeouts, rate limits, or refusals must not crash the UX. Distinct from optimize-llm-cost-latency (speed/spend), defend-llm-prompt-injection (security of inputs), and rate-limiting (protecting your own API from callers, not surviving a provider's limits).
---

## When to Use

Reach for this skill when the failure mode you fear is **the provider**, not your code or your callers:

- "The model call sometimes hangs / times out and the request just spins forever"
- "We get 429s / 529s / 500s in bursts and the feature errors out"
- "Wrap the LLM call so a bad response or refusal degrades gracefully instead of throwing"
- "Add fallback to a cheaper/other model when the primary is down or refuses"
- "JSON-mode output is occasionally malformed and crashes the parser"
- "Mid-stream the connection drops and the user sees half an answer"

NOT this skill:
- Making calls *cheaper or faster* (model routing for cost, prompt caching, token trimming) → optimize-llm-cost-latency
- Defending the prompt against injection / untrusted-content attacks → defend-llm-prompt-injection
- Limiting how often *your callers* hit *your* API (token bucket, quotas, your own 429s) → rate-limiting
- Designing the prompt + structured-output schema itself → prompt-engineering
- Measuring output quality across prompt/model changes → llm-eval-harness
- Offloading the whole LLM job to a durable background queue with DLQ → message-queue-jobs

This skill is the resilience wrapper *around* one logical LLM call. It assumes the prompt is already written.

## Steps

1. **Wrap every call in a timeout + cancellation token. No naked `await`.** A hung socket must die on a deadline you own, not the SDK default (often 600s+). Two clocks: a per-attempt timeout (the request) and a total deadline (all retries combined). Stream long calls so the per-attempt timeout measures *time-to-first-byte*, not total generation.

   ```ts
   const TOTAL_DEADLINE_MS = 30_000;   // whole operation, retries included
   const PER_ATTEMPT_MS    = 12_000;   // one HTTP attempt (TTFB for streams)

   // remainingMs = total deadline left for this attempt (computed by the caller, step 2)
   async function callWithDeadline(fn, remainingMs) {
     const ctrl = new AbortController();
     const budget = Math.max(0, Math.min(PER_ATTEMPT_MS, remainingMs));
     const t = setTimeout(() => ctrl.abort(), budget);
     try { return await fn(ctrl.signal); }
     finally { clearTimeout(t); }
   }
   ```
   Pass `signal` into the SDK (`client.messages.create({...}, { signal })`). On the user side wire the inbound request's abort signal through so a closed browser tab cancels the upstream call instead of burning tokens.

2. **Retry only what's retryable, with exponential backoff + full jitter, and honor `Retry-After`.** Classify the error before you retry — retrying a 400 is just slower failure.

   | Status / condition | Retry? | Wait |
   |---|---|---|
   | 429 rate-limited | Yes | `Retry-After` header if present, else backoff |
   | 529 overloaded (Anthropic) / 503 | Yes | backoff + jitter |
   | 500 / 502 / 504 / gateway | Yes | backoff + jitter |
   | Network reset / timeout / ECONNRESET | Yes | backoff + jitter |
   | 408 request timeout | Yes | backoff |
   | 400 / 422 bad request | **No** | fix the request, not the retry |
   | 401 / 403 auth | **No** | rotate key / fix scope |
   | 413 too large | **No** | trim input |
   | Refusal / `stop_reason` | **No retry — fall back** (step 4) | — |

   Defaults: **max 4 attempts**, base 500ms, cap 8s, **full jitter** (`sleep = random(0, min(cap, base * 2**attempt))`). Full jitter beats fixed/equal backoff because synchronized clients (a 429 storm) otherwise retry in lockstep and re-stampede. Always clamp the wait to the remaining total deadline — never sleep past it.

   ```ts
   const start = Date.now();
   const elapsed = () => Date.now() - start;
   for (let attempt = 0; attempt < 4; attempt++) {
     try { return await callWithDeadline(fn, TOTAL_DEADLINE_MS - elapsed()); }
     catch (e) {
       if (!isRetryable(e) || attempt === 3 || elapsed() > TOTAL_DEADLINE_MS) throw e;
       const ra = retryAfterMs(e);                       // parse header, seconds or http-date
       const backoff = Math.random() * Math.min(8000, 500 * 2 ** attempt);
       await sleep(Math.min(ra ?? backoff, TOTAL_DEADLINE_MS - elapsed()));
     }
   }
   ```
   LLM calls are **non-idempotent and billed** — a retry after a *partial* success double-charges. Only retry attempts that demonstrably failed before producing a usable response (connection error, non-2xx, timeout-before-first-byte). Never retry a call that already streamed a full body.

3. **Validate structured output; repair once; then fail safe — never crash on malformed JSON.** When you asked for JSON, do not feed the raw model string straight into `JSON.parse` + a schema and let it throw to the user.
   - Parse → validate against the schema (Zod / Pydantic / JSON Schema).
   - On failure, **one** repair round: send the model the broken output + the validator error, ask for corrected JSON only. Strip code fences and prose first.
   - Still invalid → return a typed safe default (e.g. `{ status: "unavailable" }`) or route to degraded mode. Log the raw output. Do **not** loop repairs (cost + latency blowup).

   Prefer the SDK's native enforcement (tool/`tool_choice` forcing, strict JSON mode) over free-text + regex — it eliminates most repairs. Repair is the safety net, not the plan.

4. **Fall back to another model on persistent failure or refusal.** When the primary is exhausted (retries spent, circuit open) or returns a refusal, try a fallback before giving up. Order by capability-then-availability, e.g. primary Sonnet → fallback Haiku, or cross-provider if you run multi-vendor.
   - A **refusal** (`stop_reason: "refusal"`, or the model declining) is not a transport error — do not retry the same model; either fall back or return the refusal as a first-class result.
   - Treat `stop_reason: "max_tokens"` as a *truncated* (not failed) result: the JSON is incomplete — repair or raise `max_tokens` and retry once, don't ship the cutoff.
   - Cap fallback depth at 1–2 models. Record which model actually served the response.

5. **Stream with a heartbeat; discard partials on mid-stream error.** Long generations should stream so the user sees progress and you detect stalls. Set an **inter-chunk idle timeout** (e.g. 20s with no new token → abort) — a stream can hang open without erroring. If the stream errors or aborts mid-way, **discard the accumulated partial** and either retry from scratch (step 2 rules) or degrade; never persist or render a half-message as if complete. Buffer to a scratch variable and only commit on the terminal `message_stop`.

6. **Circuit-breaker around the provider → degraded mode.** Per-provider breaker: after N consecutive failures (e.g. 5) or a failure rate over a window, **open** the circuit and stop calling for a cooldown (e.g. 30s), then **half-open** one probe. While open, skip the doomed call and serve degraded mode immediately: a cached previous answer, a canned/templated response, or a clear "this feature is temporarily unavailable" — chosen per feature, decided *before* the incident. This stops a provider outage from turning into 30s timeouts on every request and exhausting your own connection pool.

7. **Never lose user input on failure.** Before the call, persist the user's prompt/turn so any failure path (timeout, all-retries-exhausted, circuit open) returns a retryable state, not a black hole. The user should be able to resend with one tap, or the system auto-resumes — input is never silently dropped. For expensive multi-step agent runs, checkpoint so you resume from the failed step, not step 1.

## Common Errors

- **Relying on the SDK default timeout.** It's often minutes. A spike of hung sockets exhausts your connection pool and takes the whole service down. Set an explicit per-attempt timeout you own.
- **Retrying non-retryable errors.** Looping on a 400/401/413 wastes the deadline and (for auth) can lock the key. Classify first; only retry 408/429/5xx/network.
- **Fixed or equal-jitter backoff.** All clients that got 429'd retry at the same instant and re-stampede the provider. Use full jitter: `random(0, min(cap, base·2^n))`.
- **Ignoring `Retry-After`.** The provider told you exactly when to come back; backoff math that retries sooner just earns another 429. Parse the header (seconds *or* HTTP-date) and prefer it.
- **Retrying a partially-streamed call.** It already cost tokens and may have half-applied a side effect; the retry double-charges and can double-act. Only retry failures that occurred before a usable response.
- **`JSON.parse` straight onto the response.** One malformed token throws an unhandled exception to the user. Always validate, repair once, then fail to a typed default.
- **Infinite repair loop.** Re-asking the model until JSON is valid can run forever and 10x the bill. Exactly one repair round, then degrade.
- **Treating a refusal as a 5xx.** Retrying the identical prompt on the same model just refuses again. Fall back or surface it; don't burn retries.
- **Shipping a `max_tokens` cutoff as complete.** Truncated JSON silently corrupts downstream. Check `stop_reason`; repair or re-call with higher limit.
- **Rendering the mid-stream partial.** A dropped stream leaves a half-answer the user reads as final. Buffer and only commit on `message_stop`; discard on error.
- **No circuit breaker.** During a provider outage every request pays the full timeout × retries before failing — your latency and pool collapse. Trip the breaker and serve degraded mode fast.
- **Dropping user input on the failure path.** The user retypes everything. Persist the turn before the call; make every failure resumable.
- **Sharing one breaker/timeout budget across unrelated features.** A flaky batch job opens the circuit for your latency-critical chat path. Scope breakers per provider+route.

## Verify

Prove resilience with **fault injection**, not hope. Force each failure and assert the wrapper holds — don't wait for prod to hit them.

1. **Forced 429 storm:** Stub the client to return `429` with `Retry-After: 2` for the first 3 calls, then `200`. Assert: exactly 4 attempts, waits honor `Retry-After` (≈2s, not the backoff curve), final result returned, total stays under the deadline.
2. **Forced timeout:** Stub a response slower than `PER_ATTEMPT_MS`. Assert: the attempt aborts at the deadline (not the SDK default), the `AbortController` fired, and either a retry or a clean degraded response — never a hang.
3. **Non-retryable:** Stub a `400`. Assert: **zero** retries, immediate failure, deadline barely consumed.
4. **Malformed JSON:** Stub output that fails the schema, then valid on the repair call. Assert: exactly one repair round, valid object returned. Then stub it invalid twice → assert the typed safe default, no thrown exception.
5. **Refusal / cutoff:** Stub `stop_reason: "refusal"` → assert fallback model is tried (no same-model retry). Stub `stop_reason: "max_tokens"` → assert truncation is detected, not shipped as complete.
6. **Mid-stream drop:** Start a stream, kill the connection after 2 chunks. Assert: the partial is discarded (not rendered/persisted), and retry-or-degrade fires.
7. **Circuit breaker:** Force N consecutive failures → assert the circuit opens, subsequent calls return degraded mode **immediately** (no timeout wait), then half-open probes and closes on recovery.
8. **Input preservation:** Trigger total failure → assert the user's input is still retrievable/resumable, returned as retryable state, never silently lost.
9. **Idempotency/billing:** Assert a fully-streamed-then-errored response is **not** retried (no double charge).

Done = fault-injection tests 1–9 pass, every LLM call has an explicit per-attempt timeout + total deadline, retries use full-jitter backoff that honors `Retry-After` and never fires on non-retryable or already-served calls, malformed/refused/truncated output degrades to a typed safe path instead of throwing, the circuit breaker serves degraded mode under a forced outage without paying timeouts, and no failure path loses user input.
