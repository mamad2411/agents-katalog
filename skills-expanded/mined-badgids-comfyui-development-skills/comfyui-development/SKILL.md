---
name: comfyui-development
description: Use for any task that creates, modifies, debugs, validates, tests, packages, publishes, or reviews ComfyUI code, custom nodes, frontend extensions, workflows, subgraphs, API clients, SDK integrations, CI, or performance behavior. This root skill routes the task to focused specialist skills and requires live or version-matched verification before volatile ComfyUI details are treated as current.
metadata:
  version: "00.01.11"
---
# ComfyUI Development

This is the root router for ComfyUI development work.

ComfyUI changes quickly. Treat remembered implementation details as hints, not authority. The durable knowledge in this pack is where to find truth, how to resolve conflicting sources, how to identify the compatibility target, and how to validate the result.

## Core rule

Never rely on remembered ComfyUI implementation details when they can be verified from the target installation, a version-matched checkout, or current official Comfy-Org sources. Treat the entire `Comfy-Org` GitHub organization as the canonical upstream discovery namespace.

Safe to retain as durable knowledge:

- official source locations and their roles;
- source precedence and conflict-resolution rules;
- discovery procedures;
- validation procedures;
- task-routing rules;
- general engineering principles that do not depend on a particular ComfyUI release.

Volatile facts that must be verified before use:

- node schemas, inputs, outputs, widgets, datatypes, and enum values;
- workflow schema versions and fields;
- frontend extension hooks and frontend internals;
- server routes, payload formats, WebSocket messages, and SDK surfaces;
- `comfy_api` versions and imports;
- CLI command spelling and flags;
- packaging and registry metadata requirements;
- internal module paths, classes, function signatures, and behavior;
- supported models, loaders, filenames, and custom-node interfaces.

## First decision: identify the compatibility target

Before coding, determine which target applies. Do not silently substitute current upstream for a local or pinned target.

1. **Target installation**: the user's running/local ComfyUI and installed custom nodes are the compatibility target.
2. **Pinned target**: a named tag, release, branch, commit, dependency range, or repository lockfile is the target.
3. **Project range**: the project declares a supported ComfyUI range and changes must preserve that range.
4. **Current upstream**: the user explicitly wants current ComfyUI behavior or no older target exists and the task is forward development.

Read `references/compatibility-policy.md` when the target is not trivial.

## Source order

Read `references/authority-policy.md` before resolving a source conflict and `references/upstream-discovery.md` when choosing or discovering an official upstream repository.

Short version:

- Check `references/sources.json` for a matching machine route. For current-upstream work, follow `superseded_by` when a route is marked `superseded`; do not promote historical/archived routes over their current replacement.
- For **what runs on this installation**, the live installation wins.
- For **how a pinned/local version is implemented**, that version's source wins.
- For **current supported public behavior**, current official docs plus corresponding current source are primary.
- For **frontend implementation**, use the official frontend repository and current frontend docs.
- For **future or proposed architecture**, RFCs are evidence of proposals, not shipped behavior.
- Official examples and templates show patterns, but do not override schemas, runtime introspection, or implementation source.
- Community code is supplementary evidence only unless the task is specifically about that project.

## Route the task

Read only the specialist skill or skills needed for the task.

| Task | Specialist skill |
|---|---|
| ComfyUI core, execution, server, internals | `comfyui-core-runtime` |
| Python custom node or node pack | `comfyui-custom-node-backend` |
| JS/TS frontend extension, widget, UI behavior | `comfyui-frontend-extension` |
| Create or edit a workflow | `comfyui-workflows` |
| Diagnose or validate a workflow | `comfyui-workflow-validation` |
| REST/WebSocket/API client, SDK, MCP, proxy | `comfyui-api-and-sdk` |
| Tests, QA, CI | `comfyui-testing-and-qa` |
| Package, publish, Registry, Manager | `comfyui-packaging-and-registry` |
| Subgraphs or blueprint work | `comfyui-subgraphs` |
| Benchmarking, kernels, performance | `comfyui-performance` |
| Upstream contribution, RFC-adjacent work | `comfyui-upstream-development` |
| Explicitly requested maintenance of this pack's upstream snapshot/source routing | `comfyui-self-maintenance` |

Activate specialist skills through the harness's normal skill mechanism. Do not traverse outside this skill directory to read sibling `SKILL.md` files. If a harness cannot activate another skill from an active skill, start with the specialist skill directly from the harness's discovered skill list.

Never activate `comfyui-self-maintenance` during ordinary development simply because a new repo or feature is discovered. Ordinary discovery stays read-only. Use self-maintenance only when the current user explicitly asks the pack to maintain its own routing or upstream snapshot.

A `specialist` field learned through explicit self-maintenance is a routing hint to an existing skill. Use it when it matches the actual task, but do not let it override a more specific task classification or the compatibility target.

