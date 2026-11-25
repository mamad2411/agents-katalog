---
name: hodlmm-position-exit
description: "Pure-exit skill for HODLMM concentrated-liquidity positions on Bitflow. Withdraws user DLP from selected bins back to the wallet as raw X/Y token balances via dlmm-liquidity-router-v-1-1::withdraw-liquidity-same-multi. No rebalance, no redeploy, no cross-protocol rotation. Triple-gated with per-bin slippage floors, aggregate min-out, 4h per-pool cooldown, and mempool depth guard. Password prompted interactively — no env var, no CLI flag."
metadata:
  author: "cliqueengagements"
  author-agent: "Micro Basilisk"
  user-invocable: "false"
  arguments: "doctor | status | plan | withdraw"
  entry: "hodlmm-position-exit/hodlmm-position-exit.ts"
  requires: "wallet, bitflow, hodlmm-bin-guardian, hodlmm-move-liquidity"
  tags: "defi, write, mainnet-only, requires-funds"
---

# HODLMM Position Exit

## What it does

Withdraws the user's DLP shares from one or more bins of a Bitflow HODLMM concentrated-liquidity pool back to the wallet as raw X/Y token balances. One atomic transaction per chunk via `SM1FKXGNZJWSTWDWXQZJNF7B5TV5ZB235JTCXYXKD.dlmm-liquidity-router-v-1-1::withdraw-liquidity-same-multi`. Handles selector variants — explicit bin list, `--all`, or `--inactive-only` — plus automatic chunking at 320 bins per tx (router hard cap is 326).

Not a rebalancer. Not a redeployer. Not a yield-router. Exit to wallet, full stop. Other HODLMM skills handle everything else.

## Why agents need it

A HODLMM LP position can go from productive to capital-trapped for several reasons: the active bin drifted past the position, fees stopped paying, or a cross-protocol yield opportunity opened up (e.g. Zest supply APY > HODLMM fee APR). Every one of those cases needs exit-to-wallet as the first step before capital can move. Without this skill an agent either leaves capital stuck in dead bins or hand-crafts the Clarity call — and the closest existing skills (`hodlmm-move-liquidity`, `hodlmm-inventory-balancer`, `hodlmm-range-keeper`) only move liquidity *around* the pool; none exit it.

## Usage

```
bun run skills/hodlmm-position-exit/hodlmm-position-exit.ts <subcommand> [options]
```

## Commands

### `doctor`
Reachability check for the Bitflow APIs, Hiro API, and the DLMM router contract. Read-only, no wallet required.

```bash
bun run skills/hodlmm-position-exit/hodlmm-position-exit.ts doctor --wallet SP219TWC8G12CSX5AB093127NC82KYQWEH8ADD1AY
```

### `status`
List every bin the wallet holds in a pool with expected X/Y token balances and whether each bin is currently the active one. Read-only.

```bash
bun run skills/hodlmm-position-exit/hodlmm-position-exit.ts status --pool dlmm_1 --address SP219TWC8G12CSX5AB093127NC82KYQWEH8ADD1AY
```

### `plan`
Build a withdraw plan and emit the full verdict as JSON. Classifies the proposed withdraw against the triple-gate plus cooldown and emits `safe_to_broadcast: true|false`. Does not sign or broadcast.

```bash
bun run skills/hodlmm-position-exit/hodlmm-position-exit.ts plan \
  --pool dlmm_1 \
  --address SP219TWC8G12CSX5AB093127NC82KYQWEH8ADD1AY \
  --all \
  --slippage-bps 500 \
  --min-position-usd 0.50
```

Selector (mutually exclusive, one required):
- `--bins 617,618,619` — explicit list of bin ids
- `--all` — every bin in the position
- `--inactive-only` — every bin except the currently active one

Gating:
- `--slippage-bps <n>` (default `500` = 5%) — per-bin floor on min X/Y amounts
- `--min-position-usd <n>` (default `0.50`) — triple-gate item 2; rejects dust-exits that would waste gas

### `withdraw`
Execute the withdraw on mainnet. Requires `--confirm`. Prints the exact amounts that will move, then prompts for the wallet password interactively on stderr. Echo is suppressed; the password is never accepted via CLI flag or environment variable, and a TTY is required.

```bash
bun run skills/hodlmm-position-exit/hodlmm-position-exit.ts withdraw \
  --pool dlmm_1 \
  --address SP219TWC8G12CSX5AB093127NC82KYQWEH8ADD1AY \
  --all \
  --confirm
# → prints "══ CONFIRM WITHDRAWAL ══" block + "Wallet password:" prompt on stderr
```

Without `--confirm` the command exits at the plan stage.

## Safety notes

