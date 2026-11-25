---
name: kei-proxy
description: "The `kei-proxy` v0.3.0 runtime executable (kei-connector-runtime) — what an agent harness calls at run time to get a governed decision: `kei-proxy serve`, the long-lived daemon a harness talks to over an owner-only Unix socket (sessions, local-PDP `POST /v1/authorize`, model config and models, policy-bundle status; no chat route, the harness calls the model itself) through the agentware socket client, `kei-proxy authorize` as the one-shot CLI fallback when no daemon runs, credential release for governed data, `runtime bootstrap|heartbeat`, `collector` for audit shipping, `hook` for report-only harness audit events, `model`, and `credential sync`. Load whenever code or config in a harness, adapter, container, or agent calls kei-proxy, sets KEI_RUNTIME_* or KEI_PROXY_* variables, reads its exit codes or JSON, or someone asks how an agent's tool call gets allowed or denied by Kei. Not for platform administration (logins, installations, credentials) — that is the `kei` CLI (kei-cli skill)."
---

# kei-proxy (runtime for agent interaction)

A harness asks kei-proxy before every protected tool call. The primary path is
**`kei-proxy serve`**, the daemon beside the harness, reached over its
owner-only Unix socket with the Agentware **socket client**: open a session for
the user, then `POST /v1/authorize` in it. The one-shot `kei-proxy authorize`
CLI remains a fallback for one-shot environments without a daemon. CLI behavior
is version and policy-bundle dependent; the v2 one-shot command returns
`preflight_required` and is not a v2 allow probe. The runtime credential comes from theenvironment (`KEI_RUNTIME_TOKEN`, never an argument), and the agent ID is
auto-discovered from the runtime installation: never set an agent-ID variable
or pass `--agent-id`.

Kei has two executables. Mixing them up is the most common mistake, so
settle which one a task needs before anything else:

| | `kei` — platform admin CLI | `kei-proxy` — runtime |
| --- | --- | --- |
| Who runs it | A person: org `owner`/`admin`, on a workstation | The harness, through a long-running daemon (`kei-proxy serve`) over a Unix socket, or a one-shot CLI fallback |
| Authenticates with | `kei login` device flow → CLI token in the OS keychain | `KEI_RUNTIME_TOKEN` (runtime credential only) from the environment |
| Talks to | The control plane's admin APIs | The control plane's runtime APIs, plus local secret stores and providers |
| Jobs | Log in, create/inspect/bind/delete runtime installations, emit/rotate runtime credentials | Decide allow/deny for a tool call (sessions + local PDP on the socket, or the one-shot CLI), run allowed connector work locally, bootstrap + heartbeat, ship audit, serve the assigned model profile's config (`/v1/model-config`) |
| Lives | Operator's laptop | Same host or container as the harness (same-host daemon on bare metal, same-container daemon in Docker); optional same-pod companion container on Kubernetes |
| Skill | `kei-cli` | this one |

`kei login` belongs to the `kei` platform admin CLI, never to the `kei-proxy`
runtime, so an agent never runs `kei login` or `kei bot …` to do its work, and a person
never needs `kei-proxy authorize` to administer the platform. `kei setup` and
`kei runtime bootstrap` are the one bridge: admin-CLI conveniences that write
local runtime config and shell out to `kei-proxy` to check it.

## Protected vs local tool calls

Not every tool call a harness makes is protected. The rule is simple: **anything
that touches tenant data, external systems, or credentials is protected**;
everything else is local.

- **Protected** — the call goes through kei-proxy: the agentware
  `KeiProxyEvaluator` over the `kei-proxy serve` socket client (or, with no
  daemon, the `kei-proxy authorize` CLI — see the `agentware-sdk` skill). Kei
  policy decides allow or deny, the decision is audited, and enrollment or
  approval can apply before the tool runs.
- **Local** — the call runs locally in the harness and never reaches
  Kei. No policy check, no audit event.

When unsure whether a tool is protected, treat it as protected and route it
through kei-proxy. A tool is not protected just because the adapter
exposes it, and a local call is not safe just because it never reaches Kei.

