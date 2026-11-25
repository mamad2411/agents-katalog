---
name: solidity-testing
description: "[AUTO-INVOKE] MUST be invoked BEFORE writing or modifying Foundry test files (*.t.sol). Covers unit, fuzz, invariant, fork, adversarial, differential, and regression testing. Trigger: any task involving creating or editing Solidity tests."
---

# Solidity Testing Standards

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

## Toolchain Baseline

- Use `solc 0.8.24`, OpenZeppelin Contracts `5.0.2`, and the Foundry version installed by the repository.
- Read `foundry.toml` before changing test configuration. Preserve existing profiles and raise fuzz or invariant intensity according to risk instead of overwriting project settings.
- Use OpenZeppelin 5.x APIs and import paths in test fixtures and mocks.

## Test Organization

- Organize tests by behavior and boundary: unit, integration, fuzz, invariant, fork, and regression tests may use separate contracts or directories.
- Name ordinary tests `test_<behavior>_<scenario>` and fuzz tests `testFuzz_<behavior>`.
- Do not use `testFail_*`. Assert the intended failure with `vm.expectRevert`, preferably matching a custom-error selector or fully encoded error.
- Each test must run independently. Use `setUp()` for fixtures and never depend on execution order.
- Keep helpers and mocks minimal. A reference model must be independent from the production implementation it checks.

## Behavioral Coverage

Every core function must have tests covering:

| Scenario | What to verify |
|----------|---------------|
| Happy path | Standard input → expected output, correct state changes |
| Permission checks | Unauthorized caller → `vm.expectRevert` with correct error |
| Boundary conditions | Domain minimum/maximum, zero where valid, and off-by-one values |
| Failure scenarios | Security-relevant `require`, revert, and custom-error paths |
| State changes | Storage and balance deltas; events alone are not proof of correct state |
| Edge cases | Empty arrays, duplicate calls, self-transfers |

Select additional tests from the contract's behavior:

| Contract behavior | Additional tests |
|-------------------|------------------|
| External callbacks | Reentrancy, rejecting receiver, malformed return data |
| ERC20 integration | No-return, fee-on-transfer, rebase, and approval-reset behavior |
| Signatures | Replay, wrong signer, chain, nonce, and expired deadline |
| Oracle consumption | Stale/invalid answers, decimals, deviation, and low-liquidity conditions |
| Proxy/initializer | Reinitialization, uninitialized implementation, authorization, storage compatibility |
| Accounting/vault math | Rounding direction, first deposit, donation, solvency, and conservation |

## Foundry Cheatcodes Quick Reference

| Cheatcode | Usage |
|-----------|-------|
| `vm.prank(addr)` | Next call from `addr` |
| `vm.startPrank(addr)` | All calls from `addr` until `vm.stopPrank()` |
| `vm.warp(timestamp)` | Set `block.timestamp` |
| `vm.roll(blockNum)` | Set `block.number` |
| `vm.deal(addr, amount)` | Set ETH balance |
| `vm.expectRevert(error)` | Next call must revert with the expected selector or encoded error |
| `vm.expectEmit(true,true,false,true)` | Verify event emission (topic checks) |
| `vm.record()` / `vm.accesses()` | Track storage reads/writes |
| `makeAddr("name")` | Create labeled address for readable traces |

## Fuzz Testing Rules

- Fuzz math-heavy, accounting, authorization, and fund-flow boundaries.
- Map scalar inputs into the valid domain with `bound()` when possible. Use `vm.assume()` only for relational or structurally invalid inputs that cannot be mapped cheaply.
- Assert properties, balance deltas, and postconditions rather than duplicating the implementation line by line.
- Increase runs for high-value or complex paths based on execution cost and risk; do not prescribe one universal run count.
- Preserve any minimized failure as a deterministic regression test and record the seed needed to reproduce unresolved failures.

## Stateful Invariant Testing

- Use `StdInvariant` with a handler for multi-step protocols and state machines.
- Restrict the action space with `targetContract` and `targetSelector`; do not let irrelevant reverts dominate exploration.
- Track ghost variables when expected totals cannot be derived directly from contract state.
- Check system properties such as conservation, solvency, monotonic counters, authorization isolation, and legal state transitions.
- Unexpected reverts are findings. Do not hide them by weakening the invariant or adding broad assumptions.

Read [references/advanced-testing.md](references/advanced-testing.md) when implementing invariant handlers, deterministic fork tests, adversarial mocks, differential tests, mutation testing, or gas-regression gates.

## Fork Testing

- Pin the chain and block number. Do not base reproducible tests on the latest block.
- Assert `block.chainid`, dependency bytecode, and critical interface bindings before exercising protocol behavior.
- A missing RPC or archive capability must produce an explicit skip or failure; it must not silently pass the test.
- Keep local unit tests for business logic. Fork tests validate integration assumptions, not every code path.

## Verification Rules

- Verify state and balance changes in addition to events and return values.
- Every fixed vulnerability or production incident requires a regression test that fails before the fix.
- Coverage percentage is diagnostic only. It does not replace branch, adversarial, invariant, or mutation testing.
- Use gas snapshots for regression detection, not brittle exact-gas assertions inside ordinary tests.
- Never broadcast transactions or load production signing keys from tests.

## Common Commands

```bash
# Run all tests
forge test

# Run specific test function
forge test --match-test test_transfer

# Run specific test contract
forge test --match-contract MyTokenTest

# Verbose output with full trace
forge test -vvvv

# Gas report
forge test --gas-report

# Fuzz with a risk-appropriate run count
forge test --fuzz-runs <RUNS>

# Run invariant tests
forge test --match-test invariant_ -vvvv

# Check gas snapshots when the repository tracks them
forge snapshot --check

# Test coverage
forge coverage

# Coverage with report
forge coverage --report lcov
```
