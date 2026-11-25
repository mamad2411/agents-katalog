---
name: api-backward-compatibility
description: Design and evolve APIs without breaking existing consumers. Covers additive-only changes, versioning strategies, deprecation workflows, consumer-driven contract testing, and backward-compatible defaults. References Stripe's API stability as the gold standard.
invoke_when: Use when designing a new API, modifying an existing API, adding or removing fields, changing response shapes, discussing versioning, planning a deprecation, or reviewing API changes for backward compatibility.
---

# API Backward Compatibility

## Core Principle

Once an API is public (has consumers you do not fully control), every change must be backward compatible unless you go through a formal deprecation process. Stripe is the gold standard: their API versions from 2011 still work. Aim for that level of stability.

---

## 1. The Additive-Only Changes Rule

**Safe changes (backward compatible):**

- Adding a new optional field to a request body.
- Adding a new field to a response body.
- Adding a new endpoint.
- Adding a new optional query parameter.
- Adding a new enum value (if consumers handle unknown values gracefully).
- Adding a new webhook event type.

**Breaking changes (require versioning or migration):**

- Removing or renaming a field from a response.
- Removing or renaming a field from a request.
- Changing a field's type (string to integer, etc.).
- Changing the meaning or behavior of an existing field.
- Making an optional field required.
- Changing the URL path of an existing endpoint.
- Changing error response shapes or status codes.
- Removing an enum value.
- Changing default values in ways that alter behavior.

### Enforcement

Every API pull request must answer: "Can an existing consumer send the same request and get a response they can still parse?" If the answer is no, the change is breaking.

```typescript
// SAFE: Adding a new optional field to the response
// Before
{ "id": "usr_123", "name": "Alice" }
// After -- existing consumers ignore the new field
{ "id": "usr_123", "name": "Alice", "avatar_url": "https://..." }

// BREAKING: Renaming a field
// Before
{ "id": "usr_123", "name": "Alice" }
// After -- existing consumers looking for "name" will break
{ "id": "usr_123", "display_name": "Alice" }

// SAFE way to rename: keep both, deprecate old
{ "id": "usr_123", "name": "Alice", "display_name": "Alice" }
```

---

## 2. Versioning Strategies

### Strategy A: URL Path Versioning

```
GET /v1/users/123
GET /v2/users/123
```

- **Pros:** Explicit, easy to understand, easy to route.
- **Cons:** Encourages big-bang version bumps. Hard to maintain many versions.
- **Best for:** Public APIs with long-lived consumers.

### Strategy B: Header Versioning (Stripe-Style)

```
GET /users/123
Stripe-Version: 2024-06-01
```

- **Pros:** Clean URLs. Versions are pinned per API key, not per request. Consumers upgrade on their own timeline.
- **Cons:** More complex routing infrastructure.
- **Best for:** APIs where you want consumers to control their upgrade pace.

**How Stripe does it:**
1. Every API key is pinned to the version that existed when it was created.
2. Consumers can override with a header to test newer versions.
3. Each version maps to a set of transformations that convert the latest internal representation to the version the consumer expects.

### Strategy C: Query Parameter Versioning

```
GET /users/123?version=2
```

- **Pros:** Simple.
- **Cons:** Easy to forget. Not suitable for production-grade APIs.
- **Best for:** Internal APIs during prototyping.

### Recommendation

For public APIs: Use URL path versioning (`/v1/`) and commit to never breaking `v1`. Introduce `v2` only for fundamental redesigns. Within a version, use additive-only changes.

For internal APIs: Use header versioning or simply maintain backward compatibility without explicit versions.

---

## 3. Deprecation Workflow with Sunset Dates

Never remove an API or field without a formal deprecation process.

### Step-by-Step Deprecation

**Step 1: Announce deprecation (minimum 6 months before removal for public APIs, 3 months for internal).**

```http
HTTP/1.1 200 OK
Sunset: Sat, 01 Mar 2026 00:00:00 GMT
Deprecation: true
Link: <https://docs.example.com/migration/v2-users>; rel="successor-version"
```

**Step 2: Add deprecation warnings to documentation and changelog.**

```yaml
# OpenAPI spec
/v1/users/{id}/legacy-profile:
  get:
    deprecated: true
    x-sunset-date: "2026-03-01"
    description: |
      DEPRECATED: Use /v1/users/{id}/profile instead.
      This endpoint will be removed on 2026-03-01.
```

