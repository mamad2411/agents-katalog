---
name: genai-bootstrap
description: Build compact, evidence-based project context for Codex, Claude Code, or GitHub Copilot. Use once when onboarding North Starr to an existing codebase.
---

# Bootstrap North Starr in a Project

## Outcome

Give the active coding assistant enough verified project context to work safely
without turning every task into an architecture exercise.

Create:

- a compact root instruction file for the active tool;
- machine-readable and readable project context under `.north-starr/`;
- only the narrowly scoped module guidance justified by evidence.

Do not redesign the product, choose an AI architecture, or install dependencies
during bootstrap. Use the sibling `intake`, `assess`, and
`architecture-design` skills for those decisions.

## Platform Outputs

| Platform | Root context | Optional scoped context | Skills |
|---|---|---|---|
| Codex | `AGENTS.md` | nested `AGENTS.md` only where behavior differs | provided by the plugin or `.agents/skills/` |
| Claude Code | `CLAUDE.md` | nested `CLAUDE.md` | provided by the Claude plugin |
| GitHub Copilot | `AGENTS.md` | `.github/instructions/*.instructions.md` | `.github/skills/` |

Always create:

- `.north-starr/project-context.json`
- `.north-starr/project-context.md`

If more than one tool is in use, create the adapters the user actually needs.
Do not copy all specialist agents into a project by default. The active
assistant may delegate bounded work when a later task warrants it.

## Evidence Rules

- Read before writing.
- Record a file path, command result, or existing document for every material
  claim.
- Use `confirmed_fact`, `inference`, `assumption`, or `unknown`.
- Never infer an MCP server, model, provider, SDK, database, or deployment
  environment from a product name alone.
- Preserve existing project instructions. Merge or propose a patch; do not
  overwrite custom content.
- Show no more than three important blockers at once.
- Do not put secrets, credentials, raw customer data, or private prompt content
  in generated artifacts.

## Workflow

### 1. Detect the Environment

Identify:

- repository root and relevant nested instruction files;
- active assistant and any secondary assistants the project supports;
- existing `.north-starr/`, `.plans/`, ADRs, README, and operating docs;
- working-tree changes that must be preserved.

If the platform cannot be determined, generate the universal JSON/Markdown
context and a compact `AGENTS.md`.

### 2. Inspect the Codebase

Use focused searches and configuration files to establish:

- languages and versions;
- package manager, build, test, lint, and CI commands;
- entry points and top-level modules;
- dependency direction and external boundaries;
- deployment/runtime shape;
- data stores and authoritative sources;
- model providers, AI SDKs, agent frameworks, MCP servers, and tool adapters
  actually present;
- eval, prompt, guardrail, cost, logging, tracing, and incident mechanisms;
- high-risk modules and meaningful test gaps.

Prefer manifests, lockfiles, code imports, runtime configuration, tests, and CI
over prose claims. Do not perform an exhaustive line-by-line audit when targeted
evidence answers the question.

### 3. Build the Canonical Context

Write `.north-starr/project-context.json` with:

```json
{
  "schema_version": "1.0.0",
  "artifact_type": "project_context",
  "generated_at": "<RFC3339 timestamp>",
  "project": {
    "name": "<name>",
    "root": "<path>",
    "purpose": "<one sentence or unknown>"
  },
  "commands": {
    "build": [],
    "test": [],
    "lint": [],
    "run": []
  },
  "stack": [],
  "modules": [],
  "external_systems": [],
  "ai_components": [],
  "mcp_servers": [],
  "quality_controls": [],
  "risks": [],
  "unknowns": [],
  "evidence": [],
  "source_hashes": []
}
```

Requirements:

- `stack` items identify component, version if evidenced, purpose, status, and
  evidence references.
- `external_systems` identifies owner, authority, data direction, auth if known,
  and failure behavior.
- `ai_components` separates provider SDK, portable AI SDK, agent framework,
  workflow runtime, graph runtime, prompt/eval tooling, and model identifiers.
- `mcp_servers` records server name, transport, tools/resources/prompts exposed,
  authority, scopes, side effects, approval, failure behavior, and evidence.
- `risks` contain severity, evidence, impact, and current control.
- `source_hashes` uses unique `sha256:<64 lowercase hex>` values for material
  source artifacts; paths live in the corresponding `evidence` records.
- Unknown values remain `unknown`; do not manufacture completeness.

Render the same facts in `.north-starr/project-context.md`. JSON is canonical;
Markdown is the human review view.

### 4. Generate Compact Tool Instructions

Keep the root context below 100 lines where practical. Include only:

- actual build/test/lint/run commands;
- concise architecture and module map;
- important dependency and data boundaries;
- high-consequence landmines;
- the North Starr journey for material AI work;
- references to `.north-starr/project-context.json` for detail.

For Codex, start from `../../templates/codex/AGENTS.md`. Replace placeholders with
verified project facts and merge with an existing `AGENTS.md`.

For Claude Code, start from `../../templates/CLAUDE.md`, but simplify managed policy
when the project does not require the legacy full pipeline.

For GitHub Copilot, start from `../../templates/AGENTS.md`. Generate path-scoped
instructions only for modules whose conventions genuinely differ.

Do not put an always-on Q0–Q4 questionnaire, mandatory peer-consultation mesh, or
full specialist catalogue into a new Codex project. Those controls are
available through explicit North Starr skills when the work is material.

### 5. Verify

Before completion:

- parse all generated JSON;
- validate hashes against current files;
- ensure commands are copied exactly from project sources or marked unverified;
- ensure no placeholder remains;
- ensure existing instructions and user changes were preserved;
- ensure no secret-like values were captured;
- ensure JSON and Markdown describe the same project state.

## Handoff

Report:

- files created or updated;
- platforms configured;
- verified commands;
- up to three important unknowns;
- whether the project is ready for `intake`, `assess`, or direct ordinary
  implementation.

Do not start architecture design automatically.
