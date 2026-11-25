---
name: volcengine-ark
description: 接入火山引擎·火山方舟（Volcengine Ark，ark.cn-beijing.volces.com，豆包 Doubao / Seed / Seedream / Seedance 及 DeepSeek、GLM、Kimi、MiniMax 等第三方模型）的完整 API 使用手册，并且重点区分三套互不通用的入口：标准后付费 API（/api/v3 + 方舟 API Key + 带日期的 Model ID）、Coding Plan 编程套餐（/api/coding 或 /api/coding/v3 + 方舟 API Key + 小写 Model Name）、Agent Plan 订阅套餐（/api/plan 或 /api/plan/v3 + Agent Plan 专属 API Key + AFP 抵扣）。覆盖 Chat Completions、Responses API、深度思考、Function Calling、结构化输出、上下文缓存、多模态理解（图片/视频/文档/音频/文件）、图片生成、视频生成、向量化、语音 TTS/ASR、批量推理、应用 Bot、内置工具（联网搜索/MCP/图像处理）、管控面 API（AK/SK 签名，含 Agent/Coding Plan 套餐与用量查询）、在 Claude Code / Codex / OpenCode / OpenClaw / Cline / Cursor / TRAE 等工具里配置套餐、Ark CLI、错误码与限流。当用户提到"火山方舟""火山引擎大模型""方舟""Ark""volces""豆包 API""Doubao""Seedream""Seedance""Agent Plan""Coding Plan""AFP""ark-code-latest""arkcli""volcenginesdkarkruntime"，或者要用这些模型写代码、配置编程工具套餐、排查"用了套餐还被扣费""Key 不对""模型不存在"时，务必加载本技能，不要凭记忆编造 Base URL、Key 类型或模型名格式。
---
# 火山方舟（Volcengine Ark）接入指南

豆包 Doubao / Seedream / Seedance，以及方舟上代理的 GLM / Kimi / DeepSeek / MiniMax。
**本页只做分流与规则，字段表和示例在 `references/`。**

## 当前事实：三套互不通用的入口（本平台最容易全盘写错的地方）

同一个域名下三套入口，**Base URL、Key、`model` 格式三者必须配套**。
配错的结果不是报错，而是**从后付费余额扣钱**或**套餐额度不生效**。

| | 标准 API（后付费） | Coding Plan | Agent Plan |
| :--- | :--- | :--- | :--- |
| Base URL | `…/api/v3` | `…/api/coding/v3` | `…/api/plan/v3` |
| Anthropic 协议 | 文档自相矛盾，未实测 | `…/api/coding` | `…/api/plan`（实测 `/api/plan/v1/messages`） |
| Key | 方舟 API Key | **同一把**方舟 API Key | **Agent Plan 专属 Key**（与方舟 Key 不通用） |
| `model` 格式 | 带日期 **Model ID**，连字符：`doubao-seed-2-0-lite-260428` | 小写 **Model Name**，点号：`doubao-seed-2.0-lite` | 同 Coding Plan |
| 计费 | 按 token 后付费，需先开通模型 | 套餐次数额度 | **AFP** 抵扣 |
| 官方限制 | 任何程序调用 | **仅限 AI 编程工具内** | 文本 / 向量化同样"不可用于 API 调用" |
| 环境变量 | `ARK_API_KEY` | `ARK_API_KEY` | `ARK_AGENT_PLAN_API_KEY` |

鉴权统一 `Authorization: Bearer <KEY>`。**管控面 API 例外**——用 AK/SK 的 HMAC-SHA256 签名，
不是 API Key，务必用官方 SDK 签，别手写（见 `references/management-api.md`）。

## 你的训练数据在这几点上是错的

以下每条都用真实 Agent Plan Key 打出来验证过（2026-09-04，约 45 次调用）：

1. **控制台列出的 `Model Name: auto` 不能直接填。** 传 `model: "auto"` 返回 `404 UnsupportedModel`。
   要用 Auto 路由得填 `ark-code-latest` 并在控制台选 Auto。
2. **Plan 入口接受带日期的 Model ID，但静默按 Name 路由。** 传 `doubao-seed-2-0-lite-260428`
   返回 200，**实际服务的是 `-260215`**。要确认版本只能读响应里的 `model` 字段。
3. **Anthropic 入口把 `claude-*` 静默路由到 `doubao-seed-2-1-turbo`**（抵扣系数 **2.5**）。
   Claude Code 只设 Base URL 和 Token、忘设 `ANTHROPIC_MODEL` 时不报错，只是悄悄多烧一倍多的额度。
