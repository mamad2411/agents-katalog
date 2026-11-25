---
name: web3-checklist
description: >  
  Web3-native feature checklist for smart contract audits. 20 protocol-specific
  checks covering proxy patterns, ERC20 edge cases, oracle safety, AMM risks,   
  vault accounting, and signature security. Run during SAST phase and referenced  
  by the Threat Modeler during task generation. 
trigger: During SAST phase and Decomposer output review.
agents: [sast-integrator, decomposer, threat-modeler] 
--- 

# Web3-Native Feature Checklist   
 
> Run this checklist during decomposition. Every ✗ is a potential task target.
 
## Proxy & Upgradeability (5 checks)

### W3-01: Proxy Pattern Identification
```
Check: Is this an upgradeable proxy (UUPS, Transparent, Beacon, Diamond)?
Tool:  grep -r "delegatecall\|upgradeable\|Proxy\|proxy" src/
Risk:  Storage slot collision, uninitialized implementations, selfdestruct
Flag:  ✗ if upgradeable proxy present → generate storage-layout task
```

### W3-02: Storage Layout Collision
```
Check: Do implementation contracts have the same storage layout at each upgrade?
Tool:  forge inspect ContractV1 storage-layout > v1.json
       forge inspect ContractV2 storage-layout > v2.json
       diff v1.json v2.json
Risk:  Upgrade corrupts state variables by shifting slot assignments
Flag:  ✗ if storage layout differs between versions → Critical task
```

### W3-03: Initialize-Once Enforcement
```
Check: Can initialize() be called more than once?
Tool:  grep -n "initializer\|_initialized\|initialize" src/
Risk:  Re-initialization overwrites critical state (owner, fee, config)
Flag:  ✗ if no initializer modifier or __gap missing → task
```

### W3-04: Implementation Selfdestruct Risk
```
Check: Does the implementation contract have selfdestruct or delegatecall to arbitrary addr?
Tool:  grep -n "selfdestruct\|suicide" src/
Risk:  If implementation selfdestructs, proxy becomes non-functional permanently
Flag:  ✗ if selfdestruct present in upgradeable implementation → Critical task
```

### W3-05: Admin Key Management
```
Check: Who can call upgradeTo()? Is there a timelock?
Tool:  grep -n "upgradeTo\|upgradeToAndCall\|onlyOwner\|ProxyAdmin" src/
Risk:  Immediate upgrade with malicious implementation = rug pull
Flag:  ✗ if no timelock on upgrade → access-control task
```

## ERC20 Edge Cases (4 checks)

### W3-06: Fee-on-Transfer Token Handling
```
Check: Does the protocol use balanceOf() before/after to track actual received amounts?
Tool:  grep -n "transfer\|safeTransfer\|transferFrom" src/
       Check: uint256 before = token.balanceOf(address(this));
              token.safeTransferFrom(...);
              uint256 actual = token.balanceOf(address(this)) - before;
Risk:  Protocol credits full amount but receives less (FoT tokens)
Flag:  ✗ if amount credited without balance-diff check → Medium/High task
```

### W3-07: Rebasing Token Accounting
```
Check: Does the protocol hold rebasing tokens (stETH, aTokens, AMPL)?
Tool:  grep -rn "stETH\|aToken\|rebase\|elastic" src/ docs/
Risk:  Stored balance diverges from actual balance over time
Flag:  ✗ if rebasing tokens held without rebasing-aware accounting → task
```

### W3-08: Token Approval Race Condition
```
Check: Does the protocol use approve() instead of safeIncreaseAllowance()?
Tool:  grep -n "\.approve(" src/
Risk:  ERC20 approve race allows double-spend on allowance change
Flag:  ✗ if approve() used in user-facing flow → Low task
```

### W3-09: Missing Return Value Check
```
Check: Does the protocol use raw ERC20 calls without SafeERC20?
Tool:  grep -n "\.transfer(\|\.transferFrom(\|\.approve(" src/ | grep -v "safe\|Safe"
Risk:  Non-standard ERC20s return false instead of reverting; silent failure
Flag:  ✗ if raw ERC20 calls without return value check → Medium task
```

## Oracle Safety (3 checks)

### W3-10: Oracle Staleness Check
```
Check: Does every oracle read check the updatedAt timestamp?
Tool:  grep -n "latestRoundData\|latestAnswer\|getPrice" src/
       Check: require(updatedAt >= block.timestamp - STALENESS_PERIOD, "stale");
Risk:  Stale price used after oracle stops updating (sequencer down, oracle malfunction)
Flag:  ✗ if no staleness check → High/Critical task depending on TVL
```

