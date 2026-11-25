---
name: agentjsx
description: Authoring and diagnosing code in the agentjsx codebase (npm package `@flamecast/agentjsx`, locally at `/Users/arjun/Documents/github/effectctx`). The library lets you define an agent as a JSX tree — capability components install tools, block components emit prompt content, shaper components transform via `renderChildren`. Use whenever the user is writing new components (capability, content, or shaper), adding a new extension, debugging the render walk or tool reconciler, asking how a piece of agentjsx works internally, or referencing JSX patterns like `useRenderContext`, `runEffect`, `emitTool`, `emitFragment`, `renderChildren`. Also trigger on filenames in `src/jsx/`, `src/core/`, `src/platforms/`, `src/extensions/`, or any task touching `@flamecast/agentjsx` imports. Use proactively when you see `createAgentRuntime`, `<Workspace>`, `<Compact>`, `<McpServer>`, `<Skills>`, `<Todo>`, or any other agentjsx component in code — that's the strong signal you should consult this skill before authoring more.
---

# agentjsx

A coding-agent harness where the agent is defined as a JSX tree. Source lives at `/Users/arjun/Documents/github/effectctx` (npm: `@flamecast/agentjsx`).

## The mental model in one paragraph

Agents are components. `createAgentRuntime({ context: () => render(<Agent>…</Agent>) })` builds an agent by walking a JSX tree on every render trigger. Each component is a pure function that emits zero or more of: **fragments** (system-prompt blocks the model sees), **tools** (functions the model can call), and (via wrapper components) transformations of its descendants' emits. The runtime collects the emits, reconciles tools by name (installing new ones in per-tool Effect Scopes, releasing removed ones), feeds the fragments through `adaptToProviderContext`, and ships the result to `infer`. Same architectural shape as React DOM: declarative tree → diff against last render → side effects applied.

## When to reach for which component shape

Three shapes. Pick by what the component contributes:

| Shape | Contributes | Examples in repo | When to use |
|---|---|---|---|
| **Content** | Fragments only | `<Agent>`, `<Block name="...">`, `<Messages />` | Developer-authored prompt content, or projections of the event log |
| **Capability** | Tools + (optionally) a fragment describing them | `<Workspace>`, `<Skills>`, `<McpServer>`, `<Todo>` | Anything that gives the model new things it can call. Tool registration belongs here. |
| **Shaper** | Transforms its children's emits via `renderChildren()` | `<Compact strategy="...">` | Anything that needs to inspect what its children produced and re-emit a different version. Compaction, filtering, summarization. |

When you find yourself reaching for a side-effecting hook or hidden context to communicate state *between* components, stop. Re-derive what you need by reading the event log via `useRenderContext().events`, or wrap with a shaper. The architecture refuses cross-component hidden state on purpose.

## Key files

Read these to ground any non-trivial change:

| File | What lives there |
|---|---|
| `src/core/agent.ts` | `createAgentRuntime`, `AgentOptions`, the consumer-facing entry |
| `src/core/agent-ctx.ts` | render driver, tool reconciler (per-tool Scopes), `_setExternalContext` bridge |
| `src/jsx/runtime.ts` | `createElement`, `Fragment`, `Element`/`Node` types, `emitFragment`/`emitTool` helpers, `EMIT_SENTINEL` |
| `src/jsx/render.ts` | The walker, `RenderContext` (events + runEffect + infer), `useRenderContext()`, `renderChildren()`, the external-context bridge |
| `src/jsx/components/` | Every shipped component — skim a few before authoring a new one |
| `src/core/types.ts` | `Rendered`, `Fragment`, `Tool`, `Event`, `InferFn`, `ProviderContext` types |
| `src/core/projections.ts` | `PROJECTORS` + `EVENT_META` tables — exhaustively mapped over `Event["type"]` |

The Effect Layer extensions in `src/extensions/` are the older API. They still work and are valid for non-JSX consumers, but new work should prefer the JSX component shape unless there's a specific reason not to. See `references/extensions.md`.

## Quick patterns

For full templates + code recipes, read `references/components.md`. The three patterns that come up over and over:

### Capability component skeleton

