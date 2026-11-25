---
name: skm
displayName: skm — AI Agent 技能包管理器
description: Local skill package manager for AI Agents. Use when installing,
  uninstalling, searching, linking, or updating AI Agent skills via skm CLI,
  or when running skm scan / relink / doctor commands.
version: 0.4.6
author: mocikadev
tags: [skm, skill-manager, install, link, update, scan, agent, tooling]
compatible_agents: [opencode, claude-code, codex, atomcode, gemini, cursor]
---

# skm — AI Agent 技能包管理器

`skm` 是一个本地 CLI 工具，统一管理 AI Agent 技能包（skill）的完整生命周期：安装、卸载、跨 Agent 软链接部署、更新和备份。

## 安装 skm

**Linux / macOS**

```bash
curl -fsSL https://raw.githubusercontent.com/mocikadev/mocika-skills-cli/main/install.sh | bash
```

**Windows**（PowerShell）

```powershell
irm https://raw.githubusercontent.com/mocikadev/mocika-skills-cli/main/install.ps1 | iex
```

> Windows 需开启 Developer Mode（设置 → 系统 → 开发者选项）或以管理员身份运行。

安装后运行 `skm --help` 验证。

## 版本检查

在会话中**首次调用任何 skm 命令前**，依次执行：

```bash
skm self-update --check
skm update --check skm
```

- `skm` 有新版本：告知用户 `skm 有可用更新 vX.Y.Z，是否立即升级？`，确认后执行 `skm self-update`
- `skm` skill 有更新：直接执行 `skm update skm`（纯文本文件，无需确认）
- 两者均已最新：静默继续，不打扰用户
- 每次会话各执行一次，不重复

## 数据目录

| 路径 | 说明 |
|------|------|
| `~/.agents/skills/` | 中央技能仓库（所有技能的唯一存储位置） |
| `~/.agents/.skill-lock.json` | 安装元数据锁文件（与 skilly 共用） |
| `~/.agents/sources.toml` | 注册表源配置 |
| `~/.agents/agents.toml` | 已注册 Agent 路径配置 |
| `~/.agents/.skm-backups/` | 技能备份目录 |
| `~/.agents/.skm-source-cache/` | Git / GitHub 源本地缓存（5 分钟 TTL） |

Agent 目录下的技能文件均为指向中央仓库的软链接，不复制文件。

## 快速工作流

### 第一次使用：检测已安装 Agent

```bash
skm scan            # 检测本机所有 AI Agent，写入 agents.toml
skm agent list      # 查看已注册的 Agent 列表
```

### 安装并部署技能

```bash
# 从注册表安装（默认链接到所有 Agent）
skm install mobile-android-design

# 安装到指定 Agent
skm install mobile-android-design --link-to opencode

# GitHub 简写（owner/repo，自动补全 github.com）
skm install mocikadev/mocika-skills-cli:skills/skm

# GitHub 简写 + 子目录（支持多级路径）
skm install wshobson/agents:mobile-android-design
skm install myorg/skills:tools/formatter --link-to opencode

# 完整 Git URL（GitLab / Gitee 等非 GitHub 平台使用此格式）
skm install https://gitlab.com/myorg/skills.git

# 完整 Git URL + 子目录
skm install https://github.com/myorg/skills.git#tools/formatter

# 直接粘贴 GitHub 网页地址
skm install https://github.com/myorg/skills/tree/main/formatter
```

### 新增 Agent 后补齐链接

```bash
skm scan            # 检测新 Agent（如 cursor）
skm relink cursor   # 将所有已安装技能链接到 cursor
```

## 完整命令参考

### 技能管理

#### `skm install <NAME> [--link-to <AGENT|all>]`

从注册表或 Git 仓库安装技能，**默认链接到所有已安装 Agent**（等价于 `--link-to all`）。NAME 支持以下格式：
- `skill-name` — 注册表名称
- `owner/repo` — GitHub 仓库根目录（固定解析为 github.com）
- `owner/repo:subpath` — GitHub 子目录，支持多级路径
- `<git-url>` — 完整 Git URL（适用于 GitLab/Gitee 等）
- `<git-url>#subpath` — 完整 URL + 子目录
- GitHub 网页 URL — 自动解析仓库和路径
- `/绝对路径`、`~/路径`、`./相对路径`、`file://` — 本地目录，直接复制，无需 git

