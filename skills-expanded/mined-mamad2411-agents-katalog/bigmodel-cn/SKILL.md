---
name: bigmodel-cn
description: 接入智谱AI开放平台（bigmodel.cn / open.bigmodel.cn，GLM 系列模型）的完整 API 使用手册。当用户需要调用智谱/bigmodel.cn/GLM/CogView/CogVideoX/Zhipu AI 的任何能力时都应使用本技能——包括但不限于：GLM 对话补全（含流式、函数调用、深度思考、多模态）、图像生成（GLM-Image/CogView）、视频生成（CogVideoX/Vidu）、语音识别与合成（GLM-ASR/GLM-TTS/音色克隆）、文本向量与重排序（Embedding/Rerank）、联网搜索、网页阅读、内容安全审核、文档解析与 OCR、文件与批处理（Batch）API、托管知识库/RAG 检索、平台内置智能体（Agents/Assistant API）、GLM-Realtime 实时语音视频通话，以及通过 OpenAI SDK / Claude API / LangChain 兼容层快速迁移接入；也包括 GLM Coding Plan（编程套餐）的接入与排错——Coding Plan 的 API Key、Base URL、可用模型都与标准 API 不同，在 Claude Code / OpenCode / Kilo Code 等工具里配置套餐（个人版 Lite/Pro/Max 或团队版席位）、区分个人与团队套餐的额度和超额计费、或遇到"买了套餐却报 1113 余额不足"时也应加载本技能。只要用户提到"接入智谱""bigmodel.cn""open.bigmodel.cn""GLM 模型""智谱开放平台""zai-sdk""zhipuai""GLM Coding Plan""编程套餐"，或者要求写代码调用上述任意能力，都应主动加载本技能，不要凭记忆编造接口参数。
---
# 智谱 BigModel 接入指南

把官方文档（`docs.bigmodel.cn`）压成可直接照抄的调用规范，目标是**第一次就写对**，
而不是凭训练记忆编参数名。**本页只做分流与规则，具体字段表和示例在 `references/`。**

## 当前事实（2026-09 实测，与训练记忆冲突时以本节为准）

| 项 | 值 |
| :--- | :--- |
| Base URL | `https://open.bigmodel.cn/api/paas/v4`（标准）· `…/api/coding/paas/v4`（Coding Plan）· `…/api/anthropic`（Anthropic 兼容） |
| 鉴权 | `Authorization: Bearer <API_KEY>`，Key 走环境变量 |
| 主力对话模型 | `glm-5.3` / `glm-5.3-flash`（视觉：`glm-4.6v`、`glm-5v-turbo`） |
| Batch 白名单最强 | `glm-5.1`（**旗舰 `glm-5.3` 不在白名单内**） |
| 可用 SDK | `zai-sdk`（→ `api.z.ai`）· `zhipuai`（→ `open.bigmodel.cn`） |

## 你的训练数据在这几点上是错的

平台迭代比训练数据快。以下每条都用真实调用验证过——**与你的记忆冲突时，信这份**：

1. **`tool_choice` 只支持字符串 `"auto"`。** 传 `{"type":"function",...}` 或 `"required"` 不报错，
   但被当成 `auto`，模型可能一次都不调用。硬需求要在代码里无条件调用，别依赖这个参数。
2. **`response_format: {"type":"json_schema"}` 被静默忽略。** 只有 `text` / `json_object` 两种取值生效。
3. **思考 token 计入 `max_tokens`。** 预算给小了就是 `finish_reason=length` + 空正文。判据是
   `finish_reason`，不是空字符串本身。
4. **Coding Plan 是独立 Key + 独立端点**，不是折扣档。套餐 Key 打标准端点必报 `1113`，
   而 `1113` 的文案「余额不足」是误导——它有三种成因，排查顺序见 `references/coding-plan.md`。
5. **异步端点会静默换模型**：`glm-4.6` 实际跑 `glm-4.7`，`glm-4.7` 跑成文档里不存在的 `glm-4.7-ali`。
   同步端点不会。需要锁版本就读回响应里的 `model` 字段核对。
6. **知识库接口出错也返回 HTTP 200**，真状态在 `body.code`。`raise_for_status()` 永远不触发。

> 遇到与本节冲突的实际报错，**信 API 的报错**，并提醒用户去 `docs.bigmodel.cn` 核实——
> 本技能包的内容抓取于 2026-09。

## 我要做什么 → 读哪一份

按功能取用，**不需要通读全部**；但打开某一份时请完整读它，不要只扫一眼标题。

