---
name: antigravity-cli
description: "Operate the Antigravity CLI (agy): plugins, auth, sandbox."
version: 0.2.0
author: Tony Simons (asimons81), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Antigravity, CLI, Auth, Plugins, Sandbox]
    related_skills: [grok, codex, claude-code, hermes-agent]
---

# Antigravity CLI（`agy`）

Antigravity CLI 的操作指南，该工具的调用方式为 `agy`。所有 `agy` 命令均需通过 Hermes 的 `terminal` 工具执行；可使用 `read_file` 命令查看其配置文件与日志。该技能属于参考型加流程指导类——它并不封装任何网络 API，因此 Hermes 本身无需进行任何身份验证。

## 适用场景

- 安装、更新或对 `agy` 可执行文件进行功能测试  
- 执行非交互式的 `agy --print` / `agy -p` 单次命令  
- 调试 Antigravity 的身份认证、沙箱机制、权限设置或插件状态  
- 查看 Antigravity 的配置项、快捷键设置、对话记录或日志文件  

## 思维模型

Antigravity 具有两层结构——需明确区分这两层，否则指导信息将会出错：

1. **Shell 包装命令** — 如 `agy help`、`agy install`、`agy plugin`、`agy update`、`agy changelog`。这类命令需通过 `terminal` 工具执行。  
2. **交互式会话中的斜杠命令** — 如 `/config`、 `/permissions`、 `/skills`、 `/agents` 等。这类命令仅存在于正在运行的 `agy` 图形用户界面会话中，而非 Shell 包装层。

`agy help` 显示的是 Shell 包装层的命令列表，而非会话中的斜杠命令。

## 先决条件

- PATH 环境变量中已包含 `agy` 可执行文件。可通过 `terminal` 工具进行验证：
  `command -v agy && agy --version`。
- 该技能无需任何环境变量或 API 密钥——Antigravity 通过操作系统密钥管理器或浏览器登录机制自行处理身份认证（详见下文“身份认证”部分）。

## 执行方法

所有 `agy` 命令均需通过 `terminal` 工具来执行。示例如下：

```
terminal(command="agy --version")
terminal(command="agy help")
terminal(command="agy plugin list")
terminal(command="agy --print 'Summarize the repo in 3 bullets'", workdir="/path/to/project")
```

若需进行交互式的多轮文本用户界面对话，可像 `codex` / `claude-code` 技能那样，使用 `pty=true` 参数启动 `agy`（同时配合 `tmux` 用于捕获或监控）。而对于一次性功能测试或基于脚本的提问，则建议使用非交互模式的 `agy --print`。

若要查看 Antigravity 自身的文件，请使用下方“核心路径”中的路径调用 `read_file` 函数——切勿通过终端直接使用 `cat` 命令查看。

## 委派模式

`agy` 与 `codex` / `claude-code` 同属一类编程智能体后端，因此适用相同的委派模式。在需要将实际任务（如功能开发、缺陷修复、代码审查或第二意见征求）交给 Antigravity 处理时，即可采用这些模式，而不仅仅是进行简单的功能测试。

### 一次性模式（适用于基于脚本的提问及获取第二意见）

```
terminal(command="agy -p 'Review this diff for bugs and security issues' --model 'Gemini 3.1 Pro (High)'", workdir="/path/to/repo", timeout=300)
```

`-p` 模式为非交互式：它会显示提示语后立即退出。可通过 `--model` 选项选择模型（运行 `agy models` 可查看具体的显示字符串，例如 `'Gemini 3.1 Pro (High)'`、`'Claude Opus 4.6 (Thinking)'`）。若需添加额外的上下文路径，可使用可重复使用的 `--add-dir` 选项。

### 长时间/有时间限制的运行（测试、构建、多文件修改）

可与 `codex` 技能相同，先在后台启动任务并在完成后发送通知：

```
terminal(command="agy -p 'Implement the change described in TASK.md and run the tests' --dangerously-skip-permissions", workdir="/path/to/repo", background=true, notify_on_complete=true)
# then: process(action="poll"/"log"/"wait", session_id=<id>)
```

### 交互式多轮对话（PTY + tmux）

对于需要多轮对话的场景，可在 `pty=true` 的条件下运行 `agy -i`（或直接运行 `agy`），并结合 tmux 的 `capture-pane`/`send-keys` 功能使用，其用法与 `codex`/`claude-code` 技能文档中描述的完全一致。之后可通过 `--continue`/-c 或指定的 `--conversation <id>` 参数继续对话。

### 并行实例（批量子任务/工作树扩展模式）

为每个任务创建一个 Git 工作树，并在每个工作树下独立启动一个后台运行的 `agy -p` 实例，随后再汇总结果——这与 `codex` 技能用于批量处理问题时的工作树扩展模式相同。请根据机器性能及自身的审核能力来控制并发数量。

### 输出格式及相关限制（与 Claude Code 不同）

- `agy -p` 仅返回**纯文本**——不存在 `--output-format json` 选项，也不会生成包含 `session_id`、成本信息或轮次数的结果封装结构。需直接解析标准输出，无需期望得到 JSON 对象。
- **没有 `--max-turns` 选项**。单次运行的时长由 `--print-timeout`（默认为 5 分钟）来限制。对于耗时较长的任务，可将其值调大，例如设置为 `--print-timeout 20m`。同时建议在终端层面设置 `timeout=` 参数，以避免外部调用提前终止运行。

### 编排调度边界

