---
name: streamdeck-general
description: 'Foundational Stream Deck plugin workflow: prerequisites (Node 24+, Stream Deck 7.1+, @elgato/cli), `streamdeck create` scaffold, .sdPlugin / src project layout, the dual runtime (Node.js plugin + Chromium property inspector), hot-reload + watch, debugging via Node inspector, logging, linting. USE FOR: starting a new Stream Deck plugin, project file layout, .sdPlugin directory, src/plugin.ts entry, hot reload, watch script, attaching VS Code debugger, streamDeck.logger, ESLint/Prettier config, plugin lifecycle, plugin runtime architecture, Node version pinning, what file goes where.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "plugin-development", "nodejs", "typescript", "workflow"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — General Foundations

> **Foundational skill.** Load this before any other `streamdeck-*` skill.
> The sibling skills (`-actions`, `-property-inspector`, `-oauth`, etc.)
> assume the project layout, runtime model, and CLI/watch loop documented
> here.

## Purpose

Establish a clean, reproducible Stream Deck plugin project layout, a fast
edit/build/test loop, and the mental model of the two JavaScript runtimes
that compose every Stream Deck plugin. Every plugin in this repo should
follow these conventions so other agents, scripts, and humans can pick
the project up later without reverse-engineering it.

**Scope:**

- Prerequisites (Node, Stream Deck app, CLI)
- The dual-runtime architecture (Node.js + Chromium)
- Project file layout — what each file does and what to gitignore
- The `streamdeck create` scaffold and its outputs
- The build / watch / restart / debug loop
- Logging conventions (`streamDeck.logger`)
- Linting conventions (`@elgato/eslint-config`, `@elgato/prettier-config`)
- Version pinning (Stream Deck app, Node, SDK)

**Out of scope** (covered by sibling skills):

- Actions, keys, dials, lifecycle events → `streamdeck-actions`
- Property inspector HTML / sdpi-components → `streamdeck-property-inspector`
- Manifest JSON reference → `streamdeck-manifest`
- CLI command reference (every flag of every command) → `streamdeck-cli`
- OAuth2 flow → `streamdeck-oauth`
- Devices / deep linking / system events → `streamdeck-system-devices`
- Packaging, DRM, marketplace submission → `streamdeck-publishing`

---

## 1. Prerequisites

| Requirement | Minimum | Notes |
|---|---|---|
| Node.js | **24.x** | The CLI requires Node 24+. The plugin itself runs in a Stream Deck-managed Node 20 or 24 runtime — set in `manifest.Nodejs.Version`. |
| Stream Deck app | **7.1** | Older versions are missing the v2 SDK features. Some features (passive deep-links, device-change events) require 7.0+ specifically. |
| Stream Deck device | Any | Stream Deck Mobile is free on iOS/Android if you don't own a physical device. |
| `@elgato/cli` | latest | `npm install -g @elgato/cli@latest` — provides the `streamdeck` (or `sd`) command. |
| VS Code | recommended | First-class Node debugger; integrates with the SDK linter/prettier. |

Verify:

```pwsh
node -v          # v24.x.x
streamdeck -v    # CLI version
```

The shorthand alias `sd` works everywhere (`sd create` === `streamdeck create`).

---

## 2. Runtime architecture — the two-process model

A Stream Deck plugin is **two** JavaScript runtimes managed by the Stream
Deck app. Internalize this — it's the single most common source of
confusion.