- **Interactive password only.** No `--password` flag, no `WALLET_PASS` env fallback. The skill refuses to sign unless stdin is a TTY. Autonomous loops cannot execute `withdraw` — a human must be at the keyboard.
- **Triple-gate model.** Every `withdraw --confirm` must pass: (1) plan verdict `safe_to_broadcast: true`, (2) position USD ≥ `--min-position-usd`, (3) `--confirm` flag present.
- **4h per-pool cooldown.** Shared state file (`~/.hodlmm-position-exit-state.json`) records the last exit timestamp per pool; subsequent exits on the same pool are blocked with a reason string for 4 hours. Intended to compose with `hodlmm-move-liquidity`'s equivalent cooldown so sequential HODLMM writes do not race.
- **Mempool depth guard.** If the sender has any pending tx at broadcast time, the withdraw aborts with `blocked`. Prevents the stuck-pending class where a withdraw appears to succeed but blocks the next write on the same nonce.
- **Wallet-address match.** The unlocked wallet's STX address must equal `--address`. Catches "wrong wallet unlocked" typos before the signed tx leaves the machine.
- **Slippage at the router, not the client.** The tx's `min-x-amount-total` and `min-y-amount-total` arguments are the authoritative slippage gate — the router reverts with the equivalent of `ERR_MINIMUM_RECEIVED` if the pool under-delivers. Per-bin `min-x-amount` / `min-y-amount` additionally cap slippage at the bin level.
- **Post-condition mode.** `PostConditionMode.Allow` with empty `postConditions: []`. Rationale inline at the call site: DLP burn is internal bin-level accounting (not a SIP-010 FT), so there's no sender-side token outflow to pin. Same precedent as `hodlmm-move-liquidity` (aibtcdev/skills #317) — router arg is the canonical slippage gate. Verified against live mainnet tx `be20b594…` (see proof below).
- **No key persistence.** The password is consumed once by the wallet loader and discarded; never written to disk or emitted in JSON output. Errors never include the password string.

## Output contract

Every subcommand emits a single JSON object to stdout with four fields:

```json
{
  "status": "ok" | "degraded" | "dry-run" | "blocked" | "broadcast" | "error",
  "action": "doctor" | "status" | "plan" | "withdraw",
  "data":   { /* subcommand-specific payload, or null on error */ },
  "error":  null | "descriptive message"
}
```

Per subcommand:

| Subcommand | `status` values | `data` shape |
|---|---|---|
| `doctor`   | `ok`, `degraded`, `error`        | `{ checks: { bitflow_pools, bitflow_bins, hiro_api, router_contract, wallet? } }` |
| `status`   | `ok`, `error`                    | `{ pool, pair, active_bin, bin_count, bins[], totals }` |
| `plan`     | `ok`, `blocked`, `error`         | `{ pool, active_bin, selected_bins[], missing_bins[], plans[], chunks[][], aggregate, usd, cooldown_remaining_ms, blockers[], safe_to_broadcast }` |
| `withdraw`   | `broadcast`, `dry-run`, `blocked`, `error` | `{ pool, bin_count, chunk_count, txids[{ txid, explorer }], aggregate }` |

## Known constraints

- BFF user-positions endpoint returns only DLP shares (no per-bin reserves). The skill falls back to pool-reserves × DLP-share math for the expected-out calculation when reserves come back as `"0"`.
- `--all` on an active-range position exits the active bin too. Use `--inactive-only` to keep the active bin open for post-exit reseeding.
- USD gate is skipped when token prices are unavailable from the pools endpoint (`usd_total === 0`). Callers that want hard-USD gating should either override with a lower `--min-position-usd` or check prices separately.
- Router list cap is 326; this skill chunks at 320. Positions with more than 320 bins require multiple sequential broadcasts, nonce-serialized inside the skill.
- `PostConditionMode.Allow` is intentional and matches the merged `hodlmm-move-liquidity` pattern (see Safety notes). Tightening to `Deny` requires asserting every internal principal-to-principal FT flow the router emits — not attempted in v1.

## HODLMM integration

Yes. The skill is a pure HODLMM operation: reads HODLMM pool + user-position data via the Bitflow App API, calls the HODLMM liquidity router on-chain. Eligible for the HODLMM bonus pool.

## Live proof

Full-position exit on `dlmm_1` (sBTC/USDCx, 10 bps) on 2026-04-19 via the canonical router entrypoint. Tx `be20b594…` settled in block 7,663,125 with `tx_status: success`. 11 bins closed in one atomic transaction; ~$17.45 of trapped capital returned to the signer wallet. Router result: `(ok (tuple (results (list (tuple (x-amount uN) (y-amount uN)) …))))`.

Explorer: https://explorer.hiro.so/txid/0xbe20b59464b94286cd6478483fcdf41b2eec21b2c496ed821aa004fd632e9811?chain=mainnet

Post-exit `status` against the same pool now correctly returns `bin_count: 0` with all totals zeroed.
