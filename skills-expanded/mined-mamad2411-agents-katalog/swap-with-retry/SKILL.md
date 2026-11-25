# Swap with Retry Skill

Robust Uniswap V3 swaps with tiered slippage retry, quote-first safety, and proper error handling. Born from battle-testing daily $50 USDC pack payments.

## Core Features

1. **Quote first**: Always get Quoter V2 price before swapping
2. **Tiered slippage**: Start conservative, retry with higher slippage on failures  
3. **Gas estimation**: Fail fast if transaction will revert
4. **Comprehensive logging**: Track quote vs actual output
5. **Smart retry logic**: Handle "Too little received" errors intelligently

## Slippage Strategy

| Attempt | Slippage | Use Case |
|---------|----------|----------|
| 1 | 0.5% | Stable markets, high liquidity |
| 2 | 1.0% | Normal market conditions |
| 3 | 2.5% | Volatile markets, last resort |

## Implementation

```javascript
import { createPublicClient, createWalletClient, http } from 'viem';
import { base } from 'viem/chains';
import { encodeFunctionData, parseUnits, formatUnits, maxUint256 } from 'viem';

const RPC_URL = 'https://base-mainnet.g.alchemy.com/v2/UIq6IAtiFSotBU8rupy2z';

// Contract addresses (Base)
const QUOTER_V2 = '0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a';
const SWAP_ROUTER = '0x2626664c2603336E57B271c5C0b26F421741e481';

// ABIs
const ERC20_ABI = [
  { name: 'balanceOf', type: 'function', inputs: [{ type: 'address' }], outputs: [{ type: 'uint256' }] },
  { name: 'allowance', type: 'function', inputs: [{ type: 'address' }, { type: 'address' }], outputs: [{ type: 'uint256' }] },
  { name: 'approve', type: 'function', inputs: [{ type: 'address' }, { type: 'uint256' }], outputs: [{ type: 'bool' }] }
];

const QUOTER_ABI = [
  {
    name: 'quoteExactInputSingle',
    type: 'function',
    inputs: [
      { name: 'tokenIn', type: 'address' },
      { name: 'tokenOut', type: 'address' },
      { name: 'fee', type: 'uint24' },
      { name: 'amountIn', type: 'uint256' },
      { name: 'sqrtPriceLimitX96', type: 'uint160' }
    ],
    outputs: [{ name: 'amountOut', type: 'uint256' }]
  }
];

const SWAP_ROUTER_ABI = [
  {
    name: 'exactInputSingle',
    type: 'function',
    inputs: [{
      type: 'tuple',
      components: [
        { name: 'tokenIn', type: 'address' },
        { name: 'tokenOut', type: 'address' },
        { name: 'fee', type: 'uint24' },
        { name: 'recipient', type: 'address' },
        { name: 'amountIn', type: 'uint256' },
        { name: 'amountOutMinimum', type: 'uint256' },
        { name: 'sqrtPriceLimitX96', type: 'uint160' }
      ]
    }],
    outputs: [{ type: 'uint256' }]
  }
];

// Slippage tiers: [0.5%, 1%, 2.5%]
const SLIPPAGE_TIERS = [0.005, 0.01, 0.025];

async function swapWithRetry(walletClient, swapParams, options = {}) {
  const publicClient = createPublicClient({
    chain: base,
    transport: http(RPC_URL)
  });
  
  const {
    tokenIn,
    tokenOut,
    amountIn,
    fee = 3000, // Default to 0.3% pool
    recipient = walletClient.account.address,
    maxSlippage = 0.025, // 2.5% max
    customSlippageTiers = SLIPPAGE_TIERS,
    logLevel = 'info'
  } = { ...swapParams, ...options };
  
  const walletAddress = walletClient.account.address;
  
  // Step 1: Get quote
  const log = (level, message, data = {}) => {
    if (logLevel === 'debug' || (logLevel === 'info' && level !== 'debug')) {
      console.log(`[${level.toUpperCase()}] ${message}`, Object.keys(data).length > 0 ? data : '');
    }
  };
  
  log('info', 'Getting quote from Quoter V2...');
  
  const quote = await publicClient.readContract({
    address: QUOTER_V2,
    abi: QUOTER_ABI,
    functionName: 'quoteExactInputSingle',
    args: [tokenIn, tokenOut, fee, amountIn, 0n]
  });
  
  if (quote === 0n) {
    throw new Error('Quote returned 0 - pool may not exist or have sufficient liquidity');
  }
  
  log('info', `Quote: ${formatUnits(amountIn, 18)} → ${formatUnits(quote, 18)}`, { quote: quote.toString() });
  
  // Step 2: Check and ensure approval
  log('debug', 'Checking token approval...');
  
  const currentAllowance = await publicClient.readContract({
    address: tokenIn,
    abi: ERC20_ABI,
    functionName: 'allowance',
    args: [walletAddress, SWAP_ROUTER]
  });
  
  if (currentAllowance < amountIn) {
    log('info', 'Approving token for SwapRouter...');
    const approveTx = await walletClient.sendTransaction({
      to: tokenIn,
      data: encodeFunctionData({
        abi: ERC20_ABI,
        functionName: 'approve',
        args: [SWAP_ROUTER, maxUint256] // Unlimited approval
      })
    });
    log('debug', `Approval tx: ${approveTx}`);
    
    // Wait a moment for state to update
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Step 3: Attempt swaps with increasing slippage
  const applicableTiers = customSlippageTiers.filter(tier => tier <= maxSlippage);
  
  if (applicableTiers.length === 0) {
    throw new Error(`No applicable slippage tiers within max slippage of ${maxSlippage * 100}%`);
  }
  
  let lastError = null;
  
  for (let i = 0; i < applicableTiers.length; i++) {
    const slippage = applicableTiers[i];
    const amountOutMinimum = quote * BigInt(Math.floor((1 - slippage) * 10000)) / 10000n;
    
    log('info', `Attempt ${i + 1}/${applicableTiers.length}: ${slippage * 100}% slippage (min out: ${formatUnits(amountOutMinimum, 18)})`);
    
    try {
      const swapParams = {
        tokenIn,
        tokenOut,
        fee,
        recipient,
        amountIn,
        amountOutMinimum,
        sqrtPriceLimitX96: 0n
      };
      
      // Gas estimation
      log('debug', 'Estimating gas...');
      const swapData = encodeFunctionData({
        abi: SWAP_ROUTER_ABI,
        functionName: 'exactInputSingle',
        args: [swapParams]
      });
      
      const gasEstimate = await publicClient.estimateGas({
        account: walletAddress,
        to: SWAP_ROUTER,
        data: swapData
      });
      
      log('debug', `Gas estimate: ${gasEstimate}`);
      
      // Execute swap
      const txHash = await walletClient.sendTransaction({
        to: SWAP_ROUTER,
        data: swapData,
        gas: gasEstimate + (gasEstimate / 10n) // Add 10% buffer
      });
      
      log('info', 'Swap successful!', { 
        txHash, 
        slippageUsed: `${slippage * 100}%`,
        quoteExpected: formatUnits(quote, 18),
        minGuaranteed: formatUnits(amountOutMinimum, 18)
      });
      
      return {
        success: true,
        txHash,
        slippageUsed: slippage,
        quote: formatUnits(quote, 18),
        amountOutMinimum: formatUnits(amountOutMinimum, 18),
        attempt: i + 1
      };
      
    } catch (error) {
      lastError = error;
      const errorMsg = error.message.toLowerCase();
      
      if (errorMsg.includes('too little received') || errorMsg.includes('slippage')) {
        log('info', `Slippage error at ${slippage * 100}%, retrying with higher slippage...`);
        continue; // Try next slippage tier
      } else if (errorMsg.includes('insufficient')) {
        // Don't retry for balance issues
        throw new Error(`Insufficient balance: ${error.message}`);
      } else {
        // For other errors, log and continue trying
        log('info', `Error at ${slippage * 100}% slippage: ${error.message}`);
        if (i === applicableTiers.length - 1) {
          // Last attempt, throw the error
          throw error;
        }
      }
    }
  }
  
  // If we get here, all attempts failed
  throw new Error(`All swap attempts failed. Last error: ${lastError?.message || 'Unknown error'}`);
}

// Convenience wrapper with common token pairs
async function swapWETHtoUSDC(walletClient, wethAmount, options = {}) {
  const WETH = '0x4200000000000000000000000000000000000006';
  const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
  
  return await swapWithRetry(walletClient, {
    tokenIn: WETH,
    tokenOut: USDC,
    amountIn: parseUnits(wethAmount, 18),
    fee: 3000
  }, options);
}

async function swapUSDCtoWETH(walletClient, usdcAmount, options = {}) {
  const WETH = '0x4200000000000000000000000000000000000006';
  const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
  
  return await swapWithRetry(walletClient, {
    tokenIn: USDC,
    tokenOut: WETH,
    amountIn: parseUnits(usdcAmount, 6), // USDC has 6 decimals
    fee: 3000
  }, options);
}

export { swapWithRetry, swapWETHtoUSDC, swapUSDCtoWETH };
```

