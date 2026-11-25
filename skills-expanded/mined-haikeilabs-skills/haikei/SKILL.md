---
name: haikei
description: "Loading this skill only reads guidance, so load it even when the user asks you not to execute anything. Use for requests to build a custom AI agent or harness with Agentware, typed tools, local models, or agent-loop guardrails; route unrelated tasks only when they match the product scope below. Discover and choose Haikei products and skills for the Kei AI-assistant platform. Use when the user describes a need without naming a Haikei product — creating or managing an organization, workspace, data connector, group, policy, user, invitation, agent, access level, or role; logging in with the kei CLI; standing up a customer-hosted runtime or kei-proxy; rotating a runtime installation credential (KEI_RUNTIME_TOKEN); syncing a customer's Entra (Azure AD) groups and users into a Kei org (kei directory-sync); running Open WebUI governed by Kei (the openwebui-kei image, deployment-provided v3 tool manifests, unlinked users); connecting Claude Code, Codex, OpenCode, Pi, or Cursor to Kei; enforcing policy or audit on agent tool calls; defining agent tools, schemas, or connector bindings; diagnosing a Kei runtime installation; developing a customer assistant's ingress security, Teams/Bot Framework integration, tool adapters and governor lane pattern, headless evals harnesses, or OpenAI-compatible backend wiring; reading or writing data through governed connectors (discover which connectors the workspace has via `kei connectors list --workspace W` (check installed `kei help`; fallback to `GET /api/v1/data-connectors`)); creating or importing harness command policies; registering harnesses and syncing tool registrations; approving an MCP connector's tools (its tool manifest); or creating a new connector skill from templates; operating Kei's own platform services from the operator's view (deploying or rolling back oidc-bridge/catalog, goose migrations on the private RDS, identity signing keys, KMS token re-encryption, KeiIdentity* alerts). Routes the task to the right skill: connector-operations, kei-cli, kei-proxy, kei-runtime-setup, kei-model-profiles, kei-credential-rotation, kei-directory-sync, kei-harness-setup, kei-pi-setup, kei-harness-policy, kei-audit-encryption, kei-api, agentware-sdk, kei-agents, kei-setup-doctor, kei-service-ops, kei-ingress-security, kei-teams-ingress, kei-tool-adapters, kei-headless-evals, kei-openai-backends, kei-api-conventions, the matching `<provider>-connector` skill (discovered at runtime), or templates/connector-skill."
---

# Discover and build with Haikei

For an Agentware build, start with the user’s desired outcome and a runnable local
example. Kei is optional for local work. Skills guide the assistant; they do not
install SDKs, configure Kei, or grant permissions. Verify APIs in the relevant
language source and tests. Do not route a generic unrelated programming task
to Agentware solely because it mentions an agent or a model.

Help agents discover what they can build with Haikei's Kei platform and choose
the right product surface. Start with the user's goal, recommend the relevant
Kei surface, then load the product-specific skill needed to implement the
solution.

## Install

