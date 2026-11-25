---
name: scrapeatlas-setup
description: "Install and authenticate the ScrapeAtlas CLI (@scrapeatlas/cli) for an agent that runs commands in its own environment, such as Hermes, OpenClaw, NanoClaw, Paperclip or a Grok bot, or any server, container or CI job. Use when ScrapeAtlas MCP tools are not available and the agent needs to call ScrapeAtlas from a shell, or when the user asks to set up, connect or verify ScrapeAtlas."
homepage: "https://scrapeatlas.com/docs/cli/"
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - package: "@scrapeatlas/cli"
        manager: node
---

# ScrapeAtlas setup

Install the `scrapeatlas` CLI, give it a ScrapeAtlas API key without exposing the
key, and verify the connection with a free account read.

If the agent's runtime can connect to a remote MCP server with a custom header,
that also works: URL `https://api.scrapeatlas.com/mcp`, header
`Authorization: Bearer <API key>`, with the key taken from the runtime's secret
settings. The steps below cover the CLI.

## 1. Check Node.js

```bash
node --version
```

The CLI requires Node.js 22 or newer. If Node is missing or older, tell the user;
do not change the system Node installation without their approval.

## 2. Install the CLI

```bash
npm install -g @scrapeatlas/cli
scrapeatlas --version
```

If global installs are not allowed, run every command through npx instead:
`npx @scrapeatlas/cli@latest <command>`. To update an existing install, run
`npm install -g @scrapeatlas/cli@latest`.

## 3. Get an API key

Ask the user to create a key at https://scrapeatlas.com/dashboard/keys/. Calls
spend credits from that account.

Ask the user to store the key themselves as `SCRAPEATLAS_API_KEY` in the runtime's
secret or environment settings (for example the bot's environment variables, a
container secret or a CI secret). This keeps the key out of the conversation and
the agent's logs. Restart or reload the agent if the runtime requires it for new
variables.

## 4. Authenticate

The CLI reads credentials in this order: `--api-key`, then `SCRAPEATLAS_API_KEY`,
then the key saved by `scrapeatlas auth login`.

- **Environment variable (preferred for agents).** If `SCRAPEATLAS_API_KEY` is
  set, no login is needed. Containers and short-lived environments often lose
  saved config, so prefer this.
- **Saved login.** Interactive terminals: `scrapeatlas auth login` opens a hidden
  prompt; the user types the key. Noninteractive: pipe the key from a variable or
  secret file, never from a literal in the command:

  ```bash
  printf '%s' "$SCRAPEATLAS_API_KEY" | scrapeatlas auth login --stdin
  ```

  Login verifies the key before saving it to
  `~/.config/scrapeatlas/config.json` (mode 0600). Set `SCRAPEATLAS_CONFIG_DIR` to
  store it elsewhere.

Rules for the key:

- Never `echo` the key, print it, write it into a command line, commit it or
  include it in a reply. Avoid `--api-key` on shared hosts; it can appear in shell
  history and process lists.
- If the user pastes a key into the chat anyway, tell them it is now in the chat
  history, suggest they store it as an environment variable instead, and offer to
  continue once it is set. Do not repeat the key.
- Never ask for platform logins, passwords or cookies. ScrapeAtlas retrieves
  public data only and does not use them.

## 5. Verify

```bash
scrapeatlas auth status
```

This shows whether a key is configured and its source, without printing it or
contacting the API. Then make a free authenticated read:

```bash
scrapeatlas usage account-usage --days 1
```

This costs 0 credits. Exit code 0 with `"success":true` means the key works. Exit
code 1 with HTTP 401 means the key is missing, invalid or revoked. A revoked key
can take up to a minute to stop working.

Optional 1-credit retrieval test:

```bash
scrapeatlas bluesky profile --handle bsky.app --pretty
```

## 6. Use it

```bash
scrapeatlas list                      # platforms
scrapeatlas list tiktok               # commands for one platform
scrapeatlas tiktok profile --help     # parameters for one command
scrapeatlas list tiktok --json        # operation IDs and schemas
```

Each command makes one request and prints the response JSON to stdout. Exit codes:
0 usable (including partial), 1 API or network failure, 2 local usage error. Use
`--output file.json` to save a result. Follow the `scrapeatlas` skill for reading
status, coverage and failures, pagination and credits.

To remove the saved key: `scrapeatlas auth logout`. This does not revoke the key;
revoke it in the dashboard.
