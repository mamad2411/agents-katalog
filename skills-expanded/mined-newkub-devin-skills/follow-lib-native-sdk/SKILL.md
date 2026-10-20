---
name: follow-lib-native-sdk
description: Native SDK (@native-sdk/cli) desktop apps — TS + .native markup, compiled native, no JS runtime
argument-hint: "[feature-or-component]"
related:
  - follow-create-desktop-tauri
  - follow-lib-gpui-kit
  - follow-lang-typescript
  - follow-lang-zig
  - follow-create-mobile
  - follow-my-techstack
  - improve
  - deep-research
  - follow-devin-global-skills

---

## Goal

Build and maintain native desktop applications correctly with the Native SDK (Vercel Labs) — TypeScript app logic in `src/core.ts` + declarative markup in `.native` files, then ahead-of-time compiled (AOT) to native code so the shipped binary has **no browser/WebView/JS runtime/interpreter**

## Scope

When you want a truly native desktop app (Metal/Direct2D/software renderer), not a webview shell — the `native` CLI, `ts-core`/`zig-core` templates, the app model (TEA/Elm), markup, Cmd/Sub effects, persistence/SQLite, automation, testing, packaging, security

- Boundary: Tauri = Rust backend + web frontend (webview shell) → `/follow-create-desktop-tauri`; GPUI Kit = Rust-only components/entity model → `/follow-lib-gpui-kit`; Native SDK = TS+markup AOT, no runtime in the binary
- Mobile (iOS/Android) is **Experimental** — verified on simulators/emulators only; desktop is the mature surface
- WebViews still work as an optional path (embed a web page/host an existing frontend) — not the default path

## Facts (verified 2026-10-13)

- Repo `vercel-labs/native` (Apache-2.0, ~7.8k stars, active); npm `@native-sdk/cli` 0.10.1; docs at native-sdk.dev
- Requires **Zig 0.16.0** (the CLI downloads it into `~/.native/toolchains/` with checksum) + **Node 24+** for the TS scaffold/checker — Node is used only at build/dev time and is not in the binary
- Platforms: macOS (primary, Metal), Windows (Direct2D/DirectWrite + software fallback), Linux (software renderer via blit); iOS/Android host-tier (experimental, multi-window on desktop only)
- The state system is TEA: `Model` readonly record + `Msg` union + `update(model,msg): Model | [Model, Cmd<Msg>]`; the view derives from the model through markup
- Every app embeds an automation server (file-based protocol) — snapshot/drive/screenshot possible when built with `-Dautomation=true`
- `native skills get <core|native-ui|ts-core|ts-services|automation|zig>` returns deep content from the installed CLI (discovery stub via `npx skills add vercel-labs/native`)

## Execute

### 1. Setup & Scaffold

> Goal: a project ready for `native dev`

1. `npm install -g @native-sdk/cli` then `native version` (if npm is broken on this machine — see Rules §6)
2. Create the app:
   ```sh
   native init my_app                      # ts-core default: app.json + src/app.native + src/core.ts
   native init my_app --template zig-core  # src/main.zig + src/tests.zig (core is Zig)
   native init my_app --frontend vite      # alternative path: host a web frontend (next|vite|react|svelte|vue)
   native init --full                      # adds app-owned build files + .github/workflows/ci.yml
   ```
3. Check the toolchain: `native doctor`; validate the manifest: `native validate app.json`
4. The build graph lives under `.native/build/` — never edit it by hand; detect the language from the files (`src/main.zig` = zig-core)

### 2. Core (TypeScript TEA)

> Goal: state + messages + effects correct per the compiled subset

1. `src/core.ts` declares `Model` (readonly record), `Msg` (discriminated union), `initialModel()`, `update(model, msg)` — the full subset is in `best-practices/ts-core-subset.md`
2. Effects go through the `Cmd` vocabulary: `now/delay/fetch/readFile/writeFile/clipboard*/spawn/showNotification/quitApp/persist/store.set/db.query/Cmd.request/Cmd.batch/...`; subscriptions via `subscriptions(model): Sub<Msg>`, e.g. `Sub.timer("tick",1000,"tick")`
3. Work outside the subset (regex, JSON, Map/Set, Date, classes, child_process) → move it into `src/services/` (full ordinary TS, running on the supervised carrier `<app>_services`) and call it via `Cmd.request(name,payload,{key,ok,err})` or the typed client from `@native-sdk/services`
4. Text is bytes — use `utf8Bytes`/`asciiBytes` from `@native-sdk/core`; byte offsets, not code units
5. Modules: relative imports under `src/` with real filenames, no `../`, no cycles, no `export default`

### 3. Markup (`.native`)

> Goal: declarative UI bound to the model

1. Main elements: `row column stack panel card scroll list grid tabs table accordion alert dialog drawer sheet text badge button toggle list-item checkbox slider progress text-field search-field combobox markdown image avatar terminal chart status-bar separator` — full list in `best-practices/native-ui-markup.md`
2. Bindings `{expr}` (one expression per attribute), events `on-press="increment"` / `on-press="toggle:{t.id}"`, control flow `<for each= key= as=>` `<if test=>/<else>`
3. The expression language is limited: `+ - * / == != and or not ++` + a 17-function lib (`upper lower trim min max abs round floor ceil plural pad fixed thousands percent date time datetime`) — no method calls/ternaries
4. Layout: `gap padding grow width height min/max-width main cross columns`; component reuse: `<template name= args=>` + `<use template=>` + `<slot/>` + `<import src="src/components/...">`
5. Theming via token names (`background surface text text_muted border accent destructive success warning info focus_ring scrim disabled`) — pack `house`/`geist` in `app.json` + `themeState(model)`

