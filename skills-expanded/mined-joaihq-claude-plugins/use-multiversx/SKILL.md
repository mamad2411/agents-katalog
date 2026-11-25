---
name: use-multiversx
description: Use the MultiversX JoAi app plugin when the task needs MultiversX tools or workflows.
---

# MultiversX

Connect MultiversX to Claude, Codex, and ChatGPT. Check balances, view transactions, manage staking, and interact with ESDT tokens through natural language.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- What is the EGLD balance of erd1...?
- Show my staking delegations.
- View details for token WEGLD-bd4d79.

## Action Inventory

- `multiversx-account-guardian-data` (collect) — View guardian (2FA) information for a MultiversX blockchain account. Check if an account is protected by guardian security, view active guardian addresses, pending guardian activations, activation epochs, and service UIDs. Essential for security verification and account protection status.
- `multiversx-account-info` (collect) — View comprehensive account information for a MultiversX blockchain account. Get the account balance in eGold (EGLD), transaction nonce, username, and all account details in one place. Perfect for checking wallet status, balance verification, and account overview.
- `multiversx-account-nfts` (collect) — View all NFTs owned by a MultiversX blockchain account. See your complete NFT collection including identifiers, names, collections, nonces, creators, royalties, and attributes. Browse your NFT holdings and collection details across the MultiversX network.
- `multiversx-account-tokens` (collect) — View all ESDT tokens held by a MultiversX blockchain account with their balances. See your complete token portfolio including token identifiers, balances, decimals, names, and tickers. Track all your token holdings across the MultiversX network in one view.
- `multiversx-account-transaction-count` (collect) — View the total number of transactions for a MultiversX blockchain account.
- `multiversx-account-transactions` (collect) — View the complete transaction history for a MultiversX blockchain account. Retrieve recent transactions with full details including transaction hashes, status, timestamps, values, senders, and receivers. Track account activity and transaction flow over time.
- `multiversx-esdt-issue-fungible` (contract) — Create and issue a new fungible ESDT token on the MultiversX blockchain. Define the token name, ticker, initial supply, and decimal precision. Requires a 0.05 EGLD issuance fee. After issuance, the token identifier (e.g. MYTICKER-xxxxxx) will be assigned by the protocol.
- `multiversx-esdt-issue-nft-collection` (contract) — Create and issue a new Non-Fungible Token (NFT) collection on the MultiversX blockchain. Each token in the collection will be unique. Requires a 0.05 EGLD issuance fee. After issuance, assign the NFTCreate role to your address, then mint individual NFTs.
- `multiversx-esdt-issue-sft-collection` (contract) — Create and issue a new Semi-Fungible Token (SFT) collection on the MultiversX blockchain. SFTs combine properties of both fungible and non-fungible tokens — multiple copies of the same token can exist with shared metadata. Requires a 0.05 EGLD issuance fee. After issuance, assign the NFTCreate role to your address, then mint SFTs.
- `multiversx-esdt-nft-create` (contract) — Mint a new NFT or SFT within an existing MultiversX collection. You must own the ESDTRoleNFTCreate role for the collection to use this. Provide the collection identifier, quantity, name, royalties, optional metadata hash, attributes, and a media URI. No EGLD fee required — only gas.
- `multiversx-esdt-nft-view` (collect) — View detailed information about a specific NFT from a MultiversX collection. Shows the NFT image, name, collection, attributes, royalties, and creator.
- `multiversx-esdt-set-nft-create-role` (contract) — Assign the ESDTRoleNFTCreate role to an address for an NFT or SFT collection. This role is required before minting NFTs. Only the collection owner (issuer) can assign roles. After assigning, the address can create/mint NFTs in the collection.
- ...and 12 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
