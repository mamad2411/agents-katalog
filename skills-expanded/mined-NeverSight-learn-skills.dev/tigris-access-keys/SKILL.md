---
name: tigris-access-keys
description: Use when creating, listing, assigning, or deleting access keys for Tigris Storage
---

# Tigris Access Keys

Access keys are programmatic credentials for the Tigris API. Key IDs use the `tid_` prefix, secrets use the `tsec_` prefix.

## Commands

### `tigris access-keys list` (alias: `l`)

List all access keys in the current organization.

```bash
tigris access-keys list
tigris access-keys list --json
```

| Flag       | Alias | Description                            | Default |
| ---------- | ----- | -------------------------------------- | ------- |
| `--format` | `-f`  | Output format (`json`, `table`, `xml`) | `table` |
| `--json`   |       | Output as JSON                         |         |

### `tigris access-keys create <name>` (alias: `c`)

Create a new access key with the given name. The secret is shown only once — save it immediately.

```bash
tigris access-keys create my-ci-key
tigris access-keys create my-ci-key --json
```

| Flag       | Alias | Description                     | Default |
| ---------- | ----- | ------------------------------- | ------- |
| `--format` | `-f`  | Output format (`json`, `table`) | `table` |
| `--json`   |       | Output as JSON                  |         |

### `tigris access-keys get <id>` (alias: `g`)

Show details for an access key including its name, creation date, and assigned bucket roles.

```bash
tigris access-keys get tid_AaBbCcDdEeFf
tigris access-keys get tid_AaBbCcDdEeFf --json
```

| Flag       | Alias | Description                     | Default |
| ---------- | ----- | ------------------------------- | ------- |
| `--format` | `-f`  | Output format (`json`, `table`) | `table` |
| `--json`   |       | Output as JSON                  |         |

### `tigris access-keys delete <id>` (alias: `d`)

Permanently delete an access key. This revokes all access immediately.

```bash
tigris access-keys delete tid_AaBbCcDdEeFf --force
```

| Flag              | Description                                       |
| ----------------- | ------------------------------------------------- |
| `--force`         | Skip confirmation prompt                          |
| `--format` / `-f` | Output format (`json`, `table`; default: `table`) |
| `--json`          | Output as JSON                                    |

### `tigris access-keys assign <id>` (alias: `a`)

Assign per-bucket roles to an access key. Pair each `--bucket` with a `--role` (Editor or ReadOnly), or use `--admin` for org-wide access.

```bash
# Single bucket
tigris access-keys assign tid_AaBb --bucket my-bucket --role Editor

# Multiple buckets with different roles
tigris access-keys assign tid_AaBb --bucket a,b --role Editor,ReadOnly

# Org-wide admin access
tigris access-keys assign tid_AaBb --admin

# Revoke all roles
tigris access-keys assign tid_AaBb --revoke-roles
```

| Flag             | Alias | Description                                                                                                  |
| ---------------- | ----- | ------------------------------------------------------------------------------------------------------------ |
| `--bucket`       | `-b`  | Bucket name(s), comma-separated. Each bucket pairs positionally with a `--role` value                        |
| `--role`         | `-r`  | Role(s) to assign (`Editor`, `ReadOnly`), comma-separated. Each role pairs with the corresponding `--bucket` |
| `--admin`        |       | Grant admin access to all buckets in the organization                                                        |
| `--revoke-roles` |       | Revoke all bucket roles from the access key                                                                  |
| `--format`       | `-f`  | Output format (`json`, `table`; default: `table`)                                                            |
| `--json`         |       | Output as JSON                                                                                               |

## Workflow

```bash
# 1. Create a key
tigris access-keys create my-app-key --json
# Save the tid_ and tsec_ values from the output!

# 2. Scope it to specific buckets
tigris access-keys assign tid_AaBb --bucket my-bucket --role Editor

# 3. Configure your environment (Tigris env vars)
export TIGRIS_STORAGE_ACCESS_KEY_ID=tid_AaBb
export TIGRIS_STORAGE_SECRET_ACCESS_KEY=tsec_XxYy
export TIGRIS_STORAGE_ENDPOINT=https://t3.storage.dev
export TIGRIS_STORAGE_BUCKET=my-bucket

```

## Security Best Practices

- **Scope to specific buckets** — avoid `--admin` unless truly needed
- **Use minimal roles** — prefer `ReadOnly` when writes aren't required
- **Separate keys per app** — create dedicated keys for each application or environment
- **Rotate keys regularly** — delete old keys and create new ones
- **Never commit secrets** — use environment variables or secret managers, not source code
