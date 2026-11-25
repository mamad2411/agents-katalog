---
name: build-agents-agentware
description: Build a governed AI agent end to end with the open-source kei-agents package and the agentware SDK — compose a prebuilt agent or workflow (Pedro, the PDE search agent, bug_to_linear_pr, github_pr_review, …) from its system prompt and rendered tools, wrap every tool call with AuditedToolClient so it is decided by policy, audited, and attributed to the invoking human, use KeiProxyEvaluator to let Kei decide, and design tool arguments with the Lexicon/Pragmatics/Semantics rule (relationship arguments carry the parent id; proxy-delegated scope is never an argument). Use when someone asks how to build, compose, or wire up an agent with agentware or kei-agents, how to govern or audit an agent's tool calls, what a tool's arguments should be, how a subagent keeps the human's identity, or how an Agentware agent takes its model from the runtime's Kei model profile instead of a hard-coded endpoint, model or API key. For testing the agent load test-agents; for shipping it load deploy-agents.
---

# Build agents with the agentware SDK

An agent you can put in front of a customer has three layers. Keep them
separate; each has one owner:

| Layer | What it is | Package |
| --- | --- | --- |
| **Definition** | System prompt + tool schemas + the permissions the agent may hold | `kei-agents` (`agents` import) |
| **Guardrails** | Every tool call is decided (allow/deny/filter), audited, and attributed to a human | agentware SDK (`haikeilabs.agentware`, Go, TypeScript) |
| **Runtime decision** | The live allow/deny comes from the workspace policy, made tenant-side | `kei-proxy serve`, reached through `KeiProxyEvaluator` and the socket client |

The model never decides what it is allowed to do. A refusal in the prompt is
not a control; the policy check in front of the tool is.

## Install

The agentware SDK is published to PyPI as `haikeilabs-agentware` (import
`haikeilabs.agentware`; the old `pedro_agentware` import still works as a
deprecated shim). `kei-agents` installs from a checkout:

```bash
git clone https://github.com/HaikeiLabs/agentware && git clone https://github.com/HaikeiLabs/kei-agents
python -m venv .venv && . .venv/bin/activate
pip install haikeilabs-agentware -e ./kei-agents         # Python >= 3.10
```

TypeScript: `npm install @haikeilabs/agentware` (>= 0.11.0). Go:
`go get github.com/haikeilabs/agentware/go`.

## 1. Compose a prebuilt agent

`kei-agents` ships agents as data: an `AgentDefinition` names the agent's
permissions, its catalog tools, and a system prompt file inside the package.
Today there are two: `PEDRO_AGENT` (Discord) and `PDE_SEARCH_AGENT` (PDE).

```python
from agents import (
    PEDRO_AGENT, ModelFormat, get_agent_tools, load_system_prompt,
    render_tools, validate_agent_definitions,
)

assert validate_agent_definitions([PEDRO_AGENT]) == []      # well formed, not "permitted"
system_prompt = load_system_prompt(PEDRO_AGENT)              # reads prompts/pedro.md
tools = render_tools(get_agent_tools(PEDRO_AGENT), ModelFormat.OPENAI)
# 29 OpenAI function tools; tools[0]["function"]["name"] == "file_bug"
```

`render_tools` also takes `ModelFormat.ANTHROPIC`, `ModelFormat.OLLAMA`, or a
model name to auto-detect the format. Pass `system_prompt` and `tools` to
whatever model client your harness uses; nothing here calls a model.

**Workflows** (`bug_to_linear_pr`, `drive_publish`, `github_pr_review`,
`support`) ship a prompt under
`prompts/workflows/` and a list of catalog tools. The eval targets are the
easiest place to read both from:

```python
from importlib import resources
from agents import ModelFormat, get_tool_by_name, render_tools
from agents.evals.targets import WORKFLOW_TARGETS

target = next(t for t in WORKFLOW_TARGETS if t.name == "bug_to_linear_pr")
prompt = resources.files("agents").joinpath(target.prompt_file).read_text(encoding="utf-8")
tools = render_tools([get_tool_by_name(n) for n in target.tools], ModelFormat.OPENAI)
# tools: () -- Kei infers the runtime tools at call time
```

