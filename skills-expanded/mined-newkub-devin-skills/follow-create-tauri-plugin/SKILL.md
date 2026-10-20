---
name: follow-create-tauri-plugin
description: Build custom Tauri plugins with Rust and a JavaScript API
argument-hint: "[scope]"
related:
  - follow-create-web
  - deep-review-codebase
  - follow-tool-cargo
  - ship

---
## Goal

Build custom Tauri plugins that extend Tauri applications with a Rust backend and a JavaScript API

## Scope

Covers building plugins for desktop and mobile platforms with commands, state management, lifecycle events, and mobile native code

- Packages: `tauri` crate, `@tauri-apps/cli`, `@tauri-apps/api` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Review the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the rationale for the chosen stack and libraries for future reference (create tauri plugins)

### 2. Initialize Plugin Project

> Goal: Create a new plugin project with the Tauri CLI using the standard structure

1. Run `bunx @tauri-apps/cli plugin new <name>` to create a new plugin (alternative: `cargo tauri plugin new <name>`)
2. Use `--no-api` if you don't want an NPM package
3. Use `--android` and `--ios` for mobile support
4. Use `--github-workflows` if you want `.github` CI workflows (the current CLI doesn't generate `.github` by default)
5. The plugin is created in `tauri-plugin-<name>/`

### 3. Configure Plugin

> Goal: Define the plugin configuration through the Builder and Config struct

1. Define plugin configuration in `tauri.conf.json > plugins` — `api.config()` in `setup` returns the config parsed from this section
2. Define a `Config` struct (derive `Deserialize`) — use `Builder::<R, Option<Config>>` if the config is optional
3. Use `tauri::plugin::Builder::<R, Config>::new("<plugin-name>").setup(|app, api| { ... Ok(()) }).build()` to return a `TauriPlugin<R, Config>`

### 4. Define Commands

> Goal: Create commands for the webview to call via the invoke handler

1. Create commands in `src/commands.rs` with the `#[tauri::command]` macro — use a `tauri::ipc::Channel` parameter to stream progress back to the frontend
2. Register commands in `src/lib.rs` via `invoke_handler(tauri::generate_handler![commands::my_command])`
3. Commands can access `AppHandle`, `Window`, state, and input parameters

### 5. Implement Lifecycle Events

> Goal: Wire the plugin lifecycle hooks to manage state and events

1. Implement lifecycle hooks: `setup`, `on_navigation` (return `false` to cancel navigation), `on_page_load`, `on_webview_ready` (init scripts when the window is created), `on_event` (`RunEvent::ExitRequested`/`Exit`), `on_drop`
2. Manage state in the `setup` hook via `app.manage()` — commands access it through `tauri::State<T>`, outside commands use the `Manager` trait (`app.state::<T>()`, `app.emit()`)
3. Export the plugin API in `desktop.rs`/`mobile.rs` as a struct + extension trait (e.g. `<Name>Ext`) so it can be accessed via `app.<name>()...`

### 6. Create JavaScript API

> Goal: Create JavaScript/TypeScript bindings for calling commands from the frontend

1. Create bindings in `webview-src/index.ts`:

```typescript
import { invoke } from '@tauri-apps/api/core'
export async function myCommand() {
  await invoke('plugin:<plugin-name>|my_command')
}
```

2. Build TypeScript: `bun run build`

### 7. Add Mobile Support

> Goal: Add mobile support for Android and iOS

1. Run `bunx @tauri-apps/cli plugin android add` for Android
2. Run `bunx @tauri-apps/cli plugin ios add` for iOS
3. Implement native code in Kotlin (Android) and Swift (iOS)
4. Trigger mobile code from Rust via `mobile.rs`

### 8. Test And Publish

> Goal: Test and publish the plugin

1. Test the plugin in a Tauri app: install with `tauri add <plugin-name>`
2. Build plugin: `cargo build`
3. Publish to crates.io and NPM

### 9. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Naming Convention

- Rust crate: `tauri-plugin-<plugin-name>`
- NPM package: `@scope/plugin-<plugin-name>` or `tauri-plugin-<plugin-name>-api`
- Plugin name in `tauri.conf.json > plugins`

### 2. Project Structure

```
tauri-plugin-<name>/
├── src/
│   ├── commands.rs - Commands for the webview
│   ├── desktop.rs - Desktop implementation
│   ├── mobile.rs - Mobile implementation
│   ├── error.rs - Error types
│   ├── lib.rs - Plugin entry point
│   └── models.rs - Shared structs
├── permissions/ - Permission files
├── android/ - Android library
├── ios/ - Swift package
├── guest-js/ - JavaScript API source
├── dist-js/ - Transpiled JS
├── Cargo.toml
└── package.json
```

### 3. Command Permissions

- Commands are not accessible by default — generate permissions via `build.rs`: `tauri_plugin::Builder::new(&["cmd1", "cmd2"]).build()` automatically creates `allow-<cmd>`/`deny-<cmd>` in `permissions/` (add `global_scope_schema` for scope autocomplete)
- `permissions/default.toml` define default permission set (`"$schema" = "schemas/schema.json"` + `[default] permissions = [...]`)
- Declare platform support in `Cargo.toml > [package.metadata.platforms.support]` — `windows`/`linux`/`macos`/`android`/`ios` at level `"full"`/`"partial"`(+`notes`)/`"none"`
- Define permissions in `tauri.conf.json > capabilities`
- Use `allow-<command-name>` to grant access

### 4. State Management

- Use `app.manage()` in the `setup` hook
- Access state through extension traits on Manager instances
- Use `AppHandle`, `App`, `Window` for state access

### 5. Mobile Development

- Android: Kotlin code in `android/`
- iOS: Swift code in `ios/`
- Trigger mobile code from Rust via `mobile.rs`

- Use /follow-create-web when needed
- Use /follow-tool-cargo when needed

## Expected Outcome

- Tauri plugin created successfully with the CLI
- Commands and JavaScript API work
- Lifecycle events fully implemented
- Plugin supports desktop and mobile platforms
- Plugin can be published to crates.io and NPM

