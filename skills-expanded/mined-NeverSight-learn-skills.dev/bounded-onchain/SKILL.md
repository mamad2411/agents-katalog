---
name: bounded-onchain
description: >-
  Add onchain to a Bounded app: Solana and EVM collections, embedded
  non-custodial wallets (@user.address on every login, Crossmint), client- and
  server-signed transactions, DEX/perps trading patterns, and crypto payments
  (accept USDC/crypto non-custodially, Bounded Pay for card/fiat). Use for wallet,
  token, on-chain transaction, or crypto/fiat payment work. Part of the Bounded
  skill family; policy and the actor model live in bounded-backend.
---

# Bounded onchain

Wallets, tokens, on-chain transactions, and payments. The **canonical Bounded
login gives every user a wallet**: turn on `auth.wallets` (Crossmint, non-custodial)
and every email/social login carries a real `@user.address` — see
[docs/embedded-wallets.md](docs/embedded-wallets.md). `@user.id` (the account id)
stays the identity/ownership key; `@user.address` is the wallet. On-chain writes
still pass their policy rules and invariants first, so pair this with the
**bounded-backend** skill for the governing rules. To route across the family, see
the root **bounded** skill.

## Task Router

| User task | Read |
|---|---|
| Onchain data / Solana collections | [docs/onchain.md](docs/onchain.md) |
| Trading patterns (Phoenix perps, DEX swaps, server-signed execution) | [docs/onchain-trading.md](docs/onchain-trading.md) |
| **Launch a token** on Meteora — Dynamic Bonding Curve, anti-snipe fee decay, creator/partner fee split, graduation/migration to DAMM v2, claiming fees (`createMeteoraConfig`, `createMeteoraVirtualPool`, `claimDammV2PoolFees`, `withdrawLeftover`) | [docs/meteora-token-launch.md](docs/meteora-token-launch.md) |
| **Split fees between 3+ parties** — the oApps 55/25/20 treasury/creator/Poof model, a multi-party split composed in policy over Meteora's 2-party primitive, atomic permissionless distribute, pre-vs-post-migration phase asymmetry | [docs/oapps-tokenomics-fee-split.md](docs/oapps-tokenomics-fee-split.md) |
| **Sweep fees / run an onchain job on a schedule** — the keeper pattern (offchain schedule → function `actAs` a signer → onchain write, because schedules are rejected on onchain collections), permissionless = reliability-only | [docs/oapps-tokenomics-fee-split.md → the keeper](docs/oapps-tokenomics-fee-split.md#the-keeper--offchain-schedule--function--onchain-write) |
| **Fund build/AI spend from earned fees** — a fee-funded build allowance capped by a proven `rollingSum` burn cap on an append-only log | [docs/oapps-tokenomics-fee-split.md → build allowance](docs/oapps-tokenomics-fee-split.md#the-fee-funded-build-allowance--a-proven-rolling-burn-cap) |
| **The canonical login: give every login a wallet** (`@user.address` for email/social users), embedded/non-custodial wallets, Crossmint, `auth.wallets` | [docs/embedded-wallets.md](docs/embedded-wallets.md) |
| Let users **connect their own Solana wallet** (Phantom / Wallet-Standard) to log in — "connect wallet", wallet login, `walletLogin`, `authMethod:'phantom'`, real wallet as `@user.address`, local `signMessage`/`signTransaction` — the **bring-your-own companion** to the canonical login | [auth.md → Solana wallet login](../bounded-frontend/docs/auth.md#solana-wallet-login-bring-your-own) |
| Accept crypto / USDC, `payments.acceptCrypto`, get paid to a wallet non-custodially, seller settlement + notification, direct-transfer rail, card→crypto rail seam | [docs/accept-crypto.md](docs/accept-crypto.md) |
| Bounded Pay (accept card payments, Stripe Connect, fiat) | [docs/bounded-pay.md](docs/bounded-pay.md) |

## Term Router

| If you see | Read |
|---|---|
| `onchain:true`, `--protocol`, Solana, mainnet permit | [docs/onchain.md](docs/onchain.md) |
| `createMeteoraConfig`, `createMeteoraVirtualPool`, Dynamic Bonding Curve, DBC, bonding curve, anti-snipe / fee decay, token launch, launchpad, graduation, migrate, DAMM v2, `claimDammV2PoolFees`, `withdrawLeftover`, `getDammV2PoolAddress` | [docs/meteora-token-launch.md](docs/meteora-token-launch.md) |
| 3-way / multi-party fee split, 55/25/20, treasury/creator/Poof, oApps tokenomics, `feepool` PDA, `mulDivFloor` split, permissionless distribute, phase asymmetry, `distributionsPost` | [docs/oapps-tokenomics-fee-split.md](docs/oapps-tokenomics-fee-split.md) |
| keeper, scheduled onchain write, `schedule` + `actAs`, offchain → function → onchain, "schedule rejected on onchain collection", crank, sweep fees, `rollingSum` build allowance, fee-funded build credit | [docs/oapps-tokenomics-fee-split.md](docs/oapps-tokenomics-fee-split.md) |
| `walletLogin`, `authMethod:'phantom'`, connect wallet, Phantom login, Wallet-Standard, `window.solana`, SIWS wallet login | [auth.md → Solana wallet login](../bounded-frontend/docs/auth.md#solana-wallet-login-bring-your-own) |
| `@user.address`, embedded wallet, Crossmint | [docs/embedded-wallets.md](docs/embedded-wallets.md) |
| `payments.acceptCrypto`, USDC, seller settlement, direct-transfer rail | [docs/accept-crypto.md](docs/accept-crypto.md) |
| `payment`, `checkout`, `seller`, `merchant`, `subscription`, `Stripe`, `/connect/onboard`, `/connect/status`, `/connect/checkout`, `/connect/session` | [docs/bounded-pay.md](docs/bounded-pay.md) |

## Rules Of Thumb

- **Default onchain login = `auth.wallets` + wallet login, side by side.** Turn on `{ "auth": { "wallets": true } }` in policy so email/social users get a Crossmint wallet (the primary path), and add bring-your-own **wallet login** (`walletLogin`) for users who already hold a Solana wallet. See [docs/embedded-wallets.md → recommended login](docs/embedded-wallets.md#the-recommended-login-for-an-onchain-app). Prescribe this for any onchain app.
- Use `@user.address` only for wallet/onchain semantics; use `@user.id` for normal ownership. See the bounded-backend skill.
- For onchain writes, use explicit network/RPC configuration and devnet by default; do not treat immediate read-after-write as confirmation.
- Bounded Pay's 1% platform fee is in addition to Stripe's own processing fees.
- Crypto is accepted non-custodially; sellers settle to their own wallet.