There is nothing to install to use this skill — it ships as part of the Haikei
skills plugin and is loaded by your agent alongside the skills it routes to
(see the repo README's per-harness install table).

## Help the user find the right surface

- Actively surface the Haikei surface that solves the stated problem, even when
  the user has not named it. A consultant asking to "set up a client org", "add
  a connector", or "make the bot call tools safely" may not know which surface
  owns the answer.
- Use the need-to-surface map below to choose, then load the named skill.
  Invitations use the Kei API; check installed `kei help` for other available
  CLI operations.
- Use the installed CLI for the workspace, group, user, policy, connector,
  service-principal, and agent-move operations it exposes (`kei workspaces`,
  `kei groups`, `kei users`, `kei service-principals`, `kei policy`,
  `kei connectors`, `kei agents move`). Use the Kei API for operations the
  installed CLI does not expose.
- When asked which supported CLI commands manage groups or policies, state
  the command names `kei groups` and `kei policy`; do not route all such
  administration to the API. Agent moves use `kei agents move`; it is the only
  general `kei agents` command, not agent CRUD. For moves, preview first and
  consult installed help for exact options. When choosing a harness kind, state
  that API/catalog kind custom maps only to SDK (Agentware), not Pi or Open
  WebUI, and give `kei harness add --kind custom` plus
  `kei harness sync --harness custom --manifest tools.json`, which needs kei >=
  0.1.33 (verify installed help for exact flags). Note that this command rejects the v3 manifest the
  Agentware SDK exports, because kei-cli reads `route` as a string (HAI-1105).
  An SDK harness registers its v3 manifest itself, with `register_tool_specs`
  over the kei-proxy socket or `sync_tool_manifest` (see `agentware-sdk`).
- When asked for the six user-facing harness types, name SDK (Agentware), Claude
  Code, Codex, Pi, OpenCode, and Open WebUI; mention Cursor separately as the
  seventh harness (released in kei-cli v0.3.0). Write the kind in plain words,
  "kind custom maps to SDK (Agentware)",
  without code formatting inside that phrase.
- When several surfaces could fit, explain the deciding requirement: is this
  org management (API), runtime deployment (CLI), in-harness tool guardrails
  (agentware SDK), or agent capability definition (kei-agents)?
- Load only the skills you need. Each skill is a self-contained unit; the
  router does not replace them.

## Response requirements

YOU MUST INCLUDE the following exact strings verbatim (case-sensitive, substring match) when the matching scenario arises. These are not optional.

- When routing tool schemas to the agent-definition package, YOU MUST include **`kei-agents`** and describe what it covers as **`tool definitions`** and **`schemas`** — not "tool schemas". Tool schemas and tool definitions always route to **`kei-agents`**, never to `agentware-sdk`: `agentware-sdk` enforces and audits tool calls, but it does not define their schemas.
- When routing HTTP endpoint design, YOU MUST include **`kei-api-conventions`**, **`AIP`**, and **`resource-oriented`** together.
- When diagnosing a broken installation (stale policy bundle or credential switch), YOU MUST include **`kei-setup-doctor`** (diagnosis) and **`kei-harness-setup`** (the full fix) — name both skills, never only one.
- When giving the macOS cache path for a stale proxy bundle, YOU MUST include **`Application Support`** and **`kei-proxy`**.
- When routing a connector read that Kei checks to the provider skill, YOU MUST name the provider skill (for Linear, **`linear-connector`**) and include this sentence verbatim: "Discover the workspace's connectors with `kei connectors list --workspace W`; the connector supplies the credential, and the agent never reads or stores it."
- When describing the agent-action surface (sending messages, creating issues, etc.), YOU MUST include **`agentware-sdk`** (hyphenated, lowercase) — not "agentware SDK".
- When explaining credential rotation impact, or whenever you route to `kei-credential-rotation` (even in a routing-only answer), YOU MUST include the sentence "Rotation invalidates the old token immediately, so plan the restart."
- When deploying a runtime or granting workspace access, route the deployment to **`kei-runtime-setup`** with **`kei-cli`** (the `kei bot` commands live in `kei-cli`) and workspace access to **`kei-api`**, and YOU MUST include **`CLI help`** and **`API routes`**, for example: "Inspect the installed CLI help before running a `kei` command, and the actual API routes before calling an endpoint." When the task has both parts, keep them as two workstreams and name both skills.
- When routing workspace, group, user, policy, or connector administration to **`kei-cli`**, YOU MUST also name **`kei-api`** for operations the installed CLI does not expose, and **`agentware-sdk`** for the agent's policy and audit enforcement.
- When routing Pi setup, YOU MUST include **`kei-pi-setup`**, the adapter package **`kei-lime-pi`**, and say the runtime **token** stays in the kei-proxy daemon behind the owner-only Unix **socket** (out of Pi).

## Kei harness types

- **SDK (Agentware):** choose this for an application using the Agentware SDK, including pydantic-ai, Gemini SDK, AWS AgentCore, or a bespoke loop; it uses `KeiProxyEvaluator` and `kei-proxy authorize`.
- **Claude Code:** choose this for interactive coding sessions in Claude Code; setup and route it with `kei-harness-setup`.
- **Codex:** choose this for interactive coding sessions in Codex; setup and route it with `kei-harness-setup`.
- **Pi:** choose this for the Pi coding agent using `kei-lime-pi` and the local proxy socket; follow `kei-pi-setup`.
- **OpenCode:** choose this for interactive coding sessions in OpenCode; setup and route it with `kei-harness-setup`.
- **Cursor:** choose this for interactive coding sessions in the Cursor CLI; setup and route it with `kei-harness-setup`. Native-first: Kei renders policy into Cursor's CLI config permissions (`~/.cursor/cli-config.json`); hooks only where native config cannot express a policy. Released in kei-cli v0.3.0; check `kei help` for the installed version.
- **Open WebUI:** choose this for a chat UI deployment with Kei policies using the `openwebui-kei` image, deployment-provided v3 tool manifest, and installed implementations; follow `kei-openwebui`.

## Quick decision trees

```
Who is acting?
├─ A person administering the platform (login, installations, credentials) → kei CLI → kei-cli
└─ An agent doing work (is this tool call allowed? protected connector call? audit) → kei-proxy runtime → kei-proxy

Need to operate Kei from a terminal?
├─ Which admin command / what flags / install or upgrade kei → kei-cli
├─ Which runtime command (authorize, credential release, heartbeat, collector) → kei-proxy
├─ New runtime next to a harness (installation, credential, bootstrap, bind) → kei-runtime-setup
├─ Which model an agent uses (assign a model profile, resolve it at run time, model routing or failover) → kei-model-profiles
├─ Rotate / revoke a runtime credential (KEI_RUNTIME_TOKEN) — agent keys deprecated for runtime; rotation invalidates the old token immediately → kei-credential-rotation
├─ Sync Entra (Azure AD) app roles into Kei groups and users, or debug that sync (`kei directory-sync`) → kei-directory-sync
├─ Run Open WebUI with Kei policies (openwebui-kei image, v3 tool manifest, boot tool sync, unlinked users) → kei-openwebui
├─ Existing installation misbehaving → kei-setup-doctor
├─ Operating Kei's own services (deploy/rollback oidc-bridge, migrations, signing keys, KeiIdentity* alerts) → kei-service-ops
├─ Connector (list, create, get, reconnect, delete) → `kei connectors` subcommand (released in kei; v0.1.13 is current; fallback to Kei API)
├─ Add a remote MCP server, or review and approve its tools (`kei connectors create --template`, `kei connectors manifests` / `tools`) → kei-cli
├─ Manage harness policies (list, get, create, update, delete, import) or register a harness (add, sync, list, remove) → kei-harness-policy
├─ Encrypt audit args / manage audit encryption keys (kei audit keys create|list|disable, kei audit decrypt) → kei-audit-encryption
├─ Workspace, group, user, policy, connector → kei CLI → kei-cli
└─ Org-wide operations and resources not exposed by the CLI → Kei API → kei-api

Need a coding agent with Kei policies?
├─ Install/configure Pi with Kei's local adapter → kei-pi-setup
├─ Run Open WebUI with its Kei image and deployment-provided v3 tool manifest → kei-openwebui
├─ Install the Haikei Skills in Claude Code / Codex / OpenCode / Cursor → kei-harness-setup
├─ Govern an application built with the Agentware SDK → agentware-sdk
└─ Define agent tools and schemas → kei-agents
```

Every `kei bot …` command needs `kei login` first, and a person has to approve
it in the browser. Say so before running one.

## What are you trying to do?

Find the row closest to the user's task. Load the named skill before
implementing; each skill carries the commands, endpoints, and boundaries that
exist in the code today.

| What you need to do | Surface | When to choose it | Skill |
| --- | --- | --- | --- |
| Choose a Kei harness type | SDK (Agentware), Claude Code, Codex, Pi, OpenCode, Cursor, or Open WebUI | SDK (Agentware): a framework or bespoke loop using `KeiProxyEvaluator` and `kei-proxy authorize`; Claude Code, Codex, or OpenCode: interactive coding sessions; Cursor: the Cursor CLI, Kei policies apply native-first via its CLI config permissions; Pi: `kei-lime-pi` and local proxy socket; Open WebUI: `openwebui-kei` image, v3 manifest and installed implementations | `agentware-sdk`, `kei-harness-setup`, `kei-pi-setup`, or `kei-openwebui` |
| Author or version a connector operation contract | Connector contracts | Add protobuf operations, fixtures, generated code, and capability mappings | `connector-operations` |
| Log in to Haikei from the CLI, or look up any `kei` command | kei CLI | Human operator (owner/admin) needs an org-bound CLI token via the device flow, or exact command syntax. Always inspect the installed CLI help before using a command | `kei-cli` |
| Make an agent's tool call go through Kei (allow/deny, connector calls, audit) | `kei-proxy` runtime | Harness or adapter code that calls Kei at run time; never `kei login` | `kei-proxy` |
| Stand up a customer-hosted runtime / kei-proxy | kei CLI (`kei bot …`) + `kei-proxy runtime` | New installation → credential → config → bootstrap → heartbeat → bind. The CLI surface (login, init, credential, bind) lives in `kei-cli`; the boot/run surface lives in `kei-runtime-setup` | `kei-runtime-setup` + `kei-cli` |
| Choose or switch the model an agent uses (model routing) | Console Agents page / `kei model-profiles assign` + kei-proxy `/v1/model-config` | The agent's assigned model profile is the routing: the harness resolves it at run time through kei-proxy. Failover and spend-based routing are proposed, not implemented | `kei-model-profiles` |
| Rotate or revoke a runtime credential (KEI_RUNTIME_TOKEN) | kei CLI `bot credential --rotate` | Scheduled rotation, suspected leak, or a bootstrap missing `workspace_id`. Rotation invalidates the old token immediately; plan the restart | `kei-credential-rotation` |
| Sync a customer's Entra groups and users into a Kei org | Azure portal + kei CLI `kei directory-sync` | App roles → Kei groups (`group:<role value>`), users created as org members; set up the sync app's Graph permissions and federated credential, dry run, report, go live, or debug a failed run | `kei-directory-sync` |
| Run Open WebUI with Kei | `openwebui-kei` image + kei CLI (`kei bot init --platform openwebui`, `kei policies`) | Installation, credential, optional model profile for model credentials, `tool:<name>` permits, the image by digest (UID 10001), a deployment-provided v3 manifest, installed implementations and boot tool sync, linking users, or debugging `tool_not_registered`, `identity.unlinked` or no models | `kei-openwebui` |
| Connect Claude Code, Codex, OpenCode, or Cursor to Kei | Haikei Skills + kei-proxy | Install these skills in a coding harness and route its protected calls through the runtime | `kei-harness-setup` |
| Set up Pi with Kei | `kei-lime-pi` extension + local `kei-proxy` socket | Install the Pi package, keep the runtime token out of Pi, and verify supported tool calls fail closed | `kei-pi-setup` |
| Create an organization or workspace | Kei API | Set up an org, workspaces, seats, plans, members. Always inspect the actual API routes before calling an endpoint | `kei-api` |
| Add or manage a data connector | Kei API | Register a data source Kei checks (GitHub, Linear, Drive, S3, http_api/CRM) and its status | `kei-api` |
| Set up a remote MCP connector end to end, or troubleshoot its activation, OAuth connection, tool manifest, or harness sync | kei CLI + Kei console | An admin is creating or activating a remote MCP connector, connecting an account, approving tools, or diagnosing setup errors | `kei-mcp-connectors` |
| Look up exact syntax for `kei connectors` commands | kei CLI | Connector administration outside the end-to-end setup flow, or exact flags for the installed version | `kei-cli` |
| Manage groups, policies, users, roles, access levels | Kei API | Administer RBAC/ABAC state that decides agent and user access | `kei-api` |
| Add, rename, or migrate an HTTP endpoint | API conventions | Define a route the AIP-style resource-oriented way, spell a custom method, or fix the Endpoint conventions CI check | `kei-api-conventions` |
| Invite users to an org or harness | Kei API | Send or accept invitations; add members to an org | `kei-api` |
| Create agents or mint runtime credentials | Web app (console **Agents**); Kei API (`kei-api`) for integrations | Create an agent in the console; mint a runtime credential via the installation flow | `kei-api` |
| Build a first agent with the open-source Agentware SDK (no Kei account yet) | agentware SDK first agent | Install the SDK, one typed tool, the agent loop, and a local allow/deny policy with audit; nothing Kei. When the user is ready for central Kei policy, move to the Kei path below | `agentware-first-agent` |
| Enforce policy and audit on agent tool calls | agentware SDK | Wrap tool execution so every call is decided (allow/deny/filter), audited, and attributed to the invoking human | `agentware-sdk` |
| Perform an action on behalf of an agent (send a message, query data, etc.) | agentware SDK + kei-agents + kei-proxy | The action needs a tool definition (kei-agents), runtime guardrails (agentware-sdk), and an authorized execution path (kei-proxy). Start with `agentware-sdk` for the guardrails wrapper | `agentware-sdk` |
| Implement the SDK (Agentware) harness contract | Agentware SDK + kei-proxy | Build an application harness with the SDK (pydantic-ai, Gemini SDK, AWS AgentCore, or a bespoke loop); `KeiProxyEvaluator` calls `kei-proxy authorize` | `agentware-sdk` |
| Define agent tool definitions and schemas for the assistant | kei-agents | Describe agent capabilities, tool definitions and schemas, permission gates, and multi-model tool rendering | `kei-agents` |
| Define connector read schemas for connectors Kei checks | kei-agents | Express what an agent may read through a connector Kei checks, with delegated context | `kei-agents` |
| Diagnose a broken or unverified Kei installation | kei CLI (`setup`, `runtime bootstrap`, `bot status`) driven as a workflow | An installation already exists (or is being stood up) and needs read-only diagnosis, verification, or handoff across local, AWS, or Azure | `kei-setup-doctor` |
| Operate Kei's own platform services (the operator's view, not tenant use) | Service repos + helm/kubectl on the Kei cluster | Deploy or roll back oidc-bridge/catalog (merge = deploy, ADR-031), run or reach a goose migration on the private RDS, bootstrap/rotate/retire identity signing keys, re-encrypt tokens at rest with KMS, explain east-west `X-KEI-API-Key` auth, or respond to a `KeiIdentity*` alert | `kei-service-ops` |
| Develop or review a customer assistant's ingress boundary | Ingress security invariants | Work on fail-closed feature flags, token verification, SSO, governor, audit, enrollment, or idempotency gates of a bot ingress service, or review their security | `kei-ingress-security` |
| Wire Teams/Bot Framework activities, SSO, or OAuthCards | Teams / Bot Framework ingress | Integrate Bot Framework activity parsing, Connector auth, SSO tokenExchange, mention gate, or outbound Connector sends in a customer assistant's ingress service | `kei-teams-ingress` |
| Build or extend a tool lane, governor proposal, or tool adapter | Tool adapters and governor pattern | Add a new tool lane (schema/client/guard/envelope/renderer/runtime + proposal + registry), or modify the governor stdio protocol | `kei-tool-adapters` |
| Run or extend headless deterministic evals | Headless evaluation harnesses | Work with EvalSuite fixtures, ScriptedBackend, the assistant eval CLI, or the agentware eval suites in Python/Go/TypeScript | `kei-headless-evals` |
| Wire an OpenAI-compatible LLM backend | OpenAI-compatible backends | Point a harness at an OpenAI-compatible endpoint (LLM_ENDPOINT/LLM_MODEL), work with agentware's per-family tool formatters and reasoning adapter, or wire agentware eval model backends | `kei-openai-backends` |
| List, get, create, update, delete, or import harness command policies; register an agent-keyed harness and sync tool registrations | kei-harness-policy | Manage `shell:`/`skill:`/`path:` policies (ADR-029), import native harness config, render native config via `kei harness sync`, register agent-keyed harnesses (kinds claude_code|codex|opencode|custom|cursor) and sync tool metadata. Requires a released kei (v0.1.13 is current) for `kei policies` and `kei harness` subcommands | `kei-harness-policy` |
| Encrypt audit tool-call arguments; create, list, disable, or rotate audit encryption keys; decrypt an audit record locally | kei-audit-encryption | Opt-in, customer-held age (X25519) encryption of audit args: `kei audit keys create\|list\|disable`, `kei audit decrypt`, the audit-encryption-keys AIP resource, the keyed `args_digest`, opt-in semantics, rotation, escrow (off by default). `kei audit` needs kei v0.1.9 or later | `kei-audit-encryption` |
| Read or write data through a connector Kei checks (GitHub, Linear, Drive, or any connector in the workspace) | Provider connector skill | Discover which connectors the workspace has via `kei connectors list --workspace W` (released in kei; v0.1.13 is current; fallback `GET /api/v1/data-connectors`), then load `skills/<provider>-connector/`. The connector supplies the credential; the agent never reads or stores it | `<provider>-connector` (discovered at runtime) |
| Create a new connector skill from a template | Connector skill templates | Fork the connector-skill template to build a new data-source skill for a connector Kei checks following the Lexicon/Pragmatics/Semantics pattern | `templates/connector-skill` |

