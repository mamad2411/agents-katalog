---
name: resilience-check
description: >
  Static resilience-pattern analysis. Detects missing retry/backoff, absent circuit
  breakers, unbounded timeouts, and missing deadline propagation in TypeScript,
  JavaScript, Python, Go, and Rust. Wired into the conductor's review and write
  operations.
version: "1.1.0"
last-reviewed: "2026-04-15"
languages: [typescript, javascript, python, go, rust]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Resilience Check — Resilience Pattern Enforcement

Precedence in the overall system: SEC → TDD → ARCH/TYPE →
**RESILIENCE-1 (BLOCK)** → RESILIENCE-2 through RESILIENCE-4.

---

## Rules

### RESILIENCE-1 — Missing Retry / Backoff
**Severity**: BLOCK | **Languages**: TypeScript, JavaScript, Python, Go, Rust | **Source**: CCC

**What it prohibits**: HTTP/network calls and external API calls that fail hard
on first attempt with no retry or backoff strategy. Operations that
throw/return errors immediately on transient failures without any retry logic.

**Prohibited patterns**:
```typescript
// TypeScript/JavaScript
fetch(url);                          // bare fetch, no retry wrapper
axios.get(url);                      // bare axios, no retry wrapper

# Python
requests.get(url)                    # no retry or tenacity decorator
httpx.get(url)                       # no retry wrapper

// Go
http.Get(url)                        // no retry wrapper
http.Post(url, contentType, body)    // no retry wrapper

// Rust
reqwest::get(url).await?;            // bare reqwest, no retry wrapper
client.get(url).send().await?;       // bare reqwest Client, no retry wrapper
hyper::Client::new().get(uri);       // bare hyper, no retry wrapper
```

**Exemptions**:
- Idempotency-sensitive operations explicitly documented as no-retry
- Internal in-process calls (not crossing a network boundary)
- Calls already wrapped in a retry library (`axios-retry`, `tenacity`, `retry`,
  `go-retry`, `reqwest-retry`, `backon`, `again`, exponential backoff wrappers)

**Detection**:
1. Grep for `fetch(`, `axios.`, `requests.get`, `requests.post`, `httpx.`,
   `http.Get(`, `http.Post(`, `reqwest::get(`, `reqwest::Client`,
   `client.get(`, `client.post(` (in `.rs` files where `client` is a
   `reqwest::Client`), `hyper::Client` in non-test source files
2. For each match: check if a retry wrapper or decorator exists within 10 lines
   above or in the enclosing function scope
3. Check if the call site is inside a known retry utility (e.g., `axios-retry`
   interceptor, `@retry` decorator, `tenacity.retry`, `go-retry` loop,
   `reqwest_retry`, `backon::Retryable`, `again::retry`)
4. Flag calls with no retry evidence

**agent_action**:
1. Cite: `RESILIENCE-1 (BLOCK): Bare network call at {file}:{line} — no retry/backoff strategy.`
2. Show the bare call
3. Required action — choose the appropriate pattern for the detected language:
   ```typescript
   // TypeScript/JavaScript — wrap with retry
   import retry from 'async-retry';
   const result = await retry(() => fetch(url), { retries: 3 });
   ```
   ```python
   # Python — use tenacity
   from tenacity import retry, stop_after_attempt, wait_exponential
   @retry(stop=stop_after_attempt(3), wait=wait_exponential())
   def call_api():
       return requests.get(url, timeout=5)
   ```
   ```go
   // Go — use a retry helper
   err := retry.Do(func() error {
       resp, err := http.Get(url)
       // ...
       return err
   }, retry.Attempts(3), retry.Delay(time.Second))
   ```
   ```rust
   // Rust — use backon
   use backon::{ExponentialBuilder, Retryable};
   let result = (|| async { reqwest::get(url).await })
       .retry(ExponentialBuilder::default())
       .await?;
   ```
