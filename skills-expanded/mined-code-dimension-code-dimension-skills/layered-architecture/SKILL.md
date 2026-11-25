---
name: layered-architecture
description: Decide capability-first placement and boundaries in Nx workspaces before creating or moving code. Use for app-local versus extracted capabilities, independent or shared resources, ownership and tags, or capability internals.
metadata:
  author: code-dimension
  version: 1.0
---

# Layered Architecture

Use this skill as the single front door for repository placement. It decides the owning app or project and its architectural boundary; it does not prescribe framework APIs.

This package contains the placement rules needed to use it independently. Respect local instructions and approved architecture decisions when present; no particular instruction file, specification system, or companion skill is required. Inspect the workspace's existing project roots and conventions before choosing a path. Preserve them unless a topology migration is explicitly approved; the `projects/...` paths below are defaults only when no convention exists.

Load only the reference that matches the unresolved decision:

| Question                                                           | Reference                                                              |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| App-local workflow, extracted capability, or independent resource? | [App-local or capability](references/app-local-or-capability.md)       |
| Domain-owned, platform-shared, or cross-platform shared?           | [Shared resource placement](references/shared-resource-placement.md)   |
| Which canonical platform, type, and scope tags?                    | [Nx boundary tags](references/nx-boundary-tags.md)                     |
| How to organize slices, ports, and platform composition?           | [Internal folder boundaries](references/internal-folder-boundaries.md) |

## Canonical Internal Responsibilities

Materialize only responsibilities selected by an approved boundary. `feature` owns use cases, workflow coordination, and cohesive workflow resources. `data-access` owns database, filesystem, external gateways, remote state, and integrations. `domain` owns pure rules, contracts, constants, and deterministic transformations. `ui` is frontend-only. Optional app-local `runtime` validates execution configuration and composes bootstrap, transports, routes, and capability-module imports.

Backend direction:

| Source        | Allowed targets                    |
| ------------- | ---------------------------------- |
| `runtime`     | `feature`, `data-access`, `domain` |
| `feature`     | `data-access`, `domain`            |
| `data-access` | `domain`                           |
| `domain`      | none                               |

Frontend direction:

| Source        | Allowed targets                          |
| ------------- | ---------------------------------------- |
| `runtime`     | `feature`, `data-access`, `ui`, `domain` |
| `feature`     | `data-access`, `ui`, `domain`            |
| `data-access` | `domain`                                 |
| `ui`          | `domain`                                 |
| `domain`      | none                                     |

Use direct imports from `feature` to concrete `data-access` services or repositories by default. Before introducing a port or composing capability providers, read [ports and composition](references/internal-folder-boundaries.md#ports-and-composition).

## Hard Approval Gate

Evidence informs a recommendation; it never authorizes an undecided boundary. Before writing, stop and ask the user to choose when the task requires an unapproved decision about:

- app-local versus extracted capability placement;
- an independent layer or resource project;
- a new ownership scope not already represented in the workspace;
- `scope:shared`, platform ownership, or cross-platform placement;
- an internal responsibility split for which content/import analysis leaves at least two materially valid cohesive divisions;
- a dependency across capability boundaries; or
- consolidation of existing projects or contracts.

Present the relevant graph, consumers, imports, lifecycle, and conflict evidence; concrete alternatives; a recommendation; and the impact of each option. An explicit choice in the current request or an approved proposal, design, specification, or decision record satisfies the gate. Reuse it and do not ask again. The single-consumer app-local default does not itself require a new approval; an unresolved competing boundary does.

## Decision Flow

1. Identify the owning business scope, platform, runtime consumer, and cohesive capability or resource. Inspect existing project tags and reuse an existing ownership when it fits; if the proposed ownership is new, stop and ask the user to confirm its creation.
2. Keep top-level runtime composition in the owning app. Backend controllers, guards, pipes, middleware, bootstrap, and route composition are backend app runtime responsibilities.
3. Keep a cohesive single-consumer workflow app-local when no independent boundary is approved.
4. When an independent workflow boundary is approved, extract the whole vertical workflow as one `type:capability` project in the established library root (default: `projects/<platform>/libs/<scope>/<capability>`) and expose one curated public API.
5. Consider a separate `type:domain`, `type:data-access`, `type:ui`, or `type:utility` project only when its purpose, ownership, lifecycle, and reuse are approved independently of one capability.
6. Keep same-domain reuse under `scope:<domain>`. Use `scope:shared` only for an approved owner-neutral cross-domain resource. Use the cross-platform area (default: `projects/shared/...`) only for approved runtime-agnostic code that serves frontend and backend.
7. Materialize only the responsibility areas the approved behavior needs. Never generate every known folder for symmetry.
8. Every new library and approved migration must complete [content-driven re-slicing](references/internal-folder-boundaries.md#re-slice-populated-content) after scaffolded or copied content exists and before completion.
9. Verify resolved project tags, effective boundary configuration, internal import direction, and external public-API consumers using the [boundary validation procedure](references/nx-boundary-tags.md#validate-the-boundary).

For every approved canonical project, use exactly one platform, one type, and one scope tag. Do not add a separate architecture or migration marker. Unless separately approved, keep it internal, non-buildable, and non-publishable. External consumers use only its curated root entrypoint; do not expose internals merely to satisfy an import.

Every populated `domain`, `feature`, `data-access`, `ui`, or `runtime` responsibility contains named cohesive slices; no implementation, test, or template file remains directly in the responsibility root.

## Technology Routing

This skill stops at frontend, backend, or cross-platform responsibility placement. For framework and library APIs, consult current technology documentation or specialized guidance available in the workspace. Local instructions apply when present; no external context file or installed skill is a prerequisite for deciding placement.

Do not expand an approved boundary change to adjacent projects, contracts, or
public APIs.
