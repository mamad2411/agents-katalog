---
name: chainanalyzer-aml
description: Blockchain AML and sanctions screening for crypto addresses and transactions across 12 chains (BTC, ETH, Polygon, BNB Smart Chain, Base, Arbitrum, Optimism, Avalanche, Solana, Kaia, TRON, XRP) via the ChainAnalyzer MCP server. Use when the user asks whether a wallet or transaction is risky, sanctioned, linked to scams, mixers or hacks, wants due diligence / KYT on a counterparty address, needs to trace where funds went (including cross-chain bridges), or must screen a list of addresses for compliance.
license: MIT
metadata:
  author: refinancier, inc.
  homepage: https://chain-analyzer.com
  mcp-server: chainanalyzer-mcp (npm)
---

# ChainAnalyzer AML skill

This skill tells the agent when and how to use the `chainanalyzer-aml` MCP server tools.
It does not replace a compliance officer: results are risk indicators with on-chain evidence,
not legal determinations.

## Prerequisites

The MCP server `chainanalyzer-aml` must be configured. If its tools are not available, tell the user:

```json
{
  "mcpServers": {
    "chainanalyzer-aml": {
      "command": "npx",
      "args": ["-y", "chainanalyzer-mcp"],
      "env": { "CHAINANALYZER_API_KEY": "tfk_..." }
    }
  }
}
```

Authentication is one of:

