---
name: run-tests
description: >-
  Run the opencode-litellm test suite with bun. Use when checking if tests pass,
  running unit tests, running integration tests, debugging a failing test, or
  verifying a change hasn't broken anything. Supports filtering by suite name.
argument-hint: "[unit|integration|<filter>]"
disable-model-invocation: true
allowed-tools: Bash, Read
---
# Run Tests

## Argument Parsing

Parse `$ARGUMENTS`:
- empty → run all unit + integration tests (`bun test`)
- `unit` → run unit tests only (`bun test tests/plugin.test.ts`)
- `integration` → run integration tests only (`bun test tests/integration.test.ts`)
- anything else → pass as a filter pattern (`bun test --testNamePattern "$ARGUMENTS"`)

## Test Structure

| File | Type | What it tests |
|---|---|---|
| `tests/plugin.test.ts` | Unit | Plugin structure, auth hook (multi-prompt authorize), config hook (placeholder write + model fetch) |
| `tests/integration.test.ts` | Integration | Full round-trip against a real in-process mock LiteLLM HTTP server |
| `tests/fixtures/litellm-server.ts` | Fixture | `startMockLiteLLM({ apiKey?, models? })` — Bun HTTP server on `port: 0` |

## Steps

1. Ensure dependencies are installed:
   ```
   bun install
   ```

2. Run tests based on argument:

   **All unit + integration tests:**
   ```
   bun test
   ```

   **Unit only:**
   ```
   bun test tests/plugin.test.ts
   ```

   **Integration only:**
   ```
   bun test tests/integration.test.ts
   ```

   **By name filter:**
   ```
   bun test --testNamePattern "$ARGUMENTS"
   ```

3. Report results. If tests fail, read the failing test file and `src/index.ts`
   to diagnose before suggesting changes.

## Key Testing Patterns

**Mocking fetch (unit tests):**
```typescript
function mockFetchSuccess() {
  const original = global.fetch
  global.fetch = mock(async () => ({
    ok: true,
    json: async () => ({ data: MOCK_MODEL_IDS.map((id) => ({ id })) }),
  })) as any
  return () => { global.fetch = original }
}
// restore in afterEach: restoreFetch?.()
```

**Integration mock server:**
```typescript
const server = startMockLiteLLM({ apiKey?: string, models?: string[] })
// server.url  = "http://localhost:{os-assigned-port}"
// server.port = number
// server.chatRequests = [{ model: string, messageCount: number }, ...]
// server.stop() in afterAll
```

**Config file cleanup:** `beforeEach`/`afterEach` call `clearPluginConfig()`
which wipes `provider.litellm` from `~/.config/opencode/opencode.json` and the
`litellm` credential from `~/.local/share/opencode/auth.json`.

## Error Handling

- If `bun install` fails: check `package.json` and network connectivity
- If unit tests fail with fetch errors: check that `mockFetchSuccess()` is being
  called and restored correctly
- If integration tests fail with ECONNREFUSED: the mock server likely stopped
  early — check `beforeAll`/`afterAll` ordering
