# Core

This directory contains KOTA's kernel: the runtime substrate that modules plug
into.

- Keep `src/core/` small and protocol-oriented.
- Core owns the agent/session loop, workflow runtime, daemon runtime, event
  bus, tool runtime, and module lifecycle.
- General-purpose product capabilities should prefer `src/modules/` unless they
  are truly shared runtime primitives.
- Do not add operator-facing feature code here when it can live in a module.

## Subtrees

- `agents/` — core agent and skill definition types plus system-prompt
  primitives.
- `channels/` — core channel protocol types and provider-neutral message segmentation.
- `config/` — configuration schema, layered loading, secrets management, and
  secret providers.
- `daemon/` — daemon host, control API, scheduler persistence, and live runtime
  state.
- `events/` — typed event catalog and event bus.
- `evidence/` — shared retention, redaction, provenance, projection, and
  pruned-reference policy for durable records and client-visible evidence.
- `loop/` — `AgentSession`, turn execution, context assembly, transport,
  dynamic state, and module-contributed pre-send hooks that run once before
  the main turn loop.
- `model/` — `ModelClient` interface, registry, adaptive routing, and streaming.
  Provider implementations live in `src/modules/model-clients/`.
- `outbound-http/` — the shared policy-aware request transport used by core
  protocols and module adapters. Agent-facing web tools remain module-owned.
- `modules/` — module protocol, discovery, loading, lifecycle, storage, and
  foreign-module support.
- `tools/` — core tool runtime and the remaining truly core-hosted tools.
- `workflow/` — workflow definitions, validation, execution, runtime, and
  repair-loop mechanics. Local workflow completion uses the shared synchronous
  `finalize` hook, not child bookkeeping or publication workflows.
- `agent-harness/` — neutral `AgentHarness` protocol and registry plus the
  provider-neutral message declarations (`message-protocol.ts`) the workflow runtime, run
  stores, and step executors consume. Workflow agent steps, the repair loop,
  the agent-harness delegate backend, and the CLI all dispatch through this
  registry. Adapters (claude-agent-sdk, thin, codex, gemini, etc.) ship as
  modules and register on load. Steps inherit the active preset's harness
  unless `KotaConfig.defaultAgentHarness` or a per-step `harness` pins a
  different adapter. The Claude Agent SDK executor primitive and
  owner-questions MCP bridge live inside
  `src/modules/claude-agent-harness/`, not here.
- `prompt-input/` — harness-neutral user-prompt preprocessing
  (`@path` reference expansion). Every CLI path calls it before handing a
  prompt to `AgentHarness.run`, so every adapter receives the same
  already-expanded text.
- New non-test source should land in `src/core/<subtree>/` or `src/modules/<name>/`,
  not as another loose `src/*.ts` file.

## Strict Types Policy

`any` is forbidden in production TypeScript and is enforced by Biome's
`noExplicitAny` and `noImplicitAnyLet` rules. The same rules are intentionally
relaxed for `*.test.ts`, `*.integration.test.ts`, and `*.integration.ts`
fixtures, but that syntax exemption is not permission to cast partial object
graphs into production aggregates. Tests use narrow typed ports and builders;
only boundary parsers start from `unknown` or JSON-shaped records.

`unknown` (and the JSON-shaped alias `Record<string, unknown>`) is the right
type for untrusted input at a system boundary:

- JSON parse and disk-fixture loaders.
- HTTP/SSE/JSON-RPC frames before they have been shaped.
- External SDK adapter inputs and their raw event passthrough.
- Caught errors (`catch (err: unknown)`).
- Schema/decoder entry points whose only job is to narrow.

Inside trusted domain code — agent loops, workflow execution, event handlers,
business logic — values are expected to already carry their precise type. A
`Record<string, unknown>` that flows past a decoder is a missing decoder.

When a runtime parser legitimately needs `unknown`, expose a typed decoder
beside it (e.g. `parseQuietHours`, `decodeRootsListResult`,
`decodeGitHubIssueList`) that returns either a precise shape or a
discriminated `{ ok: false; error: string }` result. Downstream consumers
must depend on the typed result, not on the raw boundary value.

Use strict TypeScript and Biome as the mechanical guard. Tests cover decoder
acceptance/rejection and typed propagation; do not count source tokens or keep
per-file exception catalogs. Strict types serve as an authoritative proof
mechanism; do not add redundant tests for invariants already guaranteed by
the type system.
