---
name: makleen
description: Find and reclaim disk space on a Mac with makleen, a zsh cleaner for developer machines. Use when the user's Mac is low on disk space or they ask what is using storage, or want to clean caches (npm, Docker, Xcode, Gradle, Homebrew, browsers, editors), node_modules and build folders of old projects, data left behind by uninstalled apps, worktrees and temp files of AI coding agents, simulators, emulators or old Node versions. Also use to list, restore or purge makleen's quarantine. macOS only.
---

# makleen

makleen scans a Mac for space it can reclaim and cleans only the items it is given. It moves leftovers of
uninstalled apps to a quarantine they can be restored from, and deletes caches and build folders. Every
clean is logged. Work through makleen instead of deleting files yourself: it holds the safety checks
(`NEVER_TOUCH`, `PROTECT`, nothing less than two levels below `~`, items of running apps locked).

## Find it

Run `command -v makleen`. If it prints nothing, makleen isn't installed: tell the user it installs with
`brew install decoded-cipher/tap/makleen`, and install it only if they say so. This skill needs makleen
0.4.0 or later (`makleen --version`); if it's older, suggest `brew upgrade makleen`.

Always pass `--dry-run` or `--yes` to `makleen clean`, and never run plain `makleen`: they wait for
keys in a checklist or a prompt you can't answer.

## Steps

1. **Scan.** `makleen scan --json`. It changes nothing and takes up to a few minutes, so allow a long
   timeout. Add categories to scan less: `makleen scan caches projects --json`. Categories are
   `leftovers`, `caches`, `agents`, `projects` and `extras`.
2. **Explain.** Summarise for the user: free space, the total per category, and the largest items with what
   cleaning each one does. Group by what happens: quarantined and restorable, deleted and rebuilt
   on its own, deleted until reinstalled. Mention items that are `locked` and why. Quarantined leftovers
   keep using space until `makleen purge`, so say that before the user counts on it.
3. **Recommend, then let the user choose.** `preselected` is makleen's default pick; recommend from it.
   Items with `flag: "check-first"` have an unclear owner: before recommending one, look inside its paths
   (read only) and say who you think owns it. `flag: "optional"` items are large things the user may still
   want, such as simulators or models; ask about each one.
4. **Dry run.** `makleen clean --id ID1,ID2,... --dry-run` with exactly the IDs the user chose. Show the
   plan it prints. A warning that an ID wasn't found means the item changed: scan again.
5. **Clean** only after the user says yes to that plan: run the same command with `--yes` instead of
   `--dry-run`. Report the free space before and after, the log file, and for leftovers the quarantine
   batch and its undo command (`makleen restore BATCH`).

## Rules

- Always pass `--id` with `--yes`. Without it, `--yes` cleans makleen's whole default selection.
- Never add IDs the user didn't approve, and never run `--yes` on a plan the user hasn't seen.
- A `locked` item can't be cleaned. If it says `in use`, ask the user to quit that app, then scan again.
- `makleen purge` deletes quarantined leftovers for good. Run it only when the user asks, and show
  `makleen quarantine` first.
- Cleaning writes outside the project folder. If your sandbox blocks it, ask the user for the permission
  you need instead of working around it.
- If the user wants something never touched, suggest a `NEVER_TOUCH` or `PROTECT` line in
  `~/.config/makleen/config.zsh`, and edit that file only with their OK.

## Scan JSON

```json
{
  "version": "0.3.0",
  "disk": {"used_kb": 224100648, "free_kb": 239062052},
  "full_disk_access": false,
  "items": [
    {"id": "caches/npm-cache", "category": "caches", "label": "npm cache", "size_kb": 3774873, "size": "3.6 GB",
     "action": "command", "paths": [], "command": "npm cache clean --force", "note": "via `npm cache clean --force`",
     "flag": null, "locked": null, "preselected": true}
  ],
  "notes": [],
  "unused_apps": [{"name": "Android Studio", "size_kb": 2670352, "days_unused": 247}],
  "kept_active_kb": 14648364,
  "quarantine_kb": 0
}
```

- `action`: `quarantine` (moved, restorable), `delete` (the `paths` are deleted) or `command` (runs `command`).
- `flag`: `null`, `check-first` (owner unclear) or `optional` (a large optional item).
- `locked`: why it can't be cleaned now (`in use`, `needs Full Disk Access`), or `null`.
- `unused_apps` is report only: makleen doesn't uninstall apps. Suggest the user removes them.
- `kept_active_kb`: build folders left alone because their project was used recently.
- With `full_disk_access: false`, Mail, Messages, Photos, Safari and the Trash weren't measured, and
  leftovers in app containers are locked. The user can grant Full Disk Access to the app running you in
  System Settings → Privacy & Security.

## Other commands

| Command | Does |
|---|---|
| `makleen quarantine` | lists quarantined batches with size and contents |
| `makleen restore BATCH` | moves a batch back; never overwrites |
| `makleen purge [--older-than N \| --all]` | permanently deletes old batches |
| `makleen scan --days N --json` | counts projects as idle after `N` days instead of 60 |
