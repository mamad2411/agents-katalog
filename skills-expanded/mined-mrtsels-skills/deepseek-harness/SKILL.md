---
name: deepseek-harness
description: Use when working with dsh (DeepSeek Harness).
license: MIT
metadata:
  hermes:
    tags:
    - dsh
    - deepseek-harness
    - subagent
    - agent-harness
    - cordis
    - plugin
    related_skills:
    - coding-agents
    - hermes-agent
    - subagent-driven-development
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
  imported_from: hermes
---

# DeepSeek Harness (dsh)

## Overview

DeepSeek Harness (`dsh`, npm `@deepseek-ai/dsh`) is DeepSeek AI's open-source agent harness. Architecture: **everything is a plugin**, powered by the Cordis plugin framework (packages under `@deepseek-ai/*`). It is in **developer preview** — compatibility-breaking changes land frequently; pin the installed version when relying on it.

## When to Use

- User asks to install, run, debug, or extend DeepSeek Harness (`dsh`) — the `dsh web` / `dsh --profile headless|tui` CLIs
- User asks about dsh's subagent architecture, provider packages, or plugin development
- Building a Hermes-side integration that delegates tasks to dsh (load `references/subagent-dsh-plugin-design.md`)

## Install & Run

```sh
npm install -g @deepseek-ai/dsh      # global CLI → `dsh` on PATH
npx @deepseek-ai/dsh web             # run-on-demand (no install)
dsh web                              # Web UI, http://127.0.0.1:3080 (default port)
dsh --profile headless "task"        # one-shot: answer one task, print result, exit
dsh --profile tui                    # interactive TUI profile
dsh --profile web --port 8080        # custom port; --host to change bind
dsh plugin --profile <name> add <pkg>  # install a plugin into a profile
```

Profiles auto-initialize on first use under `$DSH_HOME/profiles/<name>` (default `~/.dsh/profiles/`). Shipped templates: `web` (`dsh-base` + `dsh-web-app`), `headless` (`dsh-base` + `dsh-headless`).

### Updating dsh (verified 2026-09-22)

Version channels diverge — check all three sources before touching the install:

```sh
gh release list --repo deepseek-ai/deepseek-harness --limit 5   # GitHub releases (all flagged Pre-release)
npm view @deepseek-ai/dsh dist-tags --json                        # latest / alpha / next
npm ls -g @deepseek-ai/dsh                                       # installed version
```

- npm `latest` = newest **rc**; the newest GitHub release may be a newer `-alpha`; npm `next` can carry an rc not yet released on GitHub. They routinely disagree.
- **Ask the user which channel they want** before `npm install -g @deepseek-ai/dsh@<tag>` — rc vs bleeding alpha is a real trade-off in a developer-preview project (pitfall 4).
- After any rc bump, re-check profile plugin peer deps: they must match the running rc (see the dsh-vision-router peer-dep fix below); `dsh plugin add` warnings tell you which are stale.
- A long-running `dsh web` must be restarted after upgrade, same as after plugin installs.

## Pitfalls (verified)

1. **`dsh web` auto-opens the browser since rc.8.** rc.7 and earlier only printed the URL; rc.8 added `openBrowser: true` (default) which spawns the OS default browser after the Loader tree settles. SSH launches suppress it. To disable: `dsh web --no-open`. **For the VS Code extension**: always pass `--no-open` when starting `dsh web` to prevent a browser window from popping up. Pre-rc.8 pitfall note: if "打不开", first verify the server is actually up (`lsof -nP -iTCP:3080 -sTCP:LISTEN`, `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3080/`) before assuming it crashed.
2. **`dsh web` is a foreground process** — Ctrl+C or closing the terminal stops it. A background instance started from a session dies with that session.
3. **Headless needs a configured model.** The model comes from the `agent-default-model` settings namespace — the SAME settings the web UI's Settings → Models writes. Run `dsh web` → Settings → Models (add DeepSeek API key + pick model) once, or configure `agent-default-model` in the profile patch; otherwise headless exits 1.
4. **Developer preview**: `latest` may be a `0.x.x-rc.N` tag; breaking changes between releases are expected.

### dsh-vision-router install (verified 2026-08-17, dsh 0.1.0-rc.6, plugin v1.4.4)

