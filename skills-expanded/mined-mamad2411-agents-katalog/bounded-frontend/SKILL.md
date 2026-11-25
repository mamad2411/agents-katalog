---
name: bounded-frontend
description: >-
  Wire a web or React Native frontend to Bounded: the @bounded-sh/client SDK
  (reads, writes, subscriptions, queries), hosted static frontends, and end-user
  auth UI (email OTP, OAuth, guest/anonymous accounts and upgrade). Use when
  building the client of a Bounded app or handling how end users sign in. Part of
  the Bounded skill family; server-side rules, functions, and the actor model live
  in the bounded-backend skill, and deploy/hosting config in bounded-deploy.
---

# Bounded frontend

The client side of a Bounded app: the SDK your web or mobile app calls, how end
users authenticate, and how the hosted frontend is served. Policy still governs
every write from the client, so pair this with the **bounded-backend** skill when
a client action needs a rule or invariant, and **bounded-deploy** for hosting and
domains. To route across the family, see the root **bounded** skill.

## Task Router

| User task | Read |
|---|---|
| SDK calls, reads, writes, and subscriptions | [docs/sdk-reference.md](docs/sdk-reference.md) |
| Build a web app frontend | [docs/building-a-webapp.md](docs/building-a-webapp.md) |
| Build for React Native / mobile | [docs/building-for-react-native.md](docs/building-for-react-native.md) |
| Bounded Auth, email OTP, OAuth, guest users, optional text OTP — the canonical login (**every login gets a Crossmint wallet** via `auth.wallets`) | [docs/auth.md](docs/auth.md) |
| **Bring-your-own wallet login** (connect wallet, `walletLogin`, `authMethod:'phantom'`) — the companion to the canonical login | [docs/auth.md](docs/auth.md#solana-wallet-login-bring-your-own) |
| Anonymous users, invite links, account upgrade | [docs/anonymous-accounts.md](docs/anonymous-accounts.md) |
| Hosted frontend and app URLs | [docs/frontend-hosting.md](docs/frontend-hosting.md) |

## Term Router

| If you see | Read |
|---|---|
| `getPage`, `queryAggregate`, `count`, filters, sort, cursor | [docs/sdk-reference.md](docs/sdk-reference.md) |
| `set(path, null)`, delete, `setMany` | [docs/sdk-reference.md](docs/sdk-reference.md#delete--setpath-null) |
| `bounded link`, `bounded login`, email OTP, OAuth, guest sign-in | [docs/auth.md](docs/auth.md) |
| `walletLogin`, `authMethod:'phantom'`, connect wallet, Phantom / Wallet-Standard login | [docs/auth.md](docs/auth.md#solana-wallet-login-bring-your-own) |
| `auth.wallets`, embedded wallet, Crossmint, `@user.address` on an email/social login | [../bounded-onchain/docs/embedded-wallets.md](../bounded-onchain/docs/embedded-wallets.md) |

## Rules Of Thumb

- Every client write is governed by policy; a `403` on a write is a rule denial, not a client bug. See the bounded-backend skill for the rule.
- Denied reads return empty `200` responses, never `403`.
- Put provider API keys in Bounded secrets (backend), never in frontend code.
- **The canonical login gives every user a wallet.** Turn on `auth.wallets` (Crossmint, non-custodial) in policy so every email/social login carries a real `@user.address` alongside its stable `@user.id`. See [embedded-wallets.md](../bounded-onchain/docs/embedded-wallets.md). A purely offchain app may omit the flag; everything else should keep it on.
- **`@user.id` (the account id) is identity/ownership; `@user.address` is the wallet.** Key ownership, membership, and auth guards on `@user.id` (always present). Reach for `@user.address` only for wallet/onchain semantics — never as the identity key.
