---
name: rwa-trade
description: >
  Buy and sell tokenized stocks & ETFs on Solana via the rwa CLI.
  Use when user wants to trade, buy, sell, get a quote, check market hours,
  or list available tokens. Triggers: "buy TSLA", "sell stocks", "trade RWA",
  "quote NVDA", "market hours", "list tokens", "what can I buy on Solana".
---

# RWA Trade

Buy and sell 264 tokenized stocks & ETFs ([Ondo Global Markets](https://ondo.finance/)) on Solana.

## Prerequisites

Assume `rwa` is installed and in PATH. If "command not found", install:
```bash
curl -fsSL https://raw.githubusercontent.com/outputlayer/rwa_cli/main/install.sh | bash
```

Do NOT prepend `export PATH=...` to every command. The installer adds rwa to PATH automatically.

## Agent Guidelines

- **NEVER use `&` (background) for ANY rwa command** — not for quotes, trades, history, or anything else. Jupiter API rejects concurrent requests from the same wallet with HTTP 400. Always run one command at a time, sequentially.
- **Wait between commands**: Add `sleep 3` between consecutive rwa commands. Solana RPC rate-limits aggressively.
- **RPC errors ("Solana RPC unavailable")**: Wait at least 5 seconds before retrying. Do NOT retry immediately. After 3 failures, stop and tell the user to set `RWA_RPC_URL`.
- **Quote requires AMOUNT**: `rwa --json gm quote <SYMBOL> <AMOUNT>`. Amount is mandatory (USDC for buy, tokens for sell).
- **Batch quotes**: Use a sequential loop (NO `&`). Amount is required:
  ```bash
  for sym in TSLA AAPL NVDA SPY; do rwa --json gm quote $sym 100 2>/dev/null; sleep 2; done
  ```
- **Batch history**: Sequential loop (NO `&`):
  ```bash
  for sym in TSLA AAPL NVDA; do rwa --json gm history $sym -r 1W 2>/dev/null; sleep 2; done
  ```
- **Find tokens**: Use `rwa --json gm list --search <keyword>`. NEVER dump full list without `--search`.
- **Buy multiple**: Sequential with sleep:
  ```bash
  rwa gm buy TSLA 100 -y && sleep 5 && rwa gm buy AAPL 100 -y && sleep 5 && rwa gm buy NVDA 100 -y
  ```
- **Sell multiple**: Sequential with sleep:
  ```bash
  rwa gm sell TSLA all -y && sleep 5 && rwa gm sell AAPL all -y && sleep 5 && rwa gm sell NVDA all -y
  ```

## Flags

| Flag | Required for agents |
|------|:---:|
| `--json` | Yes — always use for machine-readable output |
| `-y` | Yes — skip confirmation on buy/sell |
| `--rpc-url <URL>` | No — custom Solana RPC (or `RWA_RPC_URL` env) |

## Workflow

### 1. Check Market Hours

Trading is 24/5: Sunday 8 PM — Friday 8 PM ET.

```bash
rwa --json gm hours
```

### 2. Find Tokens

**ALWAYS use `--search` to filter** — never dump the full list, it wastes tokens:
```bash
rwa --json gm list --search biotech   # Search by sector/keyword
rwa --json gm list --search oil
rwa --json gm list --search defense
rwa --json gm list --search etf
rwa --json gm list --search amgen     # Search by company name
```

Only use `rwa --json gm list` (no filter) if the user explicitly asks for all tokens.
JSON output includes `type` ("stock" or "etf") and cleaned company name.
Both `TSLA` and `TSLAon` symbol formats accepted.

### 3. Get a Quote

```bash
rwa --json gm quote TSLA 100          # Buy: 100 USDC → TSLA
rwa --json gm quote TSLA 5 --sell     # Sell: 5 TSLA → USDC
```

### 4. Execute Trade

```bash
rwa gm buy TSLA 100 -y       # Buy with USDC
rwa gm sell TSLA all -y       # Sell entire position
rwa gm sell SPY 50% -y        # Sell half
```

## Amount Formats

- Exact: `100` (USDC for buy, tokens for sell)
- Percentage: `50%`
- All: `all`

## Key JSON Output

```json
// rwa --json gm quote TSLA 100
{"input":"USDC","output":"TSLAon","in_amount":100.0,"out_amount":0.26,"price":385.0}
```

## Errors & What To Do

The CLI has built-in retry logic (max 2 retries with fresh orders). Most transient errors resolve automatically. **Do NOT manually retry** unless the CLI says the swap failed after retries.

| Error | Cause | Agent action |
|-------|-------|-------------|
| "market closed" | Trading hours ended | Run `rwa --json gm hours`, tell user when it opens |
| "Solana RPC unavailable" | Rate-limited or down | Wait 5s, retry once. After 3 failures, tell user to set `RWA_RPC_URL` |
| "No wallet found" | No keypair | Run `rwa keys generate` |
| "Insufficient SOL for gas" | SOL < 0.01 | CLI auto-topups from USDC. If still fails, user needs to send SOL |
| "Insufficient USDC" | Not enough to buy | Tell user to send USDC to wallet |
| "Balance is 0" | Nothing to sell | Tell user they have no position |
| "Minimum buy amount is 1.0 USDC" | Amount too small | Use at least $1 |
| "Swap failed (code -2003)" | Quote expired between order and execute | CLI auto-retries with fresh order. Do NOT retry manually |
| "Swap failed (code -2004)" | Market maker rejected | CLI auto-retries with fresh order. Do NOT retry manually |
| "Swap failed (code -2005)" | Jupiter internal error | CLI auto-retries with fresh order. Do NOT retry manually |
| "Swap failed (code -1000)" | Transaction didn't land | CLI auto-retries. Do NOT retry manually |
| "No swap route found" | Running commands in parallel with `&` | **STOP.** Run sequentially, one at a time |
| "Jupiter API error (HTTP 400)" | Parallel requests or no liquidity | Stop using `&`. If sequential, token has no liquidity |
| "Jupiter API error (HTTP 429)" | Rate limited | Wait 5s, retry. Never run parallel commands |
| "Quote not available from market maker" | No liquidity for this token | Skip this token, try another |

## Safety — Pre-Trade Checklist

The CLI enforces these checks automatically, but agents should verify upfront to give clear guidance:

1. **Wallet exists**: `rwa keys show` — if fails, run `rwa keys generate` first
2. **Has SOL for gas**: portfolio must show `sol >= 0.005`
3. **Has USDC for buys**: portfolio must show `usdc >= buy amount`
4. **Market is open**: `rwa --json gm hours` must return `"status":"OPEN"`

**Recommended agent flow before any trade:**
```bash
# Step 1: Verify wallet
rwa keys show

# Step 2: Check balances
rwa --json gm portfolio

# Step 3: Check market
rwa --json gm hours

# Step 4: Only then trade
rwa gm buy TSLA 100 -y
```

If any step fails, tell the user what's missing before attempting the trade.