```
┌──────────────────────────────────────────────────────────────┐
│  Stream Deck app (native, hosts both runtimes)               │
│                                                              │
│   ┌──────────────────────────┐    ┌────────────────────────┐ │
│   │  Plugin (Node.js)        │    │  Property Inspector    │ │
│   │  src/plugin.ts           │◄──►│  (Chromium WebView)    │ │
│   │  - actions, events       │    │  ui/*.html             │ │
│   │  - global state          │    │  - HTML/CSS/JS         │ │
│   │  - HTTP / OAuth tokens   │    │  - sdpi-components     │ │
│   │  - filesystem, fs/promises│    │  - DOM only            │ │
│   │  Talks to SD via WebSocket    │  Talks to plugin via   │ │
│   │  (the SDK wraps this)    │    │  sendToPlugin messages │ │
│   └──────────────────────────┘    └────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

Implications:

- **Don't `import fs from "fs"` in property-inspector code.** It runs in
  a browser. Move filesystem / network work to the plugin runtime and
  message the result over via `sendToPlugin` / `sendToPropertyInspector`.
- **Don't store secrets in property-inspector HTML.** Even local files
  are world-readable to anyone with disk access. Use **global settings**
  written from the plugin side (see `streamdeck-oauth` and the settings
  section in `streamdeck-property-inspector`).
- **`onSystemDidWakeUp` only fires in the plugin runtime**, never the
  property inspector.
- The plugin runtime has a **single instance per plugin**. Action
  classes are singletons; all instances of an action on the user's
  canvas are handled by the one `SingletonAction` subclass.

Runtime versions (Stream Deck 7.3 at time of writing):

| Component | Pinned versions |
|---|---|
| Node.js (plugin) | 20.20.0 or 24.13.1 (pick via `manifest.Nodejs.Version`: `"20"` or `"24"`) |
| Chromium (property inspector) | 130.0.0.0 |
| SDK package | `@elgato/streamdeck` v2+ (required for SDKVersion 3 DRM) |

**Pin a Node version per plugin.** Don't rely on whatever's latest — the
SDK abstracts most of it, but native modules and `globalThis.fetch`
behavior differ between 20 and 24.

---

## 3. Project file layout

The `streamdeck create` wizard scaffolds this:

```
<project-slug>/
├── com.<author>.<plugin-slug>.sdPlugin/     # compiled plugin (ships to user)
│   ├── bin/                                 # compiled JS from src/ (gitignore? — see below)
│   ├── imgs/                                # action/category/marketplace icons
│   ├── logs/                                # runtime logs (gitignore)
│   ├── ui/                                  # property inspector HTML
│   │   └── <action>.html
│   └── manifest.json                        # plugin metadata (the source of truth)
├── src/                                     # TypeScript source — edit here
│   ├── actions/
│   │   └── <action-slug>.ts
│   └── plugin.ts                            # entry point — register + connect
├── package.json
├── rollup.config.mjs                        # bundles src/ → .sdPlugin/bin/
└── tsconfig.json
```

### What each piece is for

| Path | Role | Edit by hand? |
|---|---|---|
| `*.sdPlugin/` | The actual plugin that Stream Deck loads. **Folder name MUST equal the plugin UUID with `.sdPlugin` suffix.** | Only `manifest.json`, `imgs/`, `ui/` |
| `*.sdPlugin/bin/` | Rollup output. Regenerated on every build. | Never — gitignore optional |
| `*.sdPlugin/manifest.json` | Declares actions, UUIDs, OS/Node versions, icons, profile bundles. See `streamdeck-manifest`. | Yes |
| `*.sdPlugin/ui/*.html` | One HTML file per action's property inspector. See `streamdeck-property-inspector`. | Yes |
| `*.sdPlugin/imgs/` | Icons (PNG/SVG/WEBP, never GIF). Paths in manifest are extension-less. | Yes |
| `*.sdPlugin/logs/` | Runtime logs from `streamDeck.logger`. Auto-rotated. | Gitignore |
| `src/plugin.ts` | Entry — register every action, then `streamDeck.connect()`. | Yes |
| `src/actions/*.ts` | One class per action, extending `SingletonAction`. | Yes |
| `package.json` | Scripts: `build`, `watch`. Deps: `@elgato/streamdeck`. | Yes |
| `rollup.config.mjs` | Build config. Usually leave alone. | Rare |
| `tsconfig.json` | TS config. `experimentalDecorators` + `useDefineForClassFields: false` required for `@action(...)`. | Rare |

### Recommended `.gitignore`

```gitignore
# Build output
**/*.sdPlugin/bin/

