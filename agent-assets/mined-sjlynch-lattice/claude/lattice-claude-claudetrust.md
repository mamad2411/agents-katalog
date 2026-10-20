# backend/src/claudeTrust

Writes Claude Code's `~/.claude.json` so Lattice-spawned Claude sessions skip
the "trust this folder" dialog and pick up Lattice's managed MCP servers. This
underpins MCP injection — see the project `CLAUDE.md` MCP section and
`../mcp/CLAUDE.md` "Injection sites". `../claudeTrust.ts` is the stable public
facade; keep external imports pointed at `./claudeTrust.js` and the
implementation here.

## Modules

- `apply.ts` — `applyClaudeProjectConfig(dir, { managed })` and the trust-only
  `seedClaudeTrust(dir)`. The **apply mechanism only**: it writes a *pre-resolved*
  managed set (or `null` = trust-only) into `projects[<dir>]`. It does **not**
  resolve MCP/trust/memory policy — that stays in the main backend
  (`mcp/registry.ts` + `terminalServerClient.ts`) so the detached terminal-server
  can import this without the policy chain.
- `configFile.ts` — the `~/.claude.json` I/O primitives: parse-on-read with
  heal-from-backup (`readClaudeConfig`), the atomic temp→rename writer
  (`atomicWriteFile` / `writeClaudeConfigAtomic`), restore-from-backup, the
  `CLAUDE_GLOBAL_CONFIG` / `CLAUDE_JSON_BACKUP` paths, the `ClaudeGlobalConfig`
  type, and `toClaudeProjectKey`.
- `configLock.ts` — `withClaudeConfigLock`, the exact-path mutex with bounded
  Windows permission retries and verified dead-owner recovery. New owners use
  an exclusive file at the historical `.claude.json.lattice-lock` path; legacy
  directory owners remain authoritative until they release it.
- `maintenance.ts` — boot/timer reclamation: `pruneStaleClaudeProjectEntries`
  (drop dead ephemeral `projects[<cwd>]` entries) and
  `sweepOrphanedClaudeConfigTemps` (delete leftover `.lattice-*.tmp`), plus the
  pure `isLatticeEphemeralProjectKey` / `selectStaleEphemeralProjectKeys`.
- `util.ts` — `sleep` + best-effort `unlinkQuietly` for atomic-write temp cleanup.

## I/O-safety + locking contract

- **One mutex, one writer.** Every read-mutate-write of `~/.claude.json` runs
  inside `withClaudeConfigLock`. `readClaudeConfig` / `writeClaudeConfigAtomic`
  MUST only be called while the lock is held (`apply.ts`, `maintenance.ts`, and
  the heal path all do). `restoreClaudeConfigFromBackup` is the lock-*acquiring*
  wrapper for `../claudeConfigGuard.ts`, which doesn't otherwise hold it.
- **Read-only no-op before locking.** `apply.ts` may skip locking when a plain
  read proves that trust and the requested managed MCP configuration are already
  current. It never heals or writes from that optimistic snapshot. Any required
  change still acquires the mutex and rereads current JSON before mutation.
- **Compatibility and owner evidence.** New `open(wx)` owners occupy the SAME
  path legacy callers `mkdir`; legacy nonrecursive `rmdir` cannot remove an
  owner file. No alternative lock path or unlocked fallback is allowed. Timeout
  alone never proves death: legacy directories, partial/unrecognized records,
  symlinks, unreadable/foreign/live owners are preserved. Only a same-host PID
  probe returning ESRCH proves a known owner dead; permission denial is unknown.
- **Retirement and release.** Dead-owner retirement first claims the exact raw
  generation using a permanent exclusive filename in `<lock>.retired`, then
  verifies ownership again before unlink. Claims prevent a suspended contender
  deleting a successor. A crash/denial after claiming can conservatively block
  further retirement; do not delete those claims while contenders may remain.
  Ordinary live-owner release needs no tombstone because eligible stale
  reclaimers cannot remove a live PID and legacy `rmdir` cannot unlink a file.
  Failed release is retained locally only after its callback finishes; a later
  acquisition retries that exact owner through one shared cleanup promise,
  preventing temporary EPERM from stranding a long-lived process's own lock.
- **Bounded denial, preserved evidence.** Acquisition retries EPERM/EACCES/EBUSY
  over the existing bounded contention windows. Owner initialization, inspection,
  retirement and release use short bounded retries. Persistent errors retain
  their operation/code/path. Incomplete initialization files and ownerless legacy
  orphans require verified external cleanup; they are never guessed abandoned.
- **The mutex orders overlapping writes only.** It can't stop the slower
  lost-update: Claude reads the file at startup, holds it in memory, and writes
  the whole object back at shutdown, silently reverting any entry added in
  between. That race is shrunk by re-applying microseconds before `pty.spawn`
  (the terminal-server's `POST /sessions`), not by this lock.
- **Atomic writes, no orphans.** `atomicWriteFile` writes a
  `<file>.lattice-<pid>-<ts>-<uuid>.tmp` then renames; it unlinks the temp on any
  failure and retries the rename through transient Windows file-locks
  (EPERM/EBUSY/EACCES). The shared `TEMP_SUFFIX` / `tempPrefix` let
  `sweepOrphanedClaudeConfigTemps` recognize leftovers.
- **Heal, never wipe.** A corrupt `~/.claude.json` (truncated by a force-kill
  mid-write) is restored from `CLAUDE_JSON_BACKUP` — but only after a SECOND
  read ~200 ms later still fails to parse (Claude rewrites the file in place,
  so one failed parse may be a read landing mid-write, and restoring then rolls
  a newer config back to the backup). The guard's lock-acquiring
  `restoreClaudeConfigFromBackup` likewise re-checks the live file inside the
  lock and returns `'healthy'` without writing if it now parses. A stat error
  other than ENOENT/ENOTDIR never counts as a dead cwd in the prune. If there's no usable backup
  the parse error is surfaced so the caller skips its write — never reset to `{}`
  (that would erase the user's real projects/auth/history).
- **Best-effort, never throw.** `applyClaudeProjectConfig` /
  `pruneStaleClaudeProjectEntries` / `sweepOrphanedClaudeConfigTemps` log and
  swallow on error: worst case is one trust prompt or some uncollected cruft.

## When adding a file here

Add it to `../terminalFingerprint.ts` `FINGERPRINT_FILES` — the whole subtree is
in the terminal-server's import graph (via `applyClaudeProjectConfig` /
`pruneStaleClaudeProjectEntries`), so a byte change must invalidate stale
orphans. Conversely, do **not** import MCP-policy modules here (only
`../mcp/claudeInject.js`), or a policy edit would start respawning the
terminal-server and killing running agents.
