---
name: kei-cli
description: "The `kei` platform-administration CLI for Kei (run by an org owner/admin, not by agents) — install/upgrade, login, runtime installations, agent moves, workspaces, groups, users, service principals, directory sync, policies (`kei policy`, with deprecated `kei policies` alias), connectors, harness management, model profiles, credential store, and Haikei skill installation for supported harnesses (`kei connect claude-code|codex|opencode|pi|cursor`). Load before running or suggesting any `kei` command. Policy sources are groups or `autogroup:member` / `autogroup:admin`; direct access uses ID-based grants. Check installed help for exact syntax. For runtime tool-call authorization, use kei-proxy instead."
---

# kei CLI

Check `kei --version` and `kei help` for the installed binary before relying
on command syntax. The installed help is authoritative; release contents and
bundled `kei-proxy` versions can change independently.

`kei` is the Kei **platform administration** CLI. It authenticates an org
owner/admin and manages **runtime installations** — the identity a
customer-hosted runtime uses. It is not how agents interact with Kei at run
time; that is `kei-proxy`.

| | `kei` — platform admin (this skill) | `kei-proxy` — runtime for agent interaction |
| --- | --- | --- |
| Who runs it | A person: org `owner`/`admin` | The harness — as a `kei-proxy serve` daemon over a Unix socket (primary, through the agentware socket client), or as a one-shot CLI subprocess per protected operation (fallback with no daemon) |
| Auth | `kei login` → CLI token in the OS keychain | `KEI_RUNTIME_TOKEN` in the harness environment |
| Jobs | Login, installations, runtime credentials, bind, agents-on-installation | Allow/deny each tool call (socket `POST /v1/authorize`, or `kei-proxy authorize`), protected connector calls (credential release), heartbeat, audit shipping |
| Skill | `kei-cli` | `kei-proxy` |

If the task is "make the agent's tool call go through Kei" or "check whether
the agent may do X", the answer is kei-proxy (`kei-proxy serve` with the
agentware socket client; `kei-proxy authorize` as the no-daemon fallback) —
load `kei-proxy`, not this skill. An agent never needs `kei login` to do its work. `kei setup`
and `kei runtime bootstrap` are the only bridge: admin conveniences that write
local runtime config and invoke `kei-proxy` to verify it.

## Answer checklist

For these common questions, include every listed point directly in the answer;
do not leave it implicit or rely on a link to the reference:

- **Resource commands:** check the exact subcommand in `kei help`. If a command
  such as `kei policy update` is absent, say it is not available in that
  release and refer to the `kei-api` skill; do not invent it. Explain opaque
  page tokens for `list` and PATCH with an update mask for a supported
  `update`.
- **Per-user OAuth:** say `kei connectors connect` is for the authenticated
  user's own account, never prints a token, and cannot connect another user's
  account. Say each user must run `kei login` and then `kei connectors connect`
  for their own account.
- **Manifest review:** `kei connectors manifests show` displays added (`+`),
  removed (`-`), and changed (`~`) tools. Only an org owner or admin can
  approve with `kei connectors manifests approve`; it needs the manifest ID
  and asks for confirmation unless `--yes` is used in a script.
- **Tool-call authorization:** say `kei-proxy serve` decides calls for a
  long-lived service; `kei-proxy authorize` is the fallback when no daemon is
  running. The agent does not use `kei login`; runtime authentication uses
  `KEI_RUNTIME_TOKEN`.
- **Harness policy model:** state that policies can use only a custom group
  (`group:<name>` or a bare name), `autogroup:member`, or `autogroup:admin`.
  Owners count as admins; there is no `autogroup:owner` or agent policy
  source. Custom groups can hold users, agents, and service principals. Org
  roles are console-only. Never use email in a policy. Direct access requires
  an ID-based grant with expiry, reason, and approver. Any matching deny wins;
  there is no priority; say exactly “Bindings are wiring between resources;
  they do not authorize access.” Refer to the Policies and Groups reference in
  the Kei console. Use `kei policy migration-report --workspace WS` to review
  legacy policy rules; it is read-only. If specifically asked about the
  deprecated native-config import, explain `--from` selects the harness and
  required `--src` selects the source pattern; preview is the default and
  `--apply` creates proposals. Those harness-based sources are not valid in the
  final model, so do not apply them as current rules.

Your knowledge of `kei` flags and subcommands may be outdated; the CLI is young
and changes between releases. **Prefer retrieval over this file.**

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Installed binary | `kei help`, `kei <command> --help`, `kei bot` (lists subcommands) | Exact commands, flags, and allowed values for the version actually installed |
| Kei docs | `https://docs.haikeilabs.com/kei/get-started/sign-in`, `https://docs.haikeilabs.com/kei/reference/cli` (CLI authentication and identity), `https://docs.haikeilabs.com/kei/runtime/tenant-runtime` (proxy runtime) | The customer-facing, supported workflow |
| Published release | `https://kei-cli-releases.s3.us-east-1.amazonaws.com/kei-cli/latest.txt` | Current released version and installer |
| Release endpoint | `https://kei-cli-releases.s3.us-east-1.amazonaws.com/kei-cli/latest.txt` | Latest published version |

Append `.md` to any docs page URL for the raw page.

When this skill and `kei help` disagree, **trust `kei help`** and mention the
difference to the user.