Antigravity 实际上属于**任务执行后端或第三方审核工具**——其执行细节由负责处理任务的智能体/配置文件掌控，而非一种第一级的编排机制。因此，请勿将 `agy` 作为独立卡片放在看板系统中，也不应将其视为协调层；应通过常规的任务流程进行任务分配，由被指定的执行者自行选择是否使用 `agy`（而非 `codex`/`claude-code` 或其他直接工具）作为处理方法。仅在用户明确要求、某个执行者被配置为使用它，或需要通过 Gemini 系列模型对其他智能体的方案或差异结果进行交叉验证时，才应显式调用它。

## 核心路径

- 可执行文件/入口程序：`agy`
- 应用数据目录：`~/.gemini/antigravity-cli/`
- 配置文件：`~/.gemini/antigravity-cli/settings.json`
- 绑定配置文件：`~/.gemini/antigravity-cli/keybindings.json`
- 日志文件：`~/.gemini/antigravity-cli/log/cli-*.log`
- 对话记录目录：`~/.gemini/antigravity-cli/conversations/`
- 智能体运行相关数据：`~/.gemini/antigravity-cli/brain/`
- 历史记录文件：`~/.gemini/antigravity-cli/history.jsonl`
- 插件暂存目录：`~/.gemini/antigravity-cli/plugins/<plugin_name>/`

## 快速参考

### 包装命令
- `agy changelog`
- `agy help`
- `agy install`
- `agy plugin` / `agy plugins`
- `agy update`

### 有用参数
- `--add-dir`
- `--continue` / `-c`
- `--conversation`
- `--dangerously-skip-permissions`
- `--print` / `-p`
- `--print-timeout`
- `--prompt`
- `--prompt-interactive` / `-i`
- `--sandbox`
- `--log-file`
- `--version`

### 插件子命令（通过 `agy plugin --help` 查看）
- `list`、`import [source]`、`install <target>`、`uninstall <name>`、
  `enable <name>`、`disable <name>`、`validate [path]`、`link <mp> <target>`、
  `help`

### 安装参数（通过 `agy install --help` 查看）
- `--dir`、`--skip-aliases`、`--skip-path`

### 会话内斜杠命令
- **对话控制**：`/resume`（/switch）、`/rewind`（/undo）、
  `/rename <name>`、`/clear`、`/fork`、`/reset`、`/new`
- **设置与工具**：`/config`、`/settings`、`/permissions`、`/model`、
  `/keybindings`、`/statusline`、`/tasks`、`/skills`、`/mcp`、`/open <path>`、
  `/usage`、`/logout`、`/agents`
- **提示词辅助功能**：`@` 可实现路径自动补全；当未处于流式输入模式时，按 `esc esc` 可清除提示词；按 `!` 可直接执行终端命令；按 `?` 可打开帮助文档

## 设置与权限

### 常见设置键（位于 `settings.json` 中）
- `allowNonWorkspaceAccess`
- `colorScheme`
- `permissions.allow`
- `trustedWorkspaces`

### 权限模式
`request-review`、`always-proceed`、`strict`、`proceed-in-sandbox`。

### 沙箱模式行为
- `settings.json` 中的 `enableTerminalSandbox` 为布尔值，默认值为 `false`。
- 启动时的临时参数（如 `--sandbox`、`--dangerously-skip-permissions`）可覆盖当前会话的持久设置。

## 认证机制

- CLI 会首先尝试使用操作系统的安全密钥环进行认证。
- 若未保存任何会话信息，则会回退到基于浏览器的 Google 登录方式。
- 在本地运行时，它会自动打开默认浏览器；通过 SSH 连接时，则会输出授权 URL，等待用户粘贴授权码。
- 使用 `/logout` 命令可删除已保存的认证凭证。

## 插件

- 插件存储在 `~/.gemini/antigravity-cli/plugins/<plugin_name>/` 目录下。
- 这些插件可以集成各种技能、智能体、规则、MCP 服务器及钩子功能。
- 若 `agy plugin list` 命令未显示任何已导入的插件，这也属于正常的空状态。

## 常见问题与注意事项

- `agy help` 显示的是包装命令，而非交互式的斜杠命令。
- `agy --version` 是安全的非交互式版本检查方式；而 `agy version` 为交互式命令，在没有真实终端设备的情况下可能会失败。
- 出现故障时，首先应查看 `~/.gemini/antigravity-cli/log/cli-*.log` 文件（可使用 `read_file` 命令读取）。
- 请勿将持久化的 JSON 配置与启动时的临时参数混淆。
- `~/.gemini/antigravity-cli/bin/agentapi` 实际上是 `agy agentapi` 的简化包装版本。
- 在 WSL 环境下，令牌存储采用文件形式，因此认证问题通常属于本地文件或会话状态问题，而非仅限于浏览器的问题。
- 工作空间身份可能取决于启动目录以及 `.antigravitycli` 项目标识符。
- `agy -p` 仅输出纯文本——不存在 `--output-format json` 选项，也不会生成结果封装结构。请勿尝试从中解析 JSON 对象（这与 `claude-code` 不同）。
- 单次运行的时长由 `--print-timeout`（默认 5 分钟）控制，而非 `--max-turns`（`agy` 中并无该选项）。

## 验证安装状态

可通过 `terminal` 工具确认安装是否成功且可用（可使用 `read_file` 命令读取相关文件）：

1. `terminal(command="command -v agy")`
2. `terminal(command="agy --version")`
3. `terminal(command="agy help")`
4. `terminal(command="agy plugin list")`
5. 读取 `~/.gemini/antigravity-cli/settings.json` 文件
6. 读取最新的 `~/.gemini/antigravity-cli/log/cli-*.log` 日志文件
7. 如有需要，也可读取 `~/.gemini/antigravity-cli/keybindings.json` 文件

## 支持文档

- `references/cli-docs.md` —— 汇集了入门指南、使用说明及功能介绍文档中的核心内容。
