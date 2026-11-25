---
name: wippy-lua-developer
description: >-
  Senior-level guidance for writing Lua code and YAML registry entries for the Wippy
  platform — the single-binary, actor-model AI runtime. Use whenever working with Wippy:
  authoring or reviewing function.lua / process.lua / workflow.lua entries, _index.yaml
  entry definitions, agent.gen1 agents, http.endpoint / http.router / http.service,
  registry entries and namespace:name IDs, the module system (require + modules:/imports:),
  actor processes (process.spawn, inbox, channel.select, supervision/monitor/link),
  funcs.call / funcs.async, typed errors (result, err pairs), SQL/store/queue/fs data
  access, security (actor/scope/can), the wippy/llm and wippy/agent frameworks, or
  wippy/test BDD tests. Trigger keywords: Wippy, wippy.ai, function.lua, process.lua,
  workflow.lua, agent.gen1, _index.yaml, .wippy.yaml, wippy.lock, registry entry,
  channel.select, process.inbox, funcs.call, llm.generate, "registry:name", Lua actor.
metadata:
  author: xepozz
  version: "1.0"
  category: wippy-development
  sources:
    - https://wippy.ai/llms.txt
    - https://wippy.ai/en/start/llm-brief
    - https://wippy.ai/llm/path/en/* (lua/core, framework, guides)
---

# Wippy Lua Developer

Senior guidance for building on **Wippy** — an open-source, single-binary **actor-model
runtime** for production AI agents. Lua runs in **isolated processes with message passing**
(no shared memory, no locks). Everything is a **registry entry** (`namespace:name`), declared
in YAML and live-modifiable at runtime.

Read the reference that matches the task before non-trivial work:

- **[references/ENTRIES-AND-CONFIG.md](references/ENTRIES-AND-CONFIG.md)** — registry model,
  `_index.yaml`, entry kinds, `modules:` / `imports:`, project layout, HTTP entries, dependencies.
- **[references/LUA-PATTERNS.md](references/LUA-PATTERNS.md)** — functions, processes, workflows,
  channels, errors, `funcs`, data access (SQL/store/queue/fs), HTTP client, security, time,
  registry, events. Canonical APIs + examples.
- **[references/FRAMEWORK.md](references/FRAMEWORK.md)** — `wippy/llm`, `wippy/agent` (agent.gen1,
  tools, traits, delegation, memory), `wippy/test` BDD testing, dataflow/relay/views.

## Mental model (internalize this first)

- **Entry** = `{ id: namespace:name, kind, meta, data }`. The **kind** determines behavior.
  YAML files declare entries, but the **registry is the runtime source of truth** — entries can be
  created/updated/deleted while the system runs.
- **Three compute models:**
  - `function.lua` — **stateless**, request-scoped. Receives args, returns `result, err`. Inherits
    the caller's context; cancels when the caller cancels.
  - `process.lua` — **long-lived actor**. Own PID + inbox; keeps state across messages; yields on
    blocking I/O so thousands run concurrently.
  - `workflow.lua` — **durable actor** (Temporal-backed). Survives crashes; the runtime records
    `funcs.call` results, sleeps, and random values for deterministic replay.
- **Isolation:** processes never share memory — they communicate by **message passing** and
  **channels**. Design for **"let it crash"** + supervision (monitor/link).

## Core rules (apply by default)

1. **Always check errors.** Wippy functions return `result, err`. Errors are typed objects
   (`errors.new{ kind=errors.NOT_FOUND, message=... }`); propagate with `errors.wrap(err, "context")`
   and branch with `errors.is(err, errors.X)`. Never ignore the second return value.
2. **Declare module access.** An entry can only `require()` modules listed in its `modules:` (or
   wired via `imports:`). There is **no `os.execute`, `io.open`, `debug.*`, `package.*`** unless
   granted. If a module isn't listed, it does not exist for that entry. Keep the list minimal.
3. **`process` and `channel` are globals** — always available, not listed in `modules:`. So are
   `errors`. Most other capabilities (`sql`, `json`, `http`, `funcs`, `store`, `time`, `security`,
   `registry`, `events`, `http_client`, `fs`, `queue`, `uuid`, `llm`, `prompt`) require declaration.
