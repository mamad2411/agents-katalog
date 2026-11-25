---
name: ghpython-component-workflow
description: Develop Rhino 8 Grasshopper Python 3 components with external-source loaders and typed ports; deliver GHA or ghuser, build companion Rhino parameter panels, and produce four-view geometry review montages. Legacy capture script disabled pending native-Zoom validation. Excludes GH canvas interaction extensions.
---

# Grasshopper Python Component Workflow

Keep implementation in a stable workspace `.py`; paste its small loader into GH once. AI edits the file, and a GH recompute reads it again. Automatically configure **every input and output**: name, description, Item/List/Tree access and an appropriate type hint; inputs also declare Optional. This skill is self-contained; the author's paths, project rules and MCP setup are not prerequisites.

Companion Rhino parameter panels and direct GHA library delivery are conditional routes below. GH canvas interaction plugins (snapping, dragging, mouse hooks and editor menus) are outside this skill. For panel-only work, use the panel reference directly; Python loader generation and component port setup are not prerequisites.

## Policy and task boundaries

This skill owns reusable implementation methods, not workspace permissions or project release policy. Read the project entry point once, then only the relevant references. Keep project-specific exceptions, defaults, component counts and installation paths in their authoritative project sources; link instead of copying them into this skill.

Separate behavior development/acceptance from mechanical packaging, installation and live-canvas migration. Packaging starts from accepted sources; merge live edits only when the task actually includes accepted canvas changes. Do not make a canvas or a full historical audit a prerequisite for a source-only release. Never use this distinction to skip applicable final-artifact checks.

Run deterministic checks as scripts, retain full evidence on disk and report a bounded summary. Reuse a passed result only for the same artifact/input identity and scope. Changed identity, failure or an unresolved issue requires revalidation. For cross-agent releases send an artifact-bound task packet; use a fresh task context when supported, without claiming that editing instructions clears existing conversation history.

## Read only what the task needs

