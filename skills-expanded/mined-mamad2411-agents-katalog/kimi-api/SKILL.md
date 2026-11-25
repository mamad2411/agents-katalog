---
name: kimi-api
description: Moonshot AI / Kimi 开放平台（platform.moonshot.cn、platform.kimi.com、api.moonshot.cn）API 接入指南。凡是要写代码调用 Kimi 模型（kimi-k3、kimi-k2.7-code、kimi-k2.6）、用 OpenAI SDK / Anthropic SDK 指向 Moonshot、做 Kimi 的对话补全、流式输出、思考模式（reasoning_effort / thinking）、工具调用（function calling、$web_search）、JSON 输出、Partial Mode、图片/视频理解、文件抽取问答、Batch 批处理、Token 估算、余额查询、限速与错误排查，都要先读本技能——Kimi 与 OpenAI 有大量"不报错但不一样"或"直接报错"的差异（temperature 固定不可传、moonshot-v1 系列已下线、图片不支持 URL、Batch 不支持 K3 等），凭 OpenAI 经验直接写会写错。用户提到 Moonshot、月之暗面、Kimi API、MOONSHOT_API_KEY 时也应使用。
---

# Kimi（Moonshot AI）开放平台 API

> 状态：**文档草稿**，基于 2026-09-03 抓取的官方文档与 OpenAPI 规范整理，**尚未用真实 API Key 逐条验证**。每个 reference 文件末尾的"待验证疑点"列出了文档自相矛盾或语焉不详之处；`verification-plan.md` 是拿到 Key 后的验证清单。在验证完成前，遇到疑点条目请以"先小规模实测"为准。

## 平台共性（所有接口通用）

- **Base URL**：OpenAI 兼容 `https://api.moonshot.cn/v1`；Anthropic 兼容 `https://api.moonshot.cn/anthropic`。国际站是 `api.moonshot.ai`，**中国站与国际站的 Key、余额完全隔离**，混用 401。
- **鉴权**：`Authorization: Bearer $MOONSHOT_API_KEY`。Key 在 platform.kimi.com/console/api-keys 创建；Kimi Code、Kimi 会员的 Key 与开放平台**不通用**。代码里永远 `os.environ["MOONSHOT_API_KEY"]`，不要硬编码。
- **SDK**：直接用 `openai`（`OpenAI(api_key=..., base_url="https://api.moonshot.cn/v1")`）或 `anthropic`（base_url 指向 `/anthropic`）。Kimi 专有参数（`thinking`、`partial`）通过 `extra_body` / 消息字段传。
- **在线模型只有 4 个**：`kimi-k3`（1M 上下文，旗舰）、`kimi-k2.7-code` / `kimi-k2.7-code-highspeed`（256K，编程）、`kimi-k2.6`（256K，可关思考）。**`moonshot-v1-*`、`kimi-k2.5`、`kimi-k2-*`、`kimi-latest` 全部已下线，调用 404**。
- **采样参数是固定值**：`temperature`、`top_p`、`n`、`presence_penalty`、`frequency_penalty` 各模型固定（K3 温度 1.0），官方明确"建议不要显式传入"，K2.x 文档说传其他值会报错。从 OpenAI 迁移时把这些参数删掉。
- **思考模式**：K3 与 K2.7 Code 始终思考、关不掉；K3 用顶层 `reasoning_effort`（`low`/`high`/`max`，默认 max，**没有 medium**），K2.x 用 `thinking` 对象。思考内容在 `message.reasoning_content`。**多轮对话与工具调用循环必须把上一轮完整 assistant message（含 `reasoning_content`）原样回传**。
- **输出长度**：用 `max_completion_tokens`（`max_tokens` 已弃用）。K3 默认 131072、最大 1048576。网关按 `prompt + max_completion_tokens` 预扣 TPM 限速，别无脑设很大。
- **错误结构**：`{"error": {"type": ..., "message": ...}}`；429 要看 `error.type` 区分过载 / 限速 / 欠费；已下线模型 404。长请求用 `stream: true` 避免 900 秒 504。
- **上下文缓存是自动的**：不需要建 cache、设 TTL；保持前缀（system prompt、工具定义、长文档）稳定即可，`usage.cached_tokens` 看命中。

