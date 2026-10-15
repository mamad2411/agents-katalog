---
name: near-intents-trading
description: Use when user asks about crypto trading, swaps, portfolio rebalancing, token balances, or managing holdings across NEAR, Ethereum, Solana, Bitcoin, or other chains. Triggers on keywords like swap, rebalance, portfolio, balance, holdings, trade, DeFi.
metadata:
  version: "0.1.7"
---

# NEAR Intents Trading

Orchestrate crypto portfolio management and cross-chain swaps using two CLI tools.

## Install

If `near-intents` or `portfolio` are not installed, run:

```
curl -fsSL https://raw.githubusercontent.com/FlipsideCrypto/near-intents-cli/main/install.sh | sh
```

Or with a specific version: `VERSION=v0.1.0 curl -fsSL ... | sh`

Custom install dir: `INSTALL_DIR=~/.local/bin curl -fsSL ... | sh`

## Tools

| Tool | Purpose | Onboard command |
|------|---------|-----------------|
| `portfolio` | Read balances across all chains | `portfolio llm onboard` |
| `near-intents` | Execute swaps + get intel | `near-intents llm onboard` |

**You MUST run both onboard commands before any other action in a session — no exceptions.** Do not attempt to guess command names, flag names, or asset ID formats. Every mistake that wastes round trips (wrong flags, wrong token format, unknown commands) is documented in the onboard output. Running it takes seconds; skipping it costs minutes of failed attempts.

```
near-intents llm onboard
portfolio llm onboard
```

Run these immediately after updating. Do not proceed until you have read the output.

## The Loop

```
OBSERVE  → portfolio balances / near-intents balances
DECIDE   → near-intents intel (feed it the portfolio summary)
PLAN     → near-intents quote (price out each swap)
CONFIRM  → present plan to user with fees and steps
EXECUTE  → near-intents swap + submit-tx
VERIFY   → near-intents status (poll until terminal)
```

Never skip OBSERVE. Never skip CONFIRM.

## Before Anything

1. **Update both tools** — always run this first to ensure you have the latest version:
   ```
   near-intents update && portfolio update
   ```
   If either binary is missing, install first (see Install above), then update.

2. **Read the onboard docs** — run both of these and read the full output before proceeding:
   ```
   near-intents llm onboard
   portfolio llm onboard
   ```
   This is not optional. The onboard output contains exact command syntax, required flags, asset ID formats, and common mistakes. Skipping it and guessing will waste time.

3. Run `portfolio setup --list` — are addresses configured? If not, ask the user for their wallet addresses and add them.
4. Run `portfolio balances` (or `near-intents balances --account <id>` for NEAR-only) — establish current holdings.
5. If the user wants recommendations, summarize the balances and pass to `near-intents intel --message "Here's my portfolio: [summary]. How should I rebalance?"`.

## Key Concepts

- **Signing URL is the default.** Most swaps should use the cross-chain signing URL flow — user gets a link, opens it, connects wallet, signs. No near-cli needed, no wrapping, no storage deposits. Only use native mode if the user explicitly asks for it.
- **Ask the user, don't assume.** Present both options (signing URL vs native CLI) and let them choose. Don't probe for near-cli or check `~/.near-credentials/` unless the user wants native mode.
- **`assetId` fields** in balance output feed directly into `near-intents swap --from` / `--to`.
- **Flipside intel** is for analytical recommendations ("how should I rebalance?"), not balance lookups (use `portfolio balances` for that).
- **intents vs wallet**: Tokens in `near-intents` chain are immediately swappable. Tokens in wallet may need extra steps depending on mode.
- **No withdraw CLI command.** After native swaps, tokens land in intents.near. Withdraw via `ft_withdraw` on `intents.near` using near-cli directly. See onboard docs for exact syntax. (Only relevant in native mode.)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Guessing flag names (--account, --correlation-id) | Run `llm onboard` — correct flags are --sender, --deposit-address, etc. |
| Querying balances without setup | Check `portfolio setup --list` first |
| Advising on rebalancing yourself | Use `near-intents intel` for recommendations |
| Executing swaps without confirmation | Always present plan with fees, wait for approval |
| Assuming all tokens are in wallet | Check intents balance separately — it's a different "chain" in the output |
| Trying `near-intents withdraw` | No such command. Use `ft_withdraw` on `intents.near` via near-cli directly |
| Using `nep141:` prefix in withdrawal args | Strip it — `ft_withdraw` takes bare contract ID (e.g., `wrap.near` not `nep141:wrap.near`) |
| Using `mt_withdraw` for standard tokens | Use `ft_withdraw` for NEP-141 tokens (wNEAR, USDC, etc.) — `mt_withdraw` is for NEP-245 only |
| "Send X to Y" = buy X | It means user **has X**, deliver to Y. Confirm direction before quoting: "You're sending [A], receiving [B] at [address] — right?" |
| Searching tokens on one chain only | Search all chains first (`--search BTC`), then choose the best route — native chain beats bridged |
| Defaulting to native swap mode | Default to cross-chain (signingUrl) unless user confirms near-cli is set up |
| Quoting cross-chain swap without refund address | For non-NEAR source chains, ask for a refund address on that chain before calling swap |
| Trying bridged token before native chain | Try native chain version first (BTC on bitcoin > wBTC on NEAR). Fall back if quote fails. |
