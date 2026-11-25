---
name: ost-deanpeters-product-manager-skills-install
description: 'Use when installing, configuring, verifying, or updating deanpeters/Product-Manager-Skills for Codex, Claude Code, or Claude Desktop/Web via this open_supports package.'
argument-hint: '--client=codex-zip|codex-cli|claude-code|claude-desktop [--project-dir=PATH] [--skill=NAME] [--location=local|global] [--verify-only]'
---

# Product Manager Skills 安装（skill_for_setup）

> **安装作用域**：模式 D。`codex-zip` 以最后一个 `TARGET_DIR` / `--project-dir` 精确写入项目，不依赖 CWD；`codex-cli` 是全局模式，AI Agent 必须带 `--global` 且不得假装项目路径会改变其作用域。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)  
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> 官方仓库：[deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills)

## When to Use

当用户要把 Product Manager Skills 安装到 Codex、Claude Code、Claude Desktop 或 Claude Web，或要验证 / 更新这些安装入口时使用本 Skill。

范围包括：选择官方安装路径、运行支持包脚本、按摘要执行兜底安装、验证安装结果、提示下一步使用方式。范围不包括：详细 PM skill 使用教程、卸载、修改上游 skill 内容、账号权限处理或 API key 配置。

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) - 官方安装方式、更新方式、验证提示和注意事项
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) - 一键脚本支持的 client、flag、平台限制和验证逻辑
3. [`../../.ost-refs/`](../../.ost-refs/) 目录（如存在）- 本地约定

## Pre-checks

从对话上下文确认：

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | 自动检测 | 脚本支持 macOS、Linux、WSL；Windows 走兜底路径 |
| 目标客户端 | `codex-zip` | 可选 `codex-zip`、`codex-cli`、`claude-code`、`claude-desktop` |
| 目标项目目录 | 当前目录 | 仅 `codex-zip` 需要，用 `--project-dir=PATH` 指定 |
| skill 名称 | 无 | `codex-cli` 必填，用 `--skill=NAME` 指定 |
| 安装位置 | `local` | `codex-cli` 按官方命令需要 `--location=global` |
| 网络和命令 | 按 client 而定 | `codex-zip` 需要 `curl`、`unzip`；`codex-cli` 需要 `npx` |

缺少必填信息时，先使用脚本默认值；如果 `codex-cli` 未提供 `--skill`，要求用户选择 skill 或先用官方 list 命令发现 skill。

## Procedure

### 主路径：运行一键脚本（macOS、Linux、WSL）

从支持包根目录（本 `SKILL.md` 向上两级）执行：

```sh
sh scripts_for_install/install.sh [flags]
```

常用示例：

```sh
sh scripts_for_install/install.sh --client=codex-zip --project-dir=/path/to/project
sh scripts_for_install/install.sh --client=codex-cli --skill=prd-development --location=global
sh scripts_for_install/install.sh --client=claude-code
sh scripts_for_install/install.sh --client=claude-desktop
sh scripts_for_install/install.sh --client=codex-zip --project-dir=/path/to/project --verify-only
```

脚本行为：

- `codex-zip`：下载 latest `pm-skills-codex.zip`，复制 skill 目录到目标 repo 的 `.agents/skills/`，并创建或补充 `AGENTS.md`。
- `codex-cli`：按官方 Skills CLI 路径运行 `npx skills add deanpeters/Product-Manager-Skills --skill <name> -a codex -g`。
- `claude-code`：打印官方 Claude Code plugin marketplace 命令，由用户在 Claude Code 中执行。
- `claude-desktop` / `claude-web`：打印官方 ZIP 下载、解压、上传 individual skill ZIP 的步骤。

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 `repo_readme_summary.md` 第 2 部分（安装与更新）逐步执行：

- 用户平台是原生 Windows，脚本检测为不支持。
- 用户要求手动控制每条命令。
- `curl`、`unzip`、`npx` 缺失，且用户不希望安装这些依赖。
- 脚本下载、解压、复制或验证失败。
- 目标是 Claude Desktop / Web 上传流程，用户需要人工在 UI 中完成。
- 目标是 Claude Code plugin marketplace，需要用户在 Claude Code 交互界面运行 slash commands。

兜底时不要重新发明安装命令；按摘要中的官方路径给出步骤，并在执行 shell 命令前向用户确认。

### 验证

Codex ZIP 本地安装：

```sh
sh scripts_for_install/install.sh --client=codex-zip --project-dir=/path/to/project --verify-only
```

Codex Skills CLI 全局安装：

```sh
sh scripts_for_install/install.sh --client=codex-cli --skill=<skill-name> --location=global --verify-only
```

Claude Code / Claude Desktop / Web 没有脚本可自动验证 UI 状态；安装后用官方验证提示开启新对话或会话：

```text
Use the jobs-to-be-done skill to analyze this customer problem.
```

---

## 安装完成后告知用户

```text
Product Manager Skills 安装路径已处理。请开启新的 Codex / Claude 会话，并用以下提示验证：

Use the jobs-to-be-done skill to analyze this customer problem.

更新时，重新运行相同安装路径以获取 latest release；官方文档没有声明单独的 update command。
```

---

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| `unsupported platform` | 脚本只支持 macOS、Linux、WSL | 按 `repo_readme_summary.md` 第 2 部分走对应官方手动路径 |
| `required command not found: curl` 或 `unzip` | `codex-zip` 需要下载并解压 release ZIP | 安装缺失命令后重试，或手动下载 latest `pm-skills-codex.zip` |
| `codex-cli requires --skill` | Skills CLI 路径必须指定单个 skill | 先运行官方 list/discover 命令选择 skill，再带 `--skill=NAME` 重试 |
| `codex-cli` 要求 global | 官方 Codex Skills CLI 示例使用 `-g` | 使用 `--location=global`，或改走 `codex-zip` 本地安装 |
| Claude Desktop 上传后不可用 | 上传了外层 pack ZIP 或未开启新会话 | 先解压 pack，只上传内部 individual skill ZIPs，然后开启新 chat |
| Claude Code 命令无法在 shell 运行 | `/plugin ...` 是 Claude Code 内部 slash command | 打开 Claude Code，在交互界面运行脚本打印的命令 |
