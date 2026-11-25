---
name: megaeth-developer-skills
description: >
  MegaETH developer playbook for AI coding agents. Use when building dApps,
  smart contracts, protocol integrations, frontends, payments, agents, or
  debugging workflows on MegaETH. Covers network setup, RPC and Realtime API
  usage, Foundry deployment, MegaEVM gas and storage behavior, frontend
  patterns, canonical tokenlist usage, USDm, drand VRF, ERC-8004 agents,
  x402 payments, and protocol-specific developer and `mega moss` execution
  guidance including gTrade leveraged trading. Route MOSS wallet application
  integration to moss-wallet-sdk and MOSS CLI command mechanics to
  moss-wallet-cli.
---

# MegaETH Developer Skills

Use this skill for MegaETH application and protocol development. Keep the main
answer focused on the user's task, then read only the references that match the
work.

## Default Stack

| Layer | Default |
| --- | --- |
| Network | MegaETH mainnet `4326`, testnet `6343` |
| RPC | `https://mainnet.megaeth.com/rpc`, `https://carrot.megaeth.com/rpc` |
| Transactions | `realtime_sendRawTransaction` when receipt return without polling matters |
| Tooling | Foundry for contracts; MegaETH RPC for estimation; `mega-evme` for MegaEVM replay/debugging |
| Frontend | viem/wagmi or app-native EIP-1193 flows; use MOSS via `moss-wallet-sdk` |
| Tokens | Use `megaeth-labs/mega-tokenlist` for addresses and decimals |

## Operating Procedure

1. Classify the task: network/RPC, contract deployment, frontend integration,
   token/payment flow, protocol integration, debugging, or security review.
2. Read the matching reference before giving implementation details.
3. Be explicit about chain ID, RPC URL, token address/decimals source, gas
   estimation behavior, and whether the task needs MOSS wallet guidance.
4. For protocol integrations, keep protocol addresses, calldata, ABI
   signatures, and workflow recipes here. Route `mega moss` command safety and
   delegated-key permission mechanics to `moss-wallet-cli`.
5. Prefer official docs and canonical repos for current addresses and APIs.
   If an address or endpoint may have changed, tell the user to verify against
   the linked source.

## Guardrails

- Never hardcode token addresses or decimals without citing the tokenlist or
  protocol docs used.
- Do not assume Ethereum local simulation gas matches MegaETH. Use a MegaETH
  RPC for `eth_estimateGas` or reproduce with `mega-evme`.
- Prefer `realtime_sendRawTransaction` for new synchronous-submission code.
  The public gateway also supports `eth_sendRawTransactionSync` as a
  compatibility alias with the same parameters and receipt behavior.
- Keep protocol-specific app integration guidance and agent-operated MOSS CLI
  execution recipes in their separate protocol references. Use
  `moss-wallet-cli` for wallet command and permission mechanics.
- Use secure private-key handling for Foundry and scripts. Prefer keystores,
  environment variables, or external signers; never commit secrets.

## References

Read the relevant files:

- Network and endpoints: [references/network.md](references/network.md)
- RPC and standard methods: [references/rpc.md](references/rpc.md)
- Realtime API: [references/realtime-api.md](references/realtime-api.md)
- Foundry setup: [references/foundry.md](references/foundry.md)
- Contract deployment and patterns: [references/deploy-contracts.md](references/deploy-contracts.md)
- Gas model: [references/gas-model.md](references/gas-model.md)
- Storage model: [references/storage-model.md](references/storage-model.md)
- Local replay/debugging: [references/mega-evme.md](references/mega-evme.md)
- Frontend patterns: [references/frontend-patterns.md](references/frontend-patterns.md)
- Tokenlist usage: [references/tokenlist.md](references/tokenlist.md)
- USDm: [references/usdm.md](references/usdm.md)
- drand VRF: [references/vrf-drand.md](references/vrf-drand.md)
- ERC-8004 agents: [references/erc8004-agents.md](references/erc8004-agents.md)
- x402 payments: [references/x402-payments.md](references/x402-payments.md)
- Protocol directory: [references/protocol-directory.md](references/protocol-directory.md)
- Protocol-specific developer guidance: [references/protocols/](references/protocols/)
- Protocol-specific `mega moss` recipes: [references/protocols/moss-cli/](references/protocols/moss-cli/)
- Awesome MegaETH AI ecosystem index: [references/awesome-megaeth-ai.md](references/awesome-megaeth-ai.md)
- Testing: [references/testing.md](references/testing.md)
- Security: [references/security.md](references/security.md)
- Source links: [references/resources.md](references/resources.md)

## When To Switch Skills

- MOSS SDK, React, Smart Approvals, paymaster, backend verification, or Privy
  migration: use `moss-wallet-sdk`.
- Operating a local wallet through `mega moss`, creating delegated keys, or
  executing protocol actions with the CLI: use `moss-wallet-cli`.
- Auditing an existing MOSS integration before launch: use
  `moss-wallet-security-review`.
