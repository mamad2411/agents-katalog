---
name: hermes-agent
description: "Use, configure, theme, extend, and orchestrate Hermes Agent."
version: 3.2.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, setup, configuration, multi-agent, spawning, cli, gateway, bots, bot-mode, features, themes, skins, desktop-plugins, tui-widgets, petdex, development]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [claude-code, codex, opencode]
---

# Hermes Agent

Hermes Agent 是 Nous Research 开发的开源 AI 智能体框架，可在终端、原生桌面应用、消息平台以及集成开发环境（IDE）中运行。它与 Claude Code（Anthropic）、Codex（OpenAI）、OpenClaw 属于同一类别——这类自主编码与任务执行型智能体通过调用工具与用户的系统进行交互。Hermes 支持任何大型语言模型提供商（包括 OpenRouter、Anthropic、OpenAI、Google、DeepSeek、xAI 以及本地模型等20多种），并且可在 Linux、macOS、Windows 和 WSL 系统上运行。

Hermes 的独特之处在于：

- **通过技能实现自我提升**——Hermes 能够从经验中学习，将可复用的操作流程保存为技能，并在后续会话中自动加载使用。  
- **跨会话持久记忆**——能够记住用户身份、偏好设置、环境信息以及已获得的经验教训。支持多种可插拔的记忆后端。  
- **多平台接入能力**——同一个智能体可在 Telegram、Discord、Slack、WhatsApp、iMessage、Signal、Matrix、Teams、Email 以及十余种其他平台上运行，不仅能进行聊天，还能完整使用各类工具。  
- **多元交互界面**——同一个智能体核心可驱动 CLI 命令行工具、Ink TUI 图形界面、原生 Electron 桌面应用、网页控制面板，以及适用于 VS Code、Zed、JetBrains 等 IDE 的 ACP 服务器。  
- **与具体提供方解耦**——可在工作流程中进行模型和提供方的切换；凭据池会自动在多个 API 密钥之间轮换。  
- **独立配置文件**——可运行多个独立的 Hermes 实例，每个实例拥有独立的配置、会话、技能及记忆数据。  
- **高度可扩展与主题定制**——支持插件、MCP 服务器、自定义工具、Webhook 触发器、定时任务调度，以及用于美化各交互界面的主题皮肤、桌面 UI 插件、TUI 小部件和可爱吉祥物。

**该技能为一个核心模块。** 其正文部分涵盖了身份识别、快速入门、智能体创建/编排以及核心约束规则等内容。其他所有信息均存储在参考文件中——**在回答问题前请先加载对应的参考文件**，切勿仅依据正文内容回答细节性问题。

**文档链接：** https://hermes-agent.nousresearch.com/docs/

## 范围与验证

该技能文档仅为简明的操作指南，并非涵盖Hermes所有功能的完整参考资料。若某项功能、命令或设置未在此处或相关参考资料中提及，也请勿因此就认定其不存在。在给出否定答复之前，请务必查阅最新的代码仓库及官方文档。

建议优先核查以下内容（从最易找到的开始）：

- **所有已发布的功能，每项占一行：https://hermes-agent.nousresearch.com/docs/llms.txt**。对于“Hermes能实现X功能吗？”或“如何执行X操作？”这类问题，可从此处开始查询——该文件会对全部文档进行索引，并提供对应答案的页面链接。它会在每次构建时根据文档结构自动生成，因此永远不会落后于产品版本。可以使用`web_extract`命令获取该内容；若无法使用网络工具，则可通过`curl -s https://hermes-agent.nousresearch.com/docs/llms.txt`来获取。完整的文档集合则保存在 `/docs/llms-full.txt` 文件中。
- CLI命令：`hermes --help`、`hermes <command> --help` 以及 `hermes_cli/main.py`
- 源代码仓库：https://github.com/NousResearch/hermes-agent

切勿凭记忆就断言“Hermes无法实现某功能”。实际上，Hermes的功能远不止本技能文档所描述的那样，而该索引的存在也便于随时验证否定答复的准确性。

## 快速入门

```bash
# Install (shell installer — sets up uv, Python, the venv, and the launcher)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Interactive chat (default surface; set display.interface: tui to launch the Ink TUI instead)
hermes

# Single query
hermes chat -q "What is the capital of France?"

# Setup wizard  /  pick model+provider  /  health check
hermes setup
hermes model
hermes doctor

# Other surfaces
hermes desktop                 # launch the native desktop app (alias: hermes gui)
hermes dashboard               # web admin panel + embedded chat
hermes proxy                   # OpenAI-compatible local proxy backed by your OAuth provider
```