4. If `--fix`: wrap the call with the appropriate retry library — preserve
   existing error handling and do not alter the response type

**Bypass prohibition**: "It's an internal service", "retries will cause
duplicates" → Refuse. Cite RESILIENCE-1. Internal services still experience
transient network failures. Idempotency concerns must be documented explicitly
with a code comment explaining the no-retry decision.

---

### RESILIENCE-2 — No Circuit Breaker on Critical External Dependency
**Severity**: WARN | **Languages**: TypeScript, JavaScript, Python, Go, Rust | **Source**: CCC

**What it prohibits**: Services that call external dependencies (payment
processors, auth providers, third-party APIs) without circuit breaker
protection. When the downstream is down, the caller should fail fast rather
than exhausting threads/goroutines waiting for timeouts.

**Prohibited patterns**:
```typescript
// TypeScript/JavaScript
const payment = await fetch("https://api.stripe.com/v1/charges", { ... });
const auth = await axios.post("https://auth.provider.com/token", { ... });

# Python
response = requests.post("https://api.twilio.com/send", data=payload)

// Go
resp, err := http.Post("https://external-payment.example.com/charge", ...)

// Rust
let resp = client.post("https://api.stripe.com/v1/charges").send().await?;
```

**Exemptions**:
- Non-critical read-only external calls (e.g., fetching a public RSS feed)
- Calls already behind a circuit breaker (`opossum`, `cockatiel`, `pybreaker`,
  `gobreaker`, `resilience4j`, Hystrix patterns, `recloser`, `failsafe-rs`)

**Detection**:
1. Identify external HTTP calls to non-localhost hosts in non-test source files
2. For each match: check if the call is wrapped in a circuit breaker library
   or sits behind a circuit-breaker-enabled HTTP client
3. Flag calls to external hosts with no circuit breaker evidence

**agent_action**:
1. Cite: `RESILIENCE-2 (WARN): External call to '{host}' at {file}:{line} has no circuit breaker protection.`
2. Explain the cascading failure risk: when the downstream is unavailable,
   callers accumulate blocked connections and eventually become unavailable too
3. Propose wrapping with the appropriate circuit breaker library:
   ```typescript
   // TypeScript/JavaScript — opossum
   import CircuitBreaker from 'opossum';
   const breaker = new CircuitBreaker(callPaymentAPI, {
     timeout: 3000,
     errorThresholdPercentage: 50,
     resetTimeout: 30000,
   });
   const result = await breaker.fire(payload);
   ```
4. If `--fix`: add the circuit breaker wrapper — require human to configure
   threshold and reset values appropriate for the dependency SLA

---

### RESILIENCE-3 — Unbounded Timeout
**Severity**: WARN | **Languages**: TypeScript, JavaScript, Python, Go, Rust | **Source**: CCC

**What it prohibits**: Network calls and external I/O with no timeout
configured. Default timeouts of major HTTP libraries are often unlimited or
extremely long, causing callers to hang indefinitely when a downstream is slow.

**Prohibited patterns**:
```typescript
// TypeScript/JavaScript
fetch(url);                            // no AbortSignal.timeout
axios.get(url);                        // no timeout option

# Python
requests.get(url)                      // no timeout= parameter
httpx.get(url)                         // no timeout= parameter

// Go
http.Get(url)                          // default http.Client has no timeout
resp, err := client.Do(req)            // client with no Timeout field set
ctx := context.Background()            // no deadline on context passed to call

// Rust
reqwest::get(url).await?;              // default Client has no timeout
client.get(url).send().await?;         // Client built without .timeout()
```

**Exemptions**:
- Streaming responses where timeout semantics differ (e.g., SSE, WebSocket,
  chunked downloads) — these should use per-read deadlines instead
- Calls where timeout is set at a higher layer (e.g., middleware, reverse proxy,
  or HTTP client constructor with default timeout)