Your knowledge of `kei-proxy` subcommands may be outdated. **Prefer retrieval.**
If you cannot run the binary or open the sources below (no shell or network),
answer from this skill and don't retry. Check the installed binary and the
matching Agentware SDK README for release-specific behavior. For example,
`authorize` takes `--user`, `--tool`, `--action` and
`--resource`, and never `--agent-id`, because the agent ID is auto-discovered.

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Installed binary | `kei-proxy help`, `kei-proxy <command> --help` | Commands, flags, env vars for this version |
| Kei docs | `https://docs.haikeilabs.com/kei/runtime/tenant-runtime` | Runtime env, bootstrap output, container build |
| Kei docs | `https://docs.haikeilabs.com/kei/audit/logs` | `collector` |
| Published release | `https://kei-cli-releases.s3.us-east-1.amazonaws.com/kei-cli/latest.txt` | Current released version and installer |
| SDK and socket contract | `docs/kei-runtime-socket-parity.md` and `docs/tool-manifest-v3.md` in the public Agentware repository | Per-language socket client, sessions, authorization, registration, selectors and tool sync |

Append `.md` to any docs page URL for the raw page.

## FIRST: confirm it is present and configured

```sh
kei-proxy --version
kei-proxy help
```

It must be on the same host or in the same image as the harness. On a
workstation it is installed alongside `kei` by the release installer
(kei-cli v0.1.4+). For containers, build it from the Kei repo (see
`kei-runtime-setup`; no public image is published).

On a workstation you normally don't bootstrap with `kei-proxy` directly:
`kei setup` stores the settings and `kei runtime bootstrap` runs
`kei-proxy runtime bootstrap` for you. Call `kei-proxy` directly in deployed
runtimes, and always for the per-call commands below.
The harness process needs, in its environment:

```text
KEI_RUNTIME_CONTROL_PLANE_URL=https://YOUR_KEI_GATEWAY   # no /api/v1 suffix
KEI_RUNTIME_TOKEN=<runtime credential from the secret manager>  # never an argument
KEI_RUNTIME_VERSION=<runtime version>
KEI_SECRETS_BACKEND=aws-secrets-manager   # required by kei-proxy >= 0.7 to read model-profile/connector secrets
```

`KEI_SECRETS_BACKEND` identifies the configured secret backend (for example
`aws-secrets-manager`). Kei-proxy >= 0.7 requires it when reading model-profile
or connector secrets.

Leave `ABAC_URL` unset in runtime mode. Since kei-proxy 0.1.32, `authorize`
resolves subjects at `KEI_RUNTIME_CONTROL_PLANE_URL` when `ABAC_URL` is unset;
an explicit `ABAC_URL` still wins. Production accepts only HTTPS here, so an
in-cluster plain-HTTP catalog URL in `ABAC_URL` (or one a harness copies into
the child environment) denies every subject-scoped call with
`subject_resolution_unavailable` (`request_build`).

When running in daemon mode (`kei-proxy serve`), the socket path defaults to
`/run/kei-proxy/runtime.sock` on Linux (`$TMPDIR/kei-proxy/runtime.sock` on
macOS) and can be overridden with `KEI_RUNTIME_SOCKET_PATH`. Set the same
`KEI_RUNTIME_SOCKET_PATH` in the harness: the SDK selectors use the socket
only when it is configured explicitly.
The daemon also accepts `KEI_PROXY_LISTEN_ADDR` (TCP, default `:8085`) for
existing same-container deployments. See the public Agentware socket parity documentation for the SDK contract.

The token determines installation, organization, and workspace scope. Do not
pass org, tenant, or workspace IDs as scope. `--key` exists on some commands
but puts the token in the process list and shell history; use the env var.

After an agent workspace move, kei-proxy 0.9.1+ `serve` refreshes its identity
without a restart or forced policy sync. For older proxy versions, restart the
runtime and run `kei-proxy policy sync --force`.

