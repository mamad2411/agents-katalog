---
name: disk-hygiene
description: macOS disk cleanup, cache pruning, stale file detection, and Downloads triage. TRIGGERS - disk space, cleanup, disk usage
allowed-tools: Read, Bash, Write, Glob, Grep, AskUserQuestion
---

# Disk Hygiene

> Audit disk usage, clean developer caches, find forgotten large files, and triage Downloads on macOS.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- User asks about disk space, storage, or cleanup
- System is running low on free space
- User wants to find old/forgotten large files
- User wants to clean developer caches (brew, uv, pip, npm, cargo)
- User wants to triage their Downloads folder
- User asks about disk analysis tools (dust, dua, gdu, ncdu)

## TodoWrite Task Templates

### Template A - Full Disk Audit

```
1. Run disk overview (df -h /System/Volumes/Data && major directories)
2. Audit developer caches (uv, brew, pip, npm, cargo, rustup, Docker)
3. Scan in-repo build artifacts (Rust target/, .venv, node_modules — often the biggest, see Phase 2.5)
4. Scan for forgotten large files (>50MB, not accessed in 180+ days)
5. Present findings with AskUserQuestion for cleanup choices
6. Execute selected cleanups
7. Report space reclaimed
```

### Template B - Cache Cleanup Only

```
1. Measure current cache sizes
2. Run safe cache cleanups (brew, uv, pip, npm)
3. Report space reclaimed
```

### Template C - Downloads Triage

```
1. List Downloads contents with dates and sizes
2. Categorize into groups (media, dev artifacts, personal docs, misc)
3. Present AskUserQuestion multi-select for deletion/move
4. Execute selected actions
```

### Template D - Forgotten File Hunt

```
1. Scan home directory for large files not accessed in 180+ days
2. Group by location and type (media, ISOs, dev artifacts, documents)
3. Present findings sorted by size
4. Offer cleanup options via AskUserQuestion
```

---

## Phase 1 - Disk Overview

Get the lay of the land before diving into specifics.

```bash
/usr/bin/env bash << 'OVERVIEW_EOF'
echo "=== Disk Overview ==="
# MUST be /System/Volumes/Data, NOT `/`. On APFS (Catalina+) `/` is the SEALED
# READ-ONLY system volume and reports a fixed ~10GB used — it is not your disk.
# Verified 2026-07-31: `df -h /` said "10Gi used, 185Gi avail" on a machine that
# was actually 707GB used and 80% full. Reading `/` will make you conclude there
# is nothing to clean.
df -h /System/Volumes/Data

echo ""
echo "=== Major Directories ==="
du -sh ~/Library/Caches ~/Library/Logs ~/Library/Application\ Support \
  ~/.Trash ~/Downloads ~/Documents ~/Desktop ~/Movies ~/Music ~/Pictures \
  2>/dev/null | sort -rh

echo ""
echo "=== Developer Tool Caches ==="
du -sh ~/.docker ~/.npm ~/.cargo ~/.rustup ~/.local ~/.cache \
  ~/.conda ~/.pyenv ~/.local/share/mise 2>/dev/null | sort -rh
OVERVIEW_EOF
```

## Phase 2 - Cache Audit & Cleanup

### Cache Size Reference