## FIRST: check that `kei` is installed

```sh
kei --version     # prints "kei <version>"
```

If `kei --version` prints kubectl or AWS errors instead of a version, the name
is shadowed by an alias — oh-my-zsh's kubectl plugin defines
`alias kei='kubectl edit ingress'`. Diagnose with `type -a kei`; fix with
`unalias kei` after `source $ZSH/oh-my-zsh.sh` in `~/.zshrc`, or run
`command kei` or the full path (`~/.local/bin/kei`).

If it is missing, install with the checksum-verifying release installer
(macOS and Linux, arm64 and amd64). This is the recommended path:

```sh
export PATH="$HOME/.local/bin:$PATH"
curl -fsSL "https://haikeilabs.com/install.sh" \
  | sh -s -- -d "$HOME/.local/bin"
kei help && kei --version
```

If `haikeilabs.com` is unreachable, use the S3 fallback:
```sh
curl -fsSL "https://kei-cli-releases.s3.us-east-1.amazonaws.com/kei-cli/install.sh" \
  | sh -s -- -d "$HOME/.local/bin"
```

The installer is POSIX `sh` (it runs under `sh`, `bash`, and `dash` alike);
pipe to `sh`, not `bash`. Pin a release with `-v VERSION` (no leading `v`,
e.g. `-v 0.1.5`). Rerun the installer to upgrade. Since v0.1.4 the release
archive also carries a pinned `kei-proxy` (the runtime), and the installer puts
it next to `kei`, so a workstation gets both binaries from one install. The
bundled `kei-proxy` version is pinned in the `kei-cli` repo (the
`KEI_PROXY_VERSION` file) and verified against the release at build time, so the
proxy version is deterministic per release. `go install` builds only `kei`.

Two more installer modes exist (POSIX `sh`, same checksum verification):

```sh
# Install only kei-proxy (the runtime), pinned to KEI_PROXY_VERSION by default,
# with its own -v to pick a different version:
curl -fsSL "https://haikeilabs.com/install.sh" \
  | sh -s -- --proxy-only -d "$HOME/.local/bin"

# Remove exactly the files the installer recorded in .kei-install-manifest:
curl -fsSL "https://haikeilabs.com/install.sh" \
  | sh -s -- --uninstall -d "$HOME/.local/bin"
```

`--proxy-only` and `--uninstall` are mutually exclusive. The `--proxy-only`
default version resolves from the `KEI_PROXY_VERSION` env var, a
`KEI_PROXY_VERSION` file in the current directory, or the copy published
alongside `install.sh`.

Use the published release installer above; build commands are not part of this
public operator guide.
## FIRST: log in

Every `kei bot …` command calls the control plane with the operator's CLI
token. Log in before any of them:

```sh
kei login                                                       # opens a browser
kei login --no-browser                                          # headless: prints URL + code
```

- It is an OAuth **device flow**. The CLI prints a URL and a verification code;
  a person approves it in a signed-in browser. As an agent, run the command,
  show the user the URL and code, and wait — you cannot approve it for them.
- Only an org `owner` or `admin` can complete approval. Others can start the
  flow but are refused with `403 organization administrator role is required`.
  Don't hand the CLI to a non-admin.
- The token is bound to the organization chosen at approval and to the API URL
  host (default `https://app.haikeilabs.com`, or `KEI_WEB_URL`). Login again
  if switching environments.
- The token goes to the OS keychain (service `kei-cli`, account = API host).
  It is never printed and never written to a config file.
- It is short-lived. `not logged in; run kei login first` or a 401 mid-session
  means log in again and retry.
- Diagnosing `not logged in` after an earlier login: give both causes. The
  token is short-lived, so a login from yesterday has likely expired; and it
  is per environment (per API host), so a staging login is not a production
  login. Either way, run `kei login` again against the host you mean.
- `kei logout` removes the local keychain entry only; it does not
  revoke the token server-side. Safe to repeat.

Commands that do **not** need `kei login`: `kei setup`, `kei runtime
bootstrap`, `kei upgrade`, `kei help`, `kei --version`. The first two
authenticate with the runtime token instead.

## Troubleshooting: `kei login`

### 1. Browser lands on the Dashboard and the CLI keeps waiting

**Symptom:** You run `kei login`, the browser opens to the Kei
Dashboard instead of the approval page, and the CLI hangs waiting for approval.

**Cause:** You were not already signed in at `app.haikeilabs.com`. The SSO
sign-in flow loses the OAuth return address — a known bug (HAI-370).

**Fix:** Sign in at `app.haikeilabs.com` first, then run `kei login` again
and approve on the "Kei CLI approved" page.

### 2. macOS dialog "Keychain Not Found … app.haikeilabs.com"

**Symptom:** During `kei login` a macOS dialog appears saying "Keychain Not
Found" or referencing `app.haikeilabs.com`.

**Cause:** The `HOME` environment variable is overridden (common in sandbox
or CI environments), so macOS cannot find `~/Library/Keychains`.

**Fix:** Run `kei` with your real `HOME`, or — for a sandbox `HOME` —
create a symlink so the sandbox points to your real keychain:

```sh
ln -s ~/Library/Keychains /path/to/sandbox/Library/Keychains
```

Click **Cancel** on the dialog. **Never click "Reset To Defaults"** — that
recreates the login keychain and can break other applications.

