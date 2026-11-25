---
name: kei-agents
description: Use the kei-agents package for agent definitions, tools, and schemas on the Kei AI-assistant platform. Use when defining agent capabilities, tool schemas, permission gates, multi-model tool rendering (OpenAI, Anthropic, Ollama, Llama, vLLM), governed connector read schemas (GitHub, Linear, Google Drive/Docs, S3, http_api/CRM), policy/permission evaluation, or semantic mappings between tools and connectors. Covers render_tools, ModelFormat, Permission, ToolDefinition, ToolBinding, PolicyEngine, and validate_tool_definitions; reads are connector capabilities, writes are agent action tools.
---

# Kei Agents

`kei-agents` defines **agent capabilities, tool schemas, and semantic mappings
only**. Provider execution and customer data retrieval happen in the
tenant-side distributed proxy; Kei is a metadata catalog and ABAC is a policy
decision point. This is a docs-only repository: no provider clients, no
credential resolution, no secret material. Provider execution and credentials
stay out of kei-agents tool definitions: a tool definition describes the
capability and its schema, and the tenant-side proxy executes the call with a
credential the agent never sees.

Source of truth: the package source (`src/agents/` in the kei-agents repo,
package import name `agents`), `README.md`, `docs/connector-tool-schemas.md`.
The package source and docs are the authority for exact API names; check them
before naming a class, function, or constant, rather than relying on this
skill's summary.

## Response requirements

YOU MUST INCLUDE the following exact strings as written (case-sensitive, substring match). These are not optional — if a scenario applies, the listed terms must appear verbatim in your response.

- **Package name**: `kei-agents` — NOT the Python import name "agents". When writing import statements, use `from kei-agents import ...` only in prose descriptions (not actual Python syntax); in code blocks use `from agents import`. YOU MUST include the string `kei-agents` whenever describing the package or its concepts.
- **Entity definitions** (the `ToolDefinition` instances): `tool definitions` (lowercase, plural) — e.g. "the tool definitions in kei-agents". Do NOT substitute "ToolDefinition instances" or "tool schemas".
- **Python `ToolDefinition` class**: `ToolDefinition` (capital T, capital D)
- **`connector_id` values and binding config**: when describing a `ToolBinding`, say that binding config holds only `connector_id` placeholders (references to `abac.connection_presets.id`), never endpoints or credentials; the tenant-side runtime resolves the real preset, endpoint, and credentials at invocation time.
- **What to run before exposing tools**: `validation` — the word "validation", not just the function name "validate_tool_definitions"
- **What constant to pass to validation**: `ALL_TOOL_DEFINITIONS`
- **How permission gates are expressed on protected read schemas**: `ABAC` (the acronym must appear)
- **Which field carries tenant-side parameter names for the proxy to supply**: `delegated_context` (underscored, lowercase — not "Delegated context")
- **Where to find exact API names**: whenever an answer names a class, function, or constant, YOU MUST say the `package source` and `docs` are the authority for exact API names — also name the file `model_format.py` when describing render format detection
- **What stays out of definitions**: whenever an answer covers what kei-agents contains or where provider calls and credentials live, YOU MUST say provider execution and credentials stay out of kei-agents `tool definitions` (the tenant-side proxy executes the call)
- **`http_api`/CRM execution**: when asked where CRM or `http_api` reads run, YOU MUST include `http_api`, `crm`, `identity mode` (the read runs in kei-proxy identity mode), `kei-agents` (the read schemas in kei-agents do not change), and `POLICY_BUNDLE_V2_CONNECTORS`: say it is not live until the catalog's `POLICY_BUNDLE_V2_CONNECTORS` gate is enabled (off by default) and kei-proxy 0.2.5 or newer is deployed.
- **GitHub read-tool examples**: when listing GitHub read schemas, YOU MUST include both `list_repositories` and `read_issue` — mentioning only one of them is not sufficient. Always name both.

## Install

`kei-agents` is distributed from the internal AWS CodeArtifact index, not from
public PyPI (decision D-008). Log in once per session with the AWS CLI, then
install normally:

```bash
aws codeartifact login --tool pip --domain haikei --domain-owner <ACCOUNT_ID> --repository <REPOSITORY_NAME>
pip install kei-agents
```

- `<ACCOUNT_ID>` is the 12-digit AWS account that owns the `haikei`
  CodeArtifact domain. Substitute the real value; it is not published in this
  repo.
- `<REPOSITORY_NAME>` is the CodeArtifact repository that serves `kei-agents`.
  The AWS CLI requires `--repository` on `login`.
- Public PyPI publication is deferred to a ticket (D-008); `kei-agents` is not
  on PyPI.
- Without AWS access, install from a checkout of the kei-agents repo instead:
  `pip install -e ".[dev]"` (see Validation commands).

## Public surface

