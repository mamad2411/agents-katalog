---
name: agentware-sdk
description: Use for requests to build a custom AI agent or harness with Agentware, typed tools, local models, or agent-loop guardrails; route unrelated tasks only when they match the product scope below. Use the open-source Agentware SDK — policy enforcement and audit middleware for agent tool calls, in Go, Python, and TypeScript. Use when working with middleware policy/audit, AuditedToolClient, ToolExecutor, CallerContext, Action ALLOW/DENY/FILTER, rate limits, guardrails (response validator, step enforcer, error tracker, nudge), KEI_RUNTIME_TOKEN, OpaqueTokenProvider/JWTTokenProvider, HarnessManifest, KeiProxyEvaluator, kei-proxy, the kei-proxy serve socket client (KeiProxySocketAuthorizeClient, runtimesocket, select_authorization_client, sync_tool_manifest / toolsync), the haikeilabs.agentware import, delegation, KeiScope, GovernedTool, tool-manifest export, building an agent end to end (OpenAIBackend model wiring, tool_calls and reasoning_content parsing, ReasoningAdapter, the model from a Kei model profile, tool:<name> policies, agentware.eval-suite.v1 evals), the third-party harness contract, or the action-tool/connector boundary. This is generic agentware guidance; the tool-adapter/governor lane pattern lives in the assistant's developer skills, and no invented APIs are allowed — the code and docs in the repo are the source of truth.
---

# Open-source Agentware SDK

For an Agentware build, start with the user’s desired outcome and a runnable local
example. Kei is optional for local work. Skills guide the assistant; they do not
install SDKs, configure Kei, or grant permissions. Verify APIs in the relevant
language source and tests. Do not route a generic unrelated programming task
to Agentware solely because it mentions an agent or a model.

## Response requirements

When writing responses about agentware:

- For TypeScript runtime identity, state the compatibility minimums directly:
  Agentware 0.16.0, kei-proxy v0.6.5, and kei-cli 0.3.6. Read the assigned
  agent ID from `link.identity()?.defaultAgentId` and the agents from
  `link.identity()?.agents`; when identity is unavailable, deny protected calls
  and never guess a fallback agent ID.
- Audit argument storage depends on the port: the Go middleware records a
  SHA-256 digest of the redacted arguments (`ToolArgsDigest`), not the raw
  arguments; Python `AuditRecord.args` and `InMemoryAuditor` keep the supplied
  arguments, so sanitize them before recording.
- For a Python harness beside `kei-proxy serve`, sync tool declarations before
  serving. The socket registration option is `ToolSpec` with
  `register_tool_specs` to `POST /v1/tools:register`.
- When constructing `KeiProxyEvaluator`, name the socket client it wraps:
  `KeiProxySocketAuthorizeClient`, the socket client the selector returns when
  `KEI_RUNTIME_SOCKET_PATH` is set.
- For TypeScript, say plainly that the async evaluator cannot be used directly
  as synchronous `withPolicy` middleware; call `evaluate()` directly and await it.
- Use the exact phrase "fail-closed" (hyphenated compound adjective) when describing the deny-by-default posture.
- For downstream failures, tell the implementer to verify the exact types, methods, and failure behavior against the port's **source and tests** — include both words.
- When discussing enrollment or connect URLs, use the contiguous phrase "never log" (no markdown formatting between the words).
- When explaining enrollment, state that the user must visit the URL to **link their chat identity** before protected tools work.
- When explaining why enrollment is needed, state the user must **link their chat identity** first.
- When describing how middleware handles a downstream failure after a policy allowance, distinguish an **allowed** decision from successful provider execution — use the exact word "allowed" (not just "allow").
- When naming the three required third-party harness components, also mention `HarnessContract` assembly and `validate_contract`.
- When an answer connects a harness to kei-proxy, present `kei-proxy serve` plus the socket client as the primary path: sync the tool manifest first (`sync_tool_manifest` / `syncToolManifest` / `toolsync.Sync`; an empty manifest is refused), then build the client with the selector (`select_authorization_client` / `selectAuthorizationClient` / `runtimesocket.SelectAuthorizationClient`) and `KEI_RUNTIME_SOCKET_PATH`. The selector still chooses the deprecated `kei-proxy authorize` subprocess fallback when no socket path is configured; recommend the socket path for new integrations, and do not imply the deprecated path is equivalent.
- When a configured socket is down, say it is a refusal (`proxy_unavailable`) and **never a fall back** to the CLI, and say the runtime token is **never logged**.
- When an answer covers which model the agent uses, `model_config()`, or the socket's model or chat methods, **name the `kei-model-profiles` skill** for how the profile is assigned and resolved.