To define your own agent, build an `AgentDefinition(name=..., harness=...,
description=..., permissions=frozenset({Permission.LINEAR_WRITE, ...}),
tools=(...), system_prompt="...")` and run `validate_agent_definitions` in a
test. It rejects bare-string permissions, unknown tools, tools whose
permission is not granted, and any `*_approve` permission (reserved; agents
never hold one). `system_prompt_file` must resolve inside the `agents`
package, so an out-of-tree agent uses inline `system_prompt`.

## 2. Wrap every tool call with the SDK

`AuditedToolClient` puts one gate in front of each tool function: evaluate
policy, record an audit entry, then run the tool only when allowed. A denial
raises `PermissionError`; it is still audited.

```python
import asyncio
from haikeilabs.agentware.middleware import (
    AuditedToolClient, CallerContext,
)
from haikeilabs.agentware.kei import KeiProxyEvaluator, select_authorization_client

client = AuditedToolClient(
    source="my-harness",
    evaluator=KeiProxyEvaluator(select_authorization_client("discord")),
)

def file_bug(**args):
    return {"issue": f"{args['team_key']}-123"}

caller = CallerContext(user_id="discord:42", session_id="chan-1",
                       invoking_subject="discord:42", role="member")

async def main():
    await client.Execute("file_bug",
                         {"team_key": "KEI", "title": "Login 500", "description": "…", "severity": "high"},
                         user_id="discord:42", channel_id="chan-1", guild_id=None,
                         func=file_bug, caller=caller)              # allowed
    try:
        await client.Execute("drive.get_file", {"file_id": "f-1"}, user_id="discord:42", channel_id="chan-1",
                             guild_id=None, func=lambda **a: [], caller=caller)
    except PermissionError as exc:                                  # denied, and audited
        print(exc)   # denied by policy: no matching rules and default deny is enabled
    for r in client.records():
        print(r.tool_name, r.decision.action.value, r.invoking_subject)

asyncio.run(main())
```

Python exposes the `PolicyEvaluator` interface; it does not include a local
`Policy`, `Rule`, or `SimplePolicyEvaluator` implementation. Use the proxy
evaluator above or implement the interface for an external policy engine.
When answering a Python policy question, state plainly that Python has no local
policy engine and use `KeiProxyEvaluator` to ask Kei for decisions.

The published Python distribution is `haikeilabs-agentware`, imported as
`haikeilabs.agentware`. The TypeScript package is `@haikeilabs/agentware`.

### Let Kei decide: `KeiProxyEvaluator`

In a deployed harness, use the workspace policy evaluator; the client, the tools, and the audit stay the same:

```python
from haikeilabs.agentware import ToolSpec, register_tool_specs
from haikeilabs.agentware.kei import (   # pedro_agentware.kei still works (deprecated shim)
    KeiProxyEvaluator, ToolManifestSyncConfig, select_authorization_client, sync_tool_manifest,
)

# Before serving: sync the governed tools. An empty manifest is refused,
# and a failed sync raises ToolManifestSyncError: the harness must not serve.
sync_tool_manifest(registry.export_kei_tool_manifest(), ToolManifestSyncConfig.from_env(),
                   expect_tools=True)
# The kei-proxy serve socket client when KEI_RUNTIME_SOCKET_PATH is set,
# otherwise the one-shot `kei-proxy authorize` CLI client.
client.with_policy(KeiProxyEvaluator(select_authorization_client("discord")))
```
Instead of the control-plane sync helper above, choose direct local socket
registration: define the protected declarations as `ToolSpec` values and call
`await register_tool_specs(socket_client, specs)`;
that sends manifest v3 to `POST /v1/tools:register`. In TypeScript use
`registerToolSpecs`, and in Go use `toolsync.SocketRegistrar.Send`. Don't load
this v3 manifest with `kei harness sync --harness custom --manifest tools.json`:
kei-cli reads `route` as a string, so it rejects the v3 export (HAI-1105).