## Usage Examples

### Basic Swap with Retry
```javascript
import { parseUnits } from 'viem';

const result = await swapWithRetry(walletClient, {
  tokenIn: '0x4200000000000000000000000000000000000006', // WETH
  tokenOut: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', // USDC
  amountIn: parseUnits('0.02', 18), // 0.02 WETH
  fee: 3000 // 0.3% pool
});

console.log('Swap result:', result);
// { success: true, txHash: '0x...', slippageUsed: 0.005, quote: '45.23', amountOutMinimum: '44.99', attempt: 1 }
```

### Custom Slippage Strategy
```javascript
const result = await swapWithRetry(walletClient, {
  tokenIn: '0x...',
  tokenOut: '0x...',
  amountIn: parseUnits('100', 18)
}, {
  customSlippageTiers: [0.001, 0.005, 0.01], // 0.1%, 0.5%, 1%
  maxSlippage: 0.01,
  logLevel: 'debug'
});
```

### Convenience Wrappers
```javascript
// Swap 0.02 WETH → USDC
const result1 = await swapWETHtoUSDC(walletClient, '0.02', {
  maxSlippage: 0.015 // 1.5% max
});

// Swap 50 USDC → WETH  
const result2 = await swapUSDCtoWETH(walletClient, '50');
```

