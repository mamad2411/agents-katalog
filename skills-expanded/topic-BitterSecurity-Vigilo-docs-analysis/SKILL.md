---
name: docs-analysis
description: >
  Auto-loaded by speculator agent during Audit Phase 1 (Reconnaissance).
  Provides methodology for: documentation analysis, invariant extraction,
  trust assumption mapping, and protocol type classification from docs.
  Output: .vigilo/recon/docs-findings.md
user-invocable: false
---

# Documentation Reconnaissance Methodology

## Purpose

Rapidly understand **what the protocol should do** through documentation analysis.
This is reconnaissance, not code analysis.

---

## 1. Documentation Discovery

### Search Patterns

```
Glob("**/README*")
Glob("**/*.md")
Glob("**/docs/**/*")
Glob("**/SECURITY*")
Glob("**/*.pdf")
```

### Priority Order

| Priority | File | What to Extract |
|----------|------|-----------------|
| 1 | Root README | Project overview, quick start |
| 2 | docs/README.md | Documentation entry point |
| 3 | SECURITY.md | Security considerations, contacts |
| 4 | Whitepaper/spec | Formal specification |
| 5 | Audit reports | Known issues, past findings |

### Skip These
- Code files (`.sol`, `.rs`, etc.)
- Test documentation
- CI/CD configuration

---

## 2. The 4 Essential Questions

### Question 1: Where Is the Money?

| Asset Type | What to Look For |
|------------|------------------|
| Native tokens | ETH, MATIC, AVAX holdings |
| ERC20 tokens | USDC, USDT, DAI, protocol tokens |
| LP tokens | Uniswap, Curve, Balancer positions |
| NFTs | ERC721, ERC1155 assets |
| Shares/receipts | Vault shares, staked positions |

**Extract**: Which contracts hold assets, TVL mentions, treasury.

### Question 2: Who Can Move the Money?

**User Paths**:
| Action | Function Names |
|--------|---------------|
| Deposit | `deposit()`, `stake()`, `supply()`, `mint()` |
| Withdraw | `withdraw()`, `unstake()`, `redeem()`, `burn()` |

**Privileged Paths**:
| Action | Function Names | Risk Level |
|--------|---------------|------------|
| Emergency | `emergencyWithdraw()`, `pause()` | High |
| Recovery | `sweep()`, `rescue()`, `skim()` | High |
| Config | `setFee()`, `setOracle()`, `upgradeTo()` | Medium |

**Extract**: Function names, who can call, conditions.

### Question 3: What Invariants Must Hold?

**Explicit Invariants** - Keywords:
- "must", "always", "never", "guaranteed", "ensures"
- Mathematical relationships: `x + y = z`, `a <= b * c`
- NatSpec: `@invariant`, `@notice`

**Implicit Invariants** - By Protocol Type:

| Protocol Type | Common Invariant |
|---------------|------------------|
| Vault | `totalAssets >= totalShares * minPrice` |
| Lending | `userDebt <= userCollateral * LTV` |
| AMM | `reserveX * reserveY >= k` |
| Staking | `sum(userStakes) == totalStaked` |
| Bridge | `mintedOnL2 == lockedOnL1` |

Mark inferred invariants with `[INFERRED]`.

### Question 4: What Trust Assumptions Exist?

| Trusted Party | What They Control | Questions to Answer |
|--------------|-------------------|---------------------|
| Owner | Contract upgrades | Timelock? Multisig? |
| Admin | Parameter changes | Bounds? Frequency? |
| Oracle | Price feeds | Freshness? Backup? |
| Keeper | Liquidations | Incentives? Constraints? |

**Extract**: Who is trusted, for what, with what safeguards.

---

## 3. Protocol Type Classification

| Pattern in Docs | Protocol Type | Priority Vectors |
|-----------------|---------------|------------------|
| swap, liquidity, reserves | AMM/DEX | Price manipulation, sandwich |
| borrow, collateral, liquidate | Lending | Oracle manipulation, bad debt |
| deposit, shares, yield | Vault | Share inflation, first depositor |
| vote, propose, execute | Governance | Flash loan voting, timelock |
| lock, mint, bridge | Bridge | Double spend, replay |
| stake, reward, epoch | Staking | Reward calculation, timing |

---

## 4. Extraction Process

### Step 1: High-Level Understanding

Read overview documents to understand:
- Protocol purpose and value proposition
- Target users and use cases
- Integration with other protocols
- Economic model

### Step 2: Mechanism Analysis

For each mechanism described:
1. Identify inputs and outputs
2. Note preconditions and postconditions
3. Extract mathematical relationships
4. Identify external dependencies

### Step 3: Security Information

Look for:
- Security considerations sections
- Known limitations and risks
- Threat model descriptions
- Emergency procedures

### Step 4: Gap Identification

Note what's MISSING:
- Undefined edge cases
- Unclear trust assumptions
- Missing invariants
- Ambiguous specifications

---

## 5. Quality Assessment

| Rating | Criteria |
|--------|----------|
| Excellent | Complete invariants, clear trust model, all mechanisms documented |
| Good | Most information present, some inference needed |
| Adequate | Basic coverage, significant gaps |
| Poor | Minimal documentation, heavy inference required |
| Minimal | Almost no documentation |

---

## 6. Edge Cases

### Minimal Documentation
1. Note quality as "Poor" or "Minimal"
2. Flag ALL missing critical information
3. Infer what possible, mark as `[INFERRED]`
4. Recommend documentation improvements
5. Note increased audit risk

### Conflicting Information
1. Note the conflict explicitly
2. List all versions found
3. Flag for clarification
4. Do not assume which is correct

### Non-English Documentation
1. Note the language limitation
2. Extract what is possible
3. Flag for native speaker review

---

## Output

Write findings to `.vigilo/recon/docs-findings.md` following the format in
[`template.md`](template.md).

---

## Additional Resources

- [**`template.md`**](template.md) - Output template for documentation reconnaissance findings
- [**`examples/minimal-output.md`**](examples/minimal-output.md) - Minimal output example for sparse documentation