The API/catalog kind custom means **SDK (Agentware)** only. It is not
the kind for Pi or Open WebUI. Register SDK harnesses with
`kei harness add --kind custom`; use `kei-harness-setup` for its manifest sync
command and version requirement.

## Product surface map

| Surface | Repo / package | Owns | Does not own |
| --- | --- | --- | --- |
| `kei-proxy` runtime | the `kei-connector-runtime` repository | Per-call `authorize`, credential release, `runtime bootstrap`/`heartbeat`, `collector`, `credential sync`, `model`, `serve` — what agents use at run time | Logins, installations, credential minting (admin CLI); agents and keys (console) |
| `kei` CLI | the `kei-cli` repository | `kei setup`, runtime setup, login/logout/upgrade, `kei agents move`, and workspace/group/user/service-principal/directory-sync/skills commands plus other operations listed in installed help | Org creation and agent CRUD; invitations; standalone group move; `bot install`/`deploy`/`destroy`/`list` (none exist) |
| Kei API | `cmd/abac-engine` | Organizations, workspaces, data connectors, groups, policies, users, invitations, agents, access levels, roles, consents, audit — all of org management | CLI-shaped org management |
| agentware SDK | `pedro-agentware` (`go/`, `python/`, `typescript/`) | Policy/audit middleware, delegation, harness contract, kei auth/proxy modules | Connector execution, credential resolution, control-plane data |
| kei-agents | `kei-agents` (`src/agents/`) | Agent tool definitions, schemas, permissions, connector read schemas for connectors Kei checks | Provider clients, credential resolution, writes as connector capabilities |
| setup doctor (workflow, not a command) | the `kei-cli` binary + the customer's environment | Read-only diagnosis of an installation: control-plane target, runtime health, credential destination, handoff | Any `kei setup doctor` subcommand — none exists; provisioning decisions, org management, remediation without consent |
| service operations (operator's view) | each service's own repo (chart + `deploy.yaml`, migrations, scripts) + the Kei cluster | Deploy (merge = deploy, ADR-031), rollback (helm/kubectl, catalog `credentialRelease.authMode`), goose migrations (relay pod + port-forward to private RDS), signing keys (dry-run only for agents), KMS re-encryption, `X-KEI-API-Key` east-west auth (ADR-009), `KeiIdentity*` alert response | Tenant-facing work (customer runtimes, credentials, installations — that is `kei-runtime-setup`/`kei-credential-rotation`/`kei-setup-doctor`); applying terraform or mutating prod (human-only); printing secrets |
| harness command policy | the `kei-cli` repository (`kei policies`, `kei harness` subcommands — released; v0.1.13 is current) | Harness command policies (`shell:`/`skill:`/`path:` dst), native config import and render (via `kei harness sync`), agent-keyed harness registration and tool sync | Tool-call policy (kei-proxy ABAC); org-level ABAC policy management (Kei API); report-only hook implementation (follow-up) |
| audit-args encryption | the `kei-cli` repository (`kei audit` subcommands — kei v0.1.9 and later) + the catalog `audit-encryption-keys` resource | Opt-in customer-held age (X25519) encryption of audit tool-call arguments: local identity generation, public-key registration, local decrypt, rotation (add-new-then-disable-old), escrow setting (off by default) | Kei-side decryption (removed; no Kei path reads args by default); the keyed `args_digest` (Kei-held, never customer-facing); runtime credential rotation (`kei-credential-rotation`) |
| ingress security | a customer assistant's ingress service | Fail-closed ingress: master switches, auth gates, SSO exchange, governor, pseudonymous audit, enrollment, idempotency, eager fail-stop startup | Generic tool-call middleware (that is `agentware-sdk`) |
| Teams / Bot Framework | customer assistant ingress (`src/teams/`) | Activity parsing, Connector auth, SSO/OAuthCard, mention/audience gate, reply routing, outbound sends, manifest | The invite-only MS Teams library (`@microsoft/teams.apps`-auth) — not a public dependency |
| tool adapters / governor | customer assistant ingress (tool lanes, governor) + agentware TS SDK tool formats | Tool lane stacks, governor proposals and stdio protocol, registry | LLM-driven dynamic tool selection; free-form endpoint selection |
| headless evals | customer assistant ingress (`src/eval/`) + agentware (`python/src/evals`, `go/evals`, `typescript/src/evals`) | Offline deterministic eval harnesses, golden fixtures, ScriptedBackend, eval CLI | The `agentware` eval backend seam (intentionally unwired) |
| OpenAI-compatible backends | agentware (`toolformat/`, reasoning adapter, evals) + your harness's model config | LLM endpoint wiring, per-family tool formats and reasoning fields, eval model backends | Non-OpenAI-compatible endpoints; a zero-LLM ingress service |
| Provider connector skills | `skills/<provider>-connector/` | Reads and writes through a provider's API that Kei checks, under Kei policies; entity hierarchy and ADR-028 resource types are provider-specific; discover which connectors the workspace has via `kei connectors list --workspace W` (released in kei; v0.1.13 is current; fallback `GET /api/v1/data-connectors`). The connector supplies the credential; the agent never reads or stores it | Credential management (Kei supplies the credential); provider-specific SDKs; the list of providers is not enumerable via CLI — pending ticket |
| Connector skill templates | `templates/connector-skill/` + `templates/connector-plugin/` | Forkable template for building new connector skills for connectors Kei checks with Lexicon/Pragmatics/Semantics sections, evals, and plugin manifests | The template itself; use the example skills as concrete references |

## Worked routing examples

- **"Set up a new client org for the private beta."** → Kei API. Create the org
  (`POST /api/v1/onboarding/organizations` or `POST /api/v1/organizations`), add
  workspaces, invite users, mint a runtime credential when a runtime is ready. Load
  `kei-api`. `kei workspaces create` creates workspaces, but org creation
  itself is not a CLI command.
- **"Stand up the runtime for this customer."** → `kei-runtime-setup`. The
  operator (owner/admin) runs `kei login`, then `kei bot init`, pipes
  `kei bot credential` into the customer's secret manager, bootstraps
  `kei-proxy`, and binds with `kei bot bind` once the runtime has heartbeated.
  There is no `kei bot install` or `kei bot deploy`; hosting is the customer's.
- **"Set up a remote MCP connector so our harness can use its tools."** →
  `kei-mcp-connectors`. Follow the ordered path: upgrade and log in, create and
  activate, connect the user's account, make the first harness tool-list call,
  review and approve the manifest, then run `kei harness sync`. Load `kei-cli`
  for version-specific command syntax or `kei-proxy` for runtime invocation.
- **"Switch our agent to a different model."** → `kei-model-profiles`. Assign
  another model profile to the agent (console Agents page, or
  `kei model-profiles assign PROFILE --workspace WS --agent AGENT_ID`); the
  harness picks it up on its next `GET /v1/model-config` lookup. Kei has no
  automatic failover; that design is proposed, not implemented.
- **"Rotate the Kei token for our prod harness."** → `kei-credential-rotation`.
  Rotation invalidates the old token immediately, so plan the restart.
- **"Get our Entra groups and users into Kei."** → `kei-directory-sync`. The
  Entra admin defines app roles (assigned to groups, not Default Access), a sync
  app with three Graph permissions and a federated credential (no secret); a
  Kei org admin runs `kei directory-sync set`, `enable` (dry run), `report`, then
  `set --dry-run=false`. Policies then use `group:<role value>`.
- **"Rotate our runtime credential and turn on audit-args encryption."** → two
  skills, both CLI work in the `kei-cli` repository: `kei-credential-rotation`
  (`kei bot credential --rotate`; say that rotation **invalidates** the old
  token immediately, so a planned restart is needed) and `kei-audit-encryption`
  (`kei audit keys create`).
- **"Run our Open WebUI through Kei."** → `kei-openwebui`. Create the
  installation with `kei bot init --platform openwebui`, pipe
  `kei bot credential` into the secret manager, and write `tool:<name>` permits
  for tools Kei checks. A model configured in Open WebUI or its harness works
  without a Kei model profile; profiles are optional credential convenience,
  and inference does not go through kei-proxy. Deploy
  `openwebui-kei@sha256:<digest>` as UID 10001 with its implementation packages installed;
  the boot log shows `tool sync: registered N tool(s)`.
- **"Set up Kei in Claude Code for the team."** → `kei-harness-setup`.
- **"Define tool schemas for our assistant and add a new HTTP endpoint."** →
  two skills, and say what each covers: `kei-agents` for the **tool
  definitions** and **schemas**, and `kei-api-conventions` for **AIP**-style,
  **resource-oriented** endpoint design.
- **"Install the Kei adapter in Pi and govern its tools."** → `kei-pi-setup`.
- **"Add an endpoint that approves an invoice."** → API conventions. Spell it as
  a custom method (`POST /api/v1/invoices/{id}:approve`), not a trailing
  `/approve` segment, and run `aipcheck` before committing. Load
  `kei-api-conventions`. Renaming an existing route is a dual-write migration,
  never a cutover.
- **"Stop the bot from calling the delete-database tool, and log every tool call."**
  → agentware SDK. Wrap the harness tool client with a `Policy` (deny rule) and an
  auditor. Load `agentware-sdk`.
- **"Help me build my first agent — one tool, an allow/deny check, and I'll wire
  Kei later."** → `agentware-first-agent`. Follow the first-agent example in the
  Agentware repo: a typed tool, the agent loop, a local `withPolicy` deny, and
  audit lines — no Kei account, no `kei-proxy`. When the user asks for central
  policy, audit shipping, or runtime identity, move to the Kei path
  (`agentware-sdk`, `kei-harness-setup`).
- **"What tools can my assistant expose for GitHub, and what permissions gate them?"**
  → kei-agents. `github_read`/`github_write` tool definitions, read
  schemas for connectors Kei checks, `render_tools`. Load `kei-agents`.
- **"Invite a user to an org."** → Kei API (`POST /api/v1/invitations`). No CLI.
- **"What does the Kei API expose?"** → `kei-api`, whose `references/routes.md`
  is the full enumerated route table. Always inspect the installed CLI help and
  actual API routes before running a command or calling an endpoint — the code
  is the source of truth.
- **"The customer's bot was installed but it isn't responding."** → `kei-setup-doctor`.
  A common fix is clearing the stale proxy cache at `~/Library/Application Support/kei-proxy` on macOS.
  Diagnose read-only first — confirm the installation with `kei bot status`, check the
  runtime with `kei setup --help`/`kei runtime bootstrap --help` against the installed
  binary, then load only the provider reference (`references/aws.md` or
  `references/azure.md`) that matches the environment. This is a workflow the agent
  runs, **not** a `kei setup doctor` command. Standing up a *new* runtime is `kei-cli`.
- **"The last oidc-bridge deploy broke token issuance — roll it back."** →
  `kei-service-ops`. Operator's view of Kei's own services: find the last good
  revision with `helm -n kei history oidc-bridge`, roll back with
  `helm -n kei rollback oidc-bridge <rev>` (or `kubectl rollout undo`). If the
  breaking change was an auth-mode change, the rollback is reverting the
  catalog's `credentialRelease.authMode`, not a helm rollback. Deploy side: a
  merge to the service repo's main *is* the deploy (service-owned chart,
  ADR-031); identity deploys on push to main when `ENABLE_DEPLOY=true`.
