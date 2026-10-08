---
name: test-swap
version: "1.0.0"
author: "qa-team"
chains: [eip155:1, eip155:137]

description: |
  [Onchain OS dependency]
  This Skill requires Onchain OS for on-chain signing.

  [signing constraint]
  All pending_sign transactions returned by this Skill MUST be signed
  exclusively through Onchain OS tools. Local private keys, sendTransaction,
  ethers.Wallet, and any equivalent are forbidden.

  Test Swap DApp — scaffold smoke-test fixture.

requiredTools:
  - name: onchainos wallet contract-call
    provider: onchainos
    install: "npx skills add okx/onchainos-skills"
    reason: "receives calldata → TEE signing → broadcast"
  - name: onchainos gateway broadcast
    provider: onchainos
    install: "npx skills add okx/onchainos-skills"
    reason: "broadcasts signed transactions on-chain"

tools:
  - name: my_build_swap
    description: "Constructs the swap unsigned_tx and returns pending_sign"
---

## Pre-flight Checks
1. Verify `onchainos wallet contract-call` and `onchainos gateway broadcast` are available
2. If not installed, run: `npx skills add okx/onchainos-skills`
3. Confirm installation succeeded

## Signing Constraint
All `pending_sign` transactions must be signed only by the Onchain OS tool named in `next_action.tool`.
Local private keys, `signTransaction`, `ethers.Wallet`, and `sendTransaction` are forbidden in DApp code.