**Detection**:
1. Grep for `fetch(`, `axios.`, `requests.get`, `requests.post`, `httpx.`,
   `http.Get(`, `http.Post(`, `client.Do(`, `reqwest::get(`,
   `reqwest::Client`, `client.get(`, `client.post(` (in `.rs` files
   where `client` is a `reqwest::Client`) in non-test source files
2. For each match: check if a timeout parameter, `AbortSignal.timeout`,
   `timeout=`, context deadline, `.timeout()` builder method, or
   `tokio::time::timeout` wrapper is present in the same statement or
   enclosing client configuration
3. Flag calls with no timeout evidence

**agent_action**:
1. Cite: `RESILIENCE-3 (WARN): Unbounded timeout on network call at {file}:{line}.`
2. Show the unbounded call
3. Propose adding an explicit timeout:
   ```typescript
   // TypeScript/JavaScript
   fetch(url, { signal: AbortSignal.timeout(5000) });
   axios.get(url, { timeout: 5000 });
   ```
   ```python
   # Python
   requests.get(url, timeout=5)
   httpx.get(url, timeout=5.0)
   ```
   ```go
   // Go
   client := &http.Client{Timeout: 5 * time.Second}
   ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
   defer cancel()
   ```
   ```rust
   // Rust — set timeout on the Client builder
   let client = reqwest::Client::builder()
       .timeout(std::time::Duration::from_secs(5))
       .build()?;
   // Or wrap with tokio::time::timeout
   // (The ?? works when the error type implements From<Elapsed>,
   // e.g. anyhow::Result. Map the Elapsed error explicitly otherwise.)
   let resp = tokio::time::timeout(
       std::time::Duration::from_secs(5),
       client.get(url).send(),
   ).await??;
   ```
4. If `--fix`: add the timeout parameter — use 5 seconds as a safe default
   and add a comment prompting the developer to tune for the specific endpoint

---

### RESILIENCE-4 — Missing Context Deadline Propagation (Go)
**Severity**: WARN | **Languages**: Go | **Source**: CCC

**What it prohibits**: Functions accepting `context.Context` that create new
child contexts without propagating the parent deadline. Or functions that use
`context.Background()` inside a handler that already has a request context.
This breaks the cancellation chain and prevents upstream timeouts from
propagating to downstream calls.

**Prohibited patterns**:
```go
// Using context.Background() inside a function that receives ctx
func HandleRequest(ctx context.Context, req *Request) error {
    // BAD: ignores the parent context deadline
    newCtx := context.Background()
    resp, err := client.Do(req.WithContext(newCtx))
    // ...
}

// Using context.TODO() in production handler code
func ProcessOrder(ctx context.Context, order *Order) error {
    // BAD: context.TODO() should not appear in production handlers
    result, err := paymentClient.Charge(context.TODO(), order.Amount)
    // ...
}
```

**Exemptions**:
- Background goroutines that intentionally outlive the request (e.g., async
  event publishing) — must be documented with a comment explaining the detach
- `context.Background()` in `main()`, `init()`, or test setup functions
- `context.TODO()` in code explicitly marked as work-in-progress with a
  linked tracking issue

**Detection**:
1. Grep for `context.Background()` and `context.TODO()` in non-test `.go` files
2. For each match: check if the enclosing function signature includes a
   `ctx context.Context` parameter
3. If the function receives a context but creates `context.Background()` or
   `context.TODO()`: flag as RESILIENCE-4
4. Exclude matches in `main()`, `init()`, and test files

**agent_action**:
1. Cite: `RESILIENCE-4 (WARN): Context fork at {file}:{line} — context.Background() used inside function that receives ctx.`
2. Show the context fork
3. Propose using the passed context:
   ```go
   // Use the parent context to propagate deadlines and cancellation
   ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
   defer cancel()
   resp, err := client.Do(req.WithContext(ctx))
   ```
4. If the detach is intentional: require a comment explaining why the
   background context is needed and what cleanup mechanism exists

---

Report schema: see `skills/conductor/shared-contracts.md`.
