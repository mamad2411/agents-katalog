---
name: threat-modeling
description: Apply the STRIDE framework to identify and mitigate security threats. Covers Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege with practical questions, verification steps, and mitigations for each threat category.
invoke_when: Use when designing a new system, reviewing security of an existing system, preparing for a security review, adding authentication or authorization, handling sensitive data, or discussing threat modeling.
---

# Threat Modeling with STRIDE

## Core Principle

Threat modeling is a structured way to think about what can go wrong with a system's security before an attacker finds out. Do it during design, not after launch. The STRIDE framework gives you six categories of threats to systematically evaluate.

---

## When to Threat Model

- Before building any new service or feature that handles user data.
- When adding a new external integration or API.
- When changing authentication or authorization logic.
- When introducing a new data store or data flow.
- During design document review (see the design-documents skill).
- At least annually for existing critical services.

---

## The STRIDE Framework

### S -- Spoofing (Pretending to Be Someone Else)

**Question to ask:** "Can an attacker pretend to be another user, service, or component?"

**What to verify:**
- [ ] All API endpoints require authentication (no accidental public endpoints).
- [ ] Authentication tokens are validated on every request, not just at login.
- [ ] Service-to-service calls use mutual TLS or signed tokens, not shared secrets.
- [ ] Email/SMS-based verification prevents account takeover.
- [ ] OAuth redirect URIs are strictly validated (no open redirects).
- [ ] API keys are scoped to specific permissions, not full access.

**Common mitigations:**
- Use strong authentication (OAuth 2.0 + PKCE, SAML, or WebAuthn).
- Implement multi-factor authentication for sensitive operations.
- Use short-lived tokens (15 min access tokens, longer refresh tokens).
- Validate the `aud` (audience) claim in JWTs to prevent token reuse across services.
- Rotate API keys and credentials on a schedule.

```typescript
// Verify JWT on every request -- not just presence but validity
function authenticateRequest(req: Request): User {
  const token = req.headers['authorization']?.replace('Bearer ', '');
  if (!token) throw new AuthError('Missing authentication token');

  const payload = jwt.verify(token, publicKey, {
    algorithms: ['RS256'],
    audience: 'api.myservice.com',     // Prevent token reuse from other services
    issuer: 'auth.mycompany.com',      // Verify who issued the token
  });

  return { id: payload.sub, roles: payload.roles };
}
```

---

### T -- Tampering (Modifying Data or Code)

**Question to ask:** "Can an attacker modify data in transit, at rest, or in the request?"

**What to verify:**
- [ ] All external communication uses TLS 1.2+ (no plaintext HTTP).
- [ ] Request payloads are validated against a schema (reject unexpected fields).
- [ ] File uploads are validated (type, size, content inspection -- not just extension).
- [ ] Database inputs are parameterized (no SQL injection).
- [ ] Webhook payloads are verified with HMAC signatures.
- [ ] Client-side values (hidden fields, cookies) are not trusted as authoritative.

**Common mitigations:**
- Use parameterized queries or an ORM for all database access.
- Validate and sanitize all input at the API boundary.
- Use HMAC-SHA256 to sign webhook payloads and verify signatures on receipt.
- Implement Content Security Policy (CSP) headers to prevent XSS.
- Use integrity checks (checksums) for file transfers and deployments.

```python
# Verify webhook signature to prevent tampering
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        key=secret.encode(),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

# Usage in webhook handler
@app.post("/webhooks/payment")
def handle_payment_webhook(request: Request):
    signature = request.headers.get("X-Signature-256")
    if not verify_webhook_signature(request.body, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")
    # Process the verified webhook payload
```

---

### R -- Repudiation (Denying an Action Occurred)

**Question to ask:** "Can a user or system deny they performed an action, and can we prove otherwise?"

**What to verify:**
- [ ] All state-changing operations are logged with who, what, when, and from where.
- [ ] Audit logs are immutable (append-only, cannot be modified or deleted by application code).
- [ ] Logs include sufficient context to reconstruct what happened.
- [ ] Audit logs are stored separately from application logs.
- [ ] Time synchronization (NTP) is configured on all servers.
- [ ] Critical operations require explicit user confirmation (not just a single click).

**Common mitigations:**
- Implement an append-only audit log for all sensitive operations.
- Log the user ID, IP address, timestamp, action, and affected resource for every mutation.
- Store audit logs in a separate data store with restricted write access.
- Use digital signatures for high-value transactions.
- Retain audit logs for the period required by compliance (typically 1-7 years).