### W3-11: Oracle Manipulation Window
```
Check: Does the protocol use spot price (single block) or TWAP?
Tool:  grep -n "slot0\|getReserves\|consult\|observe" src/
Risk:  Flash loan can manipulate spot price within one block
Flag:  ✗ if spot price used for collateral/liquidation → Critical task
```

### W3-12: Oracle Sequencer Check (L2)
```
Check: On Arbitrum/Optimism: is the L2 sequencer uptime oracle checked?
Tool:  grep -rn "sequencer\|L2_SEQUENCER\|uptime" src/
Risk:  Stale oracle prices during sequencer downtime enable unfair liquidations
Flag:  ✗ if deployed on L2 without sequencer check → Medium/High task
```

## AMM & DeFi Primitives (3 checks)

### W3-13: Slippage Protection
```
Check: Do swaps/liquidity operations have slippage parameters enforced?
Tool:  grep -n "amountOutMin\|minAmountOut\|maxSlippage\|deadline" src/
Risk:  Sandwich attacks extract value from unprotected swaps
Flag:  ✗ if 0 slippage or no deadline → Medium task
```

### W3-14: Price Impact Limit
```
Check: For large AMM operations, is price impact bounded?
Tool:  Review liquidity pool interactions in business flows
Risk:  Single large trade moves price unfavorably, no protection for protocol
Flag:  ✗ if protocol executes large swaps without price impact limit → task
```

### W3-15: Rounding Direction
```
Check: In division operations involving user funds, does rounding favor the protocol?
Tool:  grep -n "mulDiv\|/ shares\|/ totalSupply\|/ totalAssets" src/
       Check: mulDivDown (floor) for user withdrawals = correct
              mulDivUp (ceil) for user deposits = correct
Risk:  Rounding in wrong direction lets users extract more than deposited
Flag:  ✗ if rounding favors user in withdrawal calculation → Medium task
```

## Vault & Share Accounting (2 checks)

### W3-16: ERC4626 Share Inflation
```
Check: Is this an ERC4626 vault? Does it use virtual shares?
Tool:  grep -n "ERC4626\|previewDeposit\|previewWithdraw\|convertToShares" src/
       Check: _decimalsOffset() returns non-zero (virtual shares protection)
Risk:  First depositor can inflate share price to steal subsequent depositors' funds
Flag:  ✗ if ERC4626 without virtual shares protection → Critical task
       (Check: does negative memory contain FP-SEED-001? If virtual shares present, skip)
```

### W3-17: Vault Donation Attack Vector
```
Check: Can a direct token transfer to the vault contract affect share price?
Tool:  Check totalAssets() implementation — does it use balanceOf(address(this))?
Risk:  Donation inflates totalAssets → share price jumps → existing holders benefit at depositors' expense
Flag:  ✗ if totalAssets reads raw balanceOf without virtual offset → task
       (Cross-check negative memory before generating — virtual shares make this a FP)
```

## Signature & Permit Security (3 checks)

### W3-18: EIP-712 Domain Separator
```
Check: Is the domain separator correctly bound to chainId and address?
Tool:  grep -n "DOMAIN_SEPARATOR\|domainSeparator\|_domainSeparatorV4" src/
       Check: includes chainId to prevent cross-chain replay
              includes address(this) to prevent cross-contract replay
Risk:  Missing chainId → signature valid on fork/testnet
Flag:  ✗ if domain separator missing chainId or address → Medium task
```

### W3-19: Permit Front-Running
```
Check: Is ERC20 permit() used in a way that can be front-run?
Tool:  grep -n "permit\|PERMIT_TYPEHASH" src/
Risk:  Attacker sees permit in mempool, calls permit() before the intended recipient,
       then the intended tx fails (DoS) — depending on protocol design
Flag:  ✗ if permit is critical path and failure is not gracefully handled → Low/Medium task
```

### W3-20: Cross-Chain Replay (Bridge Messages)
```
Check: Are cross-chain messages (bridge calls) protected against replay on the destination?
Tool:  grep -n "messageId\|nonce\|executed\|processed" src/
Risk:  Replay of bridge message executes the same action twice on destination
Flag:  ✗ if no replay protection on bridge message execution → Critical task
```

---

## Checklist Output Format

Record results in `specs/decomposition/web3-checklist.md`:

```markdown
# Web3-Native Feature Checklist — {protocol}

| Check | ID | Result | Task Generated |
|-------|----|--------|---------------|
| Proxy Pattern | W3-01 | ✓ UUPS proxy found | TASK-N: storage-layout |
| Storage Collision | W3-02 | ✓ Clean | — |
| Oracle Staleness | W3-10 | ✗ No staleness check | TASK-N: stale-oracle |
...
```
