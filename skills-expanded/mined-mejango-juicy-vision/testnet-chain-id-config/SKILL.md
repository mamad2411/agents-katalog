---
name: testnet-chain-id-config
description: |
  Fix for Relayr 502 errors or wrong chain IDs being sent despite VITE_TESTNET_MODE=true.
  Use when: (1) staging sends mainnet chain IDs (1, 10, 8453, 42161) instead of testnet,
  (2) Relayr staging API returns 502 Bad Gateway, (3) environment variable is set but
  code uses wrong chains. Root cause is typically hardcoded chain IDs in constants.
author: Claude Code
version: 1.0.0
date: 2025-01-31
---

# Testnet Chain ID Configuration

## Problem
Staging environment sends mainnet chain IDs to APIs that only support testnet, causing
502 errors or unexpected behavior despite `VITE_TESTNET_MODE=true` being correctly set.

## Context / Trigger Conditions
- Relayr staging API returns 502 Bad Gateway
- Network payload shows `chain: 1` (mainnet) instead of `chain: 11155111` (Sepolia)
- `VITE_TESTNET_MODE=true` is confirmed set in Railway/build environment
- Testnet explorers, RPCs, and other chain-specific features work correctly

## Root Cause
The `ALL_CHAIN_IDS` and `CHAINS` constants in `src/constants/index.ts` were hardcoded
to mainnet values, not using the environment-aware `SUPPORTED_CHAIN_IDS` from
`src/config/environment.ts`.

## Solution

1. Check `src/constants/index.ts` for hardcoded chain ID arrays:
   ```typescript
   // BAD - hardcoded
   export const ALL_CHAIN_IDS = [1, 10, 8453, 42161] as const

   // GOOD - environment-aware
   import { SUPPORTED_CHAIN_IDS } from '../config/environment'
   export const ALL_CHAIN_IDS = SUPPORTED_CHAIN_IDS
   ```

2. Ensure `CHAINS` object uses `CHAIN_IDS` from environment config as keys, not literals

3. Verify components use `ALL_CHAIN_IDS` from constants, not hardcoded arrays

## Key Files
- `src/config/environment.ts` - Source of truth for `IS_TESTNET`, `CHAIN_IDS`, `SUPPORTED_CHAIN_IDS`
- `src/constants/index.ts` - Must import and re-export environment-aware values
- `src/constants/chains.ts` - Contract addresses (already environment-aware)

## Chain ID Mapping
| Network   | Mainnet | Testnet (Sepolia) |
|-----------|---------|-------------------|
| Ethereum  | 1       | 11155111          |
| Optimism  | 10      | 11155420          |
| Base      | 8453    | 84532             |
| Arbitrum  | 42161   | 421614            |

## Verification
1. Build staging: `npm run build:staging`
2. Check network payload in browser devtools when creating a bundle
3. Confirm chain IDs are Sepolia variants (11155111, etc.)

## Notes
- Railway has `VITE_TESTNET_MODE=true` set as a service variable
- `.env.staging` is gitignored; Railway uses dashboard env vars
- Vite requires `VITE_*` variables at BUILD time, not just runtime
