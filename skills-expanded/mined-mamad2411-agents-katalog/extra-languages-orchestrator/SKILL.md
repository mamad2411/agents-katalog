---
name: extra-languages-orchestrator
description: "Route a long-tail language / runtime / chain-platform task to the right specialist when it falls outside the major-language clusters (rust, jvm, python-backend, systems-languages). Today the kept specialist is Solana on-chain + dApp development. USE WHEN a user is building in a niche or platform-specific stack — e.g. a Solana program, wallet flow, or transaction pipeline — but hasn't named the exact concern, or you need to decide whether the work belongs here versus a major-language cluster."
cluster: extra-languages
version: 1.0.0
---

# Extra Languages Orchestrator

The entry skill for the **long-tail** of language and runtime work — the specialists that don't
warrant their own first-class cluster yet but still carry real, opinionated, version-sensitive
knowledge. It places the task on the **stack × layer** map, decides whether the work truly
belongs here (versus a major-language cluster), and delegates to the right spoke. The one
cross-cutting rule every spoke shares — *write the platform's native idiom and pin its
toolchain; don't transliterate another language's habits* — lives in `extra-languages-core`;
read it before choosing a stack or a default dependency.

## Cluster map (spoke → role)

| Spoke | Role |
|---|---|
| `extra-languages-core` | Shared model — the platform-native-idiom decision, the boundary-isolation rule, the stack/layer matrix, version-pinning conventions, and guardrails. |
| `solana-dev` | End-to-end Solana playbook — kit-first dApp UI, wallet-standard connect, Anchor/Pinocchio programs, Codama client codegen, LiteSVM/Mollusk/Surfpool testing, security hardening, and toolchain/version-mismatch recovery. |

> This cluster is **deferred tier**: it starts thin and grows by absorbing niche specialists as
> they mature. New stacks join as spokes; ones that outgrow it graduate to their own cluster.

## Routing rules (intent → spoke)

**Decide scope first**
- Work in **Rust** generally (ownership, async, crates, no chain) → not here: route to the **rust** / **systems-languages** cluster.
- General **Python / JVM** backend → not here: **python-backend** / **jvm**.
- Generic EVM / Ethereum / Solidity → not here: **blockchain-web3**.
- A **Solana-specific** task, or a niche stack with no dedicated cluster → continue below.

**Solana — by layer** → `solana-dev`
- dApp UI, wallet connect, signing, transaction/confirmation UX (React/Next.js) → `solana-dev` (framework-kit layer).
- Client SDK / scripts / RPC / transaction building → `solana-dev` (`@solana/kit` layer).
- On-chain program (Anchor for iteration; Pinocchio for CU/footprint) → `solana-dev` (program layer).
- Typed client generation from an IDL (Codama) → `solana-dev` (codegen).
- Local/integration testing (LiteSVM, Mollusk, Surfpool) → `solana-dev` (testing layer).
- Confidential transfers / Token-2022 ZK extension → `solana-dev`.
- Security review / audit-style hardening → `solana-dev` (security).
- **Toolchain setup, GLIBC errors, Anchor/CLI version mismatch, dependency conflicts** → `solana-dev` (compatibility-matrix + common-errors).

**Anything that needs the shared rule** (which idiom? where does the foreign-runtime boundary
go? what version do we pin?) → pull `extra-languages-core` before delegating.

## Standard flow

1. **Scope check** — confirm the task isn't owned by a major-language cluster. If it is, hand it
   off there and stop. Otherwise pick the matching spoke.
2. **Pull the shared model** — if the task touches idiom choice, a foreign-runtime/legacy
   boundary, or toolchain versions, read `extra-languages-core` first.
3. **Delegate** to the spoke; multi-step asks fan out in layer order
   (e.g. "ship a Solana feature" → program → client codegen → UI → tests → security pass).
4. **Return**: chosen spoke(s), the stack/layer located, version or toolchain implications, and
   the next action.

## Guardrails

See `extra-languages-core`. In short: **prefer the platform-native, current-as-of-now stack**
(for Solana: `@solana/kit` + framework-kit; treat `web3.js` as a contained boundary adapter, not
a default) — **isolate any legacy/foreign runtime behind an adapter** instead of letting its
types leak app-wide; **pin and state the toolchain** (CLI, framework, language version) because
this long tail breaks on version drift more than on logic; **never widen a trust boundary**
(signing, fee payer, CPI authority, account writability) without saying so. When a stack
outgrows this cluster, graduate it — don't let `extra-languages` quietly become a dumping ground.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as
skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named
above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md`
inside the skill-clusters repo).
