---
name: ctf-blockchain
description: Use when a CTF challenge centers on blockchain or smart-contract logic rather than a conventional web or crypto-only path. Best for Ethereum or EVM-style tasks involving Solidity or Vyper source, ABI files, bytecode, deployed contract addresses, RPC endpoints, wallet keys, transaction traces, storage slots, proxies, delegatecall, reentrancy, signature misuse, chain-state manipulation, or scripted on-chain interaction inside a controlled CTF environment.
---

# CTF Blockchain

## Overview

Treat blockchain problems as state-machine exploits, not just code review. Reconstruct the execution environment, identify the privileged transition or broken invariant, prove it with the smallest safe on-chain or simulated action, then script the full solve path reproducibly.

## Use This Skill For

- Challenge text includes RPC URLs, contract addresses, private keys, ABI files, Solidity or Vyper source, bytecode, or transaction hashes.
- The hard part is reasoning about `msg.sender`, storage, balances, approvals, delegatecall context, proxy layouts, signatures, or chain-state transitions.
- The user needs a solve script, exploit transaction sequence, forked-chain validation, or contract-behavior triage.
- The task looks like Ethernaut, Damn Vulnerable DeFi, Paradigm-style puzzles, or bytecode-only EVM reversing.

## Workflow

1. Normalize the target.
   Capture the RPC endpoint, chain ID, player key or wallet, contract addresses, ABI or source availability, required win condition, and whether a local fork or simulator is already available.
   Read any existing `steps.md` before new probing so the current session inherits prior state reads, successful calls, failed exploit attempts, deployed helper contracts, and the last recommended next step.
2. Fingerprint the execution model.
   Identify compiler version, proxy pattern, privilege model, token standards, constructor or initializer flow, external dependencies, and whether the challenge depends on mempool timing, oracle state, flash liquidity, or off-chain signatures.
3. Map the critical state.
   Enumerate storage slots, balances, allowances, ownership, role gates, upgradeability hooks, pool accounting, and invariants that should hold before and after each transaction.
4. Pick one exploit family.
   Reentrancy, access control, storage collision, delegatecall context, signature replay, permit misuse, arithmetic or accounting bugs, oracle manipulation, unsafe upgrade paths, CREATE or CREATE2 abuse, price-share dilution, or callback misuse should each get a minimal proof first.
5. Verify with the lightest proof.
   Prefer `eth_call`, storage reads, forked-chain simulation, or one bounded transaction before a full exploit sequence. Prove the privileged state transition or invariant break with one decisive observation.
6. Script the solve path.
   Keep the exact calldata, transaction order, account assumptions, and expected post-state explicit. If helper contracts are required, keep their source and deployment steps next to the final solve script.
7. Clean the scratch space after the path is proven.
   Put RPC dumps, transaction traces, temporary bytecode decodes, fork-state notes, and trial payloads under `_artifacts/`. Keep final `solve*`, helper contract source, decisive traces, `steps.md`, and `wp.md` at the challenge root.

## Guardrails

- Work only on authorized CTF, lab, or training chains and RPC endpoints.
- Prefer read-only inspection or forked validation before sending state-changing transactions.
- Keep track of chain assumptions explicitly: block height, account balances, nonce expectations, and any required sequencing.
- If the challenge includes a dapp frontend or backend API, inspect that surface early rather than treating it as a pure on-chain problem.
- If source is missing and the bytecode path dominates, use reverse-style reasoning on dispatch logic, selectors, storage, and embedded constants before guessing blindly.
- Keep final exploit scripts and decisive traces, but prune disposable `_artifacts/` files after the solve is stable.
- Treat `steps.md` as a multi-session handoff log. Append state discoveries, helper-contract deployments, owned accounts, and next-step claims so another session can resume without replaying the chain from scratch.

## Reference Routing

- For blockchain triage, exploit families, and proof discipline, read [references/workflow.md](references/workflow.md).
- If the challenge includes a dapp or exposed API, pair with `$ctf-web` once the off-chain surface matters.
- If the task is bytecode-only or relies on unusual dispatch or initcode behavior, pair with `$ctf-reverse`.
- If the core break is signature math, finite-field recovery, or algebra around nonce generation, pair with `$ctf-crypto` and `ctf-sage`.
- If Linux-side Solidity, Foundry, or scripting workflow is needed, run it directly in the native Linux shell.

## Output Expectations

- Report the execution model, the suspected exploit family, the minimal proof, and the scripted transaction path.
- If a fork, helper contract, local node, or replay environment was started, note whether it was released before wrap-up.
- Before pausing or ending, add a short `steps.md` handoff covering current chain state assumptions, deployed helper addresses if any, proven transitions, and the next recommended action.
