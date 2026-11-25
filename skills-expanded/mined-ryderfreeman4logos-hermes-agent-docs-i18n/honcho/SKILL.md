---
name: honcho
description: Configure and troubleshoot Honcho memory for Hermes.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Honcho, Memory, Profiles, Observation, Dialectic, User-Modeling, Session-Summary]
    homepage: https://docs.honcho.dev
    related_skills: [hermes-agent]
prerequisites:
  pip: [honcho-ai]
---

# Hermes 的 Honcho Memory 功能

Honcho 提供基于人工智能的跨会话用户建模功能。它能够跨多次对话识别用户身份，为每个 Hermes 用户档案赋予独立的对等体标识，同时实现统一的用户视图。

## 适用场景

- 部署 Honcho（云端或自托管）
- 排查记忆功能失效/对等体同步问题
- 构建多档案配置，使每个智能体拥有独立的 Honcho 对等体
- 调整观察范围、回忆能力、对话深度或输出频率等参数
- 了解五种 Honcho 工具的功能及其适用场景
- 配置上下文预算与会话摘要注入功能

## 设置指南

### 云端版本（app.honcho.dev）

```bash
hermes memory setup honcho
# select "cloud", paste API key from https://app.honcho.dev
```

### 自主托管模式

```bash
hermes memory setup honcho
# select "local", enter base URL (e.g. http://localhost:8000)
```

参见：https://docs.honcho.dev/v3/guides/integrations/hermes#running-honcho-locally-with-hermes

### 验证

```bash
hermes honcho status    # shows resolved config, connection test, peer info
```

## 架构设计

### 基础上下文注入

当 Honcho 将上下文注入系统提示词中（在“混合模式”或“上下文检索模式”下），它会按以下顺序构建基础上下文模块：

1. **会话摘要**——当前会话的简短概要（置于最前端，以便模型快速保持对话连贯性）
2. **用户画像**——Honcho 所积累的关于该用户的模型信息（包括偏好、事实及行为模式）
3. **AI 对等体卡片**——该 Hermes 配置下 AI 对等体的身份标识

若存在之前的会话，会话摘要会在每个对话轮次开始时由 Honcho 自动生成。这样无需重新回放完整历史记录，即可让模型快速进入工作状态。

### 冷启动/热启动提示词选择

Honcho 会自动在两种提示词策略之间进行选择：

| 条件 | 策略 | 具体操作 |
|------|------|----------|
| 无先前会话或用户画像为空 | **冷启动** | 使用简短的引导提示词；跳过摘要注入，促使模型主动了解用户 |
| 已存在用户画像和/或会话历史 | **热启动** | 完整注入基础上下文（从摘要到用户画像再到对等体卡片）；生成更丰富的系统提示词 |

无需手动配置此功能——系统会根据会话状态自动选择相应策略。

### 对等体机制

Honcho 将对话视为**对等体**之间的交互。Hermes 会在每个会话中创建两个对等体：

- **用户对等体**（`peerName`）：代表人类用户。Honcho会根据观察到的消息构建该用户的表征。
- **AI对等体**（`aiPeer`）：代表当前的Hermes实例。每个配置文件都会对应一个独立的AI对等体，从而使智能体能够形成各自的独立认知。

### 观察功能

每个对等体都包含两个观察开关，用于控制Honcho从哪些方面获取信息：

| 开关 | 功能说明 |
|------|----------|
| `observeMe` | 观察该对等体自身的消息（用于构建自我表征） |
| `observeOthers` | 观察其他对等体的消息（用于建立跨对等体间的理解） |

默认设置：四个开关均为**开启**状态（实现完全的双向观察）。

可在 `honcho.json` 文件中为每个对等体单独配置这些选项：

```json
{
  "observation": {
    "user": { "observeMe": true, "observeOthers": true },
    "ai":   { "observeMe": true, "observeOthers": true }
  }
}
```

或者使用简写的预设配置：

| 预设值 | 用户 | AI | 适用场景 |
|--------|------|----|----------|
| `"directional"`（默认） | 我：开启，他人：开启 | 我：开启，他人：开启 | 多智能体模式，完整内存访问 |
| `"unified"` | 我：开启，他人：关闭 | 我：关闭，他人：开启 | 单智能体模式，仅用户模型 |

