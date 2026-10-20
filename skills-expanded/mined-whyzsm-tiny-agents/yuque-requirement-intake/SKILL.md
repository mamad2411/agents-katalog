---
name: yuque-requirement-intake
description: 需求链接 intake 技能：把语雀（Yuque）文档 URL 或任意 MCP 可读链接，经 Streamable HTTP MCP 服务器读取并归一化成统一 RequirementBundle JSON（正文/评论/标题/更新时间/contentHash/分段/confidence/evidence）。Python 实现，唯一运行时依赖 mcp Python SDK。用于：贴了语雀需求文档链接要读原文、需求链接结构化摄入、yuque_get_doc 工具调用、MCP 需求源适配。当用户说「读这个语雀文档」「抓取需求链接」「把链接转成需求输入」时使用。只读不回写；抓取失败保留原链接并如实记录缺失。
---

# Yuque Requirement Intake

把可定位的需求链接（语雀文档 URL 或任意 MCP 服务器可读的 URI）读取成一份统一的结构化需求输入（RequirementBundle），减少人工摘录。不改写、不回写任何文档。

## 工作方式

```
需求链接
  -> Python URL 校验
  -> 识别来源（语雀 URL 自动解析 repo_id/doc_id）
  -> MCP list_tools / read_resource / call_tool
  -> 原文、评论、元信息收集
  -> 清洗、去噪、分段、hash
  -> RequirementBundle（stdout JSON）
```

- 语雀文档 URL（`https://<space>.yuque.com/<group>/<book>/<doc-slug>`）自动解析为 `yuque_get_doc` 工具调用（repo_id + doc_id + markdown 格式），无需手工拆参数。
- MCP 服务器工具契约不同时，退回显式 `--tool-name` / `--tool-arguments`；只提供 resources 的服务器走 `--resource-uri`。
- 输出恒为单个 JSON 对象（RequirementBundle），可直接喂给后续需求整理/评审流程。

## 依赖与环境

- Python ≥ 3.10（dataclass slots 语法）。
- 唯一运行时依赖：MCP Python SDK（`pip install mcp`）；缺失时脚本会给出明确报错。
- MCP 服务器地址：环境变量 `MCP_URL` 或 `--mcp-url`（Streamable HTTP 端点，如 Yuque MCP server）。语雀 token 等凭据配置在 MCP 服务器侧，本脚本不经手。

## 使用方式

```bash
# 干跑：只打印解析出的 MCP 抓取计划，不连服务器（验证 URL 解析）
python3 scripts/mcp_requirement_source.py \
  --source-uri "https://your-space.yuque.com/group/book/doc-slug" \
  --print-fetch-plan

# 正式抓取：语雀 URL 自动映射 yuque_get_doc
MCP_URL=http://127.0.0.1:3000/mcp \
python3 scripts/mcp_requirement_source.py \
  --source-uri "https://your-space.yuque.com/group/book/doc-slug"

# 显式工具回退（MCP 服务器工具契约不同时）
MCP_URL=http://127.0.0.1:3000/mcp \
python3 scripts/mcp_requirement_source.py \
  --source-uri "https://requirements.example.com/items/123" \
  --tool-name "getRequirementDocument" \
  --tool-arguments '{"url":"https://requirements.example.com/items/123"}'
```

## RequirementBundle 字段

| 字段 | 说明 |
| --- | --- |
| `sourceType` / `sourceUri` | 入口类型（screenshot/link/text）与原始链接 |
| `title` / `updatedAt` | 从结构化返回中提取的标题与更新时间 |
| `rawText` / `comments` | 清洗后的正文与评论列表 |
| `contentHash` | 链接+标题+时间+正文+分段的 sha256，用于判断是否需重读 |
| `normalizedSections` | 分段结果（body + 每条 comment） |
| `confidence` | 有分段 0.75 / 无内容 0.35 |
| `evidence` | MCP 服务器、工具数、资源数、来源 provider、抓取模式等溯源信息 |

## 边界与铁律

1. **只读**：本路径只读取正文与评论，不扫描全站、不回写 Yuque 或任何文档存储。
2. **不固化来源**：需求链接必须来自当次用户输入或任务上下文，不得把某个语雀空间/知识库/文档 slug 写死。
3. **失败如实**：链接不可访问、MCP 不可用或内容不足时，保留原始链接并把缺失点写进 openQuestions/缺失说明，不伪装成需求完成。
4. **去重缓存**：同一链接重复读取时先比 `contentHash`/`updatedAt` 再决定是否重读。
5. **溯源留在 evidence**：来源差异（provider、host、repo_id、doc_id、模式）都留在 `evidence` 字段，不让后续阶段自己猜。
6. 本技能不决定页面类型、组件选型或实现范围——那是后续需求/方案阶段的事。
