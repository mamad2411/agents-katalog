---
name: middleware-engineer
description: Middleware Engineer Skill
category: backend
tags:
- backend
- middleware
---
## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Contract & Discovery

**BEFORE writing the adapter:**

1.  **API Audit**
    - Read the Rate Limits. (Requests per minute?).
    - Read the SLA. (Do they guarantee 99.9% uptime?).
    - **Auth Method:** OAuth2? API Key? mTLS?
    - **Webhooks:** Do they push data to us? How do we verify the signature?

2.  **Data Mapping (The Anti-Corruption Layer)**
    - **Rule:** Never let external data structures leak into your internal domain.
    - Create an "Adapter" or "Mapper" to convert their JSON to Your Object.
    - If they change their API, you only change the Mapper, not your whole app.

3.  **Secret Management**
    - Where do the API keys live? (Secret Manager).
    - Rotation Strategy: What happens if a key leaks?

### Phase 2: Resilience & Queuing

**Assume they will fail:**

1.  **Circuit Breaker Pattern**
    - If the 3rd party fails 5 times, stop calling them for 1 minute.
    - Fail fast instead of hanging the user's thread.

2.  **Asynchronous Decoupling**
    - Don't call the 3rd party in the main request loop.
    - Put the job on a Queue (SQS/RabbitMQ). "Process Payment" -> Queue.
    - **Retries:** Exponential Backoff (Retry in 1s, then 2s, then 4s).

3.  **Idempotency**
    - What happens if we send the same request twice? (Double charge?).
    - Send an "Idempotency Key" (Unique ID) with every write request.

### Phase 3: Testing & Mocking

**Don't test against production APIs:**

1.  **Sandboxing**
    - Use their Sandbox/Test environment.
    - **Warning:** Sandboxes often behave differently than Prod (faster/slower).

2.  **Mock Servers (Wiremock)**
    - Record the real response once. Replay it in your tests.
    - Simulate 500 Errors and Timeouts. Does your app handle it?

3.  **Consumer Driven Contracts**
    - Verify that the fields you need actually exist.

### Phase 4: Governance & Monitoring

**Watching the relationship:**

1.  **Quota Tracking**
    - Alert *before* you hit the rate limit.
    - Alert on cost spikes (e.g., Maps API bill usage).

2.  **Webhook Verification**
    - Verify the cryptographic signature of incoming webhooks.
    - Prevent "Replay Attacks."

3.  **Vendor Updates**
    - Subscribe to their changelog.
    - Deprecation warnings are deadlines, not suggestions.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "I'll just call the API directly from the frontend." (Leaked keys).
- "They rarely go down, I don't need a retry loop." (They will go down).
- "I'll handle the webhook later." (Data sync issues).
- "I'll store the API key in the code." (Security breach).
- "If the API is slow, the user just has to wait." (Bad UX).
- "I'll use their data format everywhere in my app." (Tight coupling).

**ALL of these mean: STOP. Return to Phase 1.**

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Contract** | Mapping, Auth, Secrets | Clean internal interface |
| **2. Resilience** | Circuit Breakers, Queues | No cascading failures |
| **3. Testing** | Mocks, Sandboxes | Tests pass without internet |
| **4. Governance** | Rate Limits, Cost alerts | No bill shock, No outages |

## 🛠️ Modern Middleware Stack (2026)

### API Gateway
- **Kong:** Open-source, plugin ecosystem, rate limiting
- **Tyk:** Developer portal, analytics
- **AWS API Gateway:** Managed, serverless
- **Envoy Proxy:** Cloud-native, used by Istio

### Service Mesh (10+ Microservices)
- **Istio:** Feature-rich, observability, mTLS
- **Linkerd:** Simpler, Rust-based, lightweight
- **Consul Connect:** HashiCorp ecosystem
- **When:** Complex inter-service communication, need per-request metrics

### Message Queues
- **RabbitMQ:** Classic, reliable, AMQP
- **Apache Kafka:** High-throughput streaming
- **AWS SQS:** Managed, serverless
- **BullMQ:** Redis-based, Node.js

### Observability (OpenTelemetry)
- **Tracing:** Jaeger, Tempo, Honeycomb
- **Metrics:** Prometheus, Datadog
- **Logs:** Grafana Loki, CloudWatch

## 📊 OpenTelemetry Integration

### Distributed Tracing
```javascript
const { trace } = require('@opentelemetry/api');

async function callExternalAPI(userId) {
  const span = trace.getActiveSpan();
  span?.setAttribute('user.id', userId);
  span?.addEvent('calling_external_api');
  
  try {
    const response = await fetch('https://api.example.com/data');
    span?.setAttribute('http.status_code', response.status);
    return response.json();
  } catch (error) {
    span?.recordException(error);
    span?.setStatus({ code: SpanStatusCode.ERROR });
    throw error;
  }
}
```

### Propagating Context
- **Trace ID:** Flows through all services
- **Baggage:** Carry metadata (user_id, tenant_id, feature_flags)
- **W3C Standard:** traceparent header

## 🔒 Security Patterns

### API Key Rotation
```
1. Generate new key
2. Deploy with both keys accepted (grace period)
3. Update clients to new key
4. Remove old key after 30 days
```

### Webhook Signature Verification
```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const digest = hmac.update(payload).digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(digest)
  );
}
```

### Rate Limiting Strategies
- **Fixed Window:** 100 req/hour (simple, can burst)
- **Sliding Window:** Smooths out bursts
- **Token Bucket:** Allows bursts up to capacity
- **Leaky Bucket:** Constant rate, smoothest
