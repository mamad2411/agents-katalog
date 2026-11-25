---
name: aave-oracle-lag-arb
description: Install, run and watch the Aave oracle-lag arbitrage bot (borrow WETH on Aave V3 at the Chainlink price, sell it on a DEX trading above the oracle, buy back after convergence) on Ethereum, Arbitrum, Base and Optimism. Use when the user wants to set up or operate the bot, set its wallet or alert webhook, schedule its health check, read its findings, or unwind and withdraw.
license: AGPL-3.0-only
metadata:
  repo: https://gitlab.com/aa22396584/aave-oracle-lag-arb
---

# Aave oracle-lag arbitrage bot

The bot holds a short-ETH position: stablecoin collateral on Aave, WETH debt. It opens only when a DEX prices ETH
above Aave's oracle by `OPEN_PREMIUM_BPS` (default 3%) for `CONFIRM_SECONDS`, closes when the premium is gone, and
deleverages on its own if the health factor drops. Read the repo README's risk section before helping anyone fund it.

Reply in the user's language. The bot's own log lines are Traditional Chinese by default; translate them when you report,
or add `BOT_LANG=en` to the env file for English output (finding codes are the same in both).

## Paths

- Repo checkout: `~/aave-oracle-lag-arb` (any path works)
- App directory: `APP=${APP_DIR:-$HOME/.local/share/aave-oracle-lag-arb}` (bundled bot, supervisor, state, log)
- Wallet and alert config: `${ARB_CONFIG_DIR:-$HOME/.config/aave-oracle-lag-arb}/env` and `alerts.env`, mode 600

## Install or update

```bash
git clone https://gitlab.com/aa22396584/aave-oracle-lag-arb.git ~/aave-oracle-lag-arb 2>/dev/null || git -C ~/aave-oracle-lag-arb pull --ff-only
bash ~/aave-oracle-lag-arb/deploy/install.sh        # --with-op: 1Password; --bundle-node: keep Node in APP (machines that lose /usr/bin/node on reboot); restarts the bot if it runs
```

Needs Linux (the supervisor uses `setsid` and `/proc`), git, curl, and Node 20+ or Linux x64/arm64 for the pinned Node 22 download.
On macOS, run `cd bot && npm install && node start.ts` in a terminal instead.

## Set the wallet

Never ask for a private key or mnemonic in ordinary chat. Use one of these:

1. **Your platform's secret input** (a masked secret card or secure prompt that becomes an environment variable).
   Ask for `AAVE_BOT_KEY` (private key or mnemonic), then:
   `"$APP/set-wallet.sh" --from-env AAVE_BOT_KEY`
   It copies the value into the env file so restarts don't depend on the variable. Never echo the variable.
2. **The user types it** in a terminal on that machine: `"$APP/set-wallet.sh"` (hidden prompt).
3. **1Password**: `"$APP/set-wallet.sh" --op op://vault/item/field --token-from-env OP_TOKEN_VAR` (install with `--with-op`).

`set-wallet.sh` ends by running `trader.sh whoami`, which prints the address and balances on every chain.
If the output mentions `MNEMONIC_INDEX`, the key is a mnemonic: show the user the numbered account list, ask which
one, then run `"$APP/set-wallet.sh" --index <n>` for MetaMask #n, or `--path "m/44'/60'/<n>'/0/0"` for Ledger Live #n.

One wallet, one running trader: two traders on the same wallet (on one machine or several) find the same contract and race each other's
transactions. If another install already trades this wallet, stop there and tell the user.

Show the address and balances and ask once before starting. The first time, also point the user to `DISCLAIMER.md` in the repo
(unaudited, leveraged short ETH, may lose everything) in one line. Starting deposits **all** USDC/USDT in that wallet as
principal on every chain where Aave accepts it; ETH stays in the wallet for gas.

## Run

```bash
"$APP/trader.sh" start       # background, restarts itself with backoff; survives your session
"$APP/trader.sh" status      # running or not, mode, last exit, last log lines
"$APP/trader.sh" whoami      # address and balances
```

Run `stop`, `close-only` or `exit` only when the user asks:
`stop` leaves positions open, `close-only` stops opening and only unwinds, `exit` closes everything and withdraws to the wallet
(if it can't finish, it restarts in close-only mode; run `exit` again later).

## Scheduled check (every 6 hours is enough; the bot itself reacts every block)

```bash
"$APP/trader.sh" ensure      # start it if it isn't running; skips if no wallet or stopped on purpose
"$APP/trader.sh" check       # exit 0: nothing changed since the last check; 1: changed; other: error
```

- `ensure` printing `started` means the bot had died or the machine rebooted: mention it.
- `ensure` printing `this environment doesn't have it`: the wallet was stored by variable name only and the variable is gone;
  ask the user to set the wallet again.
- The first `check` only records a baseline: it counts as changed only if there is a warning or critical finding
  (info codes like `aave_frozen` alone give exit 0).
- `check` exit 0 and nothing restarted: stay silent. Exit 1: summarize `new` and `resolved` in one or two sentences.
  Other exit codes: report the first lines of the error once, not every time.

Finding codes (`<code>:<chain>`, chain is mainnet / arbitrum / base / optimism):

| code | meaning | what to say |
|---|---|---|
| `premium_open` | a DEX prices ETH above the oracle by the open threshold | opportunity; the bot acts on its own. If the message says Aave is frozen, it can't borrow yet |
| `hf_low` | health factor below `EMERGENCY_HF` | urgent: liquidation risk; attach `trader.sh status` |
| `bot_not_running` | opportunity or position, but no heartbeat for a minute | run `trader.sh ensure`, report the result |
| `position_open` | a position is open | it disappearing means the bot closed it |
| `aave_frozen` | can't borrow on that chain: WETH frozen, or no stablecoin usable as collateral (LTV 0) | it in `resolved` means borrowable again; the bot deposits pending principal itself |
| `action_failing` | several actions in a row failed | attach `trader.sh status` |
| `gas_low` | position open but little ETH for gas | ask the user to send ETH on that chain |
| `rpc_error` | couldn't read that chain | |
| `trader_crashloop` (no chain) | the bot keeps exiting right after start (key unreadable, RPCs down) | urgent; attach `trader.sh status` |

## Instant alerts (optional)

If your platform gives you a webhook that turns POSTs into messages:
`"$APP/set-alerts.sh" <https://url> --header-from-env AAVE_ALERT_KEY` (a bare token becomes `Authorization: Bearer <token>`).
It sends a test POST and prints the HTTP status. The bot then POSTs `{source, chain, findings, new, resolved}` whenever a chain's
findings change. `set-alerts.sh --off` removes it.

## Never

- print, read aloud or copy the env file, keys, tokens or webhook secrets;
- send transactions yourself or edit files in `$APP`;
- run `stop`, `close-only` or `exit` without the user asking.
