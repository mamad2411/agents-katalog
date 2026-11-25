---
name: payment-processor-exchange
description: Generate NFT marketplace exchange integration code using Payment Processor V3 -- order signing, listing and buying NFTs, accepting offers, calldata encoding, filling, sweeping collections, cancellation, PermitC. Use for any ERC-721 or ERC-1155 buy/sell/trade flow.
user-invocable: true
disable-model-invocation: true
argument-hint: "[description of exchange integration requirements]"
---

# Payment Processor Exchange Integration Generator

## Project Setup

Before generating code, check the user's project is configured:
1. **Foundry**: `foundry.toml` must exist. If not: `forge init`
2. **Payment Processor** (optional): `forge install limitbreakinc/payment-processor` for direct interface imports. Otherwise, scripts use inline interface definitions with the deployed contract addresses.
3. **Local testing**: For local development, use `apptoken-dev` to bootstrap an Anvil node with all Apptoken protocols at their deterministic addresses -- see `apptoken-general/references/project-setup.md`.

## Instructions

1. Parse the exchange integration requirements from `$ARGUMENTS`.
2. **Resolve ambiguities before generating** -- if $ARGUMENTS mentions specific collections or tokens without addresses, or the order type (listing vs offer, standard vs PermitC, single vs bulk) isn't clear from context, ask in a single message. If clear, proceed.
3. Determine the order types needed:
   - Listings (single, bulk, sweep)
   - Item offers
   - Collection offers
   - Token set offers
   - Bulk orders (merkle tree signing)
   - Partial fills (ERC1155)
4. Generate integration code covering:
   - EIP-712 order signing with the correct typehash
   - Calldata encoding via the **PaymentProcessorEncoder** at `0x9A1D00C3a699f491037745393a0592AC6b62421D`
   - Proper struct construction for `Order`, `SweepOrder`, `AdvancedOrder`, etc.
5. Handle advanced features as needed:
   - **Cosigner security:** Short-lived cosignatures for order-book protection
   - **PermitC:** Time-bound approvals without `setApprovalForAll`
   - **Bulk orders:** Merkle tree signing for 2-1024 orders in a single signature
   - **Partial fills:** ERC1155 orders with `requestedFillAmount` and `minimumFillAmount`
6. **Key detail:** All trade functions on PaymentProcessor accept a single `bytes calldata data` parameter. This calldata is produced by the Encoder contract (called off-chain or on-chain).
7. The **executor** (`msg.sender` on PaymentProcessor) is always the **taker** of the trade.

## Reference Files

- `references/order-signing.md` -- EIP-712 signing, typehashes, nonces, and bulk orders
- `references/order-filling.md` -- Trade function reference, calldata encoding, cancellation, and read-only functions
- `references/permitc-integration.md` -- PermitC integration for time-bound approvals
- Protocol knowledge: `payment-processor-protocol`

## Common Mistakes

- **`beneficiary` for listings must be the buyer** -- For listings, `beneficiary` determines who receives the NFT and is set at fill time (it is NOT part of the signed SaleApproval typehash). Setting it to the seller's address causes the NFT to transfer back to the seller. For offers, `beneficiary` IS signed by the buyer and determines where the NFT goes.
- `revokeMasterNonce()` is called directly on PaymentProcessor with no parameters and no encoder -- it increments the caller's nonce by 1, invalidating ALL previously signed orders
- Cosigned orders (`nonce = 0`) cannot be cancelled on-chain -- cancellation is done off-chain by stopping cosignature issuance
- The PP and Settings Registry both emit `UpdatedCollectionPaymentSettings` events with DIFFERENT signatures -- indexers must listen on both contracts

## Related Skills

- **payment-processor-creator** -- Configure creator payment settings, pricing, and royalties before trading
- **permitc-protocol** -- PermitC fundamentals (approvals, signing, nonces) used for time-bound NFT listings
- **apptoken-general** -- ERC-721C/ERC-1155C token standards and ecosystem overview
