---
name: devcontainer-secrets-injection
description: Two-mechanism secret injection for devcontainers — Codespaces secrets block and local devcontainer.env file, with WireGuard VPN capabilities — pattern from mmalyska/home-ops
---

# Devcontainer Secrets Injection

## When to Use

Use this skill when a devcontainer needs access to credentials (API tokens, VPN keys, etc.) in both GitHub Codespaces and local VS Code Dev Containers. The pattern uses two parallel mechanisms that work transparently in each environment.

---

## Mechanism 1: Codespaces — `"secrets"` block

In GitHub Codespaces, secrets are injected as environment variables from the repository's Codespaces secrets (Settings > Secrets and variables > Codespaces).

Declare each secret in `devcontainer.json`:

```json
{
  "secrets": {
    "TERRAFORM_TOKEN": {
      "description": "Token to access Terraform Cloud."
    },
    "BWS_ACCESS_TOKEN": {
      "description": "Token to access Bitwarden Secrets Manager API."
    },
    "GITHUB_TOKEN": {
      "description": "Personal access token for GitHub API."
    },
    "WG_PRIVATE_KEY": {
      "description": "WireGuard client private key for home lab VPN."
    },
    "WG_ENDPOINT": {
      "description": "WireGuard server endpoint (host:port)."
    }
  }
}
```

The `description` fields appear in the Codespaces UI when a secret is not set.

---

## Mechanism 2: Local — `devcontainer.env` file

For local VS Code, secrets live in a gitignored `.devcontainer/devcontainer.env` file and are passed to the container via `--env-file`.

### `.devcontainer/devcontainer.env.sample`

Commit a sample file with commented-out keys and no values:

```bash
# Local development secrets — copy this file to devcontainer.env and fill in the values.
# devcontainer.env is gitignored. In GitHub Codespaces, set these as repository secrets instead.
#
# TERRAFORM_TOKEN=    # Terraform Cloud token
# BWS_ACCESS_TOKEN=   # Bitwarden Secrets Manager token
# GITHUB_TOKEN=       # GitHub PAT (also used as HOMEBREW_GITHUB_API_TOKEN)
# WG_PRIVATE_KEY=     # WireGuard client private key
# WG_ENDPOINT=        # WireGuard server endpoint host:port (e.g. vpn.example.com:51820)
```

**Never commit actual values.** All lines should be commented out in the sample.

### `.gitignore`

```gitignore
.devcontainer/devcontainer.env
```

### `runArgs` in `devcontainer.json`

```json
{
  "runArgs": ["--env-file", ".devcontainer/devcontainer.env"]
}
```

### `initializeCommand` — auto-create env from sample

```json
{
  "initializeCommand": "test -f .devcontainer/devcontainer.env || cp .devcontainer/devcontainer.env.sample .devcontainer/devcontainer.env"
}
```

This runs before the container starts and creates `devcontainer.env` from the sample if it doesn't exist. The developer then fills in the actual values without creating a blank file from scratch.

---

## WireGuard VPN Capabilities

If the container needs to establish a WireGuard VPN tunnel (e.g. to reach a homelab), add network capabilities to `runArgs`:

```json
{
  "runArgs": [
    "--env-file", ".devcontainer/devcontainer.env",
    "--cap-add=NET_ADMIN",
    "--device=/dev/net/tun"
  ]
}
```

- `--cap-add=NET_ADMIN`: allows the container to manage network interfaces
- `--device=/dev/net/tun`: exposes the TUN device for tunnel creation

**Note:** `--device=/dev/net/tun` requires the host to have `/dev/net/tun` available. This is always true on Linux hosts; on macOS with Docker Desktop it is also available. This flag is not needed in GitHub Codespaces (VPN is handled at the host level).

---

## Complete `devcontainer.json` Example

```json
{
  "name": "my-project",
  "image": "ghcr.io/owner/repo-devcontainer:main@sha256:abc123...",
  "secrets": {
    "TERRAFORM_TOKEN": {
      "description": "Token to access Terraform Cloud."
    },
    "BWS_ACCESS_TOKEN": {
      "description": "Token to access Bitwarden Secrets Manager API."
    },
    "GITHUB_TOKEN": {
      "description": "Personal access token for GitHub API."
    },
    "WG_PRIVATE_KEY": {
      "description": "WireGuard client private key."
    },
    "WG_ENDPOINT": {
      "description": "WireGuard server endpoint host:port."
    }
  },
  "runArgs": [
    "--env-file", ".devcontainer/devcontainer.env",
    "--cap-add=NET_ADMIN",
    "--device=/dev/net/tun"
  ],
  "initializeCommand": "test -f .devcontainer/devcontainer.env || cp .devcontainer/devcontainer.env.sample .devcontainer/devcontainer.env",
  "onCreateCommand": "bash .devcontainer/scripts/onCreateCommand.sh ${containerWorkspaceFolder}",
  "remoteUser": "vscode",
  "containerUser": "vscode"
}
```

---

## Codespaces vs Local Behavior

| | Codespaces | Local VS Code |
|-|-----------|--------------|
| Secret source | Repository Codespaces secrets | `.devcontainer/devcontainer.env` |
| Mechanism | `"secrets"` block | `--env-file` in `runArgs` |
| `devcontainer.env` | Not read (env injected by Codespaces) | Must exist and be filled in |
| WireGuard `--device` | Not needed | Works on Linux/macOS hosts |

When both mechanisms are present, Codespaces uses the `"secrets"` block and ignores the `--env-file` (since `devcontainer.env` doesn't exist in the Codespaces workspace). Local VS Code uses the `--env-file` and ignores the `"secrets"` block.
