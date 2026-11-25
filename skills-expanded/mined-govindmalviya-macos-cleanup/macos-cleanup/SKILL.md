---
name: macos-cleanup
description: Use when the user wants to free disk space on macOS, find leftover files from uninstalled apps, audit what is installed, or figure out why their Mac is slow or full. Scans every install surface (Homebrew, npm, .pkg installers, curl installers, language toolchains, app support data), proves what is actually used before suggesting anything, then removes only what the user confirms.
---

# macOS Cleanup

Free disk space without breaking anything.

## The shape of this skill

The scripts gather facts. **You do the judging.** They are `du`, `pkgutil` and
`lsof` with a nice window on the end — they cannot tell a build cache from the
only copy of something, and they do not know this machine.

So: run the read-only scan, **read the rows yourself**, investigate what the
rows cannot answer, and only then put a window in front of the user. A run where
you pipe `pick.sh` into `clean.sh` without reading anything is a failed run.

**Two things stay rigid, because they are what keep this safe:**

- **The GUI is the confirmation step.** Never print the candidate list as a chat
  table and never ask the user to type or paste paths. Talk *about* rows; do not
  reproduce them.
- **Never remove anything the user has not ticked or confirmed.**

### 1. Scan, then read the rows

```
bash scripts/candidates.sh
```

Read-only, deletes nothing, writes `/tmp/macos-cleanup-candidates.tsv`.

```
column -ts$'\t' /tmp/macos-cleanup-candidates.tsv | sort -rn
```

Fields: `size_mb`, `path`, `why`, `class` (`cache`/`orphan`/`ask`), `restore`,
`lastused`. Read every row. `pick.sh` reuses this scan for 10 minutes, so
reading first costs nothing.

### 2. Work out what the rows do not say

The TSV is pattern-matching. Before anyone ticks a box, answer these:

**What kind of machine is this?** iOS work, Android, Go, Rust, data science? It
changes which caches are cheap and which are a workday to rebuild.

```
ls ~/Library/Developer/Xcode 2>/dev/null; ls ~/.gradle 2>/dev/null; ls ~/code ~/Projects ~/dev 2>/dev/null | head -30
```

**Is the big stuff even in the list?** The picker has a fixed path list. The
largest pile on a developer machine is usually project build output or Xcode,
and it is frequently absent. Check before concluding the picker found it all:

```
du -sh ~/Library/Developer/Xcode/DerivedData ~/Library/Developer/Xcode/iOS\ DeviceSupport 2>/dev/null; df -H / | tail -1
```

**Is each `ask` row actually unused?** Run the four checks in step 3 for every
`ask` row before you say a word about it.

**Does any row have a non-`-` restore cost?** Say the restore command out loud
before the window opens, not after. `ms-playwright`, `puppeteer`, `Cypress` and
`~/Library/pnpm/store` all live under cache-looking paths and all need a manual
command to come back.

If you cannot answer a question from the shell, ask the user. One question is
cheaper than a wrong deletion.

### 3. Prove usage before recommending removal

Check all four. One hit means keep it.

```
grep -ac "toolname" ~/.zsh_history
```

```
ls -d ~/.toolname ~/.config/toolname 2>/dev/null
```

Project markers under `~/code` (or wherever they work):
`go.mod` → Go · `wrangler.jsonc` → wrangler · `yarn.lock` → yarn ·
`hugo.toml` → hugo · `*.tf` → terraform · `Package.swift` → Swift

And for Homebrew, always:

```
brew uses --installed FORMULA
```

Empty output means nothing depends on it. Non-empty means **do not remove it**.

### 4. Open the window, with your read alongside it

```
bash scripts/pick.sh
```

A native macOS window with real checkboxes, sizes and reasons. Selections land
in `/tmp/macos-cleanup-selected.txt`. It deletes nothing.

Beside it, give **five lines at most** — your judgment, not a re-listing:

- the one or two rows you would not tick, and why
- any restore command they are about to owe
- anything large you found that the window does not offer
- what is missing from the picture entirely (`du` skips TCC-protected dirs, so
  totals will not sum — say so rather than presenting a wrong number)

If the GUI cannot run — over SSH, or `pick.sh` says the window failed:
`--list` (plain text), `--web` (browser checkboxes), `--native` (dialog).

### 5. Remove what they ticked

```
bash scripts/clean.sh
```

Removes exactly the ticked paths, refuses protected ones, reports real space
reclaimed. `--dry-run` to preview, `--permanent` to skip the Trash.

**How things are removed:** pure build caches are deleted outright, because they
rebuild themselves and the point is to free space now. Everything else goes to
the **Trash**, so a wrong call costs a drag to undo. Routing through Finder also
gets past TCC on `~/Library/Containers`, which refuses `rm` even under `sudo`.

Trashed items still take up disk. If anything was trashed, tell the user the
space is not free until they empty it, and give them the command.

### 6. Go wider when the picker was not enough

Use this when the user asks *why* the disk is full, when the machine is slow, or
when step 2 said the big piles are outside the picker's path list.

```
bash scripts/scan.sh > /tmp/cleanup-scan.txt 2>&1; tail -5 /tmp/cleanup-scan.txt
```

Read the file. One read-only pass over every install surface, ~60s: Homebrew,
npm prefixes, pkg receipts, launch agents, orphaned processes, broken symlinks.

If the user said the machine is **slow** (not just full), read
`reference/slowness.md` first — a runaway process matters more than disk space.

Findings here have no checkbox UI, so they go through classify-and-confirm
below.

### 7. Classify what the wide scan turned up

For each thing the scan found, decide one of three:

