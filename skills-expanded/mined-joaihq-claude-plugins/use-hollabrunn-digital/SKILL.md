---
name: use-hollabrunn-digital
description: Use the Hollabrunn Digital JoAi app plugin when the task needs Hollabrunn Digital tools or workflows.
---

# Hollabrunn Digital

Connect Hollabrunn.Digital to ChatGPT, Claude, Codex, and Cursor — find local businesses, book appointments, and help partners join the directory.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- Welche Betriebe aus Hollabrunn sind auf Hollabrunn.Digital gelistet?
- Finde Wellness- oder Coaching-Angebote in Hollabrunn und gib mir den Buchungslink.
- Hilf mir, einen neuen Partner für Hollabrunn.Digital vorzubereiten (Texte + nächste Schritte).

## Action Inventory

- `hd-businesses-list` (collect) — List public Hollabrunn.Digital businesses (JoAi teams tagged hollabrunn-digital).
- `hd-business-show` (collect) — Show a business profile by slug and return hollabrunn.digital and booking links.
- `hd-outreach-draft` (collect) — Draft a WhatsApp/Messenger first-touch in Micha's Hollabrunn.Digital tone of voice.

## Usage Notes

- Prefer public Hollabrunn.Digital / JoAi team data tagged hollabrunn-digital.
- When drafting outreach or partner messages, follow the Micha tone-of-voice rules (short, casual German, always „3–4 Fotos für die Galerie“).
- Booking links use store.joai.ai/{locale}/{teamSlug}/book when appointments are enabled.
- Until the dedicated Cortex MCP app is live, fall back to the JoAi MCP app and scope tools to the hollabrunn-digital tag.

## Auth Notes

- Public browse may work without auth; partner onboarding and CRM writes require JoAi authentication.
