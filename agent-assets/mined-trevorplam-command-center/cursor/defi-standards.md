---
description: Run DeFi Protocol and Financial Standards Check
globs: ["**/defi/**/*.ts", "**/protocols/**/*.ts", "**/liquidity/**/*.ts", "**/yield/**/*.ts"]
---
# Finance: DeFi Protocol & Financial Standards

<audit_rules>
- You MUST implement proper smart contract security for financial operations including overflow/underflow protection.
- You MUST ensure all financial calculations use precise decimal arithmetic (not floating point).
- You MUST implement proper oracle security with price feed validation and delay mechanisms.
- You MUST configure proper slippage protection and maximum loss parameters for trades.
- You MUST implement proper liquidity pool management with impermanent loss calculations.
- You MUST ensure proper governance mechanisms for protocol parameter changes.
- You MUST implement proper audit trails and event logging for all financial operations.
- You MUST configure proper emergency pause mechanisms and circuit breakers.
- You MUST ensure proper yield farming calculations with APY/APR transparency.
- You MUST implement proper risk management and position monitoring systems.
</audit_rules>

<example_good>
```typescript
// DeFi Protocol Implementation with Security

import { ethers } from 'ethers';
import { FixedNumber } from '@ethersproject/bignumber';

export class DeFiProtocol {
  constructor(
    private priceOracle: PriceOracle,
    private liquidityPool: LiquidityPool,
    private governance: GovernanceContract,
    private riskManager: RiskManager
  ) {}

  async addLiquidity(
    user: string,
    tokenA: string,
    tokenB: string,
    amountA: bigint,
    amountB: bigint,
    minLiquidity: bigint
  ): Promise<LiquidityReceipt> {
    // Validate inputs
    this.validateAddress(user);
    this.validateAddress(tokenA);
    this.validateAddress(tokenB);
    this.validateAmount(amountA);
    this.validateAmount(amountB);

    // Get current prices from oracle with delay
    const priceA = await this.priceOracle.getPriceWithDelay(tokenA, 300); // 5 min delay
    const priceB = await this.priceOracle.getPriceWithDelay(tokenB, 300);

    // Calculate expected liquidity
    const expectedLiquidity = this.calculateLiquidity(amountA, amountB, priceA, priceB);
    
    // Slippage protection
    if (expectedLiquidity < minLiquidity) {
      throw new Error('Insufficient liquidity output');
    }

    // Risk management check
    await this.riskManager.validateLiquidityAddition(user, tokenA, tokenB, amountA, amountB);

    // Execute liquidity addition
    const receipt = await this.liquidityPool.addLiquidity({
      user,
      tokenA,
      tokenB,
      amountA,
      amountB,
      minLiquidity,
    });

    // Emit event for off-chain tracking
    await this.emitEvent('LiquidityAdded', {
      user,
      tokenA,
      tokenB,
      amountA,
      amountB,
      liquidityReceived: receipt.liquidity,
      timestamp: Date.now(),
    });

    return receipt;
  }

  async swap(
    user: string,
    tokenIn: string,
    tokenOut: string,
    amountIn: bigint,
    minAmountOut: bigint,
    deadline: number
  ): Promise<SwapReceipt> {
    // Validate deadline
    if (Date.now() > deadline) {
      throw new Error('Transaction expired');
    }

    // Validate inputs
    this.validateAddress(user);
    this.validateAddress(tokenIn);
    this.validateAddress(tokenOut);
    this.validateAmount(amountIn);

    // Get price with slippage protection
    const price = await this.priceOracle.getPrice(tokenIn, tokenOut);
    const expectedOut = this.calculateSwapOutput(amountIn, price);
    
    // Apply slippage tolerance (0.5%)
    const slippageTolerance = expectedOut * 995n / 1000n;
    if (slippageTolerance < minAmountOut) {
      throw new Error('Insufficient output amount');
    }

    // Risk management check
    await this.riskManager.validateSwap(user, tokenIn, tokenOut, amountIn);

    // Execute swap
    const receipt = await this.liquidityPool.swap({
      user,
      tokenIn,
      tokenOut,
      amountIn,
      minAmountOut,
    });

    // Emit event
    await this.emitEvent('SwapExecuted', {
      user,
      tokenIn,
      tokenOut,
      amountIn,
      amountOut: receipt.amountOut,
      timestamp: Date.now(),
    });

    return receipt;
  }

  async calculateYield(
    poolAddress: string,
    userAddress: string,
    period: number
  ): Promise<YieldCalculation> {
    const pool = await this.liquidityPool.getPool(poolAddress);
    const userPosition = await pool.getUserPosition(userAddress);

    // Calculate impermanent loss
    const impermanentLoss = this.calculateImpermanentLoss(pool);
    
    // Calculate trading fees earned
    const tradingFees = await this.calculateTradingFees(poolAddress, userAddress, period);
    
    // Calculate rewards (if any)
    const rewards = await this.calculateRewards(poolAddress, userAddress, period);

    // Calculate APY using precise decimal arithmetic
    const totalReturn = FixedNumber.from(tradingFees + rewards);
    const principal = FixedNumber.from(userPosition.totalLiquidity);
    const apy = totalReturn.div(principal).mul(FixedNumber.from(365 * 100)).div(FixedNumber.from(period));

    return {
      principal: userPosition.totalLiquidity,
      tradingFees,
      rewards,
      impermanentLoss,
      totalYield: tradingFees + rewards,
      apy: apy.toUnsafeFloat(),
    };
  }

  async emergencyPause(reason: string): Promise<void> {
    // Check governance authorization
    const isAuthorized = await this.governance.isAuthorized(msg.sender, 'EMERGENCY_PAUSE');
    if (!isAuthorized) {
      throw new Error('Not authorized to pause protocol');
    }

    // Execute emergency pause
    await this.liquidityPool.pause();
    
    // Emit emergency event
    await this.emitEvent('ProtocolPaused', {
      reason,
      pausedBy: msg.sender,
      timestamp: Date.now(),
    });
  }

  private validateAddress(address: string): void {
    if (!ethers.isAddress(address)) {
      throw new Error('Invalid address');
    }
  }

  private validateAmount(amount: bigint): void {
    if (amount <= 0n) {
      throw new Error('Amount must be positive');
    }
  }

  private calculateLiquidity(
    amountA: bigint,
    amountB: bigint,
    priceA: bigint,
    priceB: bigint
  ): bigint {
    // Precise liquidity calculation
    const valueA = amountA * priceB;
    const valueB = amountB * priceA;
    return (valueA + valueB) / (priceA * priceB);
  }

  private calculateSwapOutput(amountIn: bigint, price: bigint): bigint {
    // Include fees and slippage
    const fee = amountIn * 3n / 1000n; // 0.3% fee
    const amountAfterFee = amountIn - fee;
    return amountAfterFee * price / 1n18;
  }

  private calculateImpermanentLoss(pool: Pool): number {
    // Calculate impermanent loss percentage
    const currentRatio = pool.reserveA / pool.reserveB;
    const initialRatio = pool.initialReserveA / pool.initialReserveB;
    const ratioChange = currentRatio / initialRatio;
    
    // Impermanent loss formula: 2 * sqrt(ratio) / (1 + ratio) - 1
    const sqrtRatio = Math.sqrt(ratioChange);
    return (2 * sqrtRatio) / (1 + ratioChange) - 1;
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: Insecure DeFi implementation
export class InsecureDeFi {
  // BAD: Using floating point for financial calculations
  async calculateYield(principal: number, rate: number, time: number): number {
    // BAD: Floating point precision issues
    return principal * rate * time;
  }

  // BAD: No slippage protection
  async swap(user: string, tokenIn: string, tokenOut: string, amountIn: number) {
    // BAD: No minimum output check
    // BAD: No deadline check
    // BAD: No price oracle validation
    
    // BAD: Direct price calculation without delay
    const price = await this.getPrice(tokenIn, tokenOut);
    const amountOut = amountIn * price;
    
    // BAD: No risk management
    // BAD: No event logging
    return { amountOut };
  }

  // BAD: No overflow protection
  async addLiquidity(user: string, amountA: number, amountB: number) {
    // BAD: No overflow checks
    const totalLiquidity = amountA + amountB;
    
    // BAD: No impermanent loss calculation
    // BAD: No governance checks
    return { liquidity: totalLiquidity };
  }

  // BAD: No emergency mechanisms
  // BAD: No audit trails
  // BAD: No precise decimal arithmetic
}
```
</example_bad>
