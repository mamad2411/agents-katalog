# Uniswap V3 Skill

Swap tokens on Base using Uniswap V3 SwapRouter02.

## Contracts (Base)

| Contract | Address |
|----------|---------|
| SwapRouter02 | `0x2626664c2603336E57B271c5C0b26F421741e481` |
| Quoter V2 | `0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a` |

## Fee Tiers

Uniswap V3 pools have different fee tiers. Choose based on the pair:

| Fee | Value | Best For |
|-----|-------|----------|
| 0.01% | 100 | Stablecoin pairs (USDC/USDT) |
| 0.05% | 500 | Stable pairs, high volume |
| 0.30% | 3000 | Most pairs (default) |
| 1.00% | 10000 | Exotic/low liquidity pairs |

**Tip:** WETH/USDC on Base typically uses the 0.30% (3000) pool.

## Swap: Exact Input Single

Swap a specific amount of input token for as much output as possible.

```javascript
import { encodeFunctionData, parseEther, parseUnits } from 'viem';

const SWAP_ROUTER = '0x2626664c2603336E57B271c5C0b26F421741e481';
const WETH = '0x4200000000000000000000000000000000000006';
const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';

// First: approve WETH for the router (see erc20 skill)

// SwapRouter02 exactInputSingle params (no deadline in struct!)
const swapParams = {
  tokenIn: WETH,
  tokenOut: USDC,
  fee: 3000,                              // 0.3% pool
  recipient: walletAddress,
  amountIn: parseEther('0.01'),           // 0.01 WETH
  amountOutMinimum: parseUnits('18', 6),  // Min 18 USDC (slippage protection)
  sqrtPriceLimitX96: 0n                   // No price limit
};

const swapData = encodeFunctionData({
  abi: [{
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
  }],
  functionName: 'exactInputSingle',
  args: [swapParams]
});

const txHash = await walletClient.sendTransaction({
  to: SWAP_ROUTER,
  data: swapData
});
```

## Common Gotchas

### 1. SwapRouter02 vs SwapRouter

SwapRouter02 uses a **different struct** than the original SwapRouter:
- ❌ SwapRouter: includes `deadline` in the struct
- ✅ SwapRouter02: NO `deadline` in struct (uses block.timestamp internally)

### 2. Approval required

You must approve the router to spend your tokens before swapping:
```javascript
// Approve WETH for SwapRouter02
await walletClient.sendTransaction({
  to: WETH,
  data: encodeFunctionData({
    abi: [{ name: 'approve', type: 'function', inputs: [{ type: 'address' }, { type: 'uint256' }], outputs: [{ type: 'bool' }] }],
    functionName: 'approve',
    args: [SWAP_ROUTER, maxUint256]
  })
});
```

### 3. Slippage protection

Always set a reasonable `amountOutMinimum`:
```javascript
// Get current price, then allow 2% slippage
const expectedOut = 20_000000n; // 20 USDC
const minOut = expectedOut * 98n / 100n; // 19.6 USDC minimum
```

### 4. Pool doesn't exist

If swap reverts, the pool might not exist for that fee tier. Try:
1. Different fee tier (500, 3000, 10000)
2. Multi-hop route through a common token

## See Also

- [erc20](../erc20/) - For approvals and transfers
- [weth](../weth/) - For wrapping ETH before swaps