```typescript
interface AuditEntry {
  timestamp: string;       // ISO 8601
  actor: string;           // User ID or service name
  action: string;          // "user.deleted", "payment.refunded"
  resource: string;        // "user:usr_123", "payment:pay_456"
  details: object;         // Before/after state, request metadata
  sourceIp: string;
  userAgent: string;
  requestId: string;
}

async function auditLog(entry: AuditEntry): Promise<void> {
  // Write to append-only audit store (e.g., separate DB table, S3, CloudTrail)
  await auditStore.append(entry);
  // Audit writes must never fail silently -- if this fails, the operation should also fail
}
```

---

### I -- Information Disclosure (Exposing Sensitive Data)

**Question to ask:** "Can an attacker access data they should not see?"

**What to verify:**
- [ ] Error messages do not leak stack traces, SQL queries, or internal paths in production.
- [ ] API responses do not include fields the requesting user is not authorized to see.
- [ ] Logs do not contain PII, passwords, tokens, or credit card numbers.
- [ ] Database backups are encrypted.
- [ ] Sensitive data in environment variables is not exposed via debug endpoints.
- [ ] CORS policies are restrictive (not `Access-Control-Allow-Origin: *`).
- [ ] Directory listing is disabled on web servers.
- [ ] Source maps are not deployed to production.

**Common mitigations:**
- Return generic error messages to clients. Log detailed errors server-side only.
- Use field-level authorization to filter API responses based on the caller's permissions.
- Implement data masking for logs (mask credit cards, SSNs, tokens).
- Encrypt data at rest (AES-256) and in transit (TLS 1.2+).
- Use separate database credentials with minimal permissions per service.

```typescript
// Sanitize error responses -- never leak internals to clients
function errorHandler(error: Error, req: Request, res: Response): void {
  // Log the full error internally
  logger.error('Request failed', {
    error: error.message,
    stack: error.stack,
    requestId: req.id,
    path: req.path,
  });

  // Return a safe error to the client
  res.status(500).json({
    error: {
      code: 'internal_error',
      message: 'An unexpected error occurred. Please try again.',
      requestId: req.id,  // Include for support reference, not for debugging
    },
  });
}

// Mask sensitive data in logs
function maskPII(data: Record<string, unknown>): Record<string, unknown> {
  const sensitiveFields = ['password', 'ssn', 'credit_card', 'token', 'secret'];
  const masked = { ...data };
  for (const field of sensitiveFields) {
    if (masked[field]) masked[field] = '***REDACTED***';
  }
  return masked;
}
```

---

### D -- Denial of Service (Making the System Unavailable)

**Question to ask:** "Can an attacker make the system unavailable or unusable?"

**What to verify:**
- [ ] Rate limiting is applied to all public endpoints.
- [ ] Request size limits are configured (body size, file upload size).
- [ ] Query complexity is bounded (pagination limits, query depth limits for GraphQL).
- [ ] Resource-intensive operations are queued, not processed synchronously.
- [ ] Connection limits prevent a single client from exhausting the connection pool.
- [ ] DDoS mitigation is in place (WAF, CDN, auto-scaling).

**Common mitigations:**
- Implement rate limiting per API key or IP address (e.g., 100 requests/minute).
- Set maximum request body size (e.g., 1MB for API, 50MB for file uploads).
- Paginate all list endpoints with a maximum page size.
- Use a WAF (AWS WAF, Cloudflare) to block common attack patterns.
- Auto-scale horizontally to absorb traffic spikes.
- Set timeouts on all database queries and external calls.

```python
# Rate limiting configuration
from fastapi import FastAPI
from slowapi import Limiter

limiter = Limiter(key_func=get_api_key_or_ip)
app = FastAPI()

@app.get("/api/v1/search")
@limiter.limit("30/minute")    # 30 requests per minute per API key
async def search(query: str, page: int = 1, page_size: int = 20):
    if page_size > 100:
        raise HTTPException(400, "page_size must be <= 100")
    # Process search with bounded results
```

---

### E -- Elevation of Privilege (Gaining Unauthorized Access)

**Question to ask:** "Can an attacker perform actions they are not authorized to do?"

**What to verify:**
- [ ] Authorization checks happen on every request, not just in the UI.
- [ ] Object-level authorization: users can only access their own resources (IDOR protection).
- [ ] Role changes require approval and are audited.
- [ ] Admin endpoints are on a separate network or require elevated authentication.
- [ ] SQL injection, command injection, and path traversal are prevented.
- [ ] Dependencies are scanned for known vulnerabilities.

**Common mitigations:**
- Implement object-level authorization on every data access (check ownership, not just authentication).
- Use role-based access control (RBAC) or attribute-based access control (ABAC).
- Run services with the least privilege needed (no root, minimal IAM permissions).
- Scan dependencies with `npm audit`, `pip audit`, Snyk, or Dependabot.
- Separate admin functionality onto a different service/port with stricter access controls.

