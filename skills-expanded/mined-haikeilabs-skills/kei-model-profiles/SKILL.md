---
name: kei-model-profiles
description: "Kei model profiles: how an admin picks the model an agent uses and how a harness resolves it at run time. A model profile is Kei's model routing: assign one to an agent on the console's Agents page or with `kei model-profiles assign`, and the harness reads the agent's current profile from kei-proxy (`GET /v1/model-config`, `GET /v1/models`, `GET /v1/model-profiles` on the `kei-proxy serve` socket, `kei-proxy model profile`, or the Agentware socket client's `model_config` / `list_models`). Use when someone asks which model an agent uses, how to switch or assign an agent's model, about model routing, failover or a backup model in Kei, `no_profile` or `profile_revoked` from model-config, `model_not_assigned`, `credential_unavailable`, what happens when the profile changes mid-session, or whether kei-proxy serves chat completions. Diagnosing a broken runtime is kei-setup-doctor; CLI syntax is kei-cli; runtime IAM and credential sync are kei-runtime-setup."
---

# Kei model profiles

In Kei, model routing **is** the model profile. An admin assigns a profile to
an agent. At run time the harness asks kei-proxy which profile that agent
has now, and calls that model. Nothing else picks the model: there is no
per-request routing, failover or cost-based selection in Kei today.

## When you answer

- About a profile change or refresh: say kei-proxy doesn't cache, so the
  **next** lookup returns the new profile. The harness re-resolves on its own
  schedule. Always end with: if re-resolving fails, or no profile comes
  back, the harness **fails closed** and **never falls back to a hard-coded
  model**.
- About failover, backups or spend: say they are **not implemented today**,
  and that the kei#1164 design is a proposal.
- About sending chat through kei-proxy: say `kei-proxy serve` has **no**
  `POST /v1/chat/completions` route.
- About any failure (`no_profile`, `profile_revoked`, `model_not_assigned`,
  `credential_unavailable`, an unassigned profile): give the fix, and **name
  the `kei-setup-doctor` skill** for diagnosis.
- About fallback: the workspace default profile applies **only when the agent
  has no assignment at all**. A disabled assigned profile does not fall back.

Each claim below carries a status:

- **[implemented]**: in the source on `main`, with a file and line.
- **[proposed]**: in a design document, with no shipped code.
- **[unverified]**: the source doesn't settle it. Don't present it as fact.

Paths are repo-relative. The repo is named first (kei-connector-runtime,
kei-cli, kei-console, kei-policy-catalog, Agentware).

## 1. What a profile is [implemented]

A profile is metadata in the control plane: `display_name`, `endpoint` (an
OpenAI-compatible base URL), `default_model`, `auth_type` (`none` or
`api_key`), `status`, and for `api_key` profiles a `secret_backend` and
`secret_ref` that point into **your** secret store (kei-connector-runtime
`runtime/model_profile.go:14-28`). The provider API key never passes through
Kei. kei-proxy reads it from `secret_ref` with the runtime's own cloud
identity. That IAM setup, and credential sync, are in **kei-runtime-setup**.

Profiles live at the organization or workspace level. An agent's assignment is
a separate relationship from the profile.

## 2. Assign a profile to an agent

### Console [implemented, behavior partly undocumented]

- **Model profiles** page (`/models`, in the Agents section of the nav;
  kei-console `frontend/src/pages/ModelProfiles.tsx`). **Add profile** (:308)
  opens *Create Model Profile* (:361). Its fields are workspace, **Target
  agent** (:378), **Use as workspace default fallback** (:386), display name,
  endpoint, default model and authentication type. The table's *Agents using
  profile* column shows who uses each profile.
- **Agents** page: the agent row's **Model profile** button (kei-console
  `frontend/src/pages/Agents.tsx:1058`) opens a modal with one **Default
  profile** select (:1578). It lists the active profiles of the agent's
  workspace. Use **Save profile** to set it and **Clear profile** (:1596) to
  remove it. With no active profiles, the modal says "Workspace defaults are
  used automatically as fallbacks" (:1576).

No kei-console doc describes these pages. The labels above come from the
source; check them in the live console.

### kei CLI equivalent [implemented]

`kei help` lists these commands (kei-cli `internal/app/model_profiles.go`).
Exact syntax and flags are in **kei-cli**; check installed `kei help`:

```sh
kei model-profiles list --workspace WS
kei model-profiles assign PROFILE --workspace WS --agent AGENT_ID
kei model-profiles assignment --workspace WS --agent AGENT_ID
kei model-profiles unassign PROFILE --workspace WS --agent AGENT_ID
kei model-profiles readiness PROFILE --workspace WS   # can runtimes reach the provider?
```

`PROFILE` is an ID or a display name. API keys for `create` and `update
--rotate-key` come from stdin only.

### Which profile the runtime gets [implemented]

For the runtime's default agent, the catalog picks the first match in this
order (kei-policy-catalog `pkg/database/model_profiles.go:231-275`):

1. The agent's default assignment, if that profile is `active`.
2. A legacy profile set directly on the agent, only when the agent has no
   assignment.
