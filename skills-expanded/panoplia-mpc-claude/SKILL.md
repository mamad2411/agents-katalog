# CLAUDE.md -- Agent guide for Panoplia MPC

This file gives a Claude agent (or any AI coding assistant) the context needed to work on this codebase effectively.

## What this project is

Panoplia is an Express server that acts as an **always-on MPC co-signer** for a web3 wallet. It uses the `@vultisig/sdk` to participate in threshold-signature ceremonies (keygen and signing) via the Vultisig relay. The user's browser app holds one MPC share, the server holds the other. Neither can sign alone.

This is the **server side only**. A client web app (not in this repo) would run the Vultisig SDK in-browser via WASM and interact with this server's REST API.

## Tech stack

- **Runtime**: Node.js with TypeScript (ESM, `"type": "module"`)
- **Framework**: Express 4 with helmet, cors, express-rate-limit
- **Database**: SQLite via `better-sqlite3` (WAL mode, foreign keys on)
- **Auth**: bcryptjs for password hashing, jsonwebtoken for JWTs
- **Validation**: Zod schemas in middleware
- **MPC**: `@vultisig/sdk` (dynamic import, WASM-based)
- **Recovery**: `shamir-secret-sharing` (Privy's audited implementation)
- **Encryption**: Node.js crypto (AES-256-GCM with scrypt key derivation)
- **Logging**: Pino (pretty in dev, JSON in prod)
- **Testing**: Vitest + supertest, in-memory SQLite

## How to run

```bash
cp .env.example .env   # then set JWT_SECRET and SERVER_MASTER_KEY
npm install
npm run dev            # tsx watch with hot reload
npm test               # 107 tests, all should pass
npm run build          # tsc to dist/
```

## Project layout

```
src/
  index.ts              -- boots server, graceful shutdown
  app.ts                -- Express app factory (middleware + routes)
  config/index.ts       -- env var loader, validates required vars
  db/
    connection.ts       -- SQLite singleton (lazy init, creates data dir)
    migrations.ts       -- 9 tables, idempotent CREATE IF NOT EXISTS
  storage/
    ServerVaultStorage.ts -- implements Vultisig SDK Storage via kv_store table
  services/
    AuthService.ts      -- register/login/getUser, bcrypt + JWT
    VaultCoordinator.ts -- core: keygen, cosign, reshare, import/export
    TransactionService.ts -- thin facade over VaultCoordinator.coSign
    RecoveryService.ts  -- Shamir split/combine, guardian management
  middleware/
    auth.ts             -- requireAuth (JWT verify, attaches req.user)
    errorHandler.ts     -- AppError, ZodError, catch-all
    validate.ts         -- Zod schema middleware factory
  routes/
    index.ts            -- wires services to route groups
    auth.routes.ts      -- /api/auth/{register,login,me}
    vault.routes.ts     -- /api/vaults CRUD + export/import/add-device
    transaction.routes.ts -- /api/vaults/:id/transactions/{sign,list}
    recovery.routes.ts  -- setup/get/revoke + public initiate/submit/complete
  types/index.ts        -- DB row interfaces, DTOs, JwtPayload
  utils/
    crypto.ts           -- encrypt/decrypt (AES-256-GCM, random salt+IV)
    logger.ts           -- Pino singleton
```

## Database (SQLite)

9 tables created in `src/db/migrations.ts`:

| Table | Purpose |
|-------|---------|
| `kv_store` | SDK state per user (namespace, key, value) |
| `users` | Accounts (email unique, bcrypt hash) |
| `vaults` | Vault metadata (status: pending/active/archived) |
| `vault_addresses` | Derived blockchain addresses per vault+chain |
| `transactions` | Tx audit log (status: pending/signed/broadcast/confirmed/failed) |
| `recovery_configs` | Shamir setup per vault (threshold, guardian count) |
| `guardians` | Individual guardian records with encrypted shares |
| `recovery_attempts` | Active recovery sessions (72h expiry) |
| `recovery_shares` | Submitted fragments during recovery |

All IDs are UUIDs (text). Timestamps are ISO 8601 strings via `datetime('now')`.

## Key architectural patterns

**Service layer**: All business logic lives in `src/services/`. Routes are thin -- they validate input, call a service method, and format the response.

**SDK caching**: `VaultCoordinator` maintains a `Map<userId, sdkInstance>` (max 50) to avoid repeated WASM initialization. The SDK is dynamically imported (`await import("@vultisig/sdk")`).

**Background ceremonies**: `createVault` and `coSign` return immediately with session info. The actual MPC ceremony runs in background promises. On success, DB records are updated; on failure, they're marked accordingly. This means the HTTP response returns before keygen/signing finishes.

**Callback-driven flow**: The Vultisig SDK uses callbacks (`onQRCodeReady`, `onDeviceJoined`, `onProgress`). The server wraps these in Promises -- it creates a Promise that resolves when `onQRCodeReady` fires, returns that payload to the client, and lets the ceremony finish in the background.

**Storage adapter**: `ServerVaultStorage` implements the SDK's Storage interface using the `kv_store` table. Each user gets a namespace so SDK state is isolated.

## Working with the Vultisig SDK

The SDK is at version `0.1.0` (deprecated pre-release). Its API:

```typescript
const sdk = new Vultisig({ storage });
await sdk.initialize();

// Keygen
const result = await sdk.createSecureVault({
  name, devices, threshold,
  onQRCodeReady: (qrPayload) => { ... },
  onDeviceJoined: (deviceId, total, required) => { ... },
  onProgress: (step) => { ... },
});

// Join (client side)
const { vault } = await sdk.joinSecureVault(qrPayload, { onProgress });

// Sign
await vault.sign(txPayload, { onQRCodeReady, onDeviceJoined, onProgress });

// Export/import
const base64 = await vault.exportAsBase64(password?);
const vault = await sdk.addVault(file, password?);
```

In tests, the SDK is fully mocked via `vi.mock("@vultisig/sdk")`. The mock simulates callbacks firing after short timeouts.

## Testing approach

107 tests across 15 files in `tests/`:

```
tests/
  setup.ts              -- sets env vars (JWT_SECRET, etc.) before all tests
  helpers.ts            -- createTestDb(), seedUser(), seedVault(), getTestToken()
  unit/                 -- pure logic, no mocking needed
    crypto.test.ts      -- encrypt/decrypt round-trips, tampering, edge cases
    errorHandler.test.ts
    validate.test.ts
    auth-middleware.test.ts
    storage.test.ts     -- ServerVaultStorage CRUD + namespace isolation
    migrations.test.ts  -- schema creation, constraints, idempotency
  integration/          -- services with real DB, mocked SDK
    auth-service.test.ts
    recovery-service.test.ts  -- includes full Shamir round-trip
    vault-coordinator.test.ts -- mocked SDK, real DB
    transaction-service.test.ts
  api/                  -- full HTTP via supertest
    health.test.ts
    auth.test.ts
    vault.test.ts
    transaction.test.ts
    recovery.test.ts    -- end-to-end: setup -> initiate -> submit -> reconstruct
```

Each test gets a fresh in-memory SQLite database via `createTestDb()`. The SDK is mocked at the module level with `vi.mock()`.

**To run**: `npm test` (or `npx vitest run`).

## Common gotchas

- **Express 5 types**: `@types/express@5` types `req.params` values as `string | string[]`. Route handlers that access params must use `Request<{ id: string }>` generic.
- **JWT sign types**: `@types/jsonwebtoken` expects `number | StringValue` for `expiresIn`. We cast with `as string` and `as jwt.SignOptions`.
- **ESM imports**: All local imports use `.js` extensions (`"./config/index.js"`) because TypeScript compiles to ESM.
- **SDK mock**: Tests that use VaultCoordinator or routes that touch it must mock `@vultisig/sdk` before importing the service. The mock fires `onQRCodeReady` via `setTimeout` to simulate async behavior.
- **Background promises**: Vault creation and signing fire background promises. In tests, `afterEach` should wait ~100ms before closing the DB to avoid "database connection is not open" errors from background callbacks.
- **Shamir package**: The package is `shamir-secret-sharing` (by Privy), version `^0.0.4`. API is `split(secret: Uint8Array, n, k): Promise<Uint8Array[]>` and `combine(shares: Uint8Array[]): Promise<Uint8Array>`.

## Adding new features

1. **New endpoint**: Add a Zod schema + handler in the appropriate route file. Wire it through the service layer. Add tests in both `integration/` and `api/`.
2. **New DB table**: Add `CREATE TABLE IF NOT EXISTS` to `migrations.ts`. Add a row type to `types/index.ts`.
3. **New service**: Create in `src/services/`, instantiate in `routes/index.ts`, inject into routes.
4. **Environment config**: Add to `config/index.ts` using `required()` or `optional()`. Document in `.env.example`.
