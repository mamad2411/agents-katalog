---
name: fcode-core-concepts
description: Factorial Code platform architecture and core concepts — processes, modules, execution context, team variables, datastore, file storage, workspace structure, and naming conventions. Use when building, editing, or reasoning about any Factorial Code (fcode) process, module, or workspace; start here before writing process or module code.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code core concepts

Factorial Code (fcode) is an enterprise integration and automation platform.
You write **processes** (and reusable **modules**) in JavaScript or Python; the
platform handles sandboxing, dependencies, secrets, scheduling, and execution.

This skill is the mental model. For writing actual code, also use
`fcode-javascript` or `fcode-python`; for the CLI workflow, `fcode-cli`.

## Gotchas

These defy reasonable assumptions — get them wrong and the process breaks:

- **Datastore stores only strings and numbers.** Serialize objects with
  `JSON.stringify` / `json.dumps` before `set`, and parse on `get`.
- **Module files are named after their slug, not `index`/`main`.** A module
  lives at `modules/<slug>/<slug>.js` (or `.py`) — e.g.
  `modules/shopify-client/shopify-client.js`. **Never** `modules/<slug>/index.js`
  or `main.py` (those names are reserved for *process* entry files), and never
  put a module file directly under `modules/` without its own folder.
- **Never overwrite the whole `variables.env`.** Read it first and append/patch
  only the specific variable(s); rewriting the file drops every variable not in
  the new content and can break other processes.
- **Never hardcode or log secrets.** Use variables/env vars; mask or omit
  secrets from logs.
- **Runtimes are pinned:** JavaScript = **Node.js v22**, Python = **3.13**.

## Key concepts

| Concept | What it is | Key point |
|---|---|---|
| **Process** | The unit of execution (business logic) | Defines input parameters, returns structured results |
| **Module** | Reusable code library | Shared across processes, can be versioned |
| **Variables** | Configuration & secrets | Env vars; never hardcode secrets |
| **Datastore** | Persistent key-value store | **Strings and numbers only** |
| **Storage** | File storage | Binary files, documents, large payloads |

### Processes

The basic unit of execution, in JavaScript (`index.js`) or Python (`main.py`).
Processes may declare input parameters via JSON Schema (`parametersSchema.json`,
see `fcode-json-schema`) and read them through `fcode.context.parameters`.
Return structured JSON; for webhook-style responses return
`{ status, headers, body }`.

### Modules

Reusable libraries shared across processes — use them to avoid duplication,
encapsulate API clients/integrations, keep process code small, and support
versioning. See the module-naming gotcha above.

### Execution context

Each process runs isolated, with access to:

- **Input parameters**: `fcode.context.parameters`
- **Environment variables**: `process.env.*` / `os.getenv(...)` (or `fcode.env.*`)
- **Execution metadata**: `fcode.execution.*`
- **Request data** (webhooks): request body/headers when applicable

### Variables (configuration & secrets)

Store base URLs, timeouts, API keys, and tokens as variables (never hardcode).
`variables.env` holds team variables (`KEY=VALUE`); `variables.local.env` holds
local-only overrides. See the overwrite gotcha above.

### Datastore vs Storage

- **Datastore** — persistent key-value state across runs (last-run timestamps,
  cursors, dedup IDs, small caches). Strings/numbers only.
- **Storage** — files that don't belong in datastore (reports, exports, images,
  PDFs, data extracts).

## Decision guidelines

**Module vs inline code**

| Scenario | Recommendation |
|---|---|
| API client used by multiple processes | Create a module |
| Utility helpers used 2+ times | Create a module |
| One-off transformation / single-use logic | Keep inline |

**Datastore vs Variables vs Storage**

| Need | Use |
|---|---|
| Config that rarely changes; secrets/credentials | **Variables** |
| State that changes between runs; cached API responses | **Datastore** |
| Binary files / large exports | **Storage** |

## Naming conventions

| Resource | Convention | Example |
|---|---|---|
| Process slug | kebab-case | `order-sync-shopify` |
| Module slug | kebab-case | `shopify-client` |
| Variables | SCREAMING_SNAKE_CASE | `SHOPIFY_API_KEY` |
| JavaScript functions | camelCase | `fetchOrders()` |
| Python functions | snake_case | `fetch_orders()` |

## Workspace structure (CLI)

A local workspace managed by the `fcode` CLI (see `fcode-cli`):

```
📦 <workspace-name>
┣ 📂 dependencies          # shared deps: package.json (JS) / requirements.txt (Py)
┣ 📂 modules
┃ ┗ 📂 <module-slug>       # one folder per module
┃   ┗ 📜 <module-slug>.js  #   entry file named after the slug (NOT index.js)
┣ 📂 processes
┃ ┗ 📂 <process-slug>      # one folder per process
┃   ┣ 📜 index.js          #   or main.py — the process entry file
┃   ┣ 📜 parametersSchema.json   # input parameter schema (the form)
┃   ┣ 📜 parameters.json   #   default test parameters for `fcode run`
┃   ┣ 📜 README.md
┃   ┗ 📜 package.json      #   optional process-scoped dependencies
┣ 📜 datastore.json
┣ 📜 variables.env         # team variables (KEY=VALUE)
┣ 📜 variables.local.env   # local overrides (not shared)
┗ 📂 .fcode
```

Processes and modules also support `versions/` subfolders (e.g. `versions/v1.0/`)
for versioned interfaces. `dependencies/package.json` holds only the inner
`dependencies` object (e.g. `{ "axios": "^1.6.0" }`).

## General rules

- Validate inputs early — check required parameters and types at the start.
- Handle errors explicitly; throw meaningful, actionable errors.
- Use timeouts/retries for external calls; mind rate limits.
- Log key steps (start/end, major decisions, external calls) — never secrets.
- Keep outputs structured (JSON that's easy to consume and debug).
