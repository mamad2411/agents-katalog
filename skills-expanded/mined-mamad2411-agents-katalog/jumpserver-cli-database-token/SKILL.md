---
name: jumpserver-cli-database-token
description: Use when creating JumpServer database connection tokens, DSNs, jms URLs, or non-interactive database credential output with jumpserver-cli.
---

# JumpServer CLI Database Tokens

Use `jms assets databases token` to create temporary connection credentials for permitted database assets.

## Interactive Selection

```bash
jms assets databases token "prod-*"
```

The command searches permitted database assets, lets the user select assets and usernames when needed, and prints connection tables.

## Non-Interactive All Assets

```bash
jms assets databases token --all
jms assets databases token "prod-*" --all --limit 50
```

`--all` fetches all matching permitted database assets without prompts. It uses each asset's permitted account alias from the asset detail API, not a guessed account name.

## Script-Friendly Output

```bash
jms assets databases token --all --dsn
jms assets databases token "prod" --json
jms assets databases token "prod" --jms-url
```

Use `--dsn` for one DSN per line, `--json` for structured output, and `--jms-url` when the raw JumpServer client URL is needed.

## Options

- `--account <name>`: explicitly set JumpServer account alias/name.
- `--input-username <username>`: explicitly set database username.
- `--protocol <protocol>`: override asset protocol.
- `--connect-method <method>`: defaults to `db_guide`.
- `--reusable` / `--no-reusable`: control reusable token creation.

## Safety

`--all` creates tokens for every matching permitted database asset. Use a pattern first when the asset set is large or uncertain.
