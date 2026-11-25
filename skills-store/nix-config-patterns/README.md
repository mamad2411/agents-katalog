# nix-config

基于 Nix Flake 的跨平台配置管理，支持 NixOS、macOS (nix-darwin) 和远程 Linux 服务器 (home-manager standalone)。

> 📖 相关文档：
> - [新机器部署指南（AI Agent 可执行）](docs/new-machine-setup.md) — 新机器完整上线流程（含 git-crypt / agenix）
> - [配置维护与安全注意事项](docs/maintenance.md) — 检查、部署、SSH、Homebrew 与 CI 注意事项

## 支持的平台

| 配置 | 平台 | Flake 输出 |
|------|------|------------|
| NixOS 本机 | NixOS x86_64 | `nixosConfigurations.nixos` |
| MacBook Air | macOS aarch64 | `darwinConfigurations.LoyagedeMacBook-Air` |
| Headless Linux | Linux x86_64 | `homeConfigurations.headless` |
| Headless Linux (ARM) | Linux aarch64 | `homeConfigurations.headless-aarch64` |

`remote` / `remote-aarch64` 是兼容别名。

---

## 仓库路径约定

仓库默认位于 `$HOME/nix-config`。Home Manager 的 out-of-store 配置链接统一从
`vars/public.nix` 的 `repositoryDirectory` 推导；flake 求值时可通过
`NIX_CONFIG_ROOT=/绝对路径` 覆盖。NixOS 的 gitignored `hosts/local/` 也从该根目录读取，
因此本地部署需使用 `path:.` 和 `--impure`。

## 本地机器

### NixOS

```bash
sudo nixos-rebuild switch --flake path:.
# 或
just switch
```

### macOS

```bash
sudo darwin-rebuild switch --flake path:.
# 或
just switch
```

---

## 远程服务器（Ubuntu / Debian）

在远程服务器上通过 home-manager standalone 快速部署开发环境，包含：

- **Shell**：zsh + oh-my-zsh + oh-my-posh
- **编辑器**：neovim（使用 `~/nix-config/config/nvim` 配置）
- **文件管理**：yazi（catppuccin-mocha 主题）
- **版本控制**：git + lazygit
- **终端复用**：zellij
- **常用工具**：bat、btop、fzf、ripgrep、zoxide、eza、dust、duf 等

### 首次部署（有 Sudo 权限）

```bash
# 1. 安装 Nix
sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon
# 重新加载 shell 或新开终端

# 2. 克隆配置仓库
git clone <your-repo-url> ~/nix-config

# 3. 激活 home-manager 配置
#    x86_64 服务器（最常见）
nix run home-manager/master -- switch --flake ~/nix-config#remote
#    aarch64 服务器（AWS Graviton、树莓派等）
nix run home-manager/master -- switch --flake ~/nix-config#remote-aarch64

# 可能遇到的问题：
1. error: experimental Nix feature 'nix-command' is disabled; add '--extra-experimental-features nix-command' to enable it
2. warning: ignoring untrusted substituter 'xxxx', you are not a trusted user.
Run `man nix.conf` for more information on the `substituters` configuration option.
# 解决方案：给 `/etc/nix/nix.conf` 添加以下内容：
experimental-features = nix-command flakes
trusted-users = root <your-username>
# 并重启 Nix 服务：
sudo systemctl restart nix-daemon


```

### 首次部署（无 Sudo 权限）