### 3. "organization owner or admin role is required" (403)

**Symptom:** The approval page shows `403 organization owner or admin role
is required`.

**Cause:** Only org owners and admins can approve the `kei login` device
flow. A user with the `member` role (or no org membership) is refused.

**Fix:** Ask an org owner or admin to run `kei login` and approve it. The
CLI token is bound to the approver's org, not to the caller's browser
session.

Answer with the cause and the fix together: only owners and admins can
approve, a `member` role gets this 403, so ask an org owner or admin to run
`kei login` and approve it.

## Troubleshooting

### 4. `kei runtime bootstrap` fails with "mkdir /var/lib/kei-proxy: permission denied" on macOS

**Symptom:** Running `kei runtime bootstrap` on macOS fails immediately with
a filesystem error about `/var/lib/kei-proxy`:
```
Error: mkdir /var/lib/kei-proxy: permission denied
```

**Cause:** `kei-proxy` defaults to a Linux-style state directory
(`/var/lib/kei-proxy`) that does not exist on macOS and requires root to
create. The hard-coded default is a known bug (HAI-374).

**Fix:** Set `KEI_RUNTIME_STATE_DIR` to a user-writable directory with
restrictive permissions before running bootstrap:

```sh
export KEI_RUNTIME_STATE_DIR="$HOME/.kei/state"
mkdir -p "$KEI_RUNTIME_STATE_DIR"
chmod 0700 "$KEI_RUNTIME_STATE_DIR"
kei runtime bootstrap
```

The workaround is safe until a `kei-proxy` release ships a macOS-aware
default. The state dir holds transient runtime data (policy bundle cache,
heartbeat timestamps); `0700` ensures other processes on the machine cannot
read it.

### 5. `kei policy list` returns a decode error on kei ≤ 0.1.10

**Symptom:**
```
kei policy list --workspace my-workspace
```
returns a JSON decode error or a stack trace instead of the policy list.

**Cause:** `kei policies` before v0.1.11 sent a malformed request that the
server could not decode. The command crashes before printing any results
(HAI-373).

**Fix:** Upgrade kei to v0.1.11 or later. If you cannot upgrade, use the
web app at `app.haikeilabs.com` to view and manage policies.

Answer with all of it, and connect the bug to the error the user saw: "The
JSON decode error is the known kei ≤ 0.1.10 bug (HAI-373): the server could
not decode the request." Then: upgrade to v0.1.11 or later; until then, use
the web app.

For current policy commands, use the singular `kei policy` command group. The
plural `kei policies` remains a deprecated compatibility alias. Check the
installed command help for exact syntax. The human-facing policy model and
examples are in the Policies and Groups reference pages in the Kei console.

## Policies and access grants

Standing policies accept only these sources:

- A custom group, written as `group:<name>` or a bare group name. Custom
  groups can contain users, agents, and service principals.
- `autogroup:member` or `autogroup:admin`. Owners count as admins. There is no
  `autogroup:owner` source or standalone agent policy source.

Org roles are for console access, not policy sources. Never use an email address
in a policy. To give one person or agent direct access, create an access grant
for its ID; each grant needs an expiry, reason, and approver. Any matching deny
wins, with no priority. “Bindings are wiring between resources; they do not
authorize access.” For a human-facing explanation, direct admins to the
Policies and Groups reference in the Kei console.

Use the installed help as the syntax authority:

```sh
kei policy create -h
kei policy test -h
kei policy migration-report -h
kei access grant create -h
```

The installed CLI currently documents these forms:

```sh
kei policy create --workspace WORKSPACE --group GROUP --allow TARGET
kei policy create --workspace WORKSPACE --group GROUP --deny TARGET
kei policy test TARGET --workspace WORKSPACE --as autogroup:admin
kei access grant create --workspace WORKSPACE --principal user:USER_ID \
  --target TARGET --ttl 4h --reason REASON
kei policy migration-report --workspace WORKSPACE
```

The grant's `--ttl` sets its expiry. The authenticated operator is recorded as
approver; include a reason even where local CLI help marks it optional. The
migration report is read-only. For the human-facing explanation of groups,
grants, target types, and deny behavior, direct admins to the Policies and
Groups reference in the Kei console.

The deprecated `kei policies import` compatibility command imports local
harness rules. If asked about its old syntax, `--from` selects the harness and
required `--src` selects a source pattern; preview is the default and `--apply`
creates proposals. Harness-based sources are not valid in the final model, so
do not apply those proposals as current policy. Use the read-only migration
report to review legacy policy rows, then write a supported group policy.

```sh
kei policies import --from claude --src harness:* --workspace WORKSPACE
kei policies import --from claude --src harness:* --workspace WORKSPACE --apply
```

## Agent moves and workspace scope

Use `kei agents move AGENT --to-workspace WORKSPACE` to move an agent. Preview
first with `--dry-run`, inspect the plan, then repeat without `--dry-run` and
confirm with `--yes` when appropriate. Repeat `--group NAME=move|copy|leave`
to choose what happens to each group and `--installation ID=move_all|detach`
to choose what happens to each installation. Groups whose members are service
principals bound to the moving agent come along; harness tool rows are re-homed
to the destination workspace. There is no standalone group-move command or
console move UI; workspace moves are CLI/API only by design for now. When
explaining a move, explicitly say that bound service-principal-member groups
come along and harness tool rows are re-homed.