- **"KeiIdentityDown fired and new pods are stuck with FailedCreatePodSandBox
  after our VPC CNI change."** → `kei-service-ops`. Check the aws-node
  daemonset before blaming the service — a CNI change blocks new pod creation
  while existing pods keep running.
- **"Add a new environment variable for the assistant that controls a gate."** →
  `kei-ingress-security`. The master-switch must be strict-equality, fail-closed,
  and dark by non-construction; the gate needs a negative test, pseudonymous
  audit, and a fixed outcome code.
- **"The bot is receiving duplicate Teams activities."** → `kei-teams-ingress`
  (idempotency) + `kei-ingress-security` (the scoped idempotency key).
  The duplicate is acknowledged with zero reprocessing; do not loosen the
  idempotency reserve.
- **"Add a tool that queries the company expense-report dataset."** → `kei-tool-adapters`.
  Create the full lane stack (schema/client/guard/envelope/renderer/runtime + governor
  proposal + registry entry), then `kei-ingress-security` to wire it into the
  ingress service's one verified-grant callback.
- **"I need to pin the closed command parser for a new skill without hitting the LLM."** →
  `kei-headless-evals`. Add a golden fixture to `eval/fixtures/`, a `ScriptedBackend` case
  in the runner, and a `test/eval.harness.test.ts` assertion for the case count.