如果你在远程服务器上没有 `sudo` 权限，无法在根目录创建 `/nix`，请使用 [nix-portable](https://github.com/DavHau/nix-portable)：

```bash
# 1. 下载 nix-portable
curl -L https://github.com/DavHau/nix-portable/releases/latest/download/nix-portable-$(uname -m) > ~/nix-portable
chmod +x ~/nix-portable

# 2. 初始化环境（使用 nix-portable 代替 nix）
#    x86_64 服务器
./nix-portable nix run home-manager/master -- switch --flake ~/nix-config#remote
#    aarch64 服务器
./nix-portable nix run home-manager/master -- switch --flake ~/nix-config#remote-aarch64

# 3. 后续使用
# 你可以设置别名方便调用：alias nix="~/nix-portable nix"

#### 常见问题：Operation not permitted
如果在运行 `./nix-portable` 时报错 `setting up a private mount namespace: Operation not permitted`，说明服务器禁用了用户命名空间。请强制使用 proot 模式：
```bash
NP_RUNTIME=proot ./nix-portable <command>
```

```

### 切换默认 Shell

```bash
# 有 sudo 权限
chsh -s $(which zsh)

# 无 sudo 权限：在 ~/.bashrc 或 ~/.profile 中添加
# if [ -x "$(command -v zsh)" ]; then
#   exec zsh
# fi
```

> 首次运行会下载所有依赖，耗时较长，请耐心等待。

### 后续更新

```bash
cd ~/nix-config && git pull
home-manager switch --flake path:.#headless
# 或
just switch
```

> 本仓库必须使用 `path:.` 读取 git-crypt 解锁后的工作区；普通的 `.#remote` 可能从
> Git 对象取得密文。`just headless-switch` 会先实例化完整 activation derivation 作为 preflight，发现
> `vars/private.nix` 尚未解锁时直接给出提示。解锁后的 Nix 源码会进入 `/nix/store`，
> 因此 API key、token、密码和私钥必须使用 agenix，不要写入 `vars/private.nix`。
>
> Linux 上的 `just switch` 会自动判断：NixOS 执行系统 rebuild，其他发行版根据 CPU
> 架构选择 `headless` Home Manager；未安装 `home-manager` 时也会自动通过 `nix run` 首次部署。
> `headless` 表示“standalone Home Manager、无 sudo、无图形桌面”。全局
> `hostProfile.graphical = false` 会排除 GUI 模块、GUI 配置链接和仅桌面使用的软件。
> 用户名和 home 目录来自运行命令时的 `USER`/`HOME`，仓库不保存服务器用户名。
> 旧的 `#remote` / `just remote-switch` 名称暂时保留为兼容别名。

## 检查与 CI

```bash
just lint   # nixfmt、deadnix、Statix 和文本检查
just check  # 评估全部平台，只构建当前平台的完整配置
```

`.github/workflows/check-linux.yml` 与 `check-macos.yml` 分平台构建实际系统或 Home Manager
activation derivation。CI 不持有 git-crypt 密钥，而是在 checkout 后把加密的
`vars/private.nix` 替换为只含空 `sshHosts` 的临时占位配置，不输出或上传解密内容。

## 安全策略说明

- 这是个人管理的工作站配置：NixOS 有意保留 `NOPASSWD: ALL` 和普通用户
  `trusted-users`，二者都近似授予 root 权限，不应原样用于不受信任的多用户机器。
- Steam 入站防火墙开关默认全部关闭；需要时只在 `hosts/local/` 按主机开启。
- `allowUnfree = true` 有意保留，因为桌面层包含 Steam、专有 GUI 应用和字体；若用于
  更严格的服务器环境，应改为 allowlist。
- `localConfig.authorizedKeys` 支持按主机覆盖登录密钥。为避免迁移时锁死，未覆盖的主机
  暂时回退到 `vars/public.nix` 的兼容列表；确认新终端可登录后再缩小列表。
- darwin rebuild 不再自动更新、升级或 zap 清理 Homebrew；维护需显式执行
  `just brew-maintain`。

---

## 项目结构

```
nix-config/
├── flake.nix              # Flake 入口，定义所有输出
├── flake.lock
├── Justfile               # 常用命令快捷方式
├── vars/                  # 全局变量（用户名、主机列表等）
├── lib/                   # 辅助函数
├── config/                # 应用配置文件（nvim、zsh、lazygit 等）
├── modules/               # NixOS / macos 系统模块
├── home/
│   ├── tui-base/          # 共享终端开发环境（所有平台调用）
│   │   ├── git.nix
│   │   └── programs/      # nvim、yazi、zsh、eza、ohmyposh 等
│   ├── gui-base/          # 桌面机器扩展（在 tui-base 基础上加桌面工具）
│   │   └── programs/      # ai-tools、gui-tools、剪贴板绑定等
│   ├── linux/             # NixOS 专用（桌面环境、输入法等）
│   ├── macos/             # macOS 专用
│   └── remote/            # 远程服务器入口（直接调用 tui-base）
├── hosts/                 # 各主机硬件配置
└── pkgs/                  # 自定义 nix 包
```

### home 层级关系

```
remote  ──────────────────────→  tui-base
linux   →  gui-base  ─────────────→  tui-base
macos   →  gui-base  ─────────────→  tui-base
```
