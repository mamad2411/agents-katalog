---
name: op-setup
description: Install the 1Password CLI, connect it to the desktop app, sign in, scope vault permissions, and enable the Environments MCP server. Use when op commands fail with auth errors or on first-time setup.
---

# 1Password developer setup

## Install the CLI

```bash
brew install 1password-cli    # macOS
op --version                  # 2.x
```

Linux and Windows installers are on developer.1password.com. Keep the CLI
current; secret reference features track CLI releases.

## Connect to the desktop app (interactive use)

1. Install the 1Password desktop app and sign in.
2. App Settings > Developer > enable "Integrate with 1Password CLI".
3. Now `op vault list` triggers a biometric/app approval instead of passwords
   in the terminal.

Sign-in fallback without the app integration:

```bash
op account add --address my-team.1password.com --email you@example.com
eval $(op signin)     # session token in your shell, expires after inactivity
op whoami
```

Prefer the app integration on workstations: no long-lived session tokens in
shell state.

## Service accounts (CI, servers, agents)

Create in the 1Password admin console (Developer > Service Accounts):

1. Name it for the system it serves (`ci-deploy`, `staging-runner`).
2. Grant access to the minimum vaults, read-only where possible.
3. Store the issued token in your CI secret store as
   `OP_SERVICE_ACCOUNT_TOKEN`; it is shown once.

With that env var set, `op` commands and `op run` work headlessly. Note that a
few interactive commands (account management) are unavailable to service
accounts by design.

## Vault permission model

- Vault per environment (dev/staging/prod) and per blast-radius boundary.
- Humans get dev vaults; deploy systems get prod vaults; almost nobody needs
  both.
- Review vault access when rotating credentials: rotation without access
  cleanup only fixes half the incident.

## Environments MCP server (beta)

1Password publishes an official MCP server for 1Password Environments. It is
in beta, ships with the desktop tooling, and is documented at
https://www.1password.dev/environments/mcp-server. This plugin configures the
documented command:

```json
{ "mcpServers": { "onepassword": { "command": "1password-mcp" } } }
```

Key properties:

- Requires the desktop app, a 1Password account, and at least one Environment.
- Every action requires an explicit approval prompt in the 1Password app.
- Secrets are never returned to the client: the server manages Environments
  and injects values only into authorized processes at runtime, so agents can
  act on secrets without seeing them.
- Enterprise admins can enable or disable the MCP feature by policy; if the
  command is missing, the feature may be off or not yet rolled out to your
  platform, and the skills in this plugin still work via the plain op CLI.

## Troubleshooting

- `op: command not found` in MCP context: install the CLI and desktop app.
- Approval prompt never appears: the desktop app must be running and unlocked.
- `401` with service accounts: token revoked or vault grant missing.
- Session expired mid-script: switch that script to a service account.
