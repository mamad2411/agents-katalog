---
name: paperclip-board-token
description: "Generate a fresh Paperclip board API token via the CLI auth challenge flow. Use when the board token in ~/.env is expired or you need a new token for debugging Paperclip tasks. Paperclip runs on a K3s cluster ($PAPERCLIP_KUBE_CONTEXT, from ~/.env) — all API calls go through kubectl port-forward."
---

# /paperclip-board-token

Generate a fresh Paperclip board token using the CLI auth challenge flow.

## Prerequisites

Paperclip runs inside the K3s cluster named by **`$PAPERCLIP_KUBE_CONTEXT`** and is behind **Cloudflare Zero Trust Access**. Set up a port-forward before running any steps:

```bash
set -a; . ~/.env; set +a   # PAPERCLIP_KUBE_CONTEXT, PAPERCLIP_NAMESPACE, PAPERCLIP_PUBLIC_URL
kubectl --kubeconfig ~/.kube/config --context "$PAPERCLIP_KUBE_CONTEXT" -n "$PAPERCLIP_NAMESPACE" \
  port-forward deploy/paperclip 3100:3100 &
PORT_FORWARD_PID=$!
```

All API calls below target `http://localhost:3100` via this tunnel. Kill it when done:

```bash
kill $PORT_FORWARD_PID 2>/dev/null
```

## Usage

```
/paperclip-board-token                              # generate a new board token
/paperclip-board-token --store                      # generate and store the new token in ~/.env
/paperclip-board-token --help                       # show this help
```

## What You Must Do When Invoked

### Step 1 - Create the challenge

```bash
curl -s "http://localhost:3100/api/cli-auth/challenges" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"clientName":"opencode","command":"board"}' | jq .
```

This returns a JSON object with:
- `boardApiToken` — the fresh board token (e.g. `pcp_board_...`) — **available immediately**
- `token` — the CLI auth secret (used for approval/polling)
- `approvalPath` — the path component of the approval URL
- `approvalUrl` — the full localhost URL (do NOT use this for approval — see Step 2)
- `expiresAt` — when this challenge expires

### Step 2 - Approve the challenge

**Critical:** Paperclip is behind Cloudflare Zero Trust Access. The approval URL must use the **real hostname** so the user's Cloudflare session is recognized. Construct the approval URL from `approvalPath` and `token` but use `$PAPERCLIP_PUBLIC_URL`:

```
$PAPERCLIP_PUBLIC_URL/cli-auth/<challengeId>?token=<cliToken>
```

Tell the user:

```
Open this URL in your browser to approve the challenge:
$PAPERCLIP_PUBLIC_URL/cli-auth/<challengeId>?token=<cliToken>

This links the token to your signed-in session so it persists.
```

Wait for the user to confirm they've approved it, then poll:

```bash
curl -s "http://localhost:3100/api/cli-auth/challenges/<challengeId>?token=<cliToken>" | jq .
```

When `status` is `"approved"`, the token is linked to the user's session.

> **Note:** The port-forward may drop during polling. If polling fails, proceed anyway — the `boardApiToken` is available immediately from the challenge response. Approval links it to your Cloudflare session for persistence, but the token works regardless.

### Step 3 - Store the token (if --store was passed)

If the user passed `--store`, update the `PAPERCLIP_BOARD_TOKEN` line in `~/.env` (append it if missing):

```bash
TOKEN=<boardApiToken>
ENV_FILE=~/.env
if grep -q '^PAPERCLIP_BOARD_TOKEN=' "$ENV_FILE"; then
  sed -i "s|^PAPERCLIP_BOARD_TOKEN=.*|PAPERCLIP_BOARD_TOKEN=${TOKEN}|" "$ENV_FILE"
else
  echo "PAPERCLIP_BOARD_TOKEN=${TOKEN}" >> "$ENV_FILE"
fi
chmod 600 "$ENV_FILE"
```

Report the new token to the user.

> **No poll required:** You can store the `boardApiToken` immediately after the user confirms approval, even if polling the port-forward fails. The token is valid and will work for API calls.

### Step 4 - Report the token

If `--store` was not passed, report the token without modifying any files:

```
New board token: pcp_board_<token>
Expires: <expiresAt>
```

## Guardrails

- Never hard-code the token in output beyond what's necessary
- The challenge expires in 10 minutes — if the user takes too long, create a new one
- Only overwrite `~/.env` when the user explicitly passes `--store`
- The token is a bearer token — treat it like a password
- The `boardApiToken` is available immediately after challenge creation; approval only links it to the user's session for persistence
- The port-forward may be unstable; the `boardApiToken` can be stored directly from the challenge response without waiting for a successful poll. Polling is only needed to confirm the approval status, not to use the token.
- **Always use the real hostname (`$PAPERCLIP_PUBLIC_URL`) for the approval URL** — the localhost port-forward URL will redirect to Cloudflare login and fail because the user's session cookies don't work over port-forward
