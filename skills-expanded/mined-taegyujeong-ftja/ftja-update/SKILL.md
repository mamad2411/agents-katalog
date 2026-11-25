---
name: ftja-update
description: Update this FTJA folder to the latest published version (git pull, dependencies, restart the viewer) and tell the user what changed. Invoke when the user says "update FTJA", "get the latest version", or after /ftja-run or the viewer reported that an update is available.
---

# FTJA update

FTJA is installed by cloning its repository, so it only changes when the
user pulls. This skill does that pull safely. The user's own files
(`criteria.json`, `rubric.md`, `rubric-criteria.json`, `profile/`,
`seen.db`, digests, `.ftja-run/`) are ignored by git; an update never
touches them.

**On Windows**, read every `venv/bin/python` below as `venv\Scripts\python`
(and `venv/bin/pip` as `venv\Scripts\pip`), and run commands in PowerShell. The rules for each system (one shell, time limits, never cutting a command's output short) are in `.claude/skills/ftja-setup/windows.md` and `mac.md`: read the one for this system first.

## 1. Where things stand

```
venv/bin/python -m ftja.version check --force
```

Note the installed version it prints. If it says `up to date`, tell the
user and stop.

Do not update while a run is in progress: `venv/bin/python -m ftja.lock
check .ftja.lock` — if it prints `locked`, tell the user to update after
the run finishes, and stop.

## 2. Make sure the pull can't lose anything

Run `git status --short` and `git branch --show-current`.

- **Tracked files modified** (lines starting with ` M` or `M`): the user,
  or an agent on their behalf, changed FTJA's own code or skills. Stop and
  show them the list. Offer two ways forward and let them choose: keep the
  changes aside and update (`git stash`, pull, then `git stash pop` — and
  if that conflicts, show the conflict rather than resolving it by
  guessing), or leave everything as it is. Never discard their changes.
- **Not on the default branch**: tell the user which branch they are on and
  ask before doing anything.
- Untracked files (`??`) are fine; leave them alone.

## 3. Pull

```
git pull --ff-only
```

`--ff-only` refuses rather than creating a merge when the local history
has diverged. If it refuses, report git's message and stop; do not rebase,
reset or force anything.

## 4. Dependencies and the viewer

```
venv/bin/pip install -q -r requirements.txt
```

The viewer keeps the old code in memory until it restarts. If something is
listening on port 8765 (`lsof -tiTCP:8765 -sTCP:LISTEN`; Windows:
`(Get-NetTCPConnection -LocalPort 8765 -State Listen).OwningProcess`), stop that process
and start it again from this folder (`venv/bin/python -m ftja.server`, in
the background), then check `http://127.0.0.1:8765/` answers.

## 5. Tell the user what changed

```
venv/bin/python -m ftja.version changes --since <the version from step 1>
```

Relay it in the user's language, leading with each version's "What changes
for you after updating" part — those are the things they will notice or
need to do. Finish with the version they are now on.
