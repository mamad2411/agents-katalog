---
name: ns-langgraph-agents
description: (NS) LangGraph.js agent-api — StateGraph, MCP tools, skill bind/inject, checkpointers, context-window trim, HITL/SSE, prompt/locale placement. Use for agent-api, LangGraph graphs, MCP wiring, orphan layout, system-prompt compose, bind parity, graph-spec sync, or "fix my LangGraph agent" / "wire MCP tools" / "translations in the graph". Code via ns-code-coder; LangGraph vs CrewAI via ns-multi-agent-architect. Do NOT use for CrewAI crews, generic web apps, or SDD-only requirements.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.1"
depends:
  - ns-harness
---

# LangGraph Agents

Senior agent-runtime engineer. Guide construction and maintenance of **production-grade LangGraph.js** systems (Node 24+, TypeScript strict, `@langchain/langgraph`).

This skill owns **runtime doctrine and coordination** — including **placement**, **prompt/capability injection**, and **graph-spec sync**. Implementation diffs are executed via `ns-code-coder` (or `ns-code-autonomous` for larger plans). Architecture choice (LangGraph vs CrewAI) stays in `ns-multi-agent-architect`.

## Routing (read first)

| Signal | Action |
| ------ | ------ |
| No framework lock / CrewAI requested | **Stop** → `ns-multi-agent-architect` |
| Orphan / lost structure / layout unclear | Run orphan checklist **before** features (`references/orphan-recovery-checklist.md`) |
| GitLab `ISSUE_URL` or SDD version scope | **Defer** to harness `../ns-harness/references/code-skill-routing.md` — do not absorb |
| Approved placement/inject plan ready for diff | Hand off to `ns-code-coder` for implementation only — this skill does **not** write app code |

## Boot (mandatory)

See `../ns-harness/references/harness-discovery.md` — **complete Session boot (blocking)** there, then:

1. Confirm `{agent_api_root}` and `graph-spec.md` when touching runtime
2. Load placement/inject refs before path decisions (`references/placement-and-domains.md`, `references/prompt-and-capability-injection.md`)
3. Continue this skill

**Success criterion:** following placement + inject doctrine + project rules = success; inventing folders or external frameworks = failure.

## When to use

| Situation | Action |
| --------- | ------ |
| Greenfield agent-api | Follow **Build workflow**; produce `graph-spec.md` first |
| Brownfield / orphaned runtime | Run **Orphan recovery** (`references/orphan-recovery-checklist.md`) before features |
| New file / unclear folder | **Placement Decision Block** + `references/placement-and-domains.md` |
| System prompt / skill inject / bind | **Prompt/Capability plan** + `references/prompt-and-capability-injection.md` |
| Topology / state / capabilities change | **Spec Sync Gate** — update `graph-spec.md` in the same delivery |
| MCP with many servers/tools | Read `references/mcp-complex-access.md` + `references/capability-governance.md` |
| Token blow-up / slow turns | Read `references/context-window-and-tokens.md` |
| Provider message/reasoning quirks | Read `references/message-content-blocks.md` |
| HITL / streaming UX | Read `references/streaming-and-hitl.md` |
| Evals before merge | Read `references/evals-and-gates.md` |

## Core doctrine

LangGraph orchestrates **control flow**; MCP and local tools are **capabilities** beneath the graph. Keep graph state small (references and summaries, not large payloads). The checkpointer persists full state; **context window management** decides what the LLM sees — these are separate concerns.

Three capability kinds bind to the model:

| Kind | LLM wire name | Internal id |
| ---- | ------------- | ------------- |
| Local tool | `{name}` | `local:{name}` |
| MCP tool | `mcp__{server}__{tool}` | `mcp:{server}:{tool}` |
| Skill procedure | `use_skill__{id}` | `skill:{id}` |

Wire names must match `^[a-zA-Z0-9_-]{1,128}$` (use `__` separators; colons only in internal ids). Colon in a **new** wire name is Critical on review.

## Pre-change gates

Before any new file or inject/bind change, complete all three. Skip coding until they are posted.

### 1. Placement Decision Block

```markdown
### Placement Decision Block
- Artifact: …
- Type: …
- Target path: …
- Layer: …
- Refs: placement-and-domains.md
- do_not_create_under: […]
```

Full matrix: `references/placement-and-domains.md`. `tenant_model: simple` still requires the matrix; `vertical` adds verticals as **config-only** (`config/verticals/`, zero new `src/`).

### 2. Prompt / Capability plan

```markdown
### Prompt / Capability plan
- System layers touched: […]
- Canonical prompt path: …
- Session overlay: yes/no
- Bind list: […]
- Auto-inject skills: […] (exclusive of bind for same id)
- Truncate caps: tool vs skill body
- Bind parity: …
- Spec paths to sync: […]
```

Full doctrine: `references/prompt-and-capability-injection.md`.

