---
name: use-certificate
description: Use the Certificate JoAi app plugin when the task needs Certificate tools or workflows.
---

# Certificate

Connect Certificate to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Certificate tools available in this app.
- Explain what setup or authentication Certificate needs before I run an action.
- Use Certificate to help me with the task I describe next.

## Action Inventory

- `certificate-claim` (contract) — You have been issued a digital certificate on the blockchain. Connect your wallet to claim it.
- `certificate-create-collection` (contract) — Create an NFT collection on the blockchain for issuing digital certificates. Each collection represents a certificate type (e.g. Innovationssiegel, Completion, Compliance).
- `certificate-issue` (contract, collect) — Upload a PDF and issue a verifiable digital certificate on the blockchain. The recipient gets an email to claim it.
- `certificate-list` (query) — View all digital certificates you have issued on the blockchain.
- `certificate-revoke` (contract) — Permanently revoke a certificate you issued. This action cannot be undone.
- `certificate-verify` (query) — Check the authenticity and validity of a digital certificate on the blockchain by its ID.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
