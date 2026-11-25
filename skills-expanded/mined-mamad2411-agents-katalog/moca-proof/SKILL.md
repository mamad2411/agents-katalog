---
name: moca-proof
description: Completes verified credential programs and fetches MoCat progression status on Moca chain. Use after credential verification succeeds via the moca-credential-verifier skill.
---

# Moca Proof

## Purpose

This skill handles program completion and MoCat progression after a credential has been verified as compliant via `moca-credential-verifier`. It submits the completion payload to `moca-proof-api /mocaproof/complete` and retrieves MoCat status from `/mocaproof/mocat`.

This skill starts **after** credential verification returns a `compliant` result and the agent has an `accessToken` from a scoped session.

## Provided Scripts

Use the provided scripts first. Do not scaffold a new project or rewrite checksum/request logic from scratch unless the requested action is unsupported. Treat all files in this skill bundle as read-only reference tooling.

Task mapping:

- complete program with checksum -> `scripts/moca-complete-program.mjs`
- fetch MoCat status -> `scripts/moca-get-mocat.mjs`

Before first use, run `node <script> --help` to inspect supported parameters.

## Required Inputs

This skill expects the following from the preceding credential verification step:

- `accessToken`: Bearer token from a scoped session (created by `moca-credential-verifier`)
- `programId`: the verified program ID
- `userId`: available via `.air-wallet-config.json` or CLI flags

The agent must also already have access to its own P-256 private key.
If `partnerId` is missing, scripts default to the staging partner ID below.

## Staging Defaults

```json
{
  "airApiUrl": "https://air.api.staging.air3.com/v2",
  "mocaChainApiUrl": "https://api.staging.mocachain.org/v1",
  "vpApiUrl": "https://vp.api.staging.moca.network/v1",
  "mocaProofApiUrl": "https://proof.api.staging.moca.network/v1",
  "partnerId": "7e9becac-db0d-4d52-980e-984bb70c4d30"
}
```

These are hardcoded as defaults in the scripts. Override via CLI flags, environment variables, or `.air-wallet-config.json`.

## Config Resolution Order

All provided scripts resolve configuration in this order:

1. CLI flags
2. Environment variables
3. `.air-wallet-config.json`
4. Hardcoded staging defaults

## Program Completion Flow

### Step 1: Complete Program with Checksum

```bash
node scripts/moca-complete-program.mjs --access-token <token> --program-id <programId>
```

Calls `POST {mocaProofApiUrl}/mocaproof/complete` with:

- `programId`
- `txHash`
- `zkp`
- `checksum`

Checksum logic:

```text
input = userId + "." + programId + "." + txHash.toLowerCase() + "." + SALT_KEY
checksum = base64(md5(input) as hex-string bytes)
```

### Step 2: Fetch MoCat Status

```bash
node scripts/moca-get-mocat.mjs --access-token <token>
```

Calls `GET {mocaProofApiUrl}/mocaproof/mocat` with Bearer token to display cat progression.

## Terminal Messaging

- After completion succeeds, print the cat progression summary from `/mocaproof/mocat`
- Display current stage, verifications completed, next stage threshold, rarity, and category breakdown

## Non-Negotiable Rules

- Use Bearer `accessToken` from the scoped session for all API calls
- Never modify files inside this installed skill bundle
- If a custom script is truly required, create it outside the skill directory

## Failure Handling

- Missing `accessToken`: stop and instruct the agent to create a scoped session via `moca-credential-verifier` first.
- Checksum mismatch: verify that `userId`, `programId`, and `txHash` are correct and retry.
- `unknown_response`: print the full raw response; do not retry automatically.