- `CHAINANALYZER_API_KEY` (`tfk_...`). Preferred. API keys are available on every plan, including Free
  (10 scans/month): sign up at https://chain-analyzer.com/login?utm_source=skill and create a key under
  Account → Settings → API Keys (https://chain-analyzer.com/account/settings/api_keys).
- `X402_PRIVATE_KEY` for pay-per-request USDC on Base via x402, no account needed. The server pays each call
  automatically; no extra install. `X402_MAX_USD_PER_CALL` (default `1.00`) caps one payment, so `batch_screening`
  ($2.50) needs it raised to `2.50` or more. The paying address must not have an EIP-7702 delegation (a delegated
  address can fail the USDC signature check and the payment is rejected).
- A call refused by the per-call limit, or a payment the server rejects, is not charged. Relay the error text
  (it carries the server's reason and hint) and let the user decide.

### If a call fails with an auth or payment error

- `401` / `403` (missing, invalid or revoked key): stop and tell the user to create a key at the link above.
  Do not retry with guessed keys.
- `402 Payment Required` (x402 mode without a funded wallet, or API-key mode where the key is absent):
  explain the two options (free API key vs. x402 wallet) and let the user choose. Never ask for or echo
  private keys in the conversation.
- `429` (monthly quota or per-minute rate limit): report which limit was hit and suggest upgrading or
  waiting. Rate limits by plan: Free 10/min, Starter 30/min, Pro 60/min, Business 120/min, Enterprise 300/min.

## Tool selection

| Need | Tool | Cost (x402) |
| --- | --- | --- |
| Is this address sanctioned (OFAC / EU / UK / UN / JFSA / ScamDB)? | `sanctions_check` | $0.05 |
| Did this address receive stolen funds from a known hack (e.g. Binance 2026), and how many hops from the attacker? | `hack_exposure_lookup` | $0.05 |
| Is this address frozen by a stablecoin issuer (USDT / USDC / JPYC)? | `freeze_status` | $0.02 |
| Screen a list of deposit addresses against known hacks at once (up to 50) | `hack_exposure_batch` | $1.00 |
| How risky is this address? Score, detections, ML anomaly | `check_address_risk` | $0.10 |
| Where did this transaction's funds come from / go to? | `trace_transaction` | $0.30 |
| Is this Bitcoin tx a CoinJoin? (`is_coinjoin`, `mixer_type`, input / output counts, equal-value output groups) | `detect_coinjoin` | $0.10 |
| Which other addresses are controlled by the same actor? | `cluster_wallet` | $0.25 |
| Screen a list (up to 50) | `batch_screening` | $2.50 |
| Follow funds across bridges (NEAR Intents, Wormhole, Stargate, Across, deBridge, Hop, Synapse) | `bridge_flow_trace` | $0.50 |

Costs apply only in x402 mode. In API-key mode each call consumes one scan from the plan quota (Free: 10/month; a batch consumes one scan per successfully screened address). Plan gates in API-key mode: `batch_screening` needs Starter or above (up to 50 addresses per call, 10 on Starter), `bridge_flow_trace` needs Business or above. A `403` from one of these means the plan is too low, not a bad key: say so and suggest the upgrade or x402.

## Workflow

1. **Identify the chain from the address format before calling anything.**
   - `bc1...`, `1...`, `3...` → `bitcoin`
   - `0x` + 40 hex → EVM. Ambiguous between Ethereum, Polygon, BNB Smart Chain, Base, Arbitrum, Optimism, Avalanche, Kaia. Use the chain the user named; if none, default to `ethereum` and say so.
   - Base58, 32–44 chars, no `0`/`O`/`I`/`l` → `solana`
   - `T` + 33 Base58 chars → `tron`
   - `r` + 24–34 Base58 chars → `xrp`
   - Never lower-case or otherwise normalize Base58 addresses (Bitcoin, Solana, TRON, XRP). Case is significant.
2. **Screen cheap first.** Run `sanctions_check`, then `check_address_risk`. A sanctions hit alone is sufficient to stop and report.
3. **Escalate only on signal or request.** Use `cluster_wallet`, `trace_transaction` or `bridge_flow_trace` when the risk level is medium or above, when detections mention mixers / bridges / drainers, or when the user explicitly asks to follow the money.
4. **Lists go through `batch_screening`** (≤50 per call). Split larger lists and de-duplicate first; duplicates are not re-charged by the service but waste a slot.
5. **Confirm before spending in x402 mode** when a single turn would cost more than about $1 (e.g. several traces or a batch).
6. Pass `lang: "ja"` on `check_address_risk` when the user writes in Japanese.

## Interpreting results

- `risk_level` is one of `safe` / `low` / `medium` / `high` / `critical`; `risk_score` is 0–100.
- `detections` list the rules that fired with evidence (counterparty, tx hash, amount). Quote the evidence, not just the rule name.
- `ml_anomaly_score` is an unsupervised signal. Treat it as corroboration, never as the sole reason for a conclusion.
- Sanctions sources are named per hit. OFAC SDN hits are the strongest; ScamDB hits are community / vendor intelligence and should be described as such.
- `bridge_flow_trace` returns `nodes` with roles (`solver` / `relay` / `user` / `exchange` / `bridge`) and `edges` with on-chain tx signatures. `same_intent_correlation` means the source and destination legs were matched by timing and amount, which is probabilistic.

## Report format

Keep the answer short and evidence-first:

1. One-line verdict: risk level, score, sanctions status.
2. Key detections with the specific evidence (tx hash, counterparty label, amount).
3. Recommended next step framed as an option for the user's compliance policy (monitor / enhanced due diligence / escalate), never as a decision to file a report.
4. The raw address, chain and scan timestamp so the result can be reproduced.

## Limitations

- `bridge_flow_trace` starts from EVM chains (Kaia included) or Solana only. It does not accept `bitcoin`, `tron` or `xrp`.
- `detect_coinjoin` is Bitcoin only and takes a transaction id, not an address.
- `freeze_status` covers Ethereum, Polygon, Avalanche and TRON. `hack_exposure_lookup` / `hack_exposure_batch` cover EVM chains, TRON, Solana and Bitcoin.
- Risk scores reflect public ledger data only. They do not include KYC data, Travel Rule messages or off-chain information.
- Do not present a `safe` result as a guarantee. Absence of detections is not evidence of legitimacy.