If the move is blocked because the destination has no model profile, pass
`--model-profile drop` to explicitly discard the source assignment. This flag
is supported by the move workflow; if the installed `kei agents move --help`
does not show it, verify the installed release before relying on it.

On kei-proxy 0.9.1 and newer, `serve` refreshes its identity after a workspace
move; no runtime restart or `kei-proxy policy sync --force` is needed. For
older kei-proxy versions, restart the runtime and force a policy refresh after
the move.

Users are org-level identities that can span workspaces through workspace
membership. Service principals are org-scoped; they appear in a workspace only
through group membership and service-principal bindings. Groups, agents, and
policies each belong to exactly one workspace.

## Key guidelines

- **Nothing outside the usage string exists.** Check installed `kei help` and
  command-specific help before naming a command or flag. Current help includes
  `kei agents move` (not general agent CRUD), `kei users`, `kei groups`,
  `kei workspaces create`, `kei directory-sync`, and `kei skills add`, along
  with the other listed resource commands. There is no `kei org` command, no
  agent create/update/delete CLI, no group update command, and no `kei setup
  doctor`; org creation and operations not exposed by the CLI use `kei-api` or
  the console. Do not claim agents, groups, or users have no CLI support.
- **Credentials never touch the terminal.** `kei connectors connect` never
  prints a token; it prints only connection state and granted scopes.
  `kei bot credential` refuses to write to an interactive terminal; pipe it
  into a secret manager. Never pass a token as an argument unless the user
  accepts shell-history exposure.
- **The CLI does not provision infrastructure.** The customer owns hosting and
  secrets; the CLI registers and inspects control-plane metadata.
- **Every ID is a UUID.** `--installation` and `--agent` are validated as UUIDs
  before any request is made.
- **Before a resource command, verify three things:** the exact name in
  `kei help` (`kei policies`, plural), the installed version (`kei --version`),
  and the contract (opaque page tokens for `list`, PATCH with an update mask
  for `update`). Login is a precondition, not one of the three. See
  *When resource commands arrive* below.
- **Do not present a future resource command as available.** Confirm the exact
  command in the installed `kei help` and a released version or API contract;
  if the command is not confirmed, say so and describe only the documented
  contract requirements. For a released resource `update`, explain PATCH and
  its update mask; for `list`, explain opaque page tokens.
- **Model-profile status:** `kei model-profiles list` and other resource
  commands fail on kei 0.1.12 and earlier; recommend upgrading to v0.1.13 or
  later. `kei model-profiles test` validates the endpoint only and never
  contacts the provider. Use
  `kei model-profiles readiness PROFILE --workspace WORKSPACE` to check
  whether a runtime can reach the provider.
- **Runtime version labels:** `(below minimum)` means the runtime version is
  below the organization's minimum. It is display-only and does not block
  the runtime.
- **Per-user OAuth:** `kei connectors connect` connects only the authenticated
  user's own account after `kei login`; it never prints a token. Do not connect
  another user's account from your session—each user must log in and run
  `kei connectors connect` for their own account.
- **Runtime authorization:** a long-lived service uses `kei-proxy serve` for
  each tool-call decision, with `kei-proxy authorize` as the no-daemon
  fallback. The agent does not run `kei login`; that is for the human
  platform administrator using the `kei` CLI.

## Quick reference