```bash
skm install mobile-android-design
skm install mobile-android-design --link-to opencode
skm install wshobson/agents:mobile-android-design
skm install https://github.com/wshobson/agents.git --link-to opencode

# 本地路径（直接复制，无需 git）
skm install ~/dev/my-company-skills
skm install ~/dev/multi-skills#formatter       # 本地多 skill 目录 + 子目录
skm install /workspace/skills --link-to opencode
```

#### `skm uninstall <NAME>`

卸载技能：删除中央仓库目录并移除所有 Agent 的软链接。

```bash
skm uninstall mobile-android-design
```

#### `skm search <KEYWORD> [--limit <N>]`

在所有已配置的注册表中搜索技能（默认显示最多 20 条）。`skills.sh` 源走 HTTP API；GitHub / Git 源通过本地缓存扫描 SKILL.md（首次 git clone，之后 5 分钟内命中缓存）。

```bash
skm search android
skm search android --limit 5
```

输出格式：`<name>  <安装量>  <描述>`

#### `skm list [--outdated]`

列出所有已安装技能及其软链接状态。加 `--outdated` 只显示有可用更新的技能（会发起网络请求）。

```bash
skm list
skm list --outdated     # 只显示可更新的技能
```

#### `skm info <NAME>`

显示技能详细信息：frontmatter 元数据、锁文件条目、各 Agent 链接状态。

```bash
skm info mobile-android-design
```

#### `skm update [NAME] [--all] [--check]`

更新技能到最新版本（更新前自动备份）。省略 NAME 则更新全部；`--all` 是显式全部更新 flag（行为与省略 NAME 相同，但输出末尾显示错误汇总）。

```bash
skm update                                # 更新全部（隐式）
skm update --all                          # 更新全部（显式，推荐）
skm update mobile-android-design
skm update --check                        # 仅检查，不执行更新
skm update --check mobile-android-design
```

#### `skm link <NAME> <AGENT>`

为已安装技能在指定 Agent 目录下创建软链接。

```bash
skm link mobile-android-design opencode
```

#### `skm unlink <NAME> <AGENT>`

移除指定 Agent 目录下的技能软链接（不删除中央仓库文件）。

```bash
skm unlink mobile-android-design opencode
```

#### `skm relink [AGENT] [--skill <NAME>] [--force] [--backup] [--dry-run]`

批量重新链接技能。典型场景：新装 Agent 后同步所有技能。

```bash
skm relink                        # 对所有 Agent 重新链接所有技能
skm relink cursor                 # 仅对 cursor 重新链接
skm relink --skill mobile-android-design  # 仅重新链接指定技能
skm relink cursor --dry-run       # 预览，不实际执行
skm relink cursor --force         # 覆盖冲突路径
```

#### `skm export [--output <FILE>]`

将所有已安装技能（Git / GitHub / 注册表来源）导出为可分享的 `skills.bundle` 文件。本地路径来源自动跳过。

```bash
skm export                                   # → ./skills.bundle
skm export --output ~/dotfiles/skills.bundle
```

#### `skm import <FILE> [--link-to <AGENT|all>] [--force]`

从 `.bundle` 文件批量安装技能。已安装的技能默认跳过（幂等），`--force` 强制覆盖。

```bash
skm import skills.bundle
skm import skills.bundle --link-to opencode
skm import skills.bundle --force   # 强制重装所有条目
```

### 注册表管理

```bash
skm source list                                          # 列出所有注册表源（含类型）
skm source add my-org https://github.com/my-org/skills   # 添加 GitHub 仓库为源
skm source add private git@github.com:org/private-skills  # SSH 私有仓库
skm source add gitlab https://gitlab.com/org/skills.git   # 其他 Git 平台
skm source add dev ~/dev/my-company-skills               # 本地目录作为源
skm source add local-ws /workspace/shared-skills         # 本地绝对路径
skm source remove my-org                                  # 移除注册表源
```

`skm source add` 会自动检测 URL 类型：`github.com` → `github`，其他含 `://` 或 `git@` → `git`，`skills.sh` → `skills.sh`，本地路径（`/`、`~`、`./`、`../`、`file://`）→ `local`。GitHub / Git 源的搜索结果会缓存到 `~/.agents/.skm-source-cache/`；本地源直接扫描目录。

配置文件：`~/.agents/sources.toml`

### Agent 管理