在 [Honcho 控制面板](https://app.honcho.dev) 中进行的设置会在会话启动时同步回来——服务器端配置优先于本地默认设置。

### 会话

会话决定了消息和观测数据存储的范围。可用策略如下：

| 策略 | 行为方式 |
|--------|----------|
| `per-directory`（默认） | 每个工作目录对应一个会话 |
| `per-repo` | 每个 Git 仓库根目录对应一个会话 |
| `per-session` | 每次运行 Hermes 都会创建新的 Honcho 会话 |
| `global` | 所有目录共享同一个会话 |

可手动覆盖配置：`hermes honcho map my-project-name`

### 回忆模式

智能体访问 Honcho 内存的方式：

| 模式 | 是否自动注入上下文？ | 是否提供工具功能？ | 适用场景 |
|------|---------------------|-----------------|----------|
| `hybrid`（默认） | 是 | 是 | 智能体可自行决定是使用工具还是自动上下文 |
| `context` | 是 | 否（隐藏） | 流量消耗极低，无需调用工具 |
| `tools` | 否 | 是 | 智能体可完全自主控制对内存的访问 |

## 三个相互独立的调节参数

Honcho 的辩证行为由三个独立维度控制。分别调整这些参数不会相互影响：

### 频率（何时）

控制辩证逻辑调用和上下文调用的**频率**。

| 键值 | 默认值 | 描述 |
|-----|---------|-------------|
| `contextCadence` | `1` | 每次调用上下文 API 之间的最小轮次间隔 |
| `dialecticCadence` | `2` | 每次调用辩证式 API 之间的最小轮次间隔，推荐值为 1–5 |
| `injectionFrequency` | `every-turn` | 基础上下文注入的频率，可选值为 `every-turn` 或 `first-turn` |

较高的间隔值意味着辩证式大语言模型被调用的频率更低。例如，将 `dialecticCadence` 设置为 `2` 表示引擎每隔一轮才调用一次；而设置为 `1` 则表示每轮都会调用。

### 推理深度（轮数）

用于控制 Honcho 对每个查询执行多少轮辩证式推理。

| 键值 | 默认值 | 范围 | 描述 |
|-----|---------|-------|-------------|
| `dialecticDepth` | `1` | 1-3 | 每个查询的辩证式推理轮数 |
| `dialecticDepthLevels` | -- | 数组 | 可选参数，用于为每一轮单独设置不同的推理层级（见下文） |

当 `dialecticDepth` 设置为 `2` 时，Honcho 会进行两轮辩证式推理。第一轮生成初步答案，第二轮则对答案进行优化。

`dialecticDepthLevels` 允许您分别为每一轮独立设置推理层级：

```json
{
  "dialecticDepth": 3,
  "dialecticDepthLevels": ["low", "medium", "high"]
}
```

如果省略 `dialecticDepthLevels`，则轮次将使用基于 `dialecticReasoningLevel`（即基础值）计算出的**按比例分配的层级**：

| 深度 | 轮次层级 |
|-------|-----------|
| 1 | [基础] |
| 2 | [最小，基础] |
| 3 | [最小，基础，低] |

这种方式能在早期轮次保持较低成本，同时在最终合成阶段使用最大深度。

**会话启动时的深度设置。** 会话启动前的预热阶段会在第1轮之前在后台运行完整配置的 `dialecticDepth`。在对冷启动的合作伙伴进行单轮预热时，通常只能得到较为简略的输出——而多轮深度预温则会在用户发言之前就完成审核/对齐流程。第1轮会直接使用预热结果；如果预热未能及时完成，第1轮则会回退为带有时间限制的同步调用。

### 级别（难度）

用于控制每轮辩证推理的**强度**。

| 键值 | 默认值 | 描述 |
|-----|---------|-----------|
| `dialecticReasoningLevel` | `low` | `minimal`、`low`、`medium`、`high`、`max` |
| `dialecticDynamic` | `true` | 当设置为 `true` 时，模型可将 `reasoning_level` 传递给 `honcho_reasoning`，从而覆盖每次调用的默认设置。`false` 表示始终使用 `dialecticReasoningLevel`，模型设置的覆盖将被忽略 |

更高的级别能生成更丰富的合成结果，但会在 Honcho 后端消耗更多令牌。

## 多配置文件设置

每个 Hermes 配置文件拥有独立的 Honcho AI 对象，同时共享相同的工作空间（用户上下文）。这意味着：

- 所有配置文件均显示相同的用户信息呈现方式  
- 每个配置文件会构建独立的 AI 身份及观测数据  
- 由某个配置文件生成的结论可通过共享工作空间被其他配置文件查看  

### 使用 Honcho 同伴功能创建配置文件

```bash
hermes profile create coder --clone
# creates host block hermes.coder, AI peer "coder", inherits config from default
```

`--clone` 参数在 Honcho 中的作用：
1. 在 `honcho.json` 文件中创建一个 `hermes.coder` 主机配置块；
2. 设置 `aiPeer: "coder"`（即对应的配置文件名称）；
3. 沿用默认值设置 `workspace`、`peerName`、`writeFrequency`、`recallMode` 等参数；
4. 立即在 Honcho 中创建该对应节点，确保在接收第一条消息之前它就已经存在。

### 补充现有配置文件

```bash
hermes honcho sync    # creates host blocks for all profiles that don't have one yet
```

### 每个配置文件的独立设置

可覆盖主机块中的任何设置：

```json
{
  "hosts": {
    "hermes.coder": {
      "aiPeer": "coder",
      "recallMode": "tools",
      "dialecticDepth": 2,
      "observation": {
        "user": { "observeMe": true, "observeOthers": false },
        "ai": { "observeMe": true, "observeOthers": true }
      }
    }
  }
}
```

## 工具

该智能体拥有 5 个双向的 Honcho 工具（在“上下文回溯”模式下会隐藏）：

| 工具 | 是否调用 LLM？ | 成本 | 适用场景 |
|------|--------------|------|----------|
| `honcho_profile` | 否 | 极低 | 在对话开始时快速获取事实概览，或快速查询名称、角色及偏好设置 |
| `honcho_search` | 否 | 低 | 获取特定的历史事实以便自行推理——仅返回原始内容，不进行综合处理 |
| `honcho_context` | 否 | 低 | 获取完整的会话上下文快照：摘要、对方信息展示、卡片内容以及最新消息 |
| `honcho_reasoning` | 是 | 中高 | 由 Honcho 的辩证引擎生成的自然语言问题 |
| `honcho_conclude` | 否 | 极低 | 编写或删除持久性事实；若需 AI 自我认知，可传入 `peer: "ai"` 参数 |

### `honcho_profile`
读取或更新对方信息卡片——其中包含精心整理的关键信息（名称、角色、偏好及沟通风格）。如需更新信息，请传入 `card: [...]` 参数；如仅需读取则无需传入该参数。此操作不会调用 LLM。

### `honcho_search`
在存储的上下文中对特定对象进行语义搜索。返回按相关性排序的原始内容片段，不进行综合处理。默认返回 800 个标记，最多 2000 个。当您需要特定的历史事实以便自行推理而非获取综合答案时，此工具非常有用。

### `honcho_context`
获取来自 Honcho 的完整会话上下文快照——包括会话摘要、对方信息展示、卡片内容以及最新消息。此操作不会调用 LLM。当您希望一次性查看 Honcho 所掌握的关于当前会话及对方的全部信息时，可使用此工具。

### `honcho_reasoning`
通过 Honcho 的辩证推理引擎（在 Honcho 后端调用大型语言模型）来回答自然语言问题。该方式成本较高，但输出质量更优。可通过传递 `reasoning_level` 参数控制推理深度：`minimal`（快速/低成本）→ `low` → `medium` → `high` → `max`（全面深入）。若不指定该参数，则使用默认值 `low`。此功能用于深入理解用户的习惯、目标或当前状态。

### `honcho_conclude`
用于创建或删除关于某个对象的持久性结论。如需创建结论，可传递 `conclusion: "..."` 参数；如需删除结论（尤其是涉及个人身份信息时——Honcho 会逐步自动修正错误的结论，因此仅当涉及敏感信息时才需手动删除），则需传递 `delete_id: "..."` 参数。必须仅选择这两个参数中的一个使用。

### 双向对象定位功能

上述 5 种工具均支持可选的 `peer` 参数：
- `peer: "user"`（默认值）——针对用户对象操作
- `peer: "ai"` ——针对当前配置文件中的 AI 对象操作
- `peer: "<explicit-id>"` ——工作空间中的任意对象 ID

示例：
```
honcho_profile                        # read user's card
honcho_profile peer="ai"              # read AI peer's card
honcho_reasoning query="What does this user care about most?"
honcho_reasoning query="What are my interaction patterns?" peer="ai" reasoning_level="medium"
honcho_conclude conclusion="Prefers terse answers"
honcho_conclude conclusion="I tend to over-explain code" peer="ai"
honcho_conclude delete_id="abc123"    # PII removal
```

## Agent 使用模式

当 Honcho 内存处于激活状态时，Hermes 的使用指南。

### 对话开始时

```
1. honcho_profile                  → fast warmup, no LLM cost
2. If context looks thin → honcho_context  (full snapshot, still no LLM)
3. If deep synthesis needed → honcho_reasoning  (LLM call, use sparingly)
```

请勿在每个对话轮次都调用 `honcho_reasoning` 函数。自动注入机制已能负责持续更新上下文，仅当基础上下文无法提供所需的信息，且确实需要通过推理工具生成综合见解时，才应使用该功能。

### 当用户要求记住某些内容时

```
honcho_conclude conclusion="<specific, actionable fact>"
```

优秀结论示例：“更倾向于使用代码示例而非文字说明”，“截至2026年4月仍在从事Rust异步项目开发”  
较差结论示例：“用户提到了Rust”（过于模糊），“用户似乎具备技术背景”（该信息已在初始描述中体现）

```
honcho_search query="<topic>"       → fast, no LLM, good for specific facts
honcho_context                       → full snapshot with summary + messages
honcho_reasoning query="<question>"  → synthesized answer, use when search isn't enough
```

### 何时使用 `peer: "ai"` 

可使用 AI 对等体功能来构建并查询智能体自身的自我认知：
- `honcho_conclude conclusion="我在解释架构时往往话较多" peer="ai"` —— 自我修正
- `honcho_reasoning query="我通常如何处理含义模糊的请求？" peer="ai"` —— 自我审计
- `honcho_profile peer="ai"` —— 查看自身的身份信息

### 何时不应调用工具 

在 `hybrid` 和 `context` 模式下，基础上下文（用户描述 + 身份卡片 + 会话摘要）会在每一轮对话开始前自动注入。无需重新获取已注入的内容。仅在以下情况才需调用工具：
- 需要注入的上下文中没有所需信息
- 用户明确要求你调取或检查记忆内容
- 需要针对新信息撰写结论时

### 调用频率控制 

在工具端使用 `honcho_reasoning` 的成本与自动注入机制相同。在明确调用工具之后，自动注入的频率会重置——从而避免在同一轮对话中重复计费。

## 配置参考 

配置文件路径：` $HERMES_HOME/honcho.json`（针对特定配置文件）或 `~/.honcho/config.json`（全局配置）。

### 主要设置项

| 键值 | 默认值 | 描述 |
|-----|---------|-------------|
| `apiKey` | -- | API密钥（[获取方式](https://app.honcho.dev)） |
| `baseUrl` | -- | 自托管Honcho的基URL |
| `peerName` | -- | 用户对等体标识 |
| `aiPeer` | host key | AI对等体标识 |
| `workspace` | host key | 共享工作空间ID |
| `recallMode` | `hybrid` | 可选值为`hybrid`、`context`或`tools` |
| `observation` | all on | 各对等体的`observeMe`/`observeOthers`开关状态 |
| `writeFrequency` | `async` | 可选值为`async`、`turn`、`session`或整数N |
| `sessionStrategy` | `per-directory` | 可选值为`per-directory`、`per-repo`、`per-session`或`global` |
| `messageMaxChars` | `25000` | 每条消息的最大字符数（超出时会分块传输） |

### 辩证推理设置

| 键值 | 默认值 | 描述 |
|-----|---------|-------------|
| `dialecticReasoningLevel` | `low` | 可选值为`minimal`、`low`、`medium`、`high`、`max` |
| `dialecticDynamic` | `true` | 根据查询复杂度自动调整推理强度。设为`false`则表示保持固定级别 |
| `dialecticDepth` | `1` | 每次查询的辩证推理轮数（1-3轮） |
| `dialecticDepthLevels` | -- | 可选值，用于指定每轮的推理强度等级，例如`["low", "high"]` |
| `dialecticMaxInputChars` | `10000` | 辩证推理查询输入的最大字符数 |

### 上下文预算与注入机制

| 键值 | 默认值 | 描述 |
|-----|---------|-------------|
| `contextTokens` | 无上限 | 基础上下文注入内容（摘要 + 表示形式 + 卡片）的总字符数上限。该参数为可选限制——若省略则保持无上限，设置为整数则可限定注入大小。 |
| `injectionFrequency` | `every-turn` | 可选值为 `every-turn` 或 `first-turn`。 |
| `contextCadence` | `1` | 每次调用上下文 API 之间的最小轮次间隔。 |
| `dialecticCadence` | `2` | 每次调用辩证式 LLM 之间的最小轮次间隔（推荐值为 1–5）。 |

`contextTokens` 的限额会在内容注入时进行校验。如果会话中的摘要、表示形式及卡片内容总和超过该限额，Honcho 会首先截断摘要，再截断表示形式，而保留卡片内容。此举可避免在长会话中出现上下文过度膨胀的问题。

### 内存上下文净化

为防止提示注入及内容格式错误，Honcho 会在注入前对 `memory-context` 块进行净化处理：

- 移除用户生成的结论中的 XML/HTML 标签；
- 规范化空白字符与控制字符；
- 截断长度超过 `messageMaxChars` 的单个结论；
- 转义可能破坏系统提示结构的分隔符序列。

此机制可解决那些包含标记或特殊字符的原始用户结论可能损坏注入上下文块的特殊情况。

## 故障排除

### “未配置 Honcho”
运行命令 `hermes honcho setup`，并确保 `~/.hermes/config.yaml` 文件中包含 `memory.provider: honcho` 这一配置项。

### 会话之间内存无法持久化
请运行 `hermes honcho status` 检查设置，确保 `saveMessages: true` 且 `writeFrequency` 不设置为 `session`（该模式仅在会话退出时才写入数据）。

### Profile 无法获取独立节点
创建 Profile 时请使用 `--clone` 参数：`hermes profile create <name> --clone`。对于已存在的 Profile，则需执行 `hermes honcho sync`。

### 仪表板中的观测结果未同步更新
每次会话启动时，观测配置都会从服务器同步而来。在 Honcho UI 中修改设置后，请重新启动新会话。

### 消息被截断
长度超过 `messageMaxChars`（默认为 25,000 字符）的消息会自动分割，并添加 `[continued]` 标记。如果该问题频繁出现，请检查是否是工具输出或技能内容导致消息体积过大。

### 上下文注入量过大
若出现上下文预算超限的警告，请降低 `contextTokens` 值或减少 `dialecticDepth` 设置。当预算紧张时，会首先截断会话摘要内容。

### 会话摘要缺失
生成会话摘要需要当前 Honcho 会话中至少有过一次对话历史。在冷启动状态（全新会话且无历史记录）下，系统会省略摘要部分，转而使用冷启动提示策略。

## CLI 命令

| 命令 | 描述 |
|---------|-------------|
| `hermes honcho setup` | 交互式设置向导（云环境/本地环境、身份认证、监控功能、回溯机制、会话管理） |
| `hermes honcho status` | 显示已配置的参数、连接测试结果以及当前激活配置文件的节点信息 |
| `hermes honcho enable` | 为当前激活配置文件启用 Honcho 功能（如需则创建主机块） |
| `hermes honcho disable` | 禁用当前激活配置文件的 Honcho 功能 |
| `hermes honcho peer` | 显示或更新节点名称（支持参数：`--user <name>`、`--ai <name>`、`--reasoning <level>`） |
| `hermes honcho peers` | 显示所有配置文件中的节点身份信息 |
| `hermes honcho mode` | 显示或设置回溯模式（可选值：`hybrid`、`context`、`tools`） |
| `hermes honcho tokens` | 显示或设置令牌配额（支持参数：`--context <N>`、`--dialectic <N>`） |
| `hermes honcho sessions` | 列出已知的目录与会话名称之间的映射关系 |
| `hermes honcho map <name>` | 将当前工作目录映射为 Honcho 会话名称 |
| `hermes honcho identity` | 设置 AI 节点身份，或同时显示两种节点表示形式 |
| `hermes honcho sync` | 为所有尚未创建主机块的 Hermes 配置文件生成主机块 |
| `hermes honcho migrate` | 从 OpenClaw 原生内存架构逐步迁移至 Hermes + Honcho 架构的指南 |
| `hermes memory setup` | 通用内存提供程序选择器（选择 “honcho” 即会运行相同的设置向导） |
| `hermes memory status` | 显示当前使用的内存提供程序及其配置信息 |
| `hermes memory off` | 禁用外部内存提供程序 |
