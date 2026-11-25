---
name: contract-testing
description: Design contract tests for APIs and microservices with Pact. Outputs consumer-driven contracts, provider verification, and CI integration.
argument-hint: [service architecture, API contracts, teams]
allowed-tools: Read, Write, Bash
---

# Contract Testing

Design contract tests between services. Not end-to-end tests — consumer-driven contracts ensuring API compatibility without deploying all services.

## Process

1. **Identify contracts.** Service boundaries, API contracts between teams.
2. **Choose tool.** Pact (consumer-driven), Spring Cloud Contract, Postman.
3. **Write consumer tests.** Consumer defines expected API behavior.
4. **Generate contract.** Pact file with requests/responses.
5. **Verify provider.** Provider validates it meets contract.
6. **Publish contracts.** Pact Broker stores contracts for all teams.
7. **Prevent breaking changes.** CI fails if provider breaks consumer contract.

## Output Format

### Contract Testing: [Service Architecture]

**Tool:** Pact  
**Services:** 5 (frontend, order-service, payment-service, user-service, inventory)  
**Contracts:** 8 defined  
**Broker:** Pact Broker (hosted)  
**CI:** Contracts verified on every PR

---

## Problem: Integration Testing at Scale

### Traditional Approach (E2E)
```
Deploy All Services → Test Together → Find Bugs Late

Issues:
- Slow (minutes to deploy full stack)
- Flaky (network, dependencies)
- Expensive (infrastructure costs)
- Late feedback (after merge)
```

### Contract Testing Approach
```
Consumer Tests → Generate Contract → Provider Verifies

Benefits:
- Fast (no deployment needed)
- Reliable (no network calls)
- Early feedback (before merge)
- Independent (teams work in parallel)
```

---

## Consumer-Driven Contracts

### Consumer Test (Frontend)
```javascript
// Frontend defines expected API behavior
const { Pact } = require('@pact-foundation/pact');
const axios = require('axios');

const provider = new Pact({
  consumer: 'Frontend',
  provider: 'UserService',
  port: 1234,
  log: path.resolve(__dirname, 'logs', 'pact.log'),
  dir: path.resolve(__dirname, 'pacts'),
  logLevel: 'info',
});

describe('User API', () => {
  before(() => provider.setup());
  after(() => provider.finalize());

  describe('GET /users/:id', () => {
    before(() => {
      // Define expected interaction
      const expectedInteraction = {
        uponReceiving: 'a request for user 123',
        withRequest: {
          method: 'GET',
          path: '/users/123',
          headers: {
            'Authorization': 'Bearer token123',
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            id: '123',
            name: 'John Doe',
            email: 'john@example.com',
          },
        },
      };

      return provider.addInteraction(expectedInteraction);
    });

    it('returns user data', async () => {
      // Test against mock server
      const response = await axios.get('http://localhost:1234/users/123', {
        headers: { 'Authorization': 'Bearer token123' },
      });

      expect(response.status).to.equal(200);
      expect(response.data.name).to.equal('John Doe');
    });
  });
});
```

**Result:** Generates `Frontend-UserService.json` contract file

---

## Pact Contract File

```json
{
  "consumer": {
    "name": "Frontend"
  },
  "provider": {
    "name": "UserService"
  },
  "interactions": [
    {
      "description": "a request for user 123",
      "request": {
        "method": "GET",
        "path": "/users/123",
        "headers": {
          "Authorization": "Bearer token123"
        }
      },
      "response": {
        "status": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "id": "123",
          "name": "John Doe",
          "email": "john@example.com"
        }
      }
    }
  ]
}
```

---

## Provider Verification

```javascript
// UserService verifies it meets Frontend's contract
const { Verifier } = require('@pact-foundation/pact');

describe('Pact Verification', () => {
  it('validates the expectations of Frontend', () => {
    const opts = {
      provider: 'UserService',
      providerBaseUrl: 'http://localhost:3000',  // Running UserService
      
      // Fetch contract from Pact Broker
      pactBrokerUrl: 'https://pact-broker.example.com',
      pactBrokerToken: process.env.PACT_BROKER_TOKEN,
      
      // Or local file
      // pactUrls: ['./pacts/Frontend-UserService.json'],
      
      // Provider state setup
      stateHandlers: {
        'user 123 exists': () => {
          // Setup: Insert user 123 into test database
          return database.users.create({
            id: '123',
            name: 'John Doe',
            email: 'john@example.com',
          });
        },
      },
      
      publishVerificationResult: true,
      providerVersion: process.env.GIT_COMMIT,
    };

    return new Verifier(opts).verifyProvider();
  });
});
```

