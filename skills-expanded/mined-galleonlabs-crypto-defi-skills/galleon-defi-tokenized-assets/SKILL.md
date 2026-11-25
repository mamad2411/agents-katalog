---
name: galleon-defi-tokenized-assets
description: "Use when researching tokenized Treasury or securities eligibility, custody, subscriptions, transfers and redemption settlement for Ondo and OpenEden."
license: MIT
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Tokenized assets

Start with the legal product and issuer claim, then the token. A public blockchain interface or transferable balance does not establish eligibility to subscribe, hold, transfer or redeem. This skill is a research and settlement procedure, not legal advice, an issuer onboarding service or a signer.

Read [providers](references/providers.md) for the exact product. Use [workflows](references/workflows.md) for eligibility/settlement records and evaluation cases.

## Start with the requested task

Use supplied preferences and compatible tools for this request; ask only for missing terms that change its result. Public research needs no wallet. Preferences and tool access never grant financial authority.

## Workflow

1. Identify issuer, product/share class, jurisdictional offering, chain and token address, account/entity, requested action and settlement currency. Keep Ondo Stocks, USDY, OUSG and OpenEden TBILL separate; one product's access rules do not transfer to another.
2. Verify current issuer documentation for investor eligibility, KYC/KYB/KYT, wallet whitelisting, transfer restrictions, permitted recipients, fees, minimums, redemption windows and custody/legal claim. Treat eligibility as unknown until the issuer confirms it; do not infer nationality or status from a wallet or location.
3. Research NAV and its timestamp, quoted market price, backing/custodian reporting, fees and available liquidity. Separate token settlement, issuer redemption and bank/business-day settlement. Do not equate Treasury backing, ratings, or attestations with guaranteed principal or immediate cash availability.
4. If the user requests and qualifies for a transaction, use the issuer's documented interface and credentials kept outside context. Distinguish indicative quotes from binding attestations/orders; even an offchain request may consume a limit or create an obligation. Review price, notional, fee, chain, approved address, expiry and issuer terms before requesting a binding operation.
5. Prepare the concrete unsigned onchain sequence when supported and simulate it. Preserve authorization scope; onboarding documents, identity submission, binding quotes, token approvals, signatures, purchases and transfers are distinct actions. Obtain missing authorization at the applicable step without treating research as consent. Use the chosen signer; do not collect seed phrases or retain identity documents in artifacts.
6. Reconcile quote/attestation ID, approval, signature, transaction submission, receipt, token/NAV indexing, redemption request and actual settlement independently. A burned token or accepted request does not prove bank/USDC proceeds arrived. On ambiguity, query the known order/request/hash before retrying a binding action.

## Deliverable

Return exact product and source dates, confirmed versus unknown eligibility, legal/custody structure, access/tooling status, price/NAV and cost basis, settlement stages and outstanding evidence. If issuer access is unavailable, provide the research and concrete prerequisites; do not invent an API, bypass geographic restrictions or connect a third-party MCP as though it were official.

## Worked comparison

Synthetic observations below illustrate the decision; they are not live quotes or receipts.

**Request:** Compare redeeming 10,000 USD of these products by Friday. Eligibility is already confirmed.

**Available evidence:** Synthetic current issuer terms: A costs 15 USD total and settles Wednesday; B costs 5 USD total and settles next Monday. Same USD valuation basis, no other charges, confirmed eligibility and cutoff compliance supplied.

**Read sequence:** Read current issuer eligibility, claim structure, redemption fees, cutoff/calendar and settlement destination; compare net proceeds against the actual deadline.

**Completed answer:** A yields 9,985 USD on Wednesday and meets Friday. B yields 9,995 USD next Monday and misses it. Choose A for the deadline; the extra 10 USD buys the evidenced earlier settlement. Issuer terms establish expected settlement, not a completed redemption.

**Changed evidence:** A issuer calendar now marks Wednesday settlement suspended, with no replacement date.

**Useful response:** Report A timing unknown and B too late; neither has evidenced Friday settlement. Keep fee comparison, identify the missing issuer settlement date and avoid suggesting a secondary-market quote guarantees redemption.

Fetch a missing observation through an existing compatible read tool when available; otherwise return the supported partial result and exact gap. Reconcile an uncertain write through its original identity before considering a retry.

## Focused protocol procedures

For a named protocol task, load its focused skill when installed. Discover it by name; this comparison workflow remains usable without sibling files.

- `galleon-ondo-assets`: reviewing Ondo Stocks, OUSG or USDY access, quotes, token identity or redemption settlement; keep each product and jurisdiction separate.
- `galleon-openeden-tbill`: assessing OpenEden TBILL eligibility, subscriptions, whitelisted transfers or queued USDC redemption and fund settlement evidence.
