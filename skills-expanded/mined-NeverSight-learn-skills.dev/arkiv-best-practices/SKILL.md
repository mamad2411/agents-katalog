---
name: arkiv-best-practices
description: Best practices, patterns, and practical examples for building applications with Arkiv — a decentralized Ethereum database with queryable, time-scoped storage. Use this skill whenever the user is working with Arkiv SDK, the @arkiv-network/sdk package, Arkiv entities, Arkiv queries, Arkiv attributes, ExpiresIn/expiration, the Braga testnet, or building any application that stores, queries, or manages data on the Arkiv network. Also use when the user mentions decentralized data storage on Ethereum, blockchain database, Web3 data storage, on-chain data, entity CRUD operations with expiration, arkiv_query, or migrating an Arkiv project from Kaolin to Braga.
---

# Arkiv Best Practices & Practical Examples

Arkiv is a decentralized data layer that brings queryable, time-scoped storage to Ethereum. It lets developers store, query, and manage data with built-in expiration and attribute systems. Think of it as an Ethereum-native database where every record (called an **entity**) has a payload, typed attributes for querying, and a programmable lifespan.

## Architecture Overview

Arkiv uses three layers:

1. **Ethereum Mainnet** — Final settlement, proof verification, source of truth.
2. **Arkiv Coordination Layer** — Data management, registry, cross-chain sync.
3. **Specialized DB-Chains** — High-performance CRUD via JSON-RPC, indexed queries, programmable expiration.

## Core Concepts

### Entities

An entity is a data record containing:

- **Payload** — The actual data (JSON, text, binary)
- **Attributes** — Key-value pairs for querying (string or numeric)
- **ExpiresIn** — Automatic expiration measured in seconds (use `ExpirationTime` helpers)
- **Content Type** — MIME type of the payload

### Attributes

Attributes are the backbone of querying. Use the right type for each attribute because it determines what query operators are available:

```typescript
// String attributes — support eq(), glob matching (~)
{ key: 'type', value: 'note' }
{ key: 'status', value: 'active' }

// Numeric attributes — support eq(), gt(), lt(), gte(), lte() range queries
{ key: 'priority', value: 5 }
{ key: 'created', value: Date.now() }
```

**Important:** If you store a number as a string (`{ key: 'priority', value: '5' }`), you lose the ability to do range queries with `gt()`, `lt()`, etc. Always use numeric values for attributes you plan to filter by range.

### ExpiresIn

Every entity has a lifespan expressed in **seconds**. Always use the `ExpirationTime` helper to convert human-readable durations — never hardcode raw numbers:

```typescript
import { ExpirationTime } from "@arkiv-network/sdk/utils";

ExpirationTime.fromMinutes(30); // 1800 seconds
ExpirationTime.fromHours(1); // 3600 seconds
ExpirationTime.fromHours(12); // 43200 seconds
ExpirationTime.fromHours(24); // 86400 seconds
ExpirationTime.fromDays(7); // 604800 seconds
```

**Important:** The `expiresIn` field takes a value in **seconds**. A raw number like `expiresIn: 3600` means 3600 seconds (1 hour). Always prefer `ExpirationTime.fromMinutes()`, `ExpirationTime.fromHours()`, or `ExpirationTime.fromDays()` for readability and to avoid mistakes.

Entities can be extended before they expire using `extendEntity()`. Over-allocating expiration wastes storage fees — start short and extend if needed.

## SDK Setup

Arkiv provides a TypeScript SDK. For detailed SDK reference, read `references/sdk-reference.md`.

### TypeScript (Node.js / Bun)

```bash
npm install @arkiv-network/sdk
# or
bun add @arkiv-network/sdk
```

Before suggesting `import { braga } from "@arkiv-network/sdk/chains"`, check that the project is using `@arkiv-network/sdk` version `0.6.5` or higher. Do not pin the install command unless the user explicitly asks for that; instead, tell the agent to verify the currently installed version and upgrade only if needed.

Two client types exist:

1. **WalletClient** (read/write) — Requires a private key. Use for creating, updating, deleting entities.
2. **PublicClient** (read-only) — No private key needed. Use for queries.

```typescript
import {
  createWalletClient,
  createPublicClient,
  http,
} from "@arkiv-network/sdk";
import { privateKeyToAccount } from "@arkiv-network/sdk/accounts";
import { braga } from "@arkiv-network/sdk/chains";

// Write operations — keep private key in env vars, never hardcode
const walletClient = createWalletClient({
  chain: braga,
  transport: http(),
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
});

// Read operations — safe for frontend/public use
const publicClient = createPublicClient({
  chain: braga,
  transport: http(),
});
```