For work crossing boundaries, load the minimum combination. Example: a custom node with a frontend widget normally needs `custom-node-backend` plus `frontend-extension`, then `testing-and-qa` before completion.

## Mandatory discovery behavior

Before using a volatile ComfyUI fact:

1. Prefer the target checkout or running target if available.
2. Check `references/sources.json` for a matching route, its `status`, any `superseded_by` authority move, and any `specialist` hint.
3. Use `references/source-map.md` as the curated human guide for common repositories.
4. If neither map clearly covers the task, search the entire current `Comfy-Org` organization for the repository that owns the behavior.
5. Read the surrounding implementation, not just a search-result snippet.
6. If documentation and implementation disagree, determine whether they refer to different versions.
7. Record enough provenance to explain what was checked: repository/path and, when relevant, commit or installed version.

Use `references/search-recipes.md` for practical search patterns. When the task uses Comfy-Org agent tooling, `comfy-cli`, or an upstream repository's own agent instructions, read `references/official-agent-guidance.md`. Do not vendor or blindly merge upstream prompt/skill files into this package.

## Live runtime discovery

When the task concerns a particular running ComfyUI installation, query the running server rather than assuming its node catalog.

The helper scripts in `scripts/` can probe a local or remote target without third-party Python dependencies:

- `discover_comfy_org.py`
- `inspect_comfy_environment.py`
- `inspect_object_info.py`
- `validate_workflow.py`
- `source_freshness.py`
- `self_maintain.py`
- `maintenance_boundary.py`

The scripts probe documented/current endpoints with fallbacks rather than treating one URL shape as permanent. `self_maintain.py scan` is read-only. Its `apply --yes` mode is reserved for explicitly requested normal self-maintenance and may modify only `references/sources.json` and `references/upstream-snapshot.json`. If maintenance discovers that broader skill knowledge is required, activate `comfyui-self-maintenance` and present its four explicit boundary choices. `maintenance_boundary.py` validates any user-authorized local skill-only plan, records local divergence, and prepares maintainer Issue drafts without filing them.

Do not assume a custom node exists because it exists online. Do not assume its installed version matches upstream.

## No fabrication rules

Never invent any of the following to make a solution look complete:

- node class names;
- input or output sockets;
- widget order;
- model filenames;
- schema fields;
- frontend hooks;
- API routes;
- CLI options;
- Registry metadata;
- package versions.

If authoritative discovery is unavailable, state exactly what remains unverified and keep the result clearly provisional.

## Modification rules

When editing an existing project:

- preserve existing filenames and paths unless the task requires changing them;
- preserve compatibility behavior unless the task explicitly changes it;
- do not modernize unrelated code merely because a newer API exists;
- do not migrate V1 nodes to V3 unless migration is requested or necessary for the actual target;
- do not downgrade a V3 implementation to V1 simply because V1 is familiar;
- keep changes scoped and inspect the surrounding project conventions first.

## Validation gate

Do not declare ComfyUI code or a workflow correct solely because it is syntactically plausible.

Use the strongest validation available for the task:

- syntax/static checks;
- current schema validation;
- import/load checks;
- live node registration inspection;
- frontend build/type checks;
- unit tests;
- workflow preflight against live node definitions;
- representative integration workflow;
- official QA/test tools where appropriate.

A validation tool failing to run is **not** a passing result. Report it as an unverified gate.

## Completion receipt

Before finishing a substantial task, be able to answer internally:

```text
Compatibility target:
Target commit/version discovered:
Running server inspected:
Live node catalog inspected:
Official docs consulted:
Core source consulted:
Frontend source consulted:
Examples/templates consulted:
Validation performed:
Remaining uncertainty:
```

Do not dump this receipt mechanically to the user. Use it to prevent unsupported claims and surface only the parts that matter.

## Source registry

`references/sources.json` is the machine-readable **curated routing registry** of high-value official repositories known to this pack. It is not an exhaustive allowlist. Optional `status`, `superseded_by`, and `specialist` fields record authority moves without erasing historical compatibility context.

`references/upstream-snapshot.json` is a baseline of the public `Comfy-Org` repository universe used only to detect upstream changes during explicitly requested self-maintenance. It is not authority by itself.

`references/source-map.md` explains which repositories answer which kinds of questions, and `references/upstream-discovery.md` defines how to discover and classify any other current repository under `Comfy-Org`.

The authoritative upstream search universe is the entire `Comfy-Org` organization. Discover newly relevant official repositories whenever necessary; absence from `sources.json` does not make an official repository ineligible.

## Acceptance gate

Before calling ComfyUI work complete:

- identify the compatibility target;
- use the specialist skill or source set that owns the task;
- verify volatile ComfyUI facts from the target or current/version-matched official sources;
- run the strongest practical validation for the change;
- report any validation step that could not be run;
- do not invent nodes, sockets, hooks, routes, schemas, CLI flags, model names, or package requirements.