## 核心路径

```
~/.hermes/config.yaml       Main configuration (settings — never secrets)
~/.hermes/.env              API keys and secrets ONLY (under $HERMES_HOME if set)
$HERMES_HOME/skills/        Installed skills
~/.hermes/skins/            Custom themes (see references/themes.md)
~/.hermes/desktop-plugins/  Desktop app UI plugins (see references/desktop-plugins.md)
~/.hermes/tui-widgets/      TUI widget apps (see references/tui-widgets.md)
~/.hermes/pets/             Installed pet mascots (see references/petdex.md)
~/.hermes/state.db          Canonical session store (SQLite + FTS5)
~/.hermes/sessions/         Gateway routing index, request dumps, *.jsonl transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

配置文件的路径采用 `~/.hermes/profiles/<名称>/` 的格式，结构保持一致。当某个配置文件处于激活状态时，应从 `$HERMES_HOME` 变量中获取实际的主目录路径——切勿直接硬编码 `~/.hermes`。 

## 路由表——加载任务对应的参考信息

| User wants... | Load |
|---|---|
| **Anything not listed below — "can Hermes do X?", "how do I set up X?"** | **https://hermes-agent.nousresearch.com/docs/llms.txt** |
| Bots that chat, run routines, or message each other; the Bots tab | docs: `/user-guide/bot-mode` |
| CLI commands, subcommands, flags, "how do I run X" | `references/cli-reference.md` |
| In-session slash commands | `references/slash-commands.md` |
| Provider setup, API keys, OAuth | `references/providers-and-models.md` |
| config.yaml sections, toolsets, voice/STT/TTS | `references/configuration.md` |
| AGENTS.md / .hermes.md / CLAUDE.md project rules | `references/project-context-files.md` |
| Secret redaction, PII, approval modes, "reset permissions" | `references/security-privacy.md` |
| Delegation, cron, curator, kanban | `references/background-systems.md` |
| MCP servers (add, catalog, `hermes mcp`) | `references/native-mcp.md` |
| Webhook routes and event-driven runs | `references/webhooks.md` |
| A custom theme/skin ("synthwave theme", "change the gold ●") | `references/themes.md` + `templates/skin.yaml` |
| A desktop app UI element (pane, widget, ⌘K command, page) | `references/desktop-plugins.md` + `templates/plugin.js` |
| A live TUI panel or modal widget (ticker, clock, dashboard) | `references/tui-widgets.md` + `templates/clock.mjs` |
| Pet mascots — install, select, scale, diagnose | `references/petdex.md` |
| Windows-specific issues (keybinds, WinError 10106, BOM) | `references/windows-quirks.md` |
| Debugging: voice, tools missing, gateway, aux models | `references/troubleshooting.md` |
| Contributing code: adding tools, slash commands, tests | `references/contributor-guide.md` |
| delegate_task "capped at N" reports | `references/delegate-task-concurrency-diagnosis.md` |
| "Can app X use my Nous Portal subscription/OAuth?" | `references/portal-auth-for-third-party-apps.md` |
| Connecting a messaging platform (Telegram, Discord, Slack, WhatsApp, …) | docs: `/user-guide/messaging` |

上述参考列表并非功能清单——它仅列出了那些需要更详细文档说明的主题。对于Hermes已提供的其他所有功能，只需查看`llms.txt`文件，该文件会将查询内容与对应的解答页面关联起来。

即便不加载参考列表，也有两条主题设置规则始终适用：**用户需自行应用皮肤样式**（使用命令`hermes config set display.skin <名称>`——所有界面都会在约一秒内实时更新；无需告知用户运行 `/skin` 命令）；以及**如需调整某颜色，需直接编辑当前激活的皮肤样式**（使用命令`hermes skin set <键值> <十六进制颜色值>`）——切勿修改`default`皮肤，因为这会清除色彩方案并重置背景。

## 启动额外的Hermes实例

可以将多个Hermes进程作为完全独立的子进程来运行——即拥有独立的会话、工具和环境。

### 何时使用此方法而非delegate_task

| | `delegate_task` | 启动独立`hermes`进程 |
|-|-----------------|--------------------------|
| 隔离性 | 独立对话，共享同一进程 | 完全独立的进程 |
| 运行时长 | 几分钟（受父进程循环限制） | 数小时/数天 |
| 工具访问权限 | 仅能使用父进程的部分工具 | 可使用所有工具 |
| 交互性 | 不支持 | 支持（PTY模式） |
| 适用场景 | 快速处理的并行子任务 | 长时间运行的自主任务 |

### 单次执行模式

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

# Background for long tasks:
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

### 交互式 PTY 模式（通过 tmux 实现）

Hermes 使用 prompt_toolkit 库，该库需要真实的终端环境。建议使用 tmux 来实现交互式进程启动：

```
# Start
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

