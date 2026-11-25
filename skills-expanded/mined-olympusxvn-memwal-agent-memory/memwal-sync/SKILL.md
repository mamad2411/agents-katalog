# MemWal hybrid sync skill

Use `@memwalpp/core` `MemorySyncService` via `MemWalAgentBridge`:

- **Recall:** `beforeRemember` / `pullQuery`
- **Capture:** `afterThink` → local row
- **Promote:** `pushOne` (redact + quality gate inside core)
- **Batch:** `syncPending` on task complete

Run without OpenClaw: `pnpm agent:demo` from repo root.
