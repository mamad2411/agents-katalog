---
name: tigris-authentication
description: Use when authenticating with Tigris, managing credentials, or setting up the CLI
---

# Tigris Authentication & Setup

## Install the CLI

```bash
npm install -g @tigrisdata/cli
tigris --version
```

The CLI is also available as `t3` (alias for `tigris`).

## Quick Start

```bash
tigris login          # authenticate via browser
tigris whoami         # verify identity
tigris ls             # list your buckets
```

## Commands

### `tigris login`

Start a session via OAuth (default) or temporary credentials. Session state is cleared on logout.

```bash
tigris login                        # interactive — choose OAuth or credentials
tigris login oauth                  # browser-based OAuth2 device flow
tigris login credentials            # access key + secret (prompts if not provided)
tigris login credentials --access-key tid_AaBb --access-secret tsec_XxYy
```

| Subcommand          | Alias     | Description                                             |
| ------------------- | --------- | ------------------------------------------------------- |
| `login` (default)   | `l`       | Interactive — choose login method                       |
| `login oauth`       | `login o` | Login via browser using OAuth2 device flow              |
| `login credentials` | `login c` | Login with an access key and secret (temporary session) |

**`login credentials` flags:**

| Flag              | Alias      | Description                                 |
| ----------------- | ---------- | ------------------------------------------- |
| `--access-key`    | `--key`    | Access key ID (prompts if not provided)     |
| `--access-secret` | `--secret` | Secret access key (prompts if not provided) |

### `tigris configure`

Save access-key credentials to `~/.tigris/config.json` for persistent use across all commands.

```bash
tigris configure --access-key tid_AaBb --access-secret tsec_XxYy
tigris configure --endpoint https://custom.endpoint.dev
```

| Flag              | Alias      | Description                                             |
| ----------------- | ---------- | ------------------------------------------------------- |
| `--access-key`    | `--key`    | Your Tigris access key ID                               |
| `--access-secret` | `--secret` | Your Tigris secret access key                           |
| `--endpoint`      | `-e`       | Tigris API endpoint (default: `https://t3.storage.dev`) |

### `tigris whoami`

Print the currently authenticated user, organization, and auth method.

```bash
tigris whoami
tigris whoami --json
```

| Flag       | Alias | Description                                       |
| ---------- | ----- | ------------------------------------------------- |
| `--format` | `-f`  | Output format (`json`, `table`; default: `table`) |
| `--json`   |       | Output as JSON                                    |

### `tigris logout`

End the current session and clear login state. Credentials saved via `configure` are kept.

```bash
tigris logout
```

### `tigris credentials test`

Verify that current credentials are valid. Optionally checks access to a specific bucket.

```bash
tigris credentials test
tigris credentials test --bucket my-bucket
```

| Flag       | Alias | Description                                       |
| ---------- | ----- | ------------------------------------------------- |
| `--bucket` | `-b`  | Bucket name to test access against (optional)     |
| `--format` | `-f`  | Output format (`json`, `table`; default: `table`) |
| `--json`   |       | Output as JSON                                    |

### `tigris orgs list` / `create` / `select`

List, create, and switch between organizations.

```bash
tigris orgs list                    # list orgs + interactively select one
tigris orgs list --json             # list orgs as JSON
tigris orgs create my-org           # create a new organization
tigris orgs select my-org           # set active organization
```

| Command              | Alias    | Description                                         |
| -------------------- | -------- | --------------------------------------------------- |
| `orgs list`          | `orgs l` | List all organizations and interactively select one |
| `orgs create <name>` | `orgs c` | Create a new organization                           |
| `orgs select <name>` | `orgs s` | Set the named organization as active                |

## Environment Variables

When credentials are set via environment variables, they take precedence over `~/.tigris/config.json` and session state. This is common in CI/CD and serverless environments.

### Tigris

| Variable                           | Description                                 |
| ---------------------------------- | ------------------------------------------- |
| `TIGRIS_STORAGE_ACCESS_KEY_ID`     | Tigris access key ID (e.g. `tid_AaBb`)      |
| `TIGRIS_STORAGE_SECRET_ACCESS_KEY` | Tigris secret access key (e.g. `tsec_XxYy`) |
| `TIGRIS_STORAGE_ENDPOINT`          | Tigris endpoint (`https://t3.storage.dev`)  |
| `TIGRIS_STORAGE_BUCKET`            | Default bucket name                         |

## Global Flags

These flags are available on all `tigris` commands:

| Flag     | Description                                                       |
| -------- | ----------------------------------------------------------------- |
| `--json` | Output in JSON format (useful for programmatic/agent consumption) |
| `--yes`  | Skip confirmation prompts (prevents interactive mode)             |