```python
from agents import TOOL_DEFINITIONS, render_tools, ModelFormat

tools = render_tools(TOOL_DEFINITIONS, ModelFormat.OPENAI)  # or by model name: "gpt-4"
```

Also exported: `ALL_TOOL_DEFINITIONS`, per-connector read collections
(`CONNECTOR_READ_TOOL_DEFINITIONS`, `GITHUB_READ_TOOL_DEFINITIONS`,
`LINEAR_READ_TOOL_DEFINITIONS`, `DRIVE_READ_TOOL_DEFINITIONS`,
`S3_READ_TOOL_DEFINITIONS`, `HTTP_API_READ_TOOL_DEFINITIONS`),
`render_openai_tools`, `render_anthropic_tools`, `render_ollama_tools`,
`detect_model_format`, `get_tool_by_name`, `get_tools_by_category`,
`get_tools_by_permission`, `get_tools_for_model`, `validate_tool_definitions`,
plus the policy module and GitHub adapters.

## Core types

- `ModelFormat` — `OPENAI`, `ANTHROPIC`, `OLLAMA`, `LLAMA`, `VLLM`. `detect_model_format(name)`
  infers the format from a model name. An unsupported format raises an error.
  See `model_format.py` for the exact enum values and detection logic.
- `Permission` — the permission scopes that gate tools: `search_wiki`, `web_search`,
  `schedule_meetings`, `github_read`, `github_write`,
  `linear_read`, `drive_read`, `s3_read`, `http_api_read`.
- `ToolCategory` — `search`, `productivity`, `github`, `entertainment`,
  `linear`, `drive`, `s3`, `http_api`.
- `ToolParameter` — name, type, description, required, enum, default.
- `ToolBinding` — **non-secret routing metadata**: `connector_id` references
  `abac.connection_presets.id`; `config` holds non-secret routing hints;
  `delegated_context` lists field names the tenant-side proxy supplies at invocation.
  Never carries secrets, credentials, or provider clients.
- `ToolDefinition` — name (must match `^[a-z0-9_]+(\.[a-z0-9_]+)*$`), description,
  parameters, permission gate, category, `service` (credential-lookup service; empty
  means policy-only), version, tags, optional `binding`, optional `handler`
  (harness-side; not required for the catalog).

## Example agent tools

| Tool | Description | Permission |
|------|-------------|------------|
| `search_wiki` | Search conversation history | `search_wiki` |
| `web_search` | Search the web | `web_search` |
| `schedule_meeting` | Schedule calendar meetings | `schedule_meetings` |
| `list_prs` / `list_issues` | List GitHub PRs/issues | `github_read` |
| `create_issue` / `create_pull_request` | Create GitHub issues/PRs | `github_write` |
| `get_workflow_status` | Get CI/CD workflow status | `github_read` |
| `start_game` | Start interactive games | `search_wiki` |

Full list is in `src/agents/tool_definitions.py`. GitHub mutations
(`create_issue`, `create_pull_request`) are **action tools gated by
`Permission.GITHUB_WRITE`** — they are never Kei connector capabilities.

## Connector read schemas for connectors Kei checks

Provider-neutral, schema-only **read** capabilities. Each schema expresses:

1. **Capability binding** — a `Permission` gate (e.g. `linear_read`) and a `ToolCategory`.
2. **Resource binding** — `ToolBinding.config.resource` names the bound resource type
   (`repository`, `issues`, `objects`, `records`, ...). The resource scope is routing
   metadata that Kei checks, not an agent parameter.
3. **Action binding** — tool `name`/`description` are the action (list/get). Reads only;
   writes stay agent action tools.
4. **Delegated context** — `ToolBinding.delegated_context` lists non-secret field names
   the tenant-side proxy supplies at invocation. The agent never provides them, so they
   must not appear as tool parameters.

| Connector | Permission | Category | Read schemas | Delegated context |
|-----------|-----------|----------|--------------|-------------------|
| GitHub | `github_read` | `github` | `github.list_repositories`, `github.read_issue`, `github.get_pull_request` | `tenant_id`, `repository` |
| Linear | `linear_read` | `linear` | `linear.list_issues`, `linear.get_issue`, `linear.list_projects` | `tenant_id`, `workspace` |
| Google Drive/Docs | `drive_read` | `drive` | `drive.list_files`, `drive.get_file`, `docs.get_document` | `tenant_id`, `drive_id` |
| S3 | `s3_read` | `s3` | `s3.list_objects`, `s3.get_object`, `s3.get_object_metadata` | `tenant_id`, `bucket` |
| http_api/CRM | `http_api_read` | `http_api` | `http_api.list_records`, `http_api.get_record` | `tenant_id` |

`connector_id` values (`conn_github_1`, `conn_linear_1`, ...) are placeholders that
reference `abac.connection_presets.id`; the tenant-side proxy resolves the real preset,
endpoint, and credentials at invocation time.

