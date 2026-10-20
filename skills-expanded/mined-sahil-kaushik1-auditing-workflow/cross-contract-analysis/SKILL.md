---
name: cross-contract-analysis
description: >
  Multi-contract interaction safety analysis. Composability risks, cross-contract
  reentrancy, state inconsistency across contracts. Used during threat modeling.
---

# Cross-Contract Analysis Skill

## Purpose

Many real vulnerabilities don't exist inside one contract. Every module may look safe
independently while the complete flow is unsafe. This skill catalogs cross-contract
interaction patterns that commonly produce vulnerabilities.

## Common Cross-Contract Vulnerability Patterns

### 1. Cross-Contract Reentrancy
Contract A calls Contract B, which calls back into Contract A (or Contract C which
reads stale state from Contract A).

**Key check**: Does Contract A update its state BEFORE making external calls?

### 2. Inconsistent Oracle Consumption
Multiple contracts consume the same oracle but at different points in a transaction.
One sees the pre-manipulation price, another sees the post-manipulation price.

**Key check**: Is the oracle price cached or re-fetched per call?

### 3. Accounting Desync
Contract A tracks balances internally. Contract B also tracks balances. A state change
in one is not reflected in the other, creating ghost assets or phantom debt.

**Key check**: Are there multiple sources of truth for the same quantity?

### 4. Privilege Escalation via Composability
Contract A gives Contract B certain permissions. Contract B has a public function that
Contract A's developers didn't consider, allowing an attacker to use B as a proxy to
affect A's state.

**Key check**: Does the privilege granted to B exceed what's needed?

### 5. State Transition Race Conditions
Multi-step operations spanning contracts can be front-run or interleaved with other
operations, leaving the system in an inconsistent state.

**Key check**: Are multi-step operations atomic or interruptible?

### 6. Flash Loan Amplified Cross-Contract Attacks
A flash loan can temporarily alter state in Contract A (e.g., inflate a balance),
then exploit Contract B which reads that inflated state.

**Key check**: Does Contract B rely on Contract A's spot state for critical calculations?

## Analysis Protocol

1. Map all inter-contract call sites (from SAST integrator output)
2. For each call: what state can the callee observe? What state can it modify?
3. For each pair of contracts: is there shared state? Shared dependencies?
4. Generate cross-contract tasks for the Threat Modeler

## Output

Feed observations into the Threat Modeler for task generation. Cross-contract tasks
should have explicit multi-contract execution paths in their task definition.
