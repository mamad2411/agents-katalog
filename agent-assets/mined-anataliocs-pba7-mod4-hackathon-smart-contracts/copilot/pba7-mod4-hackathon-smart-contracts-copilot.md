# Copilot Instructions: Hardhat and Solidity with Ethers Smart Contract Security Best Practices

Purpose: Use this file to guide AI assistants (e.g., GitHub Copilot / Chat) and contributors toward secure patterns when
writing, modifying, or reviewing smart contracts and related scripts in this repository.

If a suggestion conflicts with any rule below, prefer SECURITY to brevity or gas savings unless explicitly justified.

## How to use this document

- When generating code, explain security-relevant choices (1–2 sentences) and point to the rule(s) you followed.
- If a request could be unsafe (e.g., bypassing checks), ask a clarifying question before producing code.
- Prefer minimal, auditable changes; avoid cleverness that obscures logic.
- Provide tests that prove security properties (reentrancy, access control, failure modes) with each change.

## Global rules

1. Fixed compiler version
    - Use a fixed pragma consistent with the project (e.g., `pragma solidity 0.8.26;`). Avoid floating pragmas.
2. No unsafe assembly by default
    - Do not introduce `assembly` unless strictly necessary. If used, isolate and document invariants thoroughly.
3. Prefer audited libraries
    - Use OpenZeppelin or well-audited equivalents for ERC standards, access control, pausing, reentrancy guards, math,
      and upgradeability patterns.
4. Explicit error handling
    - Use custom errors or clear revert messages. Check return values of external calls.
5. Minimize trust & assumptions
    - Document trust boundaries, admin powers, and dependencies. Prefer timelocks, multisig, rate limits where
      applicable.

## Core Solidity patterns

- Checks-Effects-Interactions (CEI)
    - Validate inputs and permissions first, update internal state second, interact with external contracts last.
- Reentrancy
    - Guard external-facing state-changing functions with nonReentrant or pull-payment patterns. Avoid writing business
      logic after external calls. Emit events after state changes.
- Access control
    - Enforce role-based or ownership checks for privileged actions. Avoid `tx.origin`. Use Ownable/AccessControl.
      Consider timelocks for critical ops.
- Arithmetic
    - Use Solidity >=0.8.x checked math. Where rounding matters, document it. Avoid division before multiplication when
      precision is critical.
- External calls
    - Prefer using interfaces; avoid `address.call()` unless needed. Check success and returned data. Use try/catch for
      fallible calls.
- State initialization & invariants
    - Validate constructor/initializer arguments. For upgradable contracts, protect initializers and storage layout.
      Assert invariants with tests and comments.
- Events & observability
    - Emit events for all user-impacting state transitions (ownership changes, parameter updates, critical transfers).
      Index relevant topics.
- Pull over push
    - Prefer withdrawal patterns to avoid locking funds on failing receivers. Consider ERC-2771, ERC-777 hooks
      carefully.
- Front-running & MEV
    - Include slippage limits, deadlines, and commit-reveal where relevant. Avoid reliance on `block.timestamp` for
      randomness.

## Common vulnerability checklist

- [ ] Reentrancy (direct and cross-function)
- [ ] Missing access control / auth bypass
- [ ] Uninitialized state / default values
- [ ] Integer over/underflow assumptions (even with 0.8.x)
- [ ] Inadequate input validation / invariant checks
- [ ] Incorrect order of CEI steps
- [ ] Unchecked external call return values
- [ ] Delegatecall misuse / proxy storage collision
- [ ] Oracle manipulation / stale prices
- [ ] Flash-loan attack surfaces (e.g., price-dependent logic)
- [ ] DoS vectors (unbounded loops, griefable gas patterns)
- [ ] Signature replay / improper EIP-712 domain separation
- [ ] Timestamp/blockhash dependence for randomness
- [ ] Insecure upgrade paths / missing initializer guards
- [ ] Unsafe use of selfdestruct, `tx.origin`, `block.coinbase`

