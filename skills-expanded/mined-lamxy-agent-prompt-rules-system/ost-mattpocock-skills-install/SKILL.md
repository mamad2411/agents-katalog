---
name: ost-mattpocock-skills-install
description: '帮助用户安装、更新并验证 Skills For Real Engineers（mattpocock/skills），支持 Claude Code、Codex、GitHub Copilot、Gemini CLI 插件/skills 安装与 npx skills（skills.sh）可编辑文件安装。主路径：运行支持包内的 install.sh；脚本不可用时回退到 repo_readme_summary.md 第 2 部分。范围：安装、作用域选择、更新入口、验证、提示运行 /setup-matt-pocock-skills；不含卸载、自动改写 ~/.copilot/settings.json、skill 用法教程。'
argument-hint: '--client=claude-code|codex|copilot|gemini|npx [--agent=NAME] [--yes] [--global|--local] [--verify-only] [--dry-run] [项目目录]'
---

# Skills For Real Engineers 安装（skill_for_setup）

> **安装作用域（模式 D）**：Claude Code / Codex / Copilot 插件与 `gemini skills install` 官方默认用户级；`npx skills@latest add mattpocock/skills -a <agent>` 官方默认项目级且 CWD 敏感，`-g` 为全局。项目分支必须把已确认的项目目录传给脚本，由脚本在子 Shell 中 `cd` 后执行；全局 / 插件分支不传项目目录。依据：[官方 README · Installation](https://github.com/mattpocock/skills#installation-30-second-setup)、[vercel-labs/skills · Installation Scope](https://github.com/vercel-labs/skills#installation-scope)。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)  
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> 官方仓库：[mattpocock/skills](https://github.com/mattpocock/skills)

## When to Use

- 用户要安装、更新或验证 mattpocock/skills（`mattpocock-skills` 插件，或 skills.sh 可编辑文件）。
- 用户要为 Claude Code、Codex、GitHub Copilot、Gemini CLI，或 Cursor / OpenCode / Windsurf / Amp 等其他 agent 获取这些 skills。
- 用户在问 `/grill-me`、`/setup-matt-pocock-skills` 等命令为何不可用，需要检查安装状态。

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) — 第 2 部分：安装方式、作用域表、更新与验证命令。
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) — 运行 `sh scripts_for_install/install.sh --help` 确认 flag。
3. [`../../.ost-refs/`](../../.ost-refs/)（如存在）— 本地约定。

## Pre-checks

从对话上下文确认以下信息；不明确时询问用户，不要替用户选择 local/global。

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | — | macOS / Linux / WSL 走主路径；原生 Windows 走兜底路径 |
| 客户端 | `claude-code` | `claude-code`、`codex`、`copilot`、`gemini`、`npx`。**每个 agent 只选一种方式**（插件或 npx），两种都装会让每个 skill 出现两次 |
| 安装范围 | 按客户端的官方默认 | `claude-code` / `gemini`：默认用户级，`--local` 改项目级；`codex` / `copilot`：仅用户级；`npx`：默认项目级，`--global` 改全局（`-g`） |
| 项目目录 | 无（全局 / 插件分支） | 仅项目分支需要：`claude-code --local`、`gemini --local`、`npx` 默认分支。必须向用户确认明确的已存在目录并传给脚本；不得依赖支持包目录或 Agent 当前 CWD。全局分支不得携带项目目录（脚本会报错） |
| npx 目标 agent | 交互选择 | `--agent=cursor` 等；省略时由 skills CLI 交互询问 |
| 仅验证 | 否 | `--verify-only` 只检查当前状态 |

运行任何会改动本机插件、skills 目录或 agent 配置的命令前，先用 `--dry-run` 或直接展示完整命令，获得用户确认后再执行。

## Procedure

### 主路径：运行一键脚本（macOS / Linux / WSL）

从支持包根目录（本 SKILL.md 向上两级）执行：

```sh
sh scripts_for_install/install.sh [--client=NAME] [--agent=NAME] [--yes] [--global|--local] [--verify-only] [--dry-run] [项目目录]
```

作用域说明（与 `repo_readme_summary.md` 第 2 部分及 `install.sh --help` 一致，D 类双模式）：