| Task | Command | Needs login |
| --- | --- | --- |
| Show commands for this version | `kei help` | no |
| Log in / out | `kei login [--no-browser]` / `kei logout` | — |
| List / create workspaces | `kei workspaces list [--json]` / `kei workspaces create --name NAME [--json] [--yes]` | yes |
| Move an agent | `kei agents move AGENT --to-workspace WS [--group NAME=move\|copy\|leave]… [--installation ID=move_all\|detach]… [--model-profile drop] [--dry-run] [--yes] [--json]` | yes |
| Users | `kei users list\|get\|create\|update\|resolve`; `kei users identities list USER`; `kei users remote-identities list USER` | yes |
| Groups and members | `kei groups list\|create\|delete`; `kei groups members list\|add\|remove`; add/remove accepts `--service-principal NAME` and `--workspace WS` | yes |
| Service principals | `kei service-principals list\|get\|create\|update\|delete\|bind\|unbind`; `kei service-principals bindings list --workspace WS` | yes |
| List runtime installations | `kei bot list [--json] [--all]` (v0.1.33+: shows VERSION column; flags `(below minimum)` when the installation's runtime version is below the org minimum; display-only, does not block the runtime) | yes |
| Create a runtime installation | `kei bot init --platform cli\|teams\|discord\|slack\|whatsapp\|openwebui --name NAME [--agent ID] [--workspace WS]` | yes |
| Emit the runtime credential | `kei bot credential --installation ID --workspace WORKSPACE \| <secret-manager import>` | yes |
| Rotate the runtime credential | `kei bot credential --installation ID --workspace WS --rotate \| <secret-manager import>` | yes |
| Inspect an installation | `kei bot status --installation ID` | yes |
| Activate after first heartbeat | `kei bot bind --installation ID` | yes |
| List / attach / detach agents | `kei bot agents list\|add\|remove --installation ID [--agent ID] [--default]` | yes |
| Delete an installation | `kei bot delete --installation ID --yes` | yes |
| List policies for a workspace | `kei policy list --workspace WS` | yes |
| Get a policy | `kei policy get ID --workspace WS` | yes |
| Create a group allow/deny policy | `kei policy create --workspace WS --group GROUP --allow TARGET` (or `--deny TARGET`) | yes |
| Test a policy | `kei policy test TARGET --workspace WS --as SUBJECT` | yes |
| Create a temporary access grant | `kei access grant create --workspace WS --principal user:ID --target TARGET --ttl 4h --reason REASON` | yes |
| Review legacy policy rules | `kei policy migration-report --workspace WS` (read-only) | yes |
| Delete a policy | `kei policy delete ID --workspace WS` | yes |
| List data connectors | `kei connectors list [--workspace WS] [--json]` | yes |
| Create a data connector | `kei connectors create --provider P --name NAME [--account-model M] [--set k=v] [--credential-ref R] [--capabilities a,b] [--workspace WS]` | yes |
| Connect your own per-user OAuth connector (v0.1.34+) | `kei connectors connect <id\|name> --workspace WORKSPACE [--no-browser]` | yes |
| Get / reconnect / delete a connector | `kei connectors get ID [--json]` / `kei connectors reconnect ID [--no-browser] [--keep-secret]` (v0.1.34+: on per-user connectors, points to `kei connectors connect`) / `kei connectors delete ID --yes` | yes |
| Add a remote MCP server (v0.1.32+) | `kei connectors create --template TEMPLATE_ID --label LABEL [--kind mcp] [--slug S] [--mcp-url URL] [--expected-issuer URL] [--workspace WS]` | yes |
| Review an MCP connector's tool manifests (v0.1.32+; alias `tools`) | `kei connectors manifests list\|show CONNECTOR_ID [MANIFEST_ID] [--workspace WS] [--json]` | yes |
| Approve a tool manifest (org admin, v0.1.32+) | `kei connectors manifests approve CONNECTOR_ID MANIFEST_ID [--workspace WS] [--yes]` | yes |
| Register a custom/SDK harness | `kei harness add --kind custom [--installation ID] [--agent ID]` | yes |
| Sync tool registrations | `kei harness sync [--harness KIND] [--manifest PATH] [--dry-run]` | yes |
| List registered harnesses | `kei harness list --installation ID [--json]` | yes |
| Remove a harness | `kei harness remove AGENT_ID --installation ID` | yes |
| List / wire agent↔connector bindings (kei-cli v0.3.0+ — check `kei help`) | `kei connector-bindings list [--workspace WS] [--agent AGENT_ID] [--json]` / `get BINDING_ID [--workspace WS] [--json]` / `create --agent AGENT_ID --connector CONNECTOR_ID [--capabilities A,B] --workspace WS [--json]` / `delete BINDING_ID --workspace WS --yes` — wiring only, never a permission gate (ADR-038) | yes |
| List / get model profiles | `kei model-profiles list [--workspace WS]` / `kei model-profiles get PROFILE [--workspace WS]` | yes |
| Create a model profile (no credential) | `kei model-profiles create [--workspace WS] --display-name NAME --endpoint URL --default-model MODEL --auth-type none [--workspace-default]` | yes |
| Create an API-key model profile | `<secret-manager read> \| kei model-profiles create --workspace WS --agent AGENT_ID --display-name NAME --endpoint URL --default-model MODEL --auth-type api_key` | yes |
| Update / rotate a profile key | `kei model-profiles update PROFILE [--workspace WS] [--default-model M]` / `<secret-manager read> \| kei model-profiles update PROFILE --workspace WS --rotate-key` | yes |
| Set the default profile | `kei model-profiles set-default PROFILE [--workspace WS]` | yes |
| Assign / unassign / show an agent's profile | `kei model-profiles assign PROFILE --workspace WS --agent AGENT_ID` / `unassign\|assignment --workspace WS --agent AGENT_ID` | yes |
| Can runtimes reach the provider? | `kei model-profiles readiness PROFILE --workspace WS` | yes |
| Validate an endpoint like the console's Test button (no provider call) | `kei model-profiles test --endpoint URL` / `kei model-profiles test PROFILE [--workspace WS]` | `--endpoint`: no |
| Delete a model profile | `kei model-profiles delete PROFILE [--workspace WS] --yes` | yes |
| Credential store | `kei credential-store get [--workspace WS]` / `put [--workspace WS]` (creates it) / `update` (PATCH) (v0.1.34+: `--workspace` reads/writes the workspace override) | yes |
| Entra directory sync (workflow in `kei-directory-sync`) | `kei directory-sync get\|set\|enable\|disable\|report`; see `kei directory-sync set --help` for current flags, including mutually exclusive `--app-id` and `--group-id` | yes |
| Install Haikei skills for detected agents | `kei skills add` (installs via `npx skills add HaikeiLabs/skills -g`) | no |
| One-command harness setup (v0.1.34+) | `kei connect HARNESS [--workspace NAME] [--yes]` (creates installation, credential, config, bootstrap, bind in one step) | yes |
| Write local runtime config | `kei setup [--config PATH] [--control-plane-url URL]` | no (runtime token) |
| Verify + heartbeat via local kei-proxy | `kei runtime bootstrap [--config PATH] [--proxy-path PATH]` | no (runtime token) |
| Upgrade via Go | `kei upgrade [--version VERSION]` | no |
| Report a bug (redacted harness transcript) | `kei feedback --description TEXT --export claude\|codex\|opencode [--session ID]` | yes |

All `bot` commands accept `--api-url URL` (override the default control-plane
URL). `bot bind` works but is not listed in `kei help`.

`kei harness` is **keyed by agent**, not by a surrogate harness ID: a harness
is a property of an installation-agent assignment, so `add` is for custom/SDK
harnesses (`--kind custom`) and requires `--agent` (the agent must already be
attached to the installation via `kei bot agents add`). Desktop harnesses
(`claude_code`, `codex`, `opencode`, `cursor`) are
**auto-discovered** by `kei harness sync` — do NOT use `add` for them.
`--installation` and `--agent` are optional
with defaults (single installation, default agent). `remove`/`sync` are
addressed by the agent. There is no `--display-name`/`--name` flag. The console
labels these harnesses "agents". For the full harness-command-policy workflow,
load **`kei-harness-policy`**.

`kei harness sync` backs up each native config it changes to
`<file>.kei-backup-<timestamp>` and each skill it replaces under
`skill-backups/` in the sync ledger dir. From kei 0.1.31 it keeps **one**
backup per file and per skill: the state from before the most recent
successful sync. The next successful sync removes the older one, a failed sync
rolls back and leaves it untouched, and `--dry-run` prints
`Would remove earlier Kei backup <path>`. To roll back by hand, copy the
`.kei-backup-<timestamp>` file over the native config.

## MCP connectors and tool manifests

These need `kei` v0.1.32 or later (older releases do not have them):
check `kei help` first. Depth is
in [references/mcp-connectors.md](references/mcp-connectors.md).

- **Create from a template.** `kei connectors create --template TEMPLATE_ID
  --label LABEL` reads the template from the catalog; the CLI keeps no
  template list. `--kind mcp` only checks the template's kind. Pass
  `--mcp-url https://…` when the template has no URL (`custom_mcp`), `--slug`
  to choose the immutable slug (it defaults to one derived from the label),
  and `--expected-issuer` to pin the OAuth authorization server. When you give
  the create command, also say that each user then connects their own account
  with OAuth (per user, so nothing is read from stdin) using `kei connectors
  connect` (v0.1.34+) and that the connector's tools stay blocked until an
  admin approves its tool manifest.
- **Catalog too old for `--expected-issuer`.** When the remote catalog doesn't
  support `--expected-issuer`, the CLI creates the connector without the issuer
  pin but then fails closed: it deletes the connector rather than leave one
  that trusts any authorization server. To fix this, upgrade the catalog (the
  platform side), or re-create the connector without `--expected-issuer` if
  that risk is acceptable.
- **Tools come only from the approved manifest.** The runtime submits each
  manifest it observes as a candidate. Review it with
  `kei connectors manifests show CONNECTOR_ID` (newest candidate, with tools
  added `+`, removed `-` and changed `~`). An org owner or admin approves it
  with `kei connectors manifests approve CONNECTOR_ID MANIFEST_ID`. That needs
  the manifest ID, shows the changes, and asks before approving (`--yes` in
  scripts). `tools` is an alias for `manifests`.
- `kei connectors get` shows an mcp connector's slug, MCP URL, issuer and
  manifest status; `kei connectors list --manifests` adds a status column.

## Connecting your own per-user OAuth connector (v0.1.34+)

`kei connectors connect` connects **your own** per-user OAuth connector
(GitHub, Linear, Google Drive, etc.). It starts the OAuth bridge sign-in for
the running user only; connecting another user's account is denied.

```sh
kei connectors connect <id|name> --workspace WORKSPACE [--no-browser]
```

- Opens the browser to the OAuth authorization page, or prints the URL with
  `--no-browser`.
- Polls until the connection completes (up to 10 minutes).
- Prints the connection **state** and the **granted scopes** on success.
- **Never prints a token.** The OAuth token stays server-side; the CLI shows
  only state and scopes.
- **Other users' accounts are denied.** The command is for the authenticated
  user only. To connect another user, that user must run `kei connectors
  connect` themselves after `kei login`.
- `kei connectors reconnect` on a per-user connector now points to `kei
  connectors connect` instead of the old "users connect through their chat
  harness" message.

## Model profiles and the credential store

Model profiles and the credential store are organization resources
(`/api/v1/organizations/{org}/...`); the organization is the one your `kei
login` token is bound to. Pass `--workspace` (name or ID) for a workspace's
profiles; omit it for organization-level profiles. `PROFILE` is an ID or a
display name; `--agent` takes an agent ID. Writes require an org admin.

- **API keys come from stdin only.** They are never accepted as a flag and
  never printed. Pipe them from a secret manager (or type them at the no-echo
  prompt). The CLI seals the key to the runtimes in the profile's scope (the
  agent's runtimes, or the workspace's for a workspace default) with the same
  KMP1 envelope as connector secrets, and sends only the sealed copies. If no
  runtime is eligible, `create` fails before creating anything.
