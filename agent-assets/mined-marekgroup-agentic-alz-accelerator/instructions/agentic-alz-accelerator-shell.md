---
applyTo: "**/*.{sh,bash}"
---

# Shell Script Conventions

## Style

- Use `#!/usr/bin/env bash` shebang
- `set -euo pipefail` at the top
- Quote all variables: `"$var"`
- Use `[[ ]]` for conditionals, `$()` for command substitution

## Azure CLI

- Use `az login` with OIDC or managed identity — never interactive login in CI
- Use `--output json` for parsing, `--output table` for display
- Always specify `--subscription` explicitly

## Security

- Never echo credentials or tokens
- Use `az keyvault secret show` to retrieve secrets at runtime
- Never commit `.env` files with real values
