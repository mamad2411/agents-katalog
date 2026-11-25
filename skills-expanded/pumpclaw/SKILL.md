---
name: pumpclaw
description: >
  Execute pump.fun and Raydium LaunchLab token trades via pumpfun-cli. Handles
  buy/sell with smart routing (pump.fun bonding curve or PumpSwap AMM; LaunchLab
  curve or Raydium CPMM, for letsbonk.fun, StonkFun and other launchpads),
  slippage control, priority fees, compute units, and dry-run simulation. Also
  covers pump.fun token launch, migration, wallet management, and token
  discovery. Use when the user wants to trade, swap, buy, sell, launch, or
  manage pump.fun, letsbonk.fun or StonkFun tokens.
compatibility: "Requires uv and pumpfun-cli 0.3 or later (install via uv from github.com/chainstacklabs/pumpfun-cli)"
metadata:
  author: chainstacklabs
  version: "0.3"
  category: crypto-trading
  requires:
    bins: ["uv", "pumpfun"]
    anyBins: ["uv"]
---

# PumpClaw — pump.fun Trading Skill

You are a trading assistant for pump.fun and Raydium LaunchLab coins, operating
through the `pumpfun` CLI.

## Installing pumpfun-cli

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) (handles Python automatically — no separate Python install needed).

```bash
# From GitHub (recommended)
uv tool install git+https://github.com/chainstacklabs/pumpfun-cli.git

# Upgrade
uv tool install --force git+https://github.com/chainstacklabs/pumpfun-cli.git
```

This installs `pumpfun` globally — available from any directory. `pumpfun --version` should report 0.3 or later; older versions can't trade LaunchLab coins and their `migrate` is rejected by the current programs.

## Pre-Trade Checklist

Before any trade, verify:

1. **Wallet exists**: `pumpfun wallet show` — confirms keystore is set up
2. **RPC configured**: `pumpfun config set rpc <url>`, or `PUMPFUN_RPC` env var, or `--rpc` flag
3. **Balance sufficient**: `pumpfun wallet balance` — SOL for fees, plus the coin's quote asset for the spend
4. **Token status**: `pumpfun info <mint>` — which venue the coin trades on (`venue`), whether it has graduated, and which quote asset it is priced in (`quote_symbol`)

## Smart Routing

The CLI finds where a coin trades and routes there; `venue` in every result says which:

| Coin | Before graduation | After graduation |
|---|---|---|
| pump.fun | `bonding_curve` | `pumpswap` (PumpSwap AMM) |
| Raydium LaunchLab: letsbonk.fun, StonkFun, other launchpads | `launchlab` | `cpmm` (Raydium CPMM) |

- `--force-amm` skips the curve and trades in the coin's pool: PumpSwap, or CPMM for a LaunchLab coin
- LaunchLab results also name the launchpad (`platform`)
- A LaunchLab coin that graduated to Raydium AMM v4 instead is refused (`unsupported_venue`)
- `launch`, `migrate`, `claim-cashback`, `collect-creator-fee`, `close-volume-acc` and `tokens` are pump.fun only

Always run `pumpfun info <mint>` first to understand the token's current state.

## Quote Assets

Most coins are priced in SOL, but a coin can be priced in USDC or another mint
pump.fun admits. `buy`, `sell` and `info` read the quote asset from the coin, and
every amount is in it:

- `pumpfun buy <mint> 5` spends 5 SOL on a SOL coin, and 5 USDC on a USDC coin
- buying a non-SOL coin spends that asset, so the wallet must already hold it
- results name the asset in `quote_symbol` (`SOL`, `USDC`, or the mint address)

Check `quote_symbol` in `pumpfun info <mint>` before choosing an amount.

LaunchLab coins are often priced in something other than SOL (USDC, tokenized
stocks, other tokens). The CLI finds such a coin with `getProgramAccounts`, so
it needs an RPC that serves that method.

### Transfer fees

Some LaunchLab coins (StonkFun reward coins, for example) are Token-2022 mints
with a transfer fee: `transfer_fee_bps` in `pumpfun info`. A buy delivers that
much less and a sell sends that much less into the pool, so a round trip loses
the fee twice on top of the trading fees (`curve_fee_pct`, `pool_fee_pct`). The
CLI's amounts already count it; tell the user before trading a coin that has one.

## Core Trading Commands

### Buy tokens
```bash
pumpfun buy <mint> <amount> [--slippage 15] [--force-amm] [--confirm] [--dry-run]
```
- `mint`: token mint address
- `amount`: exact amount to spend, in the coin's quote asset (float)
- `--slippage`: tolerance percent (default: 15)
- `--dry-run`: simulate without sending — **always use this first for new tokens**

### Sell tokens
```bash
pumpfun sell <mint> <amount|all> [--slippage 15] [--force-amm] [--confirm] [--dry-run]
```
- `amount`: token amount or `all` to sell entire balance
- `--dry-run`: simulate without sending

### Token info
```bash
pumpfun info <mint> [--timeout 30]
```
Shows venue, price, quote asset, bonding curve progress, reserves and graduation status. pump.fun coins add whether they are mayhem, cashback or holder-reward; LaunchLab coins add the launchpad (`platform`), `curve_fee_pct`, `transfer_fee_bps`, and once graduated the CPMM pool (`pool_address`, reserves, `pool_fee_pct`).

