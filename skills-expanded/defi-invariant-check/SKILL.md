---
name: defi-invariant-check
audience: specialist
description: Use when the audit target is a DeFi protocol — AMM, lending market, yield vault, stablecoin, or perps — and you must author the economic properties generic campaigns miss, such as token-conservation, constant-product k, share accounting, collateralization, and oracle-deviation invariants, then falsify them.
---

<!-- inspired by trailofbits/skills (concept); repointed to native CLIs for Chrono -->

# defi-invariant-check

DeFi-specific invariant authoring and testing discipline. Use this as a sub-skill during
`evm-audit-flow` when the target is a DeFi protocol (AMM, lending, yield, bridge, stablecoin,
perps). Generic Echidna/Medusa campaigns miss DeFi-specific invariants — this skill provides
the property checklist. All tools are the **native host CLIs** (`echidna`, `medusa`, `forge`,
`halmos`) run in the target project directory; there is no wrapper layer.

## Invariant categories

**Token accounting invariants (always required):**
- `totalSupply == sum(balanceOf(all_holders))` — no spurious minting or burning.
- `reserve0 * reserve1 >= k` (for constant-product AMMs) — k-invariant never decreases except via fee accrual.
- `totalBorrow <= totalDeposit` for all lending pools — protocol cannot lend out more than deposited.
- `sum(userShares) == totalShares` for yield vaults — share accounting is consistent.

**Access-control invariants:**
- Only authorized roles can set oracle addresses, fee parameters, or pause state.
- `onlyOwner`/`onlyGovernance` functions cannot be called by arbitrary external accounts.
- Upgradeable proxy implementation slots cannot be modified except through the upgrade pathway.

**Economic/oracle invariants:**
- Flash loan callbacks cannot leave the protocol in a net-loss state after the loan repayment.
- Liquidation proceeds must cover the borrowed amount plus protocol fee — no bad-debt accrual from liquidations.

**2026 incident-derived oracle-input robustness invariants (highest-priority economic class):**
- **Spot versus TWAP:** a price used for collateral, borrowing, liquidation, minting, or
  redemption must reject or clamp a same-block spot price when
  `abs(spot - TWAP) / TWAP > maxDeviation`; no value-affecting path may silently fall back
  to the divergent spot. This targets the oracle/valuation-manipulation class represented by
  Moonwell (2026-08-27), Lazy Summer (2026-07-06), Makina (2026-01-20), and Edel
  (2026-07-01) in `V114-51`.
- **Low-liquidity collateral:** within the protocol's configured manipulation budget, an
  atomic trade against a thin market cannot increase an account's borrowable value or
  liquidation proceeds by more than the attacker's net cost plus the configured safety
  margin. Reject collateral whose observable depth cannot support the valuation notional.
  This is the Moonwell low-liquidity-collateral oracle shape from `V114-51`.
- **NAV manipulation bound:** absent external profit or loss, a deposit/reprice/redeem round
  trip across any supported asset must not return more value than entered after fees and
  rounding tolerance, and one manipulable component price must not move total NAV beyond
  its configured exposure and deviation caps. This targets the Lazy Summer, Makina, and
  Edel valuation/NAV incident class from `V114-51`.

**2026 incident-derived governance/timelock invariants (second priority):**
- **Delay cannot be bypassed or shortened:** for every queued privileged operation,
  `executedAt - queuedAt >= max(delayAtQueue, protocolMinimumDelay)`. Changing the delay,
  executor, proposer, or role graph after queueing cannot accelerate that operation, and a
  delay change itself becomes effective only after the pre-change delay. This targets Term
  Finance's 2026-08-24 timelock-zeroing shape from `V114-51`.
- A role or executor change cannot authorize its own proposal or execution; every privilege
  expansion must be queued and executed by the pre-change authority after the full
  pre-change delay. Snapshot the audited role graph and assert that no post-deployment role
  drift broadens value-moving authority outside that path. This targets the TOP
  (2026-06-26) and BonkDAO (2026-07-26) governance-bypass shapes from `V114-51`.

**Rounding/precision invariants (third priority, still required):**
- Exercise zero-supply initialization, one-unit deposits/withdrawals, values immediately
  below and above every division boundary, and repeated dust operations. No non-zero asset
  input may mint zero shares unless the transaction reverts or the loss is explicitly
  bounded; no positive supply or assets may exist without corresponding claimable shares.
- A deposit/redeem or mint/withdraw round trip, with no external profit or loss, must return
  the starting economic value within the documented fee and rounding bound; splitting one
  operation into many dust-sized operations cannot improve that bound.
