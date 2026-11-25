---
name: memwal-multi-tenant-setup
description: >-
  MemWal multi-tenant operator setup — one MemWalAccount, delegate key per
  server, namespace per end-user wallet. Use when configuring MemWal mainnet,
  memory.walrus.xyz dashboard, MEMWAL env vars, or per-wallet Walrus namespaces.
---

# MemWal Multi-Tenant Setup

Operator runs **one MemWalAccount**; each user gets an isolated namespace on
that account. Users only connect a Sui wallet in the app — they do not create
their own MemWalAccount.

**Full operator guide:** [docs/MEMWAL_SETUP.md](../../../docs/MEMWAL_SETUP.md)  
**Judges / production lessons:** [FINAL_FEEDBACK.md](../../../FINAL_FEEDBACK.md)  
**MemWal issue:** [#246](https://github.com/MystenLabs/MemWal/issues/246) (Closed)

Related: [memwal-serverless](../memwal-serverless/SKILL.md),
[sui-wallet-stateless-auth](../sui-wallet-stateless-auth/SKILL.md).

---

## Roles

| Role | Does |
|------|------|
| **Operator** | Creates MemWalAccount + delegate key → server env |
| **End user** | Connect wallet + sign message → memory under their namespace |

---

## Setup checklist

```
- [ ] Connect Sui mainnet wallet at memory.walrus.xyz/dashboard
- [ ] Create MemWalAccount → copy MEMWAL_ACCOUNT_ID (object ID)
- [ ] Create delegate key (NOT owner key) → MEMWAL_PRIVATE_KEY
- [ ] Set MEMWAL_SERVER_URL=https://relayer.memory.walrus.xyz
- [ ] Set NEXT_PUBLIC_MEMWAL_ACCOUNT_ID for explorer link in UI
- [ ] npm run memwal:verify
- [ ] Deploy → confirm MemWal 🟢 LIVE badge
```

---

## Environment variables

```bash
MEMWAL_PRIVATE_KEY=0x...          # delegate hex — server only, never commit
MEMWAL_ACCOUNT_ID=0x...           # MemWalAccount object ID
MEMWAL_SERVER_URL=https://relayer.memory.walrus.xyz
NEXT_PUBLIC_MEMWAL_ACCOUNT_ID=0x...  # safe for client — explorer link
NEXT_PUBLIC_SUI_NETWORK=mainnet
```

**Do not** set a global `MEMWAL_NAMESPACE` for multi-tenant apps — namespace is
per wallet at runtime.

---

## Namespace pattern (this repo)

```typescript
// lib/memory/constants.ts
export const AGENT_MEMORY_PREFIX = "mr-toxic-special-one";

export function namespaceForWallet(address: string): string {
  return `${AGENT_MEMORY_PREFIX}-${address.toLowerCase()}`;
}
```

Legacy prefix `special-one-{address}` still read on recall fallback — see
[recall-optimization.md](../memwal-serverless/recall-optimization.md).

---

## Client factory

```typescript
MemWal.create({
  key: delegateKey,
  accountId,
  serverUrl: relayerUrl,
  namespace: namespaceForWallet(walletAddress),
});
```

Cache one client per namespace in a `Map` — see `lib/memory/client.ts`.

---

## Judge-visible proof

| UI | Purpose |
|----|---------|
| **MemWal 🟢 LIVE** | `isMemWalLive()` — keys present |
| SuiScan link | `NEXT_PUBLIC_MEMWAL_ACCOUNT_ID` → object explorer |
| Per-wallet ledger | Proves reads/writes under user namespace |

Explorer example:
`https://suiscan.xyz/mainnet/object/{MEMWAL_ACCOUNT_ID}`

---

## Security rules

1. **Delegate key only** on server — revocable from dashboard (max 20 keys).
2. Never commit `.env.local` or Vercel secrets to git.
3. Users never receive delegate key — wallet signature only.

---

## Verify

```bash
npm run memwal:verify   # checks env shape — not live relayer ping
```

Requested SDK improvement: `healthCheck()` — [#248](https://github.com/MystenLabs/MemWal/issues/248).

---

## Hackathon submission fields

| Field | Value pattern |
|-------|---------------|
| MemWalAccount explorer | SuiScan object link |
| Walrus usage | One namespace per wallet; recall + remember via relayer |
| Memory Moment | Same wallet Day 1 vs Day 4+ |

See [SUBMISSION.md](../../../SUBMISSION.md) and personal skill
`~/.cursor/skills/walrus-hackathon-submission/`.
