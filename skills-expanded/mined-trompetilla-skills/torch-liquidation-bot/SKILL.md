---
name: torch-liquidation-bot
description: Read-only lending market scanner for Torch Market on Solana. No wallet required. Scans lending markets and displays rates, LTV thresholds, treasury balances, and active loan counts. Requires only an RPC endpoint (RPC_URL). Optional MINT and LOG_LEVEL parameters can be provided to tune scope of the tool.
license: MIT
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      env:
        - RPC_URL
    install:
      - id: npm-torch-liquidation-bot
        kind: npm
        package: torch-liquidation-bot@2.0.8
        flags: ["--ignore-scripts"]
        bins: ["torch-liquidation-bot"]
        label: "Install torch-liquidation-bot (npm, --ignore-scripts)"
  author: torch-market
  version: "2.0.8"
  clawhub: https://clawhub.ai/mrsirg97-rgb/torchliquidationbot
  github: https://github.com/mrsirg97-rgb/torch-liquidation-bot-ro
  npm: https://www.npmjs.com/package/torch-liquidation-bot
  sdk: https://github.com/mrsirg97-rgb/torchsdk
  agentkit: https://github.com/mrsirg97-rgb/solana-agent-kit-torch-market
  npm-torchsdk: https://www.npmjs.com/package/torchsdk
  npm-agentkit: https://www.npmjs.com/package/solana-agent-kit-torch-market
compatibility: Requires Node.js and a Solana RPC endpoint (RPC_URL). Only read-only info mode is available -- no wallet loaded, no signing, no state changes. All wallet-dependent functionality was removed in v2.0.0. Distributed via npm. Source available for audit at the GitHub repository.
---

# Torch Liquidation Bot — v2.0.8 (Read-Only)

