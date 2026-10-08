# Doku

Document editor with an integrated Claude Code chat panel.

## Commands

- `bun run dev` - Start backend (port 39483) + Vite dev server (port 51738) concurrently
- `bun run build` - Build frontend to `dist/`
- `bun run start` - Start production server (serves frontend from `dist/`)

## Quality checks

- `bun run typecheck` - Type check frontend and server (`tsc --noEmit` for both tsconfigs)
- `bun run lint` - Lint and auto-fix with ESLint
- `bun run format` - Format with Prettier

## Stack

- Runtime: Bun
- Language: TypeScript
- Frontend: React + Vite (SPA in `src/`)
- AI: Claude Code CLI (spawned as subprocess via `claude` command)

## Structure

- `server/` - Backend: Bun HTTP server, Claude Code harness, storage layer
  - `index.ts` - HTTP server: multi-doc CRUD API, file watcher (SSE), chat proxy, and production static serving from `dist/`
  - `harness.ts` - Claude Code CLI subprocess wrapper
  - `storage.ts` - Storage utilities: project dir resolution, doc name generation, metadata management
  - `storage-provider.ts` - Storage provider abstraction (filesystem and ephemeral)
- `src/` - React frontend (components, hooks, utils)

## Storage

- Documents are stored globally at `~/.doku/projects/<encoded-cwd>/`
- Project path is encoded by replacing `/` with `-`
- Each document is a `.md` file with a randomly generated adjective-noun name
- Session IDs and metadata are persisted in `_meta.json` alongside documents
- Chat history is restored from Claude Code's JSONL session files

## Patterns

- Chat uses Claude Code CLI with `--output-format stream-json` and streams responses to the frontend via SSE
- Session persistence: the server captures `session_id` from Claude Code's result event and saves it to `_meta.json`, reusing it with `--resume` on subsequent requests
- Document sync: frontend polls for external file changes via SSE (`/api/doc/:name/watch`) so edits made by Claude Code appear in real time
- Dev mode: Vite dev server (port 51738) proxies `/api` requests to backend (port 39483)
- Multi-doc: frontend manages a document list with a dropdown switcher; hooks accept `docName` and re-initialize on changes
