---
name: snyk-setup
description: Install the Snyk CLI, authenticate, pick an organization, and wire up the MCP server and CI. Use when Snyk commands fail with auth errors or the user is starting from zero.
---

# Snyk setup

## Install the CLI

```bash
npm install -g snyk        # any platform with Node
brew install snyk-cli      # macOS
snyk --version             # want v1.1298.0 or later for MCP support
```

No global install needed if you use `npx -y snyk@latest ...` (the MCP config in
this plugin does exactly that).

## Authenticate

```bash
snyk auth
```

Opens a browser OAuth flow and stores the token locally. For headless machines
and CI, set a token instead:

```bash
export SNYK_TOKEN="<token>"
```

Get the token from the Snyk web UI under Account Settings, or use a service
account token for CI (preferred: revocable, org-scoped, not tied to a person).
Never commit the token; inject it from your secret manager or CI secret store.
Verify auth with `snyk whoami --experimental`.

## Organization selection

Scans report into an org. Set the default:

```bash
snyk config set org=<ORG_ID_OR_SLUG>
```

Or per command with `--org=<ORG>`, or via env `SNYK_CFG_ORG` (this is the
variable the MCP server respects too). Find org IDs in the Snyk UI under
Settings.

## MCP server

This plugin starts the official server with:

```bash
npx -y snyk@latest mcp -t stdio
```

Notes:

- stdio is the recommended transport for local use; `-t sse` exists for HTTP.
- The server reuses your CLI auth; run `snyk auth` once first, or export
  `SNYK_TOKEN` in the environment Caeros launches from.
- Add `-d` for debug logs when tools fail silently.
- On first scan of a folder you may need to accept folder trust; a disable
  flag exists for headless workflows (see Snyk docs).

## CI wiring (minimal)

```yaml
# any CI: fail on high+ new issues, monitor on main
- run: npx -y snyk@latest test --severity-threshold=high
  env: { SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }} }
- run: npx -y snyk@latest monitor
  if: branch == main
```

## Troubleshooting

- `401`/`Unauthorized`: token missing or revoked; rerun `snyk auth`.
- `3` exit code: no supported manifest found; check working directory.
- Wrong org in UI: set `--org` explicitly; config default beats token default.
- Proxy environments: honor `HTTPS_PROXY`; the CLI respects standard env vars.