# Runtime logs
**/*.sdPlugin/logs/

# Dependencies & env
node_modules/
.env*
*.log

# Sourcemaps and packaged installer artifacts
*.js.map
*.streamDeckPlugin
dist/
```

### Recommended `.sdignore`

The `streamdeck pack` command honors a `.sdignore` file (same syntax as
`.gitignore`) to exclude files from the shipped `.streamDeckPlugin`
installer. Default exclusions: `.git/`, `/.env*`, `*.log`, `*.js.map`.
Add anything that's developer-only:

```gitignore
# .sdignore — files excluded from packaged plugin
.git/
.env*
*.log
*.js.map
README.md            # optional — Marketplace listing has its own description
*.test.*
__tests__/
```

---

## 4. The scaffold — `streamdeck create`

The interactive wizard prompts for:

| Prompt | Constraint | Example |
|---|---|---|
| Author name | Free text | `Rick Wilson` |
| Plugin name | Display name | `Hello World` |
| Plugin UUID | Reverse-DNS, lowercase, `a-z 0-9 . -` only | `com.yourhandle.hello-world` |
| Description | Free text | `Demonstrates the SDK.` |

**The UUID is permanent.** Once published to the Marketplace it must
never change — users' on-device configurations are keyed by it. Pick
carefully:

```
com.<your-org-or-domain>.<plugin-slug>
└── reverse-DNS                ── lowercase, hyphens OK
```

After the wizard the project is auto-linked to Stream Deck and the
`watch` script is suggested. `streamdeck dev` mode is enabled
automatically, exposing the property-inspector debugger at
<http://localhost:23654/>.

---

## 5. The edit/build/test loop

```pwsh
npm run watch          # one-shot: rebuild on save AND restart plugin in Stream Deck
```

Under the hood `watch` is wired to:

```json
"watch": "rollup -c -w --watch.onEnd=\"streamdeck restart <PLUGIN_UUID>\""
```

When watching, changes to either `src/` (TypeScript) or
`*.sdPlugin/manifest.json` (or anything else in `*.sdPlugin/`) hot-reload
automatically. To stop, `Ctrl+C`.

The two-command equivalent (useful in CI, or when watch is misbehaving):

```pwsh
npm run build                        # rollup -c
streamdeck restart com.yourhandle.hello-world
```

Other lifecycle commands (see `streamdeck-cli` for full reference):

| Command | What it does |
|---|---|
| `streamdeck link <path>` | Register a `.sdPlugin/` directory with Stream Deck (no copy — symlinks) |
| `streamdeck restart <uuid>` | Stop + start the plugin in Stream Deck |
| `streamdeck stop <uuid>` | Stop the plugin without removing it |
| `streamdeck dev` | Enable property-inspector remote debugger |
| `streamdeck validate <path>` | Schema-check the manifest + project structure |
| `streamdeck pack <path>` | Build the distributable `.streamDeckPlugin` installer |

---

## 6. Debugging

### Plugin (Node.js) debugger — VS Code

The Stream Deck app launches the plugin's Node process with
`--inspect=<auto-port>` enabled by default. To attach:

1. Open Quick Open: `Ctrl+P` (or `Cmd+P`).
2. Type `> Debug: Attach to Node Process` → `Return`.
3. Pick the `node20` (or `node24`) process matching your plugin's PID.

Breakpoints in `src/**/*.ts` are honored as long as the rollup build
emits sourcemaps (the default).

Override the inspector port in `manifest.json`:

```json
{
  "Nodejs": { "Version": "20", "Debug": "enabled" }
}
```

Values for `Debug`:

| Value | Behavior |
|---|---|
| (absent) | Auto-pick a free port (recommended in dev). |
| `"enabled"` | Always enable, auto-port. |
| `"break"` | Enable + pause execution until debugger attaches (`--inspect-brk`). |

### Property inspector (Chromium) debugger

Requires `streamdeck dev` to be enabled (it is by default after `create`).
Visit <http://localhost:23654/> in your browser to see a list of pages —
each visible property inspector appears here. Click → opens DevTools
against that PI's HTML.

> The property inspector must be **visible in Stream Deck** for its page
> to appear in the list. Open the action in the Stream Deck app first.

---

## 7. Logging — `streamDeck.logger`

Always log via the SDK logger, not `console.log`. The SDK logger writes
to a rotated file and (in dev) the inspector console; `console.log`
only hits one of the two targets and is easy to miss.

```ts
import streamDeck from "@elgato/streamdeck";

streamDeck.logger.info("Hello");
streamDeck.logger.warn("Heads up");
streamDeck.logger.error("Something broke", err);
streamDeck.logger.debug("Verbose details");
streamDeck.logger.trace("Extremely verbose");
```

### Log levels

```ts
import { LogLevel } from "@elgato/streamdeck";

