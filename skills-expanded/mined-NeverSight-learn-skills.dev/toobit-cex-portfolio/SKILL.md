---
name: toobit-cex-portfolio
description: "This skill should be used when the user asks about 'account balance', 'how much USDT do I have', 'my wallet', 'show my balance', 'sub-accounts', 'balance flow', 'transaction history', 'deposit address', 'deposit history', 'withdrawal history', 'withdraw funds', 'sub-account transfer', 'check API key', 'API key permissions', 'audit log', 'trade history', or any request to view account information, deposit/withdraw, or manage sub-accounts on Toobit CEX. Requires API credentials. Do NOT use for market prices (use toobit-cex-market), or placing/cancelling orders (use toobit-cex-trade)."
license: MIT
metadata:
  author: toobit
  version: "1.0.0"
  homepage: "https://www.toobit.com"
  agent:
    requires:
      bins: ["toobit"]
    install:
      - id: npm
        kind: node
        package: "toobit-trade-cli"
        bins: ["toobit"]
        label: "Install toobit CLI (npm)"
---

# Toobit CEX Portfolio & Account CLI

Account balance, sub-accounts, balance flow, deposits, withdrawals, and API key management on Toobit exchange. **Requires API credentials.**

## Prerequisites

1. Install `toobit` CLI:
   ```bash
   npm install -g toobit-trade-cli
   ```
2. Configure credentials in `~/.toobit/config.toml`:
   ```toml
   default_profile = "live"

   [profiles.live]
   api_key    = "your-api-key"
   secret_key = "your-secret-key"
   ```
   Or set environment variables:
   ```bash
   export TOOBIT_API_KEY=your_key
   export TOOBIT_SECRET_KEY=your_secret
   ```
3. Verify credentials:
   ```bash
   toobit account check-api-key
   ```

## Credential Check

**Run this check before any authenticated command.**

```bash
toobit account check-api-key    # verify API key status and permissions
```

- If the command returns an error: **stop all operations**, guide the user to edit `~/.toobit/config.toml`, and wait for setup to complete before retrying.
- If credentials are valid: proceed with the requested operation.

### Handling Authentication Errors

If any command returns a 401 / -2015 authentication error:
1. **Stop immediately** — do not retry the same command
2. Inform the user: "Authentication failed. Your API credentials may be invalid, expired, or IP not whitelisted."
3. Guide the user to update credentials:
   ```
   ~/.toobit/config.toml
   ```
4. After the user confirms the file is updated, run `toobit account check-api-key` to verify
5. Only then retry the original operation

## Skill Routing

- For market data (prices, charts, depth, funding rates) → use `toobit-cex-market`
- For account balance, sub-accounts, deposits, withdrawals → use `toobit-cex-portfolio` (this skill)
- For spot/futures orders, leverage, margin, flash close → use `toobit-cex-trade`

## Quickstart

```bash
# Account balance (all tokens)
toobit account info

# Balance flow (transaction history)
toobit account balance-flow --tokenId USDT --limit 20

# Sub-account list
toobit account sub-accounts

# Check API key permissions
toobit account check-api-key

# Get deposit address for USDT
toobit account deposit-address --tokenId USDT

# Recent deposit history
toobit account deposits --tokenId USDT --limit 10

# Recent withdrawal history
toobit account withdrawals --tokenId USDT --limit 10

# Audit log (tool call history)
toobit account audit --limit 10
```

## Command Index

### Read Commands

| # | Command | Type | Description |
|---|---|---|---|
| 1 | `toobit account info` | READ | Account balance (all tokens with balance > 0) |
| 2 | `toobit account balance-flow` | READ | Balance flow / transaction history |
| 3 | `toobit account sub-accounts` | READ | List sub-accounts |
| 4 | `toobit account check-api-key` | READ | API key status and permissions |
| 5 | `toobit account deposit-address` | READ | Get deposit address for a token |
| 6 | `toobit account deposits` | READ | Deposit order history |
| 7 | `toobit account withdrawals` | READ | Withdrawal order history |
| 8 | `toobit account audit` | READ | Tool call audit log (trade history) |

### Write Commands

| # | Command | Type | Description |
|---|---|---|---|
| 9 | MCP `account_withdraw` | WRITE | Withdraw funds to an external address |
| 10 | MCP `account_sub_transfer` | WRITE | Transfer funds between main and sub-accounts |