### Launch a token
```bash
pumpfun launch --name <name> --ticker <ticker> --uri <metadata-json-url> [--buy <amount>] [--quote-mint <mint>] [--creator-fee-bps N] [--holder-reward] [--mayhem] [--confirm]
```
- `--uri` is a metadata JSON (`name`, `symbol`, `description`, `image`) the user already hosts; pump.fun no longer accepts anonymous uploads, so ask the user for one
- `--buy` buys in the same transaction as the create, so nobody can buy first
- `--creator-fee-bps` only applies to a coin priced in a mint pump.fun's QuoteControl admits; the CLI refuses it otherwise
- `--mayhem` only works with SOL as the quote asset

## Safety Guardrails

1. **Always dry-run first**: Use `--dry-run` on buy/sell before committing real funds
2. **Check slippage**: Default 15% is generous — tighten for large trades
3. **Priority fees**: Use `--priority-fee` global option for faster confirmation in congested periods
4. **Compute units**: Use `--compute-units` global option to override default CU limit
5. **Confirm flag**: Add `--confirm` to wait for on-chain confirmation before returning

## Common Workflows

### "Buy X of token Y" (X in the coin's quote asset)
```bash
pumpfun info <mint>                           # Check status & price
pumpfun buy <mint> <X> --dry-run              # Simulate
pumpfun buy <mint> <X> --confirm              # Execute
```

### "Sell all of token Z"
A curve can be short of the quote it owes: a pump.fun sell it can't fully pay
for sells what it can and reports the rest in `tokens_kept`, which stay in the
wallet.
```bash
pumpfun wallet tokens                         # Verify holding
pumpfun sell <mint> all --dry-run             # Simulate
pumpfun sell <mint> all --confirm             # Execute
```

### "Snipe a graduating token"
```bash
pumpfun tokens graduating                     # Find tokens near graduation
pumpfun info <mint>                           # Check specific token
pumpfun buy <mint> <amount> --confirm         # Buy before graduation
```

### "Check and collect fees"
```bash
pumpfun collect-creator-fee --confirm         # Collect SOL fees from pump.fun + PumpSwap
pumpfun collect-creator-fee --quote-mint <mint> --confirm   # Fees earned in another quote asset
pumpfun claim-cashback --confirm              # Claim volume-based rewards
```

## Global Options

These apply to ALL commands:
- `--json` — output as JSON (auto-detected when piping). Trade results carry `quote_symbol`, `quote_mint`, and amounts as `quote_spent` / `quote_received` (dry runs: `quote_in`, `expected_quote`, `min_quote_out`). Exact amounts also have an integer twin in raw units (`quote_spent_raw`, `tokens_sold_raw`, …); use those for arithmetic, since the float can drop a unit. Estimates have no twin: `quote_received`, and `tokens_received` unless the buy ran with `--confirm`. To sell everything, pass `all` rather than an amount
- `--rpc <url>` — override RPC endpoint
- `--keyfile <path>` — override wallet keystore path
- `--priority-fee <micro_lamports>` — priority fee override
- `--compute-units <limit>` — compute unit limit override

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| Wrong password | Wallet decryption failed | Re-enter correct password or set `PUMPFUN_PASSWORD` |
| Insufficient balance | Not enough SOL, or not enough of the coin's quote asset | Check `pumpfun wallet balance`, fund wallet |
| Slippage exceeded | Price moved beyond tolerance | Increase `--slippage` or retry |
| RPC error | Network/endpoint issue | Check `PUMPFUN_RPC`, try different endpoint |
| "No pump.fun or LaunchLab coin found" | Invalid mint, or a coin on another launchpad | Verify the mint with `pumpfun info <mint>`, or find it by name with `pumpfun tokens search <name>` |
| "asks for more than the … tokens left on the bonding curve" | The buy is bigger than what's left on the curve | Spend less |
| "real reserves can't pay anything for these tokens now" | The pump.fun curve can't pay for a sell right now | Nothing was sent; retry later, or after graduation |
| "Too few tokens" | The curve or pool would pay nothing for them | Nothing was sent |
| "CPMM pool is not open yet" | The LaunchLab curve is complete, Raydium hasn't opened the pool | Wait and retry |
| "graduated to Raydium AMM v4" | The LaunchLab coin migrated somewhere this CLI can't trade | Don't trade it with this CLI |
| "getProgramAccounts" | The RPC won't search LaunchLab pools for a coin priced in something other than SOL | Use an RPC that serves `getProgramAccounts` |
| "pump.fun API returned HTTP 403" from `tokens` | pump.fun's listing API is refusing non-browser clients | Listings are unavailable; ask the user for the mint |

## Full Command Reference

See [references/OPERATIONS.md](references/OPERATIONS.md) for complete details on all commands.
See [references/SAFETY.md](references/SAFETY.md) for trading safety guidelines.
See [assets/token-lifecycle.md](assets/token-lifecycle.md) for the bonding curve → graduation → AMM flow.
