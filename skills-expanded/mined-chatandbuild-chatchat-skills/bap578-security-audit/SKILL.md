---
id: bap578-security-audit
name: BAP-578 Security Audit
description: Use this skill when auditing, hardening, or verifying the security posture of BAP-578 Non-Fungible Agent deployments, including threat models, NFA-specific vulnerabilities, and remediation guidance.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Security Audit

Use this skill to audit, harden, and verify the security posture of BAP-578 Non-Fungible Agents deployments. This skill provides a structured threat model, detailed audit checklist, vulnerability patterns specific to the NFA architecture, and remediation guidance.

---

## When to use this skill

- Performing a security review before mainnet deployment.
- Investigating a suspected vulnerability or anomalous behavior.
- Reviewing access control patterns and ownership boundaries.
- Evaluating the safety of the UUPS upgrade mechanism.
- Assessing logic contract binding risks.
- Verifying fund management safety (deposits, withdrawals, treasury).
- Checking off-chain integrity mechanisms (vault hash verification).

---

## The Four Identity Questions (Security View)

### 1) Who are you?

The security layer validates trust boundaries and prevents loss. Security auditing for BAP-578 ensures that the contract's identity guarantees (ownership, metadata integrity, fund safety) cannot be subverted by attackers, malicious logic contracts, or administrative errors. The auditor's role is to verify that every claim the contract makes about identity, memory, capability, and trust is actually enforced.

### 2) What do you remember?

Security memory includes known attack patterns, prior audit findings, guard rails built into the contract, and the threat model specific to BAP-578's architecture. Key patterns to remember:

- ERC-721 + custom state = larger attack surface than plain NFTs
- UUPS proxy = upgrade risk if `_authorizeUpgrade` is not properly guarded
- Agent balance management = reentrancy risk on withdrawals
- Logic contract binding = external code execution risk
- Free mint mechanics = potential for abuse if not properly constrained

### 3) What can you do?

Run a structured security audit that produces:

- Threat model with categorized attack vectors
- Function-by-function access control review
- Reentrancy and CEI (Checks-Effects-Interactions) analysis
- Upgrade safety verification
- Fund flow analysis (deposits, withdrawals, treasury)
- Logic contract risk assessment
- Off-chain integrity verification review
- Severity-rated findings with remediation steps

### 4) How can I trust it?

Every finding maps to a specific function, modifier, or pattern in the contract source. Findings reference line numbers, function names, and concrete attack scenarios. Trust in the audit comes from:

- Reproducible analysis (anyone can verify each finding)
- Standard severity classification (Critical/High/Medium/Low/Informational)
- Concrete proof-of-concept descriptions for each finding
- Clear remediation steps

---

## Threat Model

### Attack surface overview

BAP-578 combines multiple patterns that each carry specific risks:

```
┌─────────────────────────────────────────┐
│              BAP-578 Contract            │
├──────────┬──────────┬───────────────────┤
│ ERC-721  │ UUPS     │ Custom State      │
│ Standard │ Proxy    │ (Agents, Funds)   │
├──────────┼──────────┼───────────────────┤
│ Transfer │ Upgrade  │ Mint (free/paid)  │
│ Approval │ Auth     │ Fund/Withdraw     │
│ Metadata │ Storage  │ Logic binding     │
│          │ Layout   │ Status toggle     │
│          │          │ Metadata update   │
└──────────┴──────────┴───────────────────┘
         ↓              ↓
    External actors:  Logic contracts
    (users, attackers) (external code)
```

### Categorized threat vectors

**T1: Reentrancy attacks**

Target: `withdrawFromAgent` and any function that sends BNB.

Attack scenario: A malicious contract calls `withdrawFromAgent`, and the fallback function re-enters the contract before state is updated. If the contract does not follow CEI pattern or use `nonReentrant`, the attacker can drain the agent's balance.

Verification steps:
1. Check that `withdrawFromAgent` uses the `nonReentrant` modifier.
2. Verify state is updated (balance decremented) before the external call.
3. Confirm `fundAgent` does not have re-entrancy paths.
4. Check that the treasury withdrawal (`emergencyWithdraw`) is also protected.

**T2: Access control bypass**

Target: Owner-only and token-owner-only functions.

Attack scenario: An attacker calls `setTreasury`, `setPaused`, `emergencyWithdraw`, or `grantAdditionalFreeMints` without being the contract owner. Or calls `withdrawFromAgent`, `setAgentStatus`, `setLogicAddress`, or `updateAgentMetadata` without being the token owner.

Verification steps:
1. List all functions with `onlyOwner` modifier.
2. List all functions with token-owner checks (e.g., `require(ownerOf(tokenId) == msg.sender)`).
3. Verify no function bypasses these checks.
4. Check that `transferOwnership` is properly restricted.

**T3: Malicious logic contract binding**

Target: `setLogicAddress` function.

Attack scenario: An attacker tricks a user into binding a malicious logic contract that steals funds or manipulates agent state. Or an attacker deploys a contract that appears safe but has a hidden backdoor.