```bash
skm scan                          # 自动检测并注册本机 AI Agent
skm scan --dry-run                # 预览检测结果，不写入配置
skm scan --import skills.bundle   # 检测 Agent 并同时从 bundle 导入技能
skm agent list                    # 列出所有已注册 Agent 及其技能数量
skm agent add my-agent ~/.my-agent/skills  # 手动注册自定义 Agent
```

配置文件：`~/.agents/agents.toml`

内置支持的 Agent：`claude-code`、`codex`、`atomcode`、`gemini-cli`、`copilot-cli`、`opencode`、`antigravity`、`cursor`、`kiro`、`codebuddy`、`openclaw`、`trae`、`junie`、`qoder`、`trae-cn`、`windsurf`、`augment`、`kilocode`、`ob1`、`amp`、`hermes`、`factory-droid`、`qwen`、`cline`、`roo`、`goose`、`continue`、`warp`、`openhands`、`firebender`、`zencoder`、`cortex`、`deepagents`、`crush`、`kimi-cli`、`mux`、`neovate`、`mistral-vibe`、`pochi`、`openclaude-ide`、`kode`、`mcpjam`、`bob`、`adal`、`pi`、`oh-my-pi`、`iflow-cli`、`command-code`

### 备份管理

```bash
skm backup list                                          # 列出所有技能的备份快照（按技能分组）
skm backup list mobile-android-design                    # 列出指定技能的备份快照
skm backup restore mobile-android-design                 # 恢复最新快照
skm backup restore mobile-android-design 1776758731056   # 恢复指定快照
skm backup delete mobile-android-design 1776758731056    # 删除指定快照
```

备份目录：`~/.agents/.skm-backups/<skill-name>/<snapshot-id>/`

### 诊断

#### `skm doctor`

检测环境健康状态，诊断三类问题：
- **ENV**：共享目录、锁文件、agents.toml 是否存在
- **AGENTS**：已注册 Agent 是否实际安装（可执行文件 / 配置目录存在）
- **LINKS**：已安装技能在各 Agent 下的软链接是否完整
- **INTEGRITY**：对比安装时记录的 hash，检测本地是否被意外修改

发现问题时以非零退出码（1）退出，适合在 CI 或初次配置时验证环境。

```bash
skm doctor
```

#### `skm doctor fix-skills [--dry-run]`

扫描中央仓库所有 skill 的 `SKILL.md`，自动修复 frontmatter 格式问题（缺少分隔符、name 与目录名不一致等）。`--dry-run` 仅报告，不写文件。

```bash
skm doctor fix-skills
skm doctor fix-skills --dry-run
```

#### `skm doctor sync [--agent <ID>] [--dry-run] [--force]`

扫描 Agent 的 skills 目录，清理悬空软链接（broken），并为中央仓库中未链接的 skill 补建软链接（orphan）。

```bash
skm doctor sync                          # 修复所有 Agent 的链接
skm doctor sync --dry-run                # 预览，不实际执行
skm doctor sync --agent opencode         # 只处理 opencode
skm doctor sync --force                  # 冲突路径也覆盖
```

### 自升级

```bash
skm self-update            # 升级 skm binary 到最新版本
skm self-update --check    # 仅检查是否有新版本，不执行升级
```

更新 skm skill 本身（有更新时直接执行，无需确认）：

```bash
skm update skm
skm update --check skm    # 仅检查，不执行
```

## 常用场景速查

| 场景 | 命令 |
|------|------|
| 初次配置，检测所有 Agent | `skm scan` |
| 安装技能到所有 Agent | `skm install <name>`（默认） |
| 安装到指定 Agent | `skm install <name> --link-to opencode` |
| 新装了一个 Agent | `skm scan && skm relink <new-agent>` |
| 查看某技能链接到哪些 Agent | `skm info <name>` |
| 检查是否有可用更新 | `skm update --check` |
| 升级技能（自动备份） | `skm update <name>` 或 `skm update --all` |
| 升级出问题，回滚 | `skm backup list [name]` 后 `skm backup restore <name>` |
| 导出技能集（分享/备份） | `skm export --output ~/dotfiles/skills.bundle` |
| 在新机器还原技能集 | `skm import ~/dotfiles/skills.bundle` |
| 修复悬空/缺失软链接 | `skm doctor sync` |
| 修复 SKILL.md frontmatter | `skm doctor fix-skills` |
| 诊断环境 / 链接问题 | `skm doctor` |
