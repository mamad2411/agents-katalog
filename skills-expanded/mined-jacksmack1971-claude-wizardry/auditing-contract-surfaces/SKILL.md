---
name: auditing-contract-surfaces
description: Audit contract-facing surfaces in an Ethereum TypeScript repo, including ABI drift, address management, generated artifacts, read versus write boundaries, and revert-path coverage. Use when reviewing ABI changes, contract interaction layers, generated types, contract address sources, write-path behavior, or revert and error handling.
argument-hint: "[target-path-or-contract-area]"
disable-model-invocation: false
user-invocable: true
---

# Auditing Contract Surfaces

Audit the contract interaction surface with explicit attention to public interface stability and write-path risk.

Inspect:

- ABI source-of-truth and generated artifact drift
- contract address storage and environment scoping
- separation between read paths and write paths
- revert-path handling and decoded error behavior
- generated client or type drift
- hand-edited generated artifacts

Use `references/contract-surface-checklist.md` during the pass.

Output contract:

- Contract surface audited
- Evidence files
- Interface or write-path risks
- Verification gap
- Recommended next skill