Verification steps:
1. Confirm that only the token owner can set logic address.
2. Verify that EOAs (externally owned accounts) are rejected.
3. Check whether logic contracts can call back into the main contract.
4. Assess what permissions the logic contract has.

**T4: Free mint abuse**

Target: `createAgent` free mint logic.

Attack scenarios:
- Sybil attack: create many wallets to claim free mints at scale.
- Bypass self-mint restriction: find a way to mint free tokens to another address.
- Transfer restriction bypass: find a way to transfer free-minted tokens.

Verification steps:
1. Confirm free mints require `to == msg.sender`.
2. Verify transfer hook blocks transfers of free-minted tokens.
3. Check that `isFreeMint` mapping is correctly set at mint time.
4. Verify that `grantAdditionalFreeMints` is owner-only.

**T5: Upgrade safety**

Target: UUPS proxy mechanism.

Attack scenarios:
- Unauthorized upgrade: attacker calls `upgradeTo` or `upgradeToAndCall`.
- Storage collision: new implementation reorders or removes state variables.
- Initialization replay: attacker calls initializer on new implementation.

Verification steps:
1. Confirm `_authorizeUpgrade` is guarded by `onlyOwner`.
2. Verify implementation contract disables initializers in constructor.
3. Review storage layout for append-only discipline.
4. Check that `reinitializer` is used for new initialization logic.

**T6: Fund management risks**

Target: Agent balances, treasury, and BNB flows.

Attack scenarios:
- Drain agent balance via reentrancy (see T1).
- Treasury address set to attacker's address.
- Emergency withdraw drains all funds.

Verification steps:
1. Trace all BNB flows: where does `msg.value` go at mint time?
2. Verify mint fee calculation is correct.
3. Check that treasury address changes are owner-only.
4. Verify emergency withdraw sends funds to treasury, not caller.
5. Confirm agent withdrawal checks balance before sending.

**T7: Off-chain integrity**

Target: `vaultURI` and `vaultHash`.

Attack scenarios:
- Vault content modified after hash was recorded.
- Vault URI points to malicious content.
- Hash collision (theoretical, not practical with keccak256).

Verification steps:
1. Verify that `vaultHash` is stored on-chain and updated with metadata updates.
2. Confirm off-chain consumers verify hash before trusting vault content.
3. Check that metadata update emits events for tracking.

**T8: Denial of service**

Target: `setPaused` and contract availability.

Attack scenarios:
- Admin key compromise leads to permanent pause.
- Attacker spam-mints to exhaust gas limits in enumeration functions.

Verification steps:
1. Confirm pause is owner-only.
2. Check if `tokensOfOwner` or other view functions can be DOS'd by large token counts.
3. Verify that pause does not lock funds permanently (withdrawal should work even when paused, or there should be an emergency mechanism).

**T9: Merkle tree learning integrity**

Target: `vaultHash` used as Merkle root for learning agents.

Attack scenarios:
- Attacker modifies learning tree data off-chain without updating on-chain root.
- Attacker provides fraudulent Merkle proofs with crafted sibling nodes.
- Learning data poisoning through malicious interaction data.

Verification steps:
1. Verify that any claimed learning node can be validated via Merkle proof against the on-chain `vaultHash` root.
2. Confirm the learning module (logic contract) validates proof integrity before accepting updates.
3. Check that `updateAgentMetadata` correctly updates `vaultHash` when the Merkle root changes.
4. Verify that consumers verify proofs before trusting individual learning nodes.

**T10: Logic contract as learning module risks**

Target: Logic contracts implementing RAG, MCP, or learning modules.

Attack scenarios:
- Logic contract routes to compromised external AI service (MCP pattern).
- RAG logic contract retrieves poisoned vault content.
- Learning module generates invalid Merkle roots.
- Logic contract leaks private learning data through events or public state.

Verification steps:
1. Audit the logic contract's external service integrations.
2. Verify that learning data is validated before being incorporated into the tree.
3. Check that Merkle root computation matches the claimed tree structure.
4. Ensure sensitive learning data is not exposed through public view functions.

---

## Audit Checklist

### Access Control

- [ ] `setTreasury` requires `onlyOwner`
- [ ] `setPaused` requires `onlyOwner`
- [ ] `emergencyWithdraw` requires `onlyOwner`
- [ ] `grantAdditionalFreeMints` requires `onlyOwner`
- [ ] `setFreeMintsPerUser` requires `onlyOwner`
- [ ] `_authorizeUpgrade` requires `onlyOwner`
- [ ] `withdrawFromAgent` requires token owner
- [ ] `setAgentStatus` requires token owner
- [ ] `setLogicAddress` requires token owner
- [ ] `updateAgentMetadata` requires token owner
- [ ] No unauthorized path to any privileged function

### Reentrancy & CEI

- [ ] `withdrawFromAgent` uses `nonReentrant` modifier
- [ ] State updated before external call in `withdrawFromAgent`
- [ ] `emergencyWithdraw` is reentrancy-safe
- [ ] `fundAgent` correctly updates balance before any external interaction
- [ ] No unprotected `call.value` or `transfer` patterns

### Fund Safety

