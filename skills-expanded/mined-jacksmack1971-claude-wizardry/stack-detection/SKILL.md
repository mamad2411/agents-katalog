---
name: stack-detection
description: Detect whether an Ethereum TypeScript repo is viem-first, ethers v6-first, or mixed before making architectural changes. Use before changing RPC clients, wallet flows, contract interaction layers, or shared web3 abstractions.
disable-model-invocation: false
user-invocable: true
---

# Stack Detection

Inspect:

- `package.json` dependencies and scripts
- shared client construction files
- wallet connector setup
- contract interaction callsites
- generated ABI and type locations

Classification:

- `viem-first`: shared use of `createPublicClient`, `createWalletClient`, typed contract clients, or `viem/chains`
- `ethers-v6-first`: shared use of `BrowserProvider`, `JsonRpcProvider`, `Contract`, and signer-centric flows
- `mixed`: both stacks present in meaningful runtime paths

Output:

- Chosen classification
- Evidence files
- Migration risk if the change crosses stack boundaries
- Recommended follow-on skill:
  - `auditing-wallet-flows` for wallet UX and signing paths
  - `auditing-contract-surfaces` for ABI and write-path inspection
  - `verifying-deployment-safety` for deployment and signer risk