**Step 3: Log which consumers are still using the deprecated endpoint.**

```python
def track_deprecated_usage(endpoint: str, api_key: str):
    metrics.increment("api.deprecated.usage", tags={
        "endpoint": endpoint,
        "consumer": get_consumer_name(api_key),
    })
```

**Step 4: Notify consumers directly (email, Slack, dashboard warning).**

**Step 5: Reduce availability gradually (return 299 status with warning, then 410 Gone).**

**Step 6: Remove after sunset date, returning 410 Gone with a link to the successor.**

```json
{
  "error": {
    "code": "endpoint_removed",
    "message": "This endpoint was removed on 2026-03-01. Use /v1/users/{id}/profile instead.",
    "docs_url": "https://docs.example.com/migration/v2-users"
  }
}
```

---

## 4. Consumer-Driven Contract Testing

**What it does:** Consumers define what they expect from the API (the contract). The provider runs these contracts as part of CI to ensure no consumer is broken by a change.

**When to apply:** Any API with more than one consumer, especially internal microservices.

### Using Pact (Industry Standard)

**Consumer side (defines expectations):**

```typescript
// user-consumer.pact.test.ts
const provider = new PactV4({
  consumer: 'OrderService',
  provider: 'UserService',
});

describe('UserService contract', () => {
  it('returns user by ID', async () => {
    await provider
      .addInteraction()
      .given('user usr_123 exists')
      .uponReceiving('a request for user usr_123')
      .withRequest('GET', '/v1/users/usr_123')
      .willRespondWith(200, (body) => {
        body.jsonBody({
          id: like('usr_123'),
          name: like('Alice'),
          email: like('alice@example.com'),
          // Note: consumer only asserts fields it uses
        });
      })
      .executeTest(async (mockServer) => {
        const client = new UserClient(mockServer.url);
        const user = await client.getUser('usr_123');
        expect(user.name).toBeDefined();
      });
  });
});
```

**Provider side (verifies contracts from all consumers):**

```typescript
// user-provider.pact.test.ts
const verifier = new Verifier({
  providerBaseUrl: 'http://localhost:3000',
  pactUrls: ['./pacts/OrderService-UserService.json'],
  stateHandlers: {
    'user usr_123 exists': async () => {
      await seedUser({ id: 'usr_123', name: 'Alice', email: 'alice@example.com' });
    },
  },
});

describe('UserService provider verification', () => {
  it('satisfies all consumer contracts', () => verifier.verifyProvider());
});
```

### CI Integration

- Consumer publishes pact contracts to a Pact Broker on merge to main.
- Provider CI fetches all consumer contracts and verifies them before deploying.
- If verification fails, the provider cannot deploy (the change would break a consumer).

---

## 5. Default Values for Backward Compatibility

When adding new fields that affect behavior, always set safe defaults that preserve existing behavior.

```typescript
// Adding a new "currency" field to the charges API
// Existing consumers do not send "currency", so default to USD (existing behavior)
interface CreateChargeRequest {
  amount: number;
  customer_id: string;
  currency?: string; // NEW -- defaults to "usd" if omitted
}

function processCharge(req: CreateChargeRequest) {
  const currency = req.currency ?? 'usd'; // Preserve existing behavior
  // ...
}
```

### Rules for Defaults

1. The default must produce the same behavior as before the field existed.
2. Document the default explicitly in the API docs.
3. If no safe default exists, the field must be introduced as a new endpoint or API version.
4. Never change an existing default value -- that is a breaking change.

---

## API Change Review Checklist

- [ ] Is every new field optional with a documented default?
- [ ] Are existing field names, types, and meanings unchanged?
- [ ] Are existing endpoints still available at the same paths?
- [ ] Are existing required fields still required (not more, not fewer)?
- [ ] Is the change additive-only? If not, is there a versioning/deprecation plan?
- [ ] Are consumer-driven contract tests passing?
- [ ] Is the deprecation timeline at least 6 months for public APIs?
- [ ] Are deprecated endpoints returning Sunset and Deprecation headers?
- [ ] Is deprecated endpoint usage being tracked?
- [ ] Does the OpenAPI spec accurately reflect the changes?
