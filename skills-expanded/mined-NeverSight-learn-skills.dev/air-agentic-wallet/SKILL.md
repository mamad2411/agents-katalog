---
name: air-agentic-wallet
description: Operates AIR agentic wallets through AIR's `/v2/wallet/agent-sign` HTTP endpoint and ERC-4337 UserOps. Use when an external agent receives an AIR handoff bundle with `userId`, `walletId`, `privyAppId`, `abstractAccountAddress`, and `airApiAgentSignUrl`, and needs to sign messages, typed data, or control the smart account onchain.
---

# AIR Agentic Wallet

## Purpose

This skill teaches an external agent how to authenticate to AIR with a fresh `signedMessage`, request wallet signatures from `POST /v2/wallet/agent-sign`, and control the user's AIR smart account onchain for common wallet, token, and NFT actions.

This skill starts **after** the agent key already exists.

## Provided scripts

Use the provided scripts first. Do not scaffold a new project or rewrite AIR signing logic from scratch unless the requested action is unsupported.
Treat all files in this skill bundle as read-only reference tooling.

## Default Execution Policy

Regardless of model capability, prioritize the provided scripts first and only write custom code when the requested action is unsupported.

Task mapping:

- plain message signing -> `scripts/air-personal-sign.mjs`
- typed data signing -> `scripts/air-sign-typed-data.mjs`
- read native, ERC-20, ERC-721, or ERC-1155 balances -> `scripts/air-balance.mjs`
- native token or ERC-20 transfer -> `scripts/air-send.mjs`
- approve ERC-20, ERC-721, or ERC-1155 spend/operator access -> `scripts/air-approve.mjs`
- transfer ERC-721 or ERC-1155 NFTs -> `scripts/air-nft-transfer.mjs`
- arbitrary contract execution -> `scripts/air-execute.mjs`

If a task is supported by one of these scripts, do not create a replacement script.

- `scripts/air-personal-sign.mjs`: sign plain text or hex with AIR
- `scripts/air-sign-typed-data.mjs`: sign EIP-712 typed data with AIR
- `scripts/air-balance.mjs`: read native, ERC-20, ERC-404-compatible, ERC-721, or ERC-1155 balances
- `scripts/air-send.mjs`: send native tokens or ERC-20 with AIR
- `scripts/air-approve.mjs`: prepare or submit ERC-20, ERC-404-compatible, ERC-721, or ERC-1155 approvals
- `scripts/air-nft-transfer.mjs`: prepare or submit ERC-721 or ERC-1155 transfers
- `scripts/air-execute.mjs`: submit arbitrary contract calls through the AIR smart account
- `scripts/air-common.mjs`: shared helper module used by the scripts

Before first use, run `node <script> --help` to inspect the supported parameters.

Examples:

```bash
node scripts/air-personal-sign.mjs --message "Hello from AIR"
node scripts/air-sign-typed-data.mjs --typed-data-file typed-data.json
node scripts/air-balance.mjs --asset USDC --chain-id 84532
node scripts/air-send.mjs --recipient 0xabc... --amount 0.001 --send --wait
node scripts/air-send.mjs --recipient 0xabc... --amount 0.1 --asset USDC --chain-id 84532 --send --wait
node scripts/air-approve.mjs --spender 0xabc... --amount 100 --asset USDC --chain-id 84532 --send --wait
node scripts/air-nft-transfer.mjs --standard erc721 --token-address 0xCollection... --recipient 0xabc... --token-id 1 --send --wait
node scripts/air-send.mjs --recipient 0xabc... --amount 10 --token-address 0xToken... --send --wait
node scripts/air-send.mjs --recipient 0xabc... --amount 10 --token-address 0xToken... --pre-verification-gas 0x400000 --send --wait
node scripts/air-execute.mjs --target 0xContract... --data 0xabcdef --value 0 --send --wait
```

For ERC404, only use the helper scripts when the contract is ERC20-compatible for the requested action. Otherwise use `air-execute.mjs`.

## Required Inputs

Expect a handoff bundle equivalent to:

```json
{
  "userId": "...",
  "walletId": "...",
  "privyAppId": "...",
  "abstractAccountAddress": "0x...",
  "airApiAgentSignUrl": "https://.../v2/wallet/agent-sign",
  "AgenticWalletSkillUrl": "https://..."
}
```

The agent must also already have access to its own P-256 private key.

## Project-level defaults

It is allowed to create or update a project-level `.air-wallet-config.json` file in the working directory. Use that file for defaults such as the AIR handoff bundle, RPC, bundler, paymaster, and key paths. Do not store those defaults by editing files inside this skill bundle.

Example:

```json
{
  "userId": "...",
  "walletId": "...",
  "privyAppId": "...",
  "abstractAccountAddress": "0x...",
  "airApiAgentSignUrl": "https://.../v2/wallet/agent-sign",
  "AgenticWalletSkillUrl": "https://...",
  "rpcUrl": "https://sepolia.base.org",
  "bundlerUrl": "https://api.candide.dev/public/v3/base-sepolia",
  "paymasterUrl": null,
  "privateKeyPath": "./p256-private-key.pem",
  "publicKeyPath": "./p256-public-key.pem"
}
```

All provided scripts resolve configuration in this order:

1. CLI flags
2. environment variables
3. `.air-wallet-config.json`

Minimum runtime inputs:

- `userId`
- `walletId`
- `privyAppId`
- `abstractAccountAddress`
- `airApiAgentSignUrl` as a full endpoint URL
- agent private key

Optional runtime inputs:

- `bundlerUrl`
- `paymasterUrl`
- target chain RPC

## Hardcoded AIR Assumptions

Use these AIR implementation details exactly unless AIR changes them:

```json
{
  "entryPointVersion": "0.7",
  "entryPointAddress": "0x0000000071727De22E5E9d8BAf0edAc6f37da032",
  "knownK1Validators": [
    "0x0000002D6DB27c52E3C11c1Cf24072004AC75cBa"
  ],
  "baseSepolia": {
    "chainId": 84532
  }
}
```

Assume the same `abstractAccountAddress` is used across chains.

## Non-Negotiable Rules

- Always call AIR's backend endpoint in `airApiAgentSignUrl`.
- Never call Privy directly for wallet signing.
- Never modify files inside this installed skill bundle.
- It is acceptable to create or update `.air-wallet-config.json` in the project root for default values.
- If a custom script is truly required, create it outside the skill directory.
- Generate a **fresh** `signedMessage` for every request.
- Never reuse an old `signedMessage`.
- Treat `signedMessage` and `agentSignature` as two different signatures with two different purposes.
- Discover a bundler URL yourself when you need onchain execution.
- If a paymaster URL is provided, use paymaster-sponsored UserOps.
- If no paymaster URL is provided, use self-funded mode.

## Signature Model

Every `POST /v2/wallet/agent-sign` request contains two signatures:

1. `signedMessage`: proves agent identity to AIR
2. `agentSignature`: authorizes the exact wallet signing payload AIR will send to Privy

If either one is wrong, the request fails.

## `signedMessage`

Format:

```text
agent_pubkey:userId:unixEpochTime
```

`agent_pubkey` must be the exact registered public key string, typically PEM. Sign the raw message bytes with the agent's P-256 private key using SHA-256, then send:

```json
{
  "message": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----:086c40cb-dd8d-4416-9ce8-b0a7789542f3:1773635693",
  "signature": "base64-encoded ES256 signature",
  "publicKey": "the registered public key string"
}
```

## `agentSignature`

`agentSignature` is a base64-encoded P-256 signature over this canonical Privy request payload:

```json
{
  "version": 1,
  "method": "POST",
  "url": "https://api.privy.io/v1/wallets/{walletId}/rpc",
  "body": {
    "method": "...",
    "params": {}
  },
  "headers": {
    "privy-app-id": "<privyAppId-from-handoff-bundle>"
  }
}
```

Rules:

- sort object keys lexicographically at every level
- keep array order unchanged
- sign the canonical JSON bytes with the same agent P-256 private key
- return the signature as base64

## Privy RPC Body Mapping

For `personal_sign`, transform:

```json
{
  "method": "personal_sign",
  "payload": "0x48656c6c6f"
}
```

into:

```json
{
  "method": "personal_sign",
  "params": {
    "message": "48656c6c6f",
    "encoding": "hex"
  }
}
```

For `eth_signTypedData_v4`, transform:

```json
{
  "method": "eth_signTypedData_v4",
  "payload": {
    "domain": {},
    "primaryType": "MyType",
    "types": {},
    "message": {}
  }
}
```

into:

```json
{
  "method": "eth_signTypedData_v4",
  "params": {
    "typed_data": {
      "primary_type": "MyType",
      "domain": {},
      "types": {},
      "message": {}
    }
  }
}
```

## HTTP Request Contract

Call `airApiAgentSignUrl` directly with:

```json
{
  "signedMessage": {
    "message": "agent_pubkey:userId:unixEpochTime",
    "signature": "base64-encoded ES256 signature over message",
    "publicKey": "registered public key"
  },
  "method": "personal_sign",
  "payload": "0x48656c6c6f",
  "agentSignature": "base64-encoded ES256 signature over canonical Privy payload"
}
```

Typed data example:

```json
{
  "signedMessage": {
    "message": "agent_pubkey:userId:unixEpochTime",
    "signature": "base64-encoded ES256 signature over message",
    "publicKey": "registered public key"
  },
  "method": "eth_signTypedData_v4",
  "payload": {
    "domain": {
      "name": "MyApp",
      "version": "1",
      "chainId": 84532
    },
    "primaryType": "Action",
    "types": {
      "EIP712Domain": [
        { "name": "name", "type": "string" },
        { "name": "version", "type": "string" },
        { "name": "chainId", "type": "uint256" }
      ],
      "Action": [
        { "name": "action", "type": "string" }
      ]
    },
    "message": {
      "action": "swap"
    }
  },
  "agentSignature": "base64-encoded ES256 signature over canonical Privy payload"
}
```

cURL shape:

```bash
curl -X POST "$AIR_API_AGENT_SIGN_URL" \
  -H "content-type: application/json" \
  --data '{
    "signedMessage": {
      "message": "...",
      "signature": "...",
      "publicKey": "..."
    },
    "method": "personal_sign",
    "payload": "0x48656c6c6f",
    "agentSignature": "..."
  }'
```

## HTTP Success Response Contract

```json
{
  "signature": "0x..."
}
```

The returned value is the final wallet signature from AIR's wallet backend.

## Off-Chain Workflow

For `personal_sign`, `eth_signTypedData_v4`, or a `userOpHash`: build a fresh `signedMessage`, build the canonical Privy payload, produce `agentSignature`, call `airApiAgentSignUrl`, then use the returned wallet signature.

## On-Chain Workflow

Use AIR only for the final wallet signature. Everything else is standard ERC-4337 flow.

### Step 1: Discover a bundler URL

Always try to discover a bundler URL yourself for the current chain.

Default public example for Base Sepolia:

```text
https://api.candide.dev/public/v3/base-sepolia
```

Candide-supported networks:

- Mainnet: Arbitrum One `42161`, Avalanche C-Chain `43114`, Base `8453`, BNB Smart Chain `56`, Celo `42220`, Ethereum `1`, Gnosis `100`, Optimism `10`, Polygon PoS `137`, Plasma `9745`, Worldchain `480`
- Testnet: Arbitrum Sepolia `421614`, Base Sepolia `84532`, Optimism Sepolia `11155420`, Polygon Amoy `80002`, Sepolia `11155111`, Celo Alfajores `44787`, BNB Smart Chain Testnet `97`

### Step 2: Optional paymaster

- If a paymaster URL is provided, build a paymaster-sponsored UserOp.
- If no paymaster URL is provided, build a self-funded UserOp.

### Common onchain actions

Prefer these scripts before writing any custom tooling:

- fungible balance checks: `air-balance.mjs`
- NFT ownership or token balance checks: `air-balance.mjs`
- ERC-20 approvals: `air-approve.mjs`
- ERC-721 approvals or operator approvals: `air-approve.mjs`
- ERC-1155 operator approvals: `air-approve.mjs`
- ERC-721 transfers: `air-nft-transfer.mjs`
- ERC-1155 transfers: `air-nft-transfer.mjs`
- unusual token or NFT methods, including custom ERC404 variants: `air-execute.mjs`

### Step 3: Minimal UserOp structure

Use EntryPoint v0.7 unpacked fields for this Candide path:

```json
{
  "sender": "0x...",
  "nonce": "0x...",
  "factory": null,
  "factoryData": null,
  "callData": "0x...",
  "callGasLimit": "0x...",
  "verificationGasLimit": "0x...",
  "preVerificationGas": "0x...",
  "maxFeePerGas": "0x...",
  "maxPriorityFeePerGas": "0x...",
  "paymaster": null,
  "paymasterVerificationGasLimit": null,
  "paymasterPostOpGasLimit": null,
  "paymasterData": null,
  "signature": "0x..."
}
```

Do not switch to legacy packed `initCode` / `paymasterAndData` for this flow.

### Step 4: Build arbitrary smart account calldata

Treat the AIR smart account as a generic programmable account. The same pattern applies to native transfers, ERC-20, ERC-721, ERC-1155, Uniswap, Aave, and arbitrary contract calls:

1. choose `target`
2. choose `value`
3. encode `data`
4. wrap it in the smart account execute call

Native transfer example:

```json
{
  "target": "0xRecipient",
  "value": "1000000000000000",
  "data": "0x"
}
```

ERC-20 transfer example:

```json
{
  "target": "0xToken",
  "value": "0",
  "data": "encoded transfer(address,uint256)"
}
```

### Step 5: Detect the installed validator

AIR currently uses Nexus-style validator-aware nonces.

Before fetching the nonce, check the smart account with:

```text
isModuleInstalled(uint256 moduleTypeId, address module, bytes additionalContext)
```

Use:

- `moduleTypeId = 1`
- `additionalContext = 0x`

Use the legacy Biconomy K1 Validator address from `knownK1Validators`.

### Step 6: Build the nonce key

Use the validator address value itself as the nonce key.

If the installed validator is:

```text
0x0000002D6DB27c52E3C11c1Cf24072004AC75cBa
```