- `create` requires `--default-model`; `--auth-type` is `none` or `api_key`.
- The credential store must exist before an API-key profile: `kei
  credential-store put` creates it, `update` changes it. Without one,
  `create` fails with `no active credential store; configure one with kei
  credential-store put`.

When someone asks for the command to create an API-key profile, answer in
this order: (1) the credential store must exist first, created with
`kei credential-store put`; (2) pipe the key from the secret manager into
`kei model-profiles create` with `--default-model` and `--auth-type api_key`
(plus `--workspace`/`--agent` for scope); (3) check it with
`kei model-profiles readiness`.

How a deployed runtime then uses the profile (same-account read of `secret_ref`
versus credential sync) is in `kei-runtime-setup`.

**Workspace overrides (v0.1.34+).** `kei credential-store get --workspace WS`
and `kei credential-store put --workspace WS` read or write a workspace-level
credential store override, separate from the organization-level store. Without
`--workspace`, the commands address the organization store. If no override
exists for a workspace, `get --workspace WS` reports that the workspace uses
the organization's store.
- `kei model-profiles test` (v0.1.14 or later) does what the console's
  **Test** button does: it validates the endpoint (`https`, a host, no embedded
  credentials, query, or fragment) and **never contacts the provider**.
  `test --endpoint URL` needs no login; `test PROFILE` checks a stored
  profile's endpoint. Before v0.1.14 it exited with an error. It cannot tell
  you whether the model is reachable: use `readiness` for that.
