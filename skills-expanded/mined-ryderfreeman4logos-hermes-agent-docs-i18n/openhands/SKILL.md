---
name: openhands
description: Delegate coding to OpenHands CLI (model-agnostic, LiteLLM).
version: 0.1.0
author: Tim Koepsel (xzessmedia), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Coding-Agent, OpenHands, Model-Agnostic, LiteLLM]
    related_skills: [claude-code, codex, opencode, hermes-agent]
---

# OpenHands CLI

可通过 `terminal` 工具将编程任务委托给 [OpenHands CLI](https://github.com/All-Hands-AI/OpenHands)。OpenHands 不依赖特定模型，任何支持 LiteLLM 的服务提供商（如 OpenAI、Anthropic、OpenRouter、DeepSeek、Ollama、vLLM 等）均可使用。

该技能为批量/单次任务委托提供的无界面模式封装，Hermes 不会使用交互式文本界面。

## 适用场景

- 用户希望将编程任务专门委托给 OpenHands 处理。
- 用户需要能够在非 Anthropic/非 OpenAI 的服务提供商（如 DeepSeek、Qwen、Ollama、vLLM、Nous 等）上运行的编程智能体——而兄弟技能 `claude-code` 和 `codex` 仅适用于单一供应商的服务。
- 需要在工作空间内进行多步骤文件编辑并配合 shell 命令的操作。

对于基于 Claude 的系统，建议使用 `claude-code`；对于基于 OpenAI 的系统，建议使用 `codex`；对于基于 Hermes 的子智能体，则可使用 `delegate_task`。

## 先决条件

1. 需先安装上游工具（要求 Python 3.12 及以上版本以及 `uv` 工具）：

   ```
   terminal(command="uv tool install openhands --python 3.12")
   ```

验证方式：运行 `openhands --version`（撰写本文时当前版本为 `OpenHands CLI 1.16.0` / `SDK v1.21.0`）。 

2. 选择模型，并为 `--override-with-envs` 参数设置环境变量：

   ```
   export LLM_MODEL=openrouter/openai/gpt-4o-mini       # or any LiteLLM slug
   export LLM_API_KEY=$OPENROUTER_API_KEY
   export LLM_BASE_URL=https://openrouter.ai/api/v1     # omit for native OpenAI
   ```

`LLM_MODEL` 参数应使用 LiteLLM 的完整标识符。当提供商为 OpenRouter 时，该标识符需添加双重前缀，格式为 `openrouter/<供应商>/<模型>`（例如 `openrouter/anthropic/claude-sonnet-4.5`）。对于原生 Anthropic 模型，格式为 `anthropic/claude-sonnet-4-5`；而对于原生 OpenAI 模型，则为 `openai/gpt-4o-mini`。

3. 如需隐藏启动横幅，避免 JSON 输出前出现 ASCII 艺术图案，可进行相应设置：

   ```
   export OPENHANDS_SUPPRESS_BANNER=1
   ```

## 如何运行

请始终通过 `terminal` 工具来调用该代理。在进行自动化操作时，务必添加 `--headless --json --override-with-envs --exit-without-confirmation` 参数。

### 单次任务

```
terminal(
  command="OPENHANDS_SUPPRESS_BANNER=1 LLM_MODEL=openrouter/openai/gpt-4o-mini LLM_API_KEY=$OPENROUTER_API_KEY LLM_BASE_URL=https://openrouter.ai/api/v1 openhands --headless --json --override-with-envs --exit-without-confirmation -t 'Add error handling to all API calls in src/'",
  workdir="/path/to/project",
  timeout=600
)
```

### 长时间任务的运行背景

```
terminal(command="<same as above>", workdir="/path/to/project", background=true, notify_on_complete=true)
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
```

### 恢复之前的对话

每次运行结束后，OpenHands 会输出 `Conversation ID: <32位十六进制字符串>` 以及一行提示信息 `Hint: openhands --resume <带连字符的UUID>`。请使用该带连字符格式的 UUID 来恢复对话：

```
terminal(
  command="OPENHANDS_SUPPRESS_BANNER=1 LLM_MODEL=... openhands --headless --json --override-with-envs --exit-without-confirmation --resume <dashed-uuid> -t 'Now fix the bug you found'",
  workdir="/path/to/project"
)
```

## 实际可用参数列表

已通过 `openhands --help`（CLI 1.16.0 版本）进行验证。表中未列出的参数均不属于有效参数——需通过环境变量或配置文件传递。

| 参数 | 效果 |
|------|------|
| `--headless` | 禁用用户界面，必须搭配 `-t` 或 `-f` 使用。该模式下会自动批准所有操作（无需 `--llm-approve`）。 |
| `--json` | 以 JSONL 格式输出事件流（需配合 `--headless` 使用）。 |
| `-t TEXT` | 任务提示语。 |
| `-f PATH` | 从文件中读取任务内容。 |
| `--resume [ID]` | 恢复对话。未指定 ID 时将列出最近的对话记录。 |
| `--last` | 恢复最近的一次对话（需配合 `--resume` 使用）。 |
| `--override-with-envs` | 使用 `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` 环境变量覆盖默认值。若未设置此参数，OpenHands 将读取 `~/.openhands/settings.json` 并忽略环境变量设置。 |
| `--exit-without-confirmation` | 不显示“确定要退出吗？”的确认对话框。 |
| `--always-approve` / `--yolo` | 自动批准所有操作（`--headless` 模式下的默认行为）。 |
| `--llm-approve` | 基于大语言模型的安全审核机制（仅支持交互模式，无界面模式下无效）。 |
| `--version` / `-v` | 显示版本信息后退出。 |

**不存在 `--model`、`--max-iterations`、`--workspace`、`--sandbox`、`--sandbox-type` 等参数。** 模型参数为 `LLM_MODEL`；工作目录即为传递给 `terminal` 工具的 `workdir` 参数；沙箱/运行环境则由 `RUNTIME` 和 `SANDBOX_VOLUMES` 环境变量控制。

## JSON 事件结构规范

当使用 `--json --headless` 选项时，OpenHands 会以 JSONL 格式输出数据——每行一个 JSON 对象，此外还会有一些非 JSON 格式的状态行（如 `Initializing agent...`、`Agent is working`、`Agent finished`、最终总结框、`Goodbye!`、`Conversation ID:`、`Hint:` 等）。可通过筛选以 `{` 开头的行来获取有效数据。

顶层 `kind` 字段用于区分不同类型的事件：

- `MessageEvent`：表示用户或智能体的文本轮次，`source` 字段的值为 `user` 或 `agent`。
- `ActionEvent`：表示智能体选择了某个工具，可查看 `tool_name`（如 `file_editor`、`terminal`、`finish`）以及 `action.kind`（如 `FileEditorAction`、`TerminalAction`、`FinishAction`）。
- `ObservationEvent`：表示工具的执行结果，`observation.is_error` 字段用于标识操作是否成功，`source` 字段的值为 `environment`。
- `ActionEvent` 中的 `FinishAction` 字段包含智能体的最终消息，存储在 `action.message` 中。

CLI 会首先输出 LiteLLM 和 Authlib 产生的所有标准错误信息——详情请参见“注意事项”部分。建议仅解析标准输出内容，并忽略那些不以 `{` 开头的行。

## 注意事项

- **每次调用都会出现 LiteLLM 警告信息。** 由于未安装 `botocore`，CLI 会将 `bedrock-runtime` 和 `sagemaker-runtime` 相关的警告信息输出到标准错误流中；此外还会出现 Authlib 的弃用警告。这些均为冗余信息，并非故障。可通过将标准错误流重定向至 `/dev/null` 或在展示给用户之前过滤掉这些信息。
- **横幅广告干扰。** 若未设置 `OPENHANDS_SUPPRESS_BANNER=1`，每次运行都会以多行的 `+--+` ASCII 横幅形式展示 SDK 广告。建议始终设置该环境变量以屏蔽广告。
- **自动化场景必须使用 `--override-with-envs` 参数。** 若未设置此参数，OpenHands 会忽略 `LLM_API_KEY`、`LLM_BASE_URL` 和 `LLM_MODEL` 等环境变量，转而使用 `~/.openhands/settings.json` 中的默认值。在全新安装的情况下，该文件并不存在，CLI 会因此挂起并等待首次运行设置完成。
- **模型标识符为 LiteLLM 的内部格式，而非服务提供商的格式。** `openrouter/openai/gpt-4o-mini` 可正常使用；而虽指向 OpenRouter 但格式为 `openai/gpt-4o-mini` 的模型则无法使用。`anthropic/claude-sonnet-4-5`（含连字符）为 Anthropic 官方提供的模型；`openrouter/anthropic/claude-sonnet-4.5`（含点号）则是通过 OpenRouter 访问的模型。若格式错误，将会出现含义不明的 LiteLLM 400 错误。
- **`pip install openhands-ai` 是错误的安装命令。** 那是旧版的 V0 SDK。新版 CLI 的正确安装命令为 `uv tool install openhands --python 3.12`。目前暂无维护中的 conda 版本可供安装。
- **对话恢复 ID 的格式较为特殊。** CLI 先输出 `Conversation ID: f46573d9cfdb45e492ca189bde40019b`（不含连字符），随后再输出 `Hint: openhands --resume f46573d9-cfdb-45e4-92ca-189bde40019b`（含连字符）。请务必使用带连字符的格式。
- **无界面模式会忽略 `--llm-approve` 参数。** 若尝试传递该参数，将会出现 argparse 相关错误。无界面模式默认始终自动批准所有操作。
- **上游版本不支持 Windows 系统。** OpenHands 的官方文档要求在 Windows 上使用 WSL 环境，因此该功能被限制在 `[linux, macos]` 平台上使用。
- **`~/.openhands/conversations/<id>/` 目录会持续积累数据。** 每次运行都会在该目录下保存对话轨迹。若需批量处理任务，请及时清理该目录中的旧数据。
- **安装包体积较大（约 200 个依赖包）。** 建议使用 `uv tool install` 命令在隔离的虚拟环境中进行安装，以避免与当前项目存在依赖冲突。

## 验证方法

```
terminal(
  command="OPENHANDS_SUPPRESS_BANNER=1 LLM_MODEL=openrouter/openai/gpt-4o-mini LLM_API_KEY=$OPENROUTER_API_KEY LLM_BASE_URL=https://openrouter.ai/api/v1 openhands --headless --json --override-with-envs --exit-without-confirmation -t 'Print the string OPENHANDS_OK to stdout via the terminal tool.'",
  workdir="/tmp",
  timeout=120
)
```

如果 JSONL 数据流的末尾是一个 `FinishAction`，且其 `action.message` 中包含 `OPENHANDS_OK` 字样，则说明安装过程已成功完成。

## 相关资源

- [OpenHands GitHub 仓库](https://github.com/All-Hands-AI/OpenHands)
- [OpenHands CLI 命令参考手册](https://docs.openhands.dev/openhands/usage/cli/command-reference)
- 相关技能：`claude-code`（仅支持 Anthropic）、`codex`（仅支持 OpenAI）、`opencode`（通过 OpenCode 支持多提供商）、`hermes-agent`（通过 `delegate_task` 实现的 Hermes 子智能体）。