4. **IDs are `namespace:name`.** Names use **dots for semantic separation, underscores for words**:
   `app.api:get_user`, `get_user.endpoint`. Entries reference each other by ID; the registry wires
   dependencies and initialization order automatically.
5. **Workflows must stay deterministic.** Only use deterministic modules; let the runtime handle
   `funcs.call`, `time.sleep`, `time.now`, `uuid.v4`. Never call external non-deterministic APIs
   directly from a `workflow.lua` body.
6. **Processes communicate, never share.** Use `process.send` / `inbox:receive()` /
   `channel.select` to multiplex inbox + events + custom channels. Handle `process.event.CANCEL`.
7. **Return the entry's entrypoint.** A `function.lua` module returns its handler (or a table of
   methods); the entry's `method:` selects which one. Keep modules small and composable.

## Quick reference: which kind / pattern?

| Need | Use |
|------|-----|
| Stateless callable / tool / HTTP handler | `function.lua` |
| Long-lived stateful actor / worker | `process.lua` (spawn via `process.spawn(id, host, ...)`) |
| Crash-durable multi-step flow | `workflow.lua` (Temporal) |
| HTTP route | `http.endpoint` → `func: ns:handler`, under an `http.router` + `http.service` |
| DB / cache / queue | `db.sql.postgres`/`mysql`/`sqlite`, `store.memory`/`store.sql`, `queue.queue` |
| AI text/tools/embeddings | `wippy/llm` → `llm.generate(...)` |
| Declarative AI agent | `agent.gen1` registry entry + `wippy/agent` context/runner |
| Typed service interface | `contract.definition` / `contract.binding` |
| Tests | `function.lua` with `meta.type: test` + `wippy/test` |

## Minimal example (function + HTTP endpoint)

`src/api/_index.yaml`:
```yaml
version: "1.0"
namespace: app.api
entries:
  - name: get_user
    kind: function.lua
    source: file://handler.lua
    method: get_user
    modules: [sql, json]
  - name: get_user.endpoint
    kind: http.endpoint
    meta: { router: app:api_router }
    method: GET
    path: /users/{id}
    func: app.api:get_user
```

`src/api/handler.lua`:
```lua
local sql = require("sql")
local function get_user(id)
    local db, err = sql.get("app:main_db")
    if err then return nil, err end
    local rows, err = db:query("SELECT * FROM users WHERE id = $1", id)
    if err then return nil, err end
    if #rows == 0 then
        return nil, errors.new({ kind = errors.NOT_FOUND, message = "user not found" })
    end
    return rows[1]
end
return get_user
```

## Workflow for a Wippy task

1. **Identify the kind** (function/process/workflow/http/agent) and the **namespace**.
2. **Read the matching reference** for canonical APIs before writing.
3. **Declare the entry** in `_index.yaml` (`kind`, `source`, `method`, `modules`/`imports`, `meta`).
4. **Write the Lua**, returning `result, err`; keep `modules:` minimal; use channels for concurrency.
5. **Validate:** `wippy run test` for BDD/simple tests; check the linter/LSP if available.
6. **Use the live doc API for anything not covered here:**
   - Browse: `https://wippy.ai/llm/toc` · Search: `https://wippy.ai/llm/search?q=<query>`
   - Page: `https://wippy.ai/llm/path/en/<path>` · Batch: `https://wippy.ai/llm/context?paths=a,b`
   - Full dump: `https://wippy.ai/llms-full.txt`

## Conventions checklist

- [ ] Entry ID is `namespace:name`; names use dots + underscores correctly.
- [ ] Every fallible call checks `err`; errors are typed and wrapped with context.
- [ ] `modules:` lists exactly what the entry requires — nothing more.
- [ ] Processes use message passing + `channel.select`; cancellation handled.
- [ ] Workflows avoid direct non-deterministic ops.
- [ ] Context (trace IDs, user, security) is allowed to propagate via `funcs.call` — don't bypass it.