Agentware is an MCP-compatible middleware layer that sits between an LLM
orchestrator and tool execution: calls routed through it can be evaluated and
audited. Configure the evaluator and auditor explicitly and verify the selected
port and call path. Python `AuditedToolClient` allows calls without an evaluator
and can construct caller context from supplied IDs; it does not authenticate
those IDs. The host must validate identity and enforce fail-closed behavior. It is language-agnostic and ships three ports: Go
(`github.com/haikeilabs/agentware/go`), Python (published as `haikeilabs-agentware` and imported as
`haikeilabs.agentware`, with `pedro_agentware` kept as a deprecated shim), and
TypeScript (\`@haikeilabs/agentware\`). This skill is about the
library and its seams.

## General middleware principles

These principles apply regardless of the specific agentware library or language.
They are extracted from practical middleware design and reinforced by the
Agentware codebase.

### Tool-call boundary

- Validate tool names and arguments against a closed registry before execution.
- Carry authenticated caller and delegation context separately from user text.
- Make authorization an explicit allow, deny, or filtered decision.
- Return bounded, typed results and stable correlation IDs.
- An allowed decision is not a downstream execution guarantee — the provider
  may still fail after the policy passes.
- fail-closed on malformed requests, missing identity, policy errors, timeouts,
  and unavailable providers.

### Audit boundary

Record the minimum metadata needed to reconstruct a decision: correlation ID,
caller pseudonym, tool name, policy decision, result status, timestamps, and
safe error category. Do not store bearer tokens, raw credentials, hidden model
reasoning, or unnecessary user content.

### Reasoning and context trees

When a backend exposes reasoning, normalize it into bounded structured events:
goal, observation, decision, tool-call, tool-result, conclusion, or blocker.
Retain summaries and evidence references, not raw chain-of-thought. Preserve
parent/child links and tool-call IDs so an evaluator can explain the path
without exposing private reasoning.

### Testing

Test allowed and denied calls, malformed arguments, missing identity, tool
failures, recovery, ordering, budget exhaustion, and audit redaction. Prefer
deterministic scripted backends for CI and reserve live provider tests for
explicit integration environments.

## Where things live

- `python/` — package `haikeilabs-agentware`, imported as `haikeilabs.agentware`.
- `go/` — module `github.com/haikeilabs/agentware/go`.
- `typescript/` — package `@haikeilabs/agentware`, published to npm.
- `docs/engineering-design.md` — the language-agnostic design; `docs/middleware-llm-guide.md`
  the harness guide; `docs/harness-contract.md` the third-party harness contract;
  `docs/tenant-proxy-reference.md` the authoritative architecture;
  `docs/action-tool-boundary.md` the enforcement/execution boundary.
- `docs/kei-runtime-socket-parity.md` and `docs/tool-manifest-v3.md` document
  the runtime socket client and tool registration contracts.

## Install and dependencies

As of 2026-11-05, the latest verified npm, PyPI, and Go module proxy releases
are Agentware 0.16.0. Check the package registries and the Agentware README
compatibility table for newer releases and the versions required by your setup.
For SDK 0.16.0 with Kei, the checked source table lists kei-proxy v0.6.5 and
kei-cli 0.3.6 as minimums; these are integration minimums, not SDK versions.

### Go

- Module: `github.com/haikeilabs/agentware/go`.
- Install: `go get github.com/haikeilabs/agentware/go`.
- Check `go/go.mod` for the current Go version and dependencies.

### Python

- Package: `haikeilabs-agentware`, imported as `haikeilabs.agentware`.
- Install: `pip install haikeilabs-agentware`.
- Runtime dependencies (`python/pyproject.toml`): `pydantic>=2.0`,
  `httpx>=0.27.0`. Requires Python >=3.10. Optional extra `inference` adds
  `pgmpy>=0.1.26`; `dev` adds pytest/ruff/mypy.

### TypeScript

- Package: `@haikeilabs/agentware`.
- Install: `npm i @haikeilabs/agentware`.
- Runtime dependencies (\`typescript/package.json\`): \`minimatch\`, \`zod\`. No peer
  dependencies. Requires Node >=18.

## The core pattern (same in all three ports)

The pattern is shared; the spelling is not. Go, Python, and TypeScript name and
shape these types differently (for example `Execute` vs `execute`, error
return vs raised exception, sync vs async). The names below are a map, not a
signature reference. Before writing integration code or telling someone
"this type exists", open the port they are using (`go/`, `python/`,
`typescript/`) and confirm the exact type, method, argument order, and
failure behavior there, including in its tests. Say which port you checked. If
you cannot check, say the names are unverified.

1. **Types**: `Action` (`ALLOW` | `DENY` | `FILTER`), `CallerContext` (user/session/role/
   source/trusted + delegation fields `invoking_subject`, `parent_span`, `delegation_depth`),
   `Decision` (action + rule + reason + redacted args), `MessageType`/`MessageMeta`.
   `ToolDefinition` lives in the LLM/request layer, not middleware/types.
2. **Policy interface**: `PolicyEvaluator` is the middleware decision seam.
   Python does not ship a local `Policy`/`Rule` engine or
   `SimplePolicyEvaluator`; connect a supported evaluator such as
   `KeiProxyEvaluator` or implement the interface for your policy source.
3. **Auditor**: `AuditRecord`, `AuditFilter`, `InMemoryAuditor`, `NoOpAuditor`; async batched
   logger in Go (`AsyncLogger` with drop counting).
4. **Middleware**: `MiddlewareImpl.execute` (deny → `(None, False, reason)`, filter →
   redacted args), `with_policy`, `with_auditor`, `new_middleware()`.
5. **Tool client**: `AuditedToolClient` — async `Execute(tool_name, args, user_id,
   channel_id, guild_id, func, caller)`; raises `PermissionError` on denial; records to
   the auditor.
6. **Guardrails**: `guardrails/` — `response_validator`, `step_enforcer`, `error_tracker`,
   `nudge`; the inference loop in `middleware/inference.py` (`run_inference()`,
   `RetriesExhaustedError`).

Audit fields and outcome visibility vary by port and integration. Go
(`go/middleware/middleware.go`) redacts, then stores a SHA-256 digest of the
arguments as `ToolArgsDigest`. In Python, `InMemoryAuditor` retains the
supplied arguments, so sanitize sensitive values before recording; do not
claim every port hashes or redacts arguments automatically. Check the
selected auditor's source and tests.

## Build an agent end to end

A builder goes from tool declaration to evals in five steps. Each step names
the SDK API to use and where the deeper material lives. The details, with
source lines per port, are in [`references/end-to-end.md`](references/end-to-end.md).
Verify each API in the port's **source and tests** before you rely on it.

| Step | Use | Deeper |
|---|---|---|
| 1. Declare tools | `ToolSpec` (`name`, `parameters`, `service`, `source`, `operation_class`, `route`), exported as the `kei.tool-manifest/v3` manifest and registered before serving. Registering a tool is not a grant | [Making protected tool calls](#making-protected-tool-calls), `kei-agents` |
| 2. Wire the model | Python `OpenAIBackend(model, base_url, api_key)`, TypeScript `OpenAIBackend({ model, baseUrl, apiKey })`, Go `llm.NewServerBackend(llm.ServerConfig{...})`. Take `model` and `endpoint` from the agent's **Kei model profile** (`model_config()` on the socket client), not from code | `kei-model-profiles`, `build-agents-agentware` |
| 3. Parse tool calls and reasoning | `Response.tool_calls` (`parse_tool_calls`: arguments as a JSON string or an object; anything unparseable becomes `{}`, so validate against the schema), `Response.reasoning` (`reasoning_content`), `ReasoningAdapter().strip()` / `.extract()`, `get_formatter(model)` per model family | `kei-openai-backends` |
| 4. Policy | `KeiProxyEvaluator(select_authorization_client(source))` on `AuditedToolClient`. The admin writes `kei policy create --workspace WS --group G --allow tool:NAME` and checks it with `kei policy test tool:NAME --workspace WS --as group:G`. Deny wins, and an unmatched tool is denied | [KeiProxyEvaluator per language](#keiproxyevaluator-per-language), `kei-harness-policy` |
| 5. Evals | An `agentware.eval-suite.v1` suite (`tool`, `args`, `required_arg_keys`, `forbidden_arg_keys`, `forbidden_tools`, deny cases with `allowed_tools`) run with `python -m evals.main --suite ... --model-profile ... --repeats 3`. Aim for 90% locally; the Agentware gate is 95% | `test-agents` |

Limits that change what you build:

- Python `run_inference` does not send its tools to the model. Call
  `backend.complete(messages, tools)` in your own loop.
- Python `OpenAIBackend` sends no sampling parameters.
- TypeScript `AgentLoop` runs tools with no policy hook, so call
  `evaluator.evaluate()` before each tool.
- No SDK backend runs over kei-proxy: the socket client's chat methods call a
  route `kei-proxy serve` does not serve.
- Python has no rate limiter.

## Python runtime identity/auth integration (from Agentware 0.11.0)

- `python/src/haikeilabs/agentware/kei/auth.py` — `TokenType` (OPAQUE | JWT),
  `BOOTSTRAP_TOKEN_ENV = "KEI_RUNTIME_TOKEN"`, `OpaqueTokenProvider` (current, no auto-renew;
  `invalidate()` is fail-closed with `httpx.HTTPStatusError`), `JWTTokenProvider` (future
  exchange/refresh/revoke contract, gated behind explicit `enable()`, else fail-closed).
- `python/src/haikeilabs/agentware/kei/config.py` — `HarnessManifest` (schema `1.0.0`,
  `extra="forbid"`), `validate_manifest` rejects any manifest containing the bootstrap secret,
  `load_manifest`, `get_config`.
- `python/src/haikeilabs/agentware/kei/proxy.py` — `discover_proxy`/`run_proxy`/`stop_proxy`;
  the token reaches the `kei-proxy` subprocess **only via env, never argv**.
- Contract tests: `python/tests/kei/` — `fake_kei_server.py` (`FakeKEIServer`,
  `ThreadingHTTPServer` implementing `/auth/exchange`, `/auth/refresh`, `/auth/revoke`,
  `/config`) plus `contract_test.py`, `auth_test.py`, `config_test.py`, `proxy_test.py`.
  Fixture: `fixtures/kei/harness-v1.json`.
- Go (\`go/kei/evaluator/\`) and TypeScript (\`typescript/src/kei/\`) now have
  parity KeiProxyEvaluator modules. All three ports follow the shared parity
  table in \`fixtures/kei/authorize-cases.v1.json\`; see
  \`docs/kei-proxy-evaluator-parity.md\`.

### Runtime environment for the harness and proxy

The harness and `kei-proxy` are co-located in the same container or host
runtime. Put the runtime configuration in the harness service environment so
the proxy subprocess inherits it:

```text
KEI_RUNTIME_CONTROL_PLANE_URL=https://app.haikeilabs.com
KEI_RUNTIME_TOKEN=<secret-manager-value>
KEI_RUNTIME_VERSION=<deployed-version>
```

The control-plane value is the gateway base URL; do not append `/api/v1`. In
Docker or a service manifest,
inject the URL and version as ordinary environment values and inject
`KEI_RUNTIME_TOKEN` from a protected secret or env-file. Never pass the token
as an argv flag, write it to logs, or derive authoritative scope from
`KEI_ORG_ID`; the runtime token establishes the installation and workspace
scope; the org is derived through the workspace.

The harness needs **only** `KEI_RUNTIME_TOKEN` and the control-plane URL.
Agent identity is not a user-supplied environment variable — the runtime
discovers it automatically (see below).

## Reading agent identity from the runtime

Since agentware SDK 0.4.0 (`@haikeilabs/agentware`, Python `haikeilabs.agentware`,
Go `github.com/haikeilabs/agentware/go`) and kei-proxy 0.1.11, the agent identity
assigned to a runtime installation is available through the runtime identity
event — not from an environment variable. The harness only needs
`KEI_RUNTIME_TOKEN` and the control-plane URL; the SDK discovers the agent
automatically from the `kei-proxy` identity response.

**TypeScript** (`@haikeilabs/agentware`):

```typescript
const identity = link.identity();
const defaultAgentId = identity?.defaultAgentId;  // string | undefined
const agents = identity?.agents;                   // Agent[] | undefined
```

**Python** (`haikeilabs.agentware`):

```python
identity = link.identity()
default_agent_id = identity.default_agent_id  # str | None
agents = identity.agents                      # list[Agent] | None
```

**Go** (`github.com/haikeilabs/agentware/go`):

```go
identity := link.Identity()
defaultAgentID := identity.DefaultAgentID  // string
agents := identity.Agents                 // []Agent
```

If `identity` is `None`/`undefined`/`nil` — because the runtime hasn't
bootstrapped yet, `kei-proxy` is older than 0.1.11, or agentware is older than
0.4.0 — **deny protected calls**. Never guess a fallback agent ID.

## Third-party harness contract

`docs/harness-contract.md` defines how a third-party harness gets guardrails from
agentware without depending on an agent framework. A harness provides three
required components:

1. **AuthProvider** — supplies tokens for the KEI API (use `OpaqueTokenProvider`, or
   implement the `get_token`/`invalidate`/`get_token_type` protocol).
2. **ToolExecutor** — executes tools on behalf of agents (implement `execute(tool_name, args)`).
3. **SecretProvider** — sources the bootstrap secret `KEI_RUNTIME_TOKEN`
   (use `EnvSecretProvider`).

Assemble with `HarnessContract(auth_provider, tool_executor, secret_provider)` and
validate with `validate_contract`. Optional components have defaults: `policy_evaluator`
(`None` = allow all), `auditor` (`InMemoryAuditor`), `proxy_process` (`None`).
`KeiProxyEvaluator` (`kei/evaluator.py`) is the policy-enforcement seam and is
**fail-closed: every path that is not an explicit `permit`/`allow` is denied**.

Fail-closed rules: unknown policy decision → DENY; unreachable proxy → DENY; missing
credential → DENY; expired token → DENY.

\`KeiProxyEvaluator\` carries two opaque payloads from \`kei-proxy authorize\`
on DENY decisions:

- \`decision.enrollment\` — for unlinked chat-platform users who must link
  their identity first. Contains \`url\` (one-time claim link), \`provider\`,
  \`provider_user_id\`, \`org_id\`, \`workspace_id\`. Show \`url\` privately,
  never log it, never cache an expired link.
- \`decision.connect\` — for users whose connector OAuth session has expired
  or needs reconnection. Contains \`url\` (one-time reconnect link), \`provider\`,
  \`connector_id\`, \`expires_at\`, \`reason\`. Show \`url\` privately, never
  log it. The harness must deliver the link to the user and never expose it
  outside the private channel.

## The kei-proxy socket client (primary integration)

A deployed harness runs **`kei-proxy serve`** beside it and talks to the
daemon over its owner-only Unix socket with the SDK **socket client**. It
opens a session per user, authorizes in that session, and, where the harness
needs them, reads the model config (the harness then calls the model itself) and the bundle status. The selector still
chooses the per-call `kei-proxy authorize` subprocess
(`KeiProxyAuthorizeClient`, Go `evaluator.CLIClient`) when no socket is
configured. This is a **deprecated fallback**, not the recommended path for new
integrations; configure the socket explicitly. Source of truth:
`docs/kei-runtime-socket-parity.md` in the agentware repo. All three ports replay the shared fixtures in
`testing/contracts/runtime-socket`.

| | Python | TypeScript (`@haikeilabs/agentware`) | Go (`kei/runtimesocket`, `kei/toolsync`) |
| --- | --- | --- | --- |
| Client | `KeiProxySocketAuthorizeClient(socket_path=, timeout=, model_timeout=, env=)` | `new KeiProxySocketAuthorizeClient({ socketPath, timeoutMs, modelTimeoutMs, env })` | `&runtimesocket.Client{SocketPath, Timeout, ModelTimeout, Env}` |
| Identity / session | `KeiProxySocketIdentity(source, external_id)`, `KeiProxySocketSession` | `{ source, externalId }`, `KeiProxySocketSession` | `runtimesocket.Identity{Source, ExternalID}`, `runtimesocket.Session` |
| `PUT` / `DELETE /v1/session` | `await open_session(identity)` / `await close_session(session)` | `await openSession(identity)` / `await closeSession(session)` | `OpenSession(ctx, identity)` / `CloseSession(ctx, session)` |
| Drop cached session | `forget_session(identity)` | `forgetSession(identity)` | `ForgetSession(identity)` |
| `POST /v1/authorize` | `await authorize(session, tool=, action=, ...)` | `await authorize(session, { tool, action, ... })` | `Authorize(ctx, session, evaluator.AuthorizeRequest{...})` |
| `GET /v1/model-config`, `/v1/model-profiles` | `await model_config(agent_id, profile_id)`, `await list_model_profiles(agent_id)` (credential stripped) | `await modelConfig(...)`, `await listModelProfiles(...)` | `ModelConfig(ctx, agentID, profileID)`, `ListModelProfiles(ctx, agentID)` |
| `GET /v1/models` | `await list_models(agent_id, profile_id)` | `await listModels(agentId, profileId)` | `ListModels(ctx, selectors...)` |
| `POST /v1/chat/completions` (**not served by `kei-proxy serve`**; see `kei-model-profiles`) | `chat_completion`, `stream_chat_completion` | `chatCompletion`, `streamChatCompletion` | `ChatCompletion`, `StreamChatCompletion` |
| `GET /v1/policy-bundle/status` | `await policy_bundle_status()` | `await policyBundleStatus()` | `PolicyBundleStatus(ctx)` |
| Refusal error | `KeiProxySocketError` (`reason_class`, `code`) ⊂ `KeiProxyAuthorizeError` | `KeiProxySocketError` (`reasonClass`, `code`) ⊂ `KeiProxyAuthorizeError` | `*runtimesocket.Error` (`Class`, `Code`), unwraps to `*evaluator.AuthorizeError` |
| Evaluator adapter | `KeiProxySocketAuthorizationClient(source, client)` | `new KeiProxySocketAuthorizationClient(source, client)` | `&runtimesocket.AuthorizationClient{Source, Socket}` |
| Socket or CLI selector | `select_authorization_client(source, socket_path=, env=, ...)` | `selectAuthorizationClient(source, { socketPath, env, ... })` | `runtimesocket.SelectAuthorizationClient(source, runtimesocket.SelectOptions{...})` |
| CLI fallback | `KeiProxyAuthorizeClient` | `KeiProxyAuthorizeClient` | `evaluator.CLIClient` |
| Tool sync | `sync_tool_manifest(manifest, ToolManifestSyncConfig.from_env(), expect_tools=)` | `await syncToolManifest(manifest, ToolManifestSyncConfig.fromEnv(), { expectTools })` | `toolsync.Sync(ctx, manifest, cfg, expectTools)` with `toolsync.ConfigFromEnv(env)` |
| Tool sync error | `ToolManifestSyncError` | `ToolManifestSyncError` | wraps `toolsync.ErrSyncFailed` (+ `ErrEmptyManifest`, `ErrInvalidManifest`, `ErrInvalidConfig`) |
| Register `ToolSpec` over socket | `await register_tool_specs(client, specs)` | `registerToolSpecs(specs, client)` | `toolsync.SocketRegistrar{Client: socket}.Send(ctx, specs)` |

**Python import.** The SDK is published as `haikeilabs-agentware`
(`pip install haikeilabs-agentware`) and imported as
`haikeilabs.agentware`, so the socket client is
`from haikeilabs.agentware.kei import ...`. The old `pedro_agentware.kei`
import still works as a deprecated shim.

### Startup order

1. **Register the tool manifest before serving.** Build declarations with
   `ToolSpec` and register them through the daemon socket at
   `POST /v1/tools:register` (`register_tool_specs`, `registerToolSpecs`, or
   `toolsync.SocketRegistrar`). The SDK sync helper (`sync_tool_manifest`,
   or `sync_manifest_path` for a v3 file) does the same with
   `PUT /api/v1/runtime/tools` and the runtime token. It refuses an empty
   manifest when tools are expected. `kei harness sync --manifest` is **not**
   a path for this v3 manifest (see the next section). If registration or sync fails, the harness must not serve.
2. **Pick the client once with the selector.** It returns the socket client
   when a socket path is **configured explicitly** (the argument, or
   `KEI_RUNTIME_SOCKET_PATH`), otherwise the `kei-proxy authorize` subprocess
   client. Socket path order: the explicit path, then
   `KEI_RUNTIME_SOCKET_PATH`, then `/run/kei-proxy/runtime.sock`.
3. **Wrap it in `KeiProxyEvaluator`.** The evaluator is unchanged; the socket
   adapter opens (or reuses) the session for the caller's user and authorizes
   in it.

### Fail-closed rules for the socket

- **A configured socket that is down is a refusal, never a silent fall back**
  to the CLI. The selector chooses once; it never retries the other client.
- Every failure raises the socket error, which `KeiProxyEvaluator` turns into
  a DENY: unreachable daemon `proxy_unavailable`, timeout `proxy_timeout`,
  non-2xx `proxy_error` (carrying the daemon's `code`), a body that is not a
  JSON object or has the wrong schema `malformed_response`, no
  `KEI_RUNTIME_TOKEN` `missing_token`. Only an explicit `permit`/`allow` is
  an allow; a deny is returned, not raised.
- **Sessions.** `kei.session/v2`, one cached per `(source, external_id)`.
  Requests carry `X-Kei-Session` and never name the user. A
  `session_not_found` reopens the session once; a second miss fails closed.
- **The runtime token is never logged.** `KEI_RUNTIME_TOKEN` is read per
  request and sent only as `Authorization: Bearer`. It never appears in a log
  line, an error, a repr, `JSON.stringify`/`util.inspect`, or `String()`.
  Errors carry the daemon's error code, never its message or a body.
- Ambient `HTTP(S)_PROXY` never reroutes socket requests. Tool sync goes
  through `KEI_PROXY_EGRESS_PROXY` (unless `KEI_PROXY_NO_PROXY` bypasses the
  host), else `HTTPS_PROXY` / `NO_PROXY`.
- Go is Unix only: on Windows every socket call refuses `proxy_unavailable`
  wrapping `runtimesocket.ErrUnsupportedPlatform`.

### Python

```python
from haikeilabs.agentware.kei import (   # pedro_agentware.kei still works (deprecated shim)
    KeiProxyEvaluator, ToolManifestSyncConfig, select_authorization_client, sync_tool_manifest,
)

sync_tool_manifest(registry.export_kei_tool_manifest(), ToolManifestSyncConfig.from_env(),
                   expect_tools=True)                     # raises ToolManifestSyncError: do not serve
client = select_authorization_client("discord")           # socket iff KEI_RUNTIME_SOCKET_PATH is set
evaluator = KeiProxyEvaluator(client)                     # sync evaluate(); the adapter runs the async client
decision = evaluator.evaluate("github.get_issue", {"owner": "acme"}, caller)
```

Direct use of the async client (sessions, authorize, model config, bundle status):

```python
from haikeilabs.agentware.kei import KeiProxySocketAuthorizeClient, KeiProxySocketIdentity

sock = KeiProxySocketAuthorizeClient(socket_path="/run/kei-proxy/runtime.sock")
session = await sock.open_session(KeiProxySocketIdentity("discord", "user-123"))
answer = await sock.authorize(session, tool="github.get_issue", action="read")
status = await sock.policy_bundle_status()               # kei.policy-bundle-status/v1
cfg = await sock.model_config()                         # {"model", "endpoint", ...}; credential stripped
await sock.close_session(session)
```

The real model path is `GET /v1/model-config` on the socket (`model_config()`),
and then **the harness calls the model itself** at `cfg["endpoint"]`.
`chat_completion` / `stream_chat_completion` exist in the client, but they
POST `/v1/chat/completions`, and `kei-proxy serve` has no such route today
(it was removed in HAI-671). Against a real daemon they fail with
`proxy_error`. See `kei-model-profiles`.

### TypeScript

```typescript
import {
  KeiProxyEvaluator, ToolManifestSyncConfig, selectAuthorizationClient, syncToolManifest,
} from "@haikeilabs/agentware";

await syncToolManifest(registry.exportKeiToolManifest(), ToolManifestSyncConfig.fromEnv(),
  { expectTools: true });                                 // throws ToolManifestSyncError: do not serve
const client = selectAuthorizationClient("discord");     // socket iff KEI_RUNTIME_SOCKET_PATH (or socketPath) is set
const evaluator = new KeiProxyEvaluator(client);
const decision = await evaluator.evaluate("github.get_issue", args, caller);
```

`openSession`, `authorize`, `modelConfig`, `listModels` and
`policyBundleStatus` are on `KeiProxySocketAuthorizeClient`. It also has
`chatCompletion` / `streamChatCompletion`, but the daemon has no
`POST /v1/chat/completions` route today. Use `modelConfig()` and call the
model yourself. These socket
client APIs and tool registration are available from Agentware 0.11.0.

### Go

```go
import (
    "github.com/haikeilabs/agentware/go/kei/evaluator"
    "github.com/haikeilabs/agentware/go/kei/runtimesocket"
    "github.com/haikeilabs/agentware/go/kei/toolsync"
)

cfg, err := toolsync.ConfigFromEnv(nil)                   // nil = process environment
if err != nil { return err }
if _, err := toolsync.Sync(ctx, manifestJSON, cfg, true); err != nil {
    return err                                            // errors.Is(err, toolsync.ErrEmptyManifest) etc.; do not serve
}
client, err := runtimesocket.SelectAuthorizationClient("discord", runtimesocket.SelectOptions{})
if err != nil { return err }                              // socket iff KEI_RUNTIME_SOCKET_PATH or SocketPath is set
e := evaluator.NewKeiProxyEvaluator(client)
decision := e.Evaluate("github.get_issue", args, caller)
```

Direct calls take a session: `s, err := sock.OpenSession(ctx,
runtimesocket.Identity{Source: "discord", ExternalID: "user-123"})`, then
`sock.Authorize(ctx, s, evaluator.AuthorizeRequest{Tool: ..., Action: ...})`,
`ModelConfig`, `ListModels` and `PolicyBundleStatus`. `ChatCompletion` and
`StreamChatCompletion` are also on the client, but `kei-proxy serve` has no
chat route today. Use `ModelConfig` and call the model yourself. A cancelled caller
context is a refusal that wraps `ctx.Err()`.

### Deprecated CLI fallback

Without `KEI_RUNTIME_SOCKET_PATH` (or an explicit socket path) the selectors
return the subprocess client: one `kei-proxy authorize` per call. The SDK
documents this client as deprecated; use the socket for new integrations.
A configured socket that is unavailable fails closed and never switches to
the subprocess. The rest of this section documents the legacy client.

## KeiProxyEvaluator per language

\`KeiProxyEvaluator\` is a \`PolicyEvaluator\` that asks kei-proxy before
every tool call and enforces fail-closed behavior: anything that is not an
explicit \`allow\`/\`permit\` is denied. It lives in all three agentware SDK
ports and is the one enforcement seam a harness or adapter needs. It takes
either client: the socket adapter from the selector (primary, above) or the
\`kei-proxy authorize\` subprocess client (fallback). The decision table below
is the subprocess client's; the socket client's failures map to the same
reason classes.

### Decision table

The shared parity table (\`fixtures/kei/authorize-cases.v1.json\`) is authoritative for every
port. Every reason reads \`kei-proxy <class>\` or \`kei-proxy <class>: <detail>\`.
\`rule\` is the output's \`policy_id\` (or \`policy\`) when present, else \`kei-proxy\`.

| Proxy result | Action | Reason class | Enrollment | Connect |
|---|---|---|---|---|---|
| \`allow\` / \`permit\` (any case), exit 0 | ALLOW | \`allow\` | — | — |
| \`deny\` | DENY | \`deny\` | carried when JSON | carried when JSON |
| \`deny\` + \`enrollment_required\` (legacy) | DENY | \`enrollment_required\` | carried when JSON | carried when JSON |
| \`decision\` missing, null or \`""\` | DENY | \`no_decision\` | — | — |
| any other decision, or a non-string one | DENY | \`unknown_decision\` | — | — |
| \`allow\` with exit 1 | DENY | \`exit_mismatch\` | — | — |
| exit code other than 0 or 1 | DENY | \`proxy_error\` | — | — |
| exit 1 with empty stdout | DENY | \`proxy_error\` | — | — |
| exit 0 with empty stdout | DENY | \`empty_response\` | — | — |
| stdout not JSON, or JSON but not an object | DENY | \`malformed_response\` | — | — |
| binary missing or not executable | DENY | \`proxy_unavailable\` | — | — |
| binary executable does not match sha256 pin | DENY | \`pin_mismatch\` | — | — |
| no answer within the timeout | DENY | \`proxy_timeout\` | — | — |
| no \`KEI_RUNTIME_TOKEN\` (proxy not spawned) | DENY | \`missing_token\` | — | — |

**fail-closed.** Only an explicit affirmative with exit 0 allows. Everything
else — every exit code, every parse failure, every missing binary, every
timeout — produces a DENY.

**No leaks.** The enrollment claim URL, the connect reconnect URL, the
allow-path credential, stderr, and the runtime token never appear in a
Decision reason or in a log line. Stdout and stderr are never logged.

**Token by env only.** \`KEI_RUNTIME_TOKEN\` reaches the child through its
environment and never through argv. The child sees only the allowlisted
parent variables (\`AUTHORIZE_CHILD_ENV_ALLOWLIST\`) plus explicit extra env.
KEI_PROXY_* identity variables are deliberately excluded — identity travels
as flags. Secrets such as \`DISCORD_TOKEN\` and inherited \`KEI_PROXY_*\`
variables are stripped.

**Identity by flags.** \`--user\` is the invoking subject (the human). The
delegation chain (\`--parent-span\`, \`--delegation-depth\`), agent version,
framework, \`--tool-args-digest\` (SHA-256 of the sorted-key, compact JSON of
the args) and \`--resources\` are passed as flags.

**No \`--agent-id\`.** kei-proxy (0.1.11+) resolves the agent from the runtime
installation, so no client sends \`--agent-id\` even when the caller carries an
agent id.

### When to use KeiProxyEvaluator vs raw kei-proxy

Use the evaluator when your harness uses agentware's \`AuditedToolClient\`,
\`MiddlewareImpl\`, or the \`PolicyEvaluator\` interface, with the client
from the selector. It handles the session or the spawn, timeout, env
filtering, decision parsing, enrollment extraction, and all fail-closed
invariants for you.

Call \`kei-proxy authorize\` directly only when you cannot import the SDK
and no daemon runs (e.g. a bash script in a one-shot job). In that case
replicate the invariants above manually — every mistake is a security hole.

### Python: the subprocess (CLI fallback) client

\`\`\`python
from haikeilabs.agentware.kei import KeiProxyAuthorizeClient, KeiProxyEvaluator

# Construction
client = KeiProxyAuthorizeClient(
    executable="kei-proxy",          # absolute path preferred; resolved from PATH
    timeout=10.0,                    # seconds; default 10.0
    extra_env={},                    # optional extra env vars for the child
    expected_sha256="abcd...",       # optional binary pin (mismatch → deny)
)
evaluator = KeiProxyEvaluator(client)

# Usage — synchronous
decision = evaluator.evaluate("github.get_issue", {"owner": "acme"}, caller)

# Decision inspection
if decision.action == "ALLOW":
    ...  # proceed
elif decision.connect:
    # Show reconnect link privately, never log it
    harness.send_dm(caller.user_id, decision.connect["url"])
elif decision.enrollment:
    # Show claim link privately, never log it
    harness.send_dm(caller.user_id, decision.enrollment["url"])
else:
    ...  # deny; decision.reason has the class and detail
\`\`\`

The child process receives only \`KEI_*\` environment variables (plus
\`extra_env\`). On timeout the process group is killed.

Exported symbols (kei module): `KeiProxyEvaluator`, `KeiProxyAuthorizeClient`,
`AFFIRMATIVE_DECISIONS`, `REASON_CLASSES`, `KeiProxyAuthorizeError`,
`AuthorizationClient`, `AuthorizationResponse`,
`resources_touched`, `tool_args_digest`,
`AUTHORIZE_CHILD_ENV_ALLOWLIST`, `DEFAULT_AUTHORIZE_TIMEOUT`,
`parse_authorize_output`.

Exported symbols (tools module): `ToolRegistry`, `KeiScope`, `GovernedTool`,
`Result`, `ToolRegistry.export_kei_tool_manifest()`.

### Go: the subprocess (CLI fallback) client

\`\`\`go
import "github.com/haikeilabs/agentware/go/kei/evaluator"

// CLIClient wraps exec.CommandContext
client := &evaluator.CLIClient{
    Executable: "kei-proxy",         // absolute path preferred
    Timeout:    10 * time.Second,
    ExpectedSHA256: "abcd...",       // optional binary pin ("" = no check)
}

e := evaluator.NewKeiProxyEvaluator(client)
// Optional: evaluator.WithDefaultAction("execute"),
//            evaluator.WithLogger(slog.Default())

decision := e.Evaluate("github.get_issue", args, caller)
// decision.Action     == middleware.ActionAllow / ActionDeny
// decision.Reason     string — "kei-proxy allow" or "kei-proxy deny: ..."
// decision.Rule       string — policy_id or "kei-proxy"
// decision.Enrollment map[string]any — nil on allow
// decision.Connect    map[string]any — nil on allow
\`\`\`

The child process receives only \`KEI_*\` environment variables (filtered
through \`AuthorizeChildEnvAllowlist\`). On timeout the process group is killed.
The binary path is resolved to absolute before spawn.

Exported symbols (kei/evaluator): `KeiProxyEvaluator`, `NewKeiProxyEvaluator`,
`WithDefaultAction`, `WithLogger`, `Client`, `CLIClient`,
`AuthorizeRequest`, `AuthorizeError`, `ReasonClass` and all `Reason*`
constants, `ReasonClasses`, `Rule`, `IsAffirmative`,
`AuthorizeChildEnvAllowlist`, `DefaultTimeout`, `RuntimeTokenEnv`,
`ResourcesTouched`, `ToolArgsDigest`, `middleware.Decision.Connect`.

Exported symbols (tools): `tools.KeiScope`, `tools.GovernedTool`,
`tools.NewToolRegistry`, `tools.ToolRegistry.Register`,
`tools.ToolRegistry.ExportKeiToolManifest`, `tools.ToolRegistry.Get`,
`tools.Result`.

### TypeScript: the subprocess (CLI fallback) client (agentware >= 0.11.0, async only)

Starting in `@haikeilabs/agentware` v0.11.0, `KeiProxyAuthorizeClient` is
**async only** (spawn, not spawnSync) and \`KeiProxyEvaluator.evaluate\`
returns \`Promise<Decision>\`. There is no synchronous \`evaluate()\` —
harnesses must \`await\` the call before running the tool. This async evaluator
cannot be used directly as the sync \`MiddlewareImpl.withPolicy\` middleware;
call \`evaluate()\` directly and await it.

The binary is resolved to an absolute path, pinned by optional SHA-256 digest
(mismatch produces \`pin_mismatch\` reason and a DENY), and opened with
\`O_NOFOLLOW\`. Only \`KEI_*\` environment variables reach the child process.
On timeout the process group is killed.

\`\`\`typescript
import {
  KeiProxyAuthorizeClient,
  KeiProxyEvaluator,
} from "@haikeilabs/agentware";

const client = new KeiProxyAuthorizeClient({
  executable: "kei-proxy",   // absolute path preferred; resolved from PATH
  timeoutMs: 10_000,
  expectedSha256?: string;   // optional binary pin
  extraEnv?: Record<string, string>;
});

const evaluator = new KeiProxyEvaluator(client);
const decision: Decision = await evaluator.evaluate(tool, args, caller);

if (decision.action === Action.ALLOW) {
  // proceed
} else if (decision.connect) {
  await harness.sendEphemeral(caller.userId, decision.connect.url as string);
} else if (decision.enrollment) {
  await harness.sendEphemeral(caller.userId, decision.enrollment.url as string);
}
\`\`\`

Exported symbols (kei): `KeiProxyEvaluator`, `KeiProxyAuthorizeClient`,
`KeiProxyAuthorizeRequest`, `KeiProxyAuthorizeError`,
`KeiProxyAuthorizationClient`, `KEI_PROXY_AFFIRMATIVE_DECISIONS`,
`AUTHORIZE_CHILD_ENV_ALLOWLIST`, `DEFAULT_AUTHORIZE_TIMEOUT_MS`,
`keiProxyAuthorizeArgv`, `parseKeiProxyAuthorizeOutput`.

Exported symbols (tools): `KeiScope`, `GovernedTool`, `ToolRegistry`,
`Result`, `ToolRegistry.exportKeiToolManifest()`.

## Making protected tool calls

Agentware provides **KeiScope** and **GovernedTool** — a standard
way to declare which Kei service, action, and resource patterns a tool touches,
plus an **ExportKeiToolManifest** function that produces a JSON manifest an
admin loads into the Kei policy catalog's tool registry (`POST /api/v1/tools`).

The flow is:

```
1. Declare  →  tool implements GovernedTool with a KeiScope
2. Register →  add GovernedTool tools (and any plain tools) to a ToolRegistry
3. Export   →  registry.ExportKeiToolManifest() produces deterministic JSON
4. Load     →  admin imports the JSON into the catalog (kei CLI or skill)
5. Call     →  harness calls authorize by tool name only; catalog resolves resources
6. Handle   →  allow / deny / enrollment_required / connect
```

The harness **never passes an authorize resource** (`--resource` /
`authorize_resource`). The catalog is authoritative for resource patterns from
the registered scope.

### 1. Declare a protected tool

Each language defines `KeiScope` and `GovernedTool` so existing tools compile
unchanged — only tools that explicitly declare a scope appear in the manifest.

#### Go

```go
import "github.com/haikeilabs/agentware/go/tools"

type getIssueTool struct{}

func (t *getIssueTool) Name() string        { return "github.get_issue" }
func (t *getIssueTool) Description() string { return "Fetch an issue from a GitHub repository" }
func (t *getIssueTool) Execute(ctx context.Context, args map[string]any) (*tools.Result, error) {
    // execution logic
    return &tools.Result{Success: true, Data: issue}, nil
}
func (t *getIssueTool) KeiScope() tools.KeiScope {
    return tools.KeiScope{
        Service:   "github",
        Action:    "read",
        Resources: []string{"repo:haikeilabs/*", "issue:*"},
    }
}
```

#### Python

```python
from haikeilabs.agentware.tools import KeiScope, GovernedTool, Result

class GetIssueTool:
    @property
    def name(self) -> str:
        return "github.get_issue"

    @property
    def description(self) -> str:
        return "Fetch an issue from a GitHub repository"

    def execute(self, args: dict) -> Result:
        # execution logic
        return Result(success=True, data=issue)

    def kei_scope(self) -> KeiScope:
        return KeiScope(
            service="github",
            action="read",
            resources=["repo:haikeilabs/*", "issue:*"],
        )
```

#### TypeScript

```typescript
import type { GovernedTool, KeiScope } from "@haikeilabs/agentware";
import { Result } from "@haikeilabs/agentware";

const getIssueTool: GovernedTool = {
  name: "github.get_issue",
  description: "Fetch an issue from a GitHub repository",
  execute(args: Record<string, unknown>): Result {
    // execution logic
    return new Result(true, issue);
  },
  keiScope(): KeiScope {
    return {
      service: "github",
      action: "read",
      resources: ["repo:haikeilabs/*", "issue:*"],
    };
  },
};
```

### 2. Register and call through KeiProxyEvaluator

Register tools on a `ToolRegistry`. The evaluator authorizes by **tool name
only** — never pass a resource.

#### Python

```python
from haikeilabs.agentware.tools import ToolRegistry
from haikeilabs.agentware.kei import KeiProxyEvaluator, select_authorization_client

# Register governed (and plain) tools
registry = ToolRegistry()
registry.register(get_issue_tool)

# Socket client when KEI_RUNTIME_SOCKET_PATH is set (kei-proxy serve), else the deprecated CLI fallback
evaluator = KeiProxyEvaluator(select_authorization_client("discord"))

# Authorize by tool name only — never pass resources
decision = evaluator.evaluate("github.get_issue", {"owner": "acme"}, caller)

if decision.action == "ALLOW":
    result = get_issue_tool.execute({"owner": "acme"})
elif decision.connect:
    # OAuth reconnect required — deliver link privately, never log
    harness.send_dm(caller.user_id, decision.connect["url"])
elif decision.enrollment:
    # User must link their identity first
    harness.send_dm(caller.user_id, decision.enrollment["url"])
else:
    logger.info("Denied: %s", decision.reason)
```

#### Go

```go
import (
    "github.com/haikeilabs/agentware/go/kei/evaluator"
    "github.com/haikeilabs/agentware/go/kei/runtimesocket"
    "github.com/haikeilabs/agentware/go/tools"
    "github.com/haikeilabs/agentware/go/middleware"
)

registry := tools.NewToolRegistry()
registry.Register(&getIssueTool{})

// Socket client when KEI_RUNTIME_SOCKET_PATH is set (kei-proxy serve), else deprecated evaluator.CLIClient
client, err := runtimesocket.SelectAuthorizationClient("discord", runtimesocket.SelectOptions{})
if err != nil {
    return err
}
e := evaluator.NewKeiProxyEvaluator(client)

decision := e.Evaluate("github.get_issue", args, caller)

switch {
case decision.Action == middleware.ActionAllow:
    result, _ := registry.Get("github.get_issue")
    // execute...
case decision.Connect != nil:
    // OAuth reconnect — deliver url privately, never log
    harness.SendDM(caller.UserID, decision.Connect["url"].(string))
case decision.Enrollment != nil:
    // Identity linking — deliver url privately, never log
    harness.SendDM(caller.UserID, decision.Enrollment["url"].(string))
default:
    slog.Info("denied", "reason", decision.Reason)
}
```

#### TypeScript

```typescript
import {
  ToolRegistry,
  KeiProxyEvaluator,
  selectAuthorizationClient,
  Action,
} from "@haikeilabs/agentware";

const registry = new ToolRegistry();
registry.register(getIssueTool);

// Socket client when KEI_RUNTIME_SOCKET_PATH is set (kei-proxy serve), else the deprecated CLI fallback
const evaluator = new KeiProxyEvaluator(selectAuthorizationClient("discord"));

const decision = await evaluator.evaluate("github.get_issue", args, caller);

if (decision.action === Action.ALLOW) {
  const tool = registry.get("github.get_issue");
  // execute...
} else if (decision.connect) {
  await harness.sendEphemeral(caller.userId, decision.connect.url as string);
} else if (decision.enrollment) {
  await harness.sendEphemeral(caller.userId, decision.enrollment.url as string);
} else {
  console.log("Denied:", decision.reason);
}
```

### 3. Export the tool manifest

Export protected tools to a JSON manifest that an admin loads into the Kei
policy catalog. Only tools implementing `GovernedTool` appear in the output.
The manifest is deterministic (sorted by tool name).

#### Python

```python
manifest_json = registry.export_kei_tool_manifest()
# Write to file for the admin
with open("tool-manifest.json", "w") as f:
    f.write(manifest_json)
```

#### Go

```go
manifestJSON, err := registry.ExportKeiToolManifest()
if err != nil {
    // handle error
}
os.WriteFile("tool-manifest.json", manifestJSON, 0644)
```

#### TypeScript

```typescript
const manifest = registry.exportKeiToolManifest();
const manifestJSON = JSON.stringify(manifest, null, 2);
// Write to file or pass to admin
```

#### Output shape

```json
{
  "schema": "kei.tool-manifest/v3",
  "tools": [
    {
      "name": "github.get_issue",
      "service": "github",
      "source": "github",
      "operation_class": "read",
      "route": {"connector_binding": {"agent_id": "<agent uuid>", "connector_id": "<connector uuid>"}},
      "required_capabilities": ["issue.read"],
      "description": "Fetch an issue from a GitHub repository",
      "enabled": true
    }
  ]
}
```

v3 is the only format the exporter writes (`export_kei_tool_manifest(version=3)`).
A tool the harness runs itself uses
`"route": {"harness_executor": {"executor": "...", "registration": "..."}}`
and omits `required_capabilities`.

Server-generated fields (`id`, `workspace_id`, `org_id`, `version`,
`created_at`, `updated_at`) are omitted. The exported manifest is **v3**
(`"schema": "kei.tool-manifest/v3"`), the only format the Agentware exporter
writes. kei-proxy rejects v1 and v2. When you explain loading it, say it is v3.

**The harness registers it, and the operator doesn't load it.** `kei` has no
`tools import` command. Register the v3 manifest from the harness before
serving:

- over the socket: `register_tool_specs(client, specs)` → `POST /v1/tools:register`
- or with the SDK sync: `sync_tool_manifest(manifest, ToolManifestSyncConfig.from_env())`,
  or `sync_manifest_path(path, config)` for a file → `PUT /api/v1/runtime/tools`
  (sent as `application/vnd.kei.tool-manifest.v3+json`)

**`kei harness sync --harness custom --manifest FILE` rejects this
manifest.** kei 0.3.9 fails with `'tools' must be a JSON array: json: cannot
unmarshal object into Go struct field .0.route of type string`. kei-cli reads
`route` as a string and re-sends the tools as `kei.tool-manifest/v2`, while a
v3 route is an object (kei-cli `internal/app/harness.go:461-463, 548, 594`).
Don't give it as the way to load an Agentware export.

After loading, the catalog is authoritative for resource patterns per tool
name. The harness sends only the tool name (`--tool`) on authorize.

### Runtime boundary

- **Agentware does not call an admin `/api/v1/tools` endpoint.** It can
  register tools over the local socket (`POST /v1/tools:register`), or use
  the SDK startup sync (`sync_tool_manifest` / `syncToolManifest` /
  `toolsync.Sync`, a `PUT` to `/api/v1/runtime/tools` with the runtime token).
  Registration runs before the harness serves and refuses an empty manifest.
- **Harnesses never pass an authorize resource.** The `authorize` call sends
  the tool name only; the catalog resolves resources from the declared scope.
- **Local tools are excluded.** Tools that do not implement
  `GovernedTool` / `kei_scope()` / `keiScope()` are silently omitted from the
  manifest. They continue to work locally but are not registered in the catalog.
- **Deterministic output.** Entries are sorted by tool name so the manifest can
  be committed and diffed.
- **Opt-in.** Existing tools compile unchanged. Only tools that explicitly
  declare a `KeiScope` appear in the manifest.

See the shared fixture at `fixtures/kei/tool-manifest.v3.json` for a complete
example with a harness-executed tool and a connector tool.

### Testing with the shared fixture table

All three ports test against \`fixtures/kei/authorize-cases.v1.json\`. Each
case supplies a fake \`kei-proxy\` stdout, stderr, exit code, and expected
decision. The fake binary (\`fixtures/kei/fake-kei-proxy.sh\`) prints the
canned answer and records its argv and env.

| Language | Evaluator | Subprocess client | Table test |
|---|---|---|
| Python | \`haikeilabs.agentware.kei.KeiProxyEvaluator\` | \`KeiProxyAuthorizeClient\` | \`python/tests/kei/authorize_cases_test.py\` |
| TypeScript | \`KeiProxyEvaluator\` (\`typescript/src/kei/evaluator.ts\`) | \`KeiProxyAuthorizeClient\` (\`authorizeClient.ts\`) | \`typescript/tests/kei-evaluator.test.ts\` |
| Go | \`evaluator.KeiProxyEvaluator\` (\`go/kei/evaluator\`) | \`evaluator.CLIClient\` (\`exec.CommandContext\`) | \`go/kei/evaluator/evaluator_test.go\` |

Python-only tests (the injected-client seam: legacy four-argument clients,
object-shaped results, arbitrary exceptions) stay in
\`python/tests/kei/evaluator_test.py\`.

The fixture-integrity checks (every derived case agrees with the seeded policy
rule it names) run once, in Python.

### Checked SDK baseline

These socket and sync surfaces exist from Agentware 0.11.0. This is a checked
baseline, not a claim that every feature or Kei deployment works with 0.11.0
or later. For current releases use the compatibility minimums above.

| Language | Package | Checked current SDK version |
|---|---|---|
| Python | \`haikeilabs-agentware\` (import \`haikeilabs.agentware\`) | \`0.16.0\` |
| TypeScript | \`@haikeilabs/agentware\` | \`0.16.0\` |
| Go | \`github.com/haikeilabs/agentware/go\` (\`kei/runtimesocket\`, \`kei/toolsync\`) | \`v0.16.0\` |

The Go module is published through the Go module proxy; no separate registry
login is needed.

## The control-plane and action-tool boundary

Authoritative sources: `docs/tenant-proxy-reference.md` and
`docs/action-tool-boundary.md`. Execution happens tenant-side. Kei is a
**metadata-only control plane**; ABAC is a **policy decision point only**.

- `tool_bindings` (tool → connector routing) and `secret_refs` (opaque reference
  identifiers) are **non-secret metadata**. They never grant permissions and are never
  resolved to credentials by the library.
- The **proxy is the enforcement boundary** for external operations Kei allows or denies: it
  resolves bindings and auth, invokes provider adapters, and returns data only inside
  the tenant runtime.
- **Never in Kei**: provider payloads and results, customer content, credentials,
  embeddings, and indexes.
- A custom evaluator can implement `PolicyEvaluator`; enforcement depends on the
  evaluator wired into `AuditedToolClient` or `Middleware`.
- `invoking_subject` is the human and is carried unchanged across every delegation hop.

## LangGraph and memory

- LangGraph integration is `python/src/haikeilabs/agentware/memory/langgraph.py`
  (`LangGraphMemoryTools`: `memory_ingest`, `memory_write_page`, `memory_query`,
  `memory_get_claims`, `memory_lint`) plus the `middleware/inference.py` loop — there is
  no `middleware/langgraph.py` and no `LangGraphToolWrapper`.
- Wiki memory: Go `go/memory` (ontology-constrained: vault, page parser, ontology validation,
  query, lint; `cmd/memctl` CLI) backed by the `ontologies/` git submodule.

## Validation commands

Run in a checkout of the agentware repo:

```bash
# Python
make python-lint python-typecheck python-test      # ruff check . ; mypy . ; pytest

# Go
make go-build go-test go-lint go-vet              # go build ./... ; go test ./... ; golangci-lint run

# TypeScript
cd typescript && npm run build && npm test        # tsc + jest

# KEI contract suite
cd python && pytest tests/kei/ -v

# Action-tool boundary contract tests
cd python && pytest tests/action_tool_boundary_test.py -v
cd go && go test ./middleware/... -run ActionToolBoundary -v
```

## Realistic usage boundaries

- **Do not** invent an agentware API that is not in the code. The README and
  `docs/{python,go,typescript}/README.md` drift from the source (`middleware_py`,
  `LangGraphToolWrapper` no longer exist); the tests, `docs/kei-tool-manifest.md`,
  and `python/src/evals` are the ground truth.
- **Do not** run an agent loop inside the middleware. Middleware decides and audits tool
  calls; the harness (`middleware/inference.py`, `evals`, adapters) owns the loop.
- **Do not** grant anything on a manifest. `BINDINGS_GRANT_PERMISSIONS = False` and
  `validate_manifest` is fail-closed on a bootstrap-secret-bearing manifest.
- **Do not** ship tokens through argv, logs, or audit records. `OpaqueTokenProvider` is
  fail-closed on renew; keep it that way.
- **Do not** resolve connector `secret_refs` or execute providers in the library; that is
  the proxy's job, tenant-side.
- **Do not pass authorize resources.** The harness sends only the tool name on
  `authorize`; the catalog resolves resource patterns from the registered scope.
  See `docs/kei-tool-manifest.md` and the protected tool calls section above.
- **Do not expose connect or enrollment URLs outside a private channel.**
  Both are one-time claim links. Deliver them privately to the user and never
  log them, never cache an expired link.
- **Do** expect Go/TypeScript parity with the Python KeiProxyEvaluator. All
  three ports follow the same parity table; a bug report must name which port
  and which fixture case it fails.
- The tool-adapter/governor tool-lane pattern (closed catalogs, branded governor
  proposals, typed registries) lives in `kei-tool-adapters`, not
  in this generic SDK skill.

## Related skills

- `kei-model-profiles` — which model an agent uses, resolved at run time from
  its Kei model profile (`model_config`, `/v1/model-config`).
- `kei-openai-backends` — tool-call and reasoning formats per model family.
- `kei-harness-policy` — `tool:<name>` policies, groups, `kei policy test`.
- `test-agents` — `agentware.eval-suite.v1` suites and the eval gate.
- `build-agents-agentware` — an end-to-end agent recipe on this SDK.
- `kei-agents` — agent definitions and connector read schemas for connectors Kei checks that the harness
  renders; provider-neutral and schema-only.
- `kei-api` — the control-plane API that mints harness keys and decides
  metadata-only policy, including `POST /api/v1/tools` where an admin loads the
  tool manifest exported by `export_kei_tool_manifest()`.
- `kei-proxy` — the runtime that evaluates `authorize` calls and returns
  allow/deny/enrollment/connect decisions.