- **kei ≤ 0.1.12:** `kei model-profiles` and `kei credential-store` call
  retired console routes and fail. Upgrade to v0.1.13 or later.

## Runtime installations

An installation is one customer-owned runtime boundary: the scope for
bootstrap, heartbeats, policy delivery, and audit. It is distinct from a user
login.

```sh
kei bot init --platform cli --name "Acme local runtime"
```

- `--platform` and `--name` are required; there is no default platform. v0.1.4+
  accepts `cli`, `teams`, `discord`, `slack` (earlier releases and some console
  pages omit `cli`). Use `cli` for a local coding-harness runtime. `discord` is
  for Haikei-internal harnesses only.
- The output includes the non-secret `installation_id`. No credential is
  printed here.
- `bot delete` removes the control-plane installation and revokes its
  credential immediately; it never touches customer cloud resources.
- **A `pending` status is evidence about the heartbeat, not proof of health.**
  `kei bot status --installation ID` shows `pending` until the runtime's first
  heartbeat reaches the control plane. When diagnosing a pending runtime, say
  so, then collect read-only evidence: the `kei bot status` output, whether
  the runtime process and its heartbeat loop are running, its logs, and
  whether it can reach the control plane. Never print or paste the runtime
  credential to check it.

For the full stand-up sequence (credential → config → bootstrap → heartbeat →
bind → fail-closed check), load **`kei-runtime-setup`**.

## Runtime credential

```sh
kei bot credential --installation ID --workspace WORKSPACE | <secret-manager import>
```

- Emitted once for a new installation. If one already exists the command fails
  with `bot credential already exists; use --rotate to replace it`.
- `--workspace` accepts a workspace name or ID. The credential is scoped to
  that workspace. If omitted, the existing workspace (set at installation
  creation) is used.
- `--rotate` replaces the credential in place; the old one stops working
  immediately. Load **`kei-credential-rotation`** before rotating a runtime
  that is serving traffic.

## Local runtime: `kei setup` + `kei runtime bootstrap`

This is the current way to bring up a runtime on a workstation. `kei setup`
saves the runtime settings; `kei runtime bootstrap` runs the bundled
`kei-proxy runtime bootstrap` with those settings passed in its environment
(it finds `kei-proxy` via the configured path, then `PATH`). A deployed
runtime runs `kei-proxy runtime bootstrap` itself with env from its secret
manager — see `kei-runtime-setup` and `kei-proxy`.

```sh
kei setup                      # prompts; verifies the runtime token; writes ~/.config/kei.yaml (0600)
<secret-manager read> | kei setup --control-plane-url https://app.haikeilabs.com   # token from a pipe, nobody pastes it
kei runtime bootstrap          # runs the configured kei-proxy to verify + send a heartbeat
```

`kei setup` also takes `--harness-url` (default `http://127.0.0.1:8088`),
`--proxy-path`, `--proxy-registry`, `--model-endpoint`, `--model`,
`--runtime-token` (lands in shell history — prefer the prompt), and
`--skip-verify`.

## One-command harness setup: `kei connect`

`kei connect` sets up a harness end-to-end in a single command: creates the
runtime installation, emits the credential, writes local config (`kei setup`),
bootstraps (`kei runtime bootstrap`), and binds the installation — all in one
step.

```sh
kei connect claude-code [--workspace NAME] [--yes]
kei connect codex [--workspace NAME] [--yes]
kei connect opencode [--workspace NAME] [--yes]
kei connect pi [--workspace NAME] [--yes]
```

Harness values come from the installed help: `claude-code`, `codex`,
`opencode`, `pi`, and `cursor`. Values such as `cli` and `openwebui` are not
accepted. `cursor` is the seventh value, released in kei-cli v0.3.0 (v0.3.7
is current). Cursor is Kei-checked
native-first — Kei renders policy into Cursor's CLI config permissions
(`~/.cursor/cli-config.json`); sync fails closed (exit non-zero, nothing
written) when a policy kind cannot be gated, e.g. `skill:` — and it needs a
kei-proxy runtime like the other desktop harnesses. Check `kei help` for what
your installed version accepts.

