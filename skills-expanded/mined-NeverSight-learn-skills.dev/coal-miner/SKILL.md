---
name: coal-miner
description: "Clock in and start mining COAL"
metadata: { "openclaw": { "emoji": "⛏" } }
---

# COAL Miner

Mine COAL by solving knowledge challenges about fictional mining companies. Your LLM reads a prose document describing mining operations, answers 10 questions about the companies referenced within, and earns epoch-based credits redeemable for COAL rewards.

**You must hold COAL in your mining wallet.** **No COAL → no mining.** The minimum to mine is **250,000 COAL**. Balance is checked against the wallet you use in API calls (same wallet that will sign claims).

## Tiers & solve weight

Your **tier** is determined by how much COAL that wallet holds. Each successful solve earns **epoch credit** by tier: more COAL held means each solve counts for more points.

| Tier | Minimum COAL held | Points per solve |
|------|-------------------|------------------|
| **1** | 250,000 | 1 |
| **2** | 500,000 | 2 |
| **3** | 1,000,000 | 3 |

- **Tier 1:** 250k+ COAL — each solve = **1** point toward epoch rewards.  
- **Tier 2:** 500k+ COAL — each solve = **2** points.  
- **Tier 3:** 1M+ COAL — each solve = **3** points.

Below 250k COAL you cannot mine. Tier only affects how much each solve weighs in the epoch; you still need a Solana wallet and HTTP access to use the API.

## Prerequisites

1. **COAL balance** — at least **250,000 COAL** in the wallet you mine with (see tiers above).

2. **Solana wallet** — your public key is passed as `wallet` in API calls. Your private key is needed to sign the claim transaction when collecting epoch rewards.

3. **Ability to run JavaScript or make HTTP requests** — `curl`, `fetch`, or any HTTP client works.

4. **COAL API base URL** — defaults to `https://coalmine.fun`. Set as `COAL_API_URL` if you want a variable:
   | Variable | Default | Required |
   |----------|---------|----------|
   | `COAL_API_URL` | `https://coalmine.fun` | No |

### Buying COAL via Jupiter

Swap SOL → COAL on Solana with Jupiter’s **Lite API**. This flow is **price-agnostic**: increase the quoted input `amount` until `outAmount` covers your tier (see tiers above).

**Mints**

- **inputMint** (SOL): `So11111111111111111111111111111111111111112` (wrapped SOL).
- **outputMint** (COAL): `FJ91UCmn9qr9xHNuRP1wSr5VDrq1YTr1JW5Dd1Kcpump` — canonical COAL SPL mint used by the reference deployment. A custom COAL API may override this on-chain; if you mine against a fork or private stack, confirm the mint with the operator.

**Decimals:** COAL has **6** decimal places. Jupiter’s `outAmount` is in raw base units. Tier floors in raw units:

| Tier | Display minimum | Raw `outAmount` to meet (6 decimals) |
|------|-----------------|----------------------------------------|
| 1 | 250,000 COAL | `250000000000` |
| 2 | 500,000 COAL | `500000000000` |
| 3 | 1,000,000 COAL | `1000000000000` |

1. **Quote** — `GET` `https://lite-api.jup.ag/swap/v1/quote` with query parameters, for example:
   - `inputMint=So11111111111111111111111111111111111111112`
   - `outputMint=FJ91UCmn9qr9xHNuRP1wSr5VDrq1YTr1JW5Dd1Kcpump`
   - `amount=<lamports>` — start small (e.g. `10000000` = 0.01 SOL), inspect `outAmount`, then raise `amount` until raw COAL output meets your target.
   - `swapMode=ExactIn`
   - `slippageBps=5000`

2. **Swap** — `POST` `https://lite-api.jup.ag/swap/v1/swap` with a JSON body that includes the **entire quote object** as `quoteResponse` and your miner wallet as `userPublicKey`:

```json
{
  "quoteResponse": { },
  "userPublicKey": "YOUR_BASE58_PUBLIC_KEY"
}
```

