---
name: pi-typescript-extension-engineering
description: Engineer, review, debug, and harden TypeScript for pi.dev extensions and SDK-hosted agent systems. Use when changing Pi extension entry points, custom tools, AgentSession orchestration, steering/abort flows, settings, persistence, TUI components, package metadata, tests, or release gates. Includes the stricter GroepOnline pi-agent-orchestrator conventions.
license: MIT
compatibility: Pi TypeScript extensions or SDK integrations using @earendil-works/pi-* packages; Node.js >=22.22.3. Repository-local AGENTS.md and package versions remain authoritative.
metadata:
  author: GroepOnline
  version: "1.0.0"
---

# Pi TypeScript Extension Engineering

Treat a Pi extension as trusted host code with agent-facing schemas, concurrent side effects, persistent session state, and terminal UI constraints. TypeScript correctness is necessary but not sufficient: preserve the host ABI, lifecycle semantics, cancellation, deterministic rendering, and package contract.

## Start by classifying the target

Determine which boundary is being changed before editing:

1. **Extension shell** — an exported extension factory using `ExtensionAPI`, lifecycle events, tools, commands, shortcuts, renderers, or `ctx.ui`.
2. **SDK host** — code that creates and owns `AgentSession` or `AgentSessionRuntime` instances.
3. **Pure core** — deterministic orchestration, reducers, schemas, permissions, scheduling, or persistence with no Pi runtime imports.
4. **TUI layer** — terminal components, ANSI-aware width calculations, keybindings, animation, or interactive views.
5. **Package surface** — `package.json` Pi resources, ESM output, declarations, peer compatibility, npm contents, and release workflows.

Keep pure core independent from Pi whenever practical. Put host imports at explicit adapters and entry points instead of leaking runtime types through every module.

## Repository authority order

Before applying generic guidance, inspect in this order:

1. `AGENTS.md` and nested agent instructions.
2. `package.json`, lockfile, `tsconfig.json`, and lint configuration.
3. Existing adjacent source and tests.
4. Installed Pi package versions and their matching official docs.
5. This skill.

Do not migrate an API merely because the latest Pi documentation differs from the repository's pinned host version. Make compatibility migrations explicit, isolated, and tested.

## TypeScript and ESM contract

- Keep `strict: true` and fix types at the boundary rather than weakening compiler options.
- Use ESM only when the package declares `"type": "module"`.
- Use explicit `.js` specifiers for relative imports from TypeScript source: `./settings.js`, never extensionless or `.ts`.
- Use `import type` when every imported binding is erased. Use inline `type` modifiers when mixing types and runtime values from one module.
- Prefer discriminated unions, branded identifiers, exhaustive switches, and narrow parser functions over broad casts.
- Parse untrusted config, frontmatter, persisted JSON, tool arguments, and cross-extension messages before using them.
- Never use `as any` to make a host type or test fixture compile. Build the complete shape or write a typed fixture factory.
- Preserve insertion order when UI or orchestration semantics rely on `Map` or `Set`; do not add sorting casually.

## Pi host dependency boundary

For Pi host packages:

- Keep runtime host packages as peer dependencies. They may also be dev dependencies for compilation and tests, but must not be bundled as ordinary runtime dependencies.
- Import unavoidable host types directly and explicitly at adapter sites.
- Use local structural compatibility shims for avoidable UI types when the repository already follows that pattern.
- Use dynamic import or feature detection only for genuinely optional peers, not as a workaround for required host APIs.
- Do not import internal or undocumented Pi modules when the public extension or SDK API is sufficient.

For `pi-agent-orchestrator`, preserve its three-way boundary:

- Pi TUI shapes are mirrored in `src/ui/tui-shim.ts`.
- Required `@earendil-works/pi-coding-agent`, `pi-ai`, and `pi-agent-core` types are imported at named boundary sites.
- Optional `@groeponline/context-mode` behavior remains feature-gated in `src/context-mode-bridge.ts`.

## Schema and tool design

Use TypeBox schemas as the runtime contract for every agent-callable tool.

