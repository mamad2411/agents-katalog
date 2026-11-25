---
name: biolab-api
version: 0.1.0
description: "Use when operating the Biolab lab management CLI for primer synthesis, sequencing orders, inventory, templates, lab members, or account status."
metadata:
  requires:
    bins: ["biolab"]
  cliHelp: "biolab --help"
---

# Biolab CLI Skill

This skill teaches an AI agent how to use the `biolab` command line tool safely and reliably.

## Setup

Check whether the CLI is available:

```bash
biolab --help
```

Authenticate with Feishu OAuth before making API calls:

```bash
biolab login --background
biolab status
```

The access token is loaded from `BIOLAB_TOKEN` first, then from the OS keychain. In Docker/K8s containers, if keyring is unavailable, the CLI automatically uses a container-local token file so Agent login does not require restarting the container or mounting a secret. Legacy `~/.biolab_token` files are migrated into the keychain when possible on non-container hosts; host plaintext token files require explicit `BIOLAB_INSECURE_TOKEN_FILE=1`.

## Agent Rules

- Prefer `-f json` when the next step needs machine parsing.
- Do not print tokens or secrets.
- For write operations, confirm the user's intent first when the request is destructive or changes shared lab state.
- If a command fails because login is missing or expired, run `biolab login --background`, send the printed auth URL to the user, and check `biolab status` after the user completes the browser flow.
- Use `biolab update check` to check whether the installed CLI is behind the latest release; do not auto-download or replace binaries unless the user asks.
- Use command help before guessing flags: `biolab <domain> --help`.
- Before complex domain work, read the matching reference file:
  - Orders: `references/orders.md`
  - Inventory: `references/inventory.md`
  - Templates: `references/templates.md`
  - Lab: `references/lab.md`
  - Users: `references/users.md`

## Common Commands

Account:

```bash
biolab me -f json
biolab me update '{"phone_number":"13800000000"}'
biolab update check
biolab logout
```

Orders:

```bash
biolab orders list -f json
biolab orders get <ORDER_ID> -f json
biolab orders create-primer order.json
biolab orders create-sequencing order.json
biolab orders download <ORDER_ID> order.xlsx
biolab orders download-primer-template primer_template.xlsx
biolab orders download-sequencing-template sequencing_template.xlsx
```

Inventory:

```bash
biolab inventory list -f json
biolab inventory list --low-stock -f json
biolab inventory checkin <STOCK_ID> --quantity 5 --purpose "restock"
biolab inventory checkout <STOCK_ID> --quantity 2 --purpose "PCR"
biolab inventory locations -f json
```

Templates:

```bash
biolab templates list -f json
biolab templates get-default primer_synthesis -f json
biolab templates set-default <TEMPLATE_ID>
```

Lab:

```bash
biolab lab info -f json
biolab lab members -f json
biolab lab invite <email> member
```

## Order Notes

Primer synthesis orders use `primer_synthesis`. Sequencing orders use `sequencing`.
The typical order status flow is:

```text
pending -> ordered -> received -> stored
```

When creating orders from JSON, inspect an existing order or use templates first so required customer, supplier, payment, and item fields match backend expectations.

## Skill Maintenance

Install or refresh this skill for local agent use from a project directory:

```bash
biolab skills install
```

Install globally for supported agents:

```bash
biolab skills install --global
```

The install command delegates to the standard `skills` installer. For direct installation, use:

```bash
npx -y skills add xuyuan-hub/biolab-cli --skill biolab-api -y -g
```

Check whether installed skills match the running CLI version:

```bash
biolab skills check -f json
```