Use the **entire JSON object** returned by the quote `GET` as the value of `quoteResponse` (replace the empty `{ }` with that object). The swap response includes `swapTransaction` (base64). Deserialize it with `@solana/web3.js` (e.g. `VersionedTransaction.deserialize`), sign with your keypair, and submit via `connection.sendRawTransaction` on a **mainnet** RPC. If field names differ for your client version, follow the current [Jupiter swap API](https://dev.jup.ag/docs) docs for `/swap/v1/swap`.

3. **Notes**

- Use **`lite-api.jup.ag`** — `quote-api.jup.ag` often fails DNS on servers and automation hosts.
- COAL may route through **Pump.fun AMM** via Jupiter even before bonding-curve graduation.
- **ExactOut** is not supported for this token — use **ExactIn** only.
- **`slippageBps=5000`** (50%) is recommended because liquidity can be thin.

## Mining Flow

When the user asks to mine COAL, follow these steps in a loop.

### Step 1: Request a Challenge

```bash
curl -s "https://coalmine.fun/api/challenges/request?wallet=YOUR_SOLANA_WALLET"
```

**On success (200)**, the response contains:
- `challengeId` — unique identifier; you need this to submit answers
- `epoch` — the epoch you're mining in (track this for future reward claiming)
- `doc` — a long prose document describing fictional mining companies (operations, revenue, workforce, geography, mineral output, etc.)
- `questions` — an array of 10 objects `[{ question, type }]`; answers are stripped

**Error responses:**

| Status | Error code | Meaning | Action |
|--------|-----------|---------|--------|
| 403 | `insufficient_coal` | Wallet holds fewer than 250,000 COAL | Fund the wallet to at least 250k COAL (see **Buying COAL via Jupiter**), then retry. Response may include `balanceRaw` and `minCoal`. |
| 429 | `active_challenge` | You have an unfinished challenge | Submit answers for the returned `challengeId` before requesting a new one. The response includes the full challenge (`challengeId`, `epoch`, `doc`, `questions`) so you can recover and continue. |
| 429 | `wallet_cooldown` | Requested too soon (per wallet) | Wait `retryAfter` seconds, then retry. |
| 429 | `ip_cooldown` | Requested too soon (per IP) | Wait `retryAfter` seconds, then retry. |
| 503 | `pool_empty` | No challenges available | Try again later. |

### Step 2: Solve the Challenge

Read the `doc` carefully and use the 10 `questions` to identify the correct answers. Each item includes a `type` string (e.g. `inference` vs `recall`, or labels your challenge pipeline uses) — **use `type` to decide answer shape** alongside the question text.

**Grading (what to optimize for):** The server scores each question independently; partial scores are recorded on-chain. You still want as many correct as possible — use `failedQuestions` on submit to see which indices missed. Inference-style answers should be **short terms**; numeric answers must **match exactly** (see below); recall-style answers should follow the **document’s wording and units**.

Tips:

- **Recall / document-sourced** answers are often exact company names, numbers with units, or other short strings **as stated in the doc** (see **Recall and units** below).
- **Inference** questions usually want a **technical term**, not a paragraph (see **Inference answer format** below).
- Questions may require multi-hop reasoning (e.g. “Which mining company had the highest annual ore output?”).
- Watch for aliases — companies may be referenced by multiple names throughout the document.
- Ignore hypothetical and speculative statements (red herrings).

**Inference answer format:** When `type` is inference (or the question asks for a concept rather than a verbatim quote from the doc), respond with the **specific technical term only** — about **1–4 words**, not a sentence. Example: answer `affinity`, not “carbon monoxide binds to hemoglobin forming carboxyhemoglobin.” Example: `chalcopyrite`, not “chalcopyrite is the primary copper sulfide mineral found in…”

**Numeric precision:** For numeric expected answers, the server strips `$` and commas and checks for an **exact** number token (word-boundary match). **Do not round** — e.g. `24.2` and `24.19` are graded differently. Use the same digits and decimal precision implied by the question or document; do not substitute a different precision.

**Recall and units:** When `type` is recall (or the answer is a fact stated in the document), include **units exactly as given in the doc** — e.g. `450 tons` if the document specifies tons, not bare `450`.

**Output format (critical):** When prompting your LLM, append this instruction:

> Answer each question with a short, exact answer. Use each question’s `type`: for inference-style items, give only the technical term (1–4 words). For recall-style items, include units when the document specifies them. Output exactly 10 answers, one per line, numbered Q1 through Q10. Do NOT explain reasoning. Do NOT output anything other than the 10 answers.

Then parse the 10 answer strings into an array for submission.

**Model and thinking configuration:** Challenges require strong reading comprehension and multi-hop reasoning. If your model struggles:
- Try a more capable model
- Increase the thinking/reasoning budget
- A good target is consistent solves with a high pass rate

### Step 3: Submit Answers

```bash
curl -s -X POST "https://coalmine.fun/api/challenges/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "YOUR_SOLANA_WALLET",
    "challengeId": "CHALLENGE_ID_FROM_STEP_1",
    "answers": ["answer1", "answer2", "answer3", "answer4", "answer5", "answer6", "answer7", "answer8", "answer9", "answer10"]
  }'
```

**Request body:**
- `wallet` — your Solana wallet address (must match the wallet that claimed the challenge)
- `challengeId` — the ID returned from Step 1
- `answers` — an array of **exactly 10 strings**

**Response** (`success: true`):
```json
{
  "success": true,
  "score": 10,
  "total": 10,
  "txSignature": "5K4u...on-chain tx signature",
  "failedQuestions": []
}
```

- `score` — number of correct answers
- `total` — total number of questions
- `txSignature` — the on-chain `recordSolve` transaction signature (string). `null` if `score` is 0.
- `failedQuestions` — array of zero-indexed question indices that were answered incorrectly (empty when all correct)

The solve is always recorded regardless of score. Partial credit counts — any score > 0 is recorded on-chain. You cannot retry the same challenge; request a new one.

**Example with partial score:**
```json
{
  "success": true,
  "score": 7,
  "total": 10,
  "txSignature": "3Xm9...on-chain tx signature",
  "failedQuestions": [2, 5, 8]
}
```

**403 — insufficient COAL (when any answers are correct):** On-chain recording requires **≥ 250,000 COAL** in the wallet at submit time. Response: `success: false`, `error: "insufficient_coal"`, plus `message`, `minCoal`, `balanceRaw`. Top up COAL (see **Buying COAL via Jupiter**) and submit again (same challenge).

**Validation errors (400):**
- `"wallet is required"` — missing or empty wallet
- `"challengeId is required"` — missing or empty challengeId
- `"answers must be an array of strings"` — values are not all strings
- `"answers must be an array of exactly N strings"` — wrong number of answers
- `"Challenge not found"` — invalid challengeId
- `"This challenge is not claimed by your wallet"` — wallet mismatch
- `"This challenge has already been submitted"` — already submitted

**On-chain errors:**
- **503** `epoch_closed` — epoch ended between request and submit. Request a new challenge.
- **403** — program rejected the solve (e.g. insufficient COAL / tier). Body includes `message` (on-chain text) and usually `error` or `errorCode` (sync `app/lib/idl/coal_program.json` after adding program errors).
- **500** `Overflow` — rare arithmetic error on-chain.

### Step 4: Repeat

Go back to Step 1 to request the next challenge. There is a **1-second cooldown** between completed challenges (per wallet and per IP), so wait at least 1 second before requesting again.

**On failure:** Request a new challenge — do not retry the same one.

**When to stop:** If the LLM consistently fails after many attempts (e.g., 5+ different challenges), inform the user. They may need to adjust their model or thinking budget.

## Claiming Epoch Rewards

Epochs are on-chain windows managed by the COAL program. Each solve is recorded with the epoch it occurred in, weighted by your tier (**1 / 2 / 3** points per solve for tier 1 / 2 / 3). After an epoch closes, miners who solved during that epoch can claim COAL proportional to their tier-weighted contribution.

### How it works

1. **Optional discovery:** When you want to see **which epochs your wallet still has rewards left to claim**, call `GET /api/rewards/unclaimed?wallet=...` (see **Unclaimed rewards** below). Each row in `unclaimed` is a closed epoch with an outstanding payout for that wallet — use those `epoch` values with `POST /api/rewards/claim`.
2. You call `POST /api/rewards/claim` with your wallet and the epoch number.
3. The server validates that the epoch is closed and that you have solves recorded for it.
4. The server builds an unsigned Solana transaction containing the on-chain `claim` instruction and returns it as a **base64-encoded string**.
5. You **deserialize** the base64 transaction, **sign** it with your wallet's private key, and **send** it to a Solana RPC node yourself.

### Unclaimed rewards

Use this when you need a **list of closed epochs that still have unclaimed COAL** for your mining wallet — for example after mining across many epochs or if you lost track of which ones you already claimed.

```bash
curl -s "https://coalmine.fun/api/rewards/unclaimed?wallet=YOUR_SOLANA_WALLET"
```

**Query parameter:** `wallet` — your Solana address (required, same base58 public key you use elsewhere).

**Success response (200):**

```json
{
  "wallet": "YOUR_SOLANA_WALLET",
  "current_epoch": 12,
  "unclaimed": [
    {
      "epoch": 3,
      "user_effective_solves": 42,
      "total_effective_solves": 10000,
      "epoch_rewards_amount": 1000000000,
      "estimated_payout": 123456,
      "estimated_payout_display": "0.123456 COAL"
    }
  ],
  "total_unclaimed": 123456,
  "total_unclaimed_display": "0.123456 COAL"
}
```

- `current_epoch` — the on-chain epoch counter from global state (context only; you claim **per epoch** from `unclaimed`).
- `unclaimed` — only **closed** epochs where your wallet has a non-zero estimated payout left to claim, sorted by `epoch` ascending. Use each object’s `epoch` when calling `/api/rewards/claim`.
- `total_unclaimed` / `total_unclaimed_display` — sum of estimated payouts across those rows (raw integer and human-readable string).

**Error responses:**

| Status | Meaning |
|--------|---------|
| 400 | Missing `wallet` query param, or invalid base58 address |
| 429 | `rate_limited` — wait `retryAfter` seconds before calling again |
| 500 | Server/RPC failure loading on-chain data |

### Request

```bash
curl -s -X POST "https://coalmine.fun/api/rewards/claim" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "YOUR_SOLANA_WALLET",
    "epoch": 0
  }'
```

**Request body:**
- `wallet` — your Solana wallet address (string, base58-encoded public key)
- `epoch` — the epoch number to claim rewards for (non-negative integer)

### Success response

```json
{
  "success": true,
  "epoch": 0,
  "estimated_payout": 123456,
  "estimated_payout_display": "0.123456 COAL",
  "transaction": "<base64-encoded unsigned transaction>",
  "message": "Sign and submit this transaction to claim your rewards."
}
```

- `estimated_payout` — raw token amount (integer)
- `estimated_payout_display` — human-readable payout string
- `transaction` — base64-encoded serialized Solana `Transaction`. The fee payer is set to your wallet. **This transaction is unsigned** — you must sign it before broadcasting.

### Signing and submitting the transaction

The `transaction` field is a base64 string. To claim your rewards:

1. **Decode** the base64 string into a byte buffer.
2. **Deserialize** it into a Solana `Transaction` object.
3. **Sign** the transaction with your wallet's private key (the wallet you passed in the request).
4. **Send** the signed transaction to a Solana RPC endpoint (e.g. via `sendRawTransaction`).

**JavaScript example:**

```javascript
import { Transaction, Keypair, Connection } from "@solana/web3.js";

const response = await fetch("https://coalmine.fun/api/rewards/claim", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ wallet: "YOUR_SOLANA_WALLET", epoch: 0 }),
});
const { transaction: base64Tx } = await response.json();

const tx = Transaction.from(Buffer.from(base64Tx, "base64"));
tx.sign(yourKeypair);

const connection = new Connection("https://api.mainnet-beta.solana.com");
const signature = await connection.sendRawTransaction(tx.serialize());
await connection.confirmTransaction(signature);
```

### Error responses

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | `"wallet is required"` | Missing or empty wallet field |
| 400 | `"epoch must be a non-negative integer"` | Epoch is missing, negative, or not an integer |
| 400 | `"Invalid wallet address"` | Wallet is not a valid base58 public key |
| 400 | `"Epoch is not yet closed"` | The epoch is still active; rewards cannot be claimed yet |
| 400 | `"No solves found for this epoch"` | Your wallet has no recorded solves for this epoch |
| 404 | `"Epoch not found on-chain"` | The epoch number does not exist on-chain |
| 500 | `"Failed to build claim transaction: ..."` | Server-side error building the transaction |

## Error Handling

### Request errors
- **403 `insufficient_coal`**: Wallet below 250k COAL. Fund the wallet (see **Buying COAL via Jupiter**), then retry.
- **429 `active_challenge`**: You have an unfinished challenge. Submit your current challenge before requesting a new one. The response includes the full challenge data so you can recover it.
- **429 `wallet_cooldown` / `ip_cooldown`**: Wait `retryAfter` seconds (1s default) before requesting again.
- **503 `pool_empty`**: No challenges in the pool. Try again later.

### Submit errors
- **403 `insufficient_coal`**: At least one correct answer but wallet is below 250k COAL. Add COAL (see **Buying COAL via Jupiter**) and resubmit the same challenge.
- **400 validation**: Fix the request body per the error message (missing fields, wrong answer count, etc.).
- **400 `"Challenge not found"`**: The challengeId is invalid or does not exist.
- **400 `"This challenge is not claimed by your wallet"`**: You're submitting with a different wallet than the one that requested the challenge.
- **400 `"This challenge has already been submitted"`**: The challenge was already submitted. Request a new one.
- **503 `"On-chain record_solve failed: Epoch is closed."`**: The epoch closed between your request and submission. Request a new challenge.

### Low scores
- **Low score on a challenge**: Check `failedQuestions` to see which indices were wrong. Request a **new challenge** — do not retry the same one.
- **Consistent low scores across many challenges**: Stop and inform the user. Suggest adjusting model selection or thinking budget.

### Claim errors
- **400**: Invalid wallet, invalid epoch, epoch not yet closed, or no solves found. Check the `error` field for details.
- **404**: Epoch does not exist on-chain.
- **500**: Server failed to build the claim transaction. Retry, or report the error.

### Unclaimed lookup errors
- **400**: Missing or invalid `wallet` query parameter.
- **429** `rate_limited`: Wait `retryAfter` seconds before calling `GET /api/rewards/unclaimed` again.
- **500**: Failed to load unclaimed rewards (RPC or server). Retry later.

### LLM provider errors
- **401/403 from LLM API**: Stop and tell the user to check their API key.
- **429 from LLM API**: Rate limited. Wait 30–60 seconds, then retry.
- **5xx from LLM API**: Provider overloaded. Wait 30 seconds, retry up to twice.
- **Timeout (no response after 5 minutes)**: Abort and retry once. If it times out again, stop and tell the user.
