---
name: git-global-hook-bootstrap
description: One-time per-machine setup — symlink ~/.git-hooks/ to
    repo dotfiles/git-hooks/, set git --global core.hooksPath,
    auto-bootstrap repo hooks via post-checkout discovery.
category: Git-Infrastructure
---

# Git Global Hook Bootstrap — General Infrastructure

> **Skill ID:** `git-global-hook-bootstrap`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

This skill provides the **machine-level plumbing** for git hook
bootstrapping. On any developer machine, running the setup script once
creates a symlink from `~/.git-hooks/` to a repository's
`dotfiles/git-hooks/` directory and registers it as Git's global
`core.hooksPath`.

The global directory contains exactly **one** hook: `post-checkout`.
This hook fires on every `git checkout` and `git clone` (implicit
checkout). Its job is to discover whether the checked-out repository
has a `scripts/setup-hooks.bash` file. If it does, the hook execs it
— that script handles all repo-level hook configuration. If the file
does not exist, the hook exits silently (the repo simply has no hook
setup, which is fine).

This means **any repository** can opt into automatic hook bootstrapping
by simply creating a `scripts/setup-hooks.bash` file. No global config
changes, no per-repo manual setup.

## Composition Rationale

This skill is a **standalone general infrastructure** skill. It owns
exactly one concern: "place a symlink + one global hook that discovers
and runs per-repo bootstrap scripts." It knows nothing about what those
scripts do, which hooks to install, or what checks to run.

Composers integrate this into larger workflows:

| Composer | Composition Mechanism |
| --- | --- |
| [`git-operation-blocking-hooks`](../git-operation-blocking-hooks/SKILL.md) | Composes this skill's global bootstrap + the repo hook chain + alias preflight into a complete blocking gate. The `post-checkout` hook triggers `setup-repo-hooks.bash` (from `git-repo-hook-chain`) on every checkout. |

## Environment

| Requirement | Minimum |
| --- | --- |
| Shell | Bash 4+ (hooks execute in shell context; no pwsh dependency) |
| Git | 2.x+ |
| OS | Linux, macOS, Windows (Git Bash / WSL) |

**Installation dependencies:** None. The scripts use only `ln`, `git`,
and standard POSIX file tests.

## Operational Logic

### 3.1 — Machine Setup (one-time)

Run `scripts/setup-global-hooks.bash` once per developer machine:

```bash
bash scripts/setup-global-hooks.bash "$PWD/dotfiles/git-hooks"
```

This does two things:

1. **`ln -sf <src> ~/.git-hooks`** — creates or replaces a symlink from
   the home directory to the repo's hook directory. Idempotent: `-f`
   overwrites any existing symlink. If `~/.git-hooks` is a real directory
   (not a symlink), `-f` replaces it; verify existing content first.

2. **`git config --global core.hooksPath ~/.git-hooks`** — tells Git
   to look for hooks in `~/.git-hooks/` for every repository on this
   machine. Idempotent: setting the same value again is harmless.

### 3.2 — Where the Hook Files Live

```text
dotfiles/git-hooks/           ← symlink target (in the repo)
  └── post-checkout            ← The single global hook
```

Only `post-checkout` lives here. No `pre-commit`, `pre-push`, etc. —
those are repo-level hooks managed by `git-repo-hook-chain`.

### 3.3 — What post-checkout Does

On every checkout (including `git clone`'s implicit initial checkout):

```text
1. REPO_ROOT=$(git rev-parse --show-toplevel)
2. If REPO_ROOT/scripts/setup-hooks.bash exists AND is executable:
      exec bash REPO_ROOT/scripts/setup-hooks.bash
   Else:
      exit 0   ← silently; not every repo has hooks
```

The hook runs in the context of the checked-out repository. It does not
modify global state. It does not install hooks itself — it delegates to
the repo's own setup script. This is the key design property: **the repo
contains its own hook configuration; the global hook just activates it.**

### 3.4 — How Any Repository Self-Wires

To make a repository participate in automatic hook bootstrapping, place
an executable `scripts/setup-hooks.bash` at its root. The content is
repo-specific — typically it configures `core.hooksPath`, registers
aliases, and seeds baseline snapshots.

Example minimal `scripts/setup-hooks.bash` (see also
`git-repo-hook-chain` and `git-alias-preflight`):

```bash
#!/bin/bash
set -euo pipefail
git config core.hooksPath scripts/githooks
git config alias.status "!bash scripts/githooks/lib.bash status"
```

That is the entire contract — create that one file and the global hook
will find and execute it on every checkout.

### 3.5 — Cross-Machine Portability

When moving to a new machine:

1. Clone the repository that contains `dotfiles/git-hooks/` (or any
   repo with that directory structure).
2. Run `scripts/setup-global-hooks.bash` with the correct path.
3. All subsequent checkouts of any hook-aware repo will be bootstrapped.

No per-machine customization is needed beyond the initial setup.

### 3.6 — Recovery / Tear-Down

To remove the global hook setup:

```bash
rm ~/.git-hooks
git config --global --unset core.hooksPath
```

To verify current state:

```bash
readlink ~/.git-hooks        # should show the symlink target
git config --global core.hooksPath   # should show ~/.git-hooks
```

## Script Reference

| Script | Purpose | Invocation |
| --- | --- | --- |
| [`scripts/setup-global-hooks.bash`](scripts/setup-global-hooks.bash) | One-time machine setup | `bash scripts/setup-global-hooks.bash <path/to/dotfiles/git-hooks>` |
| [`scripts/dotfiles/git-hooks/post-checkout`](scripts/dotfiles/git-hooks/post-checkout) | Global hook — repo discovery | Placed at `~/.git-hooks/post-checkout` by the symlink |

## Verification

### Confirm the symlink and config

```bash
ls -la ~/.git-hooks          # should show symlink → repo path
git config --global core.hooksPath   # should show ~/.git-hooks
```

### Confirm post-checkout fires correctly

```bash
# In a repo WITH scripts/setup-hooks.bash:
bash scripts/dotfiles/git-hooks/post-checkout
# Should exit 0 and run setup-hooks.bash

# In a repo WITHOUT:
cd /tmp && git init _test && cd _test
bash <original-repo>/dotfiles/git-hooks/post-checkout
# Should exit 0 silently
rm -rf /tmp/_test
```

### Confirm self-wire contract

Create a minimal `scripts/setup-hooks.bash` that creates a marker file,
run `bash scripts/dotfiles/git-hooks/post-checkout`, verify the marker
was created.
