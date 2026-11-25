---
name: ost-topoteretes-cognee-install
description: '帮助用户安装或更新 Cognee。主路径：运行支持包内的一键脚本；脚本不可用时回退到 repo_readme_summary.md 第 2 部分。范围：Python 包、extras、本地/用户级安装与轻量验证；不自动写入 .env、Docker、Claude、Agent 或 MCP 配置。'
argument-hint: '[--location=local|global] [--venv-dir=PATH] [--extras=LIST] [--manager=auto|uv|pip] [--dry-run]'
---

# Cognee 安装（skill_for_setup）

> **安装作用域**：模式 D；本地 wrapper 为路径参数型。AI Agent 必须传最后一个 `TARGET_DIR`，脚本会安装到 `TARGET_DIR/.venv`；`--global` 不带目录。

> 参考：[`repo_readme_summary.md`](../../repo_readme_summary.md)  
> 脚本：[`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> 官方仓库：[topoteretes/cognee](https://github.com/topoteretes/cognee)

## When to Use

当用户要求安装、更新、重装、验证 Cognee，或为 Cognee 选择 Python extras / 本地虚拟环境 / 用户级安装方式时使用本 Skill。

典型触发词：

- "install Cognee"
- "安装 cognee"
- "update Cognee"
- "给这个项目装 cognee[postgres]"
- "验证 cognee-cli 是否可用"
- `/ost-topoteretes-cognee-install`

## 适用客户端

| 客户端 | 支持状态 |
|--------|----------|
| Claude Code | 优先支持；可直接运行支持包脚本 |
| Codex CLI | 优先支持；可直接运行支持包脚本 |
| Copilot CLI | 可用；需当前环境能发现并读取本 Skill |

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) — 安装方式、平台限制、验证命令和 Docker / UI 注意事项
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) — 一键安装脚本、参数、平台检测和验证逻辑
3. [`../../.ost-refs/`](../../.ost-refs/) 目录（如存在）— 本地约定和缓存事实

## Pre-checks

从对话上下文、当前工作目录和用户给出的参数中确认：

| 信息 | 默认值 | 说明 |
|------|--------|------|
| 操作系统 | 当前 shell 平台 | 脚本支持 macOS、Linux、WSL；Windows 走兜底路径 |
| 安装位置 | `--location=local` | 默认在当前项目创建或复用虚拟环境 |
| 虚拟环境目录 | `.venv` | 仅 `--location=local` 时使用 |
| Python 版本 | 当前 `python3` 或 `python` | Cognee 需要 Python 3.10 到 3.14 |
| extras | 空 | 逗号分隔，例如 `ollama`、`postgres,neo4j,aws` |
| 包管理器 | `--manager=auto` | 优先用 `uv`，不可用时回退到 `python -m pip` |
| LLM 配置 | 不自动创建 | 默认 OpenAI 路径需要用户自行设置 `LLM_API_KEY` |

不要替用户自动创建或修改真实 `.env`、Docker Compose、Claude、Agent、MCP 或全局配置文件。若需要这些配置，先展示建议内容并让用户确认。

## Procedure

### 主路径：运行一键脚本（macOS / Linux / WSL）

从支持包根目录（本 `SKILL.md` 向上两级）执行：

```sh
sh scripts_for_install/install.sh [flags] [TARGET_DIR]
```

常用示例：

```sh
sh scripts_for_install/install.sh /path/to/project
sh scripts_for_install/install.sh --dry-run /path/to/project
sh scripts_for_install/install.sh --extras=ollama /path/to/project
sh scripts_for_install/install.sh --extras=postgres,neo4j,aws /path/to/project
sh scripts_for_install/install.sh --location=global --manager=pip
sh scripts_for_install/install.sh --location=local --venv-dir=.venv --manager=uv
```

脚本会执行这些安装 / 更新动作：

- 检测 macOS、Linux 或 WSL；其他平台直接退出并提示 Windows 手动命令
- 查找 Python 并验证版本为 3.10 到 3.14
- 按 `--location=local` 创建或复用虚拟环境，或按 `--location=global` 使用 `pip --user`
- 构造 `cognee` 或 `cognee[extra1,extra2]` 包规格
- 安装或升级 Cognee
- 验证 `import cognee`，并检查 `cognee-cli`

### 常见参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--location=local` | 是 | 在项目虚拟环境中安装或更新 Cognee |
| `--location=global` | 否 | 使用当前 Python 的 `pip --user` 安装或更新 |
| `--venv-dir=PATH` | `.venv` | 指定本地虚拟环境目录 |
| `--extras=LIST` | 空 | 安装 Cognee extras，逗号分隔；脚本允许字母、数字、下划线、连字符和逗号 |
| `--manager=auto` | 是 | 优先选择 `uv`，否则使用 `python -m pip` |
| `--manager=uv` | 否 | 要求使用 `uv`；未安装时脚本失败 |
| `--manager=pip` | 否 | 强制使用 `python -m pip` |
| `--dry-run` | 否 | 只打印计划，不安装、不修改环境 |
| `--help` / `-h` | 否 | 显示脚本帮助 |

常见 extras 组合来自本支持包摘要：

| 用途 | 参数示例 |
|------|----------|
| Ollama 本地模型 | `--extras=ollama` |
| Anthropic Claude models | `--extras=anthropic` |
| PostgreSQL 后端 | `--extras=postgres` |
| Neo4j + AWS S3 | `--extras=neo4j,aws` |
| Code graph analysis | `--extras=codegraph` |
| Web scraping + 文档格式 | `--extras=scraping,docs` |
| OpenTelemetry tracing | `--extras=tracing` |

### 兜底路径：参考 repo_readme_summary.md

遇到以下情况时，转为按 `repo_readme_summary.md` **第 2 部分（安装与更新）** 逐步执行：

- 用户平台是 Windows PowerShell 或 Windows Command Prompt
- 脚本平台检测失败，或用户明确要求手动执行
- 用户需要 Docker Compose、预构建 Docker 镜像、MCP server 源码运行、本地 UI 或特定 provider 的完整手动配置
- 脚本因 Python、`uv`、PATH、权限或网络问题失败，且用户希望绕过脚本逐条排查

兜底执行时，不要直接写入用户真实配置。需要 `.env`、Docker、MCP、Claude 或 Agent 配置时，先把建议内容展示给用户确认，再按用户确认执行。

### 验证

主路径脚本会自动执行基础验证。手动验证可用：

```sh
python -c 'import cognee; print("Cognee import OK:", cognee.__file__)'
cognee-cli remember "Cognee turns documents into AI memory."
cognee-cli recall "What does Cognee do?"
```

本地虚拟环境默认路径可用：

```sh
. .venv/bin/activate
python -c 'import cognee; print("Cognee import OK:", cognee.__file__)'
.venv/bin/cognee-cli remember "Cognee turns documents into AI memory."
.venv/bin/cognee-cli recall "What does Cognee do?"
```

本地 UI 需要 Docker 可用，然后再运行：

```sh
cognee-cli -ui
```

## 安装完成后告知用户

```text
Cognee 已安装或更新。若使用默认 OpenAI 路径，请在自己的 shell 或项目配置中设置 LLM_API_KEY，然后运行 cognee-cli remember / recall 做一次端到端检查。
本 Skill 未自动创建或修改 .env、Docker、Claude、Agent 或 MCP 配置。
需要本地 UI 时，请先确认 Docker 正在运行，再执行 cognee-cli -ui。
```

## Troubleshooting

| 现象 | 原因 | 处理 |
|------|------|------|
| 脚本提示平台不支持 | 当前 shell 不是 macOS、Linux 或 WSL | Windows 用户按 `repo_readme_summary.md` 第 2 部分的 PowerShell / CMD 命令手动安装 |
| Python 版本错误 | Cognee 要求 Python 3.10 到 3.14 | 切换符合版本的 Python 后重跑脚本 |
| `--manager=uv` 失败 | `uv` 不在 PATH | 先安装 `uv`，或改用 `--manager=pip` |
| `cognee-cli` 不在 PATH | 用户级安装的 bin 目录未加入 PATH，或当前 shell 未刷新 | 使用本地虚拟环境路径运行，或把 Python user base bin 加入 PATH 后重新打开 shell |
| `cognee-cli -ui` 失败 | 本地 UI 需要 Docker / OCI runtime | 启动 Docker Desktop、Colima 或其他 runtime 后重试 |
| `remember` / `recall` 报 provider 或 key 错误 | 未设置 `LLM_API_KEY` 或 provider 环境变量不完整 | 按 `repo_readme_summary.md` 第 2 部分配置 OpenAI、Gemini、Ollama 或其他 provider |
| extras 名称被脚本拒绝 | `--extras` 含空格或特殊字符 | 使用逗号分隔，例如 `--extras=postgres,neo4j,aws` |
