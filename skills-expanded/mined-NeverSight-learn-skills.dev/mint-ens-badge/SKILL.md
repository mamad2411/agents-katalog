---
name: mint-ens-badge
description: "Use this skill to mint an Agentic Wallet ENS Badge on X Layer. Triggers: 'mint ENS badge', 'get my agent identity', 'mint identity NFT', 'get badge number', 'ENS badge'. This skill calls a smart contract on X Layer (Chain ID 196) to mint a unique numbered identity badge NFT for your Agentic Wallet."
license: MIT
metadata:
  author: XlayerENS
  version: "1.0.0"
  homepage: "https://www.oklink.com/xlayer/address/0xa298bc6b64Be92038004cb8483068bF6e705E7A7"
---

# Mint ENS Badge for Your Agentic Wallet

Mint a unique, numbered identity NFT (ENS Badge) on X Layer (Chain ID 196). Each badge has a sequential number (#1, #2, #3...) as your agent identity credential. One badge per wallet. Cost: 0.1 OKB.

**Contract Address**: `0xa298bc6b64Be92038004cb8483068bF6e705E7A7`
**Chain**: X Layer (Chain ID `196`)

## Workflow

Follow these steps in order. This skill depends on **okx-agentic-wallet** — all wallet operations use the `onchainos` CLI.

### Step 1: Ensure Wallet Login

Check if the user is already logged into their Agentic Wallet:

```bash
onchainos wallet status
```

If `loggedIn` is `false`, guide the user through login:

1. Ask the user for their **email address**.
2. Send OTP:
   ```bash
   onchainos wallet login <email>
   ```
3. Tell the user a verification code has been sent to their email.
4. Wait for the user to provide the **6-digit code**.
5. Verify:
   ```bash
   onchainos wallet verify <otp>
   ```

### Step 2: Get Wallet Address and Check Balance

```bash
onchainos wallet balance --chain 196
```

From the response, note the user's `evmAddress`. Confirm they have at least **0.11 OKB** on X Layer (0.1 for mint + gas).

If balance is insufficient, tell the user they need to top up their X Layer wallet with OKB first.

### Step 3: Check If Already Has a Badge

Before minting, check if this wallet already owns a badge. Use the wallet's `evmAddress` from Step 2:

```bash
onchainos wallet contract-call \
  --to 0xa298bc6b64Be92038004cb8483068bF6e705E7A7 \
  --chain 196 \
  --input-data <calldata>
```

The calldata for `getBadgeInfo(address)` is: `0x693ec85e` + the wallet address padded to 32 bytes.

To construct the calldata: take the wallet's evmAddress, remove the `0x` prefix, left-pad to 64 hex chars with zeros, then prepend `0x693ec85e`.

Example for address `0x1234...abcd`:
```
0x693ec85e0000000000000000000000001234...abcd
```

If the result shows `hasBadge = true`, tell the user their badge number and stop. No need to mint.

### Step 4: Mint the Badge

Execute the mint transaction:

```bash
onchainos wallet contract-call \
  --to 0xa298bc6b64Be92038004cb8483068bF6e705E7A7 \
  --chain 196 \
  --value 0.1 \
  --input-data 0x1249c58b
```

- `--value 0.1` sends 0.1 OKB as the mint fee (in UI units, not wei).
- `--input-data 0x1249c58b` is the function selector for `mint()`.

Wait for the transaction hash in the response.

### Step 5: Confirm the Badge

After the transaction is confirmed, check the badge again using Step 3's method, or tell the user:

> "Congratulations! You've minted your Agentic Wallet ENS Badge. Your badge number will be assigned sequentially. You can now introduce yourself as ENS Badge #[number] on X Layer."

## After Minting

The user's agent can introduce itself as:

> "I am Agentic Wallet ENS Badge #[number] on X Layer."

## Verifying Other Agents

To check if another agent has a badge, use the same `getBadgeInfo` call from Step 3 with the other agent's address.

## Errors

| Error | Fix |
|---|---|
| `only smart contract wallets allowed` | The user is not using an Agentic Wallet. They must use `onchainos wallet` to transact. |
| `already minted` | This wallet already has a badge. Run Step 3 to find the badge number. |
| `insufficient payment` | The `--value` must be `0.1`. |
| Insufficient balance | User needs to add OKB to their X Layer wallet. |

## Contract ABI (Reference)

```json
[
  {"inputs":[],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},
  {"inputs":[{"name":"wallet","type":"address"}],"name":"getBadgeInfo","outputs":[{"name":"hasBadge","type":"bool"},{"name":"badgeNumber","type":"uint256"},{"name":"totalMinted","type":"uint256"}],"stateMutability":"view","type":"function"},
  {"inputs":[],"name":"totalMinted","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"},
  {"inputs":[],"name":"MINT_PRICE","outputs":[{"type":"uint256"}],"stateMutability":"view","type":"function"}
]
```