| Cache       | Location                                         | Typical Size  | Clean Command                                                           |
| ----------- | ------------------------------------------------ | ------------- | ----------------------------------------------------------------------- |
| uv          | `~/Library/Caches/uv/` **or `~/.cache/uv/`**     | 5-15 GB       | `uv cache clean`                                                        |
| Homebrew    | `~/Library/Caches/Homebrew/`                     | 3-10 GB       | `brew cleanup --prune=all`                                              |
| pip         | `~/Library/Caches/pip/`                          | 0.5-2 GB      | `pip cache purge`                                                       |
| npm         | `~/.npm/_cacache/`                               | 0.5-2 GB      | `npm cache clean --force`                                               |
| cargo       | `~/.cargo/registry/cache/`                       | 1-5 GB        | `cargo cache -a` (needs cargo-cache)                                    |
| rustup      | `~/.rustup/toolchains/`                          | 2-10 GB       | `rustup toolchain uninstall <name>` (list with `rustup toolchain list`) |
| mise        | `~/.local/share/mise/installs/<tool>/<version>/` | 0.2-2 GB each | `mise uninstall <tool>@<version>` (list with `mise ls`)                 |
| Docker      | Docker.app                                       | 5-30 GB       | `docker system prune -a`                                                |
| Playwright  | `~/Library/Caches/ms-playwright/`                | 0.5-2 GB      | `npx playwright uninstall`                                              |
| sccache     | `~/Library/Caches/Mozilla.sccache/`              | 1-3 GB        | `rm -rf ~/Library/Caches/Mozilla.sccache`                               |
| go-build    | `~/Library/Caches/go-build/`                     | 5-25 GB       | `go clean -cache` (or `rm -rf` if `go` not on PATH)                     |
| huggingface | `~/.cache/huggingface/`                          | 1-10 GB       | `rm -rf ~/.cache/huggingface/hub/<model>`                               |

### Safe Cleanup Commands (Always Re-downloadable)

```bash
/usr/bin/env bash << 'CACHE_CLEAN_EOF'
set -euo pipefail

echo "=== Measuring current cache sizes ==="
echo "uv:       $(du -sh ~/Library/Caches/uv/ 2>/dev/null | cut -f1 || echo 'N/A')"
echo "Homebrew: $(du -sh ~/Library/Caches/Homebrew/ 2>/dev/null | cut -f1 || echo 'N/A')"
echo "pip:      $(du -sh ~/Library/Caches/pip/ 2>/dev/null | cut -f1 || echo 'N/A')"
echo "npm:      $(du -sh ~/.npm/_cacache/ 2>/dev/null | cut -f1 || echo 'N/A')"

echo ""
echo "=== Cleaning ==="
brew cleanup --prune=all 2>&1 | tail -3
uv cache prune 2>&1   # prune, NOT `clean --force` — see "uv cache lock" below
pip cache purge 2>&1
npm cache clean --force 2>&1
CACHE_CLEAN_EOF
```

### Troubleshooting Cache Cleanup

| Issue                               | Cause                         | Solution                                                        |
| ----------------------------------- | ----------------------------- | --------------------------------------------------------------- |
| `uv cache` lock held                | **Identify the holder first** | See "uv cache lock" below — `--force` can be actively dangerous |
| `brew cleanup` skips formulae       | Linked but not latest         | Safe to ignore, or `brew reinstall <pkg>`                       |
| `pip cache purge` permission denied | System pip vs user pip        | Use `python -m pip cache purge`                                 |
| Docker not running                  | Docker Desktop not started    | Start Docker.app first, or skip                                 |

### ⚠️ uv cache lock — never reach for `--force` before naming the holder

`uv cache clean` waits 300 s for an exclusive lock, then errors. Earlier revisions of this skill said "use `--force`". **That advice is wrong when the lock holder is a long-running service**, and it is the same class of mistake as the catgpt-gateway incident: mutating a cache underneath a live daemon.

Measured 2026-08-24: `uv cache clean` timed out, and the holders were

```
uv 1934  uv run python ~/eon/tasc/kernel/embed.py serve  --model minishlab/potion-retrieval-32M
uv 2652  uv run python ~/eon/tasc/kernel/embed.py rerank --serve --model Xenova/ms-marco-MiniLM-L-6-v2
```

— both children of the **launchd job `com.tasc.serve`**, up 1 h 37 m. These are persistent daemons, so the lock is never released and `clean` can never succeed on its own. Always identify the holder before deciding:

```bash
lsof ~/.cache/uv/.lock 2>/dev/null          # exact PIDs holding the lock
ps -o pid,ppid,lstart,command -p <PIDS>     # how long, and whose child
launchctl list | grep -i <service>          # is the parent a launchd job?
```

Then pick by holder:

| Holder                             | Action                                                                                   |
| ---------------------------------- | ---------------------------------------------------------------------------------------- |
| Transient (`uv sync` you just ran) | Wait for it, or `--force` — genuinely safe                                               |
| **Long-running launchd/daemon**    | **Do NOT `--force`.** Either skip, or `launchctl bootout` → clean → `bootstrap` → verify |
| Unknown / can't identify           | Skip. The cache is never worth an outage                                                 |

**Prefer `uv cache prune` over `uv cache clean` in routine hygiene.** `prune` removes only _unused_ entries and leaves everything a live environment depends on, so it is the correct periodic-maintenance verb; `clean` nukes everything and forces a full re-download.

### uv `archive-v0` silently accumulates whole virtual environments

The uv cache's headline number is misleading, so classify before you judge it. `archive-v0` is documented as unpacked _wheel_ bodies that get hardlinked into each `.venv` — that part earns its keep. But it also accretes **complete virtual environments** (build envs / tool envs) that are never garbage-collected, and those are pure dead weight. Measured 2026-08-24 on a 69 GB uv cache:

| Entry shape                       | Count | Size      |
| --------------------------------- | ----- | --------- |
| Full venvs (contain `pyvenv.cfg`) | 210   | **39 GB** |
| Genuine unpacked wheels           | 1,577 | 10 GB     |

So 78 % of `archive-v0` was orphaned environments, not the dedup layer. Classify it — the split changes both the diagnosis and the remedy (`prune`, not `clean`):

```bash
du -sk ~/.cache/uv/archive-v0/* 2>/dev/null > /tmp/uv-all.txt
while read -r kb path; do
  [ -f "$path/pyvenv.cfg" ] && echo "VENV $((kb/1024))MB $path"
done < /tmp/uv-all.txt | sort -k2 -rn | head
```

**Also check hardlink counts before promising a number.** uv hardlinks cache files into live `.venv`s, so deleting a cache entry with `links>1` reclaims _nothing_:

```bash
stat -f 'links=%l size=%z %N' "$(find ~/.cache/uv/archive-v0 -type f -size +20M | head -1)"
# links=1 -> deleting truly reclaims;  links>1 -> shared with a live venv, no gain
```

**Don't let "Python is bloated" be the conclusion.** In the same audit, Rust's per-repo `target/` dirs totalled **57 GB** against ~7 GB of Python `.venv`s — 8× more — because `target/` is per-repo with no sharing while uv's archive is shared across every project. Report the measured split, not the folk wisdom.

## Phase 2.5 - Project Build Artifacts (in-repo, regenerable)

**The single most-missed category — check it on EVERY audit.** Compiler and dependency output lives _inside_ your repos, not under `~/Library`, so the Phase 1/2 scans never see it. A single active Rust repo's `target/` routinely hits 10-35 GB; across a dev tree these artifacts can dwarf every cache combined (one real audit: 62 GB of `target/` + 20 GB of `.venv`). All of it regenerates on the next build — the only cost is recompile / re-sync time.

| Artifact     | Dir name                    | Typical size     | Regenerated by        |
| ------------ | --------------------------- | ---------------- | --------------------- |
| Rust build   | `target/`                   | 1-35 GB **each** | `cargo build`         |
| Python venv  | `.venv/`                    | 0.1-2 GB each    | `uv sync` / `uv venv` |
| Node modules | `node_modules/`             | 0.1-0.5 GB each  | `npm` / `bun install` |
| Zig cache    | `.zig-cache/`, `zig-cache/` | 0.1-1 GB each    | next `zig build`      |

### Discover + size (point ROOTS at your code dirs)

```bash
/usr/bin/env bash << 'ARTIFACT_SCAN_EOF'
ROOTS=(~/eon ~/own ~/src ~/code ~/projects)
for n in target .venv node_modules .zig-cache zig-cache; do
  echo "=== $n (top 10 by size) ==="
  find "${ROOTS[@]}" -maxdepth 5 -type d -name "$n" -prune 2>/dev/null \
    -exec du -sh {} \; 2>/dev/null | sort -rh | head -10
done
ARTIFACT_SCAN_EOF
```

