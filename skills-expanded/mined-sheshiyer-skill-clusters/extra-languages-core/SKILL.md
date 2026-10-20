---
name: extra-languages-core
description: "Shared reference for the extra-languages cluster: the one decision every niche stack turns on — write the platform's native, current idiom and contain any foreign/legacy runtime behind an adapter boundary — plus version-pinning conventions, a stack × layer matrix, and the trust-boundary guardrails its spokes share. USE WHEN choosing a niche-stack idiom or default dependency, deciding where a legacy/compat layer goes, pinning a toolchain, or scoping whether work belongs here versus a major-language cluster."
cluster: extra-languages
version: 1.0.0
---

# Extra Languages Core

Shared model for the `extra-languages` cluster — the deferred-tier home for niche, platform-
specific language and runtime specialists. The spokes are independent stacks, so the value here
is the **one cross-cutting discipline** they all obey and the rules for keeping the cluster from
drifting into a junk drawer.

## 1. The decision everything turns on: native idiom + contained boundary

A niche stack fails not on algorithms but on **fighting the platform**. The rule:

> **Write the platform's current, native idiom. When you must touch a foreign or legacy runtime,
> isolate it behind an adapter — never let its types leak across the app.**

This has two halves:

- **Native + current.** Use the stack's present-day blessed toolkit, not the one your muscle
  memory or last year's tutorial reaches for. For Solana that means **`@solana/kit` first** for
  client/RPC/transaction code and **framework-kit** (`@solana/client` + `@solana/react-hooks`)
  for UI — *not* `web3.js` by default.
- **Contained boundary.** When a dependency demands the legacy runtime (a lib that wants
  `PublicKey`/`Transaction`/`Connection`), introduce a single adapter module
  (`@solana/web3-compat`) and keep those types out of the rest of the codebase. The boundary is
  a named seam, not a diffusion.

```
app code (native idiom) ──> [adapter / compat seam] ──> legacy or foreign runtime
                            ^ types stop here ^
```

## 2. Scope: what belongs in this cluster

This cluster owns the **long tail** — stacks with no dedicated cluster of their own. Before
adding or routing, check it isn't already owned:

| If the work is… | It belongs in… |
|---|---|
| Solana program / dApp / wallet / tx pipeline | **here** → `solana-dev` |
| General Rust (no chain) | `rust` / `systems-languages` |
| Python / JVM backend | `python-backend` / `jvm` |
| EVM / Ethereum / Solidity | `blockchain-web3` |
| A niche stack with no cluster yet | **here** (as a new spoke) |

**Graduation rule:** when a spoke accumulates enough depth to justify its own orchestrator +
core, promote it out of `extra-languages` rather than letting this cluster bloat.

## 3. Stack × layer matrix (current spokes)

| Stack | UI / client | Core logic | Toolchain & tests | Spoke |
|---|---|---|---|---|
| **Solana** | framework-kit (`@solana/client` + react-hooks); Wallet Standard connect | `@solana/kit` types/codecs; `@solana-program/*` builders; Anchor (iterate) or Pinocchio (CU/footprint) programs | Anchor/Solana CLI pinned; LiteSVM/Mollusk (unit), Surfpool (integration); Codama codegen from IDL | `solana-dev` |

As spokes are added, extend this table — one row per stack, same three layers, so the
orchestrator can route by *(stack, layer)* without reading each spoke.

## 4. Version & toolchain conventions

The long tail breaks on **version drift** more than on logic. Therefore:

- **Pin and state** the language/CLI/framework version for any work (e.g. Anchor + Solana CLI
  pair). Solana's moving target lives in `solana-dev`'s `compatibility-matrix.md`.
- **Recognize toolchain failures as toolchain failures** — GLIBC errors, ABI/CLI mismatches, and
  dependency conflicts are version problems, not code bugs; route them to the spoke's
  `common-errors.md`, don't rewrite working logic.
- Prefer the **newest blessed** API surface; quarantine legacy in the adapter seam (§1).

## 5. Shared guardrails

- **Native idiom first**; legacy/foreign runtime only behind a named adapter boundary.
- **State every trust-boundary fact** before acting — for on-chain work: cluster + RPC/ws
  endpoints, fee payer + recent blockhash, compute budget, expected account owners/signers/
  writability, and the token-program variant (SPL Token vs Token-2022 + extensions).
- **Never silently widen** a security boundary (signing authority, CPI target, account
  writability, scope of a compat adapter) — call it out.
- **Pin the toolchain**; treat version mismatches as the first hypothesis for niche-stack breakage.
- **Deliverables**: exact files changed + diffs, install/build/test commands, and a short risk
  note for anything touching signing/fees/CPIs/transfers.
- **Keep the cluster honest**: only long-tail stacks live here; graduate any that outgrow it.
