---
description: "Claude Code Token 优化体系 — Rule+Skill联动、渐进式披露、MCP按需加载，可从零复现的完整方法论"
---

# Token 优化体系

通过 Rule/Skill/MCP 分层管理实现 token 节省的完整方法论。本 skill 自身即采用多文件渐进式披露结构。

## 核心原则

1. **固定成本最小化** — Rule/CLAUDE.md 每轮全文加载，必须精简；Skill 按需加载，存详情
2. **渐进式披露** — 信息分层：Rule(触发索引) → Skill SKILL.md(目录) → references/(详情)
3. **元信息优于内容** — 存"哪里有什么"的索引，不存会变的实现细节

## 体系架构（四层）

| 层级 | 载体 | 加载时机 | 内容 |
|------|------|---------|------|
| L0 | Rule（≤10行） | 每轮 | 触发条件 + 指向 Skill 的索引 |
| L1 | Skill SKILL.md（≤50行） | 触发时 | 目录 + 各子文件一句话摘要 |
| L2 | Skill references/*.md | AI 按需 Read | 详细规则、模板、示例 |
| L3 | 源码 | AI 按需 Read | 实现细节（不存储，直接读源文件） |

## 参考文档目录

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `references/cost-model.md` | 上下文成本模型、MCP Tool Search、Rule 精简 | 理解原理时 |
| `references/patterns.md` | Rule+Skill 联动、多文件披露、项目文档拆分、索引自维护 | 创建 Rule/Skill 时 |
| `references/setup.md` | 从零搭建步骤、当前文件清单、新机器复用 | 首次搭建或迁移时 |

## 快速入口

- 首次搭建 → 读 `references/setup.md`
- 理解成本模型 → 读 `references/cost-model.md`
- 创建新 Rule/Skill/项目文档 → 读 `references/patterns.md`