- **用户级（官方默认，插件 / Gemini）**：`claude-code` 执行 `claude plugin install mattpocock-skills@claude-plugins-official`（默认 `--scope user`）；`codex` 写入 `~/.codex`；`copilot` 写入 `~/.copilot`；`gemini` 写入 `~/.gemini/skills/`。直接执行，不传项目目录。
- **项目级（显式 `--local`）**：`claude-code` 改用原生 `--scope project`，`gemini` 改用 `--scope workspace`；脚本验证项目目录后在 `( cd 项目目录 && ... )` 子 Shell 中执行，调用端 CWD 不变。
- **npx（官方默认项目级）**：不带 `-g` 时写入项目目录下该 agent 的项目级 skills 目录（路径因 agent 而异，例如 `claude-code` → `.claude/skills/`，`cursor` / `opencode` → `.agents/skills/`，`windsurf` → `.windsurf/skills/`；完整表见 [vercel-labs/skills · Supported Agents](https://github.com/vercel-labs/skills#supported-agents)）。skills CLI 无原生项目路径 flag，脚本在子 Shell 中 `cd` 到已验证的项目目录执行。`--global` 改为 `-g` 写入用户级目录，此时不得再给项目目录。
- 脚本对项目目录的内部默认值是 `.`；本 Skill 调用时始终传入已确认的绝对路径，不依赖该默认值。

常用示例：

```sh
# Claude Code 插件，用户级（官方默认）
sh scripts_for_install/install.sh --client=claude-code

# Claude Code 插件，项目级（用户明确选择）
sh scripts_for_install/install.sh --client=claude-code --local /work/app

# Codex / Copilot（仅用户级）
sh scripts_for_install/install.sh --client=codex
sh scripts_for_install/install.sh --client=copilot

# Gemini CLI，用户级；项目级用 --local
sh scripts_for_install/install.sh --client=gemini
sh scripts_for_install/install.sh --client=gemini --local /work/app

# npx 可编辑文件，项目级（官方默认）；先 dry-run 预览
sh scripts_for_install/install.sh --client=npx --agent=cursor --dry-run /work/app
sh scripts_for_install/install.sh --client=npx --agent=cursor /work/app

# npx 全局
sh scripts_for_install/install.sh --client=npx --agent=cursor --global
```

脚本 flag：

| Flag | 作用 |
|------|------|
| `--client=NAME` | `claude-code`（默认）、`codex`、`copilot`、`gemini`、`npx` |
| `--agent=NAME` | 仅 `npx`：目标 agent（如 `cursor`、`opencode`、`windsurf`）；省略则交互选择 |
| `--yes` | 仅 `npx`：非交互安装全部 skills（传 `-y`，含 `setup-matt-pocock-skills`）；省略则保持官方交互选择 |
| `--global` | 显式用户级 / 全局安装 |
| `--local` | 显式项目级（仅 `claude-code`、`gemini`、`npx` 支持） |
| `项目目录` | 项目级目标目录，必须已存在 |
| `--verify-only` | 不安装，只验证 |
| `--dry-run` | 只打印将执行的命令 |

注意：

- npx 安装器询问选择哪些 skills 时，**必须包含 `setup-matt-pocock-skills`**。
- `copilot` 分支只打印 `~/.copilot/settings.json` 自动更新配置，脚本不改写 JSON；如需自动更新，让用户手动合并。

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 [`repo_readme_summary.md`](../../repo_readme_summary.md) **第 2 部分（安装与更新）** 逐步执行：

- 用户平台为原生 Windows（脚本报 `不支持的平台`）。
- 脚本报 `找不到必需命令`，或其他执行错误。
- 用户使用 VS Code Copilot Chat（需在 GUI 中运行 **Chat: Install Plugin From Source**）。
- 用户想手动控制每条命令，或需要脚本未覆盖的参数（如 `--skill`、`-y`、copy/symlink 方式）。

将每条会写入本机配置的命令发给用户确认后逐条运行；项目级 npx 命令须在子 Shell 中执行：`(cd "<已确认项目目录>" && npx skills@latest add mattpocock/skills -a <agent>)`。

### 验证

```sh
sh scripts_for_install/install.sh --client=claude-code --verify-only
sh scripts_for_install/install.sh --client=codex --verify-only
sh scripts_for_install/install.sh --client=npx --verify-only /work/app
sh scripts_for_install/install.sh --client=npx --global --verify-only
```

手动验证（来自摘要第 2 部分）：

```sh
claude plugin list
codex plugin list
npx skills@latest list
npx skills@latest list -g
```

Copilot / Gemini 无专门验证命令：在 agent 中输入 `/ask-matt` 或 `/grill-me`，能被识别并开始对话即表示可用。

### 更新

- Claude Code / Codex / Copilot 插件：自动更新。
- Gemini CLI：重新运行本脚本（官方：重新执行两条 install 命令）。
- npx：`npx skills@latest update`（项目级需在目标项目目录的子 Shell 中运行）；新增 skill 需重新运行 add。

---

## 安装完成后告知用户

```
mattpocock/skills 已安装。下一步：
1. 重启或重新打开对应 agent。
2. 在每个要使用的仓库中打开 agent，各运行一次 /setup-matt-pocock-skills
   （配置 issue tracker、triage labels 和文档保存位置）。
3. 试用：/grill-with-docs I want to add CSV export to the reports page
插件路径自动更新；npx 与 Gemini 路径需手动更新。
如支持包内存在 usage_examples.md，可阅读其中的使用示例。
```

---

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| 每个 skill 出现两次 | 同一 agent 同时用了插件和 npx 两种方式 | 只保留一种；卸载方式见官方 `claude plugin uninstall` / `npx skills remove` 说明，不默认执行 |
| engineering skills 提示缺少 tracker / labels 配置 | 未运行或 npx 安装时漏选 `setup-matt-pocock-skills` | 重新 add 并勾选该 skill，然后在仓库中运行 `/setup-matt-pocock-skills` |
| `--client=codex 官方仅支持用户级插件安装` | 对 codex / copilot 传了 `--local` 或项目目录 | 去掉 `--local` 与项目目录 |
| `默认用户级安装，不接受项目目录` / `--global 模式…不接受项目目录` | 全局分支携带了项目目录 | 全局去掉目录；项目级显式加 `--local` 再传目录 |
| `找不到必需命令：git` | npx 路径需要 git 克隆仓库 | 先安装 git 再重试 |
| `项目目录不存在` | 目标目录未创建或路径有误 | 与用户确认正确的已存在目录 |
| npx 装到了错误项目 | 手动执行时 CWD 不是目标项目根 | 使用脚本并传入项目目录，或在 `(cd 目录 && ...)` 子 Shell 中执行 |
| `/grill-me` 等不可用 | agent 未重启，或 User-invoked skill 需用户手动输入 | 重启 agent 后 `--verify-only`；手动输入 `/xxx` 触发 |
| `不支持的平台` | 原生 Windows | 走兜底路径，在 PowerShell 中运行摘要第 2 部分的官方命令 |
