---
name: session-memory
description: 跨会话记忆与上下文注入——自动归档关键决策、注入历史摘要、管理短期工作记忆
version: "4.4.0"
updated: "2026-05-22"
tags: [memory, session, context, persistence]
---

# 跨会话记忆

## 核心理念

Jarvis 的记忆体系遵循"被动收集+自动注入"——你在会话中推进 Gate 时会自动记录关键事件，下次会话启动时自动加载历史上下文。你不需要显式调用任何归档命令。

## 三级记忆

| 级别 | 机制 | TTL | 触发方式 |
|------|------|-----|---------|
| Working Memory | `working_memory_add` — 手动记录关键决策/发现 | 7 天 | 手动调用或 Gate 推进自动记录 |
| Session Archive | 会话结束时自动归档到 repowiki | 永久 | 最终 Gate 或 cancel 时自动触发 |
| Context Injection | `session_join` 时自动注入历史摘要 | — | 每次会话启动自动执行 |

## 何时手动使用 working_memory_add

虽然 Gate 推进会自动记录进度，以下情况应**手动**调用 `working_memory_add`：

| 场景 | category | 示例 |
|------|----------|------|
| 做出关键架构决策 | `decision` | "选择 SQLite 作为存储引擎因为零配置需求" |
| 发现重要模式或问题 | `discovery` | "发现 MCP 工具在 Windows 路径下有反斜杠问题" |
| 遇到阻塞 | `blocker` | "等待后端 API 接口定义完成" |
| 记录重要进度 | `progress` | "已完成 3/5 个模块的迁移" |

## 自动行为

1. **session_join 时**：自动清理过期记忆，注入最近 3 次会话归档摘要到 `context_summary`
2. **advance_gate 时**：自动记录 Gate 推进到 working_memory（category: progress）
3. **最终 Gate / cancel 时**：自动消费所有事件+记忆，生成摘要写入 repowiki + session_context 表

## 查询历史

- `mcp__jarvis-engine__session_context()` — 获取历史会话摘要和未完成事项
- `mcp__jarvis-engine__working_memory_query({ query: "关键词" })` — 搜索历史记忆
- `mcp__jarvis-engine__repowiki_query({ query: "关键词" })` — 搜索知识库归档

## 红线

- 不要依赖记忆替代代码文档。记忆是上下文辅助，代码本身是真相源。
- 不要在每次小操作后写 working_memory。仅记录关键决策、发现和阻塞。
- 过期记忆（7天）会自动清理，不要手动管理 TTL。
