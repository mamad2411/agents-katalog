---
name: deploy-agents
description: Deploy and distribute a governed AI agent with Kei — create a runtime installation and deliver its credential (KEI_RUNTIME_TOKEN) to a secret manager, run kei-proxy as an in-container daemon beside the harness (runtime bootstrap, heartbeat, `kei-proxy serve` on an owner-only Unix socket, per-user sessions, local POST /v1/authorize, the agentware socket client with tool-manifest sync), bind it, connect the harness (Claude Code, Codex, OpenCode via skills + `kei harness sync`; a Discord or other chat bot via its own installation and per-user sessions), control what the agent may do with policies (tool-call policies by group, harness command policies with `kei policies`), and add connectors whose OAuth is per user (`kei connectors create --account-model per_user`, connect links). Use when someone asks how to ship, deploy, containerize, host, distribute, or roll out an agent built with agentware/kei-agents, how to give it permissions, or how users connect their own accounts. Building the agent is build-agents-agentware; testing it is test-agents.
---

# Deploy and distribute agents with Kei policies

Deploying an agent with Kei means putting a **runtime** beside it. The runtime
(`kei-proxy`) holds the installation credential, syncs the workspace policy,
makes the allow/deny decision locally, runs protected connector calls with the
user's own credential, and ships redacted audit metadata. Provider payloads,
results, and credentials stay in your environment; Kei keeps metadata only.

```
 your container ───────────────────────────────────────────────┐
 │  harness (your agent + agentware)                           │
 │      │  KeiProxyEvaluator → socket client: session, then     │
 │      │  POST /v1/authorize  (CLI subprocess only as fallback)│
 │      ▼                                                       │
 │  kei-proxy serve  (same UID, socket mode 0600)               │──► Kei control plane
 │      policy bundle · sessions · per-user connector creds     │    (policy, metadata, audit)
 └──────────────────────────────────────────────────────────────┘
```

Two CLIs, two jobs: **`kei`** is the admin CLI a person runs (needs
`kei login`, owner/admin, browser-approved); **`kei-proxy`** is what the
runtime runs (authenticates with `KEI_RUNTIME_TOKEN`, never `kei login`).

## 1. Create the runtime installation

One installation per runtime boundary (one harness deployment : one
installation : one credential).

```sh
kei login                                         # a person approves in the browser
kei bot init --platform cli --name "acme-agent"   # cli | teams | discord | slack | ... — check `kei help`
kei workspaces list
kei bot credential --installation INSTALLATION_ID --workspace WS | <secret-manager import>   # shown only once
```

**The credential is shown only once**, so tell whoever runs this before they
run it: there is no second look. Pipe it straight into the secret manager; the
CLI refuses to print it to a terminal. If it already exists the command fails —
replacing it is a rotation that breaks the running runtime immediately (load
`kei-credential-rotation`).

## 2. Run kei-proxy in the container

There is no public `kei-proxy` image: put the `kei-proxy` binary in your
harness image (it ships with the `kei` installer; container builds use the
Kei runtime Dockerfile). Inject three variables into the harness process:

```text
KEI_RUNTIME_CONTROL_PLANE_URL=https://app.haikeilabs.com   # the gateway; never append /api/v1
KEI_RUNTIME_TOKEN=<from the secret manager>                 # env only, never argv, never a file in the repo
KEI_RUNTIME_VERSION=<your deployed version>
KEI_SECRETS_BACKEND=aws-secrets-manager   # required by kei-proxy >= 0.7 to read model-profile/connector secrets
```

`KEI_SECRETS_BACKEND` identifies the configured secret backend. Kei-proxy >=
0.7 requires it when reading model-profile or connector secrets.

Never pass an org, tenant, or workspace ID as scope; the token determines it.
Entrypoint, in order:

```sh
kei-proxy runtime bootstrap                    # verify the installation; prints installation_id, org_id, workspace_id
kei-proxy runtime heartbeat --interval 1m &    # liveness, under the same supervisor as the harness
kei-proxy serve &                              # the daemon: owner-only Unix socket
exec my-harness                                # syncs its tool manifest, then serves over the socket
```

If bootstrap output has no `workspace_id`, stop and re-mint the credential.

**Workspace moves.** Existing agents move with `kei agents move`; preview
with `--dry-run` first and consult `kei-cli` for group and installation
choices. Kei-proxy 0.9.1+ refreshes its identity after the move, so no runtime
restart or forced policy sync is needed. Older proxy versions need a restart
and forced sync. Groups, agents, and policies belong to one workspace; users
span workspaces by membership, while org-scoped service principals appear in a
workspace only through group membership and bindings. There is no standalone
group move or console move UI, by design for now.