## 能力域导航

| 我想做… | 读这个文件 | 涉及接口 |
|---|---|---|
| 选模型、看各模型参数约束、迁移 | `references/models.md` | `GET /v1/models` |
| 对话补全、流式、思考/推理强度、多轮、JSON 输出、Partial Mode、上下文缓存、logprobs、predicted output | `references/chat-completions.md` | `POST /v1/chat/completions` |
| 工具调用循环、tool_choice、`$web_search` 内置搜索、官方工具（Formula）、K3 动态加载工具、重复调用排查 | `references/tools.md` | `POST /v1/chat/completions` |
| 图片/视频输入、上传文件、PDF/Word 文件问答 | `references/vision-and-files.md` | `/v1/files*`, chat |
| 离线批量推理（JSONL） | `references/batch.md` | `/v1/batches*`, `/v1/files` |
| 用 OpenAI Responses API 或 Anthropic SDK / Claude Code 接入 | `references/responses-and-messages.md` | `POST /v1/responses`, `POST /anthropic/v1/messages` |
| 错误码、限速等级、计费、Token 估算、余额、请求签名 | `references/errors-and-limits.md` | `/v1/tokenizers/estimate-token-count`, `/v1/users/me/balance`, `/v1/signatures/verify` |

托管智能体（Hosted Agents：`/docs/hosted-agents/*`、会话/记忆库/触发器等约 120 个接口）**不在本技能范围内**，本次未整理。

## 最小可用示例

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.cn/v1")

completion = client.chat.completions.create(
    model="kimi-k3",
    messages=[
        {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手。"},
        {"role": "user", "content": "你好，1+1 等于多少？"},
    ],
    reasoning_effort="low",          # K3 专用；K2.x 改用 extra_body={"thinking": {...}}
    max_completion_tokens=4096,
    # 不要传 temperature / top_p / n / penalties
)
msg = completion.choices[0].message
print(getattr(msg, "reasoning_content", None))   # 思考过程（SDK 类型里没有该字段，用 getattr）
print(msg.content)
print(completion.usage)                          # 含 cached_tokens
```

## 和 OpenAI 直觉冲突、最容易写错的 10 件事

1. `model="moonshot-v1-8k"` / `"kimi-latest"` → 404，用 `kimi-k3`。
2. 传 `temperature=0.3` → K2.x 明确报错，K3 "建议不传"（实测待补）。删掉。
3. `reasoning_effort="medium"` → 不在枚举里，只有 low/high/max。
4. 工具循环里只回传 `{"role":"assistant","tool_calls":[...]}` 而丢掉 `reasoning_content` → 思考模型要求原样回传整条 message。
5. 图片用 `{"image_url": {"url": "https://..."}}` → 不支持公网 URL，只能 base64 data URL 或上传后 `ms://<file_id>`。
6. 把 PDF 的 `file_id` 放进 messages 让模型读 → 不支持；要 `GET /v1/files/{id}/content` 取文本塞进 `system` 消息。
7. Batch 里用 `kimi-k3` → 不支持，只有 K2.7 Code / K2.6；且 `completion_window` 最小 12h、一批只能一个模型。
8. `tool_choice="required"` 给 K2.6 / K2.7 Code → 报错，只有 K3 支持。
9. `response_format={"type":"json_object"}` 却不在 prompt 里说明 JSON 结构 → 官方要求 prompt 里引导；推荐 `json_schema`（MFJS 规范）。
10. `max_tokens` → 已弃用，改 `max_completion_tokens`；Anthropic 入口的 `max_tokens` 却是必填。

## 写代码前的检查清单

- [ ] `base_url` 与 Key 来自同一站点（cn vs ai）？
- [ ] 模型 ID 在在线列表里？必要时先 `GET /v1/models`。
- [ ] 没传固定值采样参数？
- [ ] 多轮 / 工具循环回传了完整 assistant message？
- [ ] 流式请求解析了 `delta.reasoning_content` 与 `delta.content` 两路，并按 `index` 拼接 `tool_calls`？
- [ ] 视觉 `content` 是数组不是字符串？图片是 base64 或 `ms://`？
- [ ] 遇到本技能"待验证疑点"里的行为，先写一个最小脚本实测再下结论。