### Safe deletion

**Rust `target/` — guard against false matches.** Only delete a `target/` that has a sibling `Cargo.toml`, so you never nuke an unrelated folder literally named "target":

```bash
/usr/bin/env bash << 'TARGET_CLEAN_EOF'
ROOTS=(~/eon ~/own)
find "${ROOTS[@]}" -maxdepth 5 -type d -name target -prune 2>/dev/null | while read -r t; do
  [ -f "$(dirname "$t")/Cargo.toml" ] && rm -rf "$t" && echo "cleaned: $t"
done
TARGET_CLEAN_EOF
```

`.venv` / `node_modules` are safe to bulk-delete by name (regenerated on next `uv sync` / `install`):

```bash
find ~/eon ~/own -maxdepth 5 -type d -name .venv -prune -exec rm -rf {} +
```

### ⚠️ CHECK FOR DEPENDENT SERVICES FIRST — this is not optional

`node_modules` and `.venv` are only "safe to bulk-delete" for repos nobody is _running_. On 2026-07-31 a bulk delete took out `catgpt-gateway/node_modules`; its launchd watchdog then failed 95 times and, in trying to restart the gateway, drove a Chrome launch that raised a macOS TCC prompt. The user reported it as a mysterious permission pop-up, and the disk cleanup was two steps removed from the symptom.

Build the exclusion list BEFORE deleting anything:

```bash
/usr/bin/env bash << 'DEPCHECK_EOF'
# Every repo backing a live launchd job — never delete artifacts inside these.
for p in "$HOME"/Library/LaunchAgents/*.plist; do
    prog=$(plutil -extract ProgramArguments.0 raw "$p" 2>/dev/null) || continue
    case "$prog" in "$HOME"/*) ;; *) continue ;; esac
    d=$(dirname "$prog")
    for _ in 1 2 3 4 5; do
        { [ -f "$d/package.json" ] || [ -f "$d/pyproject.toml" ]; } && break
        d=$(dirname "$d"); [ "$d" = "$HOME" ] && break
    done
    [ "$d" = "$HOME" ] && continue      # walked out; not a real repo match
    echo "$d"
done | sort -u
DEPCHECK_EOF
```

Then `SKIP` any candidate path under one of those roots, and **print the skip** so the operator can see the guard fired. After cleanup, re-run the same list and assert each repo still has the manifest-matching directory (`package.json` → `node_modules`, `pyproject.toml` → `.venv`).

> **⚠️ Check EVERY manifest in the repo, not just the one at the root.** The version above walks up from the launchd program to the first `package.json` or `pyproject.toml` and stops — so for a repo whose service code lives in a subdirectory it verifies the wrong thing. Measured 2026-08-03 on `~/eon/tasc`: the root has `pyproject.toml` (so the check reported `.venv=ok` and `node_modules=—`, i.e. "not applicable") while the service actually needs **`ts/node_modules`**, which was missing. The guard reported the repo healthy while its launchd job had been crash-looping 11,593 times. Enumerate instead:
>
> ```bash
> find "$repo" -name package.json -not -path '*/node_modules/*' -maxdepth 3 \
>   | while read -r m; do d=$(dirname "$m"); [ -d "$d/node_modules" ] || echo "MISSING $d/node_modules"; done
> find "$repo" -name pyproject.toml -not -path '*/.venv/*' -maxdepth 3 \
>   | while read -r m; do d=$(dirname "$m"); [ -d "$d/.venv" ] || echo "MISSING $d/.venv"; done
> ```
>
> Also note a Python venv can be present and still incomplete: `uv sync` installs only the default dependency group. `tasc` declared its embedding deps under `[dependency-groups] embed`, so the venv existed, imported `pymupdf` fine, and failed on `import numpy` until `uv sync --group embed` was run. **A directory existing is not the same as the dependencies being installed** — where a repo documents a group/extra, restore it.