### Where `http_api`/CRM reads execute (identity mode, HAI-378)

CRM is an `http_api` connector named `crm`. There is no separate `crm` provider
to target, and nothing keys on the name. The `http_api_read` schemas do not
change: `delegated_context` is still `tenant_id`, and the base URL, allowed
paths and credential never go into binding config or tool parameters.

The tenant-side proxy executes the read. With `kei-proxy serve` in identity mode
(`KEI_CREDENTIAL_RELEASE=identity`), the daemon runs an `http_api` call from the
connector's non-secret descriptor in the v2 policy bundle (the `http_api`
registration plus a `kei://connectors/<id>/api_key` reference). It reads the
API key from the tenant secret store and injects it into the provider request.
The agent never reads the credential.

**Release status: not live yet.** It needs kei-proxy 0.2.5 or newer
(proxy-v0.2.4 and older don't have it) and the catalog's
`POLICY_BUNDLE_V2_CONNECTORS` gate enabled; the control plane emits the
descriptors only with that gate on, and it is off by default. Until then,
an `http_api`/`crm` call in identity mode denies
`credential_source_not_supported`. Runtime behavior and deny codes are in the
`kei-proxy` skill.

## Hard invariants (enforced by `validate_tool_definitions`)

Call `validate_tool_definitions(ALL_TOOL_DEFINITIONS)` to catch issues including:

- **Missing required fields** — tool definitions that omit `name`, `description`, `parameters`,
  or `permission`.
- **Invalid model formats** — tool definitions that reference an unsupported `ModelFormat` or
  whose structure doesn't match any known format.
- **Permission issues** — permission gates without ABAC conditions, or tools with
  incompatible permission/category combinations.
- **No provider credentials** — binding config keys/values that look like secrets are rejected.
- **No arbitrary URLs** — binding config keys that look like endpoints (`url`, `endpoint`,
  `base_url`, `host`, ...) and any string value containing `://` are rejected. Endpoints
  resolve from the connection preset Kei checks, never embedded.
- **No tenant IDs chosen by the agent** — a parameter that collides with a
  `delegated_context` field, or that looks like a tenant identifier (`tenant_id`,
  `account_id`, `customer_id`, `organization_id`, `org_id`), is rejected on protected
  connector read tools.
- **No direct provider calls** — protected connector read tools (a `*_read` permission with
  a binding) must not declare a `handler`; execution is delegated to the tenant-side proxy.
  They must also declare a `service`.
- **delegated_context misconfigurations** — fields listed in `delegated_context` that collide
  with tool parameter names, or that are missing from the connector's schema.

## Policy and permissions

`src/agents/policy.py`:

- `AuthorizationResult` — `ALLOW`, `DENY`, `REQUIRE_APPROVAL` (retained for compatibility; per ADR-027, per-call approval is removed).
- `PolicyDecision` — result + reason + required_permission + metadata.
- `PermissionContext` — user_id, permissions set, roles set, approval_context (retained for compatibility; see ADR-027 for the current approval model);
  `has_permission`/`add_permission`/`remove_permission`.
- `PolicyEngine` — `evaluate(tool, context)` (default: allow iff the context holds the
  tool's permission, else deny); `register_policy(tool_name, fn)` for custom policies;
  `evaluate_many`.
- `create_user_context(user_id, permission_names, roles)`, `check_tool_access`,
  `filter_accessible_tools`, `get_policy_engine`/`set_policy_engine`.

## Validation commands

```bash
# In a checkout of the kei-agents repo:
pip install -e ".[dev]"

# Tests, lint, typecheck (from README.md):
pytest
ruff check .
mypy src/agents

# Validate all tool definitions against the hard invariants:
python -c "from agents import validate_tool_definitions, ALL_TOOL_DEFINITIONS; print(validate_tool_definitions(ALL_TOOL_DEFINITIONS))"
```

## Realistic usage boundaries

- **Do not** add provider clients or credential resolution to this repository. It is a
  docs-only repo; that is a hard rule in `AGENTS.md`.
- **Do not** invent tool schemas or permissions that are not in `src/agents/`. The code
  wins over any description here.
- **Do not** add write capabilities to protected connector schemas. Reads are the only
  connector capabilities; GitHub/Linear writes are agent action tools executed by the
  agent harness, not ABAC connector capabilities.
- **Do not** let an agent supply `delegated_context` fields or tenant identifiers as tool
  parameters; that is a validation failure.
- **Do not** embed endpoints, credentials, or arbitrary URLs in binding config.
- `connector_id` values are placeholders referencing `abac.connection_presets.id`; do not
  treat them as real connector identifiers.
- The Python package is not on public PyPI (publication deferred, D-008); install
  from the internal CodeArtifact index (see Install) or from a checkout of the
  kei-agents repo.