3. The workspace default profile, **only when the agent has no assignment at
   all**.

An assigned profile that is disabled or revoked **fails closed**. It does not
fall back to the workspace default.

## 3. How a harness resolves the profile at run time

kei-proxy needs `KEI_RUNTIME_TOKEN` and `KEI_RUNTIME_CONTROL_PLANE_URL`. Each
lookup below is a **fresh** control-plane read: neither the daemon nor
`kei-proxy model profile` caches the profile (kei-connector-runtime
`serve.go:458-512`, `model_profile_command.go:19-104`). `api_key` profiles
also need `KEI_SECRETS_BACKEND` (`aws-secrets-manager`, `azure-key-vault` or
`gcp-secret-manager`; kei-connector-runtime
`internal/secrets/configured.go:12-16`). The variable is required by
kei-proxy >= 0.7; leave it unset and every secret read fails closed.

### Socket routes on `kei-proxy serve` [implemented]

The socket is `KEI_RUNTIME_SOCKET_PATH` (default
`/run/kei-proxy/runtime.sock`). Each route needs `Authorization: Bearer
$KEI_RUNTIME_TOKEN`. Every route takes optional `agent_id` and `profile_id`
query selectors; with neither, it resolves the runtime's default agent
(kei-connector-runtime `serve.go:325-339`, `serve.go:548-568`).

| Route | Returns |
|---|---|
| `GET /v1/model-config` | `{"model","endpoint","credential","is_default"}`. **`credential` is the provider API key** for `api_key` profiles (`serve.go:458-512`). |
| `GET /v1/models` | OpenAI-style `{"object":"list","data":[{"id":<default_model>}]}`; `404 model_not_assigned` with no active profile (`serve.go:435-456`). |
| `GET /v1/model-profiles` | The agent's active assignments without secrets; `502 model_profiles_unavailable` on a lookup failure (`serve.go:414-433`). |
| `GET /healthz` | Probes `<endpoint>/models` on the provider (`serve.go:356-408`). |

**There is no `POST /v1/chat/completions` on the daemon.** HAI-671 removed it.
Unknown paths are `404`. See kei-connector-runtime `CHANGELOG.md:40` and
`docs/architecture.md:320`. The harness calls the provider itself, or uses
`kei-proxy model` (below).

### CLI [implemented]

- `kei-proxy model profile [--agent-id UUID] [--profile-id UUID]` prints the
  profile as JSON on stdout. For `api_key` profiles the JSON includes
  `api_key` (`model_profile_command.go:83-104`). Keep that output private.
- `kei-proxy model profiles [--agent-id UUID]` lists active assignments
  without credentials.
- `kei-proxy model` with no subcommand (the docs call it `model invoke`)
  reads one JSON request on stdin: `{"request": <chat body>, "agent_id",
  "profile_id", "request_id"}`. kei-proxy resolves the profile, adds the key
  itself, POSTs `<endpoint>/chat/completions`, and writes the provider
  response lines to stdout. Errors go to stderr as JSON, `{"type":"error",
  ...}` (`run.go:168-178`, `model_invoke.go:20-60`,
  `runtime/model_invoke.go:80-133`). This is the only shipped path where the
  provider key never reaches the harness. `kei-proxy help` doesn't list it.

### Agentware socket client [implemented, see the gap]

| | Python | TypeScript | Go |
|---|---|---|---|
| Profile config | `model_config(agent_id, profile_id)` | `modelConfig(agentId, profileId)` | `ModelConfig(ctx, agentID, profileID)` |
| Assignments | `list_model_profiles(agent_id)` | `listModelProfiles(agentId)` | `ListModelProfiles(ctx, agentID)` |
| Models | `list_models(agent_id, profile_id)` | `listModels(agentId, profileId)` | `ListModels(ctx, selectors...)` |

Source: Agentware `python/src/haikeilabs/agentware/kei/runtime_socket.py:382-420`,
`typescript/src/kei/socketAuthorizeClient.ts:385-430`,
`go/kei/runtimesocket/client.go:439-546`.

- The SDK **strips** `credential`, `api_key`, `apiKey` and `secret_ref` from
  what it returns (`runtime_socket.py:723`). Through the SDK you get the
  endpoint and model name, never the key.
- The clients also have `chat_completion` / `stream_chat_completion`
  (`chatCompletion`, `ChatCompletion`, ...). They POST
  `/v1/chat/completions`, which the daemon does not serve (see **Known
  gaps**). Don't build on them until that is resolved.
- Errors arrive as `KeiProxySocketError` (Go `*runtimesocket.Error`) with a
  reason class (`proxy_unavailable`, `proxy_timeout`, `proxy_error`,
  `malformed_response`, `missing_token`) and the daemon's `code`, such as
  `model_not_assigned`.

### Profile changes and caching [implemented + guidance]

- kei-proxy doesn't cache profiles, so the **next** lookup after a console
  or CLI change returns the new profile, or `no_profile`.
- Any cache is the **harness's own**. Re-resolve on a timer or per
  conversation; the Pedro harness uses 300 s (see kei-runtime-setup). A
  request already sent to the provider is not recalled.