**The daemon (`kei-proxy serve`).** It listens on a Unix socket —
`/run/kei-proxy/runtime.sock` on Linux (`KEI_RUNTIME_SOCKET_PATH` overrides),
mode `0600`, so the harness must run as the same UID; on Kubernetes share the
directory through an `emptyDir`. It serves `GET /healthz`, `GET /readyz`,
model routes, and the protected routes:

- `PUT /v1/session` with `{"schema":"kei.session/v2","source":"discord","external_id":"<user id>"}`
  → `201 {"session_id":"ks_…","user_id":…,"status":"linked",…}`. One daemon
  serves **many concurrent sessions**, one per user or agent, each with its
  own subject and its own connector credentials. Session and model routes
  require the runtime bearer token.
- `POST /v1/authorize` with header `X-Kei-Session: <session_id>` — decided
  **locally** by the runtime PDP against the synced policy bundle, no per-call
  round trip. It is the only socket route that needs no bearer token (the
  `0600` socket is the boundary).
- `DELETE /v1/session` ends the session and flushes its credentials; idle
  sessions end after `KEI_SESSION_IDLE_TTL` (default `30m`). An unknown or
  expired id denies `session_not_found`.

**The harness side: the agentware socket client.** Set
`KEI_RUNTIME_SOCKET_PATH` in the harness's environment and, at startup:

Register tools over the socket with `ToolSpec` (`POST /v1/tools:register`).

1. **Sync the tool manifest before serving**: `sync_tool_manifest`
   (Python), `syncToolManifest` (TypeScript) or `toolsync.Sync` (Go). It
   `PUT`s the protected tools to the control plane with the runtime token and
   **refuses an empty manifest** (that PUT would unregister every tool). A
   failed sync means the harness does not serve.
   You can also register tools over the socket with `ToolSpec`
   (`POST /v1/tools:register`). See `agentware-sdk` for the APIs.
2. **Pick the client with the selector**: `select_authorization_client` /
   `selectAuthorizationClient` / `runtimesocket.SelectAuthorizationClient`.
   With a socket configured it returns the socket client, which opens a
   session per user and authorizes in it; otherwise the `kei-proxy authorize`
   subprocess client. Wrap it in `KeiProxyEvaluator`.

```python
from haikeilabs.agentware.kei import (   # pedro_agentware.kei still works (deprecated shim)
    KeiProxyEvaluator, ToolManifestSyncConfig, select_authorization_client, sync_tool_manifest,
)
sync_tool_manifest(manifest_json, ToolManifestSyncConfig.from_env(), expect_tools=True)
evaluator = KeiProxyEvaluator(select_authorization_client("discord"))
```

Fail closed: **a configured socket that is down is a refusal
(`proxy_unavailable`), never a silent fall back** to the CLI, and the runtime
token is never logged. The per-call `kei-proxy authorize` CLI is the
**fallback** for one-shot environments with no daemon (a batch job, a CI
step). The `agentware-sdk` skill has the TypeScript and Go spellings.

## 3. Bind and attach the agent

```sh
kei bot bind --installation INSTALLATION_ID          # explicit: a runtime cannot activate itself
kei bot agents add --installation INSTALLATION_ID --agent AGENT_ID --default
kei bot status --installation INSTALLATION_ID
```

Agents are created in the web console (**Agents**); there is no CLI command
for it. The harness discovers its agent from the runtime identity
(`link.identity()`), never from an env var.

## 4. Connect the harness

**Coding harnesses (Claude Code, Codex, OpenCode, Pi).** Install the Haikei
skills (Claude Code: `/plugin marketplace add HaikeiLabs/skills` then
`/plugin install haikei@haikei`; Codex: `codex plugin marketplace add
HaikeiLabs/skills` then `codex plugin add haikei@haikei`; OpenCode and Pi:
clone the repo and link each skill folder into `~/.config/opencode/skills/` or
`~/.agents/skills/`). On a workstation the runtime is set
up with `kei setup` (token piped on stdin) and `kei runtime bootstrap`. These
desktop harnesses are **auto-discovered**; render Kei policy into their native
config with:

```sh
kei harness sync --harness claude_code      # or codex, opencode — back up the native config first
```

