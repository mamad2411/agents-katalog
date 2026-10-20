---
name: foundry-harness
description: Foundry test generation for PoC creation, invariant testing, and fuzz testing. Used during verification by the Verifier agent.
trigger: During verification — when the Verifier needs to reproduce or refute a vulnerability hypothesis.
agents: [verifier]
---

# Foundry Harness Skill

> **Trigger**: During verification — when the Verifier builds executable evidence.
> **Purpose**: Generate Foundry test harnesses for PoC creation, invariant testing, and fuzzing.

---

## Overview

Every vulnerability claim must be backed by executable evidence. This skill provides
templates and protocols for building Foundry tests that either **confirm** or **refute**
the Deep Reasoner's hypotheses.

---

## Test Types

### 1. Exploit PoC (Confirm a Vulnerability)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
// Import target contracts

contract TASK_{N}_Exploit is Test {
    // Contract instances
    // Attacker address

    function setUp() public {
        // Option A: Fork mainnet at specific block
        // vm.createSelectFork(vm.envString("RPC_URL"), blockNumber);

        // Option B: Deploy fresh contracts
        // target = new TargetContract(params);

        // Set up attacker
        // vm.deal(attacker, 100 ether);
        // deal(address(token), attacker, 1_000_000e18);
    }

    function test_exploit() public {
        // Record pre-state
        uint256 preBalance = token.balanceOf(attacker);

        // Execute attack sequence
        vm.startPrank(attacker);
        // Step 1: ...
        // Step 2: ...
        // Step 3: ...
        vm.stopPrank();

        // Assert the failure predicate from the task
        uint256 postBalance = token.balanceOf(attacker);
        assertGt(postBalance, preBalance, "Attacker should have profited");
    }
}
```

### 2. Invariant Test (Prove Safety)

```solidity
contract TASK_{N}_Invariant is Test {
    function setUp() public {
        // Deploy contracts, set up initial state
    }

    function test_invariant_holds() public {
        // Execute the path from the task
        // Assert the invariant HOLDS
        assertGe(vault.totalAssets(), vault.totalLiabilities());
    }

    function test_boundary_values() public {
        // Test with: 0, 1, type(uint256).max, dust amounts
        // Test with: max array lengths, empty arrays
    }
}
```

### 3. Fuzz Test (Search for Violations)

```solidity
contract TASK_{N}_Fuzz is Test {
    function setUp() public {
        // Deploy contracts
    }

    function testFuzz_invariant(uint256 amount, address user) public {
        vm.assume(amount > 0 && amount < type(uint128).max);
        vm.assume(user != address(0));

        // Execute with fuzzed inputs
        vm.prank(user);
        // ... execute path

        // Assert invariant
        assertGe(totalAssets, totalLiabilities);
    }
}
```

---

## Foundry Cheatcodes Reference

### State Manipulation
```solidity
vm.prank(address)           // Next call from address
vm.startPrank(address)      // All calls from address until stopPrank
vm.deal(address, amount)    // Set ETH balance
deal(token, address, amt)   // Set ERC20 balance (forge-std)
vm.store(addr, slot, val)   // Set storage slot directly
vm.load(addr, slot)         // Read storage slot
```

### Time & Block
```solidity
vm.warp(timestamp)          // Set block.timestamp
vm.roll(blockNumber)        // Set block.number
skip(seconds)               // Advance time
```

### Forking
```solidity
vm.createSelectFork(rpc, block)  // Fork at block
vm.createSelectFork(rpc)         // Fork at latest
```

### Assertions
```solidity
assertEq(a, b)             // Equality
assertGe(a, b)             // a >= b
assertGt(a, b)             // a > b
assertLe(a, b)             // a <= b
assertLt(a, b)             // a < b
```

### Events & Reverts
```solidity
vm.expectRevert(bytes4(selector))  // Expect revert
vm.expectEmit(true, true, false, true)  // Expect event
```

---

## Execution Commands

```bash
# Run specific test
forge test --match-test test_exploit -vvvv

# Run with gas reporting
forge test --match-test test_exploit -vvvv --gas-report

# Run fuzz tests (increase runs)
forge test --match-test testFuzz -vvv --fuzz-runs 10000

# Run on fork
forge test --match-test test_exploit -vvvv --fork-url $RPC_URL --fork-block-number $BLOCK
```

---

## Output

Save test files to: `specs/verification/TASK-{N}-poc.t.sol`
Save results to: `specs/verification/TASK-{N}-verification.md`

### Verdict Classification

| Verdict | Criteria |
|---------|---------|
| **CONFIRMED** | PoC passes, failure predicate satisfied, attack is reproducible |
| **REFUTED** | PoC fails, protective mechanism verified, invariant proven to hold |
| **INCONCLUSIVE** | Cannot construct PoC (missing deps, fork issues, gas limits) |

---

## Constraints

- **DO NOT** modify target contracts to make PoC work
- **DO NOT** use unrealistic attacker capabilities (e.g., admin access)
- **DO** test at boundary values (0, 1, max, dust)
- **DO** record the exact forge command and output
- **DO** explain WHY the test passes/fails