- Fuzz solver domains and every fixed-point math-library boundary used by share conversion,
  including zero denominators, scale changes, and minimum/maximum supported values. These
  properties retain the dust/zero-supply class seen twice at Thetanuts in June 2026, while
  placing it behind the two larger 2026 code-level classes identified by `V114-51`.

**Reentrancy invariants:**
- Protocol state (balances, reserves, shares) after any external call must equal the state written before the call (CEI pattern verification).
- No re-entrant call can increase the caller's balance beyond their pre-call entitlement.

## Order of ops

1. **Identify the protocol class.** AMM, lending, vault, bridge, stablecoin, or perps. Each class has a canonical invariant set (use the category checklist above).

2. **Author Echidna properties.** Write properties as Solidity functions with prefix `echidna_` that return `bool`. Properties must be pure invariants (no state mutations inside the property). Place in `test/invariants/EchidnaTest.sol`.

3. **Run Echidna** — minimum 30 minutes for DeFi protocols:
   ```bash
   echidna . --contract EchidnaTest --config echidna.yaml --test-limit 500000
   ```
   Use `testMode: assertion` in `echidna.yaml` for complex multi-step violations.

4. **Run Medusa** as a second pass if Echidna does not find violations — Medusa's
   coverage-guided corpus often finds violations Echidna's random mutation misses:
   ```bash
   medusa fuzz --config medusa.json
   ```

5. **Flash-loan attack simulation.** Manually construct a flash-loan attack call sequence in a
   Forge test that instantiates a `FlashLoanAttacker` contract, then run `forge test --match-contract FlashLoanAttacker -vvvv`. Verify the k-invariant or balance-conservation invariant holds after the attack sequence.

6. **Price-oracle and NAV manipulation check.** For protocols with on-chain price oracles:
   write a Forge test that varies market depth, creates large single-block spot/TWAP
   divergence, and reprices each NAV component. Check whether the oracle-derived price would
   enable profitable liquidations, under-collateralized borrows, or a profitable
   deposit/reprice/redeem round trip (`forge test --match-test testOracleManip -vvvv`).

7. **Governance/timelock check.** Queue each value-moving privileged operation, then mutate
   the delay and role graph and attempt early or self-authorized execution. Use the target
   framework's time-warp primitive to assert that execution remains impossible until the
   greater of the queued delay and protocol minimum has elapsed.

8. **Rounding/precision check.** Fuzz zero-supply initialization, dust values around every
   division boundary, split-versus-batched operations, and deposit/redeem round trips. Keep
   tolerances in the protocol's documented units; a tolerance must not erase a zero-share
   mint or ghost-supply state.

## When to pivot

- **Echidna cannot construct valid state transitions:** the protocol requires complex setup (governance votes, time-locks, external oracle seeding). Author a setup harness in a `CryticSetup` contract that initializes the protocol to a valid post-deployment state.
- **Invariant is too weak:** Echidna falsifies it immediately with trivial inputs. Tighten the property — e.g., add a precondition (`require(totalSupply > 0)`) to avoid vacuous falsification.
- **Protocol uses proxy pattern:** Echidna tests the proxy ABI; ensure the proxy's `fallback` routes correctly to the implementation in the test environment.

## Anti-patterns

- Do NOT author invariants that pass by construction — e.g., an `echidna_` property that trivially returns `true` because the function under test is never called.
- Do NOT treat a single Echidna `passed` result as proof of correctness — Echidna is a fuzzer, not a prover. Use `halmos` for bounded formal guarantees on critical properties (`halmos --function check_ --loop 4`).
- Do NOT skip flash-loan simulation for lending/AMM protocols — flash loans invalidate many invariants that hold under normal call conditions.

## Example

Writing and running an Echidna token conservation invariant:

```solidity
// test/invariants/EchidnaTest.sol
contract EchidnaTest {
    Token token;

    function echidna_total_supply_equals_sum() public view returns (bool) {
        // totalSupply must equal sum of all holder balances
        return token.totalSupply() == token.balanceOf(address(this))
                                     + token.balanceOf(address(0xdead));
    }
}
```

```bash
echidna . --contract EchidnaTest --config echidna.yaml --test-limit 500000
```

## Recording (chrono-vault)

The task packet's injected memory contract owns the exact call shape, sequence, and fields - see
`wirework-reflect`. Do not copy a `record(...)` example or add fields (including `source_task`) from
memory; the server binds them, and a baked example violates the run's authenticated schema. Memory is
best-effort telemetry and never gates the work. What is worth recording here is the task-specific
outcome: protocol class, invariants tested, violations, flash-loan/oracle-manip tested?.