## Common Gotchas & Solutions

### 1. "Too Little Received" Error
**Problem:** Hardcoded `amountOutMinimum` fails when price moves between quote and execution.
```javascript
// ❌ BAD: Hardcoded minimum
amountOutMinimum: parseUnits('45', 6) // Will fail if market moves

// ✅ GOOD: Quote-based with slippage
const quote = await getQuote(...);
const amountOutMinimum = quote * 95n / 100n; // 5% slippage
```

### 2. Price Impact vs Slippage
- **Price Impact:** Your trade moves the pool price (larger trades = higher impact)
- **Slippage:** Market moves between quote and execution
- **Solution:** Account for both in your minimum out calculation

### 3. Pool Liquidity Issues
**Problem:** Pool doesn't exist or has insufficient liquidity.
```javascript
// Check quote first - if it's 0, pool has issues
if (quote === 0n) {
  throw new Error('Pool may not exist or have sufficient liquidity');
}
```

### 4. Gas Estimation Failures
**Problem:** Transaction will revert, but you don't know until you send.
```javascript
// Always estimate gas before sending
const gasEstimate = await publicClient.estimateGas({
  account: walletAddress,
  to: SWAP_ROUTER,
  data: swapData
});
// If this throws, the transaction would revert
```

### 5. Approval Race Conditions
**Problem:** Insufficient allowance, but approval transaction hasn't confirmed.
```javascript
// Check current allowance before every swap
const currentAllowance = await publicClient.readContract({
  address: tokenIn,
  abi: ERC20_ABI,
  functionName: 'allowance',
  args: [walletAddress, SWAP_ROUTER]
});

if (currentAllowance < amountIn) {
  // Need to approve
}
```

### 6. Fee Tier Selection
Different pairs use different fee tiers:

| Pair Type | Recommended Fee | Value |
|-----------|-----------------|-------|
| Stablecoins (USDC/USDT) | 0.01% | 100 |
| Major pairs (WETH/USDC) | 0.30% | 3000 |
| Exotic pairs | 1.00% | 10000 |

## Debugging Tips

### Enable Debug Logging
```javascript
const result = await swapWithRetry(walletClient, swapParams, {
  logLevel: 'debug' // Shows gas estimates, approvals, etc.
});
```

### Monitor Actual Output
Compare quote vs actual received amount in block explorer:
- Quote gave you: X tokens
- You actually received: Y tokens  
- Difference = price impact + slippage + fees

### Check Pool States
Use Uniswap V3 subgraph to verify pool exists and has liquidity:
```graphql
{
  pool(id: "pool_address") {
    liquidity
    sqrtPrice
    feeTier
  }
}
```

## See Also

- [uniswap-v3](../uniswap-v3/) - For understanding SwapRouter02 mechanics
- [erc20](../erc20/) - For token approvals and balance checks
- [scheduled-payment](../scheduled-payment/) - Uses this skill for auto-swap logic