### 3. Spec Sync Gate

If **nodes, edges, state, capabilities, recursion_limit, or wire names** change → update `graph-spec.md` in the **same** delivery. An archived or stale spec is **not** source of truth — do not "fix code to match archive" when the live graph is intentional; sync the spec to the intended runtime instead.

## Reference map

Load on demand — do not memorize entire files into the conversation.

| Reference | Read when |
| --------- | --------- |
| `references/orphan-recovery-checklist.md` | Project structure unclear or agent "lost" |
| `references/runtime-layout.md` | Scaffolding, refactors, layer violations |
| `references/placement-and-domains.md` | Where to put files; domain vs graph vs config |
| `references/prompt-and-capability-injection.md` | System prompt layers, bind vs inject, bind parity |
| `references/message-content-blocks.md` | AIMessage/HumanMessage/ToolMessage across providers |
| `references/context-window-and-tokens.md` | trim, summarize, tool vs skill body caps |
| `references/mcp-complex-access.md` | Multi-server MCP, discovery, transport, lifecycle |
| `references/capability-governance.md` | Allowlist, classification, rate limits, secrets |
| `references/error-and-reliability.md` | Tool errors, circuit breaker, retries |
| `references/observability.md` | Postgres audit, LangSmith, OTel, run context |
| `references/architectures.md` | ReAct, plan-execute, reflection, supervisor |
| `references/streaming-and-hitl.md` | SSE envelopes, `interrupt()`, `Command` resume |
| `references/evals-and-gates.md` | Architecture, tool-selection, memory evals |
| `references/anti-patterns.md` | Review gate before marking done |

Templates (copy snippets, not full scaffolds): `templates/graph-spec.md`, `templates/contracts/`, `templates/snippets/`.

## Session inputs

| Variable | Required |
| -------- | -------- |
| `{product_root}` | Yes (or infer when single product) |
| `{agent_api_root}` | Default `{product_root}/agent-api` |
| `{task}` | What to build, fix, or review |

## Orphan recovery (brownfield first)

When the runtime is disorganized or the team is blocked:

1. Read `references/orphan-recovery-checklist.md` and score the project.
2. Post a short gap report: structure, placement, context window, inject/bind parity, MCP governance, observability, HTTP contract, spec sync.
3. Propose a **ordered fix plan** (one phase per message if large).
4. Only then implement via `ns-code-coder`.

Do not add graph nodes or MCP servers until layout and governance baselines pass.

## Build workflow (greenfield or post-recovery)

### Phase 0 — Spec gate

If `graph-spec.md` is missing, create it from `templates/graph-spec.md`. Minimum sections: locked header (`framework`, `tenant_model`, `architecture`, `interaction_mode`), domain ownership, prompt composition, state schema, nodes table, edges, interrupts, memory, capability bind/inject table, recursion_limit, HTTP routes.

If the user has no architecture decision yet, stop and invoke `ns-multi-agent-architect` first.

### Phase 1 — Skeleton

Align tree per `references/runtime-layout.md` and `references/placement-and-domains.md`. Production code under `src/` only; tests under `tests/`. Graph compiles in `src/graph/graph.ts`; checkpointer in `src/memory/`. Conversation owns `prompts/`, `locale/`, `presentation/`.

Use snippets from `templates/snippets/` — do not paste a monolithic scaffold.

### Phase 2 — State and persistence

- `AgentState` with `messages` reducer (`Annotation.Root` or Zod + `MessagesZodMeta`).
- `PostgresSaver` in dev/prod; `MemorySaver` only in `tests/setup.ts`.
- Every invoke/stream: `configurable.thread_id` via `buildRunConfig`.

### Phase 3 — LLM and messages

- Provider config in `src/llm/` (infra only — no domain prompts).
- Prefer JSON mode + Zod parse for structured turns; avoid `withStructuredOutput` on OpenAI-compatible local servers.
- Normalize provider output via `contentBlocks` / `content_blocks` — see `references/message-content-blocks.md`.

### Phase 4 — Context window (mandatory)

Implement per `references/context-window-and-tokens.md`:

- `trimMessagesForLlm` before every LLM call.
- `truncateToolOutput` before `ToolMessage` enters state.
- Separate `CONTEXT_SKILL_BODY_MAX_CHARS` for skill bodies.
- Optional `summarizeOlderMessages` with **persisted compaction** (`RemoveMessage` + rewrite) in the same agent-node return.

Never pass raw `state.messages` to the model.

### Phase 5 — Capabilities

1. Local `StructuredTool`s in `src/tools/`.
2. MCP: governed client — discovery → local allowlist → wire names → singleton client lifecycle (`references/mcp-complex-access.md`).
3. Skills: `skills/*.md` auto-discovered → `use_skill__{id}` **or** auto-inject (exclusive per id).

Apply `references/capability-governance.md` and `references/prompt-and-capability-injection.md` before `bindTools`. Enforce **bind parity**.

