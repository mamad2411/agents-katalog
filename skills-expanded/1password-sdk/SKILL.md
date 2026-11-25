---
name: 1password-sdk
description: >-
  How to load secrets and environment variables from 1Password programmatically
  using the official @1password/sdk (JavaScript/TypeScript). Use this skill
  whenever code needs to read a 1Password secret, resolve an op:// reference,
  fetch many secrets at once, discover the fields/sections of a 1Password item
  (e.g. to import API keys), or read a 1Password Environment — even if the user
  doesn't name the SDK explicitly. Triggers on: "@1password/sdk", "op://",
  "OP_SERVICE_ACCOUNT_TOKEN", "DesktopAuth", "resolve a secret from 1Password",
  "1Password service account", "1Password Environments", "fetch API keys from
  1Password", or wiring 1Password into a Node/Bun/TypeScript app. Prefer this
  in-process SDK over shelling out to the `op` CLI unless the task specifically
  needs the user's interactive `op signin` session.
---

# 1Password JavaScript/TypeScript SDK

The official `@1password/sdk` reads secrets from 1Password **in-process** — no `op`
CLI subprocess, no `op signin`. It authenticates directly (service-account token
or desktop biometric) and resolves `op://vault/item/field` references to their
values. Use it whenever an app needs to pull credentials at runtime.

**Why prefer the SDK over the `op` CLI:** one auth model, one authorization
event (the CLI + SDK each prompt separately, so mixing them double-prompts),
no external binary to depend on, batched resolution, and structured per-reference
errors. The CLI's only edge is using a user's existing interactive `op signin`
session — the SDK cannot do that; it needs its own auth (below).

## Install

```bash
bun add @1password/sdk          # or npm install @1password/sdk
```

For **1Password Environments** (the `environments` API), the stable release does
NOT include it — you need the beta:

```bash
bun add @1password/sdk@0.4.1-beta.1
```

## Authenticate — create the client once

Every operation goes through a `client`. `integrationName` and
`integrationVersion` are **required** (they identify your app in 1Password's
audit log — note they do NOT change the desktop authorization prompt, which
always shows the calling process).

```ts
import { createClient, DesktopAuth } from "@1password/sdk";

// Service account — headless / CI / servers. No prompt, no desktop app.
const client = await createClient({
  auth: process.env.OP_SERVICE_ACCOUNT_TOKEN!,
  integrationName: "my-app",
  integrationVersion: "1.0.0",
});

// OR Desktop app — laptops, biometric (Touch ID). Prompts to authorize.
const client = await createClient({
  auth: new DesktopAuth("my-account-name"), // account name or UUID
  integrationName: "my-app",
  integrationVersion: "1.0.0",
});
```

**Choosing auth:**
- `OP_SERVICE_ACCOUNT_TOKEN` → headless, no prompt, but **cannot read Private/Personal
  vaults** (shared vaults only). The token is itself a full-decryption secret — never
  log or persist it.
- `DesktopAuth` → uses the running desktop app, can read your Private vault, prompts
  for Touch ID. Requires the desktop app's SDK integration to be enabled.

`createClient`, and every method below, are **async** — `await` them.

## Resolve secrets — the core operation

```ts
// One secret:
const apiKey = await client.secrets.resolve("op://Vault/Item/credential");

// Many at once (one round-trip, per-reference errors — prefer this for >1):
const res = await client.secrets.resolveAll([
  "op://Vault/Item/username",
  "op://Vault/Item/password",
]);
for (const [ref, response] of Object.entries(res.individualResponses)) {
  if (response.error) { console.error(`failed ${ref}:`, response.error); continue; }
  console.log(response.content.secret); // the value
}
```

Keep resolved secrets **in-memory only** — never write them to disk or logs.

→ Full resolution details (reference syntax, OTP/SSH query params, field types,
validating a reference, the response shapes): **`references/resolve-secrets.md`**

## Read a 1Password Environment (beta)

A named set of env vars managed in the desktop app, addressed by an opaque ID:

```ts
const res = await client.environments.getVariables("<environment-id>");
for (const v of res.variables) {
  process.env[v.name] = v.value;   // { name, value, masked }
}
```

Requires the **beta SDK** and the Environment **ID** (copied from the desktop
app: Developer → View Environments → Manage environment → Copy environment ID).

→ Details + the response shape: **`references/environments.md`**

## Discover an item's fields (for globbed / bulk imports)

When you want to pull *many* fields from one item — e.g. an item whose fields are
each named after an env var (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, …) — you must
discover them first. `items.get()` takes **IDs, not names**, so the flow is:

```ts
// 1. name → vault ID
const vaults = await client.vaults.list();
const vaultId = [...vaults].find(v => v.title === "Jack")!.id;

// 2. name → item ID
const items = await client.items.list(vaultId);
const itemId = items.find(i => i.title === "API keys")!.id;

// 3. fetch the item → fields + sections
const item = await client.items.get(vaultId, itemId);
for (const f of item.fields) {
  // f.title (label), f.sectionId, f.fieldType, f.value
  // join f.sectionId → item.sections[].title for the section label
}
```

**Note:** `items.get()` returns every field's decrypted `value` — there is no
"names without values" mode. This is the same as the `op` CLI's `op item get`
(both decrypt in memory; neither writes to disk), so it's not a security
regression — just don't persist what you don't use.

→ Full glob/discovery recipe (name→ID resolution, section-label joins, building
`op://` references, filtering by a glob): **`references/glob-discovery.md`**

## What the SDK can and cannot do

| Need | SDK | Notes |
|------|-----|-------|
| Resolve `op://` (single + batch) | ✅ | `secrets.resolve` / `resolveAll` |
| Validate a reference syntactically | ✅ | `Secrets.validateSecretReference` (static, no network) |
| List vaults / items, get item fields | ✅ | IDs only — resolve names→IDs yourself |
| Read a 1Password Environment | ✅ beta | `environments.getVariables`, **beta SDK only** |
| Use an existing `op signin` session | ❌ | SDK needs its own token/DesktopAuth |
| Read Private vault headless | ❌ | service accounts = shared vaults only |

## Other languages

The SDK is also available for Go and Python with the same shapes (different
casing/idioms). → **`references/other-languages.md`**