- Match the TypeBox package to the installed Pi host ABI. Agent Orchestra pins `@sinclair/typebox` (see `package.json`); newer Pi releases may use `typebox`. Do not mix both in one package without a deliberate migration.
- Prefer closed, explicit object schemas with descriptions on fields that influence agent behavior.
- Use finite enums for actions and modes; use the Pi AI `StringEnum` helper where provider compatibility requires it.
- Add a `prepareArguments` compatibility adapter only for a known previous argument shape. Keep it small and covered by tests.
- Tool names are stable public API. Renaming requires an alias or migration plan.
- Tool descriptions must state preconditions, side effects, failure states, output limits, and when another tool should be preferred.
- `promptGuidelines` must name the concrete tool because Pi appends them flat to the global guidelines section.

A tool implementation must handle:

1. Argument validation through its schema.
2. Domain preconditions and current state checks.
3. `AbortSignal` before and during expensive work.
4. Progress via `onUpdate` when latency is user-visible.
5. Typed success and failure results.
6. Bounded output.
7. Durable details when state reconstruction or custom rendering needs them.

Never throw for an expected domain outcome such as “agent not running” or “record not found”; return a concise typed tool result. Throw only for failures that the host should treat as exceptional.

## Concurrent mutation safety

Pi may execute tool calls in parallel.

- Wrap file read-modify-write windows with Pi's file mutation queue when a custom tool can overlap built-in edit/write operations.
- Resolve the real absolute target path from `ctx.cwd` before entering the queue.
- Queue the complete mutation window, not only the final write.
- Use a repository-level lock or transactional store for non-file shared state when multiple sessions can mutate it.
- Make retries idempotent. Persist operation IDs or compare expected state before applying a mutation twice.

## AgentSession orchestration

For subagents and embedded Pi runtimes:

- Pass the effective working directory explicitly. Never rely on ambient `process.cwd()` when a worktree or delegated cwd exists.
- Give each subagent its own session. In Agent Orchestra, use `SessionManager.inMemory(effectiveCwd)` and `SettingsManager.create(effectiveCwd, agentDir)` so project settings follow the worktree.
- Remember that `<cwd>/.pi/settings.json` overrides global `~/.pi/agent/settings.json`.
- Use `session.prompt()` for a fresh run, `session.steer()` for redirection during streaming, `session.followUp()` for work after the current run, and `session.abort()` for cancellation.
- When calling `prompt()` during streaming, set the required streaming behavior explicitly.
- Subscribe before prompting when event evidence matters, and always unsubscribe/dispose during cleanup.
- After a runtime-level new-session, switch, fork, clone, or import, treat `runtime.session` as replaced. Rebind extensions and resubscribe to the new session.
- Propagate parent cancellation to child sessions. Do not leave detached agent loops after the parent task is aborted.
- Bound turns, concurrency, retries, and wall-clock duration at the orchestration layer.

Use upstream Pi compaction as the canonical session behavior unless the extension intentionally implements and tests a complete replacement. Do not maintain dead parallel pruning state that appears configurable but is not connected to the live session.

## State and persistence

Choose state storage based on semantics:

- **Branch-aware session state:** include it in tool-result `details` and reconstruct it from the active session branch.
- **Durable TUI-only state:** use custom session entries and a renderer.
- **Project configuration:** store it in the repository's canonical `.pi` settings file and validate on load.
- **Cross-process orchestration state:** use an atomic file/store with locking, schema versioning, and recovery rules.
- **Ephemeral render state:** keep it in component or row-local state, never in persisted business state.

Every persisted schema change needs defaults, validation, backwards compatibility, tests, and documentation.

## TUI engineering

Terminal output is a layout engine, not plain strings.

- Use ANSI-aware width, wrapping, truncation, and padding helpers.
- Keep animation glyphs single-cell unless a renderer reserves a fixed width.
- Make animation and row assignment deterministic across rerenders.
- Preserve behavior at narrow and wide terminal sizes; test at 60, 80, 100, and 140 columns when changing dashboard layouts.
- Use semantic motion roles instead of applying one spinner everywhere.
- Respect configured keybindings through Pi keybinding helpers rather than hard-coded labels.
- Reuse components where supported to avoid flicker and unnecessary allocation.
- Keep render functions pure with respect to orchestration state.

