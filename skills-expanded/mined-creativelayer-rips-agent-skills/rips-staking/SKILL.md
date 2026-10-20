# RIPS Staking Skill

Stake RIPS tokens on Base and claim USDC rewards from the FeePool.

## Contracts (Base - Chain 8453)

| Contract | Address | Notes |
|----------|---------|-------|
| RIPS Token | `0xc1aDDAe61Bc74a14971BFA48A0B7141AdeD4fB07` | 18 decimals |
| Staker V2 | `0xB6d7B6F1c4Ad64d75fc8c63e56188b6e3eF0c004` | Staking contract |
| FeePool (Rewards) | `0xb0D256824ACd2EE1cbC03e97C47A7B5fec9Fe5f3` | Rewards distribution |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6 decimals, reward token |

## Flow

### 1. Approve RIPS for Staker

```javascript
await walletClient.sendTransaction({
  to: RIPS,
  data: encodeFunctionData({
    abi: erc20Abi,
    functionName: 'approve',
    args: [STAKER, maxUint256]
  })
});
```

### 2. Stake RIPS

```javascript
await walletClient.sendTransaction({
  to: STAKER,
  data: encodeFunctionData({
    abi: stakerAbi,
    functionName: 'stake',
    args: [userAddress, RIPS, amount, true, [FEEPOOL]]
  })
});
```

Parameters:
- `user` — address receiving the stake
- `token` — RIPS token address
- `quantity` — amount in wei (18 decimals)
- `customize` — `true` to specify custom fee pools
- `customPools` — array of FeePool addresses to join

### 3. Claim Rewards

```javascript
await walletClient.sendTransaction({
  to: STAKER,
  data: encodeFunctionData({
    abi: stakerAbi,
    functionName: 'claimRewards',
    args: [userAddress, USDC]
  })
});
```

## Read Operations

### Check Staked Balance

```javascript
const staked = await publicClient.readContract({
  address: STAKER,
  abi: [{ name: 'getStake', type: 'function', inputs: [{ type: 'address' }, { type: 'address' }], outputs: [{ type: 'uint256' }], stateMutability: 'view' }],
  functionName: 'getStake',
  args: [userAddress, RIPS]
});
// formatEther(staked) for human-readable
```

### Check Claimable Rewards

```javascript
const claimable = await publicClient.readContract({
  address: FEEPOOL,
  abi: [{ name: 'getUnpaidRewards', type: 'function', inputs: [{ type: 'address' }], outputs: [{ type: 'uint256' }], stateMutability: 'view' }],
  functionName: 'getUnpaidRewards',
  args: [userAddress]
});
// formatUnits(claimable, 6) for USDC amount
```

## ABIs

### Staker V2

```javascript
const stakerAbi = [
  { name: 'stake', type: 'function', inputs: [{ name: 'user', type: 'address' }, { name: 'token', type: 'address' }, { name: 'quantity', type: 'uint256' }, { name: 'customize', type: 'bool' }, { name: 'customPools', type: 'address[]' }], outputs: [] },
  { name: 'getStake', type: 'function', inputs: [{ name: 'user', type: 'address' }, { name: 'token', type: 'address' }], outputs: [{ type: 'uint256' }], stateMutability: 'view' },
  { name: 'claimRewards', type: 'function', inputs: [{ name: 'user', type: 'address' }, { name: 'token', type: 'address' }], outputs: [] }
];
```

### FeePool

```javascript
const feePoolAbi = [
  { name: 'getUnpaidRewards', type: 'function', inputs: [{ name: 'user', type: 'address' }], outputs: [{ type: 'uint256' }], stateMutability: 'view' }
];
```

## See Also

- [erc20](../erc20/) - For token approvals and transfers
- [privy-wallet](../privy-wallet/) - For wallet setup
