---
name: galleon-ondo-assets
description: "Use when reviewing Ondo Stocks, OUSG or USDY access, quotes, token identity or redemption settlement; keep each product and jurisdiction separate."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Ondo product access and settlement

## Select the exact product

Resolve issuer/product, chain, token, account/entity, action, amount and settlement currency. Ondo Stocks, OUSG and USDY have different eligibility, legal claims, APIs and exit terms. Never infer approval for one from ownership of another. Public research can proceed without an account; access decisions must come from current issuer records rather than an agent's legal inference.

Record current issuer terms, product deployment, token standard, custody/backing reports, NAV/quote timestamp, fees, minimums and transfer restrictions. EVM ERC20 and Solana Token-2022 integrations need chain-specific interfaces. Self-custody of a token does not imply direct custody or identical shareholder rights in its underlying asset.

## Follow the selected branch

**Stocks:** with already authorized API access, use official read endpoints such as `GET https://api.gm.ondo.finance/v1/assets/prices/{symbol}` and the documented non-binding soft-quote route `POST /v1/attestations/soft`. Read the live schema for amount units, supported symbols/currencies and wallet/counterparty requirements. Keep `x-api-key` in the user's secret environment, never the report. A binding `POST /v1/attestations` is a consequential preparation step: preserve action, permitted wallet, attestation ID, expiry and payload, and request it only within actual transaction authority. Do not call it as a connectivity probe.

**OUSG:** read current qualified-access status and instant/non-instant route limits. Instant USDC redemption is atomic only when that route is available and within its current limits. Non-instant settlement follows issuer processing and business-day cutoffs; record request and actual payment separately. Do not promise a date solely from a typical processing window.

**USDY:** verify the specific offering, supported chain, onboarding, transfer restrictions and issuer redemption route. Do not reuse OUSG minimums or Stocks attestation payloads. Secondary-market availability does not prove direct redemption eligibility.

## Produce a usable decision

Compare gross proceeds, fees, minimums, expiry and expected settlement form for the chosen size. Identify remaining issuer approval or liquidity evidence. Do not upload identity documents, contact an issuer or request a binding attestation merely to complete a research report.

Synthetic example:20 OUSG at an observed 105-USDC NAV gives 2,100-USDC gross value. If the current verified instant minimum is 5,000, that route fails this size even though gross value is known. Report the failed minimum and inspect the user's eligible alternative; do not enlarge the redemption or reuse a Stocks soft quote. These numbers are illustrative, not current product terms.

If an attestation expires, first reconcile whether it was consumed or a transaction was submitted. Refresh terms only within the same authorized scope. API success and quote issuance are not minting, settlement or investor approval.

## Completion evidence

Return product/chain/token, issuer-access status, source dates, amount scales, quote/NAV, exact route, restrictions and decision. For authorized execution, retain request/attestation and transaction identity, then require actual token and payment settlement evidence. Never bypass restrictions through another wallet/frontend; research and skill installation confer no financial or legal authority.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