```tsx
import { FileSystem, Path } from "@effect/platform"
import { Effect, Schema } from "effect"
import { defineTool } from "../../core/define-tool"
import { emitFragment, emitTool } from "../runtime"
import { useRenderContext } from "../render"

export function MyCapability({ root }: { root: string }) {
  const { runEffect } = useRenderContext()

  const my_tool = defineTool({
    name: "my_tool",
    description: "...",
    parameters: Schema.Struct({ path: Schema.String }),
    run: async ({ path }) => {
      try {
        return await runEffect(Effect.gen(function* () {
          const fs = yield* FileSystem.FileSystem
          // ...
          return result
        }) as unknown as Effect.Effect<string, never, never>)
      } catch (e) {
        return `[my_tool] Error: ${e instanceof Error ? e.message : String(e)}`
      }
    },
  })

  return [
    emitTool(my_tool),
    emitFragment({
      tag: "core/system",
      source: "my-capability",
      content: "<my-block>(describes what's available)</my-block>",
    }),
  ]
}
```

The `as unknown as Effect.Effect<A, E, never>` cast at the `runEffect` call site is the **intended pattern**. `runEffect`'s public signature pins `R = never` so it composes inside Promise-returning Tool.run callbacks. The runtime actually has the platform layer's services available; the cast just tells TypeScript to trust it. Use the cast at the boundary — don't propagate `R = never` typing into deeper helpers.

### Shaper component skeleton

```tsx
import { renderChildren } from "../render"
import type { Node } from "../runtime"
import { emitFragment, emitTool } from "../runtime"

export function MyShaper({ children, ...opts }: {
  children: Node | ReadonlyArray<Node>
  /* ...opts */
}) {
  const inner = renderChildren(children) // { fragments: Fragment[], tools: Tool[] }
  const transformed = transformFragments(inner.fragments, opts)
  return [
    ...transformed.map(f => emitFragment(f)),
    ...inner.tools.map(t => emitTool(t)),
  ]
}
```

Shapers walk their JSX subtree into a local collector via `renderChildren()`, inspect/transform what came out, and re-emit. The outer collector only sees the shaper's re-emits, not the children's raw emits. That's what makes nested shapers compose (`<Compact strategy="snip"><Compact strategy="truncate-tool-outputs"><Messages /></Compact></Compact>` works because each level only sees its child's output).

### Event-log state (the Todo pattern)

Component state lives in the event log, not in closures or module-level vars. Three steps:

1. **Add the event type to `src/core/types.ts`.** The `Event` union has clear shape — match it.
2. **Update `src/core/projections.ts`.** The `PROJECTORS` and `EVENT_META` tables are exhaustively mapped via TypeScript's mapped type check, so adding a new variant breaks the compile until both are updated. Add cases (usually returning `null` for projection if the event shouldn't appear in the message stream).
3. **In the component, project state from events + have tools return `extraEvents`.**

```ts
function MyState() {
  const { events } = useRenderContext()
  const items = events.reduce(reducer, initialState)

  const my_action = defineTool({
    name: "my_action",
    parameters: Schema.Struct({ data: Schema.String }),
    run: async ({ data }) => ({
      content: "ok",
      extraEvents: [{ type: "my.added", data }],
    }),
  })

  return [emitTool(my_action), emitFragment(renderItems(items))]
}
```

Why this matters: log-as-source-of-truth means hydration is free (replay events → same state), debugging is free (dump the log), multi-agent state is safe (no module-level globals colliding).

### Async data cache (the Skills / McpServer pattern)

The JSX render walk is synchronous, but you'll often want async data (reading a directory, connecting to an MCP server). The pattern:

```ts
const cache = new Map<string, { state: "loading" | "ready" | "failed"; data?: T }>()

export function MyAsyncCapability({ id }: { id: string }) {
  const { runEffect } = useRenderContext()
  let entry = cache.get(id)
  if (!entry) {
    entry = { state: "loading" }
    cache.set(id, entry)
    void runEffect(fetchData(id) as never)
      .then(data => cache.set(id, { state: "ready", data }))
      .catch(() => cache.set(id, { state: "failed" }))
  }
  // First render: cache is "loading" — emit a placeholder block.
  // Subsequent renders: cache is "ready" — emit the real content.
}
```

The UX wart: turn 1 shows `(loading...)` because the cache hasn't filled yet. Turn 2 onward, the cache is hot. Acceptable because real conversations always have a turn 2. Don't try to make it synchronous — render() is sync by design, and patching that around is more cost than the wart.

## The render walk in three sentences

