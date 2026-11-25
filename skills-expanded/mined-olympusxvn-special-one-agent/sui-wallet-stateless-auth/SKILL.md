---
name: sui-wallet-stateless-auth
description: >-
  Stateless Sui wallet auth for Vercel serverless — PersonalMessage sign-in,
  sessionStorage proof, per-request signature verify. Use with dapp-kit ConnectButton,
  Next.js API routes, or when in-memory sessions fail across lambda cold starts.
---

# Sui Wallet Stateless Auth

Wallet = identity. No traditional signup. Designed for **serverless** where
in-memory session maps do not survive lambda hops.

**Production context:** [FINAL_FEEDBACK.md](../../../FINAL_FEEDBACK.md)  
**Implementation:** `lib/auth/`, `lib/storage/wallet-auth.ts`,
`app/api/auth/verify/route.ts`

Related: [memwal-multi-tenant-setup](../memwal-multi-tenant-setup/SKILL.md),
[memwal-serverless](../memwal-serverless/SKILL.md).

---

## Flow

```text
Client                          Server
  │ Connect wallet (dapp-kit)
  │ buildAuthMessage(address)
  │ sign PersonalMessage
  │ POST /api/auth/verify ──────► verifyWalletSignature
  │ store proof in sessionStorage ◄── { ok: true }
  │
  │ Each API call (chat, memory…)
  │ body: { walletAddress, authMessage, authSignature }
  └──────────────────────────────► assertWalletAuth(...)
                                     verify OR warm Map fallback
```

---

## Auth message format

```typescript
// lib/auth/messages.ts
`${domain} wants you to sign in with your Sui account:\n${address}\n\nTimestamp: ${unix}`
```

Env: `AUTH_MESSAGE_DOMAIN` / `NEXT_PUBLIC_AUTH_MESSAGE_DOMAIN` (must match).

---

## Client storage

```typescript
// lib/storage/wallet-auth.ts — sessionStorage JSON proof
{ walletAddress, message, signature, verifiedAt }
```

Clear on disconnect / wallet change.

---

## Server verify

```typescript
import { verifyPersonalMessageSignature } from "@mysten/sui/verify";

export async function assertWalletAuth(
  walletAddress: string,
  message?: string,
  signature?: string,
): Promise<{ ok: true } | { ok: false; error: string }> {
  // 1. If message + signature present → verify every time (stateless path)
  // 2. Else fall back to in-memory Map (best-effort on warm lambda only)
  // 3. Else 401 — ask user to sign again
}
```

**Production rule:** Client should **always send** `authMessage` + `authSignature`
with protected API calls so cold lambdas never depend on Map TTL.

---

## API route pattern

```typescript
// POST /api/auth/verify
const valid = await verifyWalletSignature(walletAddress, message, signature);
if (!valid) return NextResponse.json({ error: "Invalid signature" }, { status: 401 });
markWalletVerified(walletAddress);
return NextResponse.json({ ok: true });
```

Protected route:

```typescript
const auth = await assertWalletAuth(walletAddress, authMessage, authSignature);
if (!auth.ok) return NextResponse.json({ error: auth.error }, { status: 401 });
```

---

## ChatContainer integration

On wallet connect → auto sign + verify. On `useChat` transport → attach:

```typescript
body: {
  walletAddress: account.address,
  authMessage: auth.message,
  authSignature: auth.signature,
  // …
}
```

See `components/chat/ChatContainer.tsx`.

---

## UI: connect button

Wrap dapp-kit button for luxury skin:

```tsx
<div className="luxe-connect">
  <ConnectButton connectText="Connect Sui wallet" />
</div>
```

---

## Security notes

- Timestamp in message reduces replay window (regenerate if stale).
- Never trust `walletAddress` without signature verify on mutating routes.
- MemWal namespace derives from verified address only after auth passes.

---

## Repo map

| File | Role |
|------|------|
| `lib/auth/messages.ts` | Message builder |
| `lib/auth/verify-wallet.ts` | Verify + assertWalletAuth |
| `lib/storage/wallet-auth.ts` | sessionStorage proof |
| `app/api/auth/verify/route.ts` | Initial sign-in endpoint |