streamDeck.logger.setLevel(LogLevel.DEBUG);
```

| Level | Default in dev | Default in production |
|---|---|---|
| ERROR | ✓ | ✓ |
| WARN | ✓ | ✓ |
| INFO | ✓ | ✓ |
| DEBUG | ✓ | — |
| TRACE | — | — |

### Scoped loggers (breadcrumbs)

```ts
const log = streamDeck.logger.createScope("Main");
log.info("hi");                      // "Main: hi"

const child = log.createScope("Nested");
child.info("hi");                    // "Main->Nested: hi"
```

### Log file locations

| OS | Path |
|---|---|
| Windows | `%appdata%\Elgato\StreamDeck\logs\StreamDeck0.log` |
| macOS | `~/Library/Logs/ElgatoStreamDeck/StreamDeck0.log` |

Plus per-plugin logs at `*.sdPlugin/logs/` inside the project folder.

**Rotation:** 10 files, 10 MiB each. Numbered `StreamDeck0.log` (newest)
through `StreamDeck9.log` (oldest).

> ⚠️ **Uninstalling the plugin deletes its logs.** If you're chasing a
> bug, copy `logs/` somewhere safe before the user uninstalls.

---

## 8. Linting — `@elgato/eslint-config` + `@elgato/prettier-config`

The Elgato team publishes opinionated configs that match the SDK's own
codebase. Install:

```pwsh
npm install --save-dev @elgato/eslint-config @elgato/prettier-config eslint prettier
```

### ESLint

`eslint.config.js`:

```js
import { config } from "@elgato/eslint-config";

export default config.recommended;   // or config.strict
```

Run:

```pwsh
npx eslint . --max-warnings 0
```

| Config | When to use |
|---|---|
| `config.recommended` | Default. Solid baseline. |
| `config.strict` | Stricter type-safety rules (explicit return types, member ordering). Use for plugins you intend to publish. |

### Prettier

`prettier.config.js`:

```js
import config from "@elgato/prettier-config";
export default config;
```

Defaults: tabs, width 4 (2 for YAML), single quotes off, trailing
commas everywhere, printWidth 120, semi on. Run on save in VS Code via
the `esbenp.prettier-vscode` extension.

Add to `package.json` scripts:

```json
{
  "scripts": {
    "lint": "eslint . --max-warnings 0 && prettier . --check",
    "format": "eslint . --fix && prettier . --write"
  }
}
```

---

## 9. Version-targeting checklist

Before you commit a plugin, every project's README should record:

```
Stream Deck app: 7.x (minimum X.Y as set in manifest)
Node.js runtime: 20 or 24 (manifest.Nodejs.Version)
SDK package:     @elgato/streamdeck@^2
SDKVersion:      2 (no DRM) or 3 (DRM, requires app 6.9+)
```

These four lines + the plugin UUID are enough for anyone (you, in six
months) to reproduce a build.

---

## 10. Security baseline

These rules are non-negotiable and apply to every Stream Deck plugin:

| Rule | Why |
|---|---|
| **Never embed private API keys / shared secrets in the manifest, source, or `imgs/`** | Plugins ship to the user's machine; everything is readable. Use OAuth or per-user API keys requested at runtime — see `streamdeck-oauth`. |
| **Never store user secrets in action settings** | Action settings are included in profile exports. Use **global settings**. |
| **Treat the property inspector as untrusted UI** | It's a sandboxed WebView. Sanitize anything coming back via `sendToPlugin`. |
| **Validate deep-link payloads** | The `streamdeck://plugins/message/<uuid>/...` URL is exposed to every other app on the user's machine. Anyone can POST to your handler. Validate `state` on OAuth callbacks; reject unexpected paths. |
| **Keep deep-link payloads <2,000 chars** | Hard limit. For larger data, use a local WebSocket. |

---

## See Also

- Official getting started: <https://docs.elgato.com/streamdeck/sdk/introduction/getting-started>
- Your first changes: <https://docs.elgato.com/streamdeck/sdk/introduction/your-first-changes>
- Plugin environment: <https://docs.elgato.com/streamdeck/sdk/introduction/plugin-environment>
- Logging guide: <https://docs.elgato.com/streamdeck/sdk/guides/logging>
- Linting style guide: <https://docs.elgato.com/streamdeck/sdk/style-guide/linting>
- Sibling skills: `streamdeck-manifest`, `streamdeck-actions`, `streamdeck-property-inspector`, `streamdeck-cli`