> **🔴 The walk-up finds NOTHING when the job execs a runner shim outside the repo.** Both versions above start at `ProgramArguments.0` and walk _up_ the filesystem. But a launchd runner-shim policy (signed, distinctly-named shims in `~/.local/libexec/` or `~/.claude/tools/launchd-runners/libexec/`) puts the program in a directory that has no ancestor relationship to the repo at all — the walk-up terminates at `$HOME` or, worse, lands on `~/.claude` and reports _that_ as the repo. The guard then emits a confident, entirely wrong exclusion list, and the real repo is deleted.
>
> Measured 2026-09-13: the exclusion list named `~/.claude` for 16 jobs and never mentioned `~/eon/iterm2-scripts`, `~/eon/mql5`, `~/eon/claude-sys` — so the cleanup removed all three repos' `.venv`/`node_modules`, killing `com.terryli.iterm2-autosnapshot` (crash-safety snapshots), `com.terryli.pushover-telemetry` (a Bun/TS daemon) and `com.terryli.typeless-keystroker`. **Grep the shim for repo paths as well as walking up:**
>
> ```bash
> for p in "$HOME"/Library/LaunchAgents/*.plist; do
>   prog=$(plutil -extract ProgramArguments.0 raw "$p" 2>/dev/null) || continue
>   [ -f "$prog" ] || continue
>   # shims are often compiled binaries — `strings`, not `grep`, and search env-var
>   # defaults too (e.g. ITERM2_SCRIPTS_REPO=/Users/.../eon/iterm2-scripts)
>   strings "$prog" 2>/dev/null \
>     | grep -oE '/Users/[^/]+/(eon|own|vj|src)/[A-Za-z0-9._-]+' | sort -u
> done | sort -u
> ```
>
> Union that with the walk-up result. Also check the plist's `StandardOutPath`/ `StandardErrorPath` and `WorkingDirectory` — those frequently point into the real repo even when `ProgramArguments` does not.
>
> **Corollary — a self-healing runner can be permanently poisoned while looking fine.** `iterm2-autosnapshot`'s shim rebuilds a missing venv, but caps attempts and persists the counter in `~/.local/state/<job>/venv-bootstrap-attempts.txt`. That counter had been sitting at `5/5` since Aug 21 and was never consulted, because the venv existed. Deleting the venv made the job hit the _stale_ exhausted cap on its first try and refuse to self-heal: `FATAL: venv bootstrap cap exhausted (5/5)`. Restoring deps is not enough — **reset the attempt counter and kickstart**, then confirm from the log that real work resumed (here, `[auto-snapshot] wrote 17 tabs`), not merely `exit 0`.

**Caveats:**

- Run `pgrep -fl 'cargo build|rustc|zig build'` first — never delete artifacts for a repo whose build/test is **currently running**.
- It's a regenerable-cost tradeoff: the next build is a cold rebuild (minutes for big Rust crates). Worth it for idle repos; skip the one repo you're about to build.
- `cargo clean` (run per-repo) is the tool-native equivalent of `rm -rf target` if you prefer.

## Phase 3 - Forgotten File Detection

Find large files that have not been accessed in 180+ days.

```bash
/usr/bin/env bash << 'STALE_EOF'
echo "=== Large forgotten files (>50MB, untouched 180+ days) ==="
echo ""

# Scan home directory (excluding Library, node_modules, .git, hidden dirs)
find "$HOME" -maxdepth 4 \
  -not -path '*/\.*' \
  -not -path '*/Library/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -type f -atime +180 -size +50M 2>/dev/null | \
while read -r f; do
  mod_date=$(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null)
  size=$(du -sh "$f" 2>/dev/null | cut -f1)
  echo "${mod_date} ${size} ${f}"
done | sort

echo ""
echo "=== Documents & Desktop (>10MB, untouched 180+ days) ==="
find "$HOME/Documents" "$HOME/Desktop" \
  -type f -atime +180 -size +10M 2>/dev/null | \
while read -r f; do
  mod_date=$(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null)
  size=$(du -sh "$f" 2>/dev/null | cut -f1)
  echo "${mod_date} ${size} ${f}"
done | sort
STALE_EOF
```

