---
name: agent-notifier
description: Use Agent Notifier when the user asks Codex to set up phone notifications, send meaningful encrypted alerts, request a short reply, or request an approval through the local Agent Notifier MCP server.
---

# Agent Notifier

Use Agent Notifier as a sparse, human-consent channel for AI agent work. It is for phone-visible notifications and lightweight approvals, not chat, remote control, or routine progress logs.

## Core Rules

- Use only for meaningful notifications, user-requested alerts, blocks, and required approvals.
- Do not use this for routine progress updates unless the user asked for routine updates.
- Do not invent new approval gates just because this tool exists.
- Ask before sending setup email unless the user clearly delegated setup.
- Mark sensitive content appropriately; when unsure, mark the message sensitive.
- Do not send plaintext message content or sender private keys to a hosted connector. Use the local MCP server or CLI so encryption and signing happen on the sender machine.
- If the local MCP tools are unavailable, report that setup is blocked; do not route plaintext through a hosted connector as a workaround.
- Keep messages short enough to be useful in a phone notification.

## Setup

1. Check whether the sender is already paired with `setup_notifier` or the MCP server's setup/status tool.
2. Prefer email pairing because it is asynchronous and low-friction.
3. Before email setup, confirm the recipient email and ask permission unless setup was clearly delegated. Good: "I can send the setup email to you@example.com now. Should I do that?"
4. Offer pairing code as the fallback when the user does not want email or email is awkward.
5. Explain that email is setup/recovery metadata and that message contents remain encrypted from the server.

## Tool Choice

- Use `send_notification` for one-way terminal or meaningful state changes.
- Use `request_reply` when you are blocked and need a short user answer.
- Use `request_approval` only when the user explicitly requested approval or the next action already requires approval under the surrounding workflow.
- Use `get_message_status` for a known message.
- Use `wait_for_message_state` when the user asked you to wait for delivery, a reply, an approval, rejection, or expiry.
- Use `list_senders` before changing sender setup or when troubleshooting revoked or duplicate senders.
- Use `explain_usage_policy` when the user asks when notifications should or should not be sent.

## Sensitive Classification

Mark a message sensitive when it includes or may include:

- Secrets, credentials, tokens, API keys, cookies, session identifiers, or private URLs.
- Logs, stack traces, environment dumps, CI output, or diffs likely to contain secrets.
- Private personal data, customer data, emails, phone numbers, addresses, or account identifiers.
- Security findings, vulnerability details, unreleased launch details, confidential business information, or private repo content.
- Approval context that reveals risky commands, deployment targets, financial actions, or destructive operations.

Mark a message non-sensitive only when the title and body are safe to show as a phone preview. When unsure, mark it sensitive and write a generic title.

## Message Style

- Title: specific and compact, such as "Deploy blocked" or "Review complete".
- Body: one or two sentences with the exact ask, blocker, or outcome.
- Approval request: include the action label and a concise risk/context note.
- Reply request: ask one clear question and avoid multi-turn chat framing.
- Avoid large pasted logs. Summarize and keep the source detail in the local thread.

## Safety Boundaries

The service returns signed human intent; it does not execute actions. After an approval response, apply the normal local approval policy for the action itself. After a rejection or expiry, do not perform the action.