`kei harness add --kind custom` is only for a custom/SDK harness you built.

**Chat harnesses (a Discord bot, Teams, Slack).** Create the installation with
that platform (`kei bot init --platform discord …`) and open one daemon
session per chat user (`"source":"discord","external_id":<the user's id>`).
The invoking subject is that human, carried unchanged into every subagent
call. A user whose chat identity is not linked gets a deny with an
`enrollment` claim link: send it to **that user privately** (a DM), never to
the channel, never to logs; each response mints a new link, so always show the
newest.

Then prove it fails closed: one permitted, disposable call and one call no
policy allows must be denied without reaching the provider.

## 5. Permissions are policies

What the agent may do is decided by workspace policy at run time, never by the
prompt and never by a local allow list in the harness (stale on deploy and
invisible to audit). Two kinds:

| Policy | Covers | Managed with |
| --- | --- | --- |
| **Tool-call (ABAC)** | Which subject/group may call which tool or connector capability | Console **Policies**, or `/api/v1/policies` (`kei-api`); group membership with `kei groups members add GROUP USER --workspace WS` |
| **Harness command** | What a coding harness may run (`shell:`, `skill:`, `path:` destinations) | `kei policy create`, `kei policies import|update` (deprecated alias), rendered by `kei harness sync` |

```sh
kei policy create --workspace WS --group default --allow "shell:git"
kei policies import --from claude --workspace WS            # dry run; --apply creates them
```

Policies apply to groups: `--group` takes a group name or `autogroup:member` /
`autogroup:admin`. At equal priority a deny beats a permit. A typical agent
split: everyday tools (`file_bug`, `search_wiki`, `web_search`) for the
`default` group, every tool that reads or writes protected data for admins. The protected tool must also be
registered in the catalog (its `KeiScope` manifest) before Kei can decide it.

## 6. Connectors with per-user OAuth

Each user should act with **their own** account, so the audit trail and the
provider both see the real person.

```sh
kei connectors create --workspace WS --provider linear --name linear            # OAuth; per_user is the default
kei connectors create --workspace WS --provider google_drive --name drive --account-model shared
kei connectors reconnect CONNECTOR_ID --workspace WS                            # shared account only
kei connectors list --workspace WS
```

Providers: `gmail`, `google_drive`, `linear`, `github` (OAuth), `tito`, and
`http_api` for any other API (shared secret, read from stdin, never a flag).
For a **per-user** connector
there is nothing for the admin to connect — `kei` prints "users connect their
own accounts through their chat harness". The first time a user's call needs
it, authorize denies with a `connect` block (`url`, `provider`,
`connector_id`, `expires_at`); the harness sends that one-time URL privately
to that user, and the next call succeeds. In identity mode
(`KEI_CREDENTIAL_RELEASE=identity`) the daemon fetches the user's connector
credential when their session starts and holds it **in memory for that session
only**; `POST /v1/credentials:release` returns the credential to the harness,
which calls the upstream API directly.

## Validation commands

```sh
kei help                                             # confirm every command above exists in your version
kei bot status --installation INSTALLATION_ID        # bound, heartbeating
kei-proxy runtime bootstrap                          # JSON includes workspace_id
curl --unix-socket /run/kei-proxy/runtime.sock http://localhost/readyz
kei harness sync --harness claude_code --dry-run
kei connectors list --workspace WS
```

## Realistic usage boundaries

- Never put `KEI_RUNTIME_TOKEN` in argv, a repo file, a log, or the audit
  trail. Never log or share an enrollment or connect URL.
- No public `kei-proxy` image or registry exists; do not invent one.
- Agent creation and organization creation are not CLI operations; existing
  agents can be moved with `kei agents move`. Use the supported `kei policy`
  commands for ABAC policies; consult `kei help` for the installed surface.
- Rotating the runtime credential breaks the running runtime at once; plan the
  restart (`kei-credential-rotation`).
- Only github, gmail, google_drive, and linear run with session-held OAuth in
  the daemon; other connectors use a shared secret in your secret manager.
- Kei decides; it never executes provider calls or stores provider data.

## Related skills

- `kei-runtime-setup` — the full installation walkthrough and recovery.
- `kei-proxy` — runtime command reference. `kei-cli` — admin command reference.
- `kei-harness-setup` — per-harness install scripts and troubleshooting.
- `kei-harness-policy` — harness command policies in depth.
- `build-agents-agentware`, `test-agents` — build and test before you ship.
