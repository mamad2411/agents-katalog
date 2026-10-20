---
name: conventions
description: Read Polymath marketplace conventions — naming, token budget, component choice, conformance gates, commit style — when authoring or reviewing a plugin.
---

# conventions

> Marketplace-wide conventions that apply across plugins. Load this when a task touches plugin authoring, marketplace structure, or the contribution flow.

## When to use

- A task creates or edits a plugin, skill, command, agent, hook, workflow, or connector.
- A workflow step needs to ground itself in marketplace standards.
- A contributor is being onboarded to the marketplace.

## Component choice (decide this first)

| Need | Component |
| --- | --- |
| Event-driven gate (block secrets, format on save, push reminder) | Hook |
| External service tool calls (GitHub, Jira, Datadog, …) | MCP server (connector plugin) |
| Repeating procedure with templates/scripts/references | Skill |
| Frequent direct entry point | Command (thin alias → skill) |
| ≥ 2 skills chained with data dependencies or gates | Workflow |
| Forked-context deep audit, panel, or research | Agent |

Default to **skill-only**: a command earns its place only when it is a frequent direct entry point; a workflow only when it composes skills. Command and agent descriptions count against the per-plugin budget, so a thin shim is not free.

## Naming

- Plugins: `polymath-<bare-name>` (kebab-case).
- Skills/commands: bare file names; invocation is namespaced (`/polymath-product:prd`).
- Agents: nouns-of-people (`security-reviewer`, `pm-critic`).
- Templates: PascalCase artifact names (`PRD.md`, `ADR.md`).
- Workflows: camelCase (`shipFeature.yaml`).
- Routing sidecars: `routing.yaml` beside `SKILL.md`; workflows declare theirs in `plugins/polymath-flows/routing/<name>.yaml`.

## Token budget

- Per-plugin always-on listing ≤ 400 tokens (only `name` + `description` of skills/commands/agents are measured).
- Catalog-wide measured total ≤ 1,000 tokens.
- Descriptions ≤ 200 chars; front-load the trigger phrase and end with a scope boundary where a sibling could be confused.
- SKILL.md body ≤ 500 lines; overflow goes to `references/`.

## Declaration discipline

Routing is **declare-or-exempt**: every surface either ships a `routing.yaml` (validated against `registry/schemas/surface-routing.schema.json`, compiled by `tools/build-surface-index.py`) or carries a reasoned entry in `registry/routing-exemptions.json`. Exemption is the normal posture for knowledge skills; declaring is the deliberate act.

## Conformance gates

`tools/conformance.sh --all` is the source of truth. `tools/validate-all.sh` runs the authoring subset. Key rules: MANIFEST-1/2/3, SKILL-1 (`description` ≤ 200, body ≤ 500), TEMPLATE-1, WORKFLOW-1/2/INDEX, SURFACE-INDEX (SURFACE-1/2, TOOL-1, TRUST-1), CAPABILITY-INDEX (BINDING-1, MCP-BINDING), MCP-PKG, INTEGRATION-1/2, DESC-1/2, AGENT-1, FIXTURE-1, DOCS-1/2. Re-run the relevant builder after editing a workflow (`build-workflow-index.py`), `routing.yaml` (`build-surface-index.py`), or a binding (`build-capability-index.py`); the gate fails on drift.

## Hooks

Hooks are deterministic gates. They never block silently — every block produces a user-visible reason. Hook scripts live in `hooks/scripts/`. In `hooks.json`, wrap the plugin-root placeholder in double quotes (so a path containing spaces cannot split the command) rather than leaving it bare.

## Workflows

- Schema: `registry/schemas/workflow.schema.json`.
- Every workflow declares `whenToUse` + unique `triggers` (WORKFLOW-2), and its routing surface is compiled into `plugins/polymath-flows/data/`.
- Resolution order for `.polymath/` files: project → user (`$POLYMATH_CONFIG_DIR`) → home.
- Enforcement: deterministic `mustPass` checks; AI cross-checks are advisory, not blocking.

## Commits & license

- Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, …); PR titles mirror the headline commit.
- CHANGELOG updated for every non-trivial change; version bumps follow the marketplace release (all plugins + `.claude-plugin/marketplace.json` together).
- MIT for all plugins — the patent grant matters for OSS plugins reused inside commercial agents.

## Quality bar

- Cites the section a rule comes from; never invents a convention the gates do not enforce.
- Names the exact gate ID (e.g. `SKILL-1`, `MCP-BINDING`) when pointing at a rule.
- Never restates a whole sibling doc (budget policy, workflow schema) — points at `docs/` instead.

## Output

When loaded, return a one-paragraph summary scoped to the current task plus pointers to the relevant subsection above (e.g. "authoring a connector → Component choice + Conformance gates + Declaration discipline").

```text
Loaded conventions for: authoring a new connector plugin
→ Component choice (connector = MCP server + binding)
→ Conformance gates (INTEGRATION-1/2, MCP-PKG, MCP-BINDING, CAPABILITY-INDEX)
→ Declaration discipline (routing.yaml or an exemption entry)
```
