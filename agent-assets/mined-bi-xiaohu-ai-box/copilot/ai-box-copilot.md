# AI-Box — Copilot Instructions

## Build & Run

```bash
npm run tauri dev          # Dev mode (frontend HMR + Rust auto-recompile)
npm run tauri build        # Release build (produces .msi installer)
npm run build              # Frontend only: tsc + vite build
```

No test runner is configured yet. Rust modules have inline `#[cfg(test)]` tests runnable via:

```bash
cd src-tauri && cargo test                    # All tests
cd src-tauri && cargo test doc_processor      # Single module
cd src-tauri && cargo test embedding::tests   # Specific test module
```

## Architecture

This is a **Tauri v2 desktop app** with a Rust backend and React frontend. All communication happens through Tauri's IPC bridge.

### Data Flow

```
React Component → invoke("command", {args}) → #[tauri::command] fn → Database/LLM/etc → Result<T, String>
```

For streaming (chat): the backend emits `"chat-stream"` events via `app.emit()`, and the frontend listens with `listen<ChatStreamEvent>()`.

### LLM Provider Pattern

`llm/mod.rs` defines a `Provider` enum (not a trait) dispatching to OpenAI-compatible, Claude, or Copilot backends. Ollama reuses the OpenAI implementation with a different `base_url`. Model strings use the format `"provider/model-id"` (e.g., `"openai/gpt-4o"`, `"ollama/llama3"`, `"copilot/claude-sonnet-4"`). Provider resolution happens in `commands/chat.rs::resolve_provider()`.

**Copilot provider** uses a two-step auth: OAuth token → short-lived Copilot API token (cached with auto-refresh). Chat goes through `api.githubcopilot.com`, not the OpenAI-compatible endpoint.

### State Management

- **Backend**: A single `Database` struct wraps `Mutex<Connection>` (SQLite), registered as Tauri managed state. All DB access goes through `db.conn.lock().unwrap()`.
- **Frontend**: Top-level state lives in `App.tsx` and flows down via props. No state management library — just `useState`/`useEffect`.

### Embedding & RAG

Documents are parsed (`doc_processor.rs`), chunked with overlap, and embedded via OpenAI's embedding API. Vectors are stored as BLOBs in SQLite's `chunks` table and searched with brute-force cosine similarity (`embedding.rs`). There is no vector database.

## Conventions

### Rust Backend

- **Tauri commands** return `Result<T, String>`. Convert errors with `.map_err(|e| e.to_string())`.
- **Async commands** must not hold `MutexGuard` across `.await` points — extract data from DB in a sync block, drop the lock, then await.
- **New commands** go in `src-tauri/src/commands/` as a submodule, then register in `lib.rs`'s `generate_handler![]` macro.
- **IDs** are generated with `uuid::Uuid::new_v4().to_string()`.
- **Settings** are stored as key-value pairs in the `settings` table. Sensitive values (API keys, OAuth tokens) are masked when returned to the frontend via `get_settings`.

### React Frontend

- **All Tauri `invoke()` calls** are wrapped in `src/lib/api.ts` with typed return values. Never call `invoke()` directly from components.
- **Components** are functional with TypeScript interfaces for props. Callbacks are named `onAction` (e.g., `onSelect`, `onDelete`).
- **Styling** uses Tailwind CSS v4 utility classes inline. Dark theme throughout (`bg-gray-950`, `bg-gray-900`). The only CSS file is `App.css` which imports Tailwind.
- **TypeScript is strict** — `noUnusedLocals` and `noUnusedParameters` are enforced.

### Model String Format

Models follow `"provider/model-id"` convention throughout the stack:
- `"openai/gpt-4o"`, `"claude/claude-sonnet-4-20250514"`, `"ollama/llama3"`, `"copilot/gpt-4o"`
- The prefix determines which LLM provider and API key to use.

### Adding a New LLM Provider

1. Create `src-tauri/src/llm/<provider>.rs` with a config struct and `chat`/`chat_stream`/`fetch_models` functions
2. Add variant to `Provider` enum in `llm/mod.rs`, wire up `chat`/`chat_stream` match arms
3. Add `resolve_provider` branch in `commands/chat.rs`
4. Add setting keys to `SETTING_KEYS` whitelist in `commands/settings.rs`
5. Expose any new commands in `lib.rs`'s `generate_handler![]`
6. Add frontend API wrappers in `src/lib/api.ts` and UI in `SettingsModal.tsx`
