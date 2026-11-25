---
name: ost-eyaltoledano-claude-task-master-install
description: '帮助用户安装或更新 Taskmaster / task-master-ai。主路径：运行支持包内的一键脚本；脚本不可用或用户需要手动 MCP/Windows 路径时回退到 repo_readme_summary.md 第 2 部分。范围：npm 安装、可选 Claude Code MCP 注册、可选项目初始化；不含写入 API keys 或卸载。'
argument-hint: '可选：--location=local|global、--project-dir=DIR、--claude-mcp、--tools=core|standard|all、--init-project'
---

# Taskmaster 安装（skill_for_setup）

> **安装作用域**：模式 D；本地 npm 安装为 CWD-sensitive。AI Agent 必须把目标项目作为最后一个 `TARGET_DIR` 参数（或 `--project-dir`）传入；全局安装不带目录。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)  
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> 官方仓库：[eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)

## When to Use

当用户希望安装、更新或配置 Taskmaster / `task-master-ai` 时使用本 Skill。典型触发包括：

- "安装 Taskmaster"
- "给 Claude Code 配置 task-master-ai MCP"
- "在这个项目里安装 claude-task-master"
- "更新 task-master-ai CLI"
- "初始化 Taskmaster 项目"

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) — 安装方式、平台限制、API key 位置、MCP 配置和验证命令
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) — 实际支持的参数、检查逻辑和脚本边界
3. [`../../.ost-refs/`](../../.ost-refs/) 目录（如存在）— 本地约定

## Pre-checks

从对话上下文中确认：

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | 无 | 主路径只支持 macOS、Linux、WSL；Windows native shell 走兜底路径 |
| 安装范围 | `--location=local` | 本地安装会修改目标项目；全局安装使用 `npm install -g` |
| 目标项目目录 | 当前目录 | 本地安装、初始化和 `.env` 均与项目目录相关 |
| 是否配置 Claude MCP | 否 | 只有用户明确要求 Claude Code MCP 时传 `--claude-mcp` |
| MCP 工具加载模式 | 未设置 | 可选 `core`、`standard`、`all`、`lean` 或逗号列表 |
| 是否初始化项目 | 否 | `--init-project` 会运行交互式 `task-master init` 并修改项目 |
| API keys / provider | 不写入 | 告知用户按官方文档放到 `.env` 或 MCP `env` 区块；不要代填密钥 |

如果目标项目目录、安装范围或是否配置 MCP 不明确，先向用户确认。不要在未确认目录时执行本地安装或初始化。

## Procedure

### 主路径：运行一键脚本（macOS / Linux / WSL）

从支持包根目录（本 `SKILL.md` 向上两级）执行：

```sh
sh scripts_for_install/install.sh [options] [TARGET_DIR]
```

常用示例：

```sh
sh scripts_for_install/install.sh --location=local --project-dir=/path/to/project
sh scripts_for_install/install.sh --global
sh scripts_for_install/install.sh --global --claude-mcp --tools=core
sh scripts_for_install/install.sh --location=local --init-project /path/to/project
```

脚本会执行平台检查、Node.js/npm/npx 检查、npm 安装 / 更新、CLI 验证；只有显式传 `--claude-mcp` 才会修改 Claude Code MCP 配置，只有显式传 `--init-project` 才会运行 `task-master init`。

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 `repo_readme_summary.md` **第 2 部分（安装与更新）** 逐步执行：

- 用户处于 Windows native shell，不能或不想使用 WSL / Git Bash 运行脚本
- 用户需要 Cursor 一键安装、Cursor / Windsurf / VS Code / Q Developer CLI 的手动 MCP JSON 配置
- 用户需要把 API keys 写入 MCP config 的 `env` 区块，或需要编辑 `.env`
- 脚本执行失败且错误不属于可直接补充参数的情况
- 用户需要逐条确认官方安装命令

将第 2 部分中对应路径的安装命令或 JSON 片段发给用户确认后逐条处理。不要代填 API key，不要把密钥写入仓库。

### 验证

全局安装：

```sh
task-master --version
task-master models
```

本地安装：

```sh
npx task-master --version
npx task-master models
```

项目初始化后：

```sh
task-master list
task-master next
```

如果使用 MCP，重启目标编辑器或 Claude Code 后，让 Agent 执行：

```text
Initialize taskmaster-ai in my project
What's the next task I should work on?
```

---

## 安装完成后告知用户

```text
Taskmaster 安装 / 更新完成。下一步：
1. 在项目根 .env 或 MCP 配置 env 区块中设置所需 API keys；使用 Claude Code / Codex CLI provider 时确认对应 CLI 已认证。
2. 运行 task-master models --setup 配置 main / research / fallback 模型。
3. 运行 task-master init，或通过 MCP 让 Agent 初始化项目。
4. 将 PRD 放到 .taskmaster/docs/prd.txt，然后运行 task-master parse-prd .taskmaster/docs/prd.txt。
```

---

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| Node.js 版本不满足要求 | Taskmaster `package.json` 要求 Node.js >= 20.0.0 | 先升级 Node.js，再重新运行脚本 |
| 本地安装后找不到 `task-master` | 本地 npm bin 不在 PATH | 在项目目录使用 `npx task-master ...` |
| `task-master models` 报 API key 缺失 | 选定 provider 的 key 没放到 `.env` 或 MCP `env` | 按 `repo_readme_summary.md` 第 2 部分配置 API keys |
| MCP 显示 `0 tools enabled` | 编辑器未重载或 API keys / MCP env 配置错误 | 重启编辑器，检查 MCP config 和 API keys |
| MCP 请求 60 秒超时 | `parse_prd`、`expand_task`、`research` 等操作可能运行 2-5 分钟 | 在 MCP config 加 `timeout: 300` |
| `task-master init` 不响应 | 官方已记录初始化脚本可能需要直接运行 | 按 `repo_readme_summary.md` 第 4 部分使用 Node 直接运行初始化脚本 |
| Windows native shell 报不支持 | 支持包脚本只支持 macOS、Linux、WSL | 使用官方 npm 命令或在 WSL / Git Bash 中运行脚本 |
