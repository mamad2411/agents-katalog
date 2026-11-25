---
name: ts-tauri
description: Use when building desktop apps with Tauri 2 — web frontend + Rust backend, IPC commands, capabilities, plugins.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [ts-vite, rust-essentials, react]
---

# TS Tauri 2

**Iron Law: capabilities are deny-by-default. NEVER enable everything. The Rust backend is the trust boundary — validate all input from JS. Secrets in the bundle are public.**

## Why Tauri (vs Electron / Wails)

| Tool           | Verdict                                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Tauri 2**    | webview (system, not bundled), Rust core, ~5-15MB binary, capability-scoped IPC — **default for desktop**               |
| **Electron**   | bundles Chromium, ~100-150MB binary, mature ecosystem; pick if you need a specific Chromium version or Chrome-only APIs |
| **Wails (Go)** | similar to Tauri, Go backend instead of Rust; smaller community                                                         |
| **Neutralino** | Node + system webview, simpler but less mature                                                                          |

Trade-off: Tauri uses the **system webview** (WebView2 on Win, WebKit on macOS/Linux) — pixel-identical-cross-platform is harder than Electron. Test on each target.

## Project layout

```
myapp/
├── src/                     # web frontend (Vite + React/Svelte/Vue)
├── src-tauri/               # Rust core
│   ├── Cargo.toml
│   ├── tauri.conf.json      # main config
│   ├── capabilities/        # scoped permission sets
│   │   └── default.json
│   ├── icons/
│   └── src/
│       ├── main.rs
│       └── commands.rs
└── package.json
```

## Commands — JS calls Rust

```rust
// src-tauri/src/commands.rs
#[tauri::command]
async fn save_note(title: String, body: String, state: tauri::State<'_, AppState>) -> Result<String, String> {
    if title.trim().is_empty() { return Err("title required".into()); }
    if body.len() > 1_000_000 { return Err("body too large".into()); }
    // Log the raw error Rust-side; return a generic message to JS.
    // `e.to_string()` on a sqlx/SQLite error includes SQL fragments, table names,
    // file paths — visible in devtools, console, error reporting, system logs.
    // Use tracing::error! in shipped builds — it routes through a configurable
    // subscriber (file, syslog, suppressed). eprintln! writes to process stderr
    // which power users can see when they launch the app from a terminal.
    let id = state.db.insert_note(&title, &body).await
        .map_err(|e| { tracing::error!(?e, "save_note db insert failed"); "failed to save note".to_string() })?;
    Ok(id)
}

// src-tauri/src/main.rs
fn main() {
    tauri::Builder::default()
        .manage(AppState::new())
        .invoke_handler(tauri::generate_handler![commands::save_note])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```ts
// src/api.ts
import { invoke } from "@tauri-apps/api/core";
const id = await invoke<string>("save_note", { title, body });
```

**Rust commands are the trust boundary.** Treat every argument as hostile — validate length, format, range. Convert Rust errors to **fixed generic strings** before returning to JS — never `e.to_string()`, which leaks SQL fragments, table names, file paths, hostnames. Log the raw error Rust-side with `eprintln!` / `tracing::error!`; return a sanitized message that the user can act on without exposing internals.

## Capabilities + permissions — the security model

```jsonc
// src-tauri/capabilities/default.json
{
  "identifier": "default",
  "description": "App default capability",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    { "identifier": "fs:scope", "allow": [{ "path": "$APPDATA/notes/*" }] },
    "dialog:allow-open",
    "notification:default",
  ],
}
```

**Never `"shell:default"` or `"fs:default"`** — they grant broad access. Scope every permission. Use `$APPDATA`, `$DOCUMENT`, `$HOME` variables — never absolute paths users can't read.

## Plugins worth knowing

| Plugin                            | Use                                                   |
| --------------------------------- | ----------------------------------------------------- |
| `@tauri-apps/plugin-fs`           | scoped filesystem access                              |
| `@tauri-apps/plugin-dialog`       | native open/save/message dialogs                      |
| `@tauri-apps/plugin-notification` | OS notifications                                      |
| `@tauri-apps/plugin-shell`        | spawn processes — **dangerous**, allow-list args only |
| `@tauri-apps/plugin-updater`      | signed delta updates                                  |
| `@tauri-apps/plugin-store`        | persistent key-value store                            |
| `@tauri-apps/plugin-window-state` | remember window size/position                         |

Install: `pnpm add @tauri-apps/plugin-foo` + `cargo add tauri-plugin-foo` + register in `main.rs` + add permissions in capability file.

## Window management

```rust
let window = app.get_webview_window("main").unwrap();
window.set_title("New Title")?;
window.set_size(LogicalSize { width: 1200.0, height: 800.0 })?;
// Prefer .emit("event-name", payload) over executing JS strings — keeps IPC structured
window.emit("reload-requested", ())?;
```

Multi-window: define in `tauri.conf.json` `app.windows[]` or create at runtime with `WebviewWindowBuilder`. Each window gets its own capabilities — scope tightly.

## Updater — signed deltas

```jsonc
// tauri.conf.json
"plugins": {
  "updater": {
    "endpoints": ["https://releases.example.com/{{target}}/{{current_version}}"],
    "pubkey": "<base64 pubkey from `tauri signer generate`>"
  }
}
```

Updates are **signed with your private key**. Bundle the pubkey, never the privkey. Run `tauri signer sign` in CI on the release artifact, host the `.sig` next to the binary. Without signing, an MITM serves arbitrary binaries.

## Anti-patterns

- `"core:default"` + `"fs:default"` + `"shell:default"` "to get unblocked" — full filesystem and shell from any JS XSS
- `shell.execute("git", [userInput])` — command injection; allow-list args
- Embedding API keys / secrets in the frontend or via env at build — they're in the bundle, extractable
- Trusting JS-supplied paths in Rust commands — validate against scoped allow-list
- Skipping the updater signing key — anyone on the wire can replace your app
- Disabling CSP "for dev convenience" and forgetting in prod — `tauri.conf.json` `app.security.csp`
- Pushing strings into `window.eval`-style escape hatches or `unsafe-inline` script — kills CSP guarantees; emit structured events instead
- One giant `commands.rs` — split by domain, register modules cleanly
- Forgetting `--release` for prod builds — 10x slower, debug symbols ship

## Red flags

| Thought                                               | Reality                                                     |
| ----------------------------------------------------- | ----------------------------------------------------------- |
| "Just allow everything, we'll lock down later"        | Later = never; ships with prod permissions                  |
| "The user is on their own machine — what's the risk?" | XSS in a Tauri app = arbitrary code on the user's machine   |
| "I'll embed the API key, who'd reverse-engineer?"     | `strings`/devtools/proxy — your key is public in 30 seconds |
| "Updates from any URL is fine"                        | Without signing, that's a backdoor on every install         |

## Hand-off

For Vite config the frontend builds on: `Skill(ts-vite)`. For the Rust side (error handling, async): `Skill(rust-essentials)`. For React patterns in the frontend: `Skill(react)`.