Braga is the current Arkiv testnet. If you are upgrading an existing Kaolin project, read `references/migration-guide.md` before editing code so you update chain imports, RPC URLs, wallet config, and seed data together.

## CRUD Operations

### Create

```typescript
import { jsonToPayload, ExpirationTime } from "@arkiv-network/sdk/utils";

const { entityKey, txHash } = await walletClient.createEntity({
  payload: jsonToPayload({ title: "My Note", content: "Hello Arkiv!" }),
  contentType: "application/json",
  attributes: [
    { key: "type", value: "note" },
    { key: "id", value: crypto.randomUUID() },
    { key: "created", value: Date.now() },
  ],
  expiresIn: ExpirationTime.fromHours(12),
});
```

### Read / Query

```typescript
import { eq, gt } from "@arkiv-network/sdk/query";

const query = publicClient.buildQuery();
const result = await query
  .where(eq("type", "note"))
  .where(gt("created", Date.now() - 86400000))
  .withPayload(true)
  .withAttributes(true)
  .limit(10)
  .fetch();

console.log("Found entities:", result.entities);

// Pagination — fetch the next page if one exists
if (result.hasNextPage()) {
  await result.next();
  console.log("Next page:", result.entities);
}

// Get a specific entity by key
const entity = await publicClient.getEntity(entityKey);
```

### Update

```typescript
await walletClient.updateEntity({
  entityKey: entityKey,
  payload: jsonToPayload({ title: "Updated", content: "New content" }),
  contentType: "application/json",
  attributes: [
    { key: "type", value: "note" },
    { key: "updated", value: Date.now() },
  ],
  expiresIn: ExpirationTime.fromHours(24),
});
```

### Delete

```typescript
await walletClient.deleteEntity({ entityKey });
```

### Extend Expiration

```typescript
await walletClient.extendEntity({
  entityKey: entityKey,
  expiresIn: ExpirationTime.fromHours(1), // always use the helper
});
```

## Best Practices

### 1. Always Use a Project Attribute

All entities in Arkiv are public and stored in a shared database. Every project **must** define a unique project attribute and include it on every entity. This is how you distinguish your app's data from everyone else's.

Create a dedicated file (e.g., `lib/arkiv.ts` or `constants/arkiv.ts`) that exports this attribute:

```typescript
/** All entities created by this app share this attribute for easy filtering. */
export const PROJECT_ATTRIBUTE = {
  key: "project",
  value: "<GLOBALLY_UNIQUE_STRING_THAT_IDENTIFIES_THE_PROJECT>",
} as const;

if (!PROJECT_ATTRIBUTE.value) {
  throw new Error(
    "Please set the value of PROJECT_ATTRIBUTE to a unique string that identifies your project. This will help you filter and manage your entities on the Arkiv network.",
  );
}
```

When creating this file, come up with a globally unique value — for example, a combination of your project name, organization, and a short random suffix (e.g., `"myapp-acme-7x9k"`).

Then include `PROJECT_ATTRIBUTE` in **every** create/update call and **every** query:

```typescript
// Creating — always include PROJECT_ATTRIBUTE
const { entityKey, txHash } = await walletClient.createEntity({
  payload: jsonToPayload({ title, content }),
  contentType: "application/json",
  attributes: [PROJECT_ATTRIBUTE, { key: "entityType", value: "post" }],
  expiresIn: ExpirationTime.fromDays(30),
});

// Querying — always filter by PROJECT_ATTRIBUTE
const result = await query
  .where([
    eq(PROJECT_ATTRIBUTE.key, PROJECT_ATTRIBUTE.value),
    eq("entityType", "post"),
  ])
  .withPayload(true)
  .withMetadata(true)
  .limit(50)
  .fetch();
```

Without this, your queries will return data from other projects, and other projects will see yours. This is the single most important practice for any Arkiv project.

### 2. Separate Read and Write Clients

Always use `createPublicClient` for queries. It prevents accidental writes, doesn't require a private key, and is safe for frontend/public use. Reserve `createWalletClient` for backend services that need to create/update/delete.

### 3. Design Attributes for Queryability

Think about how you'll query data when you choose attributes. Attributes are your indexes — without the right ones, you'll be fetching too much data and filtering client-side.

```typescript
// Good: attributes map to your query patterns
attributes: [
  { key: "type", value: "vote" }, // filter by entity type
  { key: "proposalKey", value: proposalId }, // link related entities
  { key: "voter", value: voterAddr }, // filter by user
  { key: "choice", value: "yes" }, // filter by value
  { key: "weight", value: 1 }, // numeric for aggregation
];
```

### 4. Use Batch Operations

Individual creates in a loop are slow and expensive. Use `mutateEntities()` for batch creates:

```typescript
// Bad — sequential, slow
for (const item of items) {
  await walletClient.createEntity(item);
}

// Good — single batch operation
await walletClient.mutateEntities({
  creates: items.map((item) => ({
    payload: jsonToPayload(item.data),
    contentType: "application/json",
    attributes: item.attributes,
    expiresIn: ExpirationTime.fromHours(1),
  })),
});
```

### 5. Write Specific Queries

Broad queries return too much data and cost more. Always add multiple filter criteria:

```typescript
// Bad — returns every note ever
await query.where(eq("type", "note")).fetch();

// Good — narrows down to what you actually need
await query
  .where(eq("type", "note"))
  .where(gt("created", Date.now() - 86400000))
  .where(gt("priority", 3))
  .fetch();
```

### 6. Right-Size Expiration

Match `expiresIn` to actual data lifetime. Session data gets 30 minutes, not 7 days. Cache gets 1 hour. Don't over-allocate — it costs more and pollutes queries with stale data before cleanup.

### 7. Never Expose Private Keys

```typescript
// Always load from environment
const privateKey = process.env.PRIVATE_KEY;

// Never hardcode
const privateKey = "0x1234..."; // DANGEROUS
```

### 8. Validate Input Before Storing

Check length and content before creating entities. Arkiv stores what you give it — garbage in, garbage out.

### 9. Use Numeric Types for Numeric Data

If you'll filter or sort by a value, store it as a number attribute. String attributes only support equality and glob matching.

### 10. Model Related Data with Shared Attributes

Link entities together using a shared attribute key (like `proposalKey` in a voting system). This is Arkiv's version of foreign keys:

```typescript
// Proposal entity
attributes: [{ key: "type", value: "proposal" }];

// Vote entities reference the proposal
attributes: [
  { key: "type", value: "vote" },
  { key: "proposalKey", value: proposalEntityKey },
];

// Query all votes for a proposal
await query
  .where(eq("type", "vote"))
  .where(eq("proposalKey", proposalEntityKey))
  .fetch();
```

### 11. Understand $owner vs $creator

Every Arkiv entity has two special metadata fields:

- **$owner** — The wallet address that currently owns the entity. The owner has permission to update, delete, and extend the entity. **Ownership can be transferred**, so the owner may change over an entity's lifetime.
- **$creator** — The wallet address that originally created the entity. This is **set at creation time and is immutable** — it can never change. Being the creator does not grant any special privileges (only the owner can modify/delete).

Query these with `.ownedBy()` and `.createdBy()`, or include them in results with `.withMetadata(true)`:

```typescript
// Filter by current owner
const owned = await publicClient
  .buildQuery()
  .where(eq(PROJECT_ATTRIBUTE.key, PROJECT_ATTRIBUTE.value))
  .ownedBy("0xOwnerAddress")
  .withPayload(true)
  .withMetadata(true)
  .fetch();

// Filter by original creator (immutable, tamper-proof)
const created = await publicClient
  .buildQuery()
  .where(eq(PROJECT_ATTRIBUTE.key, PROJECT_ATTRIBUTE.value))
  .createdBy("0xCreatorAddress")
  .withPayload(true)
  .withMetadata(true)
  .fetch();
```

**When to use which:**

- Use **$creator** (`createdBy`) when you need a tamper-proof guarantee of who originally wrote the data (e.g., verifying data came from your trusted backend). Since it's immutable, it cannot be spoofed after creation.
- Use **$owner** (`ownedBy`) when you need to know who currently controls the entity (e.g., checking who can modify it). Be aware that ownership can change.

### 12. Filter by Creator Wallet for Trusted Data

When your app has a backend that publishes data to Arkiv and a frontend that reads it, filtering by `PROJECT_ATTRIBUTE` alone is **not enough**. A malicious actor can create entities with your project attribute to inject fake data into your dashboard.

The solution: combine `PROJECT_ATTRIBUTE` filtering with `.createdBy()` to only accept entities created by your trusted backend wallet:

```typescript
// lib/arkiv.ts — export your trusted backend wallet address
export const PROJECT_ATTRIBUTE = {
  key: "project",
  value: "myapp-acme-7x9k",
} as const;

/** The wallet address of the backend that publishes trusted data. */
export const CREATOR_WALLET_ADDRESS = "0xYourBackendWalletAddress";
```

```typescript
// Reading trusted data only
import { PROJECT_ATTRIBUTE, CREATOR_WALLET_ADDRESS } from "@/lib/arkiv";

const trustedPosts = await publicClient
  .buildQuery()
  .where([
    eq(PROJECT_ATTRIBUTE.key, PROJECT_ATTRIBUTE.value),
    eq("entityType", "post"),
  ])
  .createdBy(CREATOR_WALLET_ADDRESS)
  .withPayload(true)
  .withMetadata(true)
  .fetch();
```

