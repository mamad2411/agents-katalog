---
name: jiekou-docs
description: |
  接口AI 模型服务参考文档，涵盖 LLM API（兼容 OpenAI）、图像/视频/音频 API、集成方案、鉴权/计费/定价/限流及故障排查。适用于"如何在 OpenAI SDK / LangChain 等工具中接入 接口AI？"以及 接口AI 请求失败等问题。
---

# 接口AI 平台参考

按以下流程处理：
1. 识别用户所属场景（模型调用、集成方案、故障排查）。
2. 使用 WebFetch 或等效 HTTP 读取工具，从下方映射表中获取所需的最少参考文件。
3. 将价格、模型可用性和服务状态视为动态数据，回答前先获取最新信息。
4. 尽量返回可直接复制粘贴的命令或代码片段。
5. 如果本地参考文件未涵盖所需内容，提供最接近的经验证指引，明确说明缺口，并指向官方实时文档。

## LLM(大语言模型) 快速参考

| 键 | 值 |
|-----|-------|
| **API Base URL** | `https://api.jiekou.ai/openai` |
| **鉴权方式** | `Authorization: Bearer <API_KEY>` |
| **获取 API Key** | https://jiekou.ai/settings/key-management |
| **模型列表** | https://jiekou.ai |
| **定价** | https://jiekou.ai/pricing |
| **控制台** | https://jiekou.ai/console |

## 图像、视频、音频 API 快速参考

接口AI 聚合了业内主流的多模态 API，覆盖图像生成、视频生成和语音合成三大方向。

| 键 | 值 |
|-----|-------|
| **鉴权方式** | `Authorization: Bearer <API_KEY>`（同 LLM） |
| **获取 API Key** | https://jiekou.ai/settings/key-management |
| **API 文档（MCP）** | https://jiekou.mintlify.app/mcp |
| **视频统一接口文档** | https://jiekou.ai/docs/models/reference-unified-video-generation |
| **定价** | https://jiekou.ai/pricing |

## 文档映射表

| 问题 | 读取此文件 | 实时文档 |
|----------|-----------|-----------|
| 快速入门 | [quick-start.md](https://raw.githubusercontent.com/jiekouai/jiekou-skills/main/skills/jiekou-docs/references/quick-start.md) | - |
| LLM API 使用 | [llm-guide.md](https://raw.githubusercontent.com/jiekouai/jiekou-skills/main/skills/jiekou-docs/references/llm-guide.md) | [API 参考](https://jiekou.ai/docs/models/reference-llm-create-chat-completion) |
| 图像 / 视频 / 音频 API | [quick-start.md §3](https://raw.githubusercontent.com/jiekouai/jiekou-skills/main/skills/jiekou-docs/references/quick-start.md) | [MCP 工具](https://jiekou.mintlify.app/mcp) · [视频统一接口](https://jiekou.ai/docs/models/reference-unified-video-generation) |
| 工具集成 | [integrations.md](https://raw.githubusercontent.com/jiekouai/jiekou-skills/main/skills/jiekou-docs/references/integrations.md) | - |
| 常见问题 | [faq.md](https://raw.githubusercontent.com/jiekouai/jiekou-skills/main/skills/jiekou-docs/references/faq.md) | - |

## 参考文件选择规则

- 初次配置和最简示例使用 `quick-start.md`（见上方映射表）。
- 聊天补全、工具调用、视觉、JSON 模式和批量任务使用 `llm-guide.md`（见上方映射表）。
- 图像生成、视频生成、语音合成等多模态 API 使用 `quick-start.md §3`，并指向 MCP 工具文档获取完整参数说明。
- 集成问题统一以 `integrations.md`（见上方映射表）为入口，再从中选择子文档。
- 调试时优先使用 `faq.md`（见上方映射表）。
- 如果无法从 GitHub 获取原始文件，回退到本技能目录中的本地 `references/*.md` 文件。
- 若答案涉及配额、定价、模型数量，请先通过实时文档/API 验证，并在响应中注明验证日期。

## 动态数据策略

- 将模型目录大小、定价、限流、延迟和区域可用性视为动态数据。
- 在最终响应中以 `Verified on: YYYY-MM-DD` 格式标注动态数据的验证时间。
- 如果无法实时验证，明确说明数据可能已过期，并附上官方来源链接。

## 动态数据（始终获取最新值）

### 获取最新模型列表
```bash
curl https://api.jiekou.ai/openai/v1/models \
  -H "Authorization: Bearer $接口AI_API_KEY"
```

### 当前定价
访问 https://jiekou.ai/pricing 查看最新定价。

