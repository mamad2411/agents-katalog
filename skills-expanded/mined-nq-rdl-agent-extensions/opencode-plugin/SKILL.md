---
name: opencode-plugin
license: CC-BY-4.0
compatibility: >-
  OpenCode plugins (JS/TS, run by Bun inside OpenCode) typed by
  @opencode-ai/plugin; Hooks interface checked against v1.18.33 source
  (packages/plugin/src/index.ts) on 2026-09-29. SDK versions: opencode-sdk.
description: >-
  Write or debug OpenCode plugins — JS/TS modules in `.opencode/plugins/` that
  return hook handlers (`tool.execute.before/after`, `permission.ask`, `shell.env`,
  `command.execute.before`), read bus events (`session.idle`) in the `event`
  handler, or register tools from code. Use for "OpenCode hook/stop hook"
  asks. Not Claude Code hooks, not OpenAI Codex; standalone tool files →
  opencode-dev:tools.
argument-hint: "What OpenCode plugin/hook do you want? (e.g. 'block reads of .env', 'notify when a session finishes', 'add a custom tool from a plugin')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# OpenCode Plugins & Hooks

OpenCode (the open-source coding agent at `opencode.ai`, source
`github.com/anomalyco/opencode` — **not** OpenAI Codex) extends via **plugins**: a JS/TS module exporting
`async (input, options?) => Promise<Hooks>`. There is **no settings-file hook
table like Claude Code** — "hooks" exist *only* as keys of the object your plugin
returns. Get the vocabulary layering right and most plugins are a few lines.

> **Verify-canonical guard.** OpenCode's API moves fast and predates the model's
> training cutoff — before writing plugin code, read `references/plugins.rst` AND
> re-check <https://opencode.ai/docs/plugins/> for drift. The handler-key set is
> defined in `interface Hooks` (`packages/plugin/src/index.ts`).

**Checked against.** The `interface Hooks` key set and `(input, output)` shapes below
match `packages/plugin/src/index.ts` at OpenCode `v1.18.33` (2026-09-29).
`references/plugins.rst` is the docs page as fetched 2026-06-29. Package and SDK
versions are owned by `/opencode-dev:sdk`. If the installed OpenCode differs, re-read
`interface Hooks` at that tag before relying on a field name.

---

## The one trap that breaks most plugins: handlers vs. events

The docs print a single **"Events"** list that silently mixes two different
layers. They share nouns but differ in **tense and access mechanism**:

| Layer | How you use it | Tense | Examples |
|---|---|---|---|
| **Handler keys you RETURN** | top-level keys of the returned object; called with `(input, output)` | **imperative** | `tool.execute.before`, `tool.execute.after`, `permission.ask`, `command.execute.before`, `shell.env`, `chat.message` |
| **Bus events you READ** | only inside the `event` handler, via `event.type` | **past-tense / `.updated` / `.idle`** | `command.executed`, `session.idle`, `session.updated`, `permission.asked`, `file.edited`, `lsp.updated` |

Same word, two layers: `command.execute.before` is a **handler key** you return;
`command.executed` is an **`event.type`** you match. `permission.ask` is a handler;
`permission.asked` is an event. Never write `event: { "session.idle": ... }` — the
`event` handler is one function that switches on `event.type`.

```js
return {
  "command.execute.before": async (input, output) => { /* imperative handler */ },
  event: async ({ event }) => {                          // bus reader
    if (event.type === "session.idle") { /* … */ }
  },
}
```

## Full handler-key set (`interface Hooks`)

Returnable keys, all optional: `dispose`, `event`, `config`, `tool` (a **map**,
not a function), `auth`, `provider`, `chat.message`, `chat.params`, `chat.headers`,
`permission.ask`, `command.execute.before`, `tool.execute.before`,
`tool.execute.after`, `shell.env`, `tool.definition`, and experimental
`experimental.{chat.messages.transform, chat.system.transform, provider.small_model,
session.compacting, compaction.autocontinue, text.complete}`.

