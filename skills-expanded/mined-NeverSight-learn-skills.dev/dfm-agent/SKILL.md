---
name: dfm-agent
version: 2.0.0
description: |
  Fully autonomous DTF vault management on Solana. The agent independently researches markets,
  decides vault names/symbols/allocations/policies, and deploys on-chain in a two-step flow —
  no human confirmation required. The policy engine is the guardrail, not a human approval step.
  Use when the user asks to launch a vault, rebalance, check policy, or distribute fees.
homepage: https://app.dfm.finance
license: Proprietary
compatibility: Claude Code, Codex, OpenClaw
metadata: {"category":"defi-agent","auth":"jwt+keypair","author":"dfm","tags":"solana,defi,vault,rebalance,dtf,fund-management,autonomous-agent"}
---

# DFM Agent

DFM Agent is a **fully autonomous** AI skill for DTF (DeFi Token Fund) vault management on Solana. The agent researches markets, decides everything — name, symbol, asset allocations, fee structure, policy configuration — and deploys on-chain. No human-in-the-loop confirmation. The **policy engine** is the guardrail, not a human approval step.

## Core Philosophy

**The agent is the creator. It has full authority over what it launches.**

```
+----------------------------------------------------------------+
|                    AUTONOMOUS AGENT FLOW                        |
|                                                                |
|  1. RESEARCH    Agent analyzes markets, trending tokens,       |
|                 liquidity, volume, and macro conditions         |
|                                                                |
|  2. DECIDE      Agent picks vault name, symbol, assets,        |
|                 allocations, fees, and policy rules             |
|                                                                |
|  3. DEPLOY      Two-step vault creation:                       |
|                 a) POST /launch-dtf -> unsigned transaction     |
|                 b) Agent signs tx & submits on-chain            |
|                 c) POST /dtf-create -> policy + DB persist      |
|                                                                |
|  4. MANAGE      Agent monitors, rebalances, distributes fees   |
|                 -- all autonomously via API calls               |
|                                                                |
|  GUARDRAILS:    Policy engine validates constraints.            |
|                 Invalid payloads return errors with specifics.  |
|                 NO human confirmation step.                     |
+----------------------------------------------------------------+
```

| Principle | Detail |
|---|---|
| **Fully autonomous** | Agent decides everything: name, symbol, assets, allocations, policy, fees. No confirmation prompts. |
| **Two-step vault creation** | `POST /launch-dtf` builds the unsigned tx, agent signs & submits, then `POST /dtf-create` creates policy + persists to DB. |
| **Policy engine as guardrail** | Backend validates the payload and policy config. If valid, it deploys. If not, it returns an error with the specific issue. |
| **Non-custodial** | Agent Wallet private key never leaves the user's machine. Backend never receives secret keys. |
| **Agent = on-chain authority** | The Agent Wallet becomes the permanent on-chain creator/manager of every vault it deploys. |

## Sensitive Data Rules (MANDATORY -- READ FIRST)

**NEVER print, echo, log, or display the values of these environment variables in terminal output:**
- `DFM_AUTH_TOKEN` -- JWT auth token
- `DFM_AGENT_KEYPAIR` -- base58 secret key
- Any private key, secret key, or auth token

**To check if an env var is set, use length check only:**
```bash
node -e 'console.log(process.env.DFM_AUTH_TOKEN ? "set" : "not set")'
```

**NEVER do any of the following:**
```bash
# WRONG - exposes token in terminal output
echo $DFM_AUTH_TOKEN
export DFM_AUTH_TOKEN="eyJ..."   # WRONG - token visible in bash command
curl -H "Authorization: Bearer eyJ..." ...   # WRONG - token embedded in command
curl -H "Authorization: Bearer $DFM_AUTH_TOKEN" ...   # WRONG - shell expands and displays it
```

**ALL API calls MUST use inline `node -e` scripts** that read env vars internally via `process.env`. This prevents sensitive values from appearing in the bash command itself.

**Correct pattern for API calls:**
```bash
node -e '
const http = require("http");
const https = require("https");
const url = new URL(process.env.DFM_API_URL + "/api/v2/agent/dtf/SYMBOL/state");
const client = url.protocol === "https:" ? https : http;
const req = client.get(url, { headers: { "Authorization": "Bearer " + process.env.DFM_AUTH_TOKEN } }, (res) => {
  let data = "";
  res.on("data", (chunk) => data += chunk);
  res.on("end", () => console.log(data));
});
req.on("error", (e) => console.error("Error:", e.message));
'
```

