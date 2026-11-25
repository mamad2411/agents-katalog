---
name: use-mailcoach
description: Use the Mailcoach JoAi app plugin when the task needs Mailcoach tools or workflows.
---

# Mailcoach

Connect Mailcoach to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Mailcoach tools available in this app.
- Explain what setup or authentication Mailcoach needs before I run an action.
- Use Mailcoach to help me with the task I describe next.

## Action Inventory

- `mailcoach-add-subscriber-tags` (collect) — Add one or more tags to an existing Mailcoach subscriber.
- `mailcoach-add-suppression` (collect) — Manually suppress an email address to prevent it from receiving any future emails.
- `mailcoach-append-subscriber-import` (collect) — Append additional CSV data to an existing subscriber import that is still in draft status.
- `mailcoach-confirm-subscriber` (collect) — Manually confirm a subscriber's double opt-in, moving them from unconfirmed to subscribed status.
- `mailcoach-create-campaign` (collect) — Create a new email campaign in Mailcoach. Campaigns start in draft status.
- `mailcoach-create-email-list` (collect) — Create a new email list in your Mailcoach account.
- `mailcoach-create-segment` (collect) — Create a new subscriber segment for an email list based on positive and negative tag filters.
- `mailcoach-create-subscriber-import` (collect) — Create a subscriber import from a CSV string. The import starts in draft status — call start-subscriber-import to begin processing.
- `mailcoach-create-tag` (collect) — Create a new tag for an email list in Mailcoach.
- `mailcoach-create-template` (collect) — Create a new reusable email template in Mailcoach.
- `mailcoach-delete-campaign` (collect) — Permanently delete a campaign from Mailcoach.
- `mailcoach-delete-email-list` (collect) — Permanently delete an email list and all its subscribers from Mailcoach.
- ...and 47 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