then:

```text
nonceKey = BigInt("0x0000002D6DB27c52E3C11c1Cf24072004AC75cBa")
```

### Step 7: Fetch the nonce

Call EntryPoint v0.7:

```text
getNonce(address sender, uint192 key)
```

with:

- `sender = abstractAccountAddress`
- `key = nonceKey`

### Step 8: Estimate with a dummy signature

For simulation and gas estimation, use a dummy 65-byte signature:

```text
0x + "ff" repeated 65 times
```

AIR's current smart account stack requires a decodable signature during simulation.

Use this exact recipe:

1. build the UserOp with a dummy signature
2. estimate through the bundler
3. if paymaster is available, attach paymaster fields
4. recompute `userOpHash` using the final gas and paymaster fields
5. ask AIR to sign that final hash
6. replace the dummy signature with the returned wallet signature
7. submit

If estimation fails, a temporary one-file script is acceptable. Do not scaffold a whole project unless necessary.

### Step 9: Compute `userOpHash`

Compute the ERC-4337 `userOpHash` with:

- EntryPoint version `0.7`
- EntryPoint address `0x0000000071727De22E5E9d8BAf0edAc6f37da032`
- the final gas fields
- paymaster fields included if sponsored
- `signature = 0x` in the hash input

### Step 10: Ask AIR to sign the `userOpHash`

Call `airApiAgentSignUrl` with:

```json
{
  "signedMessage": {
    "message": "agent_pubkey:userId:unixEpochTime",
    "signature": "fresh base64 signature",
    "publicKey": "registered public key"
  },
  "method": "personal_sign",
  "payload": "0xUSER_OP_HASH",
  "agentSignature": "base64 signature over canonical Privy payload"
}
```

Use the returned wallet signature as `userOperation.signature`.

### Step 11: Submit

- Sponsored: submit through bundler after paymaster fields are attached
- Self-funded: estimate through bundler, keep account-funded gas fields, then submit

### Step 12: Common UserOp traps

- Use a fresh `signedMessage` every time you call AIR
- Build `agentSignature` only after canonicalizing the exact Privy payload
- Recompute `userOpHash` after final gas values are known
- Recompute `userOpHash` again if paymaster fields change
- Keep the dummy signature only for estimation; replace it before submission
- For Candide + EntryPoint v0.7, use unpacked v0.7 fields
- If the bundler says `preVerificationGas` is too low, first retry with the built-in padding. If needed, use `--pre-verification-gas` on `air-send.mjs`, `air-approve.mjs`, `air-nft-transfer.mjs`, or `air-execute.mjs`. Do not create a replacement skill script just for that.
- If the bundler says `Invalid UserOp signature`, assume the final hash was computed with stale gas or paymaster fields

## Base Sepolia Example Defaults

Use Base Sepolia as the default worked example:

```json
{
  "chainId": 84532,
  "bundlerUrl": "https://api.candide.dev/public/v3/base-sepolia",
  "entryPointVersion": "0.7",
  "entryPointAddress": "0x0000000071727De22E5E9d8BAf0edAc6f37da032"
}
```

Keep the overall flow chain-agnostic.

## Common Chain Assets

Prefer these chains by default unless the user says otherwise:

- Base Sepolia `84532`
- Base mainnet `8453`
- Ethereum mainnet `1`

Common assets:

```json
{
  "84532": {
    "name": "Base Sepolia",
    "assets": {
      "USDC": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "EURC": "0x808456652fdb597867f38412077A9182bf77359F"
    }
  },
  "8453": {
    "name": "Base",
    "assets": {
      "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "MOCA": "0x2b11834ed1feaed4b4b3a86a6f571315e25a884d"
    }
  },
  "1": {
    "name": "Ethereum",
    "assets": {
      "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "MOCA": "0xf944e35f95e819e752f3ccb5faf40957d311e8c5"
    }
  }
}
```

## Failure Handling

- Unknown public key: the key was removed, wrong, or never registered. Stop and ask for a new handoff bundle.
- Expired signed message: rebuild a fresh `signedMessage` and retry once.
- Message timestamp too far in the future: fix clock skew, rebuild the message, retry once.
- Invalid agent signature: rebuild the canonical payload exactly, verify `walletId`, verify `privy-app-id`, regenerate `agentSignature`, retry once.
- Too many requests: back off, retry later, avoid concurrent duplicate requests for the same key.

## Minimal Checklist

- [ ] Use the provided `walletId`
- [ ] Use the provided `userId`
- [ ] Use the registered public key exactly as stored
- [ ] Generate a fresh `signedMessage`
- [ ] Build the canonical Privy payload exactly
- [ ] Include `privy-app-id` from the provided AIR handoff bundle
- [ ] Send the request to `airApiAgentSignUrl`
- [ ] Never call Privy directly