1. The runtime calls `context()`. Inside, the user calls `render(<tree>)`. The walker walks the tree depth-first, invoking each function component with its props + (synthetic) `children`, and collects every `Element` it gets back — including the sentinel-shaped `Element`s that `emitFragment` / `emitTool` produce, which the walker recognizes and pushes into the collector.
2. Function components can return arrays, Fragments, single `Element`s, strings, or null. The walker handles all of those. The walker maintains an ambient `RenderContext` so components can call `useRenderContext()` from inside their function bodies; the runtime sets that context before invoking the user's `context()` callback.
3. The walker returns `Rendered { fragments, tools }`. The runtime diffs the tool list against the previous render's tool list keyed by name, opens a new `Scope.CloseableScope` per new tool and runs `addTool` inside it, closes scopes for tools that vanished, then pipes the fragments through `adaptToProviderContext` to produce the final `{ system, messages, tools }` shape sent to `infer`.

For the full mechanism, read `references/architecture.md`.

## When NOT to use a JSX component

Stick with a Layer-based extension in `src/extensions/` if:

- You need a **forked fiber** that runs on a schedule independent of render triggers (periodic polling, watchers). JSX components have no fiber lifecycle of their own.
- You're providing **infrastructure** that should exist regardless of the JSX tree shape (e.g. a default `errorReporter` for the whole agent).
- You're wrapping a third-party SDK whose lifecycle is best managed by Effect's `Scope` primitives directly.

`references/extensions.md` covers the legacy API.

## Authoring discipline

- **Read existing source first.** `src/jsx/components/workspace.tsx` is the canonical real-capability template. `src/jsx/components/todo.tsx` is the event-log-state template. `src/jsx/components/skills.tsx` is the async-cache template. `src/jsx/components/compact.tsx` is the shaper template. Always skim before writing new.
- **Typecheck often.** The codebase has mapped-exhaustiveness checks on `Event` projections in `src/core/projections.ts` — adding a new event variant will break the compile until both `PROJECTORS` and `EVENT_META` are updated. Embrace the seam.
- **Add a test in `test/jsx/`.** Existing patterns: mocked `InferFn` that scripts tool calls, agent runs to terminal, assert on rendered context + final events. See `test/jsx/end-to-end.test.tsx`, `workspace-platform.test.tsx`, `skills-compact.test.tsx`, `mcp.test.tsx`, `compact-summary.test.tsx`.
- **Tools are reconciled by name only.** Same name across renders = no churn (closure identity doesn't matter). Different name = old released, new installed.
- **Errors inside `Tool.run` become strings the LLM sees.** Wrap your `runEffect` calls in try/catch and return a clear `[tool_name] Error: ...` string. Don't let exceptions escape — they become opaque defects.

## Source layout (after the `src/core` + `src/platforms` refactor)

```
src/
├── core/                       runtime guts (agent, types, projections, etc.)
├── jsx/                        the JSX system
│   ├── runtime.ts
│   ├── render.ts
│   ├── jsx-runtime.ts          (automatic JSX runtime entry — for `jsxImportSource`)
│   └── components/
│       ├── basics.tsx          (Agent, Block, Messages)
│       ├── workspace.tsx       (canonical capability)
│       ├── todo.tsx            (canonical event-log state)
│       ├── skills.tsx          (canonical async cache)
│       ├── mcp.tsx             (async cache + namespaced tools)
│       └── compact.tsx         (canonical shaper)
├── extensions/                 legacy Effect Layer extensions
├── providers/                  InferFn implementations (AI Gateway, OpenRouter)
└── platforms/
    ├── node/                   real fs/shell via @effect/platform-node
    ├── bun/                    BunContext re-export (full surface)
    └── browser/                partial: HTTP only, no FileSystem/CommandExecutor
```

Most authoring tasks touch only `src/jsx/components/` + maybe `src/core/types.ts` + `src/core/projections.ts` for new event types.

## Reference files

- `references/components.md` — full templates for content, capability, and shaper components, including the async-cache and event-log patterns
- `references/architecture.md` — render walk internals, the reconciler, RenderContext injection, `renderChildren` semantics
- `references/extensions.md` — the legacy Effect Layer API: when to use it, the canonical shape, migration to JSX components
- `references/platforms.md` — per-runtime adapter status (Node, Bun work; Browser partial; Worker/Cloudflare not implemented), how to wire `platform`, common gotchas