- `HARNESS` is one of the supported harness values listed above.
- `--workspace` scopes the installation to a workspace (name or ID). If
  omitted, the caller's default workspace is used.
- `--yes` skips confirmation prompts.
- The command authenticates with the `kei login` session token (login
  first).
- For the individual steps or when more control is needed, use the
  per-command sequence (`kei bot init` → `kei bot credential` → `kei setup`
  → `kei runtime bootstrap` → `kei bot bind`) — see `kei-runtime-setup`.

## Report a bug from your harness

`kei feedback` sends a bug report to Kei from the terminal, optionally with the
harness session transcript attached. It needs `kei` 0.1.20 or later for
`--export` and a `kei login` session. Run it from the project directory the
harness session ran in: without `--session`, `--export` picks the most recent
session for the current working directory. `--description` is required (1 to
4000 characters).

```sh
kei feedback --description "What happened and what you expected" --export claude     # Claude Code
kei feedback --description "What happened and what you expected" --export codex      # Codex
kei feedback --description "What happened and what you expected" --export opencode   # OpenCode (runs opencode export)
kei feedback --description "..." --export claude --session <session-id>               # a specific session
kei feedback --description "..." --session /path/to/transcript.jsonl                  # any harness: transcript file(s)
kei feedback --description "..." --file app.log --screenshot error.png               # other evidence
```

- With `--export`, `--session` is one session ID; without it, `--session` is a
  repeatable transcript file path. At most 8 evidence files, 4 MiB in total.
- **Transcripts are redacted before anything is sent.** Token-shaped strings
  (Anthropic and OpenAI keys, GitHub and Slack tokens, AWS keys, JWTs,
  `Bearer` tokens, private-key blocks, Kei runtime tokens, and
  `password=`/`token=`/`secret=` style values) become `[REDACTED:<kind>]`.
  `--file` and `--screenshot` are sent as they are.
- **The user previews and confirms.** The CLI prints the description, each
  file with its size and the redaction counts per kind (never the content),
  then asks `Send? [y/N]`. Anything other than `y`/`yes` prints
  `Feedback not submitted.` and sends nothing. `--yes` skips the prompt; an
  agent must not add it. Give the user the command to run instead. When
  explaining `kei feedback`, include this sentence: "You preview the report
  (description, files, redaction counts) and must confirm at `Send? [y/N]`;
  answering no sends nothing."
- A Kei runtime token in a transcript triggers a leak warning: rotate it with
  `kei bot credential --rotate` (see `kei-credential-rotation`).

The **Report a bug** button in the console header sends to the same place.
Per-harness detail is in `kei-harness-setup`.

## Resource command availability

The installed help currently exposes workspace, group, user, policy, connector,
harness, model-profile, credential-store, service-principal, directory-sync,
and agent-move commands. It also exposes `kei skills add` for installing the
Haikei skills. Exact flags and supported operations vary by release; consult
`kei help` and each command's `--help` before using them. Avoid stale version
claims in this skill: the binary is the authority.

Before using or documenting a resource command, confirm it in `kei help` for
the installed version and check that it follows the contract:

- `list` / `get` / `create` / `update` / `delete` map to the API's List, Get,
  Create, Update, and Delete;
- `update` uses PATCH semantics with an explicit update mask, never a full
  replace;
- `list` uses opaque page tokens and returns the next page token, not offsets;
- errors keep a stable machine-readable reason;
- non-CRUD state changes are explicit `:verb` custom methods (for example
  `:rotate`), not guessed subpaths.

Until the command exists and is tested, use the web app or `kei-api`. Do
not describe a future command as available.

When someone asks what to verify before running a resource command, answer
with all three (login is a precondition, not one of them):

1. The **exact name** in `kei help`: use singular `kei policy`; `kei policies`
   is a deprecated compatibility alias. Use `kei policy migration-report`
   for the read-only legacy policy report.
2. The **installed version**: `kei --version`; for example `kei policy list`
   needs v0.1.11 or later.
3. The **contract** above: opaque page tokens for `list`, PATCH with an
   update mask for `update`.

## Validation commands

```sh
kei --version
kei help                                  # authoritative usage for this version
kei bot                                   # "bot requires a subcommand" (exit 2)
kei login --no-browser
kei bot status --installation INSTALLATION_ID
```

## Realistic usage boundaries

- Agent creation and general agent CRUD remain outside the CLI, but `kei agents
  move` is available. Workspace-scoped group/user/policy operations and org
  users/service principals are exposed to the extent listed in the installed
  help. Invitations and other unavailable operations use `kei-api` or the
  console. For harness policy workflows, load `kei-harness-policy`.
- The CLI does not submit tool manifests (the runtime does), create connector
  templates, or grant a connector to a group (that is a policy). `--provider`
  has no `grafana` (or other MCP) value: an MCP server is added with
  `--template`.
- The CLI token is org-bound and short-lived; it is not a general user token and
  cannot be used by a runtime.
- The **Keys** page no longer exists. Agent keys were deprecated in favor of
  the runtime installation credential for all runtime operations.
- AWS, GCP, Azure, Terraform, and Helm deployment steps are not part of the
  CLI. Kei's own control plane runs on AWS EKS; customer hosting is the
  customer's choice.