| Class | Meaning | Action |
|---|---|---|
| **Orphaned** | The app is gone, only its data remains | Recommend removal |
| **Regenerable** | A cache or store that rebuilds itself | Recommend clearing |
| **In use** | Evidence says they use it | Keep, say why |

**Never classify from the name alone.** Get evidence — same four checks as
step 3, every time.

### 8. Present one confirmation table

Only for wide-scan findings. Picker rows already had their window.

Group by decision, biggest first. Every row needs a size and a reason.

```
## Recommend removing — 8.2 GB

| What | Size | Why it is safe |
|---|---|---|
| ~/.lmstudio | 4.8 GB | LM Studio.app is deleted; orphaned models |
| ~/.yarn/berry | 3.9 GB | cache, rebuilds on next install |

## Keeping — evidence of use

| What | Size | Evidence |
|---|---|---|
| /usr/local/go | 277 MB | 3 projects with go.mod, one edited this week |

## Needs your decision

| What | Size | Question |
|---|---|---|
| /usr/local/aws-cli | 217 MB | No history hits. Do you still use AWS? |
```

Then ask once: **"Remove everything in the first table?"** Let them subtract.

### 9. Execute

Read `reference/safety.md` before the first destructive command. It covers the
four failure modes that will bite you: TCC-protected paths, root-owned paths,
data directories, and `rtk` intercepting `find`.

Order matters:

1. Quit the app first — `osascript -e 'quit app "Name"'`
2. Use the package manager if there is one — `brew uninstall --cask --zap NAME`
3. Then `rm -rf` the leftovers
4. Then `brew autoremove && brew cleanup`
5. Then clean broken symlinks and dead PATH lines

### 10. Verify and report

Every run ends here, picker or wide scan.

```
df -H / | tail -1
```

Report actual reclaimed space, not predicted. If a removal freed less than
expected, say so and find out why — do not quietly move on.

End with anything the user must run themselves (sudo, Finder) as one command
per block.

## Before recommending anything, read the catalog

`reference/catalog.md` lists every location worth checking, grouped by what
restoring it costs. Consult it when the user asks what else can go, or when a
candidate is not in the picker.

Highest-yield categories, in order:

1. **Project build output** — `.next`, `target`, `dist`. Usually the single
   largest pile on a developer machine and the one most tools miss entirely.
2. **Xcode** — `DerivedData` and `iOS DeviceSupport`, often 10 GB+.
3. **`~/.gradle/caches`** on Android machines.
4. **Orphaned app data** from uninstalled apps.
5. **`docker system prune -a`** rather than deleting VM images by hand.

## Hard-won rules

- **`brew leaves` and `npm ls -g` see only brew and npm.** AWS CLI, Go, podman and
  Docker install via `.pkg` and are invisible to both. Always run `pkgutil --pkgs`.
- **`npm prefix -g` may not be where packages live.** If a global uninstall says
  "up to date" and does nothing, the package is under a different prefix. Check
  `/opt/homebrew/lib/node_modules` and pass `--prefix /opt/homebrew`.
- **A cache is not "in use" just because it is recent.** Yarn, uv, go modcache and
  Homebrew caches all rebuild on demand. Clearing them is always safe.
- **Deleting a binary does not kill a running process.** It keeps its open handle.
  Check `lsof` for a `txt` entry at a path that no longer exists.
- **`du` silently skips TCC-protected directories.** Totals will not sum to their
  parts. Say so rather than presenting a wrong number as fact.
- **The macOS Storage pane lies.** Its categories are cached Spotlight metadata
  and lag by hours. "Documents" is a catch-all, and iCloud-optimized files are
  counted at full size even when only a thumbnail is local. Trust `df`, not the pane.
- **Do not predict how much a deletion will free.** Measure before, measure after.
- **"It is only a cache" can still break things.** `ms-playwright`, `puppeteer`,
  `Cypress` and `~/Library/pnpm/store` all sit under cache paths but need a manual
  command to restore. Every candidate carries a `restore` field — if it is not `-`,
  say the command out loud before removing and again in the summary.
- **Never delete `node_modules` in a project touched recently.** The picker only
  offers ones untouched for 90+ days.
- **`rtk` rewrites `find` and `grep`.** `grep -v` can emit a match report instead
  of filtered lines, silently emptying a file it is piped into. Use `awk`, `sed`
  or python, and read the file back before acting on it.

## Never touch without asking

- `node_modules` in a project touched in the last 90 days
- `~/Library/Application Support/MobileSync/Backup` — iPhone backups, often the
  only copy of that data
- `~/Library/Developer/Xcode/Archives` — the binaries you shipped, plus the dSYMs
  needed to symbolicate real crash reports
- Any `.git` directory
- A database data directory without asking what is in it
- `/System`, `/private/var/vm`, `/private/var/db` — macOS owns these
- Anything with a non-empty `brew uses --installed`
- `~/Library/Mail`, `~/Pictures/*.photoslibrary` — TCC-protected, and deleting
  a Photos library while iCloud Photos is on just makes it re-download

## Files

- `scripts/pick.sh` — GUI picker (`--list`, `--web`, `--native` fallbacks)
- `scripts/candidates.sh` — read-only candidate detection, writes the TSV
- `scripts/clean.sh` — removes selections (`--dry-run`, `--permanent`)
- `scripts/Picker.swift` — the native window, compiled and cached on first run
- `scripts/scan.sh` — the wider read-only inventory pass
- `reference/catalog.md` — every path worth checking, by restore cost
- `reference/safety.md` — failure modes and how to handle them
- `reference/slowness.md` — triage when the Mac is slow, not just full
