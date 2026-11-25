---
name: ncm-cli-setup
description: 安装和配置 ncm-cli（网易云音乐 CLI 工具）。当用户需要安装 ncm-cli、配置 API Key、安装 mpv 播放器，或排查安装问题时，使用此 skill。
---

# ncm-cli 安装配置

ncm-cli 是网易云音乐的 CLI 工具（音乐搜索、播放控制、歌单管理、TUI 播放器）。

## 安装流程

### 第一步：安装 ncm-cli、mpv

#### 1.1 安装 ncm-cli

```bash
npm install -g @music163/ncm-cli
```

验证安装：

```bash
ncm-cli --version
```

#### 1.2 安装 mpv

仅当用户需要本地播放且选用 mpv 时安装播放器；搜索、推荐和歌单查询可跳过本节。先检测是否已安装：

```bash
mpv --version
```

**macOS / Windows**：若未安装，直接执行安装脚本：

```bash
python skills/ncm-cli-setup/scripts/install_mpv.py
```

**Linux**：询问用户是否需要播放功能：

- 如果是桌面环境、需要本地播放 → 执行 `python skills/ncm-cli-setup/scripts/install_mpv.py`
- 如果是服务器环境、不需要播放 → 跳过，搜索/歌单等命令仍可正常使用

以上路径相对仓库根目录；从其他目录执行时使用本 Skill 下 [安装脚本](scripts/install_mpv.py) 的绝对路径。`python` 不可用时使用本机实际可用的 Python 命令。安装后以 `mpv --version` 成功为准，脚本跳过安装或提示重启终端不代表当前进程已可播放。

安装脚本会自动识别包管理器：

- **macOS**：Homebrew（`brew install mpv`）或 MacPorts
- **Linux**：apt / dnf / pacman / zypper
- **Windows**：winget / Chocolatey / Scoop

### 第二步：配置 API Key

使用 ncm-cli 需要先设置API Key：

```bash
ncm-cli config set appId <你的AppId>
ncm-cli config set privateKey <你的PrivateKey>
```

> 如果还没有 API Key，请先前往[网易云音乐开放平台](https://developer.music.163.com/st/developer/apply/account?type=INDIVIDUAL)申请 API Key（appId 和
> privateKey）。

### 第三步：配置默认播放器

仅在需要播放且已有配置或用户选择不能确定时询问默认播放器；保留有效的现有配置：

- **mpv**（内置播放器）：轻量、跨平台，需先完成第一步中的 mpv 安装
- **orpheus**（云音乐 App）：调用本地网易云音乐客户端播放，仅支持 macOS

根据用户选择执行：

```bash
ncm-cli config set player mpv      # 选择内置播放器
ncm-cli config set player orpheus  # 选择云音乐 App
```

### 第四步：登录

需要登录的业务操作前检查 `ncm-cli login --check`；未登录时启动一次后台流程：

```bash
ncm-cli login --background
```

## 常见问题

| 问题                           | 解决方法                                                       |
|------------------------------|------------------------------------------------------------|
| `ncm-cli: command not found` | 用 `npm prefix -g` 查全局前缀；Windows 检查该目录，macOS/Linux 检查其 `bin/` 是否在 PATH 中                      |
| `mpv not found`              | 重新运行 `python skills/ncm-cli-setup/scripts/install_mpv.py` 或手动安装：https://mpv.io |
| 登录超时                         | 说明未完成登录；用户准备重试后再启动一次后台流程                          |

## 基本信息

- 安装前检查 Node.js、npm 和当前包声明的运行要求；不要把历史最低版本当作永久兼容保证。
- 配置只在用户本机完成，不要求用户将私钥粘贴到聊天或仓库。安装/登录完成后转回 [CLI 执行规范](../netease-music-cli/SKILL.md) 验证所需能力。