```sh
npx @deepseek-ai/dsh plugin --profile web add dsh-vision-router
# verify: npx @deepseek-ai/dsh --profile web --dump-config | grep vision-router
```

- **Peer deps do NOT auto-link into the profile** — install warns `missing peer @deepseek-ai/dsh-anonymous-user-id`, `dsh-llm-deepseek`, `sharp`. `pnpm install` in the profile says "up to date" and does NOT fix it. Manual fix (versions must match the running dsh rc):
  ```sh
  cd ~/.dsh/profiles/web && pnpm add "@deepseek-ai/dsh-anonymous-user-id@^0.1.0-rc.6" "@deepseek-ai/dsh-llm-deepseek@^0.1.0-rc.6" "sharp@^0.35.3"
  ```
- **A long-running `dsh web` must be restarted after install** to discover the plugin bundle (`kill <pid>` + relaunch). The in-browser "Vision Router is ready 🎉" onboarding card confirms load.
- **Verify in-browser**: chat model selector (lower-right) gains a "DeepSeek + 自动识图" ("+ Auto Vision") group — original DeepSeek group stays untouched. Settings → Plugins → Vision Router card should render (v1.4.4 fixed the blank rc.6 settings page; v1.4.1 and earlier crash Oh-DSH Desktop ≤0.1.5).
- Built-in OVH anonymous fallback works keyless (2 req/min/IP/model); Settings → Plugins → Vision Router shows "Connected" after a test. sharp 0.35.3 must be ≥0.35.3 for the pixel tools.

## Architecture (verified from source, master branch)

### Headless CLI contract (the Hermes-integration seam)

`packages/bundle/headless/src/index.ts` — one-shot direct Agent driver:
- Creates an Agent (`agents.create`, cwd = `process.cwd()`), submits the task as a user message, waits for idle, flushes the session.
- **stdout = final assistant text + `\n`** (only text blocks; no intermediate messages leak).
- **Exit code: 0 on `turn/end` reason `completed`, 1 otherwise**; errors go to stderr as `dsh: <code>: <message>`.
- No JSON output mode exists for headless — parse stdout as the answer.

### Subagent system (the pattern to copy when building integrations)

Relevant packages: `packages/subagent/` (subagent, tool-subagent, subagent-claude-code, subagent-codex, subagent-acp, subagent-fork-in-process, subagent-in-process-driver, subagent-spawn-in-process, tool-subagent-control, tool-subagent-report).

- **Naming trap**: there are NO packages named `tool-subagent-claude-code` / `tool-subagent-codex`. Those are instances of `@deepseek-ai/dsh-tool-subagent` configured with `provider: claude-code` / `provider: codex` and a distinct `toolName` (e.g. `subagent_claude_code`). The provider bodies are `@deepseek-ai/dsh-subagent-claude-code` and `@deepseek-ai/dsh-subagent-codex`.
- **Provider interface** (`dsh-subagent`): `SubagentProvider { name, capabilities, inheritsParentContext, start(request) → SubagentRun }`. Result contract: `SubagentResult { output: ContentBlock[], stopReason: 'completed'|'aborted'|'error'|'max-tokens'|'refusal' }`. Children get the parent session cwd (`resolveChildCwd`), NOT parent conversation (`inheritsParentContext: false`) — prompts must be self-contained.
- **claude-code provider**: official `@anthropic-ai/claude-agent-sdk` `query()`; accepts ONLY a `result` message with `subtype==='success' && !is_error && nonblank`; `persistSession: false`; `disallowedTools: ['AskUserQuestion']`; spawn hook puts the real CLI under a shared subprocess service for process-tree kill on dispose.
- **codex provider**: spawns `codex app-server --stdio` (JSON-RPC over stdio, protocol 0.147.0); handshake `initialize`/`initialized` → `thread/start {cwd, ephemeral:true}` → `turn/start` → wait `turn/completed`; final answer from `item/completed` notifications with `phase==='final_answer'` (null phase as fallback; `commentary` dropped); unattended approvals auto-responded (command/file change → `cancel` preferred over `decline`; permissions → empty; user input → empty; MCP elicitation → decline); `contextWindowExceeded` maps to `stopReason: 'max-tokens'` with partial output preserved.
- **tool-subagent wrapper**: model-facing tool with params `description` (3–5 words), `prompt` (self-contained), `run_in_background`; foreground waits and returns only final text; background returns a jobId; tool mounts on `subagent/provider-added` events; `maxDepth` default 3.
- **Cancellation/dispose pattern everywhere**: local AbortController → graceful close → terminate process tree in tiers (default 3s grace) → wait for whole-tree exit.