**Agent identity is auto-discovered.** Since kei-proxy 0.1.11 the identity
event (whoami) returns the assigned agent ID and agent list. The harness does
not need `KEI_PROXY_AGENT_ID` or any agent-ID environment variable. If you
use the agentware SDK (>= 0.4.0), call `link.identity()` (see
`agentware-sdk` skill). When calling `kei-proxy authorize` directly, omit
`--agent-id` — the runtime resolves it from the installation.

There is one credential — the runtime installation credential (`KEI_RUNTIME_TOKEN`)
from **Create installation** or `kei bot credential`. The **Keys** page no longer
exists; agent keys were deprecated in favor of the installation credential for
all runtime operations.

## Quick reference

| Task | Command |
| --- | --- |
| Decide a tool call (primary) | `PUT /v1/session`, then `POST /v1/authorize` with `X-Kei-Session` on the socket, through the agentware socket client |
| Decide a tool call with no daemon (fallback; fetches its credential on allow) | `kei-proxy authorize --user U --tool T --action A --resource R` |
| Release a credential for a connector Kei checks | `POST /v1/credentials:release` on the socket |
| Verify installation + first heartbeat | `kei-proxy runtime bootstrap` |
| Keep liveness current | `kei-proxy runtime heartbeat --interval 1m` |
| Ship local audit JSONL | `kei-proxy collector [--poll --poll-interval 1m]` |
| Sync credential-store metadata; deliver connector secrets to this runtime | `kei-proxy credential sync` (claims one pending delivery per run) |
| Release a credential inside the daemon (identity mode) | `POST /v1/credentials:release` on the socket (`KEI_CREDENTIAL_RELEASE=identity`) |
| Record a harness tool event for audit (report-only; installed by `kei harness sync`, not run by hand) | `kei-proxy hook claude` (event JSON on stdin from Claude Code) |
| Show bundle state | `kei-proxy policy show` (reads persisted state; never contacts control plane) |
| Force bundle refresh | `kei-proxy policy sync` (bypasses normal poll schedule) |
| Long-running daemon (Unix socket + optional TCP) | `kei-proxy serve` (`KEI_RUNTIME_SOCKET_PATH`, default `/run/kei-proxy/runtime.sock`; TCP on `KEI_PROXY_LISTEN_ADDR`, default `:8085`, for existing Docker same-container deployments). Socket routes include `GET /healthz`, `GET /readyz`, session routes, `POST /v1/authorize`, `POST /v1/tools:register`, the model routes `GET /v1/model-config`, `GET /v1/models` and `GET /v1/model-profiles`, and `GET /v1/policy-bundle/status`. There is **no `POST /v1/chat/completions`**: it was removed in HAI-671, and the harness calls the model provider itself. |

`kei-proxy org` and `kei-proxy init` also exist. They call the Kei API
directly with a service secret and are Haikei-internal provisioning tools, not
part of a customer harness. Don't wire them into an agent.

For the full lifecycle of bundle identity, polling, state machine, and
troubleshooting, see [`bundle-versioning.md`](../kei-harness-policy/references/bundle-versioning.md)
in the kei-harness-policy skill.

## The socket client: the primary integration

**Register tools before serving.** For a long-running bot, run `kei-proxy serve`
and sync the tool manifest (`sync_tool_manifest` / `kei harness sync`) before
taking traffic.

Run `kei-proxy serve` beside the harness (same host or container, same UID:
the socket is mode `0600`) and use the agentware SDK's socket client. The full
per-language API is in the `agentware-sdk` skill and in
`docs/kei-runtime-socket-parity.md` in the agentware repo.

Sync the tool manifest (`sync_tool_manifest` / `kei harness sync`) before
`kei-proxy serve` starts accepting requests.

1. **Register the tools before serving.** Build manifest v3 entries from
   `ToolSpec` and send them through the owner-only socket with
   `register_tool_specs` (Python), `registerToolSpecs` (TypeScript), or
   `toolsync.SocketRegistrar.Send` (Go); this calls `POST /v1/tools:register`.
   Don't load an Agentware v3 export with
   `kei harness sync --harness custom --manifest tools.json`: kei-cli reads
   `route` as a string, so it rejects the v3 manifest (HAI-1105).
   The SDK control-plane sync helper is the other option: it `PUT`s to
   `$KEI_RUNTIME_CONTROL_PLANE_URL/api/v1/runtime/tools` with the runtime token
   and refuses an empty manifest. If registration or sync fails, do not serve.