```typescript
// Object-level authorization -- prevent IDOR
async function getOrder(userId: string, orderId: string): Promise<Order> {
  const order = await orderRepository.findById(orderId);
  if (!order) throw new NotFoundError('Order not found');

  // CRITICAL: Verify the requesting user owns this order
  if (order.customerId !== userId && !hasRole(userId, 'admin')) {
    throw new ForbiddenError('You do not have access to this order');
  }

  return order;
}
```

---

## Practical Walkthrough: Threat Modeling a Web Application

Consider a typical web application with: a React frontend, a REST API, a PostgreSQL database, a Redis cache, and integration with a third-party payment provider.

### Step 1: Draw the Data Flow Diagram

```
[Browser] --HTTPS--> [CDN/WAF] --HTTPS--> [API Gateway]
                                              |
                                    [Auth Service] <-- [Identity Provider]
                                              |
                                    [Order Service] --HTTPS--> [Payment Provider]
                                        |         |
                                  [PostgreSQL]  [Redis]
```

### Step 2: Apply STRIDE to Each Component

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation |
|---|---|---|---|---|---|---|
| Browser -> API | Stolen JWT tokens | Modified request payload | User denies placing order | PII in error messages | Flood requests | IDOR on /orders/{id} |
| API -> Payment | Spoofed callback URL | Modified payment amount | Payment dispute | Payment details in logs | - | Admin payment endpoints |
| API -> Database | - | SQL injection | Missing audit logs | Unencrypted backups | Slow queries | Excessive DB permissions |
| API -> Redis | - | Cache poisoning | - | Cached PII without TTL | Memory exhaustion | - |

### Step 3: Prioritize and Mitigate

For each identified threat, assign a risk level (High/Medium/Low) based on likelihood and impact. Address High risks before launch, Medium risks within the first quarter, Low risks as capacity allows.

| Risk Level | Likelihood | Impact | Action |
|---|---|---|---|
| **High** | Likely or has happened before | Data breach, revenue loss, compliance violation | Must fix before launch |
| **Medium** | Possible but requires effort | Service degradation, limited data exposure | Fix within 30 days |
| **Low** | Unlikely or requires insider access | Minor information leak, cosmetic | Fix as capacity allows |

---

## Threat Model Document Template

```markdown
# Threat Model: [System/Feature Name]

**Date:** [YYYY-MM-DD]
**Author:** [Name]
**Reviewers:** [Names]
**Status:** [Draft / In Review / Approved]

## System Description
[Brief description of the system, its purpose, and its data flows]

## Data Flow Diagram
[Include a diagram showing components, data flows, and trust boundaries]

## Assets (What Are We Protecting?)
- User PII (names, emails, addresses)
- Authentication credentials
- Payment information
- System availability
- Business logic integrity

## Trust Boundaries
[Where does trust level change? Examples: public internet to internal network,
user-facing API to admin API, application to database]

## Threat Analysis

| ID | Category | Threat | Component | Risk | Mitigation | Status |
|----|----------|--------|-----------|------|------------|--------|
| T1 | Spoofing | Stolen JWT allows account takeover | Auth | High | Short-lived tokens + refresh rotation | Implemented |
| T2 | Tampering | SQL injection via search endpoint | API | High | Parameterized queries + WAF | Implemented |
| T3 | Repudiation | User denies placing an order | Order Service | Medium | Audit log with user ID, IP, timestamp | Implemented |
| T4 | Info Disclosure | PII in application logs | Logging | Medium | Log masking for sensitive fields | To Do |
| T5 | DoS | Unbounded search results | Search API | Medium | Pagination with max page size of 100 | Implemented |
| T6 | Elevation | IDOR on order endpoint | Order API | High | Object-level authorization check | Implemented |

## Accepted Risks
[Document any risks you are choosing to accept, with justification and owner]

| Risk | Justification | Owner | Review Date |
|------|---------------|-------|-------------|
| Redis cache not encrypted at rest | Cache contains only non-sensitive computed data with 1h TTL | @security-team | 2025-12-01 |

## Review Schedule
This threat model will be reviewed when the architecture changes or annually,
whichever comes first. Next review: [Date]
```

---

## Checklist

- [ ] A threat model exists for every service that handles sensitive data.
- [ ] All six STRIDE categories have been evaluated for every component.
- [ ] A data flow diagram exists showing trust boundaries.
- [ ] High-risk threats are mitigated before launch.
- [ ] The threat model is reviewed when the system architecture changes.
- [ ] The threat model is reviewed at least annually.
- [ ] Accepted risks are documented with justification, owner, and review date.
- [ ] Dependencies are scanned for known vulnerabilities (automated in CI).