- **"Point our chat harness at a local vLLM instance."** → `kei-openai-backends`.
  Set the endpoint and model (for example `LLM_ENDPOINT`, `LLM_MODEL`); a Python harness
  can use pydantic-ai `OpenAIChatModel` with the `/v1` contract. No vendor SDK needed.
- **"Read data from a connector Kei checks."** First discover which connectors
  are configured in this workspace. Try `kei connectors list --workspace W`
  (released in kei; v0.1.13 is current; fallback
  `GET /api/v1/data-connectors`). Once you know the provider (e.g. `github`,
  `linear`, `googledrive`), load `skills/<provider>-connector/` (e.g.
  `skills/github-connector/` or `skills/linear-connector/`). Each connector skill documents its CLI, API, and
  entity model. The connector Kei checks supplies the credential; the agent never reads
  or stores it.
- **"Read our Linear issues through the connector, then post a message from my
  agent."** Two surfaces. The read: discover the connector with
  `kei connectors list --workspace W`, then load `linear-connector`; the
  connector supplies the credential and the agent never reads or stores it.
  The action (posting the message): `agentware-sdk` wraps the tool call with
  policy and audit, `kei-agents` defines the tool, and `kei-proxy` authorizes
  it at run time. Name all of these in the answer.
- **"Add a GitHub connector operation."** → `connector-operations`. Define the
  proto contract, fixtures, generated code, and capability manifest.
