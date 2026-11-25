---
name: economic-modeling
description: >
  Economic impact modeling for DeFi protocols. AMM slippage models, vault
  share accounting models, oracle dependency graphs, and MEV calculation
  patterns. Used by the Economic Analyst agent and Threat Modeler when
  estimating economic_impact_estimate during task generation.
trigger: When generating economic_impact_estimate in tasks, or during Economic Analyst analysis.
agents: [economic-analyst, threat-modeler]
---

# Economic Modeling Skill

## Model 1: Vault Share Accounting

Used for: ERC4626 vaults, yield-bearing tokens, staking vaults

### Share Price Formula
```
share_price = totalAssets / totalShares

attack_profit = victim_deposit × (manipulated_price/fair_price - 1)

# Share inflation attack (first depositor):
# Attacker deposits 1 wei → gets 1 share
# Attacker donates X tokens directly to vault
# share_price = (1 + X) / 1 = X+1
# Victim deposits Y → gets Y/(X+1) shares ≈ 0 shares
# Attacker redeems 1 share → gets (X+1)/(1) × totalShares proportion ≈ X + victim_deposit
# Attacker profit ≈ victim_deposit - (donation cost)
```

### ERC4626 Key Functions to Check
```solidity
previewDeposit(uint256 assets) → shares     // Should round DOWN
previewMint(uint256 shares) → assets        // Should round UP
previewWithdraw(uint256 assets) → shares    // Should round UP (costs more shares)
previewRedeem(uint256 shares) → assets      // Should round DOWN (user gets less)

convertToShares: assets * totalSupply / totalAssets  // floor division
convertToAssets: shares * totalAssets / totalSupply  // floor division
```

### Red Flags
- `totalAssets()` reads `token.balanceOf(address(this))` → donation attack surface
- No virtual shares offset (`_decimalsOffset() returns 0`)
- Rounding favors user in withdrawal (mulDivUp where mulDivDown should be used)

---

## Model 2: AMM Slippage & Price Impact

Used for: Uniswap V2/V3, Curve, Balancer, custom AMMs

### Constant Product (x * y = k)
```
price_impact = deltaX / (X + deltaX)

# Flash loan manipulation:
# Pool has X ETH, Y USDC, k = X*Y
# Attacker flash loans L ETH, swaps into pool:
#   new_X = X + L
#   new_Y = k / (X + L)
# Price changes from Y/X to new_Y/new_X
# Profit depends on what protocol reads during this window
```

### MEV Window Calculation
```
# Single-block manipulation:
#   Window = 1 block (12 seconds on mainnet)
#   Attacker must front-run target tx and back-run in same block

# Multi-block TWAP manipulation:
#   Oracle reads average price over N blocks
#   Cost = sustained deviation over N blocks
#   Feasibility = (manipulation_profit) > (deviation_cost × N_blocks)
```

---

## Model 3: Liquidation State Machine

Used for: Lending protocols (Compound, Aave-style)

### Health Factor
```
health_factor = (collateral × liquidation_threshold) / debt
healthy:     health_factor >= 1.0
at_risk:     0.9 <= health_factor < 1.0
liquidatable: health_factor < 1.0
bad_debt:    collateral < debt (protocol takes loss)
```

### Liquidation Profit Window
```
liquidation_bonus = protocol-defined discount (typically 5-15%)
liquidator_profit = seized_collateral_value × liquidation_bonus - gas_cost

# Bad debt risk:
# If price drops faster than liquidators can act:
#   collateral_value < debt_value
#   Protocol absorbs the shortfall (insurance fund or socialized loss)
```

### Oracle Attack on Liquidation
```
# Attacker manipulates oracle price downward → positions become liquidatable
# Attacker acts as liquidator → acquires collateral at discount
# Profit = (fair_value - manipulated_price) × collateral - oracle_manipulation_cost
```

---

## Model 4: Flash Loan Economics

Available liquidity (as of 2024 approximate figures):

```
Aave V3 (Ethereum):
  USDC: ~$500M
  WETH: ~$300M
  DAI:  ~$200M
  Fee:  0.05% of borrowed amount

Balancer (Ethereum):
  USDC/DAI: ~$100M
  Fee:  0% (flash loans are free on Balancer)

Uniswap V3 (Ethereum):
  Any token in pools
  Fee:  0.05%, 0.30%, or 1.00% depending on pool tier
```

### Flash Loan Feasibility Check
```
required_amount = {from attack path}
available_liquidity = {check on-chain}
flash_loan_fee = required_amount × fee_rate

net_profit = attack_extract - flash_loan_fee - gas_cost

if net_profit > 0 and available_liquidity >= required_amount:
    attack is economically rational
```

---

## Model 5: Cross-Protocol Composability

Used for: Integrations between protocols (yield aggregators, meta-vaults)

### State Inconsistency Risk
```
# Protocol A reads price from Oracle O at time T1
# Protocol B reads price from Oracle O at time T2 (T2 > T1)
# If price changes between T1 and T2:
#   State in A and B is inconsistent
#   Attacker can exploit the inconsistency window

# Risk window = max(T2 - T1, block_time)
```

### Approval Dependency Attack
```
# If Protocol B relies on Protocol A's approval:
#   Attacker front-runs the approval with a transfer
#   B sees stale approval state → executes against wrong assumption
```

---

## Impact Classification (Immunefi Matrix)

```python
def classify_severity(direct_loss_usd, tvl_usd):
    pct_of_tvl = direct_loss_usd / tvl_usd

    if direct_loss_usd > 500_000 or pct_of_tvl > 0.10:
        return "Critical"
    elif direct_loss_usd > 50_000 or pct_of_tvl > 0.01:
        return "High"
    elif direct_loss_usd > 5_000:
        return "Medium"
    elif direct_loss_usd > 0:
        return "Low"
    else:
        return "Informational"
```

## Cast Commands for On-Chain Data

```bash
# Get token balance of contract
cast call $TOKEN "balanceOf(address)(uint256)" $CONTRACT --rpc-url $RPC_URL

# Get total assets
cast call $VAULT "totalAssets()(uint256)" --rpc-url $RPC_URL

# Get total shares
cast call $VAULT "totalSupply()(uint256)" --rpc-url $RPC_URL

# Get share price (both in wei, divide after)
assets=$(cast call $VAULT "totalAssets()(uint256)" --rpc-url $RPC_URL)
shares=$(cast call $VAULT "totalSupply()(uint256)" --rpc-url $RPC_URL)
echo "Share price (raw): $assets / $shares"

# Get Chainlink price
cast call $FEED "latestRoundData()(uint80,int256,uint256,uint256,uint80)" --rpc-url $RPC_URL

# Check if sequencer is up (L2)
cast call $SEQ_UPTIME_FEED "latestRoundData()(uint80,int256,uint256,uint256,uint80)" --rpc-url $RPC_URL
```