**If provider returns different response:**
```
Contract verification failed:
Expected: { "name": "John Doe" }
Actual: { "name": "Jane Doe" }
```

---

## Pact Broker

### Publish Contracts
```bash
# Consumer publishes contract after test
pact-broker publish ./pacts \
  --consumer-app-version $(git rev-parse HEAD) \
  --broker-base-url https://pact-broker.example.com \
  --broker-token $PACT_BROKER_TOKEN
```

### Provider Verifies from Broker
```bash
# Provider fetches all consumer contracts
pact-broker verify \
  --provider UserService \
  --provider-app-version $(git rev-parse HEAD) \
  --broker-base-url https://pact-broker.example.com \
  --publish-verification-results
```

### Can-I-Deploy Check
```bash
# Before deploying to production, check compatibility
pact-broker can-i-deploy \
  --pacticipant UserService \
  --version $(git rev-parse HEAD) \
  --to-environment production

# Output:
Computer says yes \o/
All required verification results are published.
```

---

## Provider States

### Problem: Test Data Setup
```
Consumer expects: "user 123 exists"
Provider test needs: User 123 in database
```

### Solution: State Handlers
```javascript
// Consumer defines required state
const interaction = {
  state: 'user 123 exists',  // Provider must setup this state
  uponReceiving: 'a request for user 123',
  ...
};

// Provider implements state handler
stateHandlers: {
  'user 123 exists': async () => {
    await database.users.create({
      id: '123',
      name: 'John Doe',
      email: 'john@example.com'
    });
  },
  'user 123 does not exist': async () => {
    await database.users.delete({ id: '123' });
  }
}
```

---

## Matchers (Flexible Contracts)

### Exact Matching (Brittle)
```javascript
body: {
  id: '123',           // Must be exactly "123"
  name: 'John Doe',    // Must be exactly "John Doe"
}
```

### Type Matching (Flexible)
```javascript
const { like, eachLike, term } = require('@pact-foundation/pact').Matchers;

body: {
  id: like('123'),              // Any string
  name: like('John Doe'),       // Any string
  email: term({
    matcher: '.+@.+\\..+',      // Regex pattern
    generate: 'john@example.com'
  }),
  orders: eachLike({            // Array of objects
    id: like('1'),
    amount: like(100.50)
  }, { min: 2 })                // At least 2 items
}
```

**Provider can return:**
```json
{
  "id": "999",  // Different ID, still valid
  "name": "Jane Smith",
  "email": "jane@test.com",
  "orders": [
    { "id": "5", "amount": 50.00 },
    { "id": "6", "amount": 75.00 }
  ]
}
```

---

## Bi-Directional Contracts

### Consumer Contract (Pact)
```
Frontend → UserService
Frontend defines expected behavior
```

### Provider Contract (OpenAPI)
```yaml
# UserService openapi.yaml
paths:
  /users/{id}:
    get:
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
```

### Verify Both Directions
```
1. Consumer tests against Pact mock
2. Provider tests against OpenAPI spec
3. Compare: Does Pact contract fit within OpenAPI spec?
```

---

## CI/CD Integration

### Consumer Pipeline
```yaml
# .github/workflows/consumer-tests.yml
name: Consumer Contract Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Pact tests
        run: npm run test:pact
      
      - name: Publish contracts
        if: github.ref == 'refs/heads/main'
        run: |
          pact-broker publish pacts/ \
            --consumer-app-version ${{ github.sha }} \
            --broker-base-url ${{ secrets.PACT_BROKER_URL }} \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }}
```

