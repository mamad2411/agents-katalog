---
name: mailclaw
description: Read, search, send, and manage emails from the MailClaw inbox via the local CLI. Use when the user asks to check emails, read messages, search inbox, find emails from a sender, review recent correspondence, or send/reply to emails.
allowed-tools: Bash(mailclaw *), Bash(brew *), Bash(curl *), Bash(chmod *), Bash(uname *), Bash(sudo *)
---

# MailClaw - Binary CLI

You have access to the local `mailclaw` binary CLI. Use it to read, search, and manage emails. Do not call the MailClaw HTTP API directly with `curl` unless the user explicitly asks for raw API requests.

By default, if `mailclaw` is missing, install it automatically and then continue the task.

## Prerequisite

Before doing anything else, verify the CLI exists and meets the minimum version:

```bash
mailclaw --version
```

- **Minimum version for send**: The `send` command requires CLI version **>= 1.0.1**. If the installed version is older, upgrade it using the install flow below before proceeding.
- If `mailclaw` is missing on macOS, install it with Homebrew.
- If `mailclaw` is missing on Linux, download the latest release binary and install it to `/usr/local/bin/mailclaw`.
- On Windows, do not guess an install flow here. Ask the user to install the CLI manually or provide the binary path.
- Once the binary is available, use it for all inbox operations.

### Automatic install flow

Run the official install script, which handles both macOS (Homebrew) and Linux (GitHub Releases) automatically:

```bash
curl -fsSL https://raw.githubusercontent.com/missuo/mailclaw/main/install.sh | bash
```

- On macOS, the script installs via `brew tap owo-network/brew && brew install owo-network/brew/mailclaw`.
- On Linux, the script detects the architecture, downloads the latest release binary, and installs it to `/usr/local/bin/mailclaw`.
- After installation, the script prompts the user to configure host and API token interactively.
- If writing to `/usr/local/bin` fails, the script will request elevated privileges automatically.
- On Windows, do not run the install script. Ask the user to install the CLI manually or provide the binary path.
- Reuse the installed CLI on future invocations unless the user asks for a specific version or a source build.

## Configuration

Use the CLI to manage config instead of reading or writing `~/.mailclaw/config.json` manually.

```bash
# Save credentials
mailclaw config set --host "https://mailclaw.example.com" --api-token "your-api-token-here"

# Show current config state
mailclaw config show --json

# Verify the configured host is reachable
mailclaw health --json
```

- If config is missing, ask the user to provide their **MailClaw Host** and **API Token**, then save them with `mailclaw config set`.
- The CLI also supports global overrides `--host <HOST>` and `--api-token <TOKEN>`, but prefer persisted config unless the user wants a one-off override.
- On Windows, ask the user for the CLI path if `mailclaw` is not already available on `PATH`.

## Available Commands

### List emails (metadata only)

```bash
mailclaw list [--limit N] [--offset N] [--from sender@example.com] [--to inbox@example.com] [--q keyword] [--after 2026-03-01] [--before 2026-03-11] [--json]
```

Returns email summaries without body content. Use this for overview and browsing.

### Export emails (with full content)

```bash
mailclaw export [same filters as list] [--json]
```

Returns full emails including `text_content` and `html_content`. Use this when the user wants body content for multiple emails.

### Get single email

```bash
mailclaw get <email_id> [--json]
```

Returns one full email, including body content and `attachments` metadata.

### List attachments

```bash
mailclaw attachments <email_id> [--json]
```

Lists attachment metadata (id, filename, mime_type, size) for an email.

### Download attachment

```bash
mailclaw download <email_id> <attachment_id> [-o <path>] [--json]
```

Downloads one attachment's binary content. Without `-o`, it saves to the
attachment's original filename in the current directory.

### Delete email

```bash
mailclaw delete <email_id> [--json]
```

Permanently deletes an email. Always confirm with the user before deleting.

### Health check

```bash
mailclaw health [--json]
```

Use this to verify the configured host is correct during setup.

## JSON Output

When you pass `--json`, the CLI prints the payload directly, not the original HTTP `{ success, data }` envelope.

### Email object (list)

```json
{
  "id": "clx...",
  "from_address": "sender@example.com",
  "to_address": "bd@example.com",
  "subject": "Subject line",
  "received_at": 1710000000,
  "has_attachments": false,
  "attachment_count": 0
}
```

### Email object (export / get)

Same as above, plus:
```json
{
  "text_content": "Plain text body...",
  "html_content": "<p>HTML body...</p>"
}
```

### Paginated response

```json
{
  "emails": [ ... ],
  "total": 128,
  "limit": 20,
  "offset": 0
}
```

## Usage Examples

```bash
# List all recent emails
mailclaw list --json

# Search emails containing "partnership"
mailclaw list --q partnership --json

# Filter by recipient and sender
mailclaw list --to bd@example.com --from partner@company.com --json

# Get emails from the last 7 days
mailclaw list --after 2026-03-03 --json

# Export emails with full content
mailclaw export --limit 10 --json

# Read a specific email
mailclaw get clx123abc --json

# Delete an email
mailclaw delete clx123abc --json
```

### Send email

```bash
mailclaw send --from "Name <sender@example.com>" --to recipient@example.com --subject "Subject" --text "Body text" [--html "<p>HTML body</p>"] [--cc cc@example.com] [--bcc bcc@example.com] [--reply-to reply@example.com] [--json]
```

Sends an email via the configured provider (Resend by default). At least `--text` or `--html` is required. Multiple `--to`, `--cc`, `--bcc`, and `--reply-to` addresses can be specified.

**JSON response:**

```json
{
  "id": "<provider-message-id>",
  "provider": "resend"
}
```

## Guidelines

1. **Use the CLI, not curl** — All inbox operations should go through `mailclaw`.
2. **Check config through the CLI** — Use `mailclaw config show --json` and `mailclaw config set ...`; do not manually edit the config file unless the user explicitly asks.
3. **Verify on first use** — After saving a new config, call `mailclaw health --json`.
4. **Start with list** — Use `mailclaw list` first to get an overview, then drill into specific emails with `mailclaw get <id>`.
5. **Use filters** — Always apply relevant filters (`from`, `to`, `q`, date range) rather than fetching everything.
6. **Prefer text_content** — When displaying email content to the user, prefer `text_content` over `html_content` for readability.
7. **Pagination** — For large inboxes, paginate through results using `limit` and `offset`.
8. **Confirm deletes** — Always ask the user for confirmation before deleting emails.
9. **Date formatting** — The `received_at` field is a Unix timestamp in seconds. Convert it to a human-readable format when presenting to the user.