# Wait for startup, then send a message
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

# Read output
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

# Send follow-up
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

# Exit
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### 多智能体协同

```
# Agent A: backend
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

# Agent B: frontend
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

# Check progress, relay context between them
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

### 会话恢复

```
# Resume most recent session
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

# Resume specific session
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

### 小贴士

- **处理快速子任务时优先使用 `delegate_task`**——相比启动完整进程，其开销更小
- **在启动用于编辑代码的 Agent 时使用 `-w`（工作树模式）**——可避免 Git 冲突
- **为一次性模式设置超时时间**——复杂任务可能需要 5-10 分钟才能完成
- **如需“发完即忘”的操作，可使用 `hermes chat -q`**——无需伪终端
- **交互式会话建议使用 tmux**——原始伪终端模式会导致 prompt_toolkit 出现 `\r` 与 `\n` 的兼容问题
- **对于定时任务**，建议使用 `cronjob` 工具而非直接启动 Agent——它能自动处理任务交付与重试机制
- **出现“`delegate_task` 的并发数已达上限”提示时**——请参阅 `references/delegate-task-concurrency-diagnosis.md`。Hermes 实际存在三种上限限制机制；若均未触发，则说明是模型自身限定了处理能力，并将其归因于“运行时上限”
- **关于“` $external_app` 能否使用我的 Nous Portal 订阅/OAuth 访问权限？”的疑问**——请参阅 `references/portal-auth-for-third-party-apps.md`。该文档会向用户详细讲解三层授权机制（插件与应用的区别、Portal 实际提供的接口功能，以及本地代理选项）

## Surfaces（快速入门）

- **桌面应用**（`hermes desktop` / `hermes gui`）——专为 macOS/Linux/Windows 系统开发的原生 Electron 应用：支持流式聊天、会话列表展示、Cmd+K 快捷调色板、文件拖放功能、原生通知，以及针对不同配置文件的远程网关登录功能。可通过 UI 插件对其进行扩展——详情参见 `references/desktop-plugins.md`。
- **Web 控制面板**（`hermes dashboard`）——功能完备的管理员面板：涵盖消息频道管理、MCP 服务目录、Webhook 配置、内存管理、配置文件构建工具，同时还内置了 `hermes --tui` 聊天界面。该面板通过 OAuth/令牌机制进行安全保护。
- **Ink TUI**（`hermes --tui` 或 `display.interface: tui`）——基于终端的 UI，配有可固定在侧边栏的插件应用——详情参见 `references/tui-widgets.md`。
- **兼容 OpenAI 的代理**（`hermes proxy`）——基于本地 OpenAI API 构建，其授权机制由您当前登录的 OAuth 提供商决定。您可以将 Codex CLI、Aider、Cline 或任何脚本指向该代理使用，无需额外 API 密钥。

## 不可违背的硬性规则（无论加载了何种功能，均不得违反）

- **严禁破坏提示词缓存**——在对话过程中不得更改历史上下文、工具集或系统提示词。唯一例外是上下文压缩操作。
- **消息角色必须交替**——禁止连续出现两条助手消息或两条用户消息；仅 `tool` 操作的结果可以重复出现。
- **敏感信息存放在 `.env` 文件中，配置项存放在 `config.yaml` 中**——切勿要求用户在 `.env` 文件中存放非凭据类配置。
- **使用与配置文件兼容的路径**——在代码中应使用 `get_hermes_home()` 函数获取路径，在会话中解析路径时则使用 `$HERMES_HOME` 变量。
- **严禁直接为用户手动编辑 `config.yaml` 文件**——应使用 `hermes config set KEY VAL` 命令进行配置修改；哪怕是微小的缩进错误都可能破坏文件结构，进而导致实时网关失效。