### Provider Pipeline
```yaml
# Provider verifies ALL consumer contracts
name: Provider Contract Verification

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start provider service
        run: docker-compose up -d
      
      - name: Verify contracts
        run: npm run test:pact:verify
      
      - name: Can I deploy?
        if: github.ref == 'refs/heads/main'
        run: |
          pact-broker can-i-deploy \
            --pacticipant UserService \
            --version ${{ github.sha }} \
            --to-environment production
```

---

## Breaking Change Prevention

### Scenario: Provider Changes Response
```javascript
// Old response (in contract)
{
  "id": "123",
  "name": "John Doe"
}

// New response (provider change)
{
  "id": "123",
  "fullName": "John Doe"  // Changed "name" → "fullName"
}
```

**Result:**
```
Contract verification FAILED
Expected field 'name', got 'fullName'
❌ Build fails, deployment blocked
```

**Solution:**
1. Add `fullName` alongside `name` (backward compatible)
2. Update consumer to use `fullName`
3. Publish new consumer contract
4. Remove `name` from provider (after all consumers updated)

---

## Testing Multiple Scenarios

```javascript
describe('User API', () => {
  // Happy path
  it('returns user when found', async () => {
    await provider.addInteraction({
      state: 'user 123 exists',
      ...
      willRespondWith: { status: 200, body: { ... } }
    });
    // Test...
  });

  // Error case
  it('returns 404 when user not found', async () => {
    await provider.addInteraction({
      state: 'user 999 does not exist',
      withRequest: {
        path: '/users/999'
      },
      willRespondWith: {
        status: 404,
        body: {
          error: 'User not found'
        }
      }
    });
    // Test...
  });

  // Authentication error
  it('returns 401 when unauthorized', async () => {
    await provider.addInteraction({
      withRequest: {
        path: '/users/123',
        headers: {} // No Authorization header
      },
      willRespondWith: {
        status: 401
      }
    });
    // Test...
  });
});
```

---

## Contract Testing vs Other Testing

### Unit Tests
- Scope: Single function/class
- Speed: Very fast (milliseconds)
- Isolation: No dependencies

### Contract Tests
- Scope: API boundary between services
- Speed: Fast (seconds)
- Isolation: Mock provider (consumer) or mock database (provider)

### Integration Tests
- Scope: Multiple services together
- Speed: Slow (minutes)
- Isolation: Real services deployed

### E2E Tests
- Scope: Full system through UI
- Speed: Very slow (10+ minutes)
- Isolation: Production-like environment

**Test Pyramid:**
```
    /\
   /E2E\        ← Few, expensive
  /______\
 /Integration\  ← Some, moderate
/______________\
/  Contract    \  ← Many, fast
/________________\
/   Unit Tests   \  ← Most, very fast
/__________________\
```

---

## Common Pitfalls

### ❌ Over-Specifying Contracts
```javascript
// Bad: Testing implementation details
body: {
  id: '123',
  name: 'John Doe',
  created_at: '2024-03-21T10:30:00Z',  // Exact timestamp
  metadata: {
    internal_id: 'abc',  // Internal field
    version: 2
  }
}
```

### ✅ Consumer-Focused Contracts
```javascript
// Good: Only fields consumer uses
body: {
  id: like('123'),
  name: like('John Doe')
  // Don't specify fields consumer doesn't use
}
```

---

### ❌ No Provider States
```javascript
// Provider test fails randomly
// Sometimes user exists, sometimes doesn't
```

### ✅ Explicit States
```javascript
state: 'user 123 exists'
// Provider always sets up this state before test
```

## Rules

- Contracts owned by consumer, not provider — consumer defines what it needs.
- One contract per consumer-provider pair — Frontend-UserService, Mobile-UserService separate.
- Provider must pass all consumer contracts — can't break any consumer.
- Use matchers, not exact values — contracts should be flexible (types, not values).
- Provider states required for data-dependent tests — explicit setup prevents flaky tests.
- Publish contracts to broker, not git — centralized visibility for all teams.
- Run can-i-deploy before production — verifies all consumers compatible.
- Contract tests don't replace integration tests — test contracts, not business logic.
- Breaking change requires consumer update first — add new field, deprecate old.
- Test error cases in contracts — 404, 401, 500 responses are part of contract.
