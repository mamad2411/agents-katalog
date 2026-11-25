---
name: onepassword-herdr
description: "Use 1Password CLI to inspect vault access, manage service-account scopes, and store credentials from a human-authenticated Herdr pane. Apply when a task combines op CLI access with Herdr or a service account; use the general secrets-handling skill for unrelated credential work."
---

# 1Password CLI with Herdr

Use the installed `op` CLI for vault and service-account operations. Use Herdr only when the required human 1Password session is available in another pane. The caller must explicitly request Herdr before inspecting or controlling its session. Skill invocation does not authorize a vault permission change, new service account, credential rotation, or account retirement; make only the mutation the user requested.

## Check identity and authority

Before a read or write, inspect the identity used by the exact command. A shell can contain both a human `OP_SESSION_*` variable and `OP_SERVICE_ACCOUNT_TOKEN`; the service-account token takes precedence. Check variable names without printing their values, then run `op whoami`.

```bash
env | cut -d= -f1 | rg '^OP_'
op whoami
```

Use `env -u OP_SERVICE_ACCOUNT_TOKEN op whoami` to verify a human session in a shell that has both. Do not assume a successful `op whoami` is human. Never print, log, or paste token values.

For Herdr operations, first confirm `HERDR_ENV=1`, read the installed `herdr --help` and pane command help, and inspect the current pane and its neighbor. Read the target pane before running a command. Use the pane ID returned by Herdr, and use `herdr pane run <pane-id> <command>` only when that pane is at a shell prompt. Do not focus or interrupt the user's pane. The Herdr skill has the full pane-control rules.

## Vault access

Distinguish human vault permissions from service-account scope:

- Human permissions use `op vault user grant --vault <vault> --user <user> --permissions allow_viewing,allow_editing`. Resolve the human with `op user list`; do not hardcode an identity. Avoid `allow_managing` unless the user specifically requests vault management.
- Service-account permissions are set when creating the account: `op service-account create <name> --vault '<vault>:read_items,write_items'`. `write_items` requires `read_items`.
- Service-account vault scope is immutable after creation. Do not try a human `op vault user grant` command to alter a service account. If the requested change requires a different scope, explain that replacement is required and inspect consumer usage before rotating an existing account. Do not create a parallel account without clear authority to replace or add one.

Read [references/service-accounts.md](references/service-accounts.md) before creating, replacing, or rotating service accounts.

Verify the human grant with:

```bash
op vault user list '<vault>' --format json
```

Verify service-account access by using that account to read the intended vault and, when authorized, perform the intended item write. A human grant listing does not prove service-account access.

## Store credentials safely

`op service-account create` returns a newly generated token only once. Capture it without echoing it, then store it in the intended vault immediately. Do not put secrets in command arguments, shell history, temporary plaintext files, chat, or routine output. Use stdin, a narrowly scoped environment variable, or a file descriptor to pass a secret to a process.

For sensitive item fields, prefer an item JSON template through stdin:

```bash
op item template get 'API Credential'
```

Populate the `credential` field in memory and pipe the JSON to `op item create --vault '<vault>' -`. Do not use `--reveal` for verification. Confirm item title, vault, category, and permissions with metadata-only commands such as `op item list` and `op item get --format json`.

Do not `source` an application `.env` file to read a credential. Parse only the required key without printing it, and pass the value to the 1Password process through stdin or an environment variable. Avoid changing application secret references unless the runtime supports the relevant `op://` injection workflow.

## Stop conditions

Stop before a mutation when the active identity is unclear, the required human session is absent, the vault is inaccessible, the requested account has unknown consumers, or the operation would expose or replace a live credential without a verified recovery path. Report the exact missing condition and preserve existing access.
