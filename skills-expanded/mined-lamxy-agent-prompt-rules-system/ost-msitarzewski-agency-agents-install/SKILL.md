---
name: ost-msitarzewski-agency-agents-install
description: '帮助用户安装或更新 Agency Agents。主路径：运行支持包内的一键脚本；脚本不可用时回退到 repo_readme_summary.md 第 2 部分。范围：CLI agent 安装、更新、选择工具/division/agent、dry-run 和验证入口；不含卸载、删除配置或桌面应用安装。'
argument-hint: '[--tool=claude-code|codex|all] [--division=engineering] [--agent=frontend-developer] [--project-dir=/path/to/project] [--dry-run] [--verify-only]'
---

# Agency Agents 安装（skill_for_setup）

> **安装作用域**：模式 D。项目级上游工具依赖 CWD；AI Agent 必须传入最后一个 `TARGET_DIR`（或 `--project-dir`），脚本会在子 Shell 中调用官方安装器。全局工具可省略目录。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)  
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> 官方仓库：[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)

## When to Use

当用户想通过自然语言为 Claude Code、Codex CLI 或脚本支持的其他 AI 工具安装、更新、预览或列出 Agency Agents 时使用本 Skill。

优先覆盖：

- Claude Code：安装到 Claude Code agents 体系，或由上游 installer 默认检测。
- Codex CLI：使用 `--tool=codex` 转换并安装 Agency Agents。

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) — 安装方式、手动兜底路径、验证方式和注意事项
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) — wrapper 实际支持的平台、参数和验证行为
3. [`../../.ost-refs/`](../../.ost-refs/) 目录（如存在）— 本地约定

## Pre-checks

从对话上下文中确认；用户没有明确说明时使用默认值，不额外追问：

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | 当前 shell 平台 | 主路径支持 macOS、Linux、WSL、Windows Git Bash/MSYS |
| 目标工具 | 脚本默认检测 | 可显式传 `--tool=claude-code` 或 `--tool=codex` |
| 安装范围 | 上游 installer 默认 | 可用 `--division=LIST`、`--agent=LIST` 或 `--agents-file=PATH` 缩小范围 |
| 项目目录 | 当前目录 | 项目级工具用 `--project-dir=PATH` 指定 |
| 是否先预览 | 否 | 不确定写入位置时先加 `--dry-run` |
| 官方 checkout 缓存 | `~/.cache/agency-agents/agency-agents` | 可用 `--repo-dir=PATH` 隔离缓存 |

## Procedure

### 主路径：运行一键脚本（macOS、Linux、WSL、Windows Git Bash/MSYS）

从支持包根目录（本 `SKILL.md` 向上两级）执行：

```sh
sh scripts_for_install/install.sh [flags]
```

脚本要求当前环境有 `git` 和 `bash`。它会克隆或快进官方 `msitarzewski/agency-agents` checkout，然后以非交互方式调用官方 Bash installer。已有 checkout 若存在本地未提交变更，脚本会停止并要求换 `--repo-dir=PATH` 或先处理该 checkout。

常用示例：

```sh
sh scripts_for_install/install.sh --tool=claude-code --division=engineering --project-dir=/path/to/project
sh scripts_for_install/install.sh --tool=codex --division=engineering --project-dir=/path/to/project
sh scripts_for_install/install.sh --tool=codex --agent=frontend-developer,backend-developer --dry-run
sh scripts_for_install/install.sh --tool=all --parallel
sh scripts_for_install/install.sh --list=teams
sh scripts_for_install/install.sh --verify-only
```

注意：本 wrapper 的 `--tool` 白名单为 `all`、`claude-code`、`copilot`、`antigravity`、`gemini-cli`、`opencode`、`openclaw`、`cursor`、`aider`、`windsurf`、`qwen`、`kimi`、`codex`、`osaurus`、`hermes`。不要把 `repo_readme_summary.md` 中其他历史或官方 README 示例里的工具名直接传给 wrapper，除非脚本已支持。

### 参数映射