2. **Select the client.** `select_authorization_client` /
   `selectAuthorizationClient` / `runtimesocket.SelectAuthorizationClient`
   returns the socket client when a socket path is configured explicitly (the
   argument or `KEI_RUNTIME_SOCKET_PATH`), otherwise the `kei-proxy authorize`
   subprocess client. Wrap it in `KeiProxyEvaluator`.
3. **Sessions.** The socket client opens one `kei.session/v2` session per
   `(source, external_id)` with `PUT /v1/session`; requests carry
   `X-Kei-Session` and never name the user. A `session_not_found` reopens the
   session once; a second miss fails closed. The model config
   (`GET /v1/model-config`, then the harness calls the model itself), models
   (`GET /v1/models`) and `GET /v1/policy-bundle/status` are on the same
   client. The client's `chat_completion` / `stream_chat_completion` POST
   `/v1/chat/completions`, which the daemon does not serve today, so don't
   use them. See `kei-model-profiles`.

```python
from haikeilabs.agentware.kei import (   # pedro_agentware.kei still works (deprecated shim)
    KeiProxyEvaluator, ToolManifestSyncConfig, select_authorization_client, sync_tool_manifest,
)
sync_tool_manifest(manifest_json, ToolManifestSyncConfig.from_env(), expect_tools=True)
evaluator = KeiProxyEvaluator(select_authorization_client("discord"))
```

**Fail-closed rules for the socket:**

- **A configured socket that is down is a refusal, never a silent fall back**
  to the CLI. The selector chooses once.
