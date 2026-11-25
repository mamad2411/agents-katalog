set shell := ["zsh", "-uc"]

# List all the just commands
default:
  @just --list

# ─────────────────────────────────────────────────────────────────────────────
# 依赖管理
# ─────────────────────────────────────────────────────────────────────────────

# 更新所有 flake 依赖
[group('flake')]
up:
  nix flake update --commit-lock-file

# 更新特定 flake 输入
[group('flake')]
update-input INPUT:
  nix flake update {{INPUT}}

# 查看 flake 依赖树
[group('flake')]
deps:
  nix flake metadata --json | jq '.locks.nodes | keys'

# ─────────────────────────────────────────────────────────────────────────────
# NixOS 构建和切换
# ─────────────────────────────────────────────────────────────────────────────

# 统一切换入口：NixOS 使用系统配置，普通 Linux 使用当前用户的 headless Home Manager
[group('rebuild')]
[linux]
switch:
  @if test -e /etc/NIXOS; then \
    test -d hosts/local || { echo "错误：NixOS 需要 hosts/local/；请从 hosts/local.example 创建并配置。" >&2; exit 1; }; \
    sudo env NIX_CONFIG_ROOT="$PWD" nixos-rebuild switch --flake path:.#nixos --impure --show-trace --print-build-logs; \
  else \
    case "$(uname -m)" in \
      x86_64) target=headless ;; \
      aarch64|arm64) target=headless-aarch64 ;; \
      *) echo "错误：不支持的架构 $(uname -m)" >&2; exit 1 ;; \
    esac; \
    just headless-preflight "$target"; \
    if command -v home-manager >/dev/null 2>&1; then \
      home-manager switch --flake "path:.#$target" --show-trace --impure -b backup; \
    else \
      nix run home-manager/master -- switch --flake "path:.#$target" --show-trace --impure -b backup; \
    fi; \
  fi

# 构建并切换 NixOS 配置 (使用测试通道)
[group('rebuild')]
[linux]
switch-test:
  test -d hosts/local || (echo "hosts/local/ 不存在！请执行: cp -r hosts/local.example hosts/local" && exit 1)
  sudo env NIX_CONFIG_ROOT="$PWD" nixos-rebuild test --flake path:.#nixos --impure --print-build-logs

[group('rebuild')]
[linux]
switch-proxy:
  test -d hosts/local || (echo "hosts/local/ 不存在！请执行: cp -r hosts/local.example hosts/local" && exit 1)
  sudo env NIX_CONFIG_ROOT="$PWD" ALL_PROXY=http://127.0.0.1:7897 nixos-rebuild switch --flake path:.#nixos --impure --show-trace --print-build-logs

[group('rebuild')]
[linux]
switch-boot:
  test -d hosts/local || (echo "hosts/local/ 不存在！请执行: cp -r hosts/local.example hosts/local" && exit 1)
  sudo env NIX_CONFIG_ROOT="$PWD" nixos-rebuild boot --flake path:.#nixos --impure --print-build-logs

# 查看 NixOS generations
[group('rebuild')]
[linux]
generations:
  sudo nix-env -p /nix/var/nix/profiles/system --list-generations

# ─────────────────────────────────────────────────────────────────────────────
# macOS 构建和切换
# ─────────────────────────────────────────────────────────────────────────────

# 构建并切换 macOS 配置
[group('rebuild')]
[macos]
switch:
  sudo darwin-rebuild switch --flake path:. --show-trace

# 查看 macOS generations
[group('rebuild')]
[macos]
generations:
  nix-env -p /nix/var/nix/profiles/system --list-generations

[group('rebuild')]
[macos]
switch-proxy:
  sudo ALL_PROXY=http://127.0.0.1:7897 darwin-rebuild switch --flake path:. --show-trace

# 显式更新 Homebrew；不再绑定到 darwin-rebuild 激活过程
[group('rebuild')]
[macos]
brew-maintain:
  brew update
  brew upgrade
  brew cleanup

# 清理旧的 macOS generations
[group('rebuild')]
[macos]
gc:
  sudo nix-collect-garbage --delete-older-than 7d

# ─────────────────────────────────────────────────────────────────────────────
# 系统清理和维护
# ─────────────────────────────────────────────────────────────────────────────

# 清理旧的 NixOS generations
[group('clean')]
[linux]
gc:
  sudo nix-collect-garbage --delete-older-than 7d

# 查看存储使用情况
[group('clean')]
[linux]
[macos]
storage:
  nix-store --gc --print-dead
  nix-store --gc --print-live

# 优化存储
[group('clean')]
[linux]
[macos]
optimize:
  nix-store --optimize

# 运行 pre-commit hooks（格式化 + 检查全部文件）
[group('clean')]
[linux]
[macos]
lint:
  nix develop -c pre-commit run --all-files

