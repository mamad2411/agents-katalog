# Cursor Rules for YTAudioBar

## Quick Start

This is a **cross-platform Tauri app** with React frontend (TS) + Rust backend.

## Folder Structure

```
/src              → React frontend (TypeScript)
/src-tauri/src    → Rust backend
/.github          → CI/CD workflows
```

## Code Standards

### Frontend

- **Language:** TypeScript
- **Framework:** React + TailwindCSS
- **File format:** Always read before modifying
- **Imports:** Use `src/lib/tauri.ts` for backend commands

### Backend

- **Language:** Rust (2021 edition)
- **Framework:** Tauri v2
- **Async:** Use `tokio::task::block_in_place()` when needed inside runtime
- **Database:** SQLite with sqlx

## Git Workflow

1. Make changes
2. Commit with: `git commit -m "message"` (includes co-author automatically via hooks)
3. Push to `main`

## Version Management

Always update these together:

- `package.json`
- `src-tauri/Cargo.toml`
- `src-tauri/tauri.conf.json`

## Release Tags

- `v2.1.5-beta` → pre-release (users don't get auto-update)
- `v2.1.5` → stable (users auto-update)

## Platform Notes

- **Linux:** Window position must be set AFTER showing window
- **Windows:** Standard positioning
- **macOS:** Uses menu bar instead of tray

## Common Commands

```bash
npm run dev           # Frontend dev server
npm run tauri build   # Build app
npm run tauri dev     # Tauri dev mode
cargo test            # Run tests (if any)
```

## Quick Reference

| Task                | Location                             |
| ------------------- | ------------------------------------ |
| Add UI              | `/src/components`, `/src/app/routes` |
| Add backend command | `/src-tauri/src/main.rs`             |
| Database changes    | `/src-tauri/src/database.rs`         |
| Audio logic         | `/src-tauri/src/audio_manager.rs`    |