The primary path is the **`kei-proxy serve` daemon plus the socket client**.
Run the daemon beside the harness and set `KEI_RUNTIME_SOCKET_PATH`; the
adapter opens a `kei.session/v2` session for the caller's user and authorizes
in it over the owner-only Unix socket. The `kei-proxy authorize` subprocess
(`KeiProxyAuthorizeClient`) is the **fallback** for one-shot environments with
no daemon (pin it with `expected_sha256=`, absolute path required). Both
**fail closed**: only an explicit `allow`/`permit` allows. An unreachable
daemon or missing binary (`proxy_unavailable`), an unset `KEI_RUNTIME_TOKEN`
(`missing_token`), a timeout, or an unparseable answer is a DENY. **A
configured socket that is down is a refusal, never a silent fall back** to the
CLI. The runtime token is never logged and never put in argv. The harness
sends the tool name and never an authorize resource; the catalog resolves
resources from the tool's registered scope.

On a deny, `decision.enrollment` (an unlinked chat user) or `decision.connect`
(the user's own OAuth connection is missing or expired) may carry a one-time
link. `AuditedToolClient` turns a deny into `PermissionError`, so when you
need those links call `evaluator.evaluate(tool, args, caller)` yourself first
and send the `url` privately to that user. Never log it or post it in a shared
channel. The `agentware-sdk` skill has the full decision table and the Go
(`runtimesocket.SelectAuthorizationClient` + `evaluator.NewKeiProxyEvaluator`,
`toolsync.Sync`) and TypeScript (`selectAuthorizationClient`,
`syncToolManifest`, async-only `await evaluator.evaluate(...)`) spellings.

### Keep the human as the invoking subject

`invoking_subject` is the person who started the task. It is set once at the
human entry point and carried unchanged through every subagent hop:

```python
child = caller.delegate()        # parent_span = caller's span, delegation_depth + 1
assert child.invoking_subject == caller.invoking_subject
```

`delegate()` refuses to override `invoking_subject`. Never replace it with the
agent's own service identity; the audit trail would then say "the bot did it".
Agent identity is discovered from the runtime (`link.identity()`), never from
an env var; if it is unavailable, deny protected calls.

## 3. Design tool arguments: Lexicon, Pragmatics, Semantics

Tool schemas are where most agent bugs start. HaikeiLabs connector skills
describe each provider in three sections, and a tool takes its shape from them:

| Section | Answers | Goes into the tool as |
| --- | --- | --- |
| **Lexicon** | What the provider calls things (commands, endpoints, field names) | Argument **names** |
| **Pragmatics** | When and how an agent should use it | The tool **description** ("Use when… Not for…") |
| **Semantics** | Entities, parent relationships, key fields and their values | **Relationship arguments** and **enum** values |

The Semantics rule:

1. **A child resource's arguments include its parent's identifier.** A Linear
   issue is created in a team, so the tool takes `team_id` (or `team_key`,
   as `file_bug` does). A Drive document is created in a folder, so it takes
   `folder_id`.
2. **Enum values come from the Semantics key-fields table** — `severity`:
   `critical|high|medium|low`, not free text.
3. **Proxy-delegated scope is never an argument.** `tenant_id`, `org_id`,
   `workspace`/`workspace_id`, `repository`, `bucket`, `drive_id`, `mailbox`
   come from the runtime token and the connector binding. An agent that can
   pass them can widen its own scope.

```python
from agents import ModelFormat, Permission, ToolCategory, ToolDefinition, ToolParameter, render_tools

create_task = ToolDefinition(
    name="tracker.create_task",
    description="Create a task in a Linear team. Use when the user asks to track follow-up work. Not for bugs (use file_bug).",
    parameters=[
        ToolParameter(name="team_id", description="ID of the Linear team that owns the task (parent)", required=True),
        ToolParameter(name="title", description="Short task title", required=True),
        ToolParameter(name="priority", description="urgent, high, medium or low", enum=["urgent", "high", "medium", "low"]),
    ],
    permission=Permission.LINEAR_WRITE,
    category=ToolCategory.LINEAR,
)
render_tools([create_task], ModelFormat.OPENAI)   # no tenant_id, workspace or repository anywhere
```

Eval cases then pin it: `"args": {"team_key": "KEI"}` for the parent, and
`"forbidden_arg_keys": ["tenant_id", "workspace", "repository"]` for the
scope (see `test-agents`).

## 4. Register protected tools with Kei

Before Kei can decide a tool by name, an admin loads its scope into the
catalog. In agentware 0.11.0 or later a tool declares a `KeiScope` (service, action,
resource patterns), and `ToolRegistry.export_kei_tool_manifest()` emits
deterministic JSON for the admin to load. The runtime never registers tools
itself. Details: `agentware-sdk`, "Making protected tool calls".

## 5. Take the model from the agent's model profile

The harness shouldn't hard-code a model endpoint, a model name or an API
key. An admin assigns a **model profile** to the agent, and the harness asks
the runtime which model to use. How profiles are chosen and resolved is in
**kei-model-profiles**. The SDK APIs used here are in **agentware-sdk**. This
section is only the recipe that joins them.

**Say both halves in every answer about this recipe.** The model comes from
the profile, and **each tool call is still decided by `KeiProxyEvaluator`**
through `AuditedToolClient` (section 2). The profile changes which model
runs. It never changes the policy.

**The flow:**

1. The admin assigns the profile, on the console's Agents page (**Model
   profile**) or with `kei model-profiles assign PROFILE --workspace WS
   --agent AGENT_ID`.
