---
name: haos-cloud-backup
description: Ship Home Assistant OS (HAOS) backups off the SD card to cloud storage (Google Drive or any rclone remote) with an upload bandwidth cap and a GFS-style retention policy (daily/weekly/monthly thinning), using the Rclone Backup add-on. Use when the user wants HA backups uploaded to Google Drive / Dropbox / cloud, complains the SD card is filling up with backups, needs 異地備份 for Home Assistant, or asks to rate-limit / throttle backup uploads because home upstream bandwidth is scarce. Also consult before suggesting the native google_drive backup agent or the sabeechen add-on — neither can throttle upload speed.
---

# HAOS Backups → Cloud (rclone, throttled, GFS retention)

Get HA's daily automatic backups off the single SD card to cloud storage, without
saturating a small home uplink, and with automatic thinning on both ends.
Battle-tested 2026-07-11 on a Raspberry Pi 4 (HAOS 18.1, Core 2026.6.4) with
**jcwillox/hassio-rclone-backup** v3.4.1 → Google Drive. ⚠️ marks real pitfalls.
`ha` = SSH alias per `haos-addon-deploy` §0/§8 (`bash -lc` rule applies).

## 0. Why this route

- ⚠️ **Only rclone can throttle.** The native `google_drive` backup agent has no
  bandwidth option, and sabeechen/hassio-google-drive-backup closed the throttle
  request as not-planned (issue #366). If upload speed matters, rclone is the
  only game in town: `--bwlimit` takes **MBytes/s** (`1.5M` = 12 Mbit/s — a
  sensible cap is ~30% of the measured uplink).
- rclone has no built-in grandfather-father-son retention, but HA backup
  filenames embed the date (`Automatic_backup_<ver>_YYYY-MM-DD_HH.MM_<id>.tar`),
  so date-anchored filters emulate it (§4).
- Schedule uploads right after HA's automatic backup time (default ~05:00 →
  upload 05:30): off-peak, and each day moves only one new file.

## 1. Install the add-on

```bash
ssh ha 'bash -lc "ha store add https://github.com/jcwillox/hassio-rclone-backup && ha store reload"'
ssh ha 'bash -lc "ha apps install 19a172aa_rclone_backup"'
```

Single-add-on repo; installed slug is `19a172aa_rclone_backup` (hash is fixed by
the repo URL). ⚠️ `ha store add`, not `add-repository` — see `haos-addon-deploy` §2
for the silent-wrong-subcommand trap.

## 2. Cloud auth (rclone.conf) — do this BEFORE configuring jobs

⚠️ **Chicken-and-egg**: the add-on validates every job's remote at startup and
**halts FATAL** if `rclone.conf` is missing or the remote isn't defined yet. Keep
`jobs: []` until the remote exists (or expect `state: error` — harmless but
confusing).

