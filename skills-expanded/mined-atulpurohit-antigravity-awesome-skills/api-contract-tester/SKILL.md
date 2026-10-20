---
name: api-contract-tester
description: "Implement consumer-driven contract testing with Pact to ensure API compatibility."
category: testing
tags: [api,contract,pact,integration,consumer-driven]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# API Contract Tester

## Purpose
Prevent API breaking changes from reaching production by testing contracts between services.

## Pact Contract Testing

### Consumer Test
```javascript
const { Pact, like, term } = require('@pact-foundation/pact');

const provider = new Pact({ consumer: 'WebApp', provider: 'UsersAPI', port: 1234 });

test('GET /users/:id returns user', async () => {
  await provider.addInteraction({
    state: 'user 123 exists',
    uponReceiving: 'a request for user 123',
    withRequest: { method: 'GET', path: '/users/123', headers: { Accept: 'application/json' } },
    willRespondWith: {
      status: 200,
      body: {
        id: '123',
        email: like('user@example.com'),
        name: like('John Doe'),
        role: term({ generate: 'user', matcher: '^(user|admin)$' }),
      },
    },
  });
  const user = await UserService.getUser('123');
  expect(user.id).toBe('123');
});
```

### Provider Verification
```javascript
test('verifies consumers', () =>
  new Verifier({
    provider: 'UsersAPI',
    providerBaseUrl: 'http://localhost:3000',
    pactUrls: ['./pacts/WebApp-UsersAPI.json'],
    stateHandlers: {
      'user 123 exists': () => db.users.upsert({ id: '123', email: 'test@example.com' }),
    },
  }).verifyProvider()
);
```

## Outputs
1. Consumer pact tests
2. Provider verification setup
3. Pact broker configuration
4. CI/CD contract testing integration
5. Contract versioning strategy