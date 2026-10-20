---
name: dependency-check-install-precondition-gate
description: Gate a multi-step workflow behind a scripted dependency probe that emits machine-readable `INSTALL_REQUIRED:<dep>` / `INSTALL_OPTIONAL:<dep>` lines, paired with an install script that detects OS/package manager and prefers user-local (no-sudo) installs, falling back to sudo-or-manual-instructions on exit code 2.
category: automation
version: 1.0.0
tags: [automation, shell, dependency-check, bootstrap, idempotent, cross-platform]
source_type: extracted-from-git
source_url: https://github.com/SimoneAvogadro/android-reverse-engineering-skill.git
source_ref: master
source_commit: ddeb9bc33272db1e34107fd286098bb1e9896e51
source_project: android-reverse-engineering-skill
source_path: plugins/android-reverse-engineering/skills/android-reverse-engineering/SKILL.md
imported_at: 2026-04-18T03:36:29Z
confidence: medium
version_origin: extracted
---

# Dependency-Check / Install Precondition Gate

A two-script pattern for ensuring a workflow's external tool dependencies are present before any real work starts, without hard-failing the user when optional tools are missing or sudo is unavailable.

## When to use

- A workflow depends on CLI tools the user may not have installed (decompilers, language runtimes, test runners).
- The workflow runs across OSes (Linux, macOS, Windows/WSL) with different package managers.
- You want an agent or human operator to automatically install missing required deps, but only *ask* about optional ones.

## The contract

### `check-deps.sh`

Emits one line per dependency in machine-readable form, plus a human-readable summary. Exit code encodes blocking status.

```
OK:java                          # installed and acceptable
INSTALL_REQUIRED:jadx            # must be installed to proceed
INSTALL_OPTIONAL:vineflower      # recommended, not blocking
INSTALL_OPTIONAL:dex2jar
```

- Exit `0` — all required deps present (optional may be missing).
- Exit `1` — at least one required dep missing.

The caller parses `INSTALL_REQUIRED:` and `INSTALL_OPTIONAL:` lines with simple grep and acts accordingly.

### `install-dep.sh <dep>`

Accepts a single dep name and installs it, using OS auto-detection:

1. **No-sudo path preferred** — download to `~/.local/share/<dep>/`, symlink binaries in `~/.local/bin/`. This works for most users without elevation.
2. **System package manager fallback** — apt / dnf / pacman / brew as appropriate, with sudo where required.
3. **Declined-sudo path** — exit code `2`, print the exact manual command for the user. Do **not** proceed silently.

Exit codes:
- `0` — installed successfully.
- `1` — unknown dep or hard failure.
- `2` — sudo needed and unavailable/declined; manual instructions printed to stdout.

## Caller loop (agent or shell)

```bash
bash check-deps.sh > deps.out || true
grep '^INSTALL_REQUIRED:' deps.out | cut -d: -f2 | while read dep; do
    bash install-dep.sh "$dep" || {
        rc=$?
        if [ $rc -eq 2 ]; then
            echo "Manual install required for $dep — see instructions above." >&2
            exit 2
        fi
        exit $rc
    }
done

# Re-run to confirm
bash check-deps.sh || exit 1
```

For **optional** deps, ask the user rather than auto-install:

```bash
grep '^INSTALL_OPTIONAL:' deps.out | cut -d: -f2 | while read dep; do
    read -p "Install optional dep $dep? [y/N] " ans
    [[ "$ans" == "y" ]] && bash install-dep.sh "$dep"
done
```

## Why machine-readable lines + exit codes

Parsing the output directly means **no prompting inside the check script** — it's a pure probe. The caller decides interaction style (auto, interactive, or non-interactive CI). Mixing user prompts into the probe would break non-interactive uses and complicate agent-driven installs.

## Why `~/.local/` first

User-local installs:
- Don't need sudo (fewer permission prompts, works in locked-down corp environments).
- Don't pollute system package state (no risk of conflicting with OS-managed versions).
- Are trivially reproducible by the same user on the same machine.

Fall back to the system package manager only when there's no portable tarball/zip for the tool (or when the user explicitly prefers system packages).

## Invariants

- **`check-deps.sh` never modifies state.** It only probes.
- **`install-dep.sh` is idempotent per dep.** Re-running on an already-installed dep exits `0` without reinstalling.
- **Exit code 2 always prints manual instructions.** Never silent — the caller or user must see them.
- **Re-run `check-deps.sh` after every install batch.** Confirms success before proceeding to the gated workflow.