### Two traps when hunting big files

**1. Apparent size ≠ allocated size (sparse files).** `ls -l` and `find -size` report the file's _logical_ extent; `du` reports blocks actually on disk. A corrupted index or a database with a runaway seek produces a sparse file where these differ by orders of magnitude. Measured 2026-08-03 on a ChromaDB HNSW file:

```
ls -l  link_lists.bin  ->  2831.5 GB   (apparent — impossible on a 926 GB disk)
du -h  link_lists.bin  ->  174 GB      (actual)
```

Always size candidates with `du`. If `ls -l` reports more than the disk holds, you have found a sparse file — and usually a bug worth reporting upstream, not just disk to reclaim. **Never `cp` such a file** (a naive copy expands the holes).

**2. Applications quarantine their own wreckage — look for self-labelled dirs.** Well-behaved data stores rename a damaged collection rather than deleting it, and the new name states the diagnosis. Grep the biggest directory for these markers:

```bash
find "$BIG_DIR" -maxdepth 2 -name '*corrupt*' -o -name '*.drift-*' \
     -o -name '*.pre-rebuild-*' -o -name '*.bak-*' -o -name '*.quarantine*'
```

Before deleting one, prove it is unreferenced and superseded:

- no live process holds an fd inside it — `lsof -p <pid> | grep <dir>` returns 0;
- the app's own index/manifest does not mention its UUID;
- a healthy replacement exists and the app has completed a run since.

Real case: `~/.mempalace` had grown to **190 GB**, of which **175 GB** was one directory named `<uuid>.corrupt-20260802-160712.drift-20260802-160712` — the app had already diagnosed and set aside the damage from a 3-day crash loop, and a healthy 882 MB collection had replaced it. Deleting it took the volume from 82 % to 60 % full in one command.

### Common Forgotten File Types

| Type                  | Typical Location                                                 | Example                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| --------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Windows/Linux ISOs    | Documents, Downloads                                             | `.iso` files from VM setup                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| CapCut/iMovie exports | Movies/                                                          | Large `.mp4` renders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Phone video transfers | Pictures/, DCIM/                                                 | `.MOV` files from iPhone                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Old Zoom recordings   | Documents/                                                       | `.aac`, `.mp4` from meetings                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Orphaned downloads    | Documents/                                                       | `CFNetworkDownload_*.mp4`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Screen recordings     | Documents/, Desktop/                                             | Capto/QuickTime `.mov`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| TTS debug WAV         | `~/.local/share/tts-debug-wav/`, `~/.local/share/kokoro-debug*/` | Debug-mode TTS audio captures — can grow 1-2 GB/day if debug mode left on. Safe to `rm -rf` the contents. **Root cause for `~/.local/share/tts-debug-wav` (`claude-tts-companion`): retention is gated by a compile-time `#if DEBUG` in `AfplayPlayer.swift` — there is NO runtime env/config toggle. A RELEASE build deletes each WAV after playback via `PlaybackDelegate`. The permanent fix is reinstalling the companion as a release build (`make` in the plugin dir, which runs `swift build -c release`), not a pruner script.** For other TTS tools, look for a `tts-prune` mise task or tighter retention config |

## Phase 4 - Downloads Triage

Use AskUserQuestion with multi-select to let the user choose what to clean.

### Workflow

1. List all files in `~/Downloads` with dates and sizes
2. Categorize into logical groups
3. Present AskUserQuestion with categories as multi-select options
4. Offer personal/sensitive PDFs separately (keep, move to Documents, or delete)
5. Execute selected actions

### Categorization Pattern

```bash
/usr/bin/env bash << 'DL_LIST_EOF'
echo "=== Downloads by date and size ==="
find "$HOME/Downloads" -maxdepth 1 \( -type f -o -type d \) ! -path "$HOME/Downloads" | \
while read -r f; do
  mod_date=$(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null)
  size=$(du -sh "$f" 2>/dev/null | cut -f1)
  echo "${mod_date} ${size} $(basename "$f")"
done | sort
DL_LIST_EOF
```