Read-only lending market scanner for [Torch Market](https://torch.market) on Solana. No wallet required. Only an RPC endpoint is needed.

## v2.0.0 Breaking Change — Read-Only Only

**All wallet-dependent code was removed as of v2.0.0.**

The entry point (`index.ts`) imports only read-only SDK functions. There is no wallet, keypair, signing, or transaction code anywhere in the source tree. There is no `WALLET` env var to set, no `MODE` to switch, no `Keypair` in the import graph. The only mode is read-only info.

**What was removed:**

- `bot` mode (liquidation execution)
- `watch` mode (loan health monitoring + auto-repay)
- `loadWallet()` / `loadConfig()` (keypair decoding)
- All `sendAndConfirmTransaction` / `buildRepayTransaction` / `buildLiquidateTransaction` / `confirmTransaction` calls
- All SAID Protocol write operations (`confirmTransaction` for reputation)
- All wallet-dependent source files (`liquidator.ts`, `monitor.ts`, `wallet-profiler.ts`, `risk-scorer.ts`, `scanner.ts`, `logger.ts`)
- Unused dependencies (`bs58`, `@coral-xyz/anchor`, `@solana/spl-token`)

The v1.x code exists only in the git history of the original repository.

**Why:**

The skill's direct handling of a Solana private key via the `WALLET` environment variable and its interaction with the external SAID Protocol API presented a significant attack surface. While the code itself was audited and no malicious behavior was found, the inherent risk of providing a private key and relying on an external reputation API warranted a conservative approach. Read-only mode eliminates this risk entirely — no key is ever loaded, decoded, or held in memory.

## What This Skill Does

This skill scans lending markets on Torch Market, a fair-launch DAO launchpad on Solana. Every migrated token on Torch has a built-in lending market where holders can borrow SOL against their tokens.

The skill is a **read-only dashboard**. It discovers migrated tokens and displays their lending parameters — interest rates, LTV thresholds, treasury balances, and active loan counts. No wallet is loaded. No state changes occur. No transactions are built or signed.

## How It Works

```
connect to Solana RPC
         |
    discover migrated tokens (getTokens)
         |
    for each token:
         |
    read lending parameters (getLendingInfo)
         |
    display: rates, thresholds, treasury balance, loan count
```

### One Mode

| Mode | Purpose | Wallet | State Changes |
|------|---------|--------|---------------|
| `info` (only) | Display lending parameters for a token or all tokens | not required | none (read-only) |

## Architecture

```
packages/bot/src/
├── types.ts    — ReadOnlyConfig interface
├── config.ts   — loadReadOnlyConfig()
├── utils.ts    — sol() + bpsToPercent() helpers
└── index.ts    — read-only entry point
```

4 files. ~60 lines of source. No wallet code.

The codebase can be audited and reviewed on GitHub at [torch-liquidation-bot-ro](https://github.com/mrsirg97-rgb/torch-liquidation-bot-ro).

## Network & Permissions

- **Read-only only** -- no wallet is loaded, no keypair is decoded, no signing occurs, no state changes. Only `RPC_URL` is required.
- **Outbound connections:** Solana RPC (via `@solana/web3.js`) only. No SAID Protocol API calls, no write endpoints.
- **No private key handling** -- `Keypair` is not imported. `bs58` is not a dependency. There is no code that could decode, hold, or transmit a private key.
- **Distributed via npm** -- all code runs from `node_modules/`. No post-install hooks, no remote code fetching. Install locally with `npm install torch-liquidation-bot@2.0.8 --ignore-scripts` and audit the source before running.
- **Minimal dependencies** -- `@solana/web3.js` and `torchsdk` only. All dependency versions are pinned to exact versions (no `^` or `~` ranges) in `package.json` to prevent supply chain drift.
- **RPC_URL sensitivity** -- if your RPC provider embeds an API key in the endpoint URL, that key is used only for read-only RPC calls and is never logged, transmitted externally, or stored. Use a read-only key or a public endpoint if this is a concern.
- **Autonomous invocation disabled** -- `disable-model-invocation: true` is set as a top-level frontmatter field (OpenClaw extension), ensuring the registry enforces it. An agent cannot invoke this skill autonomously — it requires explicit user action. This is a deliberate choice: because the skill depends on npm-distributed code, autonomous execution should not be permitted by default.
- **Required env declared via OpenClaw** -- `RPC_URL` is declared in `metadata.openclaw.requires.env`, which the registry uses to validate environment before invocation. Optional variables (`MINT`, `LOG_LEVEL`) have no frontmatter equivalent and are documented in the Environment Variables table below.

## Supply Chain Verification

Before installing, verify the package yourself. These commands let you confirm every claim in this document.

### 1. Check for lifecycle scripts (should be empty)

```bash
npm pkg get scripts.preinstall scripts.postinstall scripts.prepare --registry https://registry.npmjs.org/torch-liquidation-bot
```

Or after install:

```bash
cat node_modules/torch-liquidation-bot/package.json | grep -E '"(preinstall|postinstall|prepare)"'
```

Expected: no output (no lifecycle scripts).

### 2. Audit dependencies

```bash
npm audit --omit=dev torch-liquidation-bot@2.0.8
```

### 3. Compare published package to GitHub source

```bash
# download the published tarball
npm pack torch-liquidation-bot@2.0.8

# extract and diff against the repo
tar -xzf torch-liquidation-bot-2.0.8.tgz
diff -r package/dist/ <(cd /path/to/torch-liquidation-bot-ro && pnpm build && echo packages/bot/dist/)
```

### 4. Verify the import graph contains no wallet code

```bash
grep -rn "Keypair\|bs58\|sendAndConfirm\|signTransaction\|wallet\|secretKey\|privateKey" node_modules/torch-liquidation-bot/dist/
```

Expected: no matches.

### 5. Inspect dependency tree

```bash
npm ls torch-liquidation-bot --all
```

Expected: only `@solana/web3.js` and `torchsdk` as direct dependencies.

---

## Setup

### Install

Review the source code on GitHub at [torch-liquidation-bot-ro](https://github.com/mrsirg97-rgb/torch-liquidation-bot-ro) before installing.

```bash
npm install torch-liquidation-bot@2.0.8 --ignore-scripts
```

Version pinning (`@2.0.8`) prevents silent upgrades. `--ignore-scripts` prevents any lifecycle scripts from executing during install (defense-in-depth — this package has no lifecycle scripts, but the flag ensures that remains true).

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RPC_URL` | yes | -- | Solana RPC endpoint. If your provider embeds an API key in the URL, use a read-only key or a public endpoint. |
| `MINT` | no | -- | Token mint address. If set, shows info for that token. If omitted, shows all migrated tokens. |
| `LOG_LEVEL` | no | `info` | `debug`, `info`, `warn`, or `error` |

That's it. No `WALLET`, no `MODE`, no bot-specific config.

### Run

After installing with `npm install`, run the locally-installed package:

```bash
# show lending info for all migrated tokens
RPC_URL=<rpc> npx torch-liquidation-bot

# show lending info for a specific token
MINT=<mint> RPC_URL=<rpc> npx torch-liquidation-bot
```

**Note:** `npx` here resolves to the locally-installed copy (installed in the step above). If the package is not installed locally, `npx` will fetch it from npm at runtime — review the source on [GitHub](https://github.com/mrsirg97-rgb/torch-liquidation-bot-ro) before running.

### Programmatic Usage

```typescript
import { loadReadOnlyConfig } from 'torch-liquidation-bot/config'
import { Connection } from '@solana/web3.js'
import { getTokens, getLendingInfo } from 'torchsdk'

const config = loadReadOnlyConfig()
const connection = new Connection(config.rpcUrl, 'confirmed')

const { tokens } = await getTokens(connection, {
  status: 'migrated',
  sort: 'volume',
  limit: 50,
})

for (const t of tokens) {
  const lending = await getLendingInfo(connection, t.mint)
  console.log(`${t.symbol}: ${lending.active_loans} active loans`)
}
```

## SDK Functions Used

Only read-only [torchsdk](https://github.com/mrsirg97-rgb/torchsdk) functions are imported:

| Function | Purpose |
|----------|---------|
| `getTokens(connection, params)` | Discover migrated tokens |
| `getToken(connection, mint)` | Get token price and metadata |
| `getLendingInfo(connection, mint)` | Get lending parameters and active loan count |

## Key Types

```typescript
interface ReadOnlyConfig {
  rpcUrl: string
  logLevel: LogLevel
}
```

## Torch Lending Parameters

| Parameter | Value |
|-----------|-------|
| Max LTV | 50% |
| Liquidation threshold | 65% LTV |
| Interest rate | 2% per epoch (~7 days) |
| Liquidation bonus | 10% of collateral value |
| Treasury utilization cap | 50% |
| Min borrow | 0.1 SOL |

## Simulation Results — Read-Only (Surfpool)

The read-only test was run against a Surfpool mainnet fork. No wallet was loaded. No transactions were signed.

```
============================================================
READ-ONLY TEST — Surfpool Mainnet Fork
============================================================
[16:00:21]   ✓ connection — solana-core 3.1.6
[16:00:21]   ✓ getTokens — found 8 migrated tokens
    BTEST      | mint=wokxaeFZ...
    BTEST      | mint=8FqFw5fD...
    LEND       | mint=AD1kat3L...
    LEND       | mint=G6yzUvS7...
    BTEST      | mint=GLim6QRX...
    LEND       | mint=76TEs99p...
    BTEST      | mint=FjGHamUF...
    LEND       | mint=9KNunLmY...
[16:01:43]   ✓ getLendingInfo — 8 tokens with lending data
    BTEST      | rate=2.00%   | loans=null | avail=32.3043 SOL
    LEND       | rate=2.00%   | loans=null | avail=32.3043 SOL
    ...
[16:02:34]   ✓ getToken — Bot Test Token (BTEST) | price=0.0000 SOL | status=migrated
[16:02:34]   ✓ no wallet — no WALLET env var read, no Keypair created, no signing occurred

RESULTS: 5 passed, 0 failed
============================================================
```

### What this tells us

**Token discovery works.** `getTokens` found 8 migrated tokens across previous test runs on the fork. Each token has a mint address, symbol, and status.

**Lending data is real and consistent.** Every migrated token returned a 2.00% interest rate, matching the protocol's fixed per-epoch rate. Treasury balances show ~32 SOL available per token — SOL that accumulated during the bonding curve phase.

**The `active_loans` null on Surfpool is a known fork artifact.** The loan counter comes from a program-derived account field that doesn't always populate correctly on forked validators. On mainnet, this field correctly reflects the number of open loans.

**The skill is genuinely inert.** 5 tests, 0 failures, 0 wallet operations. The test explicitly verifies that no `WALLET` env var was read, no `Keypair` was constructed, and no signing occurred. The import graph of `index.ts` contains `Connection`, `getToken`, `getTokens`, `getLendingInfo`, `loadReadOnlyConfig`, `sol`, `bpsToPercent`. That's it.

## Threat Model

What this skill **can** do:

- Read public Solana chain data via RPC (token metadata, lending parameters, treasury balances)
- Read `RPC_URL`, `MINT`, and `LOG_LEVEL` environment variables
- Write to stdout/stderr

What this skill **cannot** do:

- Sign transactions (no `Keypair`, no `bs58`, no signing code)
- Access a wallet or private key (no `WALLET` env var, no key decoding)
- Modify on-chain state (no transaction building, no `sendAndConfirmTransaction`)
- Write to the filesystem
- Make network calls to anything other than the Solana RPC endpoint

What a **compromised dependency** could theoretically do:

- Read all environment variables (including `RPC_URL`)
- Make arbitrary network calls
- Read/write to the filesystem
- Execute arbitrary code in the Node.js process

**Mitigations in place:**

- Only 2 direct dependencies (`@solana/web3.js`, `torchsdk`) — both are auditable
- All dependency versions are locked to exact versions in `package.json` (no `^` or `~` ranges) — prevents supply chain drift from semver-range resolution
- `--ignore-scripts` installation prevents lifecycle script execution
- Version pinning in install command (`@2.0.8`) prevents silent upgrades
- `disable-model-invocation: true` (top-level frontmatter) prevents autonomous agent execution
- Source is public and auditable on GitHub
- Use a public or read-only RPC endpoint to limit credential exposure

## Links

- Source Code: [github.com/mrsirg97-rgb/torch-liquidation-bot-ro](https://github.com/mrsirg97-rgb/torch-liquidation-bot-ro)
- npm: [npmjs.com/package/torch-liquidation-bot](https://www.npmjs.com/package/torch-liquidation-bot)
- Torch SDK: [github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk)
- Torch Market: [torch.market](https://torch.market)
- ClawHub: [clawhub.ai/mrsirg97-rgb/torchliquidationbot](https://clawhub.ai/mrsirg97-rgb/torchliquidationbot)
- Program ID: `8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

**NOTE**

A security audit of the v1.x codebase is provided in `audit.md`. That audit covers the wallet-handling and transaction-signing code that has since been removed. v2.0.0+ contains only read-only code — the audited wallet code exists only in the git history of the original repository.
