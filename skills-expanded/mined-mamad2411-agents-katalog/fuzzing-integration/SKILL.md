---
name: fuzzing-integration
description: >
  Integration patterns for Echidna, Medusa, and Halmos fuzzing tools.
  Used by the Verifier when a task's phase field is 5 (medusa-fuzz),
  6 (echidna), or 7 (halmos). Provides setup templates, config files,
  and decision guide for which tool to use when.
trigger: When task.phase is 5-medusa-fuzz, 6-echidna, or 7-halmos.
agents: [verifier, sast-integrator]
---

# Fuzzing Integration Skill

## Tool Selection Guide

| Scenario | Best Tool | Why |
|---------|-----------|-----|
| Multi-step state transitions (5+ txs) | Medusa | Better at long sequences |
| Arithmetic invariants, overflow, rounding | Echidna | Faster at numeric property testing |
| Mathematical proof of safety (no counterexample) | Halmos | Symbolic, exhaustive within bounds |
| Single-transaction exploits | Foundry unit PoC | Simpler, faster |
| Accounting invariants (totalAssets, totalShares) | Foundry stateful invariants | Direct and readable |
| Unknown vulnerability type | Medusa → Echidna (sequence then property) | Broad coverage |

## Phase 5: Medusa Long-Sequence Fuzzing

### Setup

```json
// medusa.json — place at project root
{
  "fuzzing": {
    "workers": 10,
    "timeout": 300,
    "testLimit": 100000,
    "callSequenceLength": 100,
    "deploymentOrder": ["TargetContract"],
    "corpusDirectory": "specs/verification/TASK-{N}-medusa/corpus",
    "testing": {
      "stopOnFailedTest": true,
      "stopOnFailedCallSequence": false,
      "traceAll": false,
      "assertionTesting": {
        "enabled": true
      },
      "propertyTesting": {
        "enabled": true,
        "testPrefixes": ["property_"]
      }
    }
  },
  "compilation": {
    "platform": "foundry"
  }
}
```

### Property Contract Template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/TargetContract.sol";

contract TASK_{N}_MedusaProperties {
    TargetContract target;
    address attacker = address(0x1337);

    constructor() {
        target = new TargetContract();
        // Setup initial state
    }

    // Medusa calls this sequence of functions then checks property_*
    function property_totalAssets_gte_totalLiabilities() public returns (bool) {
        return target.totalAssets() >= target.totalLiabilities();
    }

    function property_share_price_non_decreasing() public returns (bool) {
        // Implement invariant check
        return true;
    }
}
```

### Run

```bash
medusa fuzz --config medusa.json --target TASK_{N}_MedusaProperties
# Output corpus to: specs/verification/TASK-{N}-medusa/
```

## Phase 6: Echidna Property Fuzzing

### Config

```yaml
# echidna.yaml — place at project root
testLimit: 50000
workers: 4
shrinkLimit: 5000
seqLen: 100
testMode: property
corpusDir: "specs/verification/TASK-{N}-echidna/corpus"
contractAddr: "0x00a329c0648769A73afAc7F9381E08FB43dBEA72"
deployer: "0x30000"
sender:
  - "0x10000"   # user 1
  - "0x20000"   # user 2
  - "0x30000"   # attacker
```

### Property Contract Template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../src/TargetContract.sol";

contract TASK_{N}_EchidnaProperties {
    TargetContract target;

    constructor() {
        target = new TargetContract();
    }

    // Echidna checks functions prefixed with "echidna_"
    function echidna_solvency() public returns (bool) {
        return target.totalAssets() >= target.totalLiabilities();
    }

    function echidna_no_free_shares() public returns (bool) {
        return target.totalShares() == 0 || target.totalAssets() > 0;
    }
}
```

### Run

```bash
echidna . --contract TASK_{N}_EchidnaProperties --config echidna.yaml
```

### Interpreting Results

```
PASSED: Property holds for all sequences tried (not a proof — increase testLimit for confidence)
FAILED: Echidna found a counterexample — extract the call sequence for the PoC
  The failing sequence will be printed. Convert it to a Foundry test for the final PoC.
```

## Phase 7: Halmos Symbolic Proof

Halmos proves invariants symbolically — it either finds a counterexample or proves
the property holds for all inputs within the specified bounds.

### Setup

```bash
# Install
pip install halmos

# Verify
halmos --version
```

### Symbolic Test Template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "halmos-cheatcodes/SymTest.sol";
import "../src/TargetContract.sol";

contract TASK_{N}_HalmosCheck is SymTest, Test {
    TargetContract target;

    function setUp() public {
        target = new TargetContract();
    }

    // Halmos checks functions prefixed with "check_"
    function check_share_price_monotonic(
        uint256 depositAmount,
        uint256 withdrawAmount
    ) public {
        // Symbolic inputs: Halmos tries ALL possible values
        vm.assume(depositAmount > 0 && depositAmount < type(uint128).max);
        vm.assume(withdrawAmount > 0 && withdrawAmount <= depositAmount);

        uint256 priceBefore = target.sharePrice();
        target.deposit(depositAmount, address(this));
        target.withdraw(withdrawAmount, address(this), address(this));
        uint256 priceAfter = target.sharePrice();

        // This assertion must hold for ALL inputs
        assert(priceAfter >= priceBefore);
    }
}
```

### Run

```bash
halmos --function check_share_price_monotonic --loop 3 --solver-timeout 60
```

### Interpreting Results

```
✓ Proved: No counterexample found within bounds → Safety argument supported
✗ Counterexample found: {symbolic values} violate the property → Convert to Foundry PoC
? Timeout: Increase --solver-timeout or simplify the property
```

## Converting Fuzzer Output to Foundry PoC

When Echidna/Medusa finds a counterexample, convert the call sequence:

```
Echidna output:
  Counterexample:
    Call 1: deposit(100)
    Call 2: withdraw(99)
    Call 3: deposit(1)
    Property violated: echidna_solvency()

Convert to:
  function test_exploit_from_fuzzer() public {
      target.deposit(100);
      target.withdraw(99);
      target.deposit(1);
      assertGe(target.totalAssets(), target.totalLiabilities()); // should FAIL
  }
```

Run the converted test with `forge test -vvvv` to get the full trace for the report.
