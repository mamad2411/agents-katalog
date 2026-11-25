---
name: kei-credential-rotation
description: Rotate or revoke a Kei runtime installation credential (the KEI_RUNTIME_TOKEN a kei-proxy runtime authenticates with) without leaking it and with a planned cutover, using `kei bot credential --rotate` or the console's Rotate button. Use whenever someone wants to rotate, re-mint, replace, roll, or revoke a Kei runtime token or installation credential, suspects one leaked, sees a bootstrap without workspace_id, or asks how key rotation works in Kei — including when they just say "rotate the Kei keys".
---

# Rotate a Kei runtime credential

This is a workflow skill. Rotation is admin work done with `kei`, the platform
admin CLI (`kei-cli` skill); the runtime (`kei-proxy`, used by agents) only
consumes the new token and is restarted and re-bootstrapped afterwards
(`kei-proxy` skill). This skill owns the cutover order and the checks.

The safe order, in short: run `kei login` (owner/admin), confirm the
installation with `kei bot status --installation INSTALLATION_ID` (it must be
`pending` or `active`; when you are not sure which installation ID is the right
one, this is the first check), then pipe `kei bot credential --rotate` straight into
the secret manager (never print or paste the token). Restart the runtime,
re-bootstrap, check `workspace_id` and the heartbeat, and confirm the old token
now fails closed. Do not keep the old token value after that check. Rotation
is immediate: there is no overlap window. Every `kei bot` command needs
`kei login` first, so list it as step 1.

To kill a leaked credential when downtime is acceptable, run
`kei bot delete --installation INSTALLATION_ID --yes` or rotate immediately.
Both invalidate the old token at once.

If bootstrap output is missing `workspace_id` after a rotation, rotate again with
`kei bot credential --installation INSTALLATION_ID --workspace WS --rotate`. The
`--workspace` flag re-scopes the credential to that workspace.

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Installed binary | `kei help` (look for `--rotate` on `bot credential`) | Whether this release supports CLI rotation |
| Docs: CLI authentication and identity | `https://docs.haikeilabs.com/kei/reference/cli` | Credential handling rules |
| Docs: Runtime installations | `https://docs.haikeilabs.com/kei/runtime/tenant-runtime` | Runtime credential management |

Append `.md` to any docs page URL for the raw page.

## Which secret?

Kei has two kinds of secret a runtime can hold. Know which one the user means
before doing anything:

| Secret | Looks like | Minted by | Rotate with |
| --- | --- | --- | --- |
| Runtime installation credential | `KEI_RUNTIME_TOKEN` for an installation | `kei bot credential`, or the console's installation reveal | This skill: `kei bot credential --rotate` or console **Rotate** |

## What rotation actually does

Rotation replaces the credential **in place**: the control plane swaps the
stored hash for the new one in a single update. The old token stops working
the moment rotation succeeds — there is no overlap window and no grace period.
Only `pending` or `active` installations can be rotated.

That makes rotation a cutover, not a background task. The running runtime will
start failing its next heartbeat and every protected call until it is restarted
with the new token. Plan the order so that gap is seconds, not hours.

## Before rotating

1. **Log in.** `kei bot credential` uses the operator's CLI token, so run
   `kei login` first (owner/admin only; a
   browser approval the user must complete). The token is short-lived and
   per-environment — re-run login on `not logged in; run kei login first` or a
   401, log in again.
2. **Confirm the installation.** `kei bot status --installation INSTALLATION_ID`
   — check it is the right name and environment, and that it is `pending` or
   `active`.
3. **Know where the runtime reads its token.** Identify the secret-manager
   entry and how the runtime is restarted (deployment rollout, service
   restart). If you cannot say how the runtime picks up the new value, stop and
   find out; rotating without that answer causes an outage.
4. **Tell the user about the gap** and get a go-ahead if the runtime serves
   real traffic.

## Rotate

Pipe the new credential straight into the secret manager. The CLI refuses to
write it to an interactive terminal, which is the point — never redirect it to
a file in the repo, echo it, or paste it into the conversation.

```sh
kei bot credential --installation INSTALLATION_ID --workspace WS --rotate | <your secret-manager import command>
```

`--workspace` accepts a workspace name or ID and re-scopes the rotated
credential. If omitted the existing workspace scope is preserved.

Web alternative: **Agents → Runtime installations → Rotate**. The new value is
revealed once; copy it directly into the secret manager.

Then immediately:

1. Get the new token to where the runtime reads it, and restart:
   - **Workstation runtime** (set up with `kei setup`): the token also lives in
     `~/.config/kei.yaml`. Pipe the new token from the secret manager into
     `kei setup` (`<secret-manager read> | kei setup --control-plane-url URL`)
     so nobody pastes it, then restart the harness.
   - **Deployed runtime**: restart or roll it so it reloads `KEI_RUNTIME_TOKEN`
     from the secret manager.
2. Re-run bootstrap and check the output:

   ```sh
   kei runtime bootstrap | jq '{installation_id, status, binding_status, workspace_id}'        # workstation
   kei-proxy runtime bootstrap | jq '{installation_id, status, binding_status, workspace_id}'  # deployed runtime
   ```

   `workspace_id` must be present. Rotation re-scopes the credential to the
   installation's workspace, which is also the fix for an old credential whose
   bootstrap lacked `workspace_id`.
3. Confirm the heartbeat process is running again and
   `kei bot status --installation INSTALLATION_ID` shows it fresh.
4. Verify the old token is dead: a protected call or bootstrap with the previous
   value (if it is still retrievable from a secret-manager version) must fail
   closed. Do not keep the old value around longer than this check needs.

## Revoking instead of rotating

If the credential leaked and the runtime can stay down, deleting the
installation revokes its credential immediately:

```sh
kei bot delete --installation INSTALLATION_ID --yes
```

This removes the control-plane installation entirely (agents detach, a new
`kei bot init` is needed to come back). It does not touch customer cloud
resources or the secret-manager entry — clean those up separately. Prefer
rotation when the runtime needs to keep serving.

## Validation commands

```sh
kei help                                          # confirms --rotate is supported by this release
kei bot status --installation INSTALLATION_ID
kei-proxy runtime bootstrap | jq '.workspace_id'  # must not be null
```

The **Keys** page no longer exists. Agent keys were deprecated in favor of the
runtime installation credential for all runtime operations. Only
`KEI_RUNTIME_TOKEN` is used today.

## Realistic usage boundaries

- Never print, log, paste, or pass a credential as a command-line argument.
  Never ask the user to paste one into the chat.
- There is no dual-credential or staged rotation. Do not promise zero downtime.
- Rotation does not change the installation ID, its agents, or its binding.
- A rotated credential for a `disabled` or `revoked` installation is refused;
  re-create the installation instead.