2. `kei-proxy serve` resolves the agent's current profile on each lookup. It
   has no cache.
3. The harness reads `model` and `endpoint` with the socket client's
   `model_config()` and builds its backend from them.
4. **The harness calls the model itself**: the loop sends its chat requests
   to the backend, which POSTs to the profile's endpoint. kei-proxy has no
   `POST /v1/chat/completions` route today, so chat never goes through the
   socket. Tool calls and reasoning are parsed from the response.
5. Each tool call goes through `AuditedToolClient` with `KeiProxyEvaluator`
   (section 2).

The harness config holds only the runtime settings: `KEI_RUNTIME_SOCKET_PATH`
and `KEI_RUNTIME_TOKEN` (the token comes from the secret manager and is read
by the socket client). It holds **no model URL, model name or API key**. A
provider credential stays with kei-proxy. The socket client strips
`credential`, `api_key` and `secret_ref` from what it returns.

```python
from haikeilabs.agentware.kei import KeiProxySocketAuthorizeClient
from haikeilabs.agentware.llm import Message, OpenAIBackend, Role
from haikeilabs.agentware.llm.request import ToolDefinition

socket = KeiProxySocketAuthorizeClient()       # socket path and runtime token from the environment

async def backend_from_profile() -> OpenAIBackend:
    cfg = await socket.model_config()          # the agent's current profile, without secrets
    if "status" in cfg:                        # no_profile / profile_revoked
        raise RuntimeError(f"no model profile: {cfg['status']}")   # fail closed, no fallback model
    return OpenAIBackend(model=cfg["model"], base_url=cfg["endpoint"])

async def turn(messages: list[Message], tools: list[ToolDefinition]):
    backend = await backend_from_profile()     # re-resolve per conversation (or on a timer)
    resp = backend.complete(messages, tools)   # pass tools yourself (see the gap below)
    for call in resp.tool_calls:               # parsed from tool_calls; resp.reasoning holds reasoning_content
        await client.Execute(call.name, call.arguments, user_id=..., channel_id=...,
                             guild_id=None, func=TOOLS[call.name], caller=caller)   # decided by KeiProxyEvaluator
```

**What works today, per port:**

| | Model from the profile | Loop | Each call decided by `KeiProxyEvaluator` |
|---|---|---|---|
| Python | `await model_config()`, then `OpenAIBackend(model, base_url)` | Your own loop calling `backend.complete(messages, tools)`. `run_inference` drops the tools (`middleware/inference.py:113-129`) | Yes: `AuditedToolClient.Execute` with the evaluator |
| TypeScript | `await modelConfig()`, then `new OpenAIBackend({ model, baseUrl })` | `AgentLoop` sends the tools and runs each tool's own `execute`. It has no policy hook (`executor/agent_loop.ts:35-47, 330-345`) | Inside each tool's `execute`, `await evaluator.evaluate(name, args, caller)` and run only on allow. The async evaluator can't be used with `withPolicy` |
| Go | `ModelConfig(ctx, "", "")`, then `llm.NewServerBackend(llm.ServerConfig{BaseURL, Model})` | `inference.RunInference` returns the tool calls; you run them | `NewAuditedToolClient(...).WithPolicy(evaluator)` |