- [ ] Mint fee sent to treasury on paid mints
- [ ] Free mints send zero value to treasury
- [ ] Agent balance correctly incremented on `fundAgent`
- [ ] Agent balance correctly decremented on `withdrawFromAgent`
- [ ] Withdrawal amount validated against balance
- [ ] Emergency withdraw sends to treasury address only
- [ ] No way to drain funds without proper authorization

### Upgrade Safety

- [ ] `_authorizeUpgrade` guarded by `onlyOwner`
- [ ] Implementation disables initializers in constructor
- [ ] Storage layout is append-only (no variable reordering)
- [ ] `reinitializer` version incremented for new versions
- [ ] Gap variables reserved for future storage expansion

### Transfer Restrictions

- [ ] Free-minted tokens cannot be transferred
- [ ] `_update` or `_beforeTokenTransfer` hook enforces restriction
- [ ] `isFreeMint` mapping set correctly at mint time
- [ ] Paid tokens transfer normally

### Logic Contract Safety

- [ ] Only token owner can set logic address
- [ ] EOA addresses rejected for logic binding
- [ ] `address(0)` correctly unbinds logic
- [ ] Logic contract has no callback path to drain funds

### Input Validation

- [ ] Metadata strings have reasonable length limits
- [ ] Zero address checks where appropriate
- [ ] Token ID existence validated before operations
- [ ] Amount > 0 for funding and withdrawal

---

## Severity Classification

**Critical** — Direct fund loss or irreversible control loss. Example: reentrancy allowing balance drain, unauthorized upgrade to malicious implementation.

**High** — Significant trust or integrity failure. Example: access control bypass on admin functions, transfer restriction bypass for free mints.

**Medium** — Operational risk or unsafe defaults. Example: missing events for state changes, no pause on critical functions during emergency.

**Low** — Gas optimization, UX issues, or missing convenience features. Example: unbounded loop in view function, missing input validation on non-critical fields.

**Informational** — Best practice recommendations, code quality notes, documentation gaps.

---

## Automated Security Tools

### Static analysis with Slither

```bash
pip install slither-analyzer
slither contracts/NonFungibleAgents.sol --config-file slither.config.json
```

Key detectors relevant to BAP-578:
- `reentrancy-eth` — reentrancy on BNB transfers
- `unprotected-upgrade` — missing `_authorizeUpgrade` guard
- `unchecked-transfer` — missing return value check on calls
- `controlled-delegatecall` — delegatecall to user-controlled address
- `arbitrary-send-eth` — unauthorized BNB transfers

### Formal verification with Certora

For critical deployments, write formal verification rules:

```
rule withdrawPreservesInvariant {
    env e;
    uint256 tokenId;
    uint256 amount;
    
    uint256 balanceBefore = getAgentState(tokenId).balance;
    withdrawFromAgent(e, tokenId, amount);
    uint256 balanceAfter = getAgentState(tokenId).balance;
    
    assert balanceAfter == balanceBefore - amount;
}
```

### Gas griefing analysis

Check that no function can be griefed by sending excessive gas or triggering out-of-gas:
- `tokensOfOwner` with a user holding many tokens
- `emergencyWithdraw` with large contract balance
- `createAgent` with very long metadata strings

---

## Common Vulnerability Patterns

### Pattern: Unchecked return values

Solidity `call` returns a boolean. If not checked, failed transfers silently succeed in the contract's view.

```solidity
// VULNERABLE
(bool success, ) = payable(owner).call{value: amount}("");
// Missing: require(success, "Transfer failed");
```

### Pattern: Front-running

If mint fees or free mint allocations can be observed in the mempool, attackers may front-run to claim free mints or manipulate pricing.

Mitigation: Free mint allocation is per-address and checked on-chain, so front-running is limited. However, if dynamic pricing is added, commit-reveal patterns may be needed.

### Pattern: Integer overflow/underflow

Solidity 0.8+ has built-in overflow checks. Verify the contract uses Solidity >= 0.8.0. If using `unchecked` blocks, verify arithmetic safety manually.

---

## Audit Report Template

```
BAP-578 Security Audit Report
══════════════════════════════
Date:       YYYY-MM-DD
Auditor:    [name/team]
Commit:     [git hash]
Scope:      NonFungibleAgents.sol + dependencies

Summary
───────
Critical:    0
High:        0
Medium:      0
Low:         0
Informational: 0

Findings
────────
[ID] [Severity] [Title]
  Location: [contract]:[function]:[line]
  Description: [what was found]
  Impact: [what could happen]
  Recommendation: [how to fix]
  Status: [open/fixed/acknowledged]

Conclusion
──────────
[overall assessment and deployment recommendation]
```

---

## Output Format

When asked to audit BAP-578, respond with:

1. **Scope** (what was reviewed)
2. **Summary of findings** (critical/high/medium/low counts)
3. **Detailed findings** with function names, severity, and reasoning
4. **Recommended fixes** for each finding
5. **Residual risks** that cannot be fully mitigated
6. **Deployment recommendation** (proceed / fix first / do not deploy)

---

## Related Skills

- `bap578`
- `bap578-upgrade`
- `bap578-scanner`
