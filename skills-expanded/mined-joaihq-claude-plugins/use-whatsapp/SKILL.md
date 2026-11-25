---
name: use-whatsapp
description: Use the WhatsApp JoAi app plugin when the task needs WhatsApp tools or workflows.
---

# WhatsApp

Connect WhatsApp to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the WhatsApp tools available in this app.
- Explain what setup or authentication WhatsApp needs before I run an action.
- Use WhatsApp to help me with the task I describe next.

## Action Inventory

- `whatsapp-auth` (prompt) — Open the WhatsApp pairing QR in a live terminal so you can scan it with your phone.
- `whatsapp-cli-update` (prompt) — Update wacli to the latest verified release for reliable personal WhatsApp messaging and sync. JoAi checks the downloaded release before installing it in the desktop app's managed tools directory.
- `whatsapp-media-import` (prompt) — Download personal WhatsApp media (voice notes, photos, and files) from the local sync store into the JoAi workspace. JoAi then attaches the file so the agent can use it in the conversation. Requires the desktop app with sync media download enabled.
- `whatsapp-send-media` (prompt) — Send a photo or file to a phone number or WhatsApp group via personal WhatsApp. Use a local workspace path or a downloadable media URL (the desktop app materializes URLs before sending).
- `whatsapp-send-text` (prompt) — Send a text message to a phone number or WhatsApp group via personal WhatsApp. Perfect for customer notifications, order updates, reminders, group replies, or quick personal messages directly from your agent.
- `whatsapp-send-voice` (prompt) — Send a voice note (OGG/Opus) to a phone number or WhatsApp group via personal WhatsApp. Use a local workspace path or a downloadable media URL (the desktop app materializes URLs before sending).
- `whatsapp-sync` (prompt) — Keep personal WhatsApp in sync and forward new messages to your agent webhook while this laptop is online.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
