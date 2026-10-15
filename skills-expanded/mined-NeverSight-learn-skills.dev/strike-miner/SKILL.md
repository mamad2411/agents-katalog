---
name: strike-miner
description: "Mine rewards by predicting crypto price direction on 15-min Polymarket rounds with stake-gated proof-of-prediction mining on Solana."
metadata: { "openclaw": { "emoji": "⚡", "requires": { "env": ["SOLANA_KEYPAIR_PATH"] } } }
---

# Strike Miner

Mine rewards by predicting crypto price direction on Polymarket 15-minute rounds. Every 15 minutes, new "Up or Down" markets open for 7 tokens (BTC, ETH, SOL, XRP, DOGE, HYPE, BNB). Your AI agent commits hashed predictions on-chain (Solana), reveals them after each round resolves, and earns credits proportional to accuracy × tier. Credits are redeemable for token rewards each epoch (~96 rounds/day).

**No external wallet service required.** Your agent holds a local Solana keypair. The coordinator returns unsigned transactions — your agent signs and submits them directly to Solana RPC.

## Prerequisites

1. **Solana keypair** on disk. Set the path as `SOLANA_KEYPAIR_PATH` env var (default: `~/.config/solana/id.json`).
   - Generate one if needed: `solana-keygen new --outfile ~/.config/solana/id.json`
   - Fund with a small amount of SOL for transaction fees (~0.01 SOL covers hundreds of TXs)

2. **Strike tokens** in a token account associated with your keypair. Minimum **1,000,000 tokens** (Tier 1) to mine.
   - Token has 6 decimals. 1,000,000 whole tokens = `1000000000000` base units.
   - Purchase on a Solana DEX (Raydium, Jupiter) or via Pump.fun.

3. **Environment variables:**
   | Variable | Default | Required |
   |----------|---------|----------|
   | `SOLANA_KEYPAIR_PATH` | `~/.config/solana/id.json` | Yes |
   | `COORDINATOR_URL` | `https://strike-coordinator-production.up.railway.app` | No |
   | `SOLANA_RPC_URL` | `http://localhost:8899` | No |

4. **Tools needed:** `curl`, `jq`, `solana` CLI (for signing), `base64` (for TX decode/encode).

## Architecture

```
Agent (this skill)              Coordinator                  Solana
─────────────────               ───────────                  ──────
1. POST /auth/nonce        ──►  generate nonce
2. sign nonce locally
3. POST /auth/verify       ──►  verify sig, return JWT

── continuous mining loop (every 15 min) ──
4. GET /round              ──►  return current round markets (7 tokens)
5. analyze markets, predict Up or Down
6. POST /submit-commit     ──►  return unsigned commit TX
7. sign TX, submit to RPC  ─────────────────────────────►  on-chain commit
8. (wait ~15 min for round to resolve)
9. POST /submit-reveal     ──►  return unsigned reveal TX
10. sign TX, submit to RPC ─────────────────────────────►  on-chain reveal
11. loop back to step 4 for next round
── end of epoch (24h) ──

12. (coordinator scores all rounds)
13. GET /claim-calldata    ──►  return unsigned claim TX
14. sign TX, submit to RPC ─────────────────────────────►  on-chain claim
```

## Tier System

Staking tokens on the program is required to mine. A 1% mining fee is deducted at stake time and added to the current epoch's reward pool. Higher tiers earn more credits per correct prediction.

| Tier | Minimum Stake | Credits per Correct Prediction |
|------|---------------|-------------------------------|
| 1 | 1,000,000 tokens | 1 credit |
| 2 | 10,000,000 tokens | 2 credits |
| 3 | 100,000,000 tokens | 3 credits |

## Setup Flow

When the user asks to mine, follow these steps in order:

### 1. Load Keypair and Resolve Miner Address

Read the Solana keypair from disk and derive the public key:

```bash
MINER=$(solana address -k "${SOLANA_KEYPAIR_PATH:-$HOME/.config/solana/id.json}")
echo "Miner address: $MINER"
```