- Swap configs only after the new one resolves.
- **Fail closed. Never fall back to a hard-coded model.** If a refresh fails
  or returns `no_profile`, stop making model calls. Don't keep a model
  hard-coded in the harness as a backup. An answer about profile changes
  always ends with this rule.

## 4. Failures [implemented]

| What you see | Meaning | Where to go |
|---|---|---|
| `{"status":"no_profile"}` (HTTP 200) from `/v1/model-config` | No active profile resolved for the agent | Assign one; see the assignment rows in **kei-setup-doctor** |
| `{"status":"profile_revoked"}` (HTTP 200) | The assigned profile is not `active`. The catalog's runtime queries already filter on `status='active'`, so in practice a disabled profile shows up as `no_profile`. There is no fallback either way | Reactivate it or assign another |
| `404 model_not_assigned` from `/v1/models` | Same as `no_profile` | As above |
| `runtime has no active model profile assigned to its default agent` (`kei-proxy model profile`, exit 1) | The runtime has no default agent, or that agent has no profile | **kei-setup-doctor** |
| `500 credential_unavailable` from `/v1/model-config`; `model profile credential unavailable` from the CLI | kei-proxy can't read `secret_ref`: IAM, region, KMS, or `KEI_SECRETS_BACKEND` unset | **kei-setup-doctor**, then **kei-runtime-setup** for IAM |
| `401 invalid_runtime_token` / `503 runtime_not_configured` | Token or control-plane URL missing or wrong | **kei-setup-doctor** |
| `404` on `POST /v1/chat/completions` | That route doesn't exist on the daemon | Use `/v1/model-config` + provider, or `kei-proxy model` |
| Old model after a change | The harness's own cache, or a stale policy or proxy state dir after switching installations | Re-resolve. For a stale state dir, see **kei-setup-doctor** (HAI-404) |

The `no_profile`, `profile_revoked` and `credential_unavailable` cases are
from kei-connector-runtime `serve.go:474-501`.

## 5. Routing and failover: proposed, not implemented

kei `docs/design/model-profile-routing-and-spend-watch.md` (kei#1164, merged
2026-11-17) is a **proposal**. The owner settled its direction on 2026-11-17:
the harness or Agentware would choose among profiles that Kei delivers, and
Kei itself would not route model calls. The implementation is still
proposed. That includes ranked backup profiles per agent, a runtime
last-good config cache, and a spend watch with alerts. None of it ships in
kei-proxy, kei-cli, the catalog query above, or Agentware. Today an agent
has one resolved profile and **no fallback**.

The catalog can already hold several assignments per agent, with exactly one
default. The runtime resolves only the default, unless the harness passes a
`profile_id` that is assigned to the agent. The playground app has its own TypeScript router (playground
`src/server/loop/model-router.ts`). That is an application-level example, not
a platform feature.

## Known gaps

- **No chat route on the daemon, but the SDK calls one.** Agentware's
  `chat_completion` / `stream_chat_completion` target `POST
  /v1/chat/completions`, which `kei-proxy serve` returns 404 for. The
  kei-proxy and agentware-sdk skills still describe that route.
- **No SDK path that keeps the key in kei-proxy.** The SDK strips the
  credential, the raw socket and `kei-proxy model profile` hand the key to the
  harness, and only the undocumented `kei-proxy model` subprocess keeps it.
  No Agentware wrapper exists for that.
- **`kei-proxy model` (invoke) is missing from `kei-proxy help`**, and its
  output contract (streamed versus buffered, exit codes) is documented only in
  code.
- **The console pages have no documentation.** kei `docs/onboarding/model-profiles.md`
  still says the CLI has no model-profile commands, which is out of date.
- **Console and CLI write different routes.** The console sets the agent's
  profile with `PUT .../agents/{id}/model-profiles`; the CLI uses
  `.../model-profile-assignments`. Whether they behave the same in every case
  (several assignments, default flag) is **[unverified]**.
- **How long a change takes to reach a running harness** depends only on the
  harness's refresh. Kei has no push notification.

## Validation commands

```sh
kei help | grep model-profiles
kei model-profiles assignment --workspace WS --agent AGENT_ID
kei-proxy help | grep -A1 'model profile'
# with KEI_RUNTIME_TOKEN set, on the runtime host:
curl --unix-socket "${KEI_RUNTIME_SOCKET_PATH:-/run/kei-proxy/runtime.sock}" \
  -H "Authorization: Bearer $KEI_RUNTIME_TOKEN" http://localhost/v1/models
```

Don't print `/v1/model-config` or `kei-proxy model profile` output in a shared
terminal: it can contain the provider key.

## Realistic usage boundaries

- This skill explains how a profile is chosen and resolved. It doesn't set up
  a runtime (**kei-runtime-setup**), diagnose one (**kei-setup-doctor**),
  give full CLI syntax (**kei-cli**), or describe tool-call authorization
  (**kei-proxy**, **agentware-sdk**).
- Kei doesn't route requests between models, fail over, or meter spend. Don't
  describe the kei#1164 design as available.
- Never invent a chat route, a CLI flag, or an SDK backend class. The code
  wins over this skill.