### AskUserQuestion Template

When presenting Downloads cleanup options, use this pattern:

- **Question 1** (multiSelect: true) - "Which items in ~/Downloads do you want to delete?"
  - Group by type: movie files (with total size), old PDFs/docs, dev artifacts, app exports
- **Question 2** (multiSelect: false) - "What about personal/sensitive PDFs?"
  - Options: Keep all, Move to Documents, Delete (already have copies)
- **Question 3** (multiSelect: false) - "Ongoing cleanup tool preference?"
  - Options: dust + dua-cli, Hazel automation, custom launchd script

## Disk Analysis Tools Reference

### Comparison (Benchmarked on ~632GB home directory, Apple Silicon)

| Tool        | Wall Time | CPU Usage            | Interactive Delete       | Install                |
| ----------- | --------- | -------------------- | ------------------------ | ---------------------- |
| **dust**    | **20.4s** | 637% (parallel)      | No (view only)           | `brew install dust`    |
| **gdu-go**  | 28.8s     | 845% (very parallel) | Yes (TUI)                | `brew install gdu`     |
| **dua-cli** | 37.1s     | 237% (moderate)      | Yes (staged safe delete) | `brew install dua-cli` |
| **ncdu**    | 96.6s     | 43% (single-thread)  | Yes (TUI)                | `brew install ncdu`    |

### Recommended Combo

- **`dust`** for quick "where is my space going?" - fastest scanner, tree output
- **`dua i`** or **`gdu-go`** for interactive exploration with deletion

### Quick Usage

```bash
# dust - instant tree overview
dust -d 2 ~              # depth 2
dust -r ~/Library         # reverse sort (smallest first)

# dua - interactive TUI with safe deletion
dua i ~                   # navigate, mark, delete with confirmation

# gdu-go - ncdu-like TUI, fast on SSDs
gdu-go ~                  # full TUI with delete support
gdu-go -n ~              # non-interactive (for scripting/benchmarks)
```

### Install All Tools

```bash
brew install dust dua-cli gdu
```

**Note**: gdu installs as `gdu-go` to avoid conflict with coreutils.

## Quick Wins Summary

Ordered by typical space reclaimed (highest first):

| Action                          | Typical Savings | Risk                                      | Command                                                          |
| ------------------------------- | --------------- | ----------------------------------------- | ---------------------------------------------------------------- |
| Rust `target/` dirs (Phase 2.5) | 10-60 GB+       | None (cold rebuild on next `cargo build`) | `find ROOTS -type d -name target` + Cargo.toml-sibling guard     |
| Python `.venv` dirs (Phase 2.5) | 5-20 GB         | None (re-sync via `uv sync`)              | `find ROOTS -type d -name .venv -prune -exec rm -rf {} +`        |
| `go clean -cache`               | 5-25 GB         | None (re-downloads)                       | `go clean -cache`                                                |
| `uv cache prune`                | 5-40 GB         | None (drops only unused entries)          | `uv cache prune` (check `lsof ~/.cache/uv/.lock` first)          |
| `brew cleanup --prune=all`      | 3-10 GB         | None (re-downloads)                       | `brew cleanup --prune=all`                                       |
| Delete movie files in Downloads | 2-10 GB         | Check first                               | Manual after AskUserQuestion                                     |
| Prune old rustup toolchains     | 2-5 GB          | Keep current                              | `rustup toolchain list` then `rustup toolchain uninstall <name>` |
| Prune stale mise toolchains     | 0.5-3 GB        | Cross-check `.mise.toml` pins first       | `mise ls`, then `mise uninstall <tool>@<version>`                |
| `npm cache clean --force`       | 0.5-2 GB        | None (re-downloads)                       | `npm cache clean --force`                                        |
| `pip cache purge`               | 0.5-2 GB        | None (re-downloads)                       | `pip cache purge`                                                |
| Docker system prune             | 5-30 GB         | Removes stopped containers                | `docker system prune -a`                                         |
| Empty Trash                     | Variable        | Irreversible                              | `find ~/.Trash -mindepth 1 -delete` (NOT `rm -rf ~/.Trash/*`)    |

