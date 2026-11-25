---
name: agent-plugin
description: "Use for designing, creating, migrating, reviewing, validating, packaging, or implementing support for portable Agent Plugins, including plugin.json manifests, Agent Skills under skills/, MCP servers in mcp.json, reverse-domain client extensions, client conformance, compatibility layers, and plugin security boundaries. Skip ordinary application plugins or isolated skill edits that do not involve an Agent Plugin package."
---

# Agent Plugin Engineering

Use [Core Method](references/core.md) as the normative baseline. Work from evidence. Label missing evidence as an assumption.

Target Agent Plugins 1.0.0. Treat the published specification as authoritative. Examples, client formats, and local validators do not replace it.

## Classify the task

- **Author:** Create the smallest portable package. Add only required components.
- **Review:** Separate conformance, portability, security, runtime, and client compatibility.
- **Migrate:** Classify every existing artifact before you change it.
- **Implement a client:** Preserve discovery, containment, version selection, placeholder expansion, and failure isolation.

## Keep the portable core narrow

- Portable core has two component types: Agent Skills and MCP servers.
- Root `plugin.json` is required.
- `plugin.json` cannot redirect discovery or contain inline components.
- Skills are immediate child directories of `skills/` with exact `SKILL.md` files.
- Optional MCP configuration exists only at root `mcp.json`.
- MCP controls wire behavior. Agent Plugins controls package configuration.
- Hooks, agents, commands, prompts, LSP, UI, authentication declarations, and marketplace data are not portable v1 components.
- Client behavior belongs in a namespace that the client owns and documents.
- Package environment values and HTTP headers are visible data.
- Schema success does not prove every text, filesystem, runtime, or client requirement.

## Load only needed references

| Need | Reference |
|---|---|
| Complete method and output | [Core Method](references/core.md) |
| Package layout and paths | [Package Model](references/package-model.md) |
| `plugin.json` | [Manifest](references/manifest.md) |
| Agent Skills | [Skills](references/skills.md) |
| `mcp.json` | [MCP Servers](references/mcp.md) |
| Failure isolation | [Failure Boundaries](references/failure-boundaries.md) |
| Client extensions | [Client Extensions](references/client-extensions.md) |
| Migration | [Migration](references/migration.md) |
| Client implementation | [Client Implementation](references/client-implementation.md) |
| Security | [Security and Supply Chain](references/security-and-supply-chain.md) |
| Testing | [Testing and Evaluation](references/testing-and-evaluation.md) |
| Client support | [Client Compatibility](references/client-compatibility.md) |
| Sources and versions | [Research Notes](references/research-notes.md) |

## Optional local tools

Run `uv sync --frozen` once. The project requires Python 3.11 or later.

- Preview a plugin: `uv run python scripts/new_plugin.py example-plugin --skill-name example-task`. Add `--write` to create it.
- Validate a plugin: `uv run python scripts/validate_plugin.py PATH`
- Write a JSON report: Add `--json`.
- Package a plugin: `uv run python scripts/package_plugin.py PATH`
- Validate this skill: `uv run python scripts/validate_skill.py . --source-checkout`
- Package this skill: `uv run python scripts/package_skill.py . --output ../agent-plugin.zip`

The project pins the official Agent Skills `skills-ref` package. Initial dependency installation requires network access. Validation and packaging make no network requests.

## Scope and output

This skill supplies portable package guidance and local tools. It does not own session coordination or client-specific behavior.

Use an asset only when the user requests it or the repository requires it. Follow the location and naming conventions of the repository.

State the Agent Plugins version and target clients. Classify all non-core artifacts.

List changed files. Separate conformance errors from warnings and local project policy.

Report exact validation and smoke-test evidence. Name all remaining security and compatibility risks.

Do not claim execution, client support, sandboxing, signing, or trust guarantees without direct evidence.
