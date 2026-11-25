---
name: contract-testing-patterns
description: Pact consumer-driven contracts, provider verification, schema evolution. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When designing or changing APIs that have consumers (internal or external). Pair with backend-dev, api-gateway-expert, graphql-expert, test-enforcement, arbiter.
---

# Contract Testing Patterns (Grok Port)

Consumer-driven contract testing (Pact et al.) so that providers never break consumers. Grok-native: Production Contract, ledger for schema changes, preflight "will this break clients?", compound from past client breakages, claim-verif on "backward compatible".

## Consumer-Driven Contract Testing with Pact (JS/TS example)
```js
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const { like, eachLike, string, integer } = MatchersV3;

const provider = new PactV3({
  consumer: 'OrderService',
  provider: 'UserService',
  logLevel: 'warn',
});

describe('User API Contract', () => {
  it('returns user by ID', async () => {
    await provider
      .given('user with ID 1 exists')
      .uponReceiving('a request for user 1')
      .withRequest({
        method: 'GET',
        path: '/api/users/1',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: integer(1),
          name: string('Jane Doe'),
          email: string('jane@example.com'),
          roles: eachLike('admin'),
        },
      })
      .executeTest(async (mockServer) => {
        const client = new UserClient(mockServer.url);
        const user = await client.getUser(1);
        expect(user.id).toBe(1);
        expect(user.name).toBeDefined();
      });
  });
});
```

## Provider Verification
```js
const { Verifier } = require('@pact-foundation/pact');

describe('User Provider Verification', () => {
  it('validates consumer contracts', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:3000',
      pactBrokerUrl: process.env.PACT_BROKER_URL,
      pactBrokerToken: process.env.PACT_BROKER_TOKEN,
      provider: 'UserService',
      providerVersion: process.env.GIT_SHA,
      providerVersionBranch: process.env.GIT_BRANCH,
      publishVerificationResult: true,
      stateHandlers: {
        'user with ID 1 exists': async () => {
          await db.users.create({ id: 1, name: 'Jane Doe', email: 'jane@example.com' });
        },
      },
    });
    await verifier.verifyProvider();
  });
});
```

## Schema Evolution Rules
- Backward compatible changes only for existing consumers (add optional fields, never remove/rename required).
- Use versioning (header or media type) when breaking changes are unavoidable.
- Contract tests run in CI for both consumer and provider repos.
- Pact Broker (or equivalent) for sharing contracts + verification results across teams.

## Grok Integration (Production Contract)
- Primary: backend-dev + api-gateway-expert + graphql-expert + test-enforcement/arbiter.
- Fire on_api_feature / on_db_change when public contracts, OpenAPI/GraphQL schema, or event schemas change.
- Pre-Flight (mandatory for any public or multi-consumer API change): "Have we written/updated consumer contract tests? Provider verification in CI? Backward compatible? Versioning strategy if breaking? Pact Broker / contract registry updated? Consumers notified?"
- Ledger: every contract change, new consumer, or verification failure with task_id + consumer list + compatibility decision.
- Handoff: contract diff (Pact or OpenAPI), list of affected consumers, verification status, deprecation timeline if any, test command to run locally.
- Friction + compound: every "we removed a field and 3 consumers broke in prod" or "contract test passed but real client failed on extra field" → compound to stricter linter rules or preflight questions.
- Palace: "Chose header-based versioning (Accept: application/vnd...v2) for public API because clients are external and long-lived; rejected URL /v2 because it pollutes and makes gateway routing harder".
- Claim-verification: Two-pass. Grep "willRespondWith" or "openapi" or "schema" → read_file actual contract test + run provider verification locally → "Contract for GET /users/1 with integer id + roles array exists at contracts/user.pact.ts:22 and provider verification passed ✓VERIFIED". Never claim "backward compatible" or "no breaking change" without reading the contract + running verification.
- Pair with: api-patterns, backend-patterns, test-enforcement, security-review (authz in contracts), preflight, compound-learnings, memory-palace (store "why we versioned this way").

## When to Activate
- Adding or changing any API surface consumed by other teams/services/clients.
- Swarm Phase 2 (API/backend) + Phase 3 (contract review).
- Before deploys that publish new contract versions.
- Any schema or DTO change in shared libraries.
- Cross-team or external integration reviews.

See .grok/skills/api-patterns/SKILL.md, backend-patterns, test-enforcement, preflight. Always run both consumer contract and provider verification. Production Contract: ledger + handoff + preflight + friction on every contract-impacting change.

Contracts are the only thing that prevents "it worked in staging" from becoming "clients are down". Treat them as first-class code.
