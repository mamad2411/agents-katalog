# CLAUDE.md — operating guide for agents working in this repository

> This repo is built **by an autonomous "Ralph" loop** (see `ralph/`). You may be that loop,
> or a human-driven session. Either way, read this file first, then `ralph/OPERATING_RULES.md`.

> **2026-07-29 note for the next session (Ralph or human):** a separate task extended the
> **other** tree in this repo — `contracts/`, `test/`, `script/`, `scripts/` (solc 0.8.20,
> Hardhat-primary, what this component's own `README.md`/CI actually build today) — NOT this
> file's `src/`/`ralph/` rewrite. That work added Polygon mainnet-fork tests, a live dual-fork
> Polygon<->Arbitrum cross-chain execution proof, hand-encoded Yul for `DexRouter`'s
> `UNISWAP_V2`/`UNISWAP_V3_SINGLE` calls plus `aavePremiumBps`/`OptimalArbitrage.getAmountOut`,
> and cross-chain-executor deploy support in both deploy scripts. See `../README.md` and
> `../docs/notes-cross-chain-flash-loans.md` for details and results. This Ralph backlog and
> progress log are untouched — Phase 0 is still the starting point for `src/` — but if a future
> iteration considers adding Polygon to *this* tree's scope, the address/DEX research already
> done for the other tree (`contracts/config/addresses.js`) is a real starting point, not a
> blocker to re-derive from scratch.

## What this project is

A **plug-and-play L2 flash-loan arbitrage engine**: gas-optimised Solidity + Yul smart contracts
that borrow via flash loan, route a trade across DEXes, repay the loan, and keep the profit —
**atomically, reverting unless profit ≥ a caller-supplied minimum**. It targets **Optimism, Base,
Ink, Unichain, and Arbitrum One**, and supports same-chain 2-hop / triangular / cross-DEX arbitrage
plus a non-atomic cross-chain 2-hop model. It ships with a multi-language integration SDK and an
off-chain scanner/router/submitter.

The authoritative design lives in `docs/` — the master plan is `docs/BUILD_PLAN.md`, deep specs are
in `docs/specs/`. The ordered, checkable work list the loop executes is `ralph/BACKLOG.md`.

## Golden rules (do not violate)

1. **Profit invariant is sacred.** The executor must never end an arbitrage with the operator/vault
   holding fewer of the profit token than it started with (net of the loan repayment). If a change
   could weaken this, it needs a fuzz/invariant test proving it holds.
2. **Atomic revert is the primary MEV defense.** No partial fills, no "best effort" trades. If the
   realized output is below `minOut`/`minProfit`, the whole transaction reverts.
3. **Validate every callback.** Flash-loan and swap callbacks must assert `msg.sender == expected pool`
   **and** `initiator == address(this)`. An unvalidated callback is a drain vector — treat it as a P0 bug.
4. **Never commit secrets.** No private keys, RPC keys, or `.env` in git. Deploy/keys come from the
   environment. If you find a secret committed, stop and flag it.
5. **Never deploy or send a live transaction from the loop.** The loop writes code, tests, and
   simulations only. Broadcasting to a live chain is a human, gated action.
6. **Stay green.** `bash scripts/verify.sh` must pass before you check a task off. Do not disable,
   `vm.skip`, or weaken a test to make it pass — fix the code or the test's premise.
7. **Do not invent on-chain addresses.** Any address in `config/chains/*.json` marked `"_verify": true`
   (or set to the zero address) is unconfirmed. Never treat it as real; verifying it is its own task.

## How the loop works (one iteration)

1. Read `ralph/OPERATING_RULES.md`, this file, and `ralph/BACKLOG.md`.
2. Pick the **single** highest-priority unchecked task whose dependencies are met.
3. Implement exactly that task. Keep the diff small and reviewable.
4. Run `bash scripts/verify.sh`. If it fails, fix it before doing anything else.
5. Check the task off in `ralph/BACKLOG.md`, append a note to `ralph/PROGRESS.md`, and record any
   durable gotcha in `ralph/MEMORY.md`.
6. Commit with a message like `feat(sizing): closed-form CPMM optimal input [P3-T2]`.
7. Stop. The loop restarts you with a fresh context — the files above are your memory.

## Coding standards

- **Solidity `0.8.24`**, `via_ir = true`. Prefer `custom error` over `require` strings. Use
  `unchecked` only with a comment proving no overflow. Pack storage; cache `SLOAD`s.
- **Yul / inline assembly** is encouraged on the hot path (route decoding, low-level calls, calldata
  packing) but every assembly block gets a comment explaining the memory/stack it touches and a
  differential test against a reference Solidity implementation.
- **Transient storage (EIP-1153)** for reentrancy guards and flash accounting **only on chains that
  support Cancun** — gate via the build profile, keep a `shanghai` fallback (see `foundry.toml`).
- **No `delegatecall` to untrusted code. No unbounded `approve`** — use exact or transient approvals
  / Permit2. Every external contract is behind a typed adapter interface (`src/interfaces/`).
- Every new public/external function gets a Foundry test (happy path + at least one adversarial path).
  Math-bearing code gets a fuzz test. Security-critical invariants get an invariant test.

## Verification gate (`scripts/verify.sh`)

Runs `forge fmt --check`, `forge build`, `forge test`, and (if installed) `slither`. This is the
**definition of done** for every task. CI runs the same script. If a tool isn't installed yet, run
`bash scripts/bootstrap.sh` first.

## Repo map

| Path | What |
|------|------|
| `ralph/` | The autonomous build loop: driver, prompts, rules, backlog, progress, memory. |
| `docs/BUILD_PLAN.md` | Master phased plan (Phase 0–9) with per-phase exit criteria. |
| `docs/ARCHITECTURE.md` | On-chain + off-chain architecture and data flow. |
| `docs/INTEGRATION.md` | How to drop this into any app / language. |
| `docs/specs/` | Deep specs: chains, flash loans, DEX adapters, strategies, sizing, MEV, gas/Yul, security, route codec, cross-chain, off-chain SDK. |
| `config/chains/` | Per-chain address registries (many entries need verification). |
| `src/` | Contracts. `src/interfaces/` is the stable ABI surface; `src/core/` the executor. |
| `test/` | Foundry tests. | 
| `scripts/` | `bootstrap.sh`, `verify.sh`, and (later) deploy scripts. |

When in doubt, the spec in `docs/specs/` wins over guesses. If a spec is missing or wrong, fixing the
spec **is** a valid task — but flag it in `ralph/PROGRESS.md` so the plan stays trustworthy.