## Cross-Skill Workflows

### Pre-trade balance check
> User: "I want to buy 0.1 BTC — do I have enough USDT?"

```
1. toobit-cex-portfolio toobit account info                           → check USDT balance
2. toobit-cex-market    toobit market ticker --symbol BTCUSDT          → check current price
        ↓ user approves
3. toobit-cex-trade     toobit spot place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.1
```

### Review account and positions
> User: "Show me my account overview"

```
1. toobit-cex-portfolio toobit account info                           → spot account balance
2. toobit-cex-trade     toobit futures balance                         → futures account balance
3. toobit-cex-trade     toobit futures positions                       → open positions
4. toobit-cex-market    toobit market ticker --symbol BTCUSDT          → current price for reference
```

### Deposit and trade flow
> User: "Where do I deposit USDT? Then I want to trade BTC"

```
1. toobit-cex-portfolio toobit account deposit-address --tokenId USDT → get deposit address
        ↓ user deposits and confirms
2. toobit-cex-portfolio toobit account deposits --tokenId USDT        → verify deposit arrived
3. toobit-cex-portfolio toobit account info                           → confirm balance updated
        ↓ ready to trade
4. toobit-cex-trade     toobit spot place --symbol BTCUSDT --side BUY ...
```

### Check balance flow after trading
> User: "Show me my recent transaction history"

```
1. toobit-cex-portfolio toobit account balance-flow --tokenId USDT --limit 20 → recent flow
2. toobit-cex-trade     toobit spot fills --symbol BTCUSDT                    → recent spot fills
3. toobit-cex-trade     toobit futures fills --symbol BTC-SWAP-USDT           → recent futures fills
```

### Sub-account management
> User: "Transfer 100 USDT to my sub-account"

```
1. toobit-cex-portfolio toobit account sub-accounts                   → list sub-accounts, get subAccountId
2. toobit-cex-portfolio toobit account info                           → confirm main account has ≥ 100 USDT
        ↓ user approves
3. toobit-cex-portfolio (MCP) account_sub_transfer                    → transfer 100 USDT
4. toobit-cex-portfolio toobit account info                           → confirm balance updated
```

## Operation Flow

### Step 0 — Credential Check

Before any authenticated command:

1. Run `toobit account check-api-key` to verify API key validity and permissions
2. If error → stop, guide user to configure `~/.toobit/config.toml`
3. If valid → proceed

### Step 1: Identify account action

- Check balance → `toobit account info`
- View transaction history → `toobit account balance-flow`
- List sub-accounts → `toobit account sub-accounts`
- Check API key → `toobit account check-api-key`
- Get deposit address → `toobit account deposit-address`
- Deposit history → `toobit account deposits`
- Withdrawal history → `toobit account withdrawals`
- Audit / trade log → `toobit account audit`
- Withdraw funds → MCP `account_withdraw`
- Sub-account transfer → MCP `account_sub_transfer`

### Step 2: Run read commands immediately — confirm writes

**Read commands** (1–8): run immediately, no confirmation needed.

- `--tokenId` filter: use token symbol like `USDT`, `BTC`, `ETH`
- `--limit`: number of records to return

**Write commands** (9–10): confirm once before executing.

- `account_withdraw`: confirm token, amount, address, chain — **irreversible once submitted**
- `account_sub_transfer`: confirm subAccountId, tokenId, amount, direction

### Step 3: Verify after writes

- After `account_withdraw`: run `toobit account withdrawals` to check withdrawal status
- After `account_sub_transfer`: run `toobit account info` to confirm balance updated

## CLI Command Reference

### Account Info — Balance

```bash
toobit account info [--json]
```

Returns table of all tokens with balance > 0: `tokenId`, `tokenName`, `total`, `free`, `locked`.

---

### Balance Flow — Transaction History

```bash
toobit account balance-flow [--tokenId <id>] [--limit <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--tokenId` | No | - | Filter by token (e.g., `USDT`) |
| `--limit` | No | 50 | Number of records |

Returns: `tokenId`, `flowType`, `amount`, `balance`, `time`, `description`.

---

### Sub-accounts — List

```bash
toobit account sub-accounts [--json]
```

Returns: list of sub-accounts with `accountId`, `accountName`, `accountType`, `status`.

---

### Check API Key

```bash
toobit account check-api-key [--json]
```

