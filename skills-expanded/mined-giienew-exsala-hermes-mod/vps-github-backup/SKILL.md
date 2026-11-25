---
name: vps-github-backup
description: "Use when running or fixing the VPS-to-GitHub daily backup."
---

# VPS → GitHub Backup

Recurring backup of Hermes config, secrets, skills, and farm-ops dirs to a GitHub **PRIVATE** repo. Standing cron was: `0 3 * * * bash ~/app` (root/ubuntu crontab). Known-good script: `scripts/backup_to_gh.sh` — deploy it to `~/app` (keep that name: the cron and runtime steps reference it).

> **State — cron DISABLED by user (2026-10-22).** Crontab emptied; user said "hapus cron auto backup ke gh semua". Script + `~/.git_token` left in place; no systemd/cron.d/root/other crontab references remain (verified). Re-enable only if user asks again. If a future session sees this skill made 'standing cron' a requirement, remember: the standing part is OPTIONAL now.

## Procedure
1. **Verify push auth BEFORE running.** The pack/split/commit half always succeeds; a missing credential only surfaces as a trailing `FAIL no credential` in the log. On this box the provisioned auth is the PAT in `~/.git_token` (user `giienew`); an SSH key was never set up, so never default the push URL to `git@`. Check in order: `~/.git_token` exists → token URL push; else `~/.ssh/id_ed25519` → SSH push; else stop and tell the user which credential to recreate.
2. Source only what matters: Hermes `config.yaml` + `.env` + skills/plugins/profiles/cron/state.db/sessions → `config.tgz`; `farming/` dirs + farm scripts → `ops.tgz`. Append `|| true` and `--ignore-failed-read` so one missing path never aborts the whole run.
3. Split every tgz with `split -b 90m -d -a 2 <f> <f>_part` and delete the original — GitHub's per-file cap is ~95MB, so a >100MB tarball is rejected. Splitting is mandatory, not optional.
4. `git add -A` exactly once; commit once with `-c user.email=... -c user.name=...` and `--allow-empty`. Inline identity survives a missing global gitconfig; `--allow-empty` keeps a no-change daily run pushable.
5. Push `-f` to `HEAD:master`, append `OK/FAIL <timestamp>` to `$HOME/backup.log`. "Backup is healthy" = one `OK` line in that log, not script exit code.
6. **Repo MUST be private** — config.tgz embeds `~/.hermes/.env` with real bot tokens/router keys. A public backup repo = every secret leaked.

## Restore to a New VPS (when `restore_new_vps.sh` is absent/outdated)
The inverse operation reads from the same private repo. Steps, with the two fixes that made this session's script work:
1. **Download each `*_partNN` over raw, not the API**: `curl -fsSL -H "Authorization: Bearer $(cat ~/.git_token)" -o config.tgz https://raw.githubusercontent.com/giienew/hermes-backup/master/config.tgz_part00`. A private repo's raw URL returns 404 without the token — the 404 is an auth signal, not a missing file, so do not assume the blob is gone.
2. Rejoin split parts: `cat config.tgz_part* > config.tgz`. List-only verify, NEVER extract into live home: `tar -tzf config.tgz | head` — keep the tree untouched until the script is final.
3. `bash -n` the restore script before running.
4. Remove the downloaded tarballs when they were test pulls — a stale tgz next to the script can be mistaken for a fresh restore.
5. Installer for a fresh Hermes: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash` — fake mirrors like `hermes-agent.ai` 404; the canonical path is the raw file in the `NousResearch/hermes-agent` repo (`scripts/install.sh`), never invent the URL from memory.

## Pitfalls
- **Silent-auth-failure trap**: tar/split/commit succeed, then push dies on a missing credential. Verify auth upfront and always read `backup.log` after a run — the result lives there.
- Defaulting the script to `git@github.com:...` when only the PAT exists guarantees FAIL. Token-first, SSH-second, in that order.
- `git add` twice in one run re-stages nothing useful; it runs once.
- Split at 90MB, never 100 — GitHub drops files over ~95MB.
- After editing the script, `bash -n` it before running.
- **Check for a standing cron BEFORE claiming backup is live**: `0 3 * * * bash ~/app` may or may not be in crontab (the user disabled it 2026-10). A backup can still be run on-demand by invoking `~/app` — the cron is just the scheduling. To (re)install: `crontab -l | grep -v backup_to_gh.sh | crontab -` deletes; add the line back to restore. Confirm actual state with `crontab -l` + `grep -rniE 'backup_to_gh' /etc/cron*` — don't assume from memory.
- A standing cron keeps running a deleted script or a dead token silently. If `backup_to_gh.sh` or `~/.git_token` is missing, don't trust "cron jalan" — re-deploy and recreate the credential, then confirm an `OK` log line.
