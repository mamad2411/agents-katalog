---
name: moss-wallet-sdk
description: >
  Build MOSS Wallet application integrations on MegaETH. Use when implementing
  or debugging the MOSS core SDK, React provider/hooks, wagmi connector, Smart
  Approvals and silent execution, paymaster sponsorship, backend SIWE/JWT
  verification, or Privy asset migration. Covers secure-context/passkey
  requirements, hosted wallet key boundaries, result-status handling, network
  constants, and routing to moss-wallet-cli for terminal delegated-key
  operation.
---

# MOSS Wallet SDK

Use this skill for application-side MOSS integrations. It is the semantic home
for the former core SDK, React, permissions, paymaster, server verification,
and Privy migration skills.

## Core Model

- The hosted wallet lives at `https://account.megaeth.com`.
- Apps never hold the user's passkey, root key, seed phrase, or Recovery Code.
- The core package exports `mega`; React apps can use
  `@megaeth-labs/wallet-sdk-react`; wagmi apps can use the MOSS wagmi
  connector.
- Transaction and signing methods return explicit statuses. Branch on the
  documented result and treat `cancelled` as neutral. Lifecycle/setup and read
  methods can still reject for configuration, transport, or input failures.
- Browser/passkey flows require a secure context and correct origin.

Read [references/behavioral-rules.md](references/behavioral-rules.md) before
changing wallet semantics, auth boundaries, sponsorship policy, permission
rules, or user-facing recovery copy.

## Install

Core SDK:

```bash
npm install @megaeth-labs/wallet-sdk
```

React:

```bash
npm install @megaeth-labs/wallet-sdk-react react@^19 react-dom@^19 @tanstack/react-query@^5
```

Server verification:

```bash
npm install @megaeth-labs/wallet-server-verify
```

## Minimal Core Flow

```typescript
import { mega } from '@megaeth-labs/wallet-sdk';
import { parseEther } from 'viem';

await mega.initialise({ network: 'mainnet', logging: 'error' });

const connected = await mega.connect();
if (connected.status !== 'connected' || !connected.address) {
  return;
}

const result = await mega.transfer({
  type: 'native',
  to: '0xRecipient',
  amount: parseEther('0.01').toString(),
});

switch (result.status) {
  case 'approved':
    break;
  case 'cancelled':
    break;
  case 'error':
    throw new Error(result.error ?? 'MOSS transfer failed');
}
```

## Task Routing

Read only the references needed for the user's task:

| Task | Reference |
| --- | --- |
| Core SDK lifecycle, methods, errors | [references/quickstart.md](references/quickstart.md), [references/lifecycle.md](references/lifecycle.md), [references/methods-reference.md](references/methods-reference.md), [references/error-handling.md](references/error-handling.md) |
| Cross-cutting wallet semantics | [references/behavioral-rules.md](references/behavioral-rules.md) |
| React provider/hooks/wagmi | [references/react.md](references/react.md) |
| Smart Approvals, `grantPermissions`, `silent: true` | [references/permissions.md](references/permissions.md) |
| Paymaster sponsorship | [references/paymaster.md](references/paymaster.md) |
| Backend SIWE/JWT verification | [references/server-verify.md](references/server-verify.md) |
| Privy asset migration | [references/privy-migration.md](references/privy-migration.md) |
| Security model | [references/security-model.md](references/security-model.md) |

## Scripts

Use bundled scripts when they match the task:

- `scripts/check-secure-context.mjs`: verify whether a URL/host is valid for
  WebAuthn/passkey account creation.
- `scripts/build-permission-policy.mjs`: build and validate Smart Approval
  payloads from JSON config.
- `scripts/sponsor-endpoint-snippet.ts`: read/adapt Express sponsorship
  endpoint skeleton.
- `scripts/siwe-verify-snippet.ts` and `scripts/jwt-verify-snippet.ts`:
  read/adapt backend auth examples.
- `scripts/build-migration-plan.mjs`: build a Privy-to-MOSS asset migration
  transfer plan.

## When To Switch Skills

- MegaETH network, contract, protocol, frontend, or tokenlist development:
  use `megaeth-developer-skills`.
- Terminal wallet operation, delegated keys, `mega moss`, or protocol
  execution through the CLI: use `moss-wallet-cli`.
- Auditing an existing MOSS integration: use `moss-wallet-security-review`.
