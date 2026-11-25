# Smart contract audit pack

When user runs `/crypto-devkit:audit`, check:

## EVM
- Reentrancy (CEI pattern)
- `onlyOwner` / roles / timelock
- Oracle staleness & manipulation
- Proxy: storage collision, `initializer`
- External calls: return value checks

## Solana
- Account owner & signer
- PDA bump canonicalization
- CPI privilege escalation
- Rent-exempt closure

Output: markdown report `AUDIT.md` in project root.
