---
name: nostr-agent-cryptographic-peer
description: Applies the Buzz project's Nostr-native agent-membership pattern (Sept 8, 2026) — AI agents hold their own keypairs and sign every action into the same event log as human teammates — as the CRYPTOGRAPHIC-PEER pattern for agent identity, auditability, and attribution, plus OpenSats' $36.6M/413-grantee pass-through funding wave as the capital layer beneath it. Use when designing agent identity/audit systems, evaluating decentralized protocols as agent infrastructure, or comparing grant funding models for OSS.
---

# Nostr Agent as Cryptographic Peer

## Overview
Buzz (NostrMag analysis, Sept 8, 2026) treats AI agents as full network members — own keypairs, same signed event log as humans — turning agent identity from a permission flag into a cryptographic fact, while OpenSats' $36.6M / 413-grantee allocation (announced Sept 7, 2026) supplies the funding model that makes such protocol-native infrastructure sustainable.

## When to Use
- Designing agent identity, audit, or provenance systems where "who did it" must be verifiable across human and AI actors
- Evaluating Nostr, ActivityPub, Cashu, or similar open protocols as substrate for multi-agent systems
- Comparing open-source funding models (pass-through grant pools vs corporate sponsorship vs patronage)
- NOT for: agent-payment rails (that is x402/AP2/MPP territory), centralized bot-permission systems, or on-chain identity ledgers with different trust models

## Core Process / Workflow

### The cryptographic-peer pattern (Buzz)
1. **Identity**: each agent gets its own Nostr keypair — same as a human teammate. No permission flags, no bot registry.
2. **Attribution**: every message, code review, and workflow step is a signed event in the same event log, regardless of human or machine origin. Audit = replay the log.
3. **Trust boundary**: trust follows the signature, not a central permission system. A compromised agent is a compromised key, not a compromised platform account.
4. **Scale evidence (vendor-internal)**: BuilderBot executes 200,000+ operations/day, merges 1,500+ PRs/week, accounts for ~15% of production code changes.

### The funding layer (OpenSats)
- 501(c)(3) public charity; **100% pass-through** — operational costs covered separately, every grant dollar reaches a recipient
- **$36.6M in Bitcoin to 413 grantees across 40+ countries**; Nostr Fund as one of two primary pools
- Major donors: Jack Dorsey's #startsmall, the Reynolds Foundation; monthly disbursements ~$1M; Q2 2026: 36 BTC sent for $12.51 in fees
- Adjacent: Jack Dorsey's $10M to "and Other Stuff" (May 2026 collective: Nostr, ActivityPub, Cashu; "community of hackers" rejecting VC structures; ethical guidelines for privacy/interoperability/transparency)

### Design workflow
1. Model agents as key-holding peers; give each agent a dedicated key with scoped spending/authority
2. Route every action through the signed event log (messages, reviews, workflow steps, decisions)
3. Separate identity keys from payment keys (Cashu/LN for money, Nostr for attribution)
4. Audit by replay: reconstruct any decision chain from signatures alone
5. Fund the commons deliberately: budget pass-through grants for protocol-native tooling rather than concentrating capital in one corporate patron

## References
- See [references/evidence-base.md](references/evidence-base.md) for the full source detail, numbers, and caveats.

### Pairs with
`agent-payment-record-gap` (the mandate-vs-payment record gap — this skill's event log is the record layer), `erc8004-empirical-trust-reality-check-2026` (on-chain trust), `ant-amp-kya-interoperability` (wallet-scale identity), `oss-endowment-and-coop-funding-2026`, `open-source-funding-channels-2026`, `agentic-oss-economics-2026` (the funded counterweight layer), `github-india-agentic-oss-growth`.

## A-Tech Alignment
- **Open source:** Nostr is an open protocol; the identity/audit pattern is implementable without any vendor lock-in.
- **Privacy:** signatures attribute actions without central identity providers; key separation limits correlation.
- **Financial freedom:** pass-through grant funding + agent keypads = funding and identity that no platform can revoke.
- **Practical:** a five-step rollout from keypair to audit-replay is deployable by a two-person team.

## Honesty Caveats
- Buzz's 200K ops/day and 1,500+ PRs/week are **vendor-internal, unaudited** figures (single NostrMag analysis; no code published).
- NostrMag's framing is a bullish editorial synthesis, not neutral reporting; adoption hurdles for decentralized social remain real.
- OpenSats numbers are grantee-breadth not per-project depth; the 413-grantee spread means small checks, not concentrated funding.
- Grant funding ≠ sustainable development: OpenSats has not published survival rates for funded projects.