---
name: boost-connect-qbd
description: Manage, diagnose, and verify Boost Connect QuickBooks Desktop integrations through the public API and bundled CLI. Use when a developer needs to install the skill, authenticate with a Developer API Key, choose Admin or Custom API-key scopes and project access, create or inspect connections, generate hosted setup, verify QuickBooks Web Connector health, read or write supported QBD data, configure webhooks, troubleshoot authentication or connector failures, or prove an integration works end to end.
---

# Boost Connect QBD

## Install, Then Run

Install this skill once with the exact `npx skills add ...` command published for its Git source. Skill distribution and API configuration are separate; installing a skill never grants API access.

Run commands relative to the installed skill folder, not the caller's repository. In the directory containing this `SKILL.md`, set a portable command for the current shell:

```bash
export BOOST_CONNECT_QBD_SKILL_DIR="$PWD"
bcqbd() { node "$BOOST_CONNECT_QBD_SKILL_DIR/scripts/boost-connect-qbd.mjs" "$@"; }
bcqbd help
```

Use `bcqbd` below. If the shell function is unavailable, run `node "$BOOST_CONNECT_QBD_SKILL_DIR/scripts/boost-connect-qbd.mjs" <command>`.

## First-Run Flow

1. Have an account owner open the portal's `/keys` page and create a **Developer API Key**. It is an opaque bearer secret, not a portal JWT or browser session token.
2. Choose **Admin** for every public developer scope, or **Custom** and select only needed scopes. Assign one or more projects. Read [references/authentication.md](references/authentication.md) before choosing.
3. Copy the secret once into a private terminal. Never paste it into chat, source code, a URL, or a command argument.

   ```bash
   printf '%s' "$BOOST_CONNECT_QBD_TOKEN" | bcqbd auth login --token-stdin
   ```

4. Prove identity and discover accessible connections.

   ```bash
   bcqbd whoami
   bcqbd connections list
   ```

5. Prove a selected connector and a live QuickBooks read.

   ```bash
   bcqbd doctor --connection-id <connection-id> --verify-qbd
   ```

`doctor --connection-id <connection-id>` needs Admin or Custom scope `diagnostics:read`. Adding `--verify-qbd` also needs `qbd:read` because it performs a live CompanyQuery through the selected connection. It proves more than edge reachability.

## Choose Workflow

- Diagnose setup, credentials, connection ownership, or Web Connector health: run `doctor`; read [references/diagnostics.md](references/diagnostics.md) if a check fails.
- Inspect or manage projects, connections, hosted setup, webhooks, or QuickBooks data: read [references/workflows.md](references/workflows.md).
- Call an operation not exposed as a named CLI command: read its public OpenAPI `x-required-permissions`, then use `request`.

```bash
bcqbd request \
  --path /api/qbd/v1/company \
  --connection-id <connection-id>
```

For a JSON write body, pipe it over stdin and add `--body-stdin`. Never put credentials in the body.

## Operational Rules

- Treat account, project, connection, key, operation, and QuickBooks record IDs as opaque.
- Require both an assigned project and all required scopes for every public API call. Do not substitute a portal JWT for a Developer API Key.
- Confirm before creating, updating, deleting, revoking, regenerating, or writing QuickBooks data unless the user explicitly requested that mutation.
- Never call paths containing `/internal/`, `/setup-callbacks/exchange`, `/setup-sessions/`, `/usage/api-calls`, or `/qbwc/`.
- Never retry a write blindly. Inspect the response or operation state first to avoid duplicate QuickBooks transactions.
- Treat QuickBooks Desktop work as asynchronous. A healthy edge API does not prove Web Connector has checked in or QuickBooks accepted the request.
- Pass a connection ID exactly once, using `--connection-id` or the OpenAPI path as required.
- Report credential identity without secrets, selected project and connection IDs, connector health, operation or record ID, HTTP status, and any remaining gap.

## Verification Standard

After a change:

1. Run `bcqbd doctor --connection-id <id> --verify-qbd` when a live QuickBooks read is required.
2. Read back the changed resource.
3. For QuickBooks writes, wait for the terminal operation result and confirm the returned QuickBooks record ID.
4. State separately whether the API, connector, and QuickBooks application passed. Do not collapse them into a generic success claim.
