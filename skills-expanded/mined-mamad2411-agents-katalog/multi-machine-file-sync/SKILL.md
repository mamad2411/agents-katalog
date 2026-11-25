---
name: multi-machine-file-sync
description: "Use when Mac↔devbox sync or hop continuity breaks."
---

# Multi-machine file sync (Mac ↔ devbox)

## Goal (user preference — non-negotiable)

**"Same desk, different chair."** Hopping Mac ↔ devbox must preserve:

- working tree (including dirty/uncommitted edits)
- **full `.git`** (branch, index, stash, history usable with `git status` / `git log`)

**Do not** propose `ignoreVcs` / drop-`.git` + git-attach/clone-on-other-side as the primary design. Cooper rejected that: it defeats seamless hops even if it saves scan cost.

## Stack map (darwin HM)

| Piece | Path |
|---|---|
| Unison module | `~/darwin/modules~/unison.nix` (`programs.unison-sync`) |
| Mutagen module | `~/darwin/modules~/mutagen.nix` (`programs.mutagen`) |
| macpro sessions | `~/darwin/homes/aarch64-darwin/cm@macpro/default.nix` |
| mbp sessions | `~/darwin/homes/aarch64-darwin/cm@mbp/default.nix` |
| devbox hub | `~/darwin/homes/x86_64-linux/cm@devbox/default.nix` |
| Linux HM imports | `~/darwin/modules~ (mutagen; unison not imported by default) |
| SSH | `Host devbox` / `Host devbox.ts` → `<REDACTED>` |

**Live Unison today:** local pairs only (`littlebird` Dropbox, `dotconfig`) — **not** `~/git`.
**Live Mutagen today:** client-owned `git` (+ macpro `omp`) → SSH hub on devbox; continuous two-way-safe.

Migration plan (Mutagen → Unison for git):
`~/git/darkmatter/.hermes/plans/2026-08-07_125110-mutagen-to-unison-git-sync.md`

## Mutagen vs Unison (choose deliberately)

| | Mutagen | Unison |
|---|---|---|
| Duty cycle | Always-on daemon + watch/scan | Episodic batch (interval / manual) |
| Steady CPU | High on large hot trees | ~0 between runs |
| Fit for Cooper | Weak for full `~/git` continuous | Preferred cadence |
| Seamless hop | Live if healthy | Needs interval ≤ hop lag **or** `unison-sync` before/after hop |

**Default recommendation:** Unison batch for `~/git` (keep `.git`); ignore high-churn paths; optional manual hop command. Do not run Mutagen and Unison writers on the same tree.

## Diagnosing sync CPU

```bash
ps auxwwr | head -25
mutagen sync list -l
pgrep -lf 'mutagen|unison'
```

Mutagen red flags: status **Scanning files**, huge synchronizable counts, transition errors under `**/runs`, `.git/index` conflicts.

## Safe shrink levers (keep `.git`)

Prefer in order:

1. **Ignore churn** (not VCS): `runs/`, `*.log`, `.cache`, `.turbo`, coverage, `.venv-*`, bot heartbeats
2. **Narrow roots** to hot orgs/repos if full `~/git` is optional
3. **Pause when idle** (`mutagen sync pause`) or Unison interval + manual hop
4. **One active git writer** during sync windows (dual live IDEs/bots cause index fights)

Port existing Mutagen ignore defaults (`node_modules`, `.venv`, `target`, `dist`, `.next`, direnv, etc.) into Unison `Name`/`Path` ignores. Keep nix-managed symlink junk ignores (pre-commit, treefmt, process-compose, agenix-rekey workflow).

## Cutover rule

```text
pause/terminate Mutagen → first Unison archive (manual) → enable Unison agent → disable Mutagen HM + hub
```

Never dual-write. Rollback = re-enable Mutagen module/sessions, bootout Unison pair agents.

## Multi-client caveat

Unison is **pairwise**. macpro↔devbox and mbp↔devbox are separate links — same divergence risk as two Mutagen clients. Prefer one primary Mac or sync before switching Macs.

## Audinate / UA (related machine-health note)

High CPU `conmon_cmm` is **Audinate Dante ConMon**, not container conmon. Path: `/Library/Application Support/Audinate/`. Cooper uses **UA Thunderbolt** for speakers — ConMon not required. Permanently disabled via `launchctl disable system/com.audinate.dante.ConMon` (plist left on disk). Do not unload `com.uaudio.*` when fixing ConMon.

## References

- `references/unison-mutagen-cutover.md` — runbook, ignores, SSH roots, validation
