---
name: termux-setup
description: Sets up and troubleshoots Termux on Android for development. Use whenever the user works in Termux, mentions pkg, termux-setup-storage, ~/storage, git on a phone, "dubious ownership", GitHub push from a phone, SSH keys or tokens on Android, or wants scripts that run in Termux, even if they only say "run this on my phone". Covers package setup, shared storage pitfalls, git authentication, wake locks and scheduled jobs.
---

# termux-setup

Practical setup and fixes for developing in Termux. Most problems come from three things: missing packages, shared storage behaving unlike a normal Linux disk, and git authentication.

```
termux-setup/
├── SKILL.md
├── scripts/
│   ├── termux_bootstrap.sh   install packages, storage access, git identity (supports --dry-run)
│   └── git_doctor.sh         diagnose a repo: ownership, location, remote, credentials
└── references/
    └── troubleshooting.md    error messages and exact fixes
```

## When to use

- First time setup of Termux for coding
- A git command fails in a repo under `~/storage`
- Push to GitHub fails or asks for a password
- A script written for Linux must run on the phone
- A task must keep running with the screen off

## Golden rules

1. Work inside `$HOME` (`/data/data/com.termux/files/home`), not inside `~/storage/...`. Shared storage has different ownership and no real permission bits, so git and chmod misbehave there.
2. Use `~/storage/downloads` only to exchange files with other apps (copy in, copy out).
3. Use `https://` clone URLs with a Personal Access Token, or an SSH key. A GitHub account password does not work.
4. Write scripts with the shebang `#!/data/data/com.termux/files/usr/bin/bash` or `#!/usr/bin/env bash`. Never hardcode `/bin/bash` or `/usr/bin`.
5. Use `pkg`, not `apt`, and never `sudo` (there is no root).

## Quick start

```bash
bash scripts/termux_bootstrap.sh            # installs git, openssh, python, zip, unzip, curl
bash scripts/termux_bootstrap.sh --dry-run  # only print what would happen
bash scripts/git_doctor.sh ~/skills         # diagnose a repo
```

## Git fixes

### "detected dubious ownership"

The repo is on shared storage or was extracted by another user. Best fix: move it into `$HOME`.

```bash
cp -r ~/storage/documents/Codes/myrepo ~/myrepo
cd ~/myrepo
git config --global --add safe.directory "$PWD"
```

Quick fix (trusts every directory, use only on a personal phone):

```bash
git config --global --add safe.directory '*'
```

### Push asks for a password

GitHub removed password login for git. Create a token (GitHub: Settings, Developer settings, Personal access tokens) with `repo` scope, then:

```bash
git config --global credential.helper store
git push origin HEAD      # username = GitHub user, password = the token
```

The token is saved in plain text in `~/.git-credentials`. Protect the phone with a lock screen.

### SSH instead of tokens

```bash
ssh-keygen -t ed25519 -C "phone"
cat ~/.ssh/id_ed25519.pub        # add this to GitHub: Settings, SSH keys
git remote set-url origin git@github.com:USER/REPO.git
ssh -T git@github.com
```

## Storage

```bash
termux-setup-storage            # once, then tap Allow
ls ~/storage                    # downloads, documents, shared, dcim ...
cp file.zip ~/storage/downloads/
```

If `~/storage` is missing after allowing, run `termux-setup-storage` again and restart Termux.

## Long running work

```bash
termux-wake-lock                # keep CPU awake; run termux-wake-unlock when done
pkg install termux-services     # service manager (sv-enable, sv up)
pkg install cronie              # crond for scheduled tasks, then: crontab -e
```

Also disable battery optimization for Termux in Android settings or the OS will kill background jobs.

## Writing portable scripts

- Check the environment: `[ -n "${PREFIX:-}" ] && [[ "$PREFIX" == *com.termux* ]]`
- Prefer `set -euo pipefail` and quote every variable
- Offer `--dry-run` for anything that deletes or pushes
- Avoid `systemd`, `apt`, `sudo`, `/tmp` assumptions (use `$TMPDIR`)

More error messages and fixes: `references/troubleshooting.md`.

## What to report back

State the exact commands run, where the repo lives (must be under `$HOME`), whether auth is token or SSH, and what to do if the step fails.

## Related skills

- `systematic-debugging`: diagnose failures with evidence
- `secrets-hygiene`: keep tokens out of repos and shell history
- `commitsmith`: commit messages for changes made on the phone