Parse tool calls and reasoning with the SDK, not by hand:

- `Response.tool_calls` comes from `parse_tool_calls`, which accepts
  arguments as a JSON string or an object. Validate the arguments against the
  tool schema.
- `ReasoningAdapter().strip()` / `.extract()` separate reasoning from the
  answer.

Per-family formats are in **kei-openai-backends**.

**SDK gaps (not built, don't invent them):**

- **No Agentware backend over kei-proxy.** No `Backend` / `AsyncBackend` /
  `llm.Backend` implementation wraps the socket client in any port (Python
  `llm/backend.py:11`, TypeScript `llm/backend.ts:12`, Go
  `go/llm/backend.go:8`).
- **The chat route the SDK calls doesn't exist.** The socket client's
  `chat_completion` / `stream_chat_completion` POST `/v1/chat/completions`,
  which `kei-proxy serve` does not serve.
- **The recipe above works only for profiles with `auth_type: none`**, such
  as a model server on your own network. An `api_key` profile needs the key
  at the provider. The only shipped path that keeps the key in kei-proxy is
  the `kei-proxy model` subprocess, and no Agentware wrapper exists for it.
  Don't copy the key into harness config.
- **TypeScript `AgentLoop` has no policy hook.** Each tool's `execute` has to check the evaluator itself.

**When the profile changes or fails:**

| Situation | What the harness sees | Do |
|---|---|---|
| The admin changes the profile on the console mid-session | The next `model_config()` returns the new model; kei-proxy doesn't cache | Re-resolve per conversation or on a timer, and build a new backend. A request already sent is not recalled |
| The profile is unassigned or disabled | `{"status":"no_profile"}` (a disabled profile shows the same; `profile_revoked` is possible but rare) | Stop model calls and tell the user. The workspace default applies only when the agent has no assignment at all |
| The credential is unavailable (`api_key` profile) | `KeiProxySocketError` with reason `proxy_error`, code `credential_unavailable` | Stop. See **kei-setup-doctor** |
| The daemon is down | `KeiProxySocketError` with reason `proxy_unavailable` | Stop. Never fall back to a hard-coded model |

## Validation commands

```bash
# In a kei-agents checkout
pytest && ruff check . && mypy src/agents
python -c "from agents import HARNESS_AGENT_DEFINITIONS, validate_agent_definitions as v; print(v(HARNESS_AGENT_DEFINITIONS))"   # []

# In an agentware checkout
cd python && pytest tests/kei/ -v                 # KeiProxyEvaluator fail-closed table
cd python && pytest tests/action_tool_boundary_test.py -v

# Prove fail-closed locally: with no kei-proxy on PATH every call is denied
PATH=/usr/bin:/bin python your_harness.py         # expect "kei-proxy missing_token" or "proxy_unavailable"
# ...and with a configured socket and no daemon: a refusal, never a CLI fall back
KEI_RUNTIME_SOCKET_PATH=/tmp/no-daemon.sock python your_harness.py   # expect "proxy_unavailable"
```

## Realistic usage boundaries

- The code is the source of truth. `docs/{python,go,typescript}/README.md` in
  agentware show old APIs (`middleware_py`, `LangGraphToolWrapper`) that no
  longer exist; trust the tests and the package exports.
- `kei-agents` is schemas, prompts, and permissions only. It has no provider
  clients and resolves no credentials; provider execution happens tenant-side
  in `kei-proxy`.
- `validate_agent_definitions` says an agent is well formed, not that it is
  allowed. The allow/deny is the workspace policy, at run time.
- Middleware decides and audits; it does not run the agent loop. Your harness
  (or `middleware/inference.py`) owns the loop.
- Writes (GitHub, Linear) are agent action tools executed by the harness,
  not connector capabilities.

## Related skills

- `agentware-sdk` — full SDK reference, decision table, Go/TypeScript ports.
- `kei-model-profiles` — how the agent's model profile is assigned and resolved at run time.
- `kei-agents` — the tool catalog, connector read schemas for connectors Kei checks, `render_tools`.
- `test-agents` — table-test evals for the agent you just built.
- `deploy-agents` — runtime, harness, policies, and per-user connectors.
- `templates/connector-skill` — where Lexicon/Pragmatics/Semantics are written down.
