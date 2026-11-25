# Agent instructions

See [CLAUDE.md](./CLAUDE.md) for the full repo guide (layout, commands, conventions). It is tool-agnostic; all AI coding assistants should follow it.

Quick essentials:

- Frontend: `shell/frontend/` (Vue 3 + Vite + TS). Verify with `npm run lint`, `npm run test:unit -- --run`, `npm run build`.
- Backend: `shell/backend/` (.NET 10, controllers). Verify with `dotnet test` and `dotnet format --verify-no-changes`.
- Record significant decisions as ADRs in `docs/adr/`; architecture changes as new numbered snapshots in `docs/architecture/`.