- **There is no `stop` hook** — a community gist invents one; it does not exist.
  For "session finished," read `event` + `event.type === "session.idle"`.
- There is **`command.execute.before`** but no `command.execute.after` handler —
  the after-the-fact signal is the `command.executed` *event*.

## The `(input, output)` contract

Imperative handlers receive two args: **`input` is read-only; mutate `output` in
place; `throw` to block** the action.

| Handler | `input` (read) | `output` (mutate) | Block by |
|---|---|---|---|
| `tool.execute.before` | `{ tool, sessionID, callID }` | `{ args }` | `throw` |
| `tool.execute.after` | `{ tool, … }` | `{ title, output, metadata }` | — |
| `permission.ask` | the `Permission` | `{ status: "ask" \| "deny" \| "allow" }` | set `status` |
| `shell.env` | `{ cwd, … }` | `{ env }` | — |
| `command.execute.before` | `{ command, sessionID, arguments }` | `{ parts }` | `throw` |
| `tool.definition` | tool id | `{ description, parameters }` | — |

Gotcha: the field is `output.args`, keyed by tool. For `read` it's
`output.args.filePath`; for the **`apply_patch`** tool it's `output.args.patchText`
(there is no `filePath`). Don't assume a uniform arg shape.

## Where plugins live, and how they load

- `.opencode/plugins/` (project) or `~/.config/opencode/plugins/` (global) —
  top-level `*.ts`/`*.js` files auto-load at startup. Plural is the documented
  name; v1.18.33 also scans singular `plugin/` (`{plugin,plugins}` glob), so a
  singular directory is not why a plugin fails to load.
- **npm packages** via the config `"plugin": [...]` array — Bun-installed to
  `~/.cache/opencode/node_modules/`. Both bare and `@scoped` names work.
- **Local runtime deps**: add `.opencode/package.json`; OpenCode runs `bun install`
  at startup, then your plugin/tool can `import` them.

## PluginInput — the context you destructure

`PluginInput` is `{ client, project, directory, worktree, serverUrl, $ }` (plus
`experimental_workspace`). Two non-obvious points: `$` is **Bun's shell**, and for
structured logs the docs direct you to the SDK client — `client.app.log({ body: {
service, level, message, extra } })`, level `debug|info|warn|error` — instead of
`console.log`.

## Registering a custom tool from a plugin

The `tool` key is a **map** (`{ name: tool(...) }`), not a function — `import
{ tool } from "@opencode-ai/plugin"`, build arg schemas off `tool.schema.*`. A
plugin tool whose name matches a built-in **takes precedence**.

> This is the *programmatic* route. Filesystem-discovered custom tools in
> `.opencode/tools/*.ts` and the full `tool()` API are the **tools** facet
> (`/opencode-dev:tools`) — cross-reference, don't duplicate.

---

## Recipes (full code in `references/plugins.rst`)

| Goal | Key | Sketch |
|---|---|---|
| Block reading `.env` | `tool.execute.before` | `if (input.tool === "read" && output.args.filePath.includes(".env")) throw …` |
| Sanitize bash args | `tool.execute.before` | mutate `output.args.command` (e.g. `shescape`) |
| Notify on session done | `event` | `if (event.type === "session.idle") await $\`…\`` |
| Inject shell env | `shell.env` | `output.env.MY_API_KEY = "…"` |
| Persist context across compaction | `experimental.session.compacting` | `output.context.push("…")` or set `output.prompt` |
| Add a custom tool | `tool` map | `tool({ description, args, execute })` |

Starter scaffold pairing one imperative handler with the `event` reader:
[`assets/starter-plugin.ts`](assets/starter-plugin.ts).

## Reference files

| File | Contents |
|---|---|
| [references/plugins.rst](references/plugins.rst) | Verbatim `/docs/plugins/` (load order, all examples, logging, compaction) + the `interface Hooks` key set and `PluginInput` type surface |