**Do NOT use `curl` for API calls.** Always use `node -e` with `process.env` references so tokens and keys are never visible in the command string.

**IMPORTANT: No timeout on API calls.** When running Bash commands that make API calls, always set `timeout: 600000` (10 minutes) or use `run_in_background: true`. The default Bash timeout is 2 minutes which is too short for on-chain operations like vault creation, rebalancing, and fee distribution. Never let an API call get killed by a timeout.

## Pre-Flight Auth Check (REQUIRED)

**You MUST complete this check before making any API call.** Do not skip this step.

### Step 1: Ensure `.claude/settings.json` has env vars

Claude Code runs bash in a non-interactive subprocess that does NOT source `~/.zshrc` or `~/.bashrc`. Environment variables set via `export` in the user's terminal are NOT available to Claude Code's bash commands. The **only reliable way** to pass env vars to Claude Code is via `.claude/settings.json`.

**On every pre-flight check**, run this script to sync env vars from `~/.zshrc` into `.claude/settings.json`:

```bash
node -e '
const fs = require("fs");
const path = require("path");
const os = require("os");

const settingsPath = path.join(process.cwd(), ".claude", "settings.json");
let settings = {};
try { settings = JSON.parse(fs.readFileSync(settingsPath, "utf8")); } catch {}
if (!settings.env) settings.env = {};

// Read from ~/.zshrc to find exported DFM vars
const zshrc = fs.readFileSync(path.join(os.homedir(), ".zshrc"), "utf8");
const envVars = ["DFM_API_URL", "DFM_AUTH_TOKEN", "DFM_AGENT_KEYPAIR", "SOLANA_RPC_URL", "AGENT_WALLET_PATH"];
for (const v of envVars) {
  // Match export VAR="value" or export VAR=value
  const match = zshrc.match(new RegExp("export\\s+" + v + "=[\"'\\'']?([^\"'\\''\\n]+)[\"'\\'']?"));
  if (match && match[1]) settings.env[v] = match[1];
  // Also check current process.env as fallback
  if (!settings.env[v] && process.env[v]) settings.env[v] = process.env[v];
}

// DFM_API_URL must be set by the user — no default

fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));

// Report status without exposing values
for (const v of envVars) {
  console.log(v + "=" + (settings.env[v] ? "set" : "NOT SET"));
}
'
```

**If `DFM_AUTH_TOKEN` is NOT SET after this script**, run the automated agent profile creation flow:

1. Ask the user for their **DFM-registered wallet address** (the Solana public key they used to sign up on the DFM Dashboard):

   > To set up your DFM Agent, I need the **Solana wallet address** you registered on the DFM Dashboard (https://app.app.dfm.finance).
   > Please paste your wallet public key.

2. Once the user provides the wallet address, **auto-generate** the agent profile name and username:
   - Name: generate a creative agent name (e.g. "Alpha Sentinel", "Momentum Agent", "DeFi Navigator")
   - Username: generate a unique username from the name (e.g. "alpha_sentinel", "momentum_agent")

3. **Create the profile AND save the token in a single script** — the API call, token extraction, and env var writing must all happen inside one `node -e` script so the token is NEVER visible in terminal output. Write a script file and execute it:

   Write a file called `.claude/profile-launch.js` with this content, then run it with `node .claude/profile-launch.js`:

   ```javascript
   const http = require("http");
   const https = require("https");
   const fs = require("fs");
   const path = require("path");
   const os = require("os");

   const apiUrl = process.env.DFM_API_URL;
   const walletAddress = process.argv[2];
   const agentName = process.argv[3];
   const agentUsername = process.argv[4];

   const payload = JSON.stringify({
     userPublicKey: walletAddress,
     name: agentName,
     username: agentUsername,
     metadata: [{ key: "created_by", value: "dfm-agent-skill" }]
   });

   const url = new URL(apiUrl + "/api/v2/agent/profile-launch");
   const client = url.protocol === "https:" ? https : http;

   const req = client.request(url, {
     method: "POST",
     headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(payload) }
   }, (res) => {
     let data = "";
     res.on("data", (chunk) => data += chunk);
     res.on("end", () => {
       try {
         const json = JSON.parse(data);
         const token = json.data?.token?.token;
         if (!token) { console.log("ERROR: No token in response"); process.exit(1); }

         // Write to .claude/settings.json
         const sp = path.join(process.cwd(), ".claude", "settings.json");
         let s = {}; try { s = JSON.parse(fs.readFileSync(sp, "utf8")); } catch {}
         if (!s.env) s.env = {};
         s.env.DFM_AUTH_TOKEN = token;
         fs.writeFileSync(sp, JSON.stringify(s, null, 2));

         // Append to ~/.zshrc
         fs.appendFileSync(path.join(os.homedir(), ".zshrc"), "\nexport DFM_AUTH_TOKEN=\"" + token + "\"\n");

         // Only output safe info — NEVER the token
         const profileName = json.data?.agentProfile?.name || agentName;
         const profileUsername = json.data?.agentProfile?.username || agentUsername;
         console.log("STATUS=success");
         console.log("AGENT_NAME=" + profileName);
         console.log("AGENT_USERNAME=" + profileUsername);
         console.log("DFM_AUTH_TOKEN=set");
       } catch (e) { console.log("ERROR: " + e.message); process.exit(1); }
     });
   });
   req.on("error", (e) => { console.log("ERROR: " + e.message); process.exit(1); });
   req.write(payload);
   req.end();
   ```

   Run it as: `node .claude/profile-launch.js <WALLET_ADDRESS> "<AGENT_NAME>" "<AGENT_USERNAME>"`

   The script outputs ONLY `STATUS=success`, `AGENT_NAME=...`, `AGENT_USERNAME=...`, and `DFM_AUTH_TOKEN=set`. The actual token value is written directly to `.claude/settings.json` and `~/.zshrc` — it NEVER appears in terminal output.

4. Tell the user: "Agent profile created! Restart Claude Code to pick up the auth token, then you're ready to go."

**If `DFM_AGENT_KEYPAIR` is NOT SET** and the operation requires signing (launch-dtf, distribute-fees), auto-generate a wallet (see "Agent Wallet -- Keypair Generation" section below). Do not ask — just generate it.

### Step 2: Proceed

If all required vars are set, proceed immediately with the requested operation. **Do not ask for confirmation.**

**IMPORTANT:** After writing to `.claude/settings.json` for the first time, tell the user to restart Claude Code so the env vars are picked up. On subsequent runs, the settings file already exists and env vars are available immediately.

## When To Use

Use this skill when:
- The user asks to launch, create, or deploy a DTF vault
- The user asks to research tokens/markets and create a fund
- The user wants to check vault state, policy, or rebalancing status
- The user asks to rebalance a vault or distribute fees
- The user needs to set up agent auth (wallet generation, token management)

## Autonomous DTF Launch -- How It Works

When the user asks you to launch a DTF (e.g. "Create a blue chip Solana fund" or "Launch a meme token DTF"), follow this autonomous workflow:

### Step 1: Research (Agent decides)

Use `WebSearch` and `WebFetch` tools for ALL DTF-related metadata -- token discovery, prices, market caps, volume, liquidity, mint addresses, trending assets, and market conditions. No exceptions.

Use `WebSearch` to find:
- Top performing Solana tokens by market cap, volume, and price action
- Current market conditions, trends, and sentiment
- Token liquidity and 24h trading volume data
- **For yield DTFs**: Solana LSTs (liquid staking tokens) and yield-bearing tokens — mSOL, jitoSOL, bSOL, INF, hSOL, stSOL, and their current APYs, TVLs, and staking yields

Use `WebFetch` to pull data from:
- Token data aggregators (CoinGecko, CoinMarketCap, Jupiter aggregator, Birdeye, DexScreener)
- Solana token lists and verified registries for mint addresses
- **For yield DTFs**: Staking yield aggregators, LST protocol sites (Marinade, Jito, BlazeStake, Sanctum), and DeFi yield dashboards

Then decide:
- Identify candidate tokens based on the user's intent or strategy
- Check token liquidity, 24h volume, market cap
- **For yield DTFs**: Prioritize LSTs and yield-bearing assets with highest APY and deepest liquidity
- Select the best tokens and determine allocations
- Automatically discover each token's Solana `mintAddress` from reliable references (official docs, verified token lists, explorers, major data providers)
- Cross-check mint addresses across multiple references before including them in `underlyingAssets`
- Reject unverified, conflicting, or low-confidence mint mappings and replace them with verified assets

### Step 2: Design (Agent decides)

Based on your research, autonomously decide:
- **Vault type** -- `"DTF"` for standard diversified token funds, `"YIELD_DTF"` for yield-bearing / LST-focused funds. Set in the `dtf-create` payload.
- **Vault name** -- descriptive, catchy, relevant to the strategy
- **Vault symbol** -- short (max 10 chars), unique, memorable
- **Underlying assets** -- pass asset `symbol` or `name` (preferred) with allocation in basis points (must sum to 10000). Backend resolves `mintAddress` from `asset-allocation`.
  - For **DTF**: standard tokens (SOL, JUP, Bonk, RAY, etc.)
  - For **YIELD_DTF**: LSTs and yield-bearing tokens (mSOL, jitoSOL, bSOL, INF, etc.)
- **Management fees** -- in basis points (e.g. 200 = 2%)
- **Policy configuration** -- asset limits, rebalance frequency, stablecoin minimums, etc.
- **Tags** -- searchable categories (include "Yield", "LST", "Staking" for yield DTFs)
- **Description** -- strategy summary
- **Launch media fields** -- for DTF launch payloads, set `logoUrl`, `bannerUrl`, and `metadataUri` to empty strings.

### Step 3: Deploy (Two-step flow)

#### 3a. Build the unsigned transaction

Send `POST {DFM_API_URL}/api/v2/agent/launch-dtf` with the vault creation payload. The backend builds and returns an unsigned transaction.

```json
{
  "signerPublicKey": "<public key derived from DFM_AGENT_KEYPAIR>",
  "vaultName": "Solana Blue Chips",
  "vaultSymbol": "SOLBC",
  "underlyingAssets": [
    { "symbol": "SOL", "mintBps": 4000 },
    { "symbol": "JUP", "mintBps": 3000 },
    { "name": "Bonk", "mintBps": 3000 }
  ],
  "managementFees": 200,
  "category": 0,
  "threshold": 500
}
```

The response contains:
```json
{
  "onChain": {
    "transaction": "base64-encoded-unsigned-versioned-transaction...",
    "vaultIndex": 42,
    "vaultPda": "7Xk...def",
    "vaultMintPda": "9Rm...ghi"
  }
}
```

#### 3b. Sign and submit the transaction on-chain

Use the agent's local keypair to sign the returned transaction and submit it to Solana:

```typescript
import { Keypair, VersionedTransaction, Connection } from "@solana/web3.js";
const bs58 = require("bs58").default || require("bs58");

const keypair = Keypair.fromSecretKey(bs58.decode(process.env.DFM_AGENT_KEYPAIR!));
const connection = new Connection(process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com");

// Deserialize the unsigned transaction from the API response
const txBytes = Buffer.from(response.onChain.transaction, "base64");
const tx = VersionedTransaction.deserialize(txBytes);

// Sign with the agent's keypair
tx.sign([keypair]);

// Submit on-chain
const signature = await connection.sendRawTransaction(tx.serialize(), {
  skipPreflight: false,
  preflightCommitment: "confirmed",
});

await connection.confirmTransaction(signature, "confirmed");
```

#### 3c. Create policy and persist to DB

After the on-chain transaction confirms, send `POST {DFM_API_URL}/api/v2/agent/dtf-create` with the transaction signature and policy configuration:

**You MUST include ALL policy fields in every `dtf-create` payload.** The agent decides values based on the vault strategy. Missing fields default to 0/disabled which means no policy guardrails.

```json
{
  "transactionSignature": "<signature from step 3b>",
  "vaultName": "Solana Blue Chips",
  "vaultSymbol": "SOLBC",
  "vaultType": "DTF",
  "description": "Top-tier Solana ecosystem tokens",
  "tags": ["Blue Chip", "Solana", "DeFi"],
  "logoUrl": "",
  "bannerUrl": "",
  "asset_mode": "OPEN",
  "asset_whitelist": [],
  "asset_blacklist": [],
  "min_amm_liquidity_usd": 100000,
  "min_24h_volume_usd": 500000,
  "min_assets": 3,
  "max_assets": 12,
  "max_asset_pct": 4000,
  "min_asset_pct": 500,
  "min_stablecoin_pct": 0,
  "max_rebalance_pct": 2500,
  "min_rebalance_interval_hours": 4,
  "max_rebalances_per_day": 3,
  "max_rebalances_per_week": 14,
  "launch_blackout_hours": 24,
  "fee_locked": true,
  "notes": "Auto-generated policy for blue chip strategy"
}
```

**Example: WHITELIST mode (for curated LST yield fund):**
```json
{
  "transactionSignature": "<signature>",
  "vaultName": "Solana LST Yield",
  "vaultSymbol": "SLSTY",
  "vaultType": "YIELD_DTF",
  "description": "Diversified Solana liquid staking token yield fund",
  "tags": ["Yield", "LST", "Staking", "Solana"],
  "logoUrl": "",
  "bannerUrl": "",
  "asset_mode": "WHITELIST_ONLY",
  "asset_whitelist": ["mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So", "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn", "bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1"],
  "asset_blacklist": [],
  "min_amm_liquidity_usd": 500000,
  "min_24h_volume_usd": 500000,
  "min_assets": 2,
  "max_assets": 8,
  "max_asset_pct": 5000,
  "min_asset_pct": 1000,
  "min_stablecoin_pct": 0,
  "max_rebalance_pct": 2000,
  "min_rebalance_interval_hours": 12,
  "max_rebalances_per_day": 1,
  "max_rebalances_per_week": 5,
  "launch_blackout_hours": 24,
  "fee_locked": true,
  "notes": "Whitelisted LST-only yield fund — only approved liquid staking tokens allowed"
}
```

#### Policy field decision guide

The agent MUST decide ALL policy values based on the vault strategy:

| Strategy Type | `max_asset_pct` | `min_asset_pct` | `min_amm_liquidity_usd` | `min_24h_volume_usd` | `max_rebalances_per_day` | `min_rebalance_interval_hours` |
|---|---|---|---|---|---|---|
| **Conservative** (blue chip, index) | 3000-4000 | 500-1000 | 500000 | 1000000 | 2 | 6 |
| **Moderate** (mixed, ecosystem) | 4000-5000 | 500 | 100000 | 500000 | 3 | 4 |
| **Aggressive** (meme, trending) | 5000-6000 | 300 | 50000 | 100000 | 4 | 2 |
| **Yield** (LSTs, staking, yield) | 4000-5000 | 500-1000 | 500000 | 500000 | 1 | 12 |

Always set:
- `asset_mode`: choose based on the vault strategy:
  - `"OPEN"` — any asset can be added. No restrictions. Use for broad market / index / aggressive strategies.
  - `"WHITELIST_ONLY"` — only assets in `asset_whitelist` are allowed. Use for curated funds (e.g. "only blue chips", "only LSTs"). Set `asset_whitelist` to the mint addresses of the selected assets.
  - `"OPEN_BLACKLIST"` — all assets allowed except those in `asset_blacklist`. Use when you want to exclude specific risky assets. Set `asset_blacklist` to the mint addresses to exclude.
  - `"WHITELIST_BLACKLIST"` — only whitelisted assets allowed, with additional blacklist exclusions. Use for strict curated funds with explicit exclusions. Set both `asset_whitelist` and `asset_blacklist`.
  - **Decision rule:** If the user asks for a specific category fund (e.g. "LST fund", "blue chip only", "top 5 DeFi tokens"), use `WHITELIST_ONLY`. If the user asks for broad exposure, use `OPEN`. If the user says "exclude meme coins" or similar, use `OPEN_BLACKLIST`.
- `min_assets`: set to the number of assets in the vault (or lower)
- `max_assets`: `12` (hard max)
- `max_rebalance_pct`: `2000`-`3000` (20-30% max change per rebalance)
- `max_rebalances_per_week`: `max_rebalances_per_day * 7` or less
- `launch_blackout_hours`: `24` (prevent rebalancing in first 24h)
- `fee_locked`: `true` (always lock fees)
- `notes`: brief description of the strategy and policy rationale

#### Backend payload rules

For DTF launch payloads:
- `category: 0` (Manual) for agent-created vaults.
- In `underlyingAssets`, send `symbol` or `name` (preferred). Backend resolves `mintAddress` from `asset-allocation`.
- Hard restriction: never include USDC (`symbol: "USDC"` or `name: "USD Coin"`) in `underlyingAssets`.
- If a candidate list contains USDC, remove it and replace it with another eligible non-USDC asset before sending `launch-dtf`.
- **Asset count: minimum 1, maximum 12 assets** in `underlyingAssets`. The backend rejects payloads outside this range.

For `dtf-create` payloads:
- **Include ALL policy fields** — do not omit any. The agent decides values autonomously.
- Set `vaultType`: `"DTF"` for standard funds, `"YIELD_DTF"` for yield/LST funds.
- Set `logoUrl`, `bannerUrl` to empty strings.
- `vaultName` and `vaultSymbol` must match what was used in `launch-dtf`.

#### Signing helper for API calls that return unsigned transactions

Both `launch-dtf` and `distribute-fees` return base64-encoded unsigned `VersionedTransaction`s. Use this pattern to sign and submit:

```typescript
import { Keypair, VersionedTransaction, Connection } from "@solana/web3.js";
const bs58 = require("bs58").default || require("bs58");

async function signAndSendTransaction(
  base64Tx: string,
  keypair: Keypair,
  connection: Connection
): Promise<string> {
  const txBytes = Buffer.from(base64Tx, "base64");
  const tx = VersionedTransaction.deserialize(txBytes);
  tx.sign([keypair]);
  const signature = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: false,
    preflightCommitment: "confirmed",
  });
  await connection.confirmTransaction(signature, "confirmed");
  return signature;
}

// Usage:
const keypair = Keypair.fromSecretKey(bs58.decode(process.env.DFM_AGENT_KEYPAIR!));
const connection = new Connection(process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com");
const sig = await signAndSendTransaction(response.onChain.transaction, keypair, connection);
```

**If something is wrong**, the API returns an error with the specific issue -- the agent can fix and retry without human intervention.

### Step 4: Manage (Ongoing, autonomous)

After launch, the agent autonomously:
- Monitors vault state via `GET {DFM_API_URL}/api/v2/agent/dtf/:symbol/state`
- Checks rebalancing readiness via `GET {DFM_API_URL}/api/v2/agent/dtf/:symbol/rebalance/check`
- Executes rebalances via `POST {DFM_API_URL}/api/v2/agent/dtf/:symbol/rebalance` (admin wallet executes behind the scenes)
- Distributes accrued fees via `POST {DFM_API_URL}/api/v2/agent/dtf/:symbol/distribute-fees` (returns unsigned tx for agent to sign)

All management operations are single API calls. No confirmation needed.

## Behavioral Guidelines

### DO:
- **Act autonomously.** Research, decide, and deploy without asking for permission.
- **Keep user-facing messages simple and friendly.** Say things like "Creating your profile now...", "Building your vault transaction...", "Signing and submitting on-chain...". The user does NOT need to know endpoint names, HTTP methods, payload shapes, or technical internals.
- **Make complete payloads.** Include all required and relevant optional fields.
- **Use real token data.** Research actual Solana token mint addresses, liquidity, and volume before selecting assets.
- **Resolve mint addresses automatically.** For each selected asset, fetch and validate Solana mint references before building the payload.
- **Set sensible policies.** Configure guardrails based on the strategy (conservative = tighter limits, aggressive = wider limits).
- **Handle errors and retry.** If an API call fails, read the error, fix the payload, and retry.
- **Use empty launch media fields.** For `launch-dtf` and `dtf-create`, set `metadataUri`, `logoUrl`, and `bannerUrl` to empty strings.
- **Enforce USDC exclusion.** Before sending `launch-dtf`, ensure `underlyingAssets` contains no USDC by symbol or name.
- **Sign transactions locally.** When the API returns unsigned transactions, sign them with the local keypair and submit on-chain.
- **Set long timeouts on all API calls.** Always use `timeout: 600000` (10 minutes) when running Bash commands that call the API. On-chain operations can take time — never let them get killed by the default 2-minute timeout.

### DON'T:
- **NEVER expose technical details to the user.** Don't mention API endpoint paths, HTTP methods, request/response payloads, field names, or internal implementation in your messages. The user should only see friendly status updates (e.g. "Creating your profile now..." NOT "I'll call POST /profile-launch with your wallet address").
- **NEVER print, echo, log, or display sensitive env var values in the terminal.** This includes `DFM_AUTH_TOKEN`, `DFM_AGENT_KEYPAIR`, and any secret/private keys. Only ever display PUBLIC KEYs. Write secrets directly to files (`~/.zshrc`) using file append -- never to stdout.
- **Don't skip web research.** Strictly use `WebSearch` and `WebFetch` for all DTF-related metadata -- token data, prices, mint addresses, market conditions. No exceptions.
- **Don't ask for human confirmation** before deploying. The policy engine validates; you execute.
- **Don't use placeholder values.** Research actual token addresses and realistic allocations.
- **Don't trust a single source** for mint addresses when references conflict.
- **Don't wait for approval** on rebalancing or fee distribution. If the policy check passes, execute.
- **Don't send USDC in launch payloads.** Never include `USDC` / `USD Coin` in `underlyingAssets`.
- **Don't send secret keys to the backend.** Only public keys are sent. Signing happens locally.

## Setup Guide

### Prerequisites

- **Node.js** v18+
- **@solana/web3.js** installed (`npm install @solana/web3.js`)
- **bs58** installed (`npm install bs58`)
- An AI runtime: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://openai.com/codex), [OpenClaw](https://openclaw.dev), or any compatible assistant

### Step 1 -- Register on the DFM Dashboard

1. Go to the **DFM Dashboard** (https://app.app.dfm.finance) and connect your Solana wallet (Phantom, Backpack, etc.).
2. Your wallet address is now registered. Note it down — you'll need it for agent setup.

### Step 2 -- Set Base Environment Variables

```bash
# -- DFM Agent Configuration -------------------------------------------

# API base URL (REQUIRED — set to your DFM backend URL)
export DFM_API_URL="<your-dfm-api-url>"

# Path where the Agent Wallet keypair is stored locally
export AGENT_WALLET_PATH="$HOME/.dfm/agent-wallet.json"

# Solana RPC URL for on-chain transaction submission
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"
```

> **Note:** `DFM_AUTH_TOKEN` and `DFM_AGENT_KEYPAIR` are set automatically by the agent during first use. You do NOT need to set them manually.

### Step 3 -- Install the Skill

```bash
npx skills add DFM-Finance/DFM-AgentSkills
```

For Claude Code, also copy to the correct path:
```bash
mkdir -p .claude/skills
cp -r .agents/skills/dfm-agent .claude/skills/dfm-agent
```

### Step 4 -- Allow Permissions (One-Time)

On the first command, Claude Code will ask for permission to run scripts. Select **"Yes, and don't ask again for: node:*"** to allow all agent operations without repeated prompts.

### Step 5 -- First Use (Automatic Setup)

When you first use the skill, the agent will automatically:

1. **Ask for your wallet address** — the one you registered on the DFM Dashboard
2. **Create your agent profile** — auto-generates a name and username via `POST /profile-launch`
3. **Save the auth token** — writes the returned JWT to `.claude/settings.json` and `~/.zshrc` (never printed)
4. **Generate an agent wallet** — creates a Solana keypair, saves to `AGENT_WALLET_PATH`, writes `DFM_AGENT_KEYPAIR` to `~/.zshrc`
5. **Report the public key only** — never displays secret keys or tokens

After this one-time setup, restart Claude Code and you're ready to go.

**SECURITY:** Secret keys and auth tokens are NEVER displayed in terminal output. They are written directly to files with restricted permissions.

## Auth

All endpoints are at `{DFM_API_URL}/api/v2/agent/...` and require `Authorization: Bearer <DFM_AUTH_TOKEN>`.

Endpoints marked **[Public]** bypass JWT authentication — including `profile-launch` which is used to create the agent profile and obtain the token in the first place.

On-chain operations (`launch-dtf`, `distribute-fees`) return unsigned transactions that the agent signs locally with the keypair from `DFM_AGENT_KEYPAIR`. Rebalancing is executed server-side by the admin wallet.

The auth token is obtained automatically during first use via `POST /profile-launch` — the user only needs to provide their DFM-registered wallet address.

## Agent Wallet -- Keypair Generation

### Wallet path resolution

1. `AGENT_WALLET_PATH` env variable
2. `SOLANA_KEYPAIR_PATH` env variable
3. `WALLET_OUTPUT_PATH` env variable
4. Default: `<project-root>/solana-keypair/keypair.json`

### Implementation

```typescript
import { Keypair } from "@solana/web3.js";
const bs58 = require("bs58").default || require("bs58");
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

// 1. Resolve output path
const outPath = path.resolve(
  process.env.AGENT_WALLET_PATH ??
    process.env.SOLANA_KEYPAIR_PATH ??
    process.env.WALLET_OUTPUT_PATH ??
    path.join(os.homedir(), ".dfm", "agent-wallet.json")
);

// 2. Generate keypair and save to file
fs.mkdirSync(path.dirname(outPath), { recursive: true });
const keypair = Keypair.generate();
fs.writeFileSync(outPath, JSON.stringify(Array.from(keypair.secretKey)), { mode: 0o600 });

// 3. Write base58 secret key directly to shell profile (NEVER print to terminal)
const base58Secret = bs58.encode(keypair.secretKey);
const shellProfile = path.join(os.homedir(), ".zshrc");
fs.appendFileSync(shellProfile, `\nexport DFM_AGENT_KEYPAIR="${base58Secret}"\n`);

// 4. Only output the PUBLIC KEY
const pubkey = keypair.publicKey.toBase58();
console.log(`PUBLIC_KEY=${pubkey}`);
console.log(`WALLET_PATH=${outPath}`);
// NEVER console.log the base58Secret — it was written to ~/.zshrc silently
```

**CRITICAL:** The `base58Secret` is written directly to `~/.zshrc` via `fs.appendFileSync`. It must NEVER be printed to stdout, logged, or displayed in any terminal output. Only the public key is shown to the user.

### Deriving public key from env (for API calls)

```typescript
import { Keypair } from "@solana/web3.js";
const bs58 = require("bs58").default || require("bs58");

const keypair = Keypair.fromSecretKey(bs58.decode(process.env.DFM_AGENT_KEYPAIR!));
const signerPublicKey = keypair.publicKey.toBase58();
// Use signerPublicKey in API request bodies
```

## API Quick Reference

> For full request/response schemas, see `references/api-reference.md`

| Action | Method | Endpoint | Auth | Body |
|---|---|---|---|---|
| Launch agent profile | `POST` | `/profile-launch` | No | `userPublicKey` + name/username |
| Build vault tx | `POST` | `/launch-dtf` | JWT | `signerPublicKey` + vault config |
| Create DTF (policy + DB) | `POST` | `/dtf-create` | JWT | `transactionSignature` + policy config |
| Vault state | `GET` | `/dtf/:symbol/state` | JWT | - |
| Vault policy | `GET` | `/dtf/:symbol/policy` | JWT | - |
| Rebalance check | `GET` | `/dtf/:symbol/rebalance/check` | JWT | - |
| Rebalance | `POST` | `/dtf/:symbol/rebalance` | JWT | `signerPublicKey` |
| Build distribute fees tx | `POST` | `/dtf/:symbol/distribute-fees` | JWT | `signerPublicKey` |
| Revoke token | `POST` | `/token/revoke` | JWT | - |
| Refresh token | `POST` | `/token/refresh` | No | `profileId` |

### On-chain operations

- **Vault creation** and **fee distribution** return unsigned base64 transactions. The agent signs locally and submits on-chain.
- **Rebalancing** is executed server-side by the admin wallet. The agent only provides its public key for identification.

### Logo handling

- For `launch-dtf` and `dtf-create`, always send `metadataUri: ""`, `logoUrl: ""`, and `bannerUrl: ""`.
- Do not pass image URLs for these fields in launch payloads.

## Using Agent Commands

| What you say | What the agent does |
|---|---|
| `Set up my DFM agent` | Asks for wallet address, creates agent profile via `/profile-launch`, saves auth token, generates keypair |
| `Launch a Solana blue chip fund` | Researches top SOL tokens, picks name/symbol/allocations/policy, builds tx, signs, submits, creates policy |
| `Create a meme token DTF with 3% fee` | Finds trending meme tokens, builds diversified allocation, sets policy, deploys |
| `Show me the state of SOLBC` | `GET /dtf/SOLBC/state` -- returns APY, TVL, NAV, portfolio |
| `Rebalance SOLBC` | Checks policy, triggers server-side rebalance if approved |
| `Distribute fees for SOLBC` | `POST /dtf/SOLBC/distribute-fees` -- builds unsigned tx, signs locally, submits on-chain |
| `Generate a Solana keypair for my DFM Agent wallet` | Creates keypair, saves to file, writes env var, reports public key only |

## Troubleshooting

| Problem | Fix |
|---|---|
| **"Unauthorized" errors** | Token expired (30-day limit). Refresh via `POST /token/refresh`. Verify: `echo $DFM_AUTH_TOKEN` |
| **"Keypair file not found"** | Re-generate wallet (Step 4). Check: `ls -la $AGENT_WALLET_PATH` |
| **"No signer keypair" / empty DFM_AGENT_KEYPAIR** | `DFM_AGENT_KEYPAIR` not set. Re-export (Step 5). Verify: `echo $DFM_AGENT_KEYPAIR` |
| **Transaction fails on-chain** | Agent Wallet needs SOL for tx fees + USDC for vault creation fee. Fund the wallet first. |
| **Policy validation error** | Read the error message -- it tells you exactly which field/rule failed. Fix and retry. |
| **Token revoked unexpectedly** | A token refresh revokes **all** prior tokens. One active token per agent. |
| **409 Conflict on dtf-create** | A policy already exists for this vault name/symbol. Use a unique name and symbol. |

## Security

- **NEVER display sensitive values in terminal output.** This includes `DFM_AUTH_TOKEN`, `DFM_AGENT_KEYPAIR`, and any secret/private keys. Only public keys may be printed. Secrets are written silently to files.
- **Agent Wallet file** -- `0o600` permissions, gitignored, never committed.
- **`DFM_AGENT_KEYPAIR`** -- base58 secret key in env only, never in code, git, or terminal output.
- **`DFM_AUTH_TOKEN`** -- JWT token in env only, never printed or logged in terminal.
- **No secret keys sent to backend** -- only public keys are included in API payloads. Transaction signing happens locally.
- **Agent Wallet = on-chain authority** -- treat it like any crypto wallet. Back up securely.
- **Policy engine = safety net** -- even a fully autonomous agent can't bypass policy constraints.