### 4. Data & Native Platform

> Goal: persist/state/native features through capability declarations in `app.json`

1. Capability `persist` → `Cmd.persist()` (debounce 500ms, snapshot.nsd + .bak, `migrate(snapshot, fromVersion)`)
2. Capability `store` → key-value: `Cmd.store.set/get/delete/scan/setMany` (key ≤512B, value ≤1MiB)
3. Capability `sqlite` → `app.db` WAL; migrations in `src/schema/NNNN_name.sql` + `native db new-migration|status|reset --yes`; named queries in `src/queries.sql` (`-- name: x :live`) → generated `Cmd.qName(params, route)` + `Sub.qName`; bounds 64 params/1MiB
4. Windows: `windows(model): readonly WindowDescriptor[]` (scene model, ≤16, `close_policy quit|hide` — hide on Windows requires the `"tray"` capability); menus ≤16/128 items; shortcuts ≤64; tray = macOS/Windows only (Linux `UnsupportedService`)
5. File paths outside the app roots require `filesystem` permission; external links must be allowlisted in the security policy

### 5. Test & Automate

> Goal: confirm real behavior for both humans and agent loops — details in `best-practices/automation-testing.md`

1. `native check [--strict]` (type-checks the core subset) → `native test` (TS unit via `@native-sdk/core/testing` `NativeApp.start()`: `findWidget/click/setText/menu/frame/snapshot/effects/verifyReplay`)
2. Automation: `native build -Dautomation=true` then the file protocol under `.zig-cache/native-sdk-automation/` (`snapshot.txt`, `accessibility.txt`, `screenshot-<label>.png`, `command-<n>.txt` queue) — CLI: `native automate list|snapshot|screenshot|reload|assert [--timeout-ms]|widget-click|menu-command|shortcut|bridge '<json>'`
3. Record/replay: `NATIVE_SDK_SESSION_RECORD=1` / `REPLAY=1`; asserts use a regex subset (no groups/alternation)
4. CI tiers from `--full`: tier1 `-Dplatform=null` unit; tier2 Linux Xvfb + `-Dautomation=true`; tier3 macOS GUI — golden screenshots byte-compare only on the same runner image

### 6. Package & Ship

> Goal: distribution-ready artifacts — details in `best-practices/packaging-platform-security.md`

1. `native build` → ReleaseFast at `zig-out/bin/`; `native package --target macos|linux|windows|ios|android`
2. macOS: `.app` + DMG (`--archive`), signing `--signing adhoc|identity --identity --entitlements`, notarize `--notarize --notary-profile` (only macOS can sign)
3. Icons: one square `assets/icon.png/.svg` → every format automatically; release-time updates: own signed Ed25519 updater (`native update keygen|sign`, manifest `updates{feed_url,public_key}` HTTPS, macOS only)

## Rules

### 1. No-Runtime Reality

- The shipped binary has no JS runtime/interpreter — `src/core.ts` is compile-AOT only; never expect dynamic import, eval, or npm runtime in the core
- If you need full ordinary TS → services (`src/services/`), not the core

### 2. Subset Discipline

- core.ts may use only the compiled subset (read `best-practices/ts-core-subset.md` before writing) — violations fail the checker, not the runtime
- Memory is a 1 MiB per-dispatch arena — never hold state across dispatches outside the Model

### 3. Platform Honesty

- iOS/Android = experimental — never sell it as production mobile; multi-window on desktop only; no tray on Linux; Chromium/CEF on macOS only; registered fonts on mobile = unverified
- The Windows renderer is early development for packaging — test on real hardware before shipping

### 4. Automation & Test Gate

- Every feature must pass `native check` + `native test` before claiming done; agent-driven verification uses `native automate` snapshot/assert, not the naked eye
- Never edit `.native/build/` or generated artifacts directly

### 5. Composition

- Webview-shell apps (existing frontend + Rust backend) → `/follow-create-desktop-tauri`; Rust-native GUI → `/follow-lib-gpui-kit`; this skill covers the Native SDK only — the SDK's current deep content is read via `native skills get <name>` (vendor-side SSOT)

### 6. Broken-npm Escape (this machine)

- `@native-sdk/cli` cannot be installed via npm when mise node's bundled npm is broken (npm-cli.js missing), and `bunx @native-sdk/cli` also fails ("could not find skills/ or skill-data/ near the native-sdk executable") — use the docs dumps at `AppData\Local\Temp\nsd\*.md` (47-page mirror from native-sdk.dev via Lightpanda) as the reference until npm is fixed (`mise uninstall node@26.11.1 && mise install node@26.11.1` + trim PATH to <8191 chars)

## Expected Outcome

- A new app from `native init` runs with `native dev` and builds with `native build`
- core.ts and markup are subset-correct, effects are Cmd/Sub, and full-TS work is properly separated into services
- Test tiers pass + `native automate snapshot/assert` confirms real behavior
- The user understands the boundary: native AOT with no runtime, mobile experimental, platform caveats clear