## Upgradability guidance (if used)

- Use OpenZeppelin Transparent/UUPS proxies.
- Lock implementation contracts after deployment; prevent direct initialization.
- Preserve storage layout. Document variable ordering, gaps, and reserved slots.
- Include upgrade authorization and, ideally, timelocks/multisig.

## Token standards and transfers

- ERC-20: Handle non-standard return values. Use safe wrappers. Beware of fee-on-transfer tokens.
- ERC-721/1155: Handle hooks safely; validate receiver contracts. Avoid reentrancy on callbacks.
- Approvals: Minimize approval scope; support permit (EIP-2612/EIP-712) securely.

## Testing requirements

- Write tests for:
    - Reentrancy attempts (including cross-function)
    - Access control (happy/deny paths)
    - Pausing/emergency flows
    - Edge cases: zero amounts, max values, duplicates
    - Failure modes for external calls
    - Invariant/fuzz tests for critical math or accounting
- Prefer Hardhat with Mocha/Chai; consider Foundry fuzzing as a complement. Keep tests deterministic.

## Tooling & verification

- Static analysis: Slither
- Symbolic/SMT: Mythril or MythX (if available)
- Fuzzing: Echidna or Foundry
- Gas/size: hardhat-gas-reporter (if configured)
- Linters: solhint/solium per project setup
- CI: run analyzers on PRs where possible; block on critical findings

## Polkadot / PolkaVM context

- External calls and cross-chain messaging may have different guarantees—validate assumptions about finality and message
  ordering.
- Be explicit about fee models and weight limits; avoid unbounded operations.
- For EVM-on-Polkadot environments (PolkaVM), apply the same Solidity rules plus chain-specific limits. Avoid relying on
  Ethereum-only precompiles unless confirmed available.

## Do / Don’t snippets

- Do: CEI with reentrancy guard

```solidity
pragma solidity 0.8.26;

import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract SafeVault is ReentrancyGuard {
    mapping(address => uint256) public balance;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    function deposit() external payable {
        require(msg.value > 0, "ZERO_AMOUNT");
        balance[msg.sender] += msg.value; // Effects
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external nonReentrant {
        require(amount > 0 && amount <= balance[msg.sender], "INVALID_AMOUNT");
        balance[msg.sender] -= amount; // Effects
        (bool ok,) = msg.sender.call{value: amount}(""); // Interaction
        require(ok, "TRANSFER_FAIL");
        emit Withdrawn(msg.sender, amount);
    }
}
```

- Don’t: External call before state update (reentrancy risk)

```solidity
pragma solidity 0.8.26;

contract AntiPattern {
    mapping(address => uint256) public balance;

    function withdraw(uint256 amount) external {
        require(amount > 0 && amount <= balance[msg.sender], "INVALID_AMOUNT");
        // Anti-pattern: interaction before effects
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok, "TRANSFER_FAIL");
        balance[msg.sender] -= amount; // too late — state updated after external call
    }
}
```

## Review prompts for AI assistants

When asked to write or modify contracts, consider asking:

- What are the trust assumptions and privileged roles?
- What invariants must hold before/after this function?
- Could an external call reenter or grief this flow?
- Are inputs validated and corner cases covered?
- Are events emitted for user-visible state changes?
- Do tests prove negative and edge cases?

## References

- OpenZeppelin Contracts: https://docs.openzeppelin.com/contracts
- SWC Registry (Smart Contract Weakness Classification): https://swcregistry.io/
- ConsenSys Best Practices: https://consensys.github.io/smart-contract-best-practices/
- Trail of Bits blog: https://blog.trailofbits.com/tag/smart-contracts/

## Repository links

- Contributing & Security Policy: docs/general/contributing.md
- License: ./LICENSE

---
Maintainers: Keep this file short, opinionated, and actionable. Update when toolchain or chain context changes.