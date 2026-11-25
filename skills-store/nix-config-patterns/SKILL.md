---
name: nix-config-patterns
description: Coding patterns extracted from nix-config repository
version: 1.0.0
source: local-git-analysis
analyzed_commits: 70
---

# nix-config Patterns

## Commit Conventions

This project uses **informal, descriptive commits** (not conventional commits):

- Short imperative phrases: `add chrome`, `fix gtk bug`, `delete openclaw`
- Prefixed refactors: `refact home dir`, `refact tui tools path`
- Prefixed fixes: `fix fcitx5 bug in KDE`, `fix boot problem`
- Lock file updates: `flake.lock: Update`
- Feature additions: `add <thing>`, `add nix-flatpak`
- Config tweaks: `<component>: <what changed>` e.g. `fcitx5: set shift to noop`

**No conventional commit prefixes (feat:/fix:/chore:) are used in this repo.**

## Code Architecture

```
nix-config/
├── flake.nix              # Inputs, mkNixosSystem, all host definitions
├── vars/default.nix       # nixosHosts, hostnames, username
├── lib/                   # mylib helpers (scanPaths, relativeToRoot)
├── hosts/
│   ├── thinkpad/          # Per-host hardware-configuration.nix + host-user.nix
│   ├── legion/            # Per-host hardware-configuration.nix + host-user.nix
│   └── local.example/     # Template for local-only hosts (gitignored)
├── modules/
│   ├── base/              # Cross-platform NixOS modules (apps.nix, etc.)
│   ├── linux/             # Linux-only system modules (kde.nix, host-user.nix)
│   └── macos/             # macOS system modules
├── home/
│   ├── tui-base/          # Shared HM config (nvim, zsh, yazi, etc.)
│   ├── gui-base/          # Desktop HM config (yazi-clipboard, zsh-extra)
│   ├── linux/             # Linux-specific HM (fcitx5, kde, noctalia)
│   ├── macos/             # macOS-specific HM
│   └── remote/            # Headless server HM (minimal toolset)
├── config/                # Mutable configs symlinked via mkOutOfStoreSymlink
│   ├── niri/              # niri compositor (config.kdl, keybindings.kdl, etc.)
│   ├── nvim/              # Neovim lua configs
│   ├── noctalia/          # Noctalia bar settings.json
│   ├── rime/              # Rime IME default.custom.yaml
│   └── zsh/               # Zsh extra scripts (aliases, etc.)
├── pkgs/                  # Custom packages (e.g. fcitx5-vinput.nix)
└── Justfile               # Task runner for rebuild, update, gc
```

## Key Patterns

### scanPaths Auto-Import
`mylib.scanPaths` auto-imports all `.nix` files in a directory — no manual list needed:
```nix
imports = lib.flatten [
  (mylib.scanPaths ./programs)
];
```

### mkOutOfStoreSymlink for Mutable Configs
Configs that need runtime editing (niri, nvim, rime, noctalia) use symlinks:
```nix
xdg.configFile."niri".source =
  config.lib.file.mkOutOfStoreSymlink "${myvars.nixConfigPath}/config/niri";
```

### Per-Host Specialization
Common settings go in `modules/linux/host-user.nix`; host-specific overrides live in `hosts/<name>/host-user.nix`. When settings are shared between legion and thinkpad, move them up to the module level.

### Home Manager Layers
Home config is layered by capability scope:
1. `home/tui-base` — universal (all platforms, all contexts)
2. `home/gui-base` — GUI systems
3. `home/linux` or `home/macos` — platform-specific
4. `home/remote` — headless servers (minimal)

### Local Host Pattern
`hosts/local.example/` is a template for personal/local hosts. Real `hosts/local/` is gitignored. Copy and adapt when setting up a new machine locally.

## Workflows

### Apply NixOS Config Change
```bash
just switch           # Linux: sudo nixos-rebuild switch --flake .#nixos
just switch-test      # Test without committing to boot
```

### Apply Home Manager Only
```bash
just home-switch      # home-manager switch --flake .
```

### Update Flake Inputs
```bash
just up                        # Update all inputs + commit lock file
just update-input nixpkgs-unstable  # Update single input
```

### Remote Server Setup
```bash
just remote-init      # First-time: install HM + apply #remote config
just remote-switch    # After HM installed: update remote config
```

### Cleanup
```bash
just gc               # Delete generations older than 7d + collect garbage
just optimize         # nix-store --optimize
```

### Adding a New Program
1. Create `home/<layer>/programs/<name>.nix`
2. It's auto-imported by `scanPaths` — no manual import needed
3. If it needs a mutable config, add symlink via `mkOutOfStoreSymlink` pointing to `config/<name>/`

### Adding a New Host
1. Copy `hosts/local.example/` to `hosts/<name>/`
2. Add hardware-configuration.nix (generate with `nixos-generate-config`)
3. Register in `vars/default.nix` under `nixosHosts`
4. Add to `flake.nix` nixosConfigurations if needed

## Most Active Files (change hotspots)

| File | Commit Count | Notes |
|------|-------------|-------|
| `config/noctalia/settings.json` | 20 | Noctalia bar — frequent tweaking |
| `home/linux/programs/default.nix` | 18 | Linux program list |
| `flake.lock` | 17 | Regular dependency updates |
| `flake.nix` | 15 | Inputs + host definitions |
| `modules/linux/host-user.nix` | 13 | Shared Linux system config |
| `config/niri/windowrules.kdl` | 8 | Niri window rules |
| `home/linux/programs/fcitx5.nix` | 8 | Input method config |
| `config/niri/keybindings.kdl` | 7 | Niri keybindings |

## Testing / Validation

No automated tests. Validation workflow:
1. `just switch-test` — applies config without setting as default boot entry
2. Verify system behavior manually
3. `just switch` — commit to the change

## Notes

- `flake.lock: Update` commits are generated by `just up` (uses `--commit-lock-file`)
- `hosts/local/` and `hosts/legion/hardware-configuration.nix`, `hosts/thinkpad/hardware-configuration.nix` are gitignored (sensitive hardware info)
- Chinese commit messages appear occasionally — this is intentional
- Justfile uses Chinese comments for documentation
