---
name: use-signature
description: Use the Signature JoAi app plugin when the task needs Signature tools or workflows.
---

# Signature

Connect Signature to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Signature tools available in this app.
- Explain what setup or authentication Signature needs before I run an action.
- Use Signature to help me with the task I describe next.

## Action Inventory

- `signature-cancel` (query, contract) — Cancel a pending signature request you created. This is recorded permanently on-chain.
- `signature-create` (contract, collect) — Send a legally-binding signature request. The signer receives an email and confirms the document with one click.
- `signature-decline` (query, contract, collect) — Formally decline a signature request. This records your refusal on-chain.
- `signature-list` (query) — View all signature requests you have created.
- `signature-remind` (query, collect) — Resend the signing link to a signer who hasn't responded yet.
- `signature-self-sign` (contract, collect) — Upload a document and sign it yourself. Creates an on-chain proof of authorship — ideal for sending a signed copy via email.
- `signature-sign` (query, contract) — Review the document and confirm your signature. Your approval is permanent and tamper-proof.
- `signature-view` (query) — See the details and current status of a signature request.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