## Post-Change Checklist

After modifying this skill:

1. [ ] Cache commands tested on macOS (Apple Silicon)
2. [ ] Benchmark data still current (re-run if tools updated)
3. [ ] AskUserQuestion patterns match current tool API
4. [ ] All bash blocks use `/usr/bin/env bash << 'EOF'` wrapper
5. [ ] No hardcoded user paths (use `$HOME`)
6. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)

## Troubleshooting

| Issue                                                                      | Cause                                                                                                                                                                                          | Solution                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `uv cache clean` hangs / times out after 300 s                             | Lock held by a uv process — often a **persistent launchd daemon**, so it never releases                                                                                                        | `lsof ~/.cache/uv/.lock` to name the holder, THEN choose. Never blind `--force`. Prefer `uv cache prune`. See "uv cache lock" in Phase 2                                                                                                           |
| `rm -rf ~/.Trash/*` aborts with `no matches found` and exits 1             | The shell is **zsh**, whose default `nomatch` makes an unmatched glob a fatal error — so `rm` never runs, and the non-zero status can abort a `set -e` script or be misread as a failed delete | Use `find ~/.Trash -mindepth 1 -delete`, which is glob-free, handles spaces/brackets in the movie-release filenames, and is a no-op on an empty Trash                                                                                              |
| `brew cleanup` frees 0 bytes                                               | Already clean or formulae linked                                                                                                                                                               | Run `brew cleanup --prune=all`                                                                                                                                                                                                                     |
| `find` reports permission denied                                           | System Integrity Protection                                                                                                                                                                    | Add `2>/dev/null` to suppress                                                                                                                                                                                                                      |
| `gdu` command not found                                                    | Installed as `gdu-go`                                                                                                                                                                          | Use `gdu-go` (coreutils conflict)                                                                                                                                                                                                                  |
| `dust` shows different size than `df`                                      | Counting method differs                                                                                                                                                                        | Normal - `df` includes filesystem overhead                                                                                                                                                                                                         |
| Stale file scan is slow                                                    | Deep directory tree                                                                                                                                                                            | Limit `-maxdepth` or exclude more paths                                                                                                                                                                                                            |
| Docker not accessible                                                      | Desktop app not running                                                                                                                                                                        | Start Docker.app or skip Docker cleanup                                                                                                                                                                                                            |
| `parse error near TASK_ID=$(pueue add ...)` from heredoc with spaced paths | A user shell hook (e.g. pueue submission) re-parses the command string and breaks on `${var}/Path With Spaces/*` globs inside heredocs                                                         | Write multi-line scripts to `/tmp/<name>.sh` first via Write tool, then invoke as `bash /tmp/<name>.sh` — bypasses the inline heredoc → hook re-quote path entirely                                                                                |
| Removing a mise toolchain triggers immediate auto-reinstall                | A project's `.mise.toml` pins the version you just removed; mise restores it on next invocation from that project                                                                              | Before `mise uninstall <tool>@<version>`, grep all reachable `.mise.toml` and `mise.toml` files for the version. If pinned, leave it alone or update the pin first. Same applies to rustup toolchains vs. `rust-toolchain.toml` files in projects. |

### Hook-safe multi-line scripts

If the user's shell environment has bash hooks that intercept tool calls (pueue, asciinema, etc.) and the heredoc pattern fails with cryptic parse errors, write the script to a temp file and invoke it:

```bash
# Instead of: bash << 'EOF'  ... EOF
# Use: Write tool → /tmp/<task>.sh, then:
bash /tmp/<task>.sh
```

Single-line bash invocations like `du -sh "$HOME/Library/Application Support"/Google/* 2>/dev/null | sort -rh | head` work fine even with hooks installed — only multi-line heredocs containing spaced-path globs are problematic.

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Fix any script, reference, or dependency that no longer matches reality.
4. **Log it.** — Evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