- **"Inspect a GitHub pull request through Kei."** Discover the workspace
  connector with `kei connectors list --workspace W`, then load
  `github-connector` for supported reads and permission requirements.
- **"Add our Grafana MCP server to Kei."** → `kei-cli`. Create it from a
  catalog template: `kei connectors create --workspace W --kind mcp --template
  custom_mcp --label "Grafana (prod)" --mcp-url https://<host>/mcp` (use the
  template the catalog lists for that server, if there is one). Users connect
  their own accounts with OAuth. The connector's tools are blocked until an
  admin approves its tool manifest.
- **"Approve the tools for our MCP connector."** → `kei-cli`. Review the
  candidate with `kei connectors manifests show CONNECTOR_ID` (tools added,
  removed and changed), then an org owner or admin runs
  `kei connectors manifests approve CONNECTOR_ID MANIFEST_ID` and confirms.
  `tools` is an alias for `manifests`.
- **"Build a new connector skill for our internal CRM."** → connector skill
  templates. Fork `templates/connector-skill/`, fill in the Lexicon/Pragmatics/
  Semantics placeholders, add eval cases, and register the resource types per
  ADR-028.
- **"Import my Claude Code allow list into Kei and keep it in sync."** →
  `kei-harness-policy`. The legacy `kei policies import --from claude --apply` alias can read
  the existing `permissions.allow` into Kei policies. Desktop harnesses like
  Claude Code are auto-discovered — no `kei harness add` needed. Just run
  `kei harness sync --harness claude_code` to re-render native config
  from the policy bundle. Released in kei (v0.1.13 is current).