Returns: API key status, account type (master/sub), permissions (read/trade/withdraw), IP whitelist info.

---

### Deposit Address

```bash
toobit account deposit-address --tokenId <id> [--json]
```

| Param | Required | Description |
|---|---|---|
| `--tokenId` | Yes | Token to deposit (e.g., `USDT`, `BTC`) |

Returns: `tokenId`, `address`, `addressTag` (memo), `chain`.

---

### Deposit Orders

```bash
toobit account deposits [--tokenId <id>] [--limit <n>] [--json]
```

Returns: deposit records with `tokenId`, `amount`, `address`, `txId`, `status`, `time`.

---

### Withdrawal Orders

```bash
toobit account withdrawals [--tokenId <id>] [--limit <n>] [--json]
```

Returns: withdrawal records with `tokenId`, `amount`, `address`, `txId`, `status`, `fee`, `time`.

---

### Audit Log — Trade History

```bash
toobit account audit [--limit <n>] [--json]
```

Returns: recent tool call / trade audit records with timestamp, tool name, parameters, and result summary.

---

## MCP Tool Reference

| Tool | Description |
|---|---|
| `account_get_info` | Account balance (all tokens) |
| `account_get_balance_flow` | Balance flow / transaction history |
| `account_get_sub_accounts` | List sub-accounts |
| `account_check_api_key` | API key status and permissions |
| `account_get_deposit_address` | Get deposit address for a token |
| `account_get_deposit_orders` | Deposit history |
| `account_get_withdraw_orders` | Withdrawal history |
| `account_withdraw` | Withdraw funds (WRITE — confirm before executing) |
| `account_sub_transfer` | Transfer between main and sub-accounts (WRITE) |
| `trade_get_history` | Tool call audit log |
| `system_get_capabilities` | Get system capabilities and available modules |

---

## Input / Output Examples

**"How much USDT do I have?"**
```bash
toobit account info
# → tokenId: USDT | total: 5000.00 | free: 4500.00 | locked: 500.00
#    tokenId: BTC  | total: 0.50    | free: 0.50    | locked: 0.00
```

**"Show my recent balance changes"**
```bash
toobit account balance-flow --tokenId USDT --limit 10
# → table: tokenId, flowType, amount, balance, time, description
```

**"List my sub-accounts"**
```bash
toobit account sub-accounts
# → table: accountId, accountName, accountType, status
```

**"Check my API key permissions"**
```bash
toobit account check-api-key
# → accountType: master | permissions: read, spot-trade, futures-trade
```

**"Where do I deposit USDT?"**
```bash
toobit account deposit-address --tokenId USDT
# → chain: TRC20 | address: TXyz...abc123 | memo: (none)
```

**"Show my recent deposits"**
```bash
toobit account deposits --tokenId USDT --limit 5
# → table: tokenId, amount, address, txId, status, time
```

**"Show my recent withdrawals"**
```bash
toobit account withdrawals --limit 5
# → table: tokenId, amount, address, txId, status, fee, time
```

**"Show recent audit log"**
```bash
toobit account audit --limit 5
# → table: time, tool, params summary, result
```

## Edge Cases

- **No balance shown**: `account info` only shows tokens with balance > 0; zero-balance tokens are hidden
- **Futures balance**: futures account balance is separate — use `toobit futures balance` from `toobit-cex-trade` skill
- **Deposit address**: different chains may have different addresses; Toobit may return multiple chain options
- **Deposit not showing**: confirmations may be pending; check again after a few minutes
- **Withdrawal limits**: check API key permissions; some keys may not have withdrawal permission
- **Sub-account transfer**: requires main account API key with appropriate permissions
- **balance-flow tokenId**: case-sensitive; use uppercase (e.g., `USDT` not `usdt`)

## Global Notes

- All commands require valid API credentials in `~/.toobit/config.toml` or env vars
- `--json` returns raw Toobit API response
- Rate limit: 10–20 requests per second for account endpoints
- All timestamps are in milliseconds (Unix epoch)
- API key permissions determine which endpoints are accessible:
  - **Read**: balance, positions, orders, history
  - **Spot Trade**: spot order placement and cancellation
  - **Futures Trade**: futures order placement and cancellation
  - **Withdraw**: fund withdrawal (use with extreme caution)
- IP whitelist: your machine's public IP must be whitelisted in the Toobit API management console