## Output and context discipline

Agent-facing output must be bounded.

- Use head truncation for file/search content and tail truncation for logs or command output.
- Preserve the host defaults unless the tool has a justified smaller limit.
- When truncating, state what was omitted and save the full output to a discoverable file when appropriate.
- Put concise model-facing text in `content`; put structured render/state data in `details`.
- Do not inject large debug objects, stack traces, or raw child transcripts into the parent context.

## Error handling and cleanup

- Narrow caught values with `err instanceof Error ? err.message : String(err)`.
- Distinguish cancellation, expected domain rejection, invalid input, infrastructure failure, and programmer defects.
- Cleanup belongs in `finally` or `session_shutdown`: timers, subscriptions, file watchers, child sessions, locks, temp files, and telemetry spans.
- Report settings persistence errors through the app layer; flush pending settings writes at durability boundaries.
- Do not hide deterministic failures behind retries. Retry only classified transient operations and preserve the final cause.

## Testing strategy

Tests live in `test/` and use Vitest for Agent Orchestra.

For each change, select the smallest complete set:

1. **Pure unit test** for parsers, reducers, permission calculations, scheduling, and formatters.
2. **Contract test** for TypeBox schemas, tool result shapes, package resources, or persisted JSON.
3. **Lifecycle test** for session start/shutdown, cancellation, steering, replacement, and cleanup.
4. **Concurrency test** for locks, queues, duplicate calls, or overlapping writers.
5. **TUI test** for ANSI width, wrapping, deterministic frames, responsive layouts, and partial rendering.
6. **SDK smoke/e2e test** using in-memory settings/session state when real Pi behavior must be verified.
7. **Performance assertion** using explicit thresholds, not console output as evidence.

Build complete typed fixtures. Verify both the accepted path and at least one rejection, cancellation, or compatibility path.

## Agent Orchestra overlay

When working in `GroepOnline/pi-agent-orchestrator`, preserve these invariants:

- Node.js must satisfy the repository's exact minimum, currently `>=22.22.3`.
- TypeScript is strict, emits declarations, targets ESM, and resolves with `moduleResolution: "bundler"`.
- Biome is the only linter; formatting is disabled; strings use double quotes.
- Schema imports use the pinned `@sinclair/typebox` family from `package.json`, not the newer bare `typebox` package, unless an explicit migration is underway.
- Tests use Vitest and live in `test/`.
- Settings persist to `.pi/subagents.json` (project: `<cwd>/.pi/subagents.json`; user: `$PI_CODING_AGENT_DIR/subagents.json`) and must be surfaced through the settings snapshot/menu and API documentation.
- Built-in agent changes update defaults, focused tests, and the README.
- The package entry remains `package.json` → `pi.extensions` → `./dist/index.js`.
- Keep read-only discovery agents read-only and preserve permission inheritance.
- Known Windows schedule-test flakes are not proof that unrelated code is broken; still investigate newly introduced deterministic failures.

Run the authoritative gate:

```bash
npm run typecheck && npm run lint && npm test && npm run build && npm run verify:package
```

For release-sensitive work, also run the repository release-policy verifier and the Cursor Cloud verification path when relevant.

## Review procedure

Before declaring a Pi TypeScript change complete:

1. Identify the host boundary and installed Pi version.
2. Confirm ESM import correctness and type-only imports.
3. Trace cancellation and cleanup from parent to every child/resource.
4. Check parallel mutation and idempotency risks.
5. Validate tool schemas, descriptions, result shape, and truncation.
6. Verify session cwd/settings/resource loading and replacement semantics.
7. Check persisted state migration and branch behavior.
8. Exercise responsive and ANSI-safe TUI paths when UI changed.
9. Run targeted tests, then the repository's full authoritative gate.
10. Report exact evidence, deliberate exclusions, and remaining compatibility risk.

## Reference material

Load these only when the task needs deeper examples:

- `references/patterns.md` — implementation patterns and anti-patterns.
- `references/review-checklist.md` — compact PR and release checklist.
