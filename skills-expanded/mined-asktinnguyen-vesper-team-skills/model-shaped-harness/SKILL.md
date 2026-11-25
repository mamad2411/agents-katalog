---
name: model-shaped-harness
description: Optimize agent tool mounting and execution surfaces to reduce token overhead. Use when consolidating large tool catalogs, introducing code mode, defining mount profiles, or shaping a model-facing harness in Vesper or similar agent apps.
---

# Model-Shaped Harness

Design the model-facing tool harness around what the model actually needs per turn, not around how many internal services happen to exist.

Treat prompt mass as architecture.

## Before You Start

Collect these inputs before changing the harness:

- one or two representative turns that currently feel expensive
- the current mounted tool/server surface for those turns
- a measurement method for prompt/tool mass
- provider/runtime context for the target model path
- the relevant app files or architecture docs for the affected mounting path

Measurement method hierarchy:

1. Use runtime telemetry if the app already records tool counts, deferred tool tokens, or request usage.
2. If telemetry is missing, estimate schema mass from serialized tool definitions or prompt-prefix snapshots.
3. If token estimation is unavailable, fall back to mounted tool count, mounted server count, and duplicated surface count.

Always report which method was used.

## When To Use

Use this skill when:
- reducing token overhead from large MCP or tool catalogs
- introducing or refining code mode, typed execution, or batched tool execution
- replacing eager tool mounting with profile-driven mounting
- removing duplicate capability exposure across built-in tools and source servers
- designing a reusable model-facing harness for Vesper or another agent application
- deciding which capabilities belong in a compact executor versus standalone interactive tools

## Relationship To Other Skills

Use `agent-native-architecture` for parity-by-design, shared core logic, and broader agent-product philosophy.

Use `mcp-builder` for MCP server and tool-contract design.

Use this skill when the main problem is mounted-surface optimization: executor consolidation, progressive discovery, cache-stable prefixes, and profile-based harness shaping.

## Quick Example

Example request:

- “Reduce tool bloat in Vesper’s code-mode path.”

Expected approach:

1. Capture before metrics for one default turn and one minimal turn.
2. Identify duplicated surfaces and broad eager mounts.
3. Classify tools into executor, standalone, or escalation-required paths.
4. Propose one compact executor path plus explicit mount profiles.
5. Verify lower mounted-surface cost without losing required capability.

## Core Thesis

Prefer a three-phase optimization loop:

1. Deduplicate overlapping capability surfaces.
2. Replace giant static schema dumps with runtime discovery.
3. Mount tools and sources through explicit profiles instead of eager defaults.

The goal is not to hide capability. The goal is to keep full capability while only paying detailed prompt cost when the model actually needs it.

## Required Output

Produce an artifact with these fields:

- `baseline_metrics`
- `measurement_method`
- `duplicate_surfaces_found`
- `tool_classification_summary`
- `executor_or_pack_changes`
- `mount_profiles`
- `files_or_layers_to_edit`
- `verification_evidence`
- `open_questions_or_unverified_assumptions`

## Default Workflow

1. Measure current prompt cost.
   Record tool count, deferred tool tokens when available, and which servers contribute most schema mass.
   State the measurement method used.
2. Map overlapping surfaces.
   Find capabilities exposed twice, especially when code mode and standalone sources both expose the same family.
3. Split tools by execution shape.
   Keep deterministic CRUD, search, config, and orchestration status operations code-eligible.
   Keep UI pauses, OAuth handshakes, human judgment, and blocking dialogs as traditional tools.
4. Collapse code-eligible tools behind one executor.
   Give the model one obvious execution entrypoint instead of dozens of sibling tools.
5. Add progressive discovery helpers.
   Expose lightweight catalog helpers such as `tool_catalog_list` and `tool_catalog_get` so exact schema is fetched only when needed.
6. Add mount profiles.
   Make turn-level mounting explicit with profiles such as `default`, `schedule_minimal`, or app-specific variants.
7. Normalize auto-mounted sources.
   Strip duplicate sources when the executor already covers that capability, and emit sync events so the UI reflects the effective source set.
8. Re-measure and document.
   Compare before/after token mass and record the architecture rule so future features do not reintroduce eager bloat.

## Tool Classification Rubric