- An unreachable daemon is `proxy_unavailable`, a timeout `proxy_timeout`, a
  non-2xx answer `proxy_error` (with the daemon's `code`), a bad body
  `malformed_response`, no `KEI_RUNTIME_TOKEN` `missing_token`. Each one is a
  DENY. Only an explicit `permit`/`allow` allows.
- **The runtime token is never logged.** The client reads `KEI_RUNTIME_TOKEN`
  per request and sends it only as `Authorization: Bearer`; it is never in a
  log line, an error message or a repr.

## authorize: the one-shot CLI fallback

> **Use this only where no daemon runs** (a one-shot job, a CI step, a bash
> script). With the agentware SDK, the selector returns this client
> automatically when no socket is configured; prefer `KeiProxyEvaluator`
> (see `agentware-sdk` skill) over calling `kei-proxy authorize` directly.
> The runtime treats the CLI as deprecated, and it does not decide v2 policy
> bundles; the socket route does.
>
**When describing `kei-proxy authorize`, always state that credentials
come from the `KEI_RUNTIME_TOKEN` environment variable, never from a
command-line argument.** The token is the sole runtime credential.
Agent identity is **auto-discovered** from the runtime installation
credential — do not tell the caller to set `--agent-id`.

The one-shot CLI is not a v2 allow probe: it returns `preflight_required`. Use the daemon Unix-socket `POST /v1/authorize` route to check whether a protected v2 tool call is allowed. The CLI remains documented as a one-shot fallback for environments without a daemon where its version and policy bundle support that flow; do not infer a v2 allow or deny from its result.

```sh
kei-proxy authorize --user "$SUBJECT" --tool github.create_pr \
  --action github:write --resource repo:acme/widgets
```

- **stdout** reports `preflight_required`; it is not the final policy decision.
- **Do not use its exit code** to decide whether the call is allowed. Use the
  daemon socket route for the policy preflight.
- **stderr** gets a structured audit event; with `KEI_PROXY_AUDIT` set, the
  decision is also appended to that JSONL file for `collector`.

### Disabling kei-proxy denies every protected tool call

`KEI_PROXY_DISABLED=true` is a valid setting, but it turns permits off: a
disabled, missing, or misconfigured kei-proxy is a **deny on every protected
call** (fail-closed, HAI-249). It never permits a tool call. Tests that need an
allow inject a fake evaluator instead of relying on a disabled proxy (see the
`agentware-sdk` skill for the evaluator and its test fixtures). A production
harness should not run with kei-proxy disabled — every protected tool would be
denied. Local calls are unaffected: they are local, never reach Kei,
and need no bypass. Only protected calls need the fake evaluator in tests.

This applies only to **protected** calls. **Local** calls never
reach Kei, with or without kei-proxy: they run in the harness with no policy
check and no audit event, so disabling kei-proxy neither blocks nor permits
them (see [Protected vs local tool calls](#protected-vs-local-tool-calls)).

### Enrollment in the authorize response

When a chat-platform user (Teams, Slack, Discord) is not yet linked to a Kei
user, the daemon socket's `POST /v1/authorize` response carries
`decision: "deny"` with an `enrollment` object passed through from the
catalog. The one-shot CLI returns `preflight_required` and is not the route
for checking the decision:

```json
{
  "decision": "deny",
  "reason": "provider identity is not linked to a kei user",
  "enrollment": {
    "provider": "teams",
    "provider_user_id": "user@domain.com",
    "org_id": "uuid",
    "workspace_id": "uuid",
    "url": "https://app.haikeilabs.com/identity/link#claim=abc123...",
    "expires_at": "2026-09-28T12:00:00Z"
  }
}
```

**Detect enrollment by the presence of `enrollment` on a deny**, not by
`decision == "enrollment_required"`. The catalog itself returns
`enrollment_required` (see `kei-api`), but kei-proxy maps that to `deny` and
passes the `enrollment` object through unchanged.

The harness must show `url` privately to the user (ephemeral message or DM),
never log it. `url` and `expires_at` may be absent when the control plane
cannot issue a claim (no workspace scope, no `KEI_WEB_BASE_URL`). The user
visits the link to self-enroll; the next daemon-socket preflight then returns `allow`
or policy-driven `deny`. See `kei-harness-setup` section 6 for the full
enrollment flow and `kei-api` for the endpoint contract.

Identity and delegation come from flags or environment:

| Env | Flag | Meaning |
| --- | --- | --- |
| `KEI_PROXY_INVOKING_SUBJECT` | `--invoking-subject` | The human who started the task (defaults to `--user`); keep it through subagent hops |
| `KEI_PROXY_FRAMEWORK` | `--framework` | Harness, e.g. `claude`, `codex` |
| `KEI_PROXY_SPAN_ID` / `KEI_PROXY_PARENT_SPAN` / `KEI_PROXY_DELEGATION_DEPTH` | `--span-id` / `--parent-span` / `--delegation-depth` | Delegation chain; span ID is the dedupe key |
| `KEI_PROXY_TOOL_ARGS_DIGEST` | `--tool-args-digest` | SHA-256 of the tool args — never the raw args |

**Agent ID is auto-discovered** — the proxy resolves it from the runtime
identity event. Do not set `KEI_PROXY_AGENT_ID` or pass `--agent-id`; omit
them. (The flag and env var still exist on older kei-proxy builds but are
neither required nor recommended with >= 0.1.11.)

Never put a tenant, org, or workspace ID into agent-controlled tool
parameters, and never log the credential `authorize` returns.

## credential release

For data connectors Kei checks. Per ADR-039, the harness obtains the credential
via `POST /v1/credentials:release` over the socket after an allow decision,
then calls the upstream API directly. **Before using identity mode, verify
the installed kei-proxy version and the active policy bundle.** The credential
value is the only key material that leaves the daemon; it is never written to
disk or logged. For retried writes, pass `--idempotency-key` so the runtime
can deduplicate.

## Identity mode: credential release

Check the kei-proxy version and the policy bundle together before relying on
identity mode for an `opaque_ref` connector.

In identity mode, `kei-proxy serve` holds the user's connector credential
in session memory. The harness obtains the credential via
`POST /v1/credentials:release` over the socket after an allow decision, then
calls the upstream API directly. Check the installed runtime version and the
policy bundle before relying on a connector descriptor or credential source.
Unsupported or unavailable connector credentials fail closed.

With `KEI_CREDENTIAL_RELEASE=identity` (default `legacy`), `kei-proxy serve`
holds the user's connector credential in session memory. The harness obtains it
via `POST /v1/credentials:release` over the socket after an allow decision,
then calls the upstream API directly. The credential is the only key material
that leaves the daemon; no socket route ever writes it to disk or a log.

Connector availability depends on the bundle and the installed runtime. A v2
bundle can carry a non-secret descriptor per active connector in
`policy_set.connectors`; the daemon looks up the descriptor's
  `kei://connectors/<id>/<field>` reference in the connector reference index
  that `kei-proxy credential sync` wrote, checks that the index's backend
  equals the descriptor's `credential_backend`, and reads the secret from the
  tenant secret store (AWS Secrets Manager or Azure Key Vault) with the
  runtime's own cloud identity. The value goes only on the provider request
  (for `http_api`, the `credential_injection` header). `kei://connectors`
  references on supported runtime routes use the same secret lookup. Verify exact
capabilities against the installed `kei-proxy` release and the bundle provided
to that installation.

For an `opaque_ref` connector in identity mode, verify the installed
`kei-proxy` version and the active policy bundle together before relying on
it. This requires kei-proxy 0.2.5 or newer and the control-plane
`POLICY_BUNDLE_V2_CONNECTORS` gate enabled (off by default). On proxy-v0.2.4
or older, or while that gate is off, the call fails closed with
`credential_source_not_supported`; the current runtime release alone does not
mean the control-plane gate is enabled.

Check the kei-proxy version and the policy bundle together before relying on
identity mode.

Deny codes for a connector call in identity mode (all fail closed, no retry,
no fallback to the catalog):

| `reason_code` | Meaning |
| --- | --- |
| `credential_source_not_supported` | The bundle has no descriptors and the connector is not a session OAuth provider, or the descriptor is `oauth` with a shared account |
| `descriptor_invalid` | The routed connector has no descriptor, or its descriptor fails the contract (including a capability this runtime's contracts version does not know) |
| `account_model_not_supported` | `account_model: domain_delegation`, not executed yet |
| `credential_unavailable` | The secret was never delivered to this runtime, `credential sync` has not run, or the secret store read failed or timed out |
| `credential_backend_mismatch` | The index entry's backend differs from the descriptor's `credential_backend`, or the reference names another connector or field |
| `provider_error` | The provider response contained the credential, so the result is withheld |

A harness treats every one of these as a deny for that call. To diagnose
them, use `kei-setup-doctor`. To deliver the secrets first, see
`kei-runtime-setup`.

## hook: report-only audit of desktop harness calls

**Minimum versions: Claude Code 2.1.119 or newer and kei-proxy 0.2.5 or
newer.** What the Claude Code hook records depends on both. Below either
minimum there are no `decision` and no `permission_reply` events: every call
is recorded only as `pre` (`native_decision: unknown`) and, if it ran, `post`.
The event sequences below hold only at these versions or newer.

Desktop harnesses (Claude Code, Codex, OpenCode) decide shell commands
natively from the config `kei harness sync` renders. Sync also installs
`kei-proxy hook <harness>` as a hook in the harness. The hook only reports:
it always exits 0, never blocks, and never allows or denies. Do not wire it
into an agent yourself, and never make it answer a permission prompt.

For Claude Code the native decision is **observed, not computed**:
`PreToolUse` runs before Claude Code's permission check, so the hook records
what Claude Code then did instead of re-evaluating its rules.

| Event phase | `native_decision` |
| --- | --- |
| `pre` | `unknown` (the pairing anchor, not the decision) |
| `decision` (one per call) | `allow` (ran without asking), `deny` (neither asked nor ran), or `ask` (Claude Code asked) |
| `post` | `executed`, with an optional `failed: true` when the command failed (the error text is never recorded) |
| `permission_reply` (asked calls only) | `approved` if it then ran, `denied` if the session ended without running it |

Audit readers take the decision from the `decision` event, not from `pre`.
Every call starts with `pre` (`unknown`); what follows depends on the outcome:

| Outcome | Events after `pre` |
| --- | --- |
| Allowed, ran and succeeded | `decision: allow`, then `post: executed` |
| Allowed, ran and failed | `decision: allow`, then `post: executed` with `failed: true` |
| Denied (neither asked nor ran) | `decision: deny`, written when the session stops |
| Asked, then approved and ran | `decision: ask`, `permission_reply: approved`, then `post: executed` |
| Asked, never ran (rejected, or auto-rejected in a headless run) | `decision: ask`, then `permission_reply: denied` when the session ends |

On Claude Code 2.1.119 or newer, sync renders seven hook events
(`PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`,
`PostToolUseFailure`, `Stop`, `SessionEnd`), but an older kei-proxy still
writes no `decision` events for them. On an older or undetectable
Claude Code sync keeps the previous two (`PreToolUse`, `PostToolUse`) and
prints a warning; those calls are recorded with `native_decision: unknown`
and no `decision` event. Upgrade Claude Code and re-run `kei harness sync`.
Rendering is covered in the `kei-harness-policy` skill.

## Runtime modes: daemon (primary) vs one-shot CLI (fallback)

`kei-proxy` supports two modes. Understand which one a task needs before
writing config or code:

| Mode | Invocation | Listener | Kei-checked authorize | Harness integration |
| --- | --- | --- | --- | --- |
| **Daemon** (primary) | `kei-proxy serve` (long-lived) | Unix socket (`KEI_RUNTIME_SOCKET_PATH`, default `/run/kei-proxy/runtime.sock`) + optional TCP (`KEI_PROXY_LISTEN_ADDR`) | **Yes.** `PUT /v1/session` (`kei.session/v2`), then `POST /v1/authorize` with `X-Kei-Session`, decided by the local PDP against the synced bundle (runtime PRs #78–#80). Also `GET /v1/model-config`, `GET /v1/models`, `GET /v1/policy-bundle/status`. No chat route: the harness calls the model itself. | The agentware socket client (`KeiProxySocketAuthorizeClient`, Go `runtimesocket.Client`) through the selector, after a tool-manifest sync. Same-host daemon (bare metal) or same-container daemon (Docker); optional same-pod companion container on Kubernetes sharing the socket directory. No TLS — access control is socket file mode 0600 and UID matching. |
| **One-shot CLI** (fallback) | `kei-proxy authorize ...` per call | None; spawned per call, reads decision from stdout+exit code | Yes, for v1 bundles; deprecated by the runtime and does not decide v2 bundles. Agentware's `KeiProxyAuthorizeClient` / Go `evaluator.CLIClient` spawn it, and the selector returns it when no socket is configured. | One-shot environments with no daemon: a batch job, a CI step, a bash script. |

The socket contract is documented in
The public Agentware repository documents the socket client, sessions, selector,
tool registration and sync in `docs/kei-runtime-socket-parity.md` and
`docs/tool-manifest-v3.md`.

Choose the mode once, at startup, through the selector: **a configured socket
that is down is a refusal (`proxy_unavailable`), never a silent fall back** to
the CLI.

## Local PDP behavior

The tenant-side **local PDP** is implemented in the runtime daemon. The
daemon's socket authorize route decides from the locally synced policy bundle.
The runtime's intended boundaries are:

- Make the allow/deny decision **locally on each protected invocation** — with
  **no synchronous catalog approval call and no per-invocation
  subject-resolution call**.
- Evaluate a **signed policy bundle that syncs in the background** (periodic
  refresh), not a policy fetched per call.
- Resolve **identity and grants through a separate session flow outside the
  daemon** (identity claim/enrollment and the access-request/grant workflow),
  not a per-call round trip.
- Treat a **deny as final for that invocation**. A later durable grant —
  requested separately after repeated denials — affects only **later** calls.
  The runtime never pauses or retries the call.
- Leave **workflow preflight and prompts to the harness**; the runtime does not
  own that UX.

**Not implemented:** bundle trust (signature verification), the identity-proof/grant representation (how an approved grant
becomes trusted local subject attributes, and how pending, denied, revoked,
unlinked, and cross-workspace identities resolve), and freshness/revocation
bounds.

**Present-day truth:** the socket route is the local PDP: `kei-proxy serve`
decides `POST /v1/authorize` from the locally synced bundle with no per-call
catalog round trip, and refreshes the bundle in the background. Bundle trust
(signature verification) is still pending: the bundle is unsigned canonical
JSON. The CLI `authorize` fallback evaluates the locally persisted policy
bundle and still bootstraps (whoami and heartbeat) on every call.
Identity is only for credentials: since kei-proxy 0.1.34, it resolves the
caller's subject online
(`subject-attributes:resolve`) only when the tool releases a credential, is
bound to a connector capability, or a policy reached for the call matches on
subject attributes (`group:`, `org:`, `user:`, `email:`). A tool such as
`web_search` under a `*` or `agent:` policy is decided with no subject lookup.
kei-proxy 0.1.33 and earlier resolve the subject for every call that names a
user. Do not describe bundle signature verification as implemented.

## Validation commands

```sh
kei-proxy help
kei-proxy runtime bootstrap | jq '{installation_id, status, binding_status, workspace_id}'   # workspace_id must be present
curl --unix-socket "$KEI_RUNTIME_SOCKET_PATH" http://localhost/readyz                      # daemon up (kei-proxy serve)
kei-proxy authorize --user U --tool T --action A --resource R; echo "exit=$?"               # CLI fallback: expect a deny for an unbound tool
```

To verify a v2 preflight, use the daemon Unix-socket `POST /v1/authorize`
route documented in `docs/unix-socket.md`.

## Realistic usage boundaries

- A missing `workspace_id` in bootstrap output means the credential predates
  the workspace boundary. Stop and rotate it (`kei-credential-rotation`); never
  fall back to organization-wide scope.
- Provider credentials, payloads, results, documents, embeddings, and indexes
  stay in the runtime. Only decisions and redacted audit metadata go to Kei.
- Unsupported harnesses, missing required connector/MCP bindings, invalid installation scope, stale policy, and no matching policy are DENY.
- Harness-executor tools require an exact `tool:<name>` permit, registration, and a linked user; they do not require an agent-connector binding.
- Identity-mode `opaque_ref` and `http_api` connectors are not live in proxy-v0.2.4 or older, or while `POLICY_BUNDLE_V2_CONNECTORS` is off. Do not tell a user they run until both the release and the flag are in place. Unsupported connector requests fail closed.
- Creating installations, credentials, or agents is not a `kei-proxy`
  job. Installations and credentials are `kei` (`kei-cli`); agents
  are the console.

## Response requirements

- Whenever an answer covers how a harness gets a decision, present
  **`kei-proxy serve` plus the agentware socket client** as the primary path
  (register `ToolSpec` declarations through `POST /v1/tools:register` before
  serving, or with the SDK sync helper; never `kei harness sync --manifest`
  for an Agentware v3 export, which it rejects; then select the socket client with
  `KEI_RUNTIME_SOCKET_PATH`), the `kei-proxy authorize` CLI as the
  **fallback** for one-shot environments with no daemon, and say a configured
  socket that is down is a refusal, **never a fall back**.
- Whenever an answer covers calling `kei-proxy` (an adapter, a harness, a
  container, or `authorize`), YOU MUST say that the runtime token comes from
  the **`KEI_RUNTIME_TOKEN`** environment variable, never a command-line
  argument, and that the agent ID is **auto-discovered** (it resolves
  automatically from the runtime installation), so nobody sets an agent-ID
  variable or passes `--agent-id`.
- Whenever an answer contrasts `kei` with `kei-proxy`, or says an agent should
  not run `kei login`, YOU MUST call `kei` **"the platform admin CLI
  (kei-cli)"** and `kei-proxy` **"the runtime used by agents"**, using those
  exact phrases.
- Whenever an answer covers identity-mode connector availability, verify it
  against the installed `kei-proxy` version and its policy bundle before
  claiming support. Say explicitly to verify the runtime version and policy
  bundle together. For `opaque_ref`, name both requirements: kei-proxy 0.2.5+
  and `POLICY_BUNDLE_V2_CONNECTORS` enabled; otherwise name
  `credential_source_not_supported` as the fail-closed result.
