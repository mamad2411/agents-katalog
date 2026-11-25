---
name: evidence-gates
description: >
  10-gate evidence engine. Every finding must pass all applicable gates before
  reaching CONFIRMED status. The Judge runs this checklist sequentially.
  A failed gate stops promotion. Used by Verifier (after verdict) and Judge (final decision).
trigger: After any CONFIRMED verdict. Mandatory before Judge approves a finding.
agents: [verifier, judge]
---

# Evidence Gates Skill — 10-Gate Checklist

> No PoC = No confirmed finding. No gate = No evidence.

Run all 10 gates in order. Each gate must produce PASS, FAIL, or WAIVED (with reason).
A single FAIL downgrades the finding from CONFIRMED to CANDIDATE until resolved.

---

## Gate 1: In-Scope Gate

**Question**: Is this finding within the declared audit scope?

```
Check:
  □ Target contract is in the declared audit scope
  □ Attack does NOT require a trusted role (unless admin-bug scope declared)
  □ Attack does NOT match any out_of_scope_cases in the task file

Evidence required: Contract name in scope list + out_of_scope_cases review

FAIL → Mark: REJECTED-OUT-OF-SCOPE
WAIVED if: Scope explicitly includes admin/trusted-role vulnerabilities
```

## Gate 2: Reachability Gate

**Question**: Can an external attacker reach the vulnerable code?

```
Check:
  □ Entry function is public or external (not internal/private)
  □ No modifier blocks access (onlyOwner, onlyRole, whenNotPaused, etc.)
  □ No require() on the call path the attacker cannot satisfy
  □ If state-dependent: required state is reachable by the attacker

Evidence required: Function visibility + every modifier/require on the call path (with line refs)

FAIL → Mark: INCONCLUSIVE-REACHABILITY
```

## Gate 3: Attacker Controllability Gate

**Question**: Does the attacker control the critical parameter?

```
Check:
  □ The attacker can freely set the input that triggers the failure predicate
  □ The attacker cannot be front-run between setup and exploitation
  □ If ordering-dependent: attacker can guarantee the ordering (e.g., atomic tx)

Evidence required: Which parameter is controlled + how attacker sets it

FAIL → Mark: INCONCLUSIVE-CONTROLLABILITY
```

## Gate 4: State Feasibility Gate

**Question**: Can the required pre-state be achieved on-chain?

```
Check:
  □ Required token balances are achievable (not "assume infinite liquidity")
  □ Required transaction sequence is feasible (no impossible ordering)
  □ If flash loan: loan amount is available at Aave/Balancer/Euler
  □ No time locks or cooldowns make the window infeasible

Evidence required: Specific state preconditions + how each is achievable

FAIL → Mark: INCONCLUSIVE-STATE-FEASIBILITY
```

## Gate 5: Asset Impact Gate

**Question**: Does this result in measurable asset loss or protocol damage?

```
Check:
  □ Attacker gains tokens, ETH, or protocol shares
  OR Protocol loses solvency / totalAssets < totalLiabilities
  OR Users are permanently denied access to funds

Evidence required: Specific token/ETH flow in the PoC

FAIL → Mark: LOW-INFORMATIONAL (downgrade if impact is only theoretical)
WAIVED if: Scope explicitly includes DoS with no economic impact
```

## Gate 6: No Trusted-Role Dependency Gate

**Question**: Does the attack require a trusted admin action?

```
Check:
  □ Attack does NOT need admin to set a malicious parameter first
  □ Attack does NOT need governance to pass a malicious proposal first
  □ Attack works against the protocol as currently deployed

Evidence required: Confirm no privileged tx in the attack path

FAIL → Mark: REJECTED-TRUSTED-ROLE-DEPENDENCY
WAIVED if: task.attacker_model.can_be_trusted_role = true (explicit scope)
```

## Gate 7: No Unsupported Token Assumption Gate

**Question**: Does the attack depend on non-standard ERC20 behavior?

```
Check:
  □ If attack needs fee-on-transfer: is this in scope per task.token_model?
  □ If attack needs rebasing token: is this in scope?
  □ If attack needs ERC777 callbacks: is this in scope?

Cross-check: task.token_model.exceptions list

FAIL → Mark: REJECTED-TOKEN-ASSUMPTION-VIOLATED
WAIVED if: task.token_model.exceptions explicitly includes the required behavior
```

## Gate 8: Deterministic Replay Gate

**Question**: Does the PoC run deterministically?

```
Check:
  □ forge test --match-test test_exploit passes 3/3 consecutive runs
  □ No timing dependencies causing intermittent failures
  □ If fork-based: pinned to specific block number (--fork-block-number N)

Evidence required: 3 consecutive forge test outputs (all passing)

FAIL → Mark: INCONCLUSIVE-FLAKY-POC, return to Verifier
```

## Gate 9: Counterfactual Fix Gate

**Question**: Does fixing the root cause actually prevent the attack?

```
Check:
  □ Apply the minimal suggested fix (e.g., add CEI, add slippage check)
  □ Re-run the PoC: it MUST fail after the fix
  □ This proves the identified root cause is correct

Evidence required: Modified contract + PoC failure output after fix

FAIL → Mark: INCONCLUSIVE-WRONG-ROOT-CAUSE, return to Reasoner
```

## Gate 10: Severity Calibration Gate

**Question**: Is the severity label correctly calibrated?

```
Check:
  □ Economic impact assessment (from Economic Analyst) matches severity label
  □ Immunefi matrix applied consistently:
      Critical: > $500k OR > 10% TVL
      High:     $50k-$500k OR 1-10% TVL
      Medium:   $5k-$50k OR < 1% TVL
      Low:      < $5k OR theoretical
  □ Gas cost of exploit < extracted value (economically rational)

Evidence required: Economic Analyst report + severity mapping

FAIL → Adjust severity to match economic evidence
```

---

## Gate Results Table Format

Include in verification artifact and gate decision file:

```markdown
## Evidence Gate Results — TASK-{N}

| Gate | Name | Result | Key Evidence |
|------|------|--------|-------------|
| 1 | In-Scope | PASS | Contract in scope list, no out_of_scope match |
| 2 | Reachability | PASS | withdraw() public, no modifier |
| 3 | Controllability | PASS | Attacker controls `shares` param |
| 4 | State Feasibility | PASS | Flash loan from Aave V3 |
| 5 | Asset Impact | PASS | ~500k USDC extracted |
| 6 | No Trusted Role | PASS | Only requires user role |
| 7 | Token Assumptions | PASS | Standard ERC20 only |
| 8 | Deterministic Replay | PASS | 3/3 forge test runs pass |
| 9 | Counterfactual Fix | PASS | CEI fix causes PoC to fail |
| 10 | Severity Calibration | PASS | Critical confirmed by economic model |

**Final Verdict**: CONFIRMED — Critical
**Gates Passed**: 10/10
```

## Gate Failure Actions

| Failure Type | Action |
|-------------|--------|
| REJECTED-* | Finding is dead. Document in gap record. Add to negative memory. |
| INCONCLUSIVE-REACHABILITY | Return to Context Builder for deeper code trace |
| INCONCLUSIVE-CONTROLLABILITY | Return to Reasoner for attacker model revision |
| INCONCLUSIVE-STATE-FEASIBILITY | Return to Reasoner with feasibility constraint |
| INCONCLUSIVE-FLAKY-POC | Return to Verifier to stabilize PoC |
| INCONCLUSIVE-WRONG-ROOT-CAUSE | Return to Reasoner to reidentify root cause |
| Severity Mismatch | Adjust severity in place, do not reject finding |