### Phase 6 — HTTP and interaction mode

| Mode | Requirements |
| ---- | ------------ |
| `sync_json` | `POST /threads`, `POST /threads/:id/message` |
| `streaming_sse` | SSE envelope per `references/streaming-and-hitl.md` |
| HITL | `interrupt()` + `POST /threads/:id/resume` with `Command({ resume })` |

Keep Postman collection aligned with live routes.

### Phase 7 — Observability

Wire `references/observability.md`: `initDb`, `runStorage`, `logLlmCall`, `logToolExecution`. LangSmith and OTel are opt-in.

### Phase 8 — Evals and review

- Add suites per `references/evals-and-gates.md`.
- Run `npm run build && npm test` in `{agent_api_root}`.
- Invoke `ns-code-reviewer` on the diff; ask it to verify placement, inject, wire-name, and bind-parity anti-patterns when the diff touches `agent-api`.

## Maintenance workflow

For ongoing work (not greenfield):

1. Run the three **Pre-change gates**.
2. Confirm `graph-spec.md` will match the intended compiled graph after the change.
3. Identify layer: graph node, conversation domain, MCP, memory, HTTP.
4. Read the matching reference section before editing.
5. Implement minimal diff via `ns-code-coder` with placement/inject handoff fields.
6. Update Postman when HTTP routes change.
7. Re-run orphan checklist items touched by the change.

## MCP complex access (quick rules)

When multiple MCP servers expose overlapping or large tool catalogs:

- **Filter at discovery** — agent sees only allowlisted tools (`tools/list` filtered before bind).
- **Classify locally** — `read | write | destructive | admin`; never trust server "read-only" flags.
- **Reuse client** — one `MultiServerMCPClient` (or equivalent) per process; no per-request subprocess spawn in production.
- **Transport** — Streamable HTTP for deployed services; stdio only for local single-user dev.
- **Errors** — MCP execution errors (`isError: true`) become recoverable `ToolMessage` with `status: "error"`; protocol failures may abort the run with a structured HTTP/SSE `failed` envelope.
- **Secrets** — env or `RunnableConfig.configurable` / request payload only; never graph state or checkpointer snapshots.

Full patterns: `references/mcp-complex-access.md`.

## Handoff to ns-code-coder

When implementation is approved, delegate with:

```markdown
## LangGraph implementation task
- Root: {agent_api_root}
- Spec: path/to/graph-spec.md
- Phase: [number and name from this skill]
- target_paths: […]
- layer: […]
- do_not_create_under: […]
- injection_notes: [layers / bind vs auto-inject / caps]
- spec_paths_to_sync: […]
- References to apply: [list]
- Acceptance: build + test pass; orphan checklist items [n] resolved; placement + inject + bind parity verified
- Review: ns-code-reviewer after tests — must check placement, inject, wire names (`:`), bind parity (load ns-langgraph-agents anti-patterns when diff touches agent-api)
```

Stay in this skill for diagnosis, spec updates, placement, and governance design; switch to coder for the diff.

## Stop conditions

| Condition | Action |
| --------- | ------ |
| No `graph-spec.md` and user wants code now | Create spec or invoke architect |
| Path outside placement matrix / inventing folders | Stop; propose legal path |
| Domain / locale / copy landing in `graph/` or `llm/` | Stop; reroute to conversation/config |
| Bind without parity (dispatchable but unbound) | Stop; fix bind or document unbound + test |
| `:` in a new wire name | Stop; use `__` separators |
| Skill auto-inject + bind same id without explicit decision | Stop; choose one mode |
| CrewAI requested | Redirect to appropriate skill |
| Change spans >3 layers without plan | One-line phased plan, wait for approval |
| Critical security gap (secrets in state, ungoverned MCP) | Block feature work; fix governance first |

## Related skills (ownership)

| Skill | Owns |
| ----- | ---- |
| `ns-langgraph-agents` | Doctrine, placement, inject plan, graph-spec |
| `ns-code-coder` | Diff + review loop |
| `ns-code-reviewer` | Verdict; when diff touches `agent-api`, apply placement + inject + wire-name + bind-parity anti-patterns from this skill |
| `ns-multi-agent-architect` | Framework choice only |
| `ns-code-investigator` | Runtime debug |

## Forbidden

- Storing secrets, API keys, or system prompts in graph state or checkpointer
- Passing unbounded tool/MCP output into `state.messages`
- Applying tool/MCP truncate caps to skill bodies (use `CONTEXT_SKILL_BODY_MAX_CHARS`)
- Trusting MCP tool metadata for security classification
- Spawning stdio MCP subprocesses per HTTP request in production
- `memory/` compiling `StateGraph`
- Domain qualify/conversation prompts in `src/llm/`
- Locale/presentation under `graph/`
- Nudge as fake `HumanMessage`
- Tests under `src/`