| Case | Default decision |
|------|------------------|
| Deterministic CRUD/search/config/status call with typed params | Keep in executor |
| Human approval, UI pause, OAuth, credential acquisition | Keep standalone |
| Broad tool family where exact method is rarely needed up front | Keep behind deferred discovery or pack |
| Side-effectful mutation with simple typed params and retry-safe behavior | Usually executor, but document timeout/retry risk |
| Side-effectful flow with partial completion risk or hidden external state | Needs explicit retry guidance or escalation |
| Provider- or permission-sensitive flow with unclear runtime guarantees | Escalate before bundling |

## Design Rules

- Prefer one compact model-facing executor for code-eligible capability.
- Keep exact argument discovery on demand, not embedded up front.
- Mount nothing by accident. Make profiles shared, typed, and centrally resolved.
- Preserve parity-by-design. Human and agent paths should still use the same core service logic.
- Keep the executor safe to retry. Surface timeout guidance, completed calls, and side-effect warnings.
- Give the model a direct path. If one tool is the intended entrypoint, state that clearly in system instructions.
- Optimize the model interface, not just the internal API graph.

## Code Mode Guidance

Use code mode to help the model:

- batch multiple data operations into one tool call
- avoid repeated tool-call/tool-result round trips
- discover exact schemas only when needed
- centralize timeout, logging, and execution safeguards
- keep broad capability available without mounting dozens of separate tools

Do not force interactive workflows into code mode. Leave `ask_user`, `render_ui`, OAuth, and other pause-or-judgment flows as standalone tools.

## Progressive Tool Mounting

Treat mounting as a product surface, not a side effect.

- Define a typed mount-profile resolver.
- Let each profile decide whether to include session tools, code mode, built-in servers, workspace sources, and all-sources context.
- Clear stale source state for minimal profiles instead of inheriting previously mounted servers.
- Keep minimal automation profiles deterministic and cheap.

## Reference Routing

Load `references/model-shaped-harness-patterns.md` by subtask:

- measurement and validation -> `Measurement Guidance` and `Verification Checklist`
- executor design -> `Compact Executor With Progressive Discovery`
- mounting policy -> `Progressive Tool Mounting`
- prompt/cache behavior -> `System Prompt And Tool Routing`
- implementation sequencing -> `Integration Sequence`
- failure handling -> `Troubleshooting And Recovery`
- Vesper-specific wiring -> `Vesper Implementation Map`

Load `references/openai-focus-harness.md` only when the target provider is OpenAI-family or OpenAI-compatible. Treat it as a freshness-sensitive provider appendix, not a provider-agnostic default. Re-verify doc-sensitive claims before implementation.

Use `references/openai-focus-harness.md` for:
- Responses-native OpenAI harness guidance
- Codex-shaped versus general-model versus mini-model mounting
- provider-contract detection and fallback strategy
- prompt caching, strict schemas, deferred loading, and compaction notes

If working in Vesper, jump to `Vesper Implementation Map` in `references/model-shaped-harness-patterns.md`.

## Anti-Patterns

Avoid:
- exposing the same capability through code mode and standalone sources at the same time
- embedding the full schema of every possible tool in the executor description
- letting "minimal" turns inherit old mounts
- forcing the model to discover the intended primary tool through ToolSearch every turn
- treating token cost as prompt-copy trivia instead of interface design
- building a harness around backend module boundaries instead of model reasoning patterns

## Done Criteria

The harness is moving in the right direction when the implementation report includes:

- before/after measurements for at least two representative turns
- the measurement method and any estimation fallback used
- a clear executor/standalone/escalation classification for changed surfaces
- a mount-profile matrix showing what is included for each affected profile
- one retained-capability proof via deferred discovery or executor use
- evidence that duplicate or stale mounts were removed or intentionally preserved
- any unverified provider assumptions called out explicitly

## Verification Checklist

Verify these before considering the work complete:

1. Replay at least one common turn and one minimal turn.
2. Confirm mounted surface reduction or improved schema mass for the target path.
3. Confirm no required capability was lost.
4. Confirm stale source state is not inherited where the profile should be minimal.
5. Confirm timeout/retry behavior is documented for any long-running executor path.
6. Record remaining unknowns instead of silently assuming provider/runtime support.

## Troubleshooting Trigger

If the work uncovers stale mounts, partial side effects, tool-catalog drift, provider-contract ambiguity, or UI/source desync, load `Troubleshooting And Recovery` in `references/model-shaped-harness-patterns.md` before continuing.