This works because `$creator` is immutable — no one can create an entity and fake the creator address. Even if someone creates an entity with your project attribute, it won't pass the `.createdBy()` filter unless it was actually created by your whitelisted wallet.

**Use this pattern whenever:**

- Your backend publishes data that a frontend/dashboard reads
- You need to trust the source of entities
- You're building any system where data integrity matters

### 13. Handle Errors Gracefully

The Arkiv SDK does not retry on failure — all methods throw on error. Write operations (create, update, delete, extend) can fail for several reasons: the user rejects the transaction in MetaMask, the wallet has insufficient gas, the RPC endpoint is unreachable, or the entity has already expired. Wrap write operations in try/catch and handle each failure mode appropriately:

```typescript
try {
  const { entityKey, txHash } = await walletClient.createEntity({
    payload: jsonToPayload({ title: "My Post" }),
    contentType: "application/json",
    attributes: [PROJECT_ATTRIBUTE, { key: "entityType", value: "post" }],
    expiresIn: ExpirationTime.fromHours(12),
  });
} catch (error) {
  // Common failures:
  // - User rejected the transaction (MetaMask popup dismissed)
  // - Insufficient funds / gas
  // - Network error (RPC unreachable)
  // - Entity already expired (for update/extend)
  console.error("Transaction failed:", error);
}
```

Read operations (`buildQuery().fetch()`, `getEntity()`) can also throw on network errors. If your app needs retries, implement them yourself — the SDK won't do it for you.

### 14. Validate Entity Data and Model Relationships

Two important advanced patterns for production Arkiv apps:

- **Schema validation** — `entity.toJson()` returns `any`. Always validate with a schema library (zod, valibot, etc.) to protect against malformed payloads and namespace collisions.
- **Relationship entities** — Arkiv attributes are flat key-value pairs with no array type. To model one-to-many or many-to-many relationships (tags, skills, memberships), create separate relationship entities instead of encoding lists into attributes.

For full examples and code for both patterns, read `references/advanced-patterns.md`.

## Migration from Kaolin to Braga

When a user wants to upgrade an existing Arkiv project, treat it as a migration instead of a generic refactor. The SDK API is unchanged; the main work is swapping the target chain, updating wallet/network config, renaming Kaolin-specific env vars, and recreating testnet data that lived on Kaolin.

Follow this sequence:

1. Read `references/migration-guide.md` before making edits.
2. Check the installed `@arkiv-network/sdk` version first. The `braga` chain export is only available in `0.6.5` or higher.
3. Replace `kaolin` chain imports/usages with `braga`.
4. Update RPC URLs, WebSocket URLs, chain IDs, explorer links, faucet links, and wallet `nativeCurrency` from ETH to GLM.
5. Rename env vars and config keys so `KAOLIN_*` names do not remain in active codepaths.
6. Re-seed or recreate any entities the app expects on startup, because Kaolin state does not migrate to Braga.

Keep Kaolin only as legacy context during migration work. For new code, examples, and setup instructions, default to Braga.

## Reference Files

The `references/` directory contains detailed documentation for specific topics. Read these when you need deeper information:

- **`references/sdk-reference.md`** — Full SDK API surface: all WalletClient/PublicClient methods, query builder API, ExpirationTime helpers, payload utilities, MetaMask browser usage, and CDN imports.
- **`references/integration-patterns.md`** — Three integration scenarios: backend read/write (Next.js/Express), client-side reading (TanStack Query hooks), and client-side writing (MetaMask and wagmi/RainbowKit).
- **`references/api-reference.md`** — Raw JSON-RPC 2.0 API: `arkiv_query` syntax, query operators, synthetic attributes (`$owner`, `$creator`, `$key`), pagination with cursors, and utility methods.
- **`references/advanced-patterns.md`** — Advanced data modeling: schema validation with zod/valibot, and modeling lists with relationship entities.
- **`references/migration-guide.md`** — Step-by-step Kaolin to Braga migration checklist: chain swaps, env/config updates, wallet settings, faucet, bridge changes, and reseeding testnet data.

## Testnet Resources

| Resource | URL                                            |
| -------- | ---------------------------------------------- |
| Chain ID | `60138453102`                                  |
| HTTP RPC | `https://braga.hoodi.arkiv.network/rpc`        |
| Faucet   | `https://braga.hoodi.arkiv.network/faucet/`    |
| Explorer | `https://explorer.braga.hoodi.arkiv.network/`  |

## Troubleshooting

- **"Invalid sender"** — Your RPC URL may point to the wrong network. Verify it matches Braga.
- **"Insufficient funds"** — Get test GLM from the Braga faucet. Writes require gas.
- **Queries return empty** — Check that attributes match exactly (case-sensitive). Verify entities haven't expired.
