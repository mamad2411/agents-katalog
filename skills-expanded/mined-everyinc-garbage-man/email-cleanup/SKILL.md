---
name: email-cleanup
description: Build a read-only email sender inventory from a native connector, IMAP, or canonical metadata; launch a private keyboard-first domain review app; and export portable future-mail policies plus Gmail and Sieve rules. Use when a user asks to clean up recurring email, reach inbox zero, review newsletter or sender volume, block future mail by domain, or create durable email rules from mailbox history on any provider.
---

# Email Cleanup

Create future-mail policy without changing the mailbox during review. Keep runtime data in the current workspace's `.mailroom/` directory, never inside this plugin.

## Safety contract

- Keep inventory, review, and export read-only.
- Never send, draft, label, archive, trash, mark read, unsubscribe, or install server-side rules unless the user separately and explicitly asks.
- Inventory headers and message metadata only. Do not read bodies.
- Exclude Spam, Trash, Drafts, and Sent.
- Do not infer that unread mail is unwanted. The user must decide every blocked domain.
- Never ask the user to paste mailbox passwords, app passwords, or tokens into chat.
- Do not publish, commit, or quote mailbox inventory.
- Treat a root-domain block as broad. Show observed exact senders and representative subjects before each decision.

Create `.mailroom/` with owner-only permissions. In a Git worktree, add `.mailroom/` to the worktree's local `.git/info/exclude`; do not edit the tracked `.gitignore` merely to run this workflow.

Before ingestion, install the plugin's pinned runtime dependencies when `<plugin-root>/node_modules` is absent:

```sh
npm install --omit=dev --ignore-scripts --prefix <plugin-root>
```

## 1. Choose a source adapter

Read [provider-adapters.md](references/provider-adapters.md) and use the first available route:

1. Native email connector already available to the AI.
2. Read-only IMAP with credentials configured locally by the user.
3. Canonical metadata JSONL produced from another connector or a local export.

Default to unread messages from the last 60 days across non-junk mail, with Inbox membership counted separately. Honor a different user-specified window.

For native connectors, paginate completely and write one record per message to `.mailroom/messages.jsonl` using [message-schema.md](references/message-schema.md). Capture a stable message ID for deduplication, exact From address, display name, subject, date, folder/labels, and List-ID when already available. Do not open messages merely to obtain List-ID.

Convert records to the exact-sender inventory:

```sh
node <plugin-root>/scripts/ingest-messages.js --data-dir <workspace>/.mailroom
```

For IMAP, follow the command in [provider-adapters.md](references/provider-adapters.md); it writes the same inventory directly.

## 2. Launch the review deck

Run:

```sh
node <plugin-root>/scripts/server.js --data-dir <workspace>/.mailroom
```

Use another free port only if the default is occupied. Open the printed loopback URL in the AI's local browser tool when available; otherwise give it to the user to open.

Explain only the two decisions:

- `B`: add the displayed root domain to the future-mail block policy.
- `S`: skip the domain and do nothing.

Decisions and plain-English exception notes autosave to `.mailroom/decisions.json`.

## 3. Compile exceptions

Wait until the user says review is complete. Read `.mailroom/decisions.json` without changing email.

For every blocked domain with a note, translate the note into conservative provider-neutral conditions and write `.mailroom/exceptions.json` using [exceptions-schema.md](references/exceptions-schema.md).

- Preserve the original note in `sourceNote`.
- Prefer narrow subject phrases or exact sender addresses supported by the review evidence.
- Do not invent exceptions.
- Ask when a note is ambiguous.
- Show every compiled exception and get confirmation before export.

## 4. Generate portable rules

After confirmation, run:

```sh
node <plugin-root>/scripts/generate-rules.js --data-dir <workspace>/.mailroom
```

The generator refuses incomplete reviews and blocked domains with uncompiled notes. It writes:

- `email-policy.json`: provider-neutral source of truth.
- `rule-review.csv`: human-readable audit.
- `gmail-filters.xml`: importable Gmail filters.
- `email-cleaner.sieve`: Sieve rules for compatible providers.

Validate reported Block, Skip, and exception counts. Tell the user no mailbox changes have been made. Explain that enforcement depends on the provider: import Gmail XML, install Sieve where supported, or use `email-policy.json` with a provider connector/API.

Unsubscription is separate. Offer it only when the user explicitly requests it and a safe provider-specific method exists.