## Hermes ↔ dsh integration

The `subagent-dsh` plugin design (spawn `dsh --profile headless "task"` as a Hermes tool; mirror dsh's result contract: final answer only, exit-code mapping, killpg process-tree teardown, partial output on error) lives in `references/subagent-dsh-plugin-design.md`.

## dsh web HTTP/WS wire contract (building any client)

Verified envelope shapes, the real turn timeline (two `block-end`, no live `assistant/message`), trust-fence 403, and `session.history`-replay semantics live in `references/dsh-web-wire-contract.md`. Re-probe after dsh upgrades (`node scripts/probe.mjs --write-doc` in the dsh-for-vs-code repo).

## dsh web UI embedding (webview / alternative host)

The browser UI is a Cordis-plugin + slot system booted by `AppWebEntry(el).run()` from
`window.__DSH_BOOT__`; npm publish of the client stack is incomplete (peer deps 404), the upstream
repo is its own pnpm workspace (nested workspaces don't merge), and the connection client derives
its API base from `location.origin` (must be patched for webviews). Full architecture + the
recursive asset-fetch recipe + debug channel: `references/dsh-web-client-embedding.md`.

**User's UI direction for the dsh-for-vs-code extension (explicit, 2026-08-16):** reuse dsh's
native React components via vendored upstream source with **custom assembly adapted to the VS Code
sidebar** (like claude-code/codex extensions). Rejected: iframe-embedding the 3080 URL, and
self-built simplified webview UIs. Don't fall back to either without asking.

## Icon extraction (dsh-for-vs-code UI)

Physical icons (PNG/SVG) + 70 inline SVG components in `ui-primitives/src/icons/index.tsx`. Full extraction recipe, pitfalls, and standalone SVG output: `references/dsh-icon-extraction.md`.

## Host/Client Plugin Split Pattern

The dual-registration pattern for plugins with both Node.js host and browser client halves, including the critical pitfall of client entries blocking Node.js boot: `references/dsh-plugin-host-client-split.md`.

## dsh-for-vs-code Development Workflow

When modifying the dsh-for-vs-code extension: **read ARCH.md §7 first** to locate the exact file, then make targeted edits. Do NOT grep/search broadly — the user explicitly corrected this workflow. Full build pipeline, file location table, and pitfalls: `references/dsh-vscode-dev-workflow.md`.

Key insight: `shell.css` and `bridge.js` are template strings inside `scripts/build-web-shell.mjs`, not separate files. CSS/bridge changes require running `node scripts/build-web-shell.mjs` separately from `pnpm build`.

## Cordis Plugin Types: Dynamic vs Static

dsh has two ways to load Cordis plugins. Understanding the distinction is critical for plugin development.

### Installing a Plugin into a Local dsh Instance

```sh
# Install a plugin bundle into a profile
dsh plugin --profile <name> add <pkg-path-or-name>

# Examples
dsh plugin --profile web add ./my-plugin          # local directory
dsh plugin --profile web add dsh-vision-router    # npm package

# Verify installation
dsh --profile web --dump-config | grep my-plugin

# The plugin is symlinked into ~/.dsh/profiles/<name>/node_modules/
# Its cordis.patch.yml entries are applied at startup
```

**After install, restart `dsh web`** to load the new plugin.

### Host vs Client Plugin Split (Critical Pattern)

dsh has TWO Cordis loaders: one in Node.js (host) and one in the browser (client). Plugins must be registered in the right place:

| | Host Plugin | Client Plugin |
|---|---|---|
| **Runs in** | Node.js process | Browser webview |
| **Registered via** | `cordis.patch.yml` insert | `package.json` `dsh.client` declaration |
| **Discovered by** | Cordis loader at boot | `dsh-client-modules` scanner |
| **Can depend on** | `tools`, `fs`, `llm`, etc. | `slots`, `timer`, `remote`, etc. |
| **CANNOT depend on** | Browser-only services | Node.js-only services |

**Pitfall: Client entries in cordis.patch.yml block Node.js boot.**
If you put a client plugin in `cordis.patch.yml` with `inject: ['slots']`, the Node.js Cordis loader tries to activate it at boot and fails because `slots` only exists in the browser. The error is:
```
dsh: 1 entry did not activate
dsh-file-attach/client: pending (waiting for service: slots)
```

**Correct pattern — dual registration:**

```yaml
# cordis.patch.yml — ONLY host entries
- insert:
    - id: my-plugin
      name: my-plugin
      inject: ['tools']     # host-side services only
```

```json
// package.json — client declaration for dsh-client-modules discovery
{
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" },
    "client": {
      "platform": "web",
      "inject": ["@deepseek-ai/dsh-client-connection"]
    }
  }
}
```

The `dsh-client-modules` package (part of `dsh-web-app` bundle) scans all loader entries for packages with `dsh.client` in their `package.json`. It composes the browser boot manifest (`window.__DSH_BOOT__`) and serves `/plugins/<id>/client.js` routes. Client plugins are loaded by the **browser's** Cordis loader, not the Node.js one.

### Static Plugins (cordis.yml insert)

Standard Cordis plugins declared in `cordis.patch.yml` via `insert` rows. Loaded at process startup by the Cordis loader.

```yaml
# cordis.patch.yml
- insert:
    - id: my-plugin
      name: '@deepseek-ai/dsh-my-plugin'
      inject: ['tools']
```

```ts
// TypeScript module with standard Cordis exports
import type { Context } from '@deepseek-ai/cordis'
export const name = 'my-plugin'
export const inject = ['tools']
export function apply(ctx: Context) {
  ctx.tools.register(/* ... */)
}
```

- Language: **TypeScript** with proper imports
- Loading: process startup, `cordis.patch.yml` declaration
- Dependency injection: `inject: ['tools']` (declaration)
- Service access: `ctx.tools`, `ctx.fs`, `ctx.llm` etc.
- Lifecycle: fiber state machine (PENDING → LOADING → ACTIVE → DISPOSED)
- Cleanup: automatic via `ctx.on`/`ctx.effect` disposer pattern
- Publishing: npm package with `dsh.bundle` manifest → `dsh plugin add`

### Dynamic Plugins (cordis_define / cordis_run)

Runtime-injected plugins via `@deepseek-ai/dsh-tool-cordis` toolset. Code is passed as **plain JavaScript function bodies** (no TypeScript, no imports) to `cordis_define`, then activated via `cordis_run`.

```js
// host.js — pure JS function body, no imports
return {
  apply(ctx) {
    harness.handle('my-method', async (args) => { /* ... */ })
    ctx.on('agent/pre-step', async (payload, next) => { /* ... */ })
  }
}
```

```js
// client.js — pure JS function body
return {
  inject: ['timer'],
  apply(ctx) {
    host.call('my-method', { sessionId })  // calls harness.handle on host
    // ... React UI via slots.inject
  }
}
```

- Language: **plain JavaScript function bodies** (no imports, no TypeScript compilation)
- Loading: runtime via `cordis_define` (define) + `cordis_run` (activate)
- VM sandbox: code runs in `node:vm` sandbox (host) or browser Cordis context (client)
- RPC: `harness.handle(method, fn)` (host) ↔ `host.call(method, args)` (client)
- Client code: injected into browser by `build-web-shell.mjs`
- Lifecycle: define → run → stop → undefine (process-memory only, lost on restart)

### Key Difference: RPC Mechanism

| | Static Plugin | Dynamic Plugin |
|---|---|---|
| **Host→Client** | Cordis events/slots | `host.call()` (client) |
| **Client→Host** | Cordis Remote / gateway fetch | `harness.handle()` (host) |
| **harness.handle** | ❌ Not available | ✅ VM sandbox API |
| **host.call** | ❌ Not available | ✅ Client sandbox API |
| **ctx.tools.register** | ✅ Model-visible tools | ✅ Also works |
| **ctx.on events** | ✅ Standard Cordis | ✅ Also works |

### Conversion Pitfall: harness.handle is Dynamic-Only

`harness.handle(method, fn)` is a **VM sandbox context API** provided by `cordis-host-runner` — it only exists inside the dynamic plugin sandbox. It is NOT available in static plugins loaded by the Cordis loader.

**To convert a dynamic plugin to static:**
1. Replace `harness.handle` with `ctx.tools.register` (model-visible tools) or a custom Service
2. Replace `host.call` (client) with gateway fetch or Cordis Remote
3. The extension side may need adaptation if it uses `dynamicCordisRunner.invoke`

### Harness-Specific Events (Not in Base Cordis)

These events are Harness-specific, not in the base `@deepseek-ai/cordis` Events type:

- `agent/pre-step` — waterfall, inject messages before model request
- `session/event` — emit, session lifecycle events (step/end, turn/end, etc.)
- `session/disposed` — emit, cleanup when session is destroyed

When using these in TypeScript, cast with `as any` since they're not in the base Events interface:
```ts
ctx.on('agent/pre-step' as any, async (payload: any, next: () => Promise<any>) => { ... })
```

### TypeScript for Dynamic Plugins

Dynamic plugin code is plain JS function bodies — TypeScript compilation doesn't directly apply. However, you CAN:
1. Write TypeScript source with proper types
2. Compile to JS with `tsc`
3. Extract the `apply` function body from compiled output
4. Pass to `cordis_define` as `code.host` / `code.client`

This gives type safety during development while keeping the dynamic loading mechanism.

### Client Plugin Runtime Checks (Not Module-Level inject)

Client plugins that need browser-only services (`slots`, `timer`) MUST NOT declare `inject` at the module level:
```ts
// ❌ WRONG — blocks Node.js boot
export const inject = ['slots', 'timer']
export function apply(ctx) { ... }

// ✅ CORRECT — runtime check
export function apply(ctx) {
  const slots = ctx.get('slots')
  if (slots === undefined) return  // silently skip in Node.js
  // ... use slots
}
```

The `dsh-client-modules` scanner handles browser-side dependency ordering via `dsh.client.inject` in `package.json` (module load order in the browser), not Cordis service injection.

## Vendor Release Compatibility Review (upstream rc upgrades)

When a new dsh rc lands in the vendor submodule, review compatibility with the dsh-for-vs-code extension before rebuilding. Full methodology and the rc.8 example: `references/dsh-vendor-release-review.md`.

**Quick checklist:**
1. `git log --oneline <current-head>..<new-commit>` — find the release commit and list all non-merge commits
2. Diff stat for each significant commit — focus on `packages/client/`, `packages/bundle/web-app/`, `packages/bundle/base/`, `packages/subagent/`
3. Check `resolveBase` in `packages/client/connection/src/client/rpc.ts` and `web-api-client.ts` — adapter seam breakage = build failure
4. Check `cordis.patch.yml` changes — new entries may need trimming in the build graph
5. Check slot declarations (`SlotMap` interface additions in `contract/slots.ts`) — new slots may need occupant fallbacks
6. Check `connection` package.json — peerDependency reshuffling affects vendor rebuild
7. Check `apps/web/vite.config.ts` — alias/define changes affect the web build
8. Run `pnpm build:lib:client` → `pnpm build:shell` → `node scripts/smoke-shell.mjs` for end-to-end verification

## Source map for future development

```
packages/subagent/subagent-*          # provider implementations
packages/subagent/tool-subagent/      # model-facing delegation tool
packages/subagent/subagent/           # shared service: provider iface, result contract, settleRunResult, subprocessRunHandle
packages/subprocess/subprocess/       # spawn service, resolveExecutable, scrubbedParentEnv
packages/bundle/headless/             # one-shot runner (stdout = answer, exit 0/1)
packages/boot/app-boot/src/profile.ts # profile discovery, PROFILE_TEMPLATES
apps/cli/src/args.ts                  # launcher arg parsing (flags first, rest to app)
```

## Verification Checklist

- [ ] `dsh --version` works after install
- [ ] `dsh web` serves HTTP 200 on 127.0.0.1:3080 (curl, not browser assumption)
- [ ] Model configured before first headless call (else exit 1)
- [ ] For integration work: read the provider package source before mirroring its contract