4. **「向量化不支持 OpenAI API」是错的。** Plan 入口 `POST /embeddings` 可用；
   但纯文本向量化**只能用 `doubao-embedding-vision`**——`doubao-embedding-text` / `-large` 全部 404。
5. **两个向量化端点形状不同**：`/embeddings` 返回 `data` 是数组、`dimensions:1024` 生效；
   `/embeddings/multimodal` 返回 `data` 是**对象**、维度固定 2048。抄错端点会 `TypeError`。
6. **`kimi-k3` 的 `max_tokens` 把思维链算进去**：`max_tokens:64` 时 `finish_reason: "length"`、
   `content: ""`。改用 `max_completion_tokens` 才正常。
7. **SDK 里没有 `ARKApi().get_afp_usage()` 这类方法。** `volcengine-python-sdk` 5.0.48 的 `ARKApi`
   只有 17 个方法，套餐 / 用量 / 限流类 Action 必须走 `UniversalApi(...).do_call(...)`。

> 遇到与本节冲突的实际报错，**信 API 的报错**。本技能包抓取于 2026-09-03，控制台页面实读。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 |
| :--- | :--- |
| **我买了 Agent Plan 订阅套餐** | [`agent-plan.md`](references/agent-plan.md) |
| **我买了 Coding Plan 编程套餐** | [`coding-plan.md`](references/coding-plan.md) |
| 在 Claude Code / Codex / Cline / Cursor 里配置套餐 | [`tools-setup.md`](references/tools-setup.md) |
| 文本对话、流式、思考、Function Calling、结构化输出、上下文缓存 | [`chat.md`](references/chat.md) |
| Responses API（有状态多轮） | [`responses.md`](references/responses.md) |
| 图片 / 视频 / 文档 / 音频输入 | [`multimodal-input.md`](references/multimodal-input.md) |
| 图片生成（Seedream）、视频生成（Seedance） | [`image-video.md`](references/image-video.md) |
| 向量化、语音 TTS / ASR | [`embeddings-speech.md`](references/embeddings-speech.md) |
| 批量推理、应用 Bot | [`batch-and-bot.md`](references/batch-and-bot.md) |
| 联网搜索 / MCP / 图像处理等内置工具 | [`tools.md`](references/tools.md) |
| 管控面 AK/SK 接口、套餐与用量查询 | [`management-api.md`](references/management-api.md) |
| 选哪个模型、上下文窗口、能否关思考 | [`models.md`](references/models.md) |
| OpenAI / Anthropic SDK 与官方 SDK | [`sdk-and-compat.md`](references/sdk-and-compat.md) |
| 错误码、限流、重试 | [`errors-and-limits.md`](references/errors-and-limits.md) |

## House rules（写代码前必读）

- **别让钱扣错地方。** 套餐用户绝不要打 `…/api/v3`；标准用户也不要打 `/api/plan`、`/api/coding`。
  控制台那句「请勿使用 `/api/v3`，接入会产生额外费用」针对的就是套餐用户。
- **锁模型版本只能读回显。** 请求里写什么不代表跑的是什么——Plan 入口忽略日期后缀，
  Anthropic 入口会换模型。需要对账就核对响应里的 `model`。
- **标准 API 要先「开通模型」**，按量模型逐个开通（或开自动开通）；套餐购买即开通，无需接入点。
- **用 AK/SK 鉴权时 `model` 必须填 `ep-` 接入点 ID**，不是模型名。
- **Plan 入口没有这四类能力**：`/models`、`/tokenization`、`/context/create`（上下文缓存）、
  `/files`（Files API）全部 404。需要它们就得走标准入口。

## 文档与实测不符之处

在 reference 里统一用 `<!-- Gap: … -->` 标记（8 处），可直接 grep 定位。
上方「训练数据错误」一节已覆盖其中 7 条，另一条是：
`service_tier: "fast"` 在 **Agent Plan** 入口报错，文案却写的是 `coding plan` —— 报错文案本身串了台。

## 验证边界

**已验证**：Agent Plan 入口（`/api/plan/v3` 与 `/api/plan/v1/messages`），测试账号 Medium 档，约 45 次真实调用。
**未验证**：标准后付费入口（无标准 Key）、Coding Plan 套餐内行为（未订阅）、语音 / 同传、管控面 Action。
未验证部分是文档转录，reference 里一律标注「文档原文，未实测」。