**CHECKPOINT**: Tell the user their mining wallet address. Example:
> Your mining wallet is `ABC...XYZ` on Solana. This address needs tokens staked and a small amount of SOL for transaction fees.

Do NOT proceed until you have successfully resolved the wallet address.

### 2. Check SOL Balance

```bash
solana balance "$MINER" --url "${SOLANA_RPC_URL:-http://localhost:8899}"
```

If SOL balance is zero or very low (<0.005 SOL), the user needs to fund the wallet for transaction fees. Stop and inform them.

### 3. Stake Tokens

Miners must **stake** tokens on the program before they can submit predictions. Staking locks tokens in the program vault and assigns a tier based on staked amount.

**Step 1: Get your token account address.** This is the associated token account (ATA) for your wallet and the Strike mint.

```bash
MINER_TOKEN_ACCOUNT=$(spl-token accounts --owner "$MINER" --url "${SOLANA_RPC_URL:-http://localhost:8899}" | grep "$STRK_MINT" | awk '{print $1}')
```

**Step 2: Get unsigned stake transaction from coordinator:**

```bash
# amount in base units (6 decimals). 1M ENEL = 1000000000000
curl -s -X POST "${COORDINATOR_URL:-http://localhost:3000}/v1/submit-stake" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"miner\": \"$MINER\",
    \"amount\": \"1000000000000\",
    \"minerTokenAccount\": \"$MINER_TOKEN_ACCOUNT\"
  }"
```

Response: `{ "transaction": "<base64-encoded unsigned TX>" }`

**Step 3: Sign and submit:**

```bash
# Decode, sign, and send
echo "$TX_BASE64" | base64 -d > /tmp/strike_tx.bin
solana confirm -v $(
  solana send-transaction /tmp/strike_tx.bin \
    --keypair "${SOLANA_KEYPAIR_PATH:-$HOME/.config/solana/id.json}" \
    --url "${SOLANA_RPC_URL:-http://localhost:8899}"
)
```

**Unstake flow (two steps, with cooldown):**

1. **Request unstake** — `POST /v1/submit-unstake` with `{ "miner": "$MINER" }`. Sign and submit. This immediately sets tier to 0 and starts the 24-hour cooldown.
2. **Withdraw** — After cooldown, `POST /v1/submit-withdraw` with `{ "miner": "$MINER", "minerTokenAccount": "$MINER_TOKEN_ACCOUNT" }`. Sign and submit. Tokens return to your wallet.

**CHECKPOINT**: Confirm stake is active (≥1M staked, no pending unstake) before proceeding.

### 4. Authenticate

Complete the auth handshake to obtain a bearer token for coordinator API calls.

```bash
# Step 1: Request nonce
NONCE_RESPONSE=$(curl -s -X POST "${COORDINATOR_URL:-http://localhost:3000}/v1/auth/nonce" \
  -H "Content-Type: application/json" \
  -d "{\"miner\": \"$MINER\"}")
MESSAGE=$(echo "$NONCE_RESPONSE" | jq -r '.message')
NONCE=$(echo "$NONCE_RESPONSE" | jq -r '.nonce')

# Step 2: Sign the message with ed25519 (Solana native)
# The message must be signed as raw bytes using the keypair's ed25519 key
SIGNATURE=$(echo -n "$MESSAGE" | solana sign \
  --keypair "${SOLANA_KEYPAIR_PATH:-$HOME/.config/solana/id.json}" \
  --output bs58)

# Step 3: Verify and obtain JWT
VERIFY_RESPONSE=$(curl -s -X POST "${COORDINATOR_URL:-http://localhost:3000}/v1/auth/verify" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg miner "$MINER" --arg msg "$MESSAGE" --arg sig "$SIGNATURE" \
    '{miner: $miner, message: $msg, signature: $sig}')")
TOKEN=$(echo "$VERIFY_RESPONSE" | jq -r '.token')
EXPIRES_AT=$(echo "$VERIFY_RESPONSE" | jq -r '.expiresAt')
```