Config lives at **`/homeassistant/rclone.conf`** (same folder as
`configuration.yaml`; the path is the add-on's `config_path` default). Two ways in:

- **Web UI route**: start the add-on (empty jobs) → Open Web UI. ⚠️ The login
  page is cosmetic — the GUI runs with `--rc-no-auth`; keep the prefilled URL,
  leave username/password **blank**, click Login. Configs → create remote. OAuth
  through ingress can fail on the localhost redirect, which leads to:
- **Token-paste route (robust, used in the field)**: on any machine with a
  browser, `rclone authorize "drive"` → user completes the Google consent → the
  command prints a token JSON block. Write the conf and ship it:

  ```ini
  [gdrive]
  type = drive
  scope = drive
  token = {"access_token":"...","refresh_token":"...","expiry":"..."}
  ```

  `chmod 600`. The refresh token self-renews on the device from then on — the
  helper machine's rclone can be uninstalled. Verify from inside the container:

  ```bash
  ssh ha 'sudo docker exec addon_19a172aa_rclone_backup \
      rclone --config /homeassistant/rclone.conf about gdrive:'
  ```

- ⚠️ The Web UI only shows rclone remotes and live transfers. Jobs, schedules
  and bwlimit are **add-on options** (HA → Settings → Apps → the add-on →
  Configuration tab) — users looking for settings in the Web UI find nothing.
- ⚠️ **Display quirks that look like corruption but aren't**: the HA YAML
  editor may render a `flags:` map back as a Python-repr string
  (`"{'bwlimit': '1.5M'}"`) — cosmetic; trust the job log
  (`Starting bandwidth limiter at 1.500Mi Byte/s`) over the editor. Likewise
  the `?` characters in date filters (`*_????-??-01_*`) are rclone
  single-character glob wildcards, not mojibake — users report both as broken.

## 3. Jobs (upload + prune)

Field notes that cost real debugging time:

- ⚠️ **`delete` jobs put the path in `source`, never `destination`** — the
  add-on halts FATAL with "at least 1 source must be specified".
- `flags:` is a map (underscores auto-convert to dashes). Ordered `--filter`
  rules must go in `extra_flags` — order matters and `include:`/`exclude:`
  arrays don't guarantee it.
- A job with no `schedule` runs at add-on startup — handy for a one-shot test,
  dangerous on delete jobs.
- **Filename rename is what makes name-based filters work**: HA natively
  stores backups as `<slug>.tar` (8 hex chars, unreadable). The add-on renames
  files in `/backup` **in place** to `{name}_{date}_{slug}.tar` (the
  `renamed/unrenamed N backups` log lines; first run also renames pre-existing
  backups) — the `+ Automatic_backup_*` filters above match these renamed
  names, and local/remote filenames stay identical. Harmless to HA: the
  Supervisor identifies backups by tar metadata, not filename, so restore is
  unaffected; the trailing slug still maps back to the HA backup ID.
- **Global `dry_run: true` = free rehearsal, but remember to flip it off.**
  Recommended flow: leave it on through the first scheduled day, read the
  `Skipped ... as --dry-run is set` lines as validation that every job selects
  exactly the right files, then set `dry_run: false` and restart. ⚠️ While it's
  on, **nothing uploads or deletes at all**, yet every job logs "finished" and
  the log looks healthy at a glance — easy to forget for weeks.

```yaml
jobs:
  - name: upload to cloud
    schedule: "30 5 * * *"
    command: copy            # copy, not sync — never mirror deletions upward
    sources: [/backup]
    destination: "gdrive:HA-Backups"
    flags: { bwlimit: 1.5M }
  - name: prune local autos
    schedule: "0 7 * * *"
    command: delete
    source: /backup
    flags: { min-age: 7d }   # SD card keeps ~7 dailies
    extra_flags: ["--filter", "+ Automatic_backup_*", "--filter", "- *"]
  - name: prune local others   # named/milestone + addon-update backups
    schedule: "5 7 * * *"
    command: delete
    source: /backup
    flags: { min-age: 90d }
```

## 4. GFS thinning on the remote (date-anchored)

Weekly keeper = day-of-month 01/08/15/22; monthly keeper = day 01. Not "every
Monday" — anchors are calendar dates, same density. Filter order is
first-match-wins: protect anchors, then match the daily pattern, then drop the
rest. Named backups never match the pattern, so they survive forever.

```yaml
  - name: thin to weekly (7d-28d)
    schedule: "10 7 * * *"
    command: delete
    source: "gdrive:HA-Backups"
    flags: { min-age: 7d, max-age: 28d }
    extra_flags: ["--filter", "- *_????-??-01_*", "--filter", "- *_????-??-08_*",
                  "--filter", "- *_????-??-15_*", "--filter", "- *_????-??-22_*",
                  "--filter", "+ Automatic_backup_*", "--filter", "- *"]
  - name: thin to monthly (28d-180d)
    schedule: "15 7 * * *"
    command: delete
    source: "gdrive:HA-Backups"
    flags: { min-age: 28d, max-age: 180d }
    extra_flags: ["--filter", "- *_????-??-01_*",
                  "--filter", "+ Automatic_backup_*", "--filter", "- *"]
  - name: purge (>180d)
    schedule: "20 7 * * *"
    command: delete
    source: "gdrive:HA-Backups"
    flags: { min-age: 180d }
    extra_flags: ["--filter", "+ Automatic_backup_*", "--filter", "- *"]
```

Before trusting any delete job, run its exact command manually with `--dry-run`
inside the container (`sudo docker exec addon_19a172aa_rclone_backup rclone …`)
and read what it *would* delete. Google Drive deletes go to trash by default
(30-day extra safety net); add `drive-use-trash: false` only if quota is tight.

## 5. Cleaning up an existing backlog

Old backups often pile up (retention was never on). Rules:

- ⚠️ **Delete through the Supervisor, not `rm`**: `ha backups remove <slug>` —
  raw `rm` leaves the Supervisor's backup list stale.
- ⚠️ **The Supervisor list shows UTC dates; filenames show local time** — a
  05:00 local backup lists as the *previous* day. Match by full ISO timestamp
  (or slug), never by date string.
- Order of operations: verify the cloud copy exists **first**, then delete
  local. First test upload: run the copy manually with `--bwlimit` and compare
  the byte size on the remote (`rclone ls`) against the source file.

## 6. Verify end-to-end

```bash
ssh ha 'bash -lc "ha apps logs 19a172aa_rclone_backup"'   # want: "scheduled jobs:" listing all
ssh ha 'sudo docker exec addon_19a172aa_rclone_backup rclone --config /homeassistant/rclone.conf ls gdrive:HA-Backups'
```

A 611 MB backup at `bwlimit 1.5M` takes ~7 minutes — if it finishes much faster,
the cap isn't being applied (check the flag reached the command in the job log).

## 7. Changing options from the CLI (e.g. flipping dry_run off)

For a human at the UI, **Configuration tab → ⋮ → Edit in YAML → Save → restart**
is the normal route — this section is for headless/agent changes over SSH.

⚠️ `ha apps` has **no `options` subcommand** — set options via the Supervisor
API. Always send the **full options object** (fetch → mutate → POST), never a
partial one:

```bash
ssh ha 'bash -lc "ha apps info 19a172aa_rclone_backup --raw-json"' > opts.json
python3 - <<'EOF'
import json
d = json.load(open('opts.json'))['data']['options']
d['dry_run'] = False
json.dump({'options': d}, open('payload.json', 'w'), ensure_ascii=False)
EOF
ssh ha 'bash -lc "curl -sS -X POST -H \"Authorization: Bearer \$SUPERVISOR_TOKEN\" \
    -H \"Content-Type: application/json\" -d @- \
    http://supervisor/addons/19a172aa_rclone_backup/options"' < payload.json
ssh ha 'bash -lc "ha apps restart 19a172aa_rclone_backup"'
```

- ⚠️ **Escape it as `\$SUPERVISOR_TOKEN`.** The remote parent shell is
  non-login: an unescaped `$SUPERVISOR_TOKEN` expands there to empty and the
  API answers a misleading `401: Unauthorized` (the var must expand inside
  `bash -lc`, which loads the env).
- Keep the pre-change `opts.json` as the rollback copy; verify afterwards with
  `ha apps info --raw-json` (want `"dry_run": false`, jobs intact) and the log's
  `scheduled jobs:` listing.
