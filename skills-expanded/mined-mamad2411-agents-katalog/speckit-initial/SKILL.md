---
name: speckit-initial
description: Run `specify init` in the current or target directory to bootstrap a Spec Kit project (pull .specify/ and slash commands); supports multiple AI agents and --script sh/ps. Use when the user says "initialize Spec Kit project", "specify init", or "set up Spec Kit in this repo".
---

# Spec Kit Initial Skill

Run **specify init** to initialize a Spec Kit project: pull `.specify/` (memory, scripts, templates, specs) and register `/speckit.*` slash commands with the chosen AI Agent. This skill assumes the Specify CLI is already installed; if not, direct the user to **speckit-install** first.

## When to Use

- First time enabling Spec Kit in a project ("initialize Spec Kit", "set up Spec Kit here").
- Switching AI Agent (e.g. from Claude to Cursor or Gemini).
- Initializing in a new or existing directory.
- Need PowerShell scripts on Windows (`--script ps`).

## Prerequisites

- **Specify CLI** installed (see **speckit-install**). If `specify` is not in PATH, guide the user to run **speckit-install** before proceeding.
- **Git** (optional; use `--no-git` if the project is not a git repo or you want to skip git-related setup).

## Workflow

1. **Verify CLI**
   - If the user reports "specify command not found" or has not installed the CLI, direct them to **speckit-install** first. Otherwise proceed.

2. **Choose parameters**
   - **--ai** (required for slash commands): `claude` | `cursor-agent` | `gemini` | `copilot` | `windsurf` | `qwen` | `opencode` | `codex` | `qoder` | `amp` | `shai` | `bob` | `kilocode` | `auggie` | `roo` | `codebuddy` — pick the agent the user will use in this project.
   - **--script**: `sh` (default, Bash) or `ps` (PowerShell). Use `ps` on Windows when the user needs PowerShell scripts.
   - **Target**: `specify init .` or `specify init --here` for current directory; or `specify init <project_name>` for a new subdirectory.
   - **--force**: Overwrite existing `.specify/` if present (use with care).
   - **--no-git**: Skip git-related setup.
   - **--ignore-agent-tools**: Do not install or check agent-specific tools; only pull templates and `.specify/` structure.
   - **--github-token** or `GITHUB_TOKEN`: For private repos or rate-limited access.

3. **Run the command**
   - Give a concrete command for the user's OS and chosen agent. Examples:
     - Current dir, Cursor: `specify init . --ai cursor-agent`
     - Current dir, Claude: `specify init . --ai claude`
     - Windows, Copilot, PowerShell scripts: `specify init . --ai copilot --script ps`
     - New subdir: `specify init my-app --ai gemini`

4. **Confirm outputs**
   - After success: project contains `.specify/` (memory, scripts, templates, specs) and the Agent has `/speckit.*` slash commands available.

## Outputs

- **Project**: `.specify/` directory with memory, scripts, templates, and specs.
- **Agent**: Slash commands (e.g. `/speckit.constitution`, `/speckit.specify`, `/speckit.plan`) available in the chosen AI Agent.

## Next Steps

- Run **speckit-check** to verify the environment (optional but recommended).
- Then use **speckit-constitution** or **speckit-specify** to start the Spec Kit workflow.

## Different Environments

| Environment | Example |
|-------------|---------|
| **Linux / macOS, Cursor** | `specify init . --ai cursor-agent` |
| **Linux / macOS, Claude** | `specify init . --ai claude` |
| **Windows, Copilot, PowerShell** | `specify init . --ai copilot --script ps` |
| **New subdirectory** | `specify init my-project --ai gemini` |
| **Overwrite existing .specify** | `specify init . --ai claude --force` |
| **No git** | `specify init . --ai claude --no-git` |
| **Templates only (no agent tools)** | `specify init . --ai claude --ignore-agent-tools` |

## Troubleshooting

- **"specify: command not found"**: Use **speckit-install** first.
- **Windows slash commands not appearing**: Ensure you used `--script ps` if the agent expects PowerShell, and that the agent is configured to load commands from the project.
- **Private repo / rate limit**: Set `GITHUB_TOKEN` or pass `--github-token <token>` as documented by spec-kit.

## References

- [GitHub spec-kit](https://github.com/github/spec-kit) — Get Started: Initialize your project

## 国内适配

- 支持中文文档和中文注释
- 示例代码兼容国内开发环境
- 提供中文 FAQ 和常见问题解答

## 能力边界

### ✅ 适用场景
- 当你需要使用此技能对应的技术栈时
- 当项目需要遵循最佳实践时
- 当需要快速上手或深入理解核心概念时

### ⚠️ 需要注意
- 复杂业务逻辑需要结合具体场景调整
- 性能优化需要根据实际数据量评估

### ❌ 不适用场景
- 不相关的技术栈或框架
- 需要完全自定义的特殊场景

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
