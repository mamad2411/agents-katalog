---
name: moca-credential-verifier
description: Verifies user credentials on Moca chain testnet via AIR agent sessions. Use when a user wants to verify a credential, list available verification programs, check credential compliance, or see MoCat progression status.
---

# Moca Credential Verifier

## Purpose

This skill teaches an agent how to browse available verification programs, show numeric options, auto-try tiers from highest to lowest through `moca-chain-api` in **query_match mode**, submit completion to `moca-proof-api /mocaproof/complete`, and display MoCat progression.

This skill starts **after** the agent key already exists and the handoff bundle is available.

## Provided Scripts

Use the provided scripts first. Do not scaffold a new project or rewrite signing/request logic from scratch unless the requested action is unsupported. Treat all files in this skill bundle as read-only reference tooling.

Task mapping:

- create a scoped session -> `scripts/moca-create-session.mjs`
- list/browse verification programs -> `scripts/moca-list-programs.mjs`
- trigger credential verification (`query_match` mode) -> `scripts/moca-verify-by-agent.mjs`
- complete program with checksum -> `scripts/moca-complete-program.mjs`
- poll verification status -> `scripts/moca-poll-status.mjs`
- fetch MoCat status -> `scripts/moca-get-mocat.mjs`
- run the full end-to-end flow with automatic tier fallback -> `scripts/moca-verify-flow.mjs`

Before first use, run `node <script> --help` to inspect supported parameters.

## Required Inputs

Expect a handoff bundle equivalent to:

```json
{
  "userId": "...",
  "walletId": "...",
  "privyAppId": "...",
  "abstractAccountAddress": "0x...",
  "airApiAgentSignUrl": "https://.../v2/wallet/agent-sign",
  "partnerId": "7e9becac-db0d-4d52-980e-984bb70c4d30"
}
```

The agent must also already have access to its own P-256 private key.
If `partnerId` is missing, scripts default to the staging partner ID above.

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

## Project-Level Defaults

It is allowed to create or update a project-level `.air-wallet-config.json` file in the working directory. Use that file for defaults such as endpoint URLs, partner ID, and key paths. Do not store defaults by editing files inside this skill bundle.

Example additions for this skill:

```json
{
  "airApiUrl": "https://air.api.staging.air3.com/v2",
  "mocaChainApiUrl": "https://api.staging.mocachain.org/v1",
  "vpApiUrl": "https://vp.api.staging.moca.network/v1",
  "mocaProofApiUrl": "https://proof.api.staging.moca.network/v1",
  "partnerId": "7e9becac-db0d-4d52-980e-984bb70c4d30"
}
```

## Config Resolution Order

All provided scripts resolve configuration in this order:

1. CLI flags
2. Environment variables
3. `.air-wallet-config.json`
4. Hardcoded staging defaults

## Credential Verification Flow

### Step 1: Create a Scoped Session

```bash
node scripts/moca-create-session.mjs --program-id <programId>
```

Calls `POST {airApiUrl}/auth/agent/session` with:
- `signedMessage`: fresh agent-signed message
- `scope`: `"<programId>,<partnerId>"`

Returns an `accessToken` used as Bearer token for all subsequent calls.

### Step 2: List Verification Programs (No Token First)

```bash
node scripts/moca-list-programs.mjs
# optional personalized mode
node scripts/moca-list-programs.mjs --access-token <token>
```

Calls `GET {vpApiUrl}/vp/mocaproof/search?page=1&limit=20`.

- Without token: public listing mode
- With token: personalized listing mode (user verified metadata and filtering)

Results are paginated. The script shows a summary of the first page. Use `--page <n>` to fetch more.

The list output includes numeric options in this format:

- Option index: `[1]`, `[2]`, ...
- Tier index inside option: `(1.1)`, `(1.2)`, ...

### Step 3: Auto Tier Fallback Strategy

For one-shot end-to-end flow, run:

```bash
node scripts/moca-verify-flow.mjs
```

Behavior:

1. List options publicly first (no token)
2. For each option, try top tier first
3. If tier returns non-compliant/no-credential/other non-success bucket, try next tier
4. On first compliant tier:
   - create scoped session for that `programId`
   - call verify-by-agent (`query_match`)
   - call `/mocaproof/complete`
   - call `/mocaproof/mocat`
5. If all tiers across selected options fail, print `Sorry, not compliant`

Optional scoping:

- `--option-index <n>`: only try one listed option
- `--program-id <id>`: only try one exact program ID

### Step 4: Trigger Verification (query_match mode)

```bash
node scripts/moca-verify-by-agent.mjs --access-token <token> --program-id <programId>
```

Calls `POST {mocaChainApiUrl}/credentials/verify-by-agent` with:
- `programId` in the body
- `responseMode: "query_match"` in the body
- Bearer `accessToken` in the Authorization header

The response is normalized using the rules below.

### Step 5: Complete Program with Checksum

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

### Step 6: Fetch MoCat Status

```bash
node scripts/moca-get-mocat.mjs --access-token <token>
```

Calls `GET {mocaProofApiUrl}/mocaproof/mocat` with Bearer token to display cat progression.

### Optional: Poll VP Status

```bash
node scripts/moca-poll-status.mjs --access-token <token>
```

Use this when you want to inspect status progression separately from the default flow.

## Verify Response Normalization

The `verify-by-agent` endpoint returns inconsistent response shapes. Normalize exactly as:

- `verified: true` -> `compliant`
- `verified: false` + `reason: "NO_CREDENTIAL"` -> `no_vc`
- `verified: false` + `reason: "NOT_COMPLIANT"` -> `non_compliant`
- `verified: false` + `status: "NON_COMPLIANT"` -> `non_compliant`
- `verified: false` + `status` present -> `status_bucket:<status>`
- `verified: false` + only `code` present -> `unknown_failure_code:<code>`
- `verified: "pending"` -> `processing`
- Any other shape -> `unknown_response` (print raw payload)

Known `status` values:

- `NO_EXIST`: user has no credential for this program
- `WAIT_ONCHAIN`: credential is being published on-chain
- `EXPIRE`: credential has expired
- `WAIT_REMOVE`: credential is being revoked
- `REMOVE`: credential has been revoked
- `NON_COMPLIANT`: credential does not meet requirements

## Terminal Messaging

When running the full flow (`moca-verify-flow.mjs`):

- Print numeric options and tiers before verification attempts
- Print `Verifying....` on each tier attempt
- Auto-try next tier when a tier is non-compliant (or other non-success response bucket)
- If every attempted tier fails, print `Sorry, not compliant` and end
- When verify succeeds in query_match mode: print `OK, verified, <verifier name> is processing your data`
- Submit `/mocaproof/complete`, then print cat progression summary from `/mocaproof/mocat`

## Non-Negotiable Rules

- Always generate a **fresh** `signedMessage` for every session request
- Never reuse an old `signedMessage`
- Use Bearer `accessToken` from scoped session for all downstream API calls
- Never modify files inside this installed skill bundle
- If a custom script is truly required, create it outside the skill directory

## Failure Handling

- Unknown public key: the key was removed, wrong, or never registered. Stop and ask for a new handoff bundle.
- Expired signed message: rebuild a fresh `signedMessage` and retry once.
- `unknown_failure_code`: print the raw code and payload for debugging; do not retry automatically.
- `unknown_response`: print the full raw response; do not retry automatically.