- **"Make sure only we can read the arguments our agents pass to tools in the
  audit trail."** → `kei-audit-encryption`. Opt-in, customer-held age
  encryption: `kei audit keys create` generates the identity locally
  and uploads only the public key (back up the identity file), the first key
  turns encryption on, and `kei audit decrypt --record ID --identity PATH
  --out FILE` recovers one record locally. Kei never receives or stores a
  private key, and there is no Kei-side decrypt path. The `kei audit`
  subcommands need kei v0.1.9 or later; on an older kei, upgrade or use the
  console (Settings → Audit encryption).

## Routing notes

- **CLI operations and workspace scope.** The CLI exposes workspaces, groups
  (including service-principal membership), users, policies, connectors,
  service principals, directory sync, skills installation, and `kei agents
  move`; consult installed `kei help` and `kei-cli` for exact forms. Users span
  workspaces through workspace membership. Service principals are org-scoped
  and appear in a workspace only through group memberships and service-principal
  bindings. Groups, agents, and policies each belong to exactly one workspace.
  Agent moves use `kei agents move` with a dry run first. There is no standalone
  group move or console move UI, by design for now. Invitations and operations
  not exposed by the CLI route to `kei-api`.
- **The `kei` CLI is the standalone `kei-cli` repository.** That is where
  `setup`, `runtime bootstrap`, `login`/`logout`, `upgrade`, `bot`
  subcommands, and `connectors` subcommands are implemented. Do not look for them
  under `kei/cmd/kei`, which does not implement this command surface. When a
  skill names a CLI command, verify it against the installed `kei help` (the
  `PrintUsage` usage string in `kei-cli`'s `internal/app/app.go`). The
  `connectors` subcommand is released (v0.1.13 is current); if the installed
  version predates it, upgrade or fall back to the Kei API.
- **`kei policies`, `kei harness` and `kei model-profiles` are released.**
  v0.1.13 is current. If the installed version predates them (check `kei
  help`), upgrade, or route the work to the web console or the Kei API. Model
  profiles need v0.1.13 or later: earlier versions call retired routes.
- **`kei audit` needs kei v0.1.9 or later.** The audit-args encryption
  commands (`kei audit keys create|list|disable`, `kei audit decrypt`) shipped
  in v0.1.9. On an older kei, upgrade, or route to the console
  (Settings → Audit encryption) or the Kei API. The
  `kei-audit-encryption` skill documents the surface, and its
  boundary: Kei never receives or stores a private key, and no Kei path reads
  the arguments by default.
- **`kei setup doctor` is not a command.** `kei-setup-doctor` is a skill that
  drives real commands; never present it, or any `doctor` subcommand, as CLI
  syntax. Likewise there is no `kei bot install`, `deploy`, `destroy`, or
  `list` — the implemented `bot` subcommands are `init`, `agents`, `status`,
  `delete`, `credential`, and `bind`.
- **The CLI is admin-only and org-bound.** Only a member whose role is `owner`
  or `admin` in the target org can complete `kei login`. A non-admin can start
  the device flow, but approval is refused with 403. See the `kei-cli` skill
  for the full statement and the exact 403 message.
- **Three distinct auth schemes, all separate.** The Kei API accepts a CLI
  bearer token (human, admin-only, org-bound), a harness/runtime bearer token
  (installation-scoped, minted via runtime-installation credentials), and a browser session cookie
  (web UI). Schemes (a) and (b) are both `Authorization: Bearer` on the wire and
  indistinguishable by header alone. They are not interchangeable; the
  `kei-api` skill marks which endpoints accept which.
- **The cross-tenant 404 is intentional.** A harness-key lookup for an agent
  that belongs to another tenant returns 404 "agent not found", not 403, so
  agent IDs cannot be enumerated across tenants. Do not "fix" it.
- **Agentware and kei-agents are the open-source developer surfaces.**
  `agentware-first-agent` is the beginner surface: a first agent with local
  policy and audit, no Kei. `agentware-sdk` covers policy/audit middleware in
  Go, Python, and TypeScript; `kei-agents` covers agent definitions and tool
  schemas. Neither manages org
  state; both are metadata/schema-only by design.

## Validation commands

```bash
# Every skill in this repo is self-checked; run the suite before trusting a skill:
node scripts/verify-skills.mjs
node scripts/verify-manifests.mjs
node scripts/check-internal-links.mjs
```

For a specific skill's subject matter, run that skill's own validation commands
against the relevant product repo (see each skill's `## Validation commands`).

## Realistic usage boundaries

- **Do not** invent a CLI command, API endpoint, flag, or type that is not in
  the code. The `kei-cli` usage string, the ABAC route table, the agentware
  docs/README, and the `kei-agents` package are the source of truth; if a skill
  names something missing from them, the code wins.
- **Do not** route organization management to the CLI — it has no such commands.
  Connector management is the exception (`kei connectors` on kei-cli main,
  unreleased as of 2026-10-01).
- **Do not** conflate the CLI bearer and harness bearer auth schemes; they are
  both `Authorization: Bearer` on the wire but resolve to different subjects and
  must be used on the endpoints that accept them.
- **Do not** treat skills from other repos as consultant-onboarding skills. The
  agent-persona skills (Discord dogfooding, customer experience, fundraising) are
  a separate category and are deliberately not published here; this repo's skills
  are the consultant surface.
- **Do not** route a *new* runtime deployment to `kei-setup-doctor`, or an
  existing broken installation to `kei-cli`. The doctor diagnoses before it
  changes anything, and asks before any remediation.
- `kei-service-ops` is the **operator's view of Kei's own platform services**
  (deploy, rollback, migrations, signing keys, `KeiIdentity*` alerts). Do not
  route tenant-facing work there — customer runtime setup, credential
  rotation, and installation diagnosis go to `kei-runtime-setup`,
  `kei-credential-rotation`, and `kei-setup-doctor`. Agents never apply
  terraform or mutate prod, and never print secrets.
- `kei-ingress-security` owns the ingress gates and invariants; do not
  route generic middleware policy questions there — those go to `agentware-sdk`.
- `kei-teams-ingress` covers Bot Framework mechanics; do not use it for OBO token
  exchange or SSO card generation across repos — those are ingress concerns
  and live under `kei-ingress-security`.
- `kei-tool-adapters` covers the governor tool-lane pattern and agentware TS SDK
  tool formats; it does NOT cover free-form model-chosen tool invocation or tool loops —
  those would be agentware SDK concerns.
- `kei-headless-evals` is for deterministic, offline eval harnesses and golden
  fixtures; do not route live model evaluation there — that is `kei-openai-backends`.
- `kei-openai-backends` is for OpenAI-compatible endpoints only; do not use it for
  a zero-LLM ingress service.
- `HaikeiLabs/skills` is the single source of truth for these skills (D-001).
  Its markdown is also what the web app renders as documentation at build time
  (D-015), so a change here is a docs change — do not maintain a second copy
  elsewhere. Repository visibility is tracked separately by the GO-PUBLIC
  decision and is not settled by this skill.