**Auth token reuse (critical):**
- Perform nonce+verify **once**, then reuse the token for all challenge/submit calls until it expires.
- Do NOT run auth handshake inside the mining loop.
- Only re-auth on 401 from any endpoint, or when token is within 60 seconds of expiry.
- The `expiresAt` field is a Unix timestamp — compare with `date +%s`.

**Auth handshake rules:**
- **Always** send `Authorization: Bearer $TOKEN` on protected endpoints (challenge, submit-*, claim-*).
- Use the nonce message exactly as returned — no edits, trimming, or reformatting.
- Do not reuse a nonce — each handshake gets a fresh nonce from `/v1/auth/nonce`.
- Build JSON payloads with `jq --arg` to avoid newline corruption.

**Validation (fail fast):** Before continuing, verify: nonce response has `.message`, verify response has `.token`. If missing or null, stop and retry from step 1.

### 5. Start Mining Loop

Once stake and auth are confirmed, enter the continuous mining loop. Each epoch runs for 24 hours. Within an epoch, new 15-minute rounds appear continuously (~96 rounds/day). Both commit and reveal windows are open for the entire epoch — you commit and reveal continuously.

#### Step A: Get Current Round

```bash
ROUND_INFO=$(curl -s "${COORDINATOR_URL:-http://localhost:3000}/v1/round" \
  -H "Authorization: Bearer $TOKEN")
EPOCH_ID=$(echo "$ROUND_INFO" | jq -r '.epochId')
ROUND_END=$(echo "$ROUND_INFO" | jq -r '.roundEnd')
```

Response contains:
- `epochId` — the epoch you're mining in; **record this** for claiming later
- `roundEnd` — when this round's markets resolve (Unix timestamp)
- `creditsPerSolve` — 1, 2, or 3 depending on your staked tier
- `markets` — array of 7 crypto "Up or Down" markets (one per token):
  - `marketId` — hex-encoded 32-byte deterministic ID (used in commit/reveal)
  - `sourceMarketId` — Polymarket conditionId (hex)
  - `question` — e.g., "Bitcoin Up or Down - 15 min"
  - `token` — BTC, ETH, SOL, XRP, DOGE, HYPE, or BNB

If no round is active, wait and poll again.

#### Step B: Analyze Markets and Decide

For each market in the round, your agent must decide: **Up (2)** or **Down (1)**.

Use whatever reasoning approach works best for your LLM:
- Consider recent price action, momentum, volatility
- 15-minute timeframe — short-term signals matter most
- Make a binary prediction: will the price go up (2) or down (1)?

**Tips for prediction quality:**
- More capable models with extended thinking tend to predict better
- Consider momentum and recent candle patterns for 15-min predictions
- Diversify across the 7 tokens — don't always predict the same direction

#### Step C: Commit Predictions

For each market, generate a random salt and commit the hash.

**Commit hash construction** (must match the on-chain program exactly):
```
SHA256(salt + miner_pubkey + epoch_id_le_bytes + market_id + prediction_byte)
```

Where:
- `salt`: 32 random bytes (hex-encoded for API, save for reveal)
- `miner_pubkey`: your wallet's 32-byte public key
- `epoch_id_le_bytes`: epoch ID as 8-byte little-endian
- `market_id`: 32-byte market ID from challenge response
- `prediction_byte`: `0x01` for NO, `0x02` for YES

