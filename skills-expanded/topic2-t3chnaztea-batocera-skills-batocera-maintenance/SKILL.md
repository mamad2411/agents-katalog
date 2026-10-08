---
name: batocera-maintenance
description: >-
  Use when keeping a Batocera cabinet healthy over time: running scripts or
  scheduled jobs at boot and on an interval without cron, the custom_service
  boot-service pattern (which replaced custom.sh in v43), backing up /userdata
  to another machine over SSH, and upgrading between major Batocera versions
  (v42 to v43 and similar) including the ROM-directory renames and post-upgrade
  checklist. Covers why there is no crond, the backup-before-upgrade doctrine,
  and catch-up scheduling. Not for performance tuning (batocera-tuning).
compatibility: Requires SSH access to a Batocera host (tested on v41-v43).
---

# Batocera Maintenance

Keeping the cabinet healthy: running things at boot and on a schedule, backing up
what matters, and surviving version upgrades. Assumes the connection pattern and
filesystem model from `batocera-ops`.

## There is no crond — use a boot service

Batocera does **not** run a general-purpose `crond`. Don't write a crontab and
assume it fires; it won't. The mechanism for "run this at boot / on a schedule"
is a **boot service**.

Since v43, the entry point is `/userdata/system/services/custom_service` (it
replaced `/userdata/system/custom.sh`; the upgrade auto-converts an existing
`custom.sh`). A service is a script Batocera runs at boot with a `start`
argument. Enable/inspect services:

```bash
SSHB "batocera-services list"
SSHB "cat /userdata/system/services/custom_service"
```

### Scheduling without cron: the boot-loop pattern

To run something periodically, the service launches a background loop that sleeps
and re-checks. This is how the cabinet does hourly/daily/monthly work with no
cron:

```bash
# inside custom_service, on the 'start' case:
(
  while true; do
    # hourly re-assert (e.g. CPU governor; see batocera-tuning)
    /etc/init.d/S18governor start 2>/dev/null

    # once-a-day / once-a-month gating: compare a stamp file to `date`
    stamp=/userdata/system/.last-monthly-backup
    if [ "$(cat "$stamp" 2>/dev/null)" != "$(date +%Y-%m)" ]; then
      /userdata/system/tools/backup-to-remote.sh && date +%Y-%m > "$stamp"
    fi

    sleep 3600
  done
) &
```

Key ideas:
- **Catch-up, not clock-exact.** Gate on "has this period's job run yet?"
  (compare a stamp to `date +%Y-%m` or `%Y-%m-%d`), not on "is it exactly 3 AM?".
  A cabinet that's powered off at 3 AM would never run a clock-exact job; the
  stamp approach runs it on the first boot of the new period instead.
- **Idempotent body.** The loop may re-enter; the gated job must be safe to skip
  when already done this period.
- **Don't park schedulable scripts in `/userdata/system/scripts/`** — ES invokes
  executables there as game event hooks (see `batocera-ops` → emulationstation).
  Put tools in `/userdata/system/tools/` or similar and call them from the
  service.

After editing `custom_service`, back it up first and test the loop logic before
relying on it (run the gated command by hand once).

## Backups

The doctrine: **push-only, dry-run-first, over SSH.** The cabinet pushes a copy
of the important parts of `/userdata` to another machine; you always dry-run an
rsync before letting it delete anything. Architecture, what to include/exclude,
and the catch-up schedule are in [references/backup.md](references/backup.md).

**Back up before every upgrade.** A major-version upgrade is the highest-risk
routine event; a fresh backup of saves/system/bios (and ideally decorations/
shaders/themes) is the difference between a 10-minute rollback and a rebuild.

## Version upgrades

Major Batocera upgrades rename ROM directories, change the boot-service model,
and swap emulators — each of which silently breaks things if you don't migrate.
The v42→v43 migration (representative of the class) with the full rename table
and a post-upgrade checklist is in
[references/v42-to-v43.md](references/v42-to-v43.md). The short doctrine:

1. Full backup first (above).
2. Upgrade.
3. Walk the post-upgrade checklist: move content out of renamed/stub dirs,
   migrate moved saves, confirm the boot service converted, and **re-check the
   CPU governor** (a v43 build can boot stuck in powersave — see
   `batocera-tuning`).
4. Verify a game from each major system actually launches before calling it done.
