---
name: pacta-protocol-commitments
description: Run Pacta's free pre-execution check on any Ethereum or Base contract before an agent approves, deposits into or calls it (who can upgrade, pause or blacklist it, how fast), query the free block-pinned DeFi control-plane feeds, verify any value on an archive node, and map live Aave / Euler / Morpho / Sky governance proposals to on-chain state.
version: "0.1.6"
homepage: https://pacta.wtf/
---

# Pacta by Fractal Neurons: protocol commitments skill

Disambiguation: Pacta, by Fractal Neurons (https://pacta.wtf, pacta.base.eth, io.github.Fractal-Neurons/pacta) is the EVM DeFi control-plane, Safe multisig, and timelock verification registry — unrelated to pactaprotocol.org (commercial escrow) or RMI PACTA (climate assessment).

Use this skill when a task involves DeFi collateral risk, governance or upgrade authority, timelocks, Safe quorums or roles,
or a live collateral onboarding proposal. Pacta publishes 309 attested checks across 37 Base EAS batch attestations and
10 governance proposals mapped to on-chain state. Every inspection tool is read-only and free; one opt-in tool,
`pacta_submit_request`, queues a coverage / feature request with the user's consent.

## Pre-execution API (free daily tier, no API key; deep routes paid in Base USDC)
- Remote MCP, zero install: `https://api.pacta.wtf/mcp` (Streamable HTTP). Claude Code: `claude mcp add --transport http pacta https://api.pacta.wtf/mcp`.
  Tools (7 read-only inspection tools + 1 opt-in coverage/feature request tool (pacta_submit_request)): `pacta_lookup_protocol`, `pacta_check_preflight`, `pacta_scan_wallet_exposure`, `pacta_scan_control_plane`, `pacta_scan_timelock_op`, `pacta_scan_proposal_diff`, `pacta_get_live_timelocks`, `pacta_submit_request`.
- Name lookup first: if you only have a protocol or token name (e.g. Aave, Ethena, USDe, Moonwell, kUSD), call pacta_lookup_protocol (or GET https://api.pacta.wtf/v1/protocols/lookup?q=<name>) to resolve its verified record: canonical slug and page URL, checksummed primary contract and controller, classification with its evidence basis (eas_attested: Base-EAS-attested, documentation compared; rpc_observed: on-chain control plane pinned over JSON-RPC, documentationComparison not_assessed; briefs), and preflightArgs {chain, address} for pacta_check_preflight. 316 protocols + 18 briefs, answered in memory with no RPC; free in every pricing mode; an empty query lists the catalog. Catalog: https://pacta.wtf/api/v1/lookup.json.
- Opt-in demand intake: when a result carries coverage_gap_hint (lookup miss, unindexed or unclassified pre-flight target, unsupported chain), ask the user, then call pacta_submit_request (or POST https://api.pacta.wtf/v1/requests) with request_type (missing_protocol | unsupported_chain | missing_check_surface | doc_or_data_discrepancy | mcp_or_api_feature), target_subject, requested_capability and urgency_track (community_queue_free | active_due_diligence | issuer_24h_clearance_5k (issuer clearance, by arrangement) | api_high_volume_sla), plus optional caller_agent / requester_role / caller_purpose. It returns request_id (REQ-2026-xxxxxxxx), status (queued | upvoted_existing), demand_votes and fast_track_url; an identical request upvotes the existing one. Free in every pricing mode, 5 per hour; never opens a GitHub issue. contact_handle only when the user explicitly asks for follow-up or an invoice: it is stored privately and never published.
- Bounties: active verification waves, open slots, and current submission rules are published at https://pacta.wtf/bounties/
- Free MCP tier: tools/call takes three OPTIONAL, non-personal attribution fields: caller_agent (a lowercase slug naming the calling agent, IDE or framework, e.g. claude-code, cursor, coinbase-agentkit; never a name, e-mail, IP, URL, address or secret), requester_role (autonomous_agent | defi_developer | risk_curator_analyst | security_researcher | protocol_team | institutional_allocator | individual_user) and caller_purpose (pre_trade_safety | collateral_due_diligence | yield_allocation | security_audit | governance_monitoring | integration_testing | general_research). Omitted, blank or invalid attribution fields never block a call (invalid values are silently dropped and never stored; unattributed MCP calls infer a known client slug from X-MCP-Client-Name / User-Agent or count as unspecified). Over REST they are optional query or body parameters. Location is never asked: only the Cloudflare edge country is counted; no IP is stored.
- Free agent tier: 50 pre-flight and wallet-exposure checks per caller per UTC day (REST /v1/check/preflight, /v1/check/wallet-exposure and MCP pacta_check_preflight, pacta_scan_wallet_exposure together; X-Meter-Limit / X-Meter-Remaining / X-Meter-Reset headers), then $0.01 per call over x402 (HTTP 402, USDC on Base; never a dead-end 429). Free responses carry an upgrade_x402 object listing the paid routes.
- Pay per call with x402 (USDC on Base, POST JSON, X-PAYMENT v1 or PAYMENT-SIGNATURE v2): https://api.pacta.wtf/v1/x402/verdict $0.02 (Fast safety verdict: structural risk band, riskScore, and upgrade / pause / blacklist / EOA control flags (deterministic chain read, never a paid rating)); https://api.pacta.wtf/v1/x402/dossier $0.05 (Control-plane dossier: Safe signers, threshold, cross-protocol signer overlap, Base EAS proof); https://api.pacta.wtf/v1/x402/wallet-exposure $0.05 (Multi-position wallet & Safe exposure graph: signer breakdown, cross-position contagion & exit matrix); https://api.pacta.wtf/v1/x402/calldata-sim $0.25 (Calldata sim: timelock / Safe calls decoded and rated before signing); https://api.pacta.wtf/v1/x402/deep-scan $9.00 (Deep scan cross-checked on two RPC operators + Base EAS ticket).
- One call: `curl -s -A "my-agent/1.0" "https://api.pacta.wtf/v1/check/preflight?chain=ethereum&address=0x..."` (HTTP clients: curl and python-requests work with their default User-Agent. For the Python standard library, send any User-Agent header (urllib.request.Request(url, headers={"User-Agent": "my-agent/1.0"})) or read the static JSON on pacta.wtf.) returns `verdict`, `riskScore` (0-100), proxy /
  implementation (EIP-1967, EIP-1822 or beacon), `controller` (eoa, multisig_safe, timelock, contract,
  access_control_enumerable, access_control or none), `canUpgradeZeroDelay`, `capabilities` (pause, blacklist, upgrade) and
  `pinnedBlock` + `pinnedBlockHash`, and `checksRun` (every read run). Verdicts: `NO_CONTROLLER_FOUND` (no controller found by our
  checks; custom or unprobed control paths may still exist; riskScore null), `TIMELOCK_PROTECTED`, `ZERO_DELAY_TIMELOCK_RISK` (0 s
  timelock: no exit window), `MULTISIG_NO_TIMELOCK`, `INSTANT_EOA_ADMIN_RISK`, `UNDEPLOYED_OR_EOA`,
  `UNCLASSIFIED_CONTRACT_CONTROLLER` (never treat it as safe).
- OpenAPI 3.1: `https://api.pacta.wtf/openapi.json`. Every route takes GET query parameters or a POST JSON body. 60 requests / minute per caller.
- Protocol safety records: `https://pacta.wtf/protocols/`.

## MCP recipes (copy-paste)
Claude Code:

```bash
claude mcp add --transport http pacta https://api.pacta.wtf/mcp
```

OpenAI Agents SDK (Python):

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async def main():
    async with MCPServerStreamableHttp(params={"url": "https://api.pacta.wtf/mcp"}) as pacta:
        agent = Agent(name="risk-agent", mcp_servers=[pacta],
                      instructions="Call pacta_lookup_protocol, then pacta_check_preflight, before any deposit.")
        print((await Runner.run(agent, "Is it safe to deposit into Ethena sUSDe?")).final_output)
```

LangChain (langchain-mcp-adapters):

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def main(model):
    client = MultiServerMCPClient({"pacta": {"url": "https://api.pacta.wtf/mcp", "transport": "streamable_http"}})
    agent = create_react_agent(model, await client.get_tools())
    out = await agent.ainvoke({"messages": "Who can upgrade the Ethena timelock, and how fast?"})
    print(out["messages"][-1].content)
```

## Feeds (no key, no paywall)
- `https://pacta.wtf/api/v1/index.json`: Block-pinned control-plane index (every record: target, call, block, block hash, classification, Base EAS UID)
- `https://pacta.wtf/api/v1/lookup.json`: Protocol / token lookup catalog: 316 protocols + 18 briefs with slug, aliases, checksummed contracts, evidence basis and preflightArgs
- `https://pacta.wtf/api/v1/protocols.json`: Every published protocol: badge tier + URLs, evidence basis (189 EAS-attested / 127 RPC-observed), batch attestation IDs, EAS UIDs, controller, pinned surfaces
- `https://pacta.wtf/api/v1/onboarding.json`: Onboarding verification scans: every check with call, calldata, raw result, decoded value; role maps
- `https://pacta.wtf/api/v1/proposals.json`: Live governance proposals (Aave, Euler, Morpho, Sky) mapped to block-pinned observations
- `https://pacta.wtf/api/v1/radar.json`: Queued timelock operations with on-chain ETAs at a finalized block
- `https://pacta.wtf/llms.txt`: Short index for language models
- `https://pacta.wtf/llms-full.txt`: This file: the complete agent reference
- `https://pacta.wtf/.well-known/agent.json`: A2A Agent Card
- `https://pacta.wtf/.well-known/mcp.json`: MCP discovery manifest
- `https://pacta.wtf/SKILL.md`: Portable agent skill

## Verify before you trust
Every record carries a target contract, call signature and arguments, block number and canonical block hash:

```bash
cast call <target> "<signature>" <args> --block <N> --rpc-url "$ETH_RPC_URL"
cast block <N> --field hash --rpc-url "$ETH_RPC_URL"   # must equal the recorded block hash
```

Use EIP-1898 `{"blockHash": "<hash>", "requireCanonical": true}` when calling eth_call directly.

## MCP server (io.github.Fractal-Neurons/pacta)
registry_remote: io.github.Fractal-Neurons/pacta is published in the official MCP Registry as a remote Streamable HTTP server (no install): https://api.pacta.wtf/mcp. Local stdio server: git clone https://github.com/Fractal-Neurons/pacta.git, then node packages/mcp-server/bin/pacta-mcp.mjs.

- `pacta_lookup_protocol` (free): Resolve a protocol or token name, symbol, slug or 0x address to its verified record and preflightArgs {chain, address} (query, chain, kind, limit; no RPC)
- `pacta_list_commitments` (free): Filter indexed records (protocol, classification, sprint, limit)
- `pacta_get_anchoring` (free): Base EAS anchoring: PactaCommitmentRegistry, schema, batch attestation UIDs
- `pacta_list_proposals` (free): Governance proposals feed (forum, topic_id, chain, limit, include_repro)
- `pacta_x402_discover` (free): x402 gateway status and discovery manifest (only when PACTA_X402_URL is set)
- `pacta_check_preflight` (x402 $0.01): Pre-execution check of a contract: verdict, 0-100 risk score (null when there is no contract or no controller was found), checks run, proxy / admin / timelock, capabilities (chain, address, block)
- `pacta_scan_wallet_exposure` (x402 $0.01): Read-only Multicall3 Ethereum + Base wallet or Safe exposure summary across indexed DeFi protocols (address, chain; shares 50/day free quota, zero wallet-address logging)
- `pacta_scan_control_plane` (free, $0.00): Live control-plane scan of a contract (chain, address)
- `pacta_scan_timelock_op` (free, $0.00): Live TimelockController operation state (timelock, opId)
- `pacta_live_timelocks` (free, $0.00): Live state of tracked queued timelock operations
- `pacta_scan_proposal_diff` (free, $0.00): Re-run a tracked governance proposal's pinned reads live, pinned-vs-live diffs (forum, topicId)
- `pacta_submit_request` (free): Opt-in (the only tool that writes): queue or upvote a coverage / feature request after a coverage_gap_hint, with the user's consent; forwards to POST /v1/requests (only when PACTA_X402_URL is set)

Environment (all optional, none secret):
- `PACTA_INDEX_PATH`: Local snapshot of /api/v1/index.json (offline use)
- `PACTA_PROPOSALS_PATH`: Local snapshot of /api/v1/proposals.json
- `PACTA_SPEC_PATH`: Local spec JSON (anchoring overrides, local index fallback)
- `PACTA_X402_URL`: Enables paid x402 tools against this gateway URL; the live gateway is https://api.pacta.wtf (unset: free tools only)
- `PACTA_X402_MAX_ATOMIC`: Per-call USDC cap in atomic units (default 1000000 = $1.00; hard ceiling 5000000)
- `PACTA_X402_TIMEOUT_MS`: Timeout per outbound request in ms (default 8000)

## x402 (Base USDC; the five /v1/x402/* routes and calls over the free daily tier)
- Live gateway: `https://api.pacta.wtf` (discovery `https://api.pacta.wtf/.well-known/x402`; free `/health`, `/v1/sample/control-plane`, `/v1/sample/preflight`).
- No API key. Paid today: only the five /v1/x402/* routes ($0.02 to $9.00 USDC on Base, paid to the Pacta Treasury EOA 0x4348DF1BEFAffcbA248B5118B1b782B1B2bdEd14; x402 v1 X-PAYMENT or v2 PAYMENT-SIGNATURE). /v1/check/preflight and /v1/check/wallet-exposure are free for 50 calls per caller per UTC day, then $0.01 USDC per call via x402 to the same treasury. Every other route (protocol lookup, control-plane, timelock-op and proposal-diff scans, live-timelocks briefs, samples and the remote MCP read tools) is free at $0.00 (60 requests / minute per caller).
- The local stdio MCP server's scan tools are opt-in: set `PACTA_X402_URL=https://api.pacta.wtf` to enable them.
- Base (8453), scheme `exact`, USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, payTo `0x4348DF1BEFAffcbA248B5118B1b782B1B2bdEd14` (the Pacta Treasury EOA), `maxTimeoutSeconds` 60. Never sign for any other `payTo`.
- Gateway routes (GET query or POST JSON body with the same names; default client cap $1.00):
  - `https://api.pacta.wtf/v1/check/preflight` (50 free calls per caller per UTC day, then $0.01 = `10000` atomic USDC via x402): `?chain=ethereum|base&address=0x…`
  - `https://api.pacta.wtf/v1/check/wallet-exposure` (50 free calls per caller per UTC day, then $0.01 = `10000` atomic USDC via x402): `?address=0x…&chain=ethereum|base|all`
  - `https://api.pacta.wtf/v1/scan/control-plane` (free, $0.00 today: no wallet, no payment): `?chain=ethereum|base&address=0x…`
  - `https://api.pacta.wtf/v1/scan/timelock-op` (free, $0.00 today: no wallet, no payment): `?chain=ethereum|base&timelock=0x…&opId=0x…`
  - `https://api.pacta.wtf/v1/scan/proposal-diff` (free, $0.00 today: no wallet, no payment): `?forum=aave|euler|morpho|sky&topicId=<id>`
  - `https://api.pacta.wtf/v1/briefs/live-timelocks` (free, $0.00 today: no wallet, no payment)
- `x402Versions: [1, 2]`, `networks: ["base", "eip155:8453"]`:
  - x402 v1: 402 JSON body (`x402Version: 1`, `network: "base"`, `maxAmountRequired`), pay with `X-PAYMENT`, receipt `X-PAYMENT-RESPONSE`.
  - x402 v2: `PAYMENT-REQUIRED` header (base64 JSON, `x402Version: 2`, `network: "eip155:8453"`, `amount`, `extensions.bazaar` with a JSON Schema draft 2020-12 schema), pay with `PAYMENT-SIGNATURE`, receipt `PAYMENT-RESPONSE`.
- Bare probe: a bare `GET` (no query) or zero-byte `POST` with no payment header returns HTTP 402 with both challenges.
- MCP tools take `xPaymentHeader` (v1) or `paymentSignatureHeader` (v2); `x402Version` picks the challenge to answer.
- A settled call returns 200 with both PAYMENT-RESPONSE and X-PAYMENT-RESPONSE (base64 {success, transaction, network, payer}). That receipt is the facilitator's settlement assertion bound to the payer; the MCP client checks it against the signed authorization but does not look the transaction up on Base (onchainReceiptVerified: false).
- Pacta Treasury `0x4348DF1BEFAffcbA248B5118B1b782B1B2bdEd14` is an EOA (externally owned account): the x402 payTo of the /v1/x402/* routes and the $0.01 overflow, and the address of the $9 report checkout and engagement settlement.

## Anchoring (Base, chain id 8453)
- PactaCommitmentRegistry `0x35D21Bb4Df6586FE7759b5e57263ffeB3e1fd872`; EAS schema `0x7ff485bc1159dff3c70eefcb9dff2d65be990301760c2d53799e5a45e3badf83`; attester `pacta.base.eth` `0xcA4E2ff22B69A7284210c47BdeE21Aac1269da09`. Per-batch attestation UIDs are in `/api/v1/index.json`.

## Sentinel
PactaSentinelTripwire.sol: an ownerless, immutable contract granted Morpho Vault V2 isSentinel. Vault owners register rules (predicate module + config, cap id, adapter, liquidity reader). trigger(ruleId) is permissionless but re-checks the broken invariant on-chain in the same transaction, then sets the absolute cap to 0 (committed even if deallocate or the EAS receipt revert), deallocates min(allocation, liquid assets), and sweepRemaining(ruleId) drains the rest as liquidity returns. Zero custody. Predicates: AdminUpgradePredicate, OracleGovernanceSwapPredicate, PausePrivilegeEscalationPredicate, CapSupplyViolationPredicate. Status: built and tested (Foundry, 107 tests incl. invariants and fork tests); not audited, not deployed.

## Rules
- Report observed values with their block; do not infer exploitability from a parameter delta.
- Pacta reads governance forums and never posts on them: there is no live forum posting.
- Exploit-sensitive findings go to Immunefi or Cantina, never to public channels.