| Task | Read / run |
| --- | --- |
| First component or unfamiliar setup | [quickstart.md](references/quickstart.md); run `scripts/create_component.py` |
| New ports, type changes or loader setup | [loader-and-ports.md](references/loader-and-ports.md); consult [type-hints.md](references/type-hints.md) for relevant types |
| Algorithm-only edit | Component header, specs and target function; reuse known infrastructure |
| Trees or diagnostic failures | [data-and-debug.md](references/data-and-debug.md), [troubleshooting.md](references/troubleshooting.md) as needed |
| Runtime/API, geometry or substantial edits | Relevant section of [development.md](references/development.md) |
| Shared helper changes, backups or release maintenance | Relevant section of [maintenance.md](references/maintenance.md) |
| Validation or delivery choice | [validation.md](references/validation.md); choose the requested artifact below |
| Rhino geometry four-view review montage | [fourview-capture.md](references/fourview-capture.md); legacy capture script is disabled pending a compliant native-Zoom implementation |
| Direct compiled component library (.gha), including companion input placement/alignment | [compiled-gha.md](references/compiled-gha.md); no intermediate ghuser required |
| Repeated GHA releases: orchestrating build, diff evidence, acceptance record, KRL safety gate | [release-pipeline.md](references/release-pipeline.md); run `scripts/release-pipeline/package.py --config <pipeline.json>` |
| Authorized script-only update of saved GHA canvas instances | [canvas-upgrade.md](references/canvas-upgrade.md); run `scripts/upgrade_canvas.py` inside the existing Rhino: plan, then apply; summaries only |
| Requested User Objects (.ghuser) | [packaging-mcp.md](references/packaging-mcp.md) |
| Companion Rhino parameter panel; Framework/Core compatibility | [rhino-panels.md](references/rhino-panels.md) |
| Whole workflow, library delivery or file reorganization | [workflow-and-artifacts.md](references/workflow-and-artifacts.md) |
| Custom component icons | Source-backed function/geometry brief in [icons.md](references/icons.md), then use `oil-icon` for artwork |
| Icon-only ghuser updates | [packaging-mcp.md](references/packaging-mcp.md#icon-embedding-and-icon-only-updates) |

Do not load all references, tests, READMEs or templates each turn. Use the generator to copy tested infrastructure instead of reproducing it in chat. Inspect that infrastructure when changing it or diagnosing it. Reuse recorded runtime, source path and hint catalog; do not re-enumerate types or browse unchanged APIs for every component. Prefer bounded Debug summaries and focused tests. Read additional material when a failure or uncertainty requires it; token savings must not hide unverified behavior.

## Essential workflow

1. Follow applicable project instructions. Inspect an existing component's header/specs and preserve agreed behavior. For a new workspace, use `project-control.md` and `tests/<workflow>/`; the [control template](assets/project-control-template.md) records only environment, paths, interface decisions and verification state. Keep existing project layouts.
2. Confirm Rhino 8 Python 3 versus legacy IronPython, a usable helper interpreter, and whether Rhino can read the **same current source file**. Remote/container paths require explicit Rhino-side mapping or synchronization. A running Rhino does not prove an MCP connection. MCP is optional; provide manual steps when unavailable or declined.
3. Generate a standalone source plus loader with `scripts/create_component.py <source.py> --example curve-divide` (or `tree`). Keep the generated helpers; change the usage header, specs and algorithm. The example body alone is not a complete component. Preserve recoverable originals before edits; do not overwrite an accepted release.
4. Match type hints deliberately on both sides. Prefer Curve, Point3d, number, integer, bool, etc. when the contract requires those types; use object for genuinely mixed/custom data. Never silently fall back to object because a requested hint failed. The starter accepts aliases or explicit CLR types and verifies selection before changing ports. Legacy four-field outputs remain accepted as object; new outputs have five fields including Hint.
5. Schedule port changes outside the current solve, discard superseded callbacks and preserve compatible parameter identities, wires and persistent values. Revisions/messages alone do not rebuild ports. Wait for configuration and the following solve before evaluating output. Required/invalid old inputs can prevent the loader from executing; resolve that blocking input or use a fresh component.
6. Verify unfamiliar API signatures against installed XML or official Rhino documentation. Preserve meaningful tree paths and empty branches, distinguish geometry from display samples, and declare units/tolerance where relevant. Keep complete component usage in its source header, not a separate per-component manual.
7. Run checks relevant to the change. Use current Debug/source identity for fragile or repeatedly failing components. Distinguish offline tests, real Rhino geometry, live GH ports and save/reopen checks. If live access is unavailable, deliver the useful source and concrete manual acceptance steps; do not imply live verification.
8. For authorized delivery, follow the [stage and artifact map](references/workflow-and-artifacts.md): accepted behavior → standalone source → requested language/icon preparation → format-specific build/serialization and final-artifact readback → manifest-based archive → authorized installation → batch archive. Preserve a baseline for bounded updates and report each stage's actual evidence. Keep current releases, reusable tooling/design masters and historical experiments separate without breaking development loaders.

## Chinese-version language contract

When delivering a Chinese version, use Chinese for the component's displayed name, functional description, input/output descriptions, and source usage header. Adapt wording to accepted user terminology rather than literal translation. Complex components may need multiple sentences or paragraphs. Component help, port help and footer messages have separate roles; none substitutes for the others. Read the field-by-field table in [presentation-and-parity.md](references/presentation-and-parity.md) when localizing or packaging.

Keep the remaining interface and implementation in English: port names/nicknames, custom configuration surface fields, code identifiers and ordinary code comments, categories/subcategories unless the project explicitly overrides them, protocol keys, API/type names and technical tokens. Normalize field shorthand to established PascalCase, such as ToolBaseSetup. Preserve identifiers and data contracts. The skill and reusable templates remain English.

For GHA packaging or recovery into sources, read [presentation-and-parity.md](references/presentation-and-parity.md). Keep accepted metadata and prose in authoritative development sources or a shared source-owned schema, and derive loaders, wrappers and manifests from that contract. Packaging must not independently regenerate descriptions. Verify loader and compiled instances after complete host solutions; initialization-only metadata checks are insufficient.

Distinguish authored diagnostics from GH/Python host messages such as missing required input, conversion/type-hint failures and uncaught exception reports. Translate messages the component owns, preserving severity and useful technical details; document host-controlled text that cannot be localized at component level. Never make required inputs Optional, weaken type hints, swallow exceptions, or change failure/output semantics merely to suppress an English message. For packaged verification, follow the [language checks](references/packaging-mcp.md#verify-chinese-version-text).

## Delivery

For source/loader delivery, link the source and provide the **complete ready-to-paste loader in a fenced Python block**, with the actual Rhino-readable path substituted. A downloadable loader alone is insufficient. For later same-path edits, only remind the user to recompute; repeat the loader when requested or when its path changes. Report the result, relevant checks and remaining limits concisely; do not echo the entire source or standard workflow.

Package only when requested or already authorized, and honor the selected format. For an installable component library with no specified format, prefer direct `.gha` delivery from accepted standalone Python sources when the target host APIs are verified; do not require `.ghuser` first or rewrite working algorithms in C#. When the same library will be released more than once, drive that delivery with the [release pipeline](references/release-pipeline.md) rather than ad-hoc commands. Use `.ghuser` for an explicit User Object request. Companion Rhino parameter panels use `.rhp` and, when both Windows runtime modes are requested, a shared-source dual-target package. Follow the relevant reference, preserve connected development instances, and state actual host dependencies and runtime acceptance. Deliver the plugin/package and concise evidence; a pasteable loader is required only when delivering a development loader.
