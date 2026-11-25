---
name: use-peerme
description: Use the PeerMe JoAi app plugin when the task needs PeerMe tools or workflows.
---

# PeerMe

Connect PeerMe to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the PeerMe tools available in this app.
- Explain what setup or authentication PeerMe needs before I run an action.
- Use PeerMe to help me with the task I describe next.

## Action Inventory

- `peerme-earn-claim-peerme-dao` (contract) — Claim your SUPER staking rewards from PeerMe Earn.
- `peerme-earn-distribute-colombia-staking` (contract) — Distribute COLS to stakers of COLS via the PeerMe Earn module.
- `peerme-earn-distribute-peerme-dao` (contract) — Distribute rewards to the trust holders of the PeerMe DAO.
- `peerme-earn-get-entity-users` (query) — Get the users of an entity in the PeerMe Earn module.
- `peerme-earn-stake-peerme-dao` (contract) — Stake SUPER tokens to earn rewards through PeerMe Earn.
- `peerme-earn-withdraw-peerme-dao` (contract) — Withdraw your staked SUPER tokens from PeerMe Earn.
- `peerme-identity-burn-for-trust` (contract) — Burn $SUPER tokens for trust in the PeerMe Identity module.
- `peerme-multisig-check-signed` (query) — Check if a specific user has signed a MultiSig proposal. Use this to verify whether a board member has already approved a specific proposal before asking them to sign.
- `peerme-multisig-check-user-role` (query) — Verify a user's role and permissions in a MultiSig wallet. Use this to determine if an address is a board member (can sign), proposer (can propose), or has no access.
- `peerme-multisig-deposit` (contract) — Deposit EGLD or tokens into the multi-sig wallet. Anyone can deposit funds, and they can later be transferred via proposals.
- `peerme-multisig-discard-action` (contract) — Use when a user wants to discard and remove a multi-sig proposal. All signatures must be removed first before a proposal can be discarded.
- `peerme-multisig-get-action-details` (query, query, query, query, query) — Get detailed information about a specific MultiSig proposal including its type, signers, and whether quorum has been reached. Use this to inspect a proposal before signing or executing it.
- ...and 25 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
