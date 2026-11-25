---
name: galleon-openeden-tbill
description: "Use when assessing OpenEden TBILL eligibility, subscriptions, whitelisted transfers or queued USDC redemption and fund settlement evidence."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# OpenEden TBILL subscription and redemption

## Identify issuer and requested action

Resolve product/share class, supported chain, TBILL vault/token, investor entity, whitelisted wallet, amount/unit and USDC settlement address. TBILL represents an economic fund claim with offchain custody; holding tokens is not direct ownership of Treasury bills. Read current issuer onboarding and terms, not an old launch announcement.

Record actual issuer approval/whitelist evidence without collecting identity documents in an agent artifact. Professional/accredited status and jurisdictional access are issuer decisions. Never infer eligibility from a public wallet balance, location or another permissioned token.

## Read the backing and token state

Use current official contract-address documentation and verified deployment ABI for token balance/decimals, vault identity, transfer access, price/NAV, pauses and supported subscription/redemption methods. Do not assume a generic ERC-4626 API: use the product's documented contract or app interface. Compare onchain balances, NAV reports and custody attestations with their own dates and scopes. One does not prove all the others.

For subscription, confirm issuer-approved source wallet, USDC mint/address, current first/subsequent deposit minimum, fees and current minting terms. A USDC approval is not a subscription, and sending directly to a remembered contract address is not a safe discovery step.

For transfer, verify the recipient's whitelist/access status before preparing an unsigned payload. Do not switch recipients to evade a restriction.

## Assess a redemption

1. Read the current minimum, fee and queue rules for this investor/product. Convert requested TBILL shares using a dated NAV only as an estimate.
2. Preserve the actual redemption request ID/hash, owner, shares burned, queue position/status and USDC receiver. Price and transaction fee are determined at processing in the documented flow, so requested gross value is not locked proceeds.
3. Treat typical next-US-business-day processing as an estimate. Holidays, queue/liquidity and issuer processing can change timing; a burn event does not prove USDC arrived.
4. Reconcile actual payout with processed NAV, fee and token balance. A pending request is a distinct receivable, not an additional wallet token holding.

## Worked decision

Synthetic 10,000 TBILL processed at 1.05 USDC gives 10,500 gross. A verified 5-bps redemption fee on that gross is 5.25, leaving 10,494.75 USDC. Before processing,1.05 and 5 bps are only scenario inputs; do not promise that payout or exact settlement date. If the recipient is not whitelisted, the action is not ready even if this arithmetic is complete.

If an app shows requested while USDC remains absent, keep it pending and investigate the exact queue/request. If a transaction timed out, inspect its original hash and issuer status before another request; duplicate burns are not a recovery strategy.

## Completion evidence

Return product/deployment, issuer eligibility, source dates, current terms, estimated versus processed amounts, queue identity and missing evidence. Research grants no subscription, transfer or identity-sharing authority. For separately authorized execution, require successful request/settlement evidence and actual USDC receipt at the agreed wallet before calling redemption complete.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
