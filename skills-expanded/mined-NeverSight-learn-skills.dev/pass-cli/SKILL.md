---
name: pass-cli
description: >
  Safely retrieve Proton Pass secrets or inject them into a command or protected
  config file with pass-cli, including scoped Agent-token session recovery.
disable-model-invocation: false
---

# Pass CLI — Safe Secret Consumption

Use Proton Pass secrets by the least-exposing route. This skill covers finding
an accessible secret, passing it to a process, or rendering a requested local
config file. It does **not** administer vaults, shares, agents, or access
permissions: those are owner actions with a larger blast radius.

## Choose the route before reading anything

| Need | Use |
| --- | --- |
| A program needs a secret, but the agent does not | `pass-cli run` with a `pass://` reference. This is the default. |
| A requested config artifact needs a secret | `pass-cli inject` to an explicit file path. This writes secret material to disk. |
| The task genuinely requires the value in context | `pass-cli item view --field`. Retrieve one field only. |

Never use `pass-cli run --no-masking`. Do not read a full item merely to pass a
secret to another command. Do not put a resolved value in a shell command,
source file, commit, ticket, or final response.

## Session health and recovery

Run the intended command first; do not preflight it. Recover **only** for a
clear authentication error such as `not authenticated`, `session expired`,
`invalid session`, or `401`. Item-not-found, vault-not-found, and permission
errors need discovery or an owner access change—not re-authentication.

The owner must have already created a private environment file containing the
Agent PAT. Never create, print, inspect, or change that file. On authentication
failure, run this recovery and the original command in the **same shell** so
that the isolated session directory applies to both:

```bash
if [ ! -r "$HOME/.pass-cli-env" ]; then
  printf '%s\n' 'FATAL: pass-cli Agent credentials are not configured for this user.' >&2
  exit 1
fi

# The file is owner-managed and must not be printed.
. "$HOME/.pass-cli-env"
: "${PROTON_PASS_PAT:?FATAL: PROTON_PASS_PAT is not configured}"

export PROTON_PASS_SESSION_DIR="${PASS_CLI_AGENT_SESSION_DIR:-$HOME/.local/share/pass-cli-agent}"
(umask 077; mkdir -p "$PROTON_PASS_SESSION_DIR")

# This isolated session may safely be discarded without affecting a human session.
pass-cli logout --force || printf '%s\n' 'No reusable Agent session to discard; continuing with login.' >&2
PROTON_PASS_PERSONAL_ACCESS_TOKEN="$PROTON_PASS_PAT" pass-cli login
pass-cli info

# Retry the original command here, with its required reason if it reads an item.
```

Do not echo `$PROTON_PASS_PAT` or pass it by a command-line flag. Keep
`PROTON_PASS_SESSION_DIR` set for every later `pass-cli` invocation; separate
shell/tool calls do not retain an earlier `export`.

If login fails because secure key storage is unavailable (common in a headless
container), stop and explain the error. The owner may deliberately choose the
documented `PROTON_PASS_KEY_PROVIDER=fs` fallback; do not enable it silently,
because it stores the local encryption key on disk.

## Discover precise identifiers

Discovery exposes item metadata, so list only the scope needed for the task.
Use JSON when parsing it.

```bash
pass-cli vault list --output json
pass-cli item list --vault-name "Vault Name" --output json
```

Once found, prefer the vault share ID and item ID for automation. Names are
convenient for an interactive one-off, but duplicate vault or item names can
resolve to the wrong object.

## Give a process a secret without exposing it

Use a field-level reference in an environment variable, then run the target as
a child process. `pass-cli` replaces the reference only for that child and
masks resolved values in its output by default.

```bash
export DEPLOY_TOKEN='pass://SHARE_ID/ITEM_ID/token'
pass-cli run -- ./deploy.sh
```

For project configuration, keep only references in a gitignored env file:

```dotenv
DATABASE_PASSWORD=pass://SHARE_ID/ITEM_ID/password
```

```bash
pass-cli run --env-file .env.secrets -- ./start-server
```

A TOTP reference resolves to the current code. Use `?totp=uri` only when the
task explicitly requires the underlying `otpauth://` URI.

## Render a requested configuration file

`inject` materializes secrets. Only use it when the task explicitly needs that
file, choose an explicit output path, and keep the default `0600` permissions.
Never write the result to stdout.

```yaml
# app-config.yaml.template
api_token: '{{ pass://SHARE_ID/ITEM_ID/token }}'
```

```bash
pass-cli inject \
  --in-file app-config.yaml.template \
  --out-file .runtime/app-config.yaml
```

Do not use `--force` unless the user has explicitly approved overwriting that
specific file. Treat the generated file as secret material: do not commit it.

## Read one field only when its value is necessary

An Agent-token operation that views an item requires a non-empty reason (at
most 300 characters). State the concrete task purpose; never include a secret
in the reason.

```bash
PROTON_PASS_AGENT_REASON="Use the deploy token for the requested release" \
  pass-cli item view --share-id "SHARE_ID" --item-id "ITEM_ID" --field token
```

If you need to discover field names, a full item view is allowed only when the
field cannot be identified otherwise. Give it the same reason and do not repeat
the resulting values in your response.

## Audit boundary

The account owner can inspect Agent accesses with:

```bash
pass-cli agent monitor "agent-name" --output json
```

Do not create, renew, delete, grant, or revoke Agents/PATs as part of a secret
retrieval task. Ask the owner to provision the narrowest possible, expiring
viewer access—ideally to the single required item—when access is missing.

## Quick reference

```bash
pass-cli vault list --output json
pass-cli item list --vault-name "Vault Name" --output json
pass-cli run --env-file .env.secrets -- ./command
pass-cli inject --in-file template --out-file .runtime/config
PROTON_PASS_AGENT_REASON="..." pass-cli item view --share-id ID --item-id ID --field field
pass-cli info
pass-cli test
```
