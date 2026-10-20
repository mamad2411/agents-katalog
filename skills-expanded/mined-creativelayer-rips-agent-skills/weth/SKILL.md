# WETH Skill

Wrap and unwrap ETH on Base and other EVM chains.

## What is WETH?

WETH (Wrapped ETH) is an ERC20 version of ETH. You need it because:
- Many DeFi protocols only work with ERC20 tokens
- Uniswap V3 swaps require ERC20 tokens
- You can't use native ETH directly in most smart contracts

## Contract Address (Base)

```
WETH: 0x4200000000000000000000000000000000000006
```

This is the same address on most L2s (Base, Optimism, Arbitrum).

## Wrap ETH → WETH

Send ETH to the WETH contract's `deposit()` function:

```javascript
import { encodeFunctionData, parseEther } from 'viem';

const WETH = '0x4200000000000000000000000000000000000006';

const txHash = await walletClient.sendTransaction({
  to: WETH,
  value: parseEther('0.1'), // Amount of ETH to wrap
  data: encodeFunctionData({
    abi: [{ name: 'deposit', type: 'function', inputs: [], outputs: [] }],
    functionName: 'deposit',
    args: []
  })
});
```

Or simply send ETH to the WETH address (it auto-wraps):
```javascript
const txHash = await walletClient.sendTransaction({
  to: WETH,
  value: parseEther('0.1'),
});
```

## Unwrap WETH → ETH

Call `withdraw()` to get your ETH back:

```javascript
const txHash = await walletClient.sendTransaction({
  to: WETH,
  data: encodeFunctionData({
    abi: [{ 
      name: 'withdraw', 
      type: 'function', 
      inputs: [{ type: 'uint256' }], 
      outputs: [] 
    }],
    functionName: 'withdraw',
    args: [parseEther('0.1')] // Amount of WETH to unwrap
  })
});
```

## Check Balances

```javascript
// ETH balance
const ethBalance = await publicClient.getBalance({ address: walletAddress });

// WETH balance
const wethBalance = await publicClient.readContract({
  address: WETH,
  abi: [{
    name: 'balanceOf',
    type: 'function',
    inputs: [{ type: 'address' }],
    outputs: [{ type: 'uint256' }]
  }],
  functionName: 'balanceOf',
  args: [walletAddress]
});
```

## When to Wrap vs Unwrap

| Situation | Action |
|-----------|--------|
| Need to swap on Uniswap | Wrap ETH → WETH first |
| Received WETH, want ETH for gas | Unwrap WETH → ETH |
| Sending to CEX | Usually unwrap (they want ETH) |
| DeFi protocols | Usually keep as WETH |

## Gas Considerations

- Wrapping: ~25,000 gas
- Unwrapping: ~30,000 gas
- On Base, this costs fractions of a cent

Keep some unwrapped ETH for gas fees!
