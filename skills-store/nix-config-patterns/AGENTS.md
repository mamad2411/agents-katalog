# AGENTS.md

Cross-platform Nix Flake config: NixOS (x86_64-linux), nix-darwin (aarch64-darwin), and standalone home-manager for remote Linux servers.

## Commands (full list in Justfile)

```bash
just switch                # unified: NixOS/darwin rebuild, ordinary Linux headless HM
just switch-test           # apply config without changing boot entry
just switch-boot           # apply on next boot only
just up                    # nix flake update --commit-lock-file (commits "flake.lock: Update")
just update-input <name>   # update a single input
just home-switch           # home-manager switch --flake path:. --show-trace
just remote-init           # first-time server deploy (x86_64); remote-init-arm for aarch64
just remote-switch         # reapply server config after HM installed
just headless-switch       # preferred name: no-sudo, non-graphical standalone HM
just gc / just optimize    # cleanup
just lint                  # run pre-commit hooks on all files
just check                 # nix flake check (all configs + pre-commit checks)
just hooks-install         # install git pre-commit hooks
```

Same `just switch` on macOS runs `darwin-rebuild switch --flake path:.`; recipes are gated by `[linux]`/`[macos]` attributes.

## Must know

- **`just switch` 是统一入口。** NixOS/macOS 走系统 rebuild；普通 Linux 自动选择当前架构的 headless standalone Home Manager。Headless 在 `home/home-setting.nix` 中通过 `USER`/`HOME` 获取当前身份，因此必须以目标用户运行并保留 `--impure`；纯求值时为空则回退到仓库默认用户。
- **`hosts/local/` is gitignored and mandatory.** To set up a machine: `cp -r hosts/local.example hosts/local`, then edit `host-user.nix` (hostname, GRUB dual-boot UUIDs, resume device). `nixosConfigurations.nixos` is only defined when this dir exists (so `nix flake check` passes on non-Linux machines); the Justfile `switch*` recipes check for it and print a friendly error. This is where the NixOS hostname comes from — it is not set anywhere in the flake.
- **`config/` dirs are symlinked at build time** with `config.lib.file.mkOutOfStoreSymlink` from `${HOME}/nix-config/config` (hardcoded in `home/programs/core-tools/default.nix`, `home/programs/linux-only/DE/default.nix`, `home/home-setting.nix`, fcitx5). The repo must be checked out at `~/nix-config` on every target machine or those symlinks break.
- **`mylib.scanPaths` auto-imports** every `.nix` file and subdirectory of a dir, excluding `default.nix` (see `lib/default.nix`). Adding `home/programs/<layer>/<name>.nix` or a module file picks it up automatically; import order is alphabetical.
- **`specialArgs`** = `{ inputs, myvars, mylib }` is injected into every module. Prefer `myvars` (username `loyage`, keys, hostnames) over hardcoded values. `vars/` is split: `vars/public.nix`（用户名/公钥等公开数据）+ `vars/private.nix`（含 ssh 公网 IP，**git-crypt 加密**，克隆后需 `git-crypt unlock` 才能 eval）。

## Structure

- `modules/base` — cross-platform system modules (nix, agenix secrets, shell-tools)
- `modules/linux`, `modules/macos` — platform system config; `modules/optional` — desktop/dev opt-ins
- `home/programs/core-tools` — shared HM layer (imported by nixos/mac/remote entries)
- `home/programs/core-tools/gui` — desktop-only HM layer; the flake injects global `hostProfile.graphical`; headless configs set it to `false`, excluding this subtree plus GUI config links/Orca
- `home/programs/linux-only` — NixOS-only HM (DE/niri/noctalia, fcitx5, etc.), subdirs scanPath'd too
- `home/{nixos,mac,remote-server}.nix` — per-platform HM entrypoints
- `hosts/local{,example}/`, `hosts/remote/` — machine-specific overrides
- `secrets/` — agenix encrypted `.age` files; public keys in `vars/public.nix`. `secrets/secrets.nix` is pure (imports `../vars` directly, no `<nixpkgs>` channel), so `agenix -r` works without a nixpkgs channel. `secrets/git-crypt-key.age` is the agenix-encrypted git-crypt key for unlocking `vars/private.nix`.
- `git-hooks.nix` — pre-commit hooks config (nixfmt-rfc-style, deadnix, trim-trailing-whitespace, end-of-file-fixer)

## Pre-commit hooks

- Hooks defined in `git-hooks.nix`, exposed via `checks.<system>.pre-commit-check` and `devShells.<system>.default`.
- `just lint` runs all hooks on all files (`nix develop -c pre-commit run --all-files`).
- `just check` runs `nix flake check` (evaluates all configs + builds/runs the pre-commit check). `nixosConfigurations` is only defined when `hosts/local/` exists, so `just check` passes on both macOS and NixOS.
- `just hooks-install` installs the git hook (also auto-installed when entering `nix develop`).

## Gotchas

- **部署必须使用 `path:.`，新文件在正式部署前仍必须 `git add`。** 普通的 Git flake source（`.#...`）会从 Git 对象取得 git-crypt 密文；`path:.#...` 才读取解锁后的工作区，也可能让未跟踪文件在本机参与构建。新模块即使本机可见也必须提交，否则其他机器拉取后会缺文件。`hosts/local/` 是有意 gitignore 的例外。
- **不要把高敏感明文放进 `vars/private.nix`。** `path:.` 会把解锁后的源码复制进通常可被本机其他用户读取的 `/nix/store`。公网 IP、主机名等低敏感结构化配置可使用 git-crypt；API key、token、密码和私钥必须使用 agenix。
- No automated tests. Validation flow: `just switch-test`, verify manually, then `just switch`.
- `flake.nix` overlays pin custom `qq` / `wechat` builds with exact hashes — update the hash when bumping versions.
- Headless standalone Home Manager derives `home.username`/`home.homeDirectory` from `USER`/`HOME`; run `just switch` as the target user. No server-specific username is committed.
- Commit messages are short and descriptive; recent history uses `feat/fix(<scope>)` prefixes, lockfile bumps read `flake.lock: Update` (from `just up`), and occasional Chinese messages are intentional.
