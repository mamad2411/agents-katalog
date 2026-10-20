# ShieldAgent Skill

Autonomous DeFi smart contract vulnerability scanner.

## Usage

```bash
shield-agent scan <address>
shield-agent monitor <address> --interval 3600
shield-agent report <scan_id>
```

## Integration

This skill integrates with EvoClaw's agent runtime and ClawChain's
`pallet-agent-receipts` for on-chain audit attestation.

Every scan result is recorded as an immutable receipt on ClawChain,
providing verifiable proof of security audits.
