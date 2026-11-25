---
name: setting-up-dev-machine
description: Bootstraps a fresh Ubuntu machine into the managed dev-machine pattern (etckeeper, server-config repo with host package manifest, chezmoi dotfile loaders, Devbox Global, direnv). Use when setting up a new dev server/VM from scratch, or when asked to "set up this machine", "bootstrap the dev box", or install the baseline tooling on a clean install. For machines with existing state, use migrating-dev-machine instead.
---

# Setting up a dev machine

Layer model and conventions: see the managing-dev-machine skill.

Order matters: etckeeper is installed **before** other packages so the
`/etc` baseline and every subsequent package's config changes are recorded
(`scripts/apply.sh` handles this).

## Steps

```
Setup progress:
- [ ] 1. Snapshot (if VM) and record baseline
- [ ] 2. Run scripts/apply.sh
- [ ] 3. Wire chezmoi ownership of the loader blocks
- [ ] 4. Host extras (Docker etc.) via host scripts
- [ ] 5. Devbox Global profile
- [ ] 6. Verify with a fresh login shell
```

**1. Baseline.** Take a provider snapshot if possible. Record
`cat /etc/os-release; id; df -hT` into `$SERVER_CONFIG_DIR/inventories/<host>-baseline/`.

**2. Apply.** Run `scripts/apply.sh`. It is idempotent, bootstraps AND
converges: etckeeper first; creates and git-inits `$SERVER_CONFIG_DIR`
(default `~/server-config`); snapshots the image's `apt-mark showmanual`
as `host/apt-baseline.txt`; seeds `host/apt-packages.txt` and installs
whatever that manifest lists; runs any `host/scripts.d/*.sh`; installs
chezmoi + devbox to `~/.local/bin`; creates
`~/.config/shell/{bashrc.d,profile.d}/`; inserts the marker-guarded loader
blocks into `.bashrc`/`.profile`; writes the devbox-global and direnv-hook
snippets and the `use_personal_devbox` direnv helper; installs itself as
`$SERVER_CONFIG_DIR/host/apply.sh` — run that copy from then on. Adding a
host package later = edit the manifest, rerun apply, commit.

**3. Chezmoi ownership.** Copy `templates/modify_dot_bashrc` and
`templates/modify_dot_profile` into the chezmoi source dir
(`$SERVER_CONFIG_DIR/dotfiles/`), then `chezmoi add` every file under
`~/.config/shell/` and `~/.config/direnv/lib/`. From then on the loader
blocks and snippets are chezmoi-managed; installer edits show up in
`chezmoi diff` (handle those with the normalizing-dotfiles skill).

**4. Host extras.** Anything needing an apt repo/keyring or a checksummed
binary download gets an idempotent script in
`$SERVER_CONFIG_DIR/host/scripts.d/` (apply.sh runs them in order).
`templates/install-docker.sh` is the model. Keep the host layer small:
Docker, ssh, tmux, build prerequisites — not language runtimes.

**5. Devbox Global.** `devbox global add ripgrep jq fd fzf bat gh just
shellcheck` (adjust to taste), then `devbox global install` — from a
not-yet-activated shell, `add` records packages without materializing the
nix profile, so `install` ensures the binaries actually exist. Symlink or
copy the resulting global `devbox.json` into
`$SERVER_CONFIG_DIR/devbox-global/` and commit.

**6. Verify.** Open a **new login shell** and check:
`command -v devbox direnv chezmoi rg` all resolve; `chezmoi diff` is clean;
`sudo etckeeper vcs status` is clean; rerunning `host/apply.sh` reports
"No changes" (idempotence is the test that the setup is reproducible).

Commit each step to `$SERVER_CONFIG_DIR` as you go.

## Adding language runtimes

Do not install nvm/rustup here by default. Install them on first need via
the installing-dev-tools skill so the integration snippet and provenance
commit happen together.

## Why a shell script and manifest, not Ansible

For a single machine the declarative **manifest is the asset**, not the
tool: `apt install` is already idempotent, and drift detection is a `comm`
against `apt-mark showmanual` (built into apply.sh and the audit).
Reintroduce Ansible (or similar) if any of these become true: a second
machine to keep in sync, templated system config files, or more than a
handful of managed services — at that point, translate `apt-packages.txt`
and `scripts.d/` into roles and keep the same layer boundaries.