| 我要做什么 | 读 | 核心 endpoint |
| :--- | :--- | :--- |
| 文本对话、流式、函数调用、多模态输入、深度思考、结构化输出、上下文缓存、异步对话 | [`chat.md`](references/chat.md) | `/chat/completions`、`/async/chat/completions` |
| 文生图 / 图生图、文生视频、语音识别与合成、音色克隆 | [`media.md`](references/media.md) | `/images/generations`、`/videos/generations`、`/audio/*` |
| 向量化、重排序、Token 计数、文档解析、联网搜索、网页阅读、内容安全 | [`tools.md`](references/tools.md) | `/embeddings`、`/rerank`、`/web_search`、`/reader` |
| 文件上传与管理、大文件异步解析、OCR、批量处理 Batch | [`files-batch.md`](references/files-batch.md) | `/files`、`/batches` |
| 内置智能体、Assistant API、托管知识库 / RAG、多模态检索 | [`agents-assistant-knowledge.md`](references/agents-assistant-knowledge.md) | `/v1/agents`、`/llm-application/open/*` |
| 用 OpenAI / Claude / LangChain SDK 接入，或官方 Python / Java SDK | [`sdk-and-compat.md`](references/sdk-and-compat.md) | 兼容层 base_url |
| **GLM Coding Plan 编程套餐**：配置、可用模型、`1113` 排错、个人版 vs 团队版、附赠 MCP、查剩余额度 | [`coding-plan.md`](references/coding-plan.md) | `…/api/coding/paas/v4`、`…/api/anthropic`、`…/api/monitor/usage/*` |
| 实时语音 / 视频通话 | [`realtime.md`](references/realtime.md) | GLM-Realtime WebSocket |
| 选哪个模型、上下文与输出上限、思考模式默认行为 | [`models.md`](references/models.md) | — |
| 报错排查、重试策略、速率限制 | [`errors-and-limits.md`](references/errors-and-limits.md) | — |

## House rules（写代码前必读）

不属于任何单一接口，但每个能力域都会踩：

- **两套 Key 不能混用。** 同一项目既要套餐额度跑对话、又要调套餐不含的能力时，
  **同时管理两个 Key 和两个 Base URL**，分开命名（`GLM_CODING_PLAN_API_KEY` / `ZHIPUAI_API_KEY`）。
- **上传成功 ≠ 能用。** 文件要在 chat 里引用，`purpose` 必须是 `user_data`；
  知识库文档要能检索，必须轮询 `GET /document/{id}` 的 `embedding_stat` 到 `1`。
- **流式统一 SSE**，以 `data: [DONE]` 结束。流式没有独立错误码，异常体现在每个 chunk 的 `finish_reason` 里。
- **多模态输入用 `content` 数组**而非纯字符串；`file` 类型是**视觉模型**的能力，
  普通文本模型（如 `glm-4.6`）传 `file` 块会报 `content.type 参数非法`。
- **速率限制按并发数算，不是 QPS**，且无接口可查。批量场景走 Batch 或异步接口，别对同步接口猛发并发。
- **生成类接口默认打 AI 水印**，关闭需要额外权限。
- **拿到空内容先看 `finish_reason`**，不要直接当成模型不会答。

## 文档与实测不符之处

以下是官方文档写错或没写、只有真实调用才会暴露的地方。详情与报错原文在对应 reference 里，
在 reference 里统一用 `<!-- Gap: … -->` 标记（9 处），可直接 grep 定位：

| 位置 | 文档怎么说 | 实测是什么 |
| :--- | :--- | :--- |
| `tools.md` / `chat.md` | 搜索结果都带来源链接 | `link` 是否为空取决于 `search_engine`：`search_std`/`search_pro` 恒为空串 |
| `chat.md` | 引用需要的字段自动返回 | 不显式设 `search_result: true`，`web_search` 数组根本不出现 |
| `files-batch.md` | Batch 可用平台模型 | 独立白名单，旗舰不在其中；这条只出现在报错里 |
| `files-batch.md` | `custom_id` 无限制 | 有未文档化的 6 字符下限；`request_counts` 是嵌套对象 |
| `agents-assistant-knowledge.md` | `stream` 默认 `true` | `glm-4-assistant` 不传或传 `false` 都报 `1212`，只有 `true` 行 |
| `agents-assistant-knowledge.md` | Agent 响应 `content` 是字符串 | 实际是 `{"type":"text","text":"…"}` 对象 |
| `realtime.md` | 握手先到 `session.updated` | 先到 `session.created`，规范里没有这个事件 |
| `sdk-and-compat.md` | 调用成功就有内容 | 可能返回空字符串，判据是 `finish_reason` |
| `coding-plan.md` | 没有用量或余额查询接口 | 账户余额确实没有 API；套餐额度有 3 个未文档化的 `/api/monitor/usage/*` 接口可查 |

（其余 7 条与上方「训练数据错误」一节重合，不重复列出。）