```bash
# Generate salt (save this — you need it to reveal!)
SALT=$(openssl rand -hex 32)

# Compute the hash (example using Python for byte manipulation)
HASH=$(python3 -c "
import hashlib, struct
salt = bytes.fromhex('$SALT')
miner = bytes.fromhex('$(solana address -k $SOLANA_KEYPAIR_PATH | python3 -c \"import sys; from base58 import b58decode; print(b58decode(sys.stdin.read().strip()).hex())\")')
epoch = struct.pack('<Q', $EPOCH_ID)
market = bytes.fromhex('$MARKET_ID')
prediction = bytes([2])  # 2=YES, 1=NO
h = hashlib.sha256(salt + miner + epoch + market + prediction).hexdigest()
print(h)
")

# Get unsigned commit transaction
COMMIT_RESPONSE=$(curl -s -X POST "${COORDINATOR_URL:-http://localhost:3000}/v1/submit-commit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"miner\": \"$MINER\",
    \"marketId\": \"$MARKET_ID\",
    \"hash\": \"$HASH\"
  }")
TX_BASE64=$(echo "$COMMIT_RESPONSE" | jq -r '.transaction')
```

Sign and submit the transaction to Solana RPC (same pattern as staking).

**CRITICAL:** Save the `SALT`, `MARKET_ID`, `PREDICTION`, and `EPOCH_ID` for each commitment. You need all of these to reveal later. If you lose the salt, your prediction cannot be revealed and you earn zero credits for that market.

Repeat for each market in the challenge set.

#### Step D: Reveal Predictions

After the round resolves (~15 min after commit), reveal each committed prediction:

```bash
REVEAL_RESPONSE=$(curl -s -X POST "${COORDINATOR_URL:-http://localhost:3000}/v1/submit-reveal" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"miner\": \"$MINER\",
    \"epochId\": $EPOCH_ID,
    \"marketId\": \"$MARKET_ID\",
    \"salt\": \"$SALT\",
    \"prediction\": $PREDICTION
  }")
TX_BASE64=$(echo "$REVEAL_RESPONSE" | jq -r '.transaction')
```

Sign and submit each reveal TX. The on-chain program verifies `SHA256(salt + miner + epoch + market + prediction)` matches the original commit hash. If it doesn't match, the TX will fail.

**CRITICAL:** Reveal predictions before the epoch ends. Unrevealed predictions are treated as wrong — you earn zero credits for them.

#### Step E: Loop to Next Round

After revealing, immediately check for the next round. New rounds appear every 15 minutes.

```bash
# Wait for next round, then go back to Step A
sleep 60  # brief pause, then poll for next round
```

When `epochId` increments, the previous epoch is scored. Claim rewards (Step 6), then continue mining in the new epoch.

### 6. Claim Rewards

After an epoch ends and is funded, claim your token rewards.

**Check credits:**

```bash
curl -s "${COORDINATOR_URL:-http://localhost:3000}/v1/credits?miner=$MINER"
```

Returns your credits per epoch. Claimable epochs are those where:
1. Epoch has ended (`epochId < currentEpoch`)
2. Epoch has rewards (funded by mining fee pool from staking fees)
3. You earned credits (correctly predicted and revealed)
4. You haven't already claimed

**Claim:**

```bash
# Single epoch
CLAIM_RESPONSE=$(curl -s "${COORDINATOR_URL:-http://localhost:3000}/v1/claim-calldata?epochs=$EPOCH_ID&miner=$MINER&minerTokenAccount=$MINER_TOKEN_ACCOUNT" \
  -H "Authorization: Bearer $TOKEN")

# Multiple epochs (comma-separated)
CLAIM_RESPONSE=$(curl -s "${COORDINATOR_URL:-http://localhost:3000}/v1/claim-calldata?epochs=1,2,3&miner=$MINER&minerTokenAccount=$MINER_TOKEN_ACCOUNT" \
  -H "Authorization: Bearer $TOKEN")
```

Response: `{ "transactions": [{ "epochId": 1, "transaction": "<base64>" }, ...] }`

Sign and submit each transaction.

**Reward formula:**
```
miner_reward = epoch_reward_pool × (miner_credits / total_epoch_credits)
```

### 7. Close Commitments (Rent Recovery)

After claiming rewards for an epoch, close your commitment PDAs to recover rent SOL:

```bash
CLOSE_RESPONSE=$(curl -s "${COORDINATOR_URL:-http://localhost:3000}/v1/close-commitment-calldata?epochId=$EPOCH_ID&miner=$MINER&marketId=$MARKET_ID" \
  -H "Authorization: Bearer $TOKEN")
TX_BASE64=$(echo "$CLOSE_RESPONSE" | jq -r '.transaction')
```

Sign and submit. The rent (~0.002 SOL per commitment) is refunded to your wallet. Do this for each market you committed to in the epoch.

## Transaction Signing Pattern

All coordinator endpoints return base64-encoded unsigned Solana transactions. The signing pattern is the same for every operation:

```bash
# 1. Get unsigned TX from coordinator
TX_BASE64=$(echo "$RESPONSE" | jq -r '.transaction')

# 2. Decode, sign, and submit
echo "$TX_BASE64" | base64 -d > /tmp/strike_tx.bin

# Using solana CLI:
solana send-transaction /tmp/strike_tx.bin \
  --keypair "${SOLANA_KEYPAIR_PATH:-$HOME/.config/solana/id.json}" \
  --url "${SOLANA_RPC_URL:-http://localhost:8899}" \
  --skip-preflight
```

**Important:** Use `--skip-preflight` for reveal and claim TXs to avoid simulation failures due to timing edge cases. The on-chain program enforces all constraints.

## Epoch Timeline

```
T=0h                                                      T=24h
 │                                                          │
 ├──────────────────────────────────────────────────────────┤
 │  COMMIT + REVEAL OPEN (overlapping, continuous)          │
 │                                                          │
 │  round 1 ──► round 2 ──► round 3 ──► ... ──► round 96   │
 │  (15 min)    (15 min)    (15 min)            (15 min)    │
 ▼                                                          ▼
 epoch                                                      epoch
 starts                                                     ends → scoring
```

- **Epoch**: 24 hours, commit and reveal windows open the entire time
- **Rounds**: New round every 15 minutes (~96 rounds/day), 7 crypto markets each
- **Commit**: Must commit before the round's market resolves (coordinator enforces)
- **Reveal**: Reveal after the round resolves, before the epoch ends
- **Scoring**: After epoch ends — coordinator sums all correct predictions, scores miners
- **Claim**: After funding — claim proportional token rewards

## API Reference

All endpoints are prefixed with `/v1/`.

### Public Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/health` | Health check, current epoch, market count |
| GET | `/v1/epoch` | Current epoch timing info |
| GET | `/v1/credits?miner=<pubkey>` | Miner's credits per epoch (last 10) |

### Auth Endpoints

| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | `/v1/auth/nonce` | `{ miner }` | Request signing nonce |
| POST | `/v1/auth/verify` | `{ miner, message, signature }` | Verify sig, get JWT |

### Protected Endpoints (require `Authorization: Bearer <token>`)

| Method | Path | Body/Query | Description |
|--------|------|------------|-------------|
| GET | `/v1/challenge` | — | Get challenge set (market list) |
| GET | `/v1/round` | — | Get current 15-min round markets |
| POST | `/v1/submit-commit` | `{ miner, marketId, hash }` | Get unsigned commit TX |
| POST | `/v1/submit-reveal` | `{ miner, epochId, marketId, salt, prediction }` | Get unsigned reveal TX |
| POST | `/v1/submit-stake` | `{ miner, amount, minerTokenAccount }` | Get unsigned stake TX |
| POST | `/v1/submit-unstake` | `{ miner }` | Get unsigned unstake TX |
| POST | `/v1/submit-withdraw` | `{ miner, minerTokenAccount }` | Get unsigned withdraw TX |
| GET | `/v1/claim-calldata` | `?epochs=1,2&miner=<pk>&minerTokenAccount=<pk>` | Get unsigned claim TX(s) |
| GET | `/v1/close-commitment-calldata` | `?epochId=1&miner=<pk>&marketId=<hex>` | Get unsigned close TX |

### Field Formats