# 评估所有平台；只构建当前平台的完整配置，避免 macOS 构建 Linux derivation
[group('clean')]
[linux]
[macos]
check:
  nix flake check --all-systems --no-build --show-trace --impure
  @case "$(uname -s)-$(uname -m)" in \
    Darwin-arm64) attrs="pre-commit-check darwin-system" ;; \
    Linux-x86_64) attrs="pre-commit-check headless-activation nixos-system" ;; \
    Linux-aarch64|Linux-arm64) attrs="pre-commit-check headless-activation" ;; \
    *) echo "错误：不支持的平台 $(uname -s)-$(uname -m)" >&2; exit 1 ;; \
  esac; \
  for attr in ${=attrs}; do nix build --impure ".#checks.$(nix eval --impure --raw --expr builtins.currentSystem).$attr" --show-trace; done

# 安装 git pre-commit hooks（进入 devShell 时也会自动安装）
[group('clean')]
[linux]
[macos]
hooks-install:
  nix develop -c pre-commit install

# ─────────────────────────────────────────────────────────────────────────────
# Home Manager
# ─────────────────────────────────────────────────────────────────────────────

# 兼容入口：系统集成 HM 与 standalone Linux 均转发到统一 switch
[group('home')]
[linux]
[macos]
home-switch:
  just switch

# 查看 Home Manager generations
[group('home')]
[linux]
[macos]
home-generations:
  home-manager generations

# 清理旧的 Home Manager generations
[group('home')]
[linux]
[macos]
home-clean:
  home-manager remove-generations old

# ─────────────────────────────────────────────────────────────────────────────
# 无 sudo、无图形桌面的 standalone Home Manager 环境
# ─────────────────────────────────────────────────────────────────────────────

# 部署前检查：拒绝把尚未解锁的 git-crypt 文件交给 Nix，并实例化完整 activation derivation
[group('remote')]
headless-preflight TARGET="headless":
  @magic="$(od -An -tx1 -N10 vars/private.nix | tr -d ' \n')"; \
    test "$magic" != "00474954435259505400" || \
    { echo "错误：vars/private.nix 尚未解锁，请先按 docs/new-machine-setup.md 第 5 步执行 git-crypt unlock。" >&2; exit 1; }
  nix eval path:.#homeConfigurations.{{TARGET}}.activationPackage.drvPath --raw --impure >/dev/null

# 首次部署：通过 nix run 安装 home-manager 并激活配置（x86_64）
[group('remote')]
remote-init:
  just headless-preflight remote
  nix run home-manager/master -- switch --flake path:.#remote --show-trace --impure -b backup

# 首次部署：aarch64 服务器（AWS Graviton、树莓派等）
[group('remote')]
remote-init-arm:
  just headless-preflight remote-aarch64
  nix run home-manager/master -- switch --flake path:.#remote-aarch64 --show-trace --impure -b backup

# 更新远程配置（已安装 home-manager 后使用）
[group('remote')]
remote-switch:
  just headless-preflight remote
  home-manager switch --flake path:.#remote --show-trace --impure -b backup

# 更新远程配置（aarch64）
[group('remote')]
remote-switch-arm:
  just headless-preflight remote-aarch64
  home-manager switch --flake path:.#remote-aarch64 --show-trace --impure -b backup

# 首次部署 headless x86_64 环境（推荐名称）
[group('headless')]
headless-init:
  just headless-preflight headless
  nix run home-manager/master -- switch --flake path:.#headless --show-trace --impure -b backup

# 更新 headless x86_64 环境（推荐名称）
[group('headless')]
headless-switch:
  just headless-preflight headless
  home-manager switch --flake path:.#headless --show-trace --impure -b backup

# 首次部署 / 更新 headless aarch64 环境
[group('headless')]
headless-init-arm:
  just headless-preflight headless-aarch64
  nix run home-manager/master -- switch --flake path:.#headless-aarch64 --show-trace --impure -b backup

[group('headless')]
headless-switch-arm:
  just headless-preflight headless-aarch64
  home-manager switch --flake path:.#headless-aarch64 --show-trace --impure -b backup

# 旧名称兼容入口
[group('remote')]
remote-preflight TARGET="remote":
  just headless-preflight {{TARGET}}

# 查看远程 home-manager generations
[group('remote')]
remote-generations:
  home-manager generations

# 清理远程旧 generations 并回收空间
[group('remote')]
remote-clean:
  home-manager remove-generations old && nix-collect-garbage --delete-older-than 7d

# ─────────────────────────────────────────────────────────────────────────────
# 展示一个 nix flake 所提供的东西
[linux]
[macos]
show target:
  nix flake show {{target}}
