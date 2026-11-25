---
name: tdm-daos-agent
description: >
  Handle the current public TDM DaOS payment contract and recovery guidance.
  Use when a TDM service returns HTTP 402 from POST /authorize, when the user
  needs help with Session Gas Tank behavior, or when the user should be guided
  toward tdm connect, tdm fuel, tdm sweep, or tdm cashout.
metadata:
  author: ToDealMarket
  version: 0.1.0
  sdk-package: tdm-sdk
  target-agents:
    - claude
    - claude-code
    - api-agents
---

# TDM DaOS Agent

TDM DaOS Agent is the agent guidance layer inside TDM DaOS. Treat the TDM SDK npm
package and Contour Runtime as the canonical product surface; this skill only explains
agent-facing payment interpretation, recovery, and safe next actions.

## Use this skill for

- HTTP 402 responses from `POST /authorize`
- `billingMode`, `settlementMode`, `paymentOptions`, and `retryEndpoint`
- current JS helper names such as `makePayable(...)`, `createFetchHookClient(...)`, `createAuthorizeClient(...)`, `createGatewayClients(...)`, `createSessionTanksClient(...)`, and `createCheckoutClient(...)`
- framework-mode charge helpers: `charge(...)`, `chargeFetchHandler(...)`, `chargeExpressHandler(...)`, `chargeHonoHandler(...)`, `chargeNextHandler(...)`, `chargeElysiaHandler(...)`, `chargeDenoHandler(...)`
- session recovery using `tdm_get_session_state`
- runtime discovery using `tdm_capability_list`
- plugin, contour, budget, and gated memory guidance through current MCP tools
- `session_gas_tank` guidance
- sweep vs cashout clarification
- agent vault command guidance
- agent-first paid execution guidance for tools, APIs, routes, and runtime actions

## Read only what you need

- Read [references/adaptation-map.md](references/adaptation-map.md) for older terminology and draft wording.
- Read [references/authorize-contract.md](references/authorize-contract.md) for current public fields and endpoints.
- Read [references/mcp-runtime.md](references/mcp-runtime.md) for state-based recovery guidance.
- Read [references/sdk-sweep-capabilities.md](references/sdk-sweep-capabilities.md) before suggesting sweep flows.
- Read [references/vault-scenarios.md](references/vault-scenarios.md) for agent vault and cashout guidance.

## Hard rules

1. Do not invent undocumented payment fields.
2. Prefer exact current fields: `allowed`, `authorizationId`, `charged`, `balanceMinor`, `priceMinor`, `billingMode`, `settlementMode`, `paymentOptions`, and `retryEndpoint`.
3. Use `tdm_capability_list` to discover the MCP surface when available.
4. Use `tdm_get_session_state` before asking the user for money.
5. If the state is `UNINITIALIZED`, instruct the user to run `tdm connect`.
6. If the state is `DEPLETED` and dust is available, prefer `tdm sweep`.
7. If the state is `DEPLETED` and no dust is available, suggest `tdm fuel`.
8. Do not describe `tdm sweep` as a cashout.
9. Do not suggest `tdm cashout` as a way to satisfy an active payment challenge.

## Recommended operator commands

- `tdm vault create <name> [--use]`
- `tdm vault use <name|default>`
- `tdm connect`
- `tdm login --gateway https://tdm.todealmarket.com` (advanced/manual only)
- `tdm fuel --amount <usd> --yes`
- `tdm sweep --network solana --resume-burner --deposit-address <solana_address>`
- `tdm sweep --network solana --resume-burner --target-agent <name>`
- `tdm sweep --network base --project-id <walletconnect_project_id> --treasury <base_address>`
- `tdm sweep status`
- `tdm cashout`
- `tdm agent list`
- `tdm agent boot <name>`
- `tdm agent status <name>`
- `tdm mcp`
- `tdm mcp serve`

## Named vault guidance

- Prefer one named vault per business contour when operators manage many agents.
- For larger fleets, prefer multiple named vaults over one giant vault.
- If the operator uses named vaults, respect their active vault or explicit `--vault <name>` choice.

## Product framing guidance

- Treat TDM as DaOS-first: Contour Runtime + TDM Hub + AgentPay/Gateway.
- Treat AgentPay as guidance inside DaOS, not as the whole product.
- Default mental model: price a protected call, authorize it, then continue execution.
- Mention file, note, or content unlock flows only as an additional layer on top of the core agent/runtime payment surface.

## Bundled helpers

- [scripts/fetch_x402_price.mjs](scripts/fetch_x402_price.mjs)
- [scripts/run_tdm_sweep.mjs](scripts/run_tdm_sweep.mjs)