- `miner`: base58-encoded Solana public key
- `marketId`: 64 hex chars (32 bytes)
- `hash`: 64 hex chars (32 bytes, SHA256 output)
- `salt`: 64 hex chars (32 bytes)
- `prediction`: `1` (Down) or `2` (Up)
- `epochId`: integer
- `amount`: string representation of base units (6 decimals)
- `transaction`: base64-encoded unsigned Solana transaction

## Error Handling

### Coordinator errors (retry with backoff)

Use one retry helper for all coordinator calls.

**Backoff:** Retry on `429`, `5xx`, network timeouts. Backoff: `2s, 4s, 8s, 16s, 30s, 60s` (cap 60s). Add 0–25% jitter. Stop after 6 attempts; surface clear error.

**Per endpoint:**
- **`POST /v1/auth/nonce`** — 429/5xx: retry. Other 4xx: fail.
- **`POST /v1/auth/verify`** — 429: retry with backoff. 401: get fresh nonce, re-sign, retry once. 403: stop (insufficient stake).
- **`GET /v1/challenge`** — 429/5xx: retry. 401: re-auth then retry. 403: stop (insufficient stake).
- **`POST /v1/submit-commit`** — 429/5xx: retry. 401: re-auth, retry. 400: check field formats.
- **`POST /v1/submit-reveal`** — 429/5xx: retry. 401: re-auth, retry. 400: check hash matches.
- **`GET /v1/claim-calldata`** — 429/5xx: retry. 400: fix epoch/miner format.

**Concurrency:** Max 1 in-flight auth per wallet. Max 1 in-flight submit per wallet. No tight loops.

### On-chain transaction errors

- **CommitWindowClosed**: You're past the commit deadline for this round. Wait for the next round.
- **RevealWindowNotOpen / RevealWindowClosed**: Not in the reveal window. Check epoch timing.
- **HashMismatch**: Your reveal data doesn't match the committed hash. Verify salt, prediction, and market ID match exactly what you committed.
- **InsufficientStake / NotEligible**: Stake more tokens to reach Tier 1 (1M minimum).
- **UnstakePending**: Cannot commit while unstake is pending. Cancel unstake or wait.
- **EpochNotFunded**: No rewards in epoch pool (no miners staked during this epoch). Try claiming later.
- **AlreadyClaimed**: You already claimed this epoch. Skip it.
- **AlreadyRevealed**: This commitment was already revealed. Skip it.
- **AlreadyScored**: This miner was already scored for this epoch. This is not an error for the miner.

### LLM provider errors

- **401/403 from LLM API**: Stop and tell the user to check their API key.
- **429 from LLM API**: Wait 30–60 seconds, retry.
- **5xx from LLM API**: Wait 30 seconds, retry up to 2 times.
- **Timeout (>5 minutes)**: Abort and retry. If it times out twice, stop and inform user.

### Critical rules

- **Never lose your salt.** Store salt + prediction + marketId + epochId immediately after committing. Without the salt you cannot reveal and earn zero credits.
- **Reveal before the window closes.** Unrevealed = wrong. Set a timer.
- **One auth token per session.** Don't re-auth inside the mining loop.
- **Don't spam.** One commit per market per epoch. One reveal per commitment.

## Quick Start Summary

```
1. Load keypair               → solana address -k ~/.config/solana/id.json
2. Stake tokens               → POST /v1/submit-stake → sign → submit
3. Auth handshake              → POST /auth/nonce → sign → POST /auth/verify → JWT

── continuous mining loop (every 15 min) ──
4. Get current round           → GET /v1/round
5. For each market (7 tokens):
   a. Decide Up/Down
   b. Generate salt, compute SHA256 hash
   c. Commit                   → POST /v1/submit-commit → sign → submit
6. Wait ~15 min for round to resolve
7. For each commitment:
   a. Reveal                   → POST /v1/submit-reveal → sign → submit
8. Loop → step 4 (next round)
── end of epoch (24h) ──

9. Claim rewards               → GET /v1/claim-calldata → sign → submit
10. Close commitments          → GET /v1/close-commitment-calldata → sign → submit
11. Continue mining in new epoch → step 4
```