| 用户意图 | 使用参数 |
|----------|----------|
| 安装到 Claude Code | `--tool=claude-code` |
| 安装到 Codex CLI | `--tool=codex` |
| 安装 engineering division | `--division=engineering` |
| 安装单个或多个 agent | `--agent=frontend-developer,backend-developer` |
| 从文件读取 agent 列表 | `--agents-file=/path/to/agents.txt` |
| 指定项目目录 | `--project-dir=/path/to/project` |
| 指定官方 checkout 缓存 | `--repo-dir=/path/to/cache/agency-agents` |
| 覆盖单工具安装目录 | `--path=/path/to/tool/config` |
| 使用 symlink | `--link` |
| 不自动转换 | `--no-convert` |
| 并行安装 | `--parallel --jobs=N` |
| 只预览 | `--dry-run` |
| 只验证 wrapper 和上游 installer | `--verify-only` |
| 列出工具、teams/divisions 或 agents | `--list=tools`、`--list=teams`、`--list=agents`、`--list=all` |

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 `repo_readme_summary.md` **第 2 部分（安装与更新）** 逐步执行：

- 用户环境不是 macOS、Linux、WSL 或 Windows Git Bash/MSYS。
- 用户没有 `git` 或 `bash`，且不希望安装这些依赖。
- wrapper 报错且用户要求手动控制安装过程。
- 用户要安装 Agency Agents 桌面应用，而不是 CLI agents。
- 用户要求的目标工具不在 wrapper `--tool` 白名单内，但官方摘要提供了对应手动命令。

将兜底路径中的安装命令发给用户确认后逐条运行。不要在本 Skill 中默认执行卸载或删除配置。

### 验证

Wrapper 自检：

```sh
sh scripts_for_install/install.sh --verify-only
```

该命令会确认官方 checkout 存在 `scripts/install.sh` 和 `scripts/convert.sh`，并运行上游 installer 的 `--list tools` 响应检查。

安装前预览：

```sh
sh scripts_for_install/install.sh --tool=codex --division=engineering --dry-run
```

安装后验证方式取决于目标工具；官方摘要没有提供统一的命令行验证。可使用以下事实来源中的检查：

```sh
codex --help
opencode agent list
```

Claude Code 没有在摘要中给出专用 CLI 验证命令；安装完成后重启 Claude Code，并用自然语言提到已安装 agent 名称进行检查，例如 `Frontend Developer`。

---

## 安装完成后告知用户

```text
Agency Agents install/update completed.

Next steps:
1. Restart the target AI tool so it reloads agent files.
2. Reference an installed agent by name, for example Frontend Developer.
3. Re-run this script later to fast-forward the official checkout and update files.

For the desktop app instead, use the official release page:
https://github.com/msitarzewski/agency-agents-app/releases/latest
```

---

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| `missing required command: git` | wrapper 需要 Git 克隆或更新官方仓库 | 安装 Git 后重试，或改走摘要第 2 部分的手动路径 |
| `missing required command: bash` | 上游官方 installer 是 Bash 脚本 | 安装 Bash 3.2 或更新版本后重试，或改走手动路径 |
| `unsupported platform` | 当前平台不在 macOS、Linux、WSL、Windows Git Bash/MSYS 内 | Windows 用户可使用 Git Bash/MSYS，或安装官方桌面应用 |
| `checkout has local changes` | `--repo-dir` 指向的官方 checkout 有本地修改 | 处理该 checkout 的修改，或指定新的 `--repo-dir=PATH` |
| `--tool must be ...` | 传入的工具名不在 wrapper 白名单 | 改用白名单工具名；若官方摘要有手动命令，走兜底路径 |
| 不确定会写入哪些文件 | 多工具安装涉及多个目标目录 | 先运行同参数加 `--dry-run` |
| 安装后目标工具没有显示 agents | 工具可能需要重新加载配置，或目标目录不符合预期 | 重启目标 AI 工具；必要时用 `--dry-run` 或 `--path=PATH` 检查目标目录 |
