---
description: "TOP (Token Optimization Plan) — AI 编程助手 Token 优化体系，Rule+Skill联动、渐进式披露、按需加载，适用于 Claude Code 和 Codex"
---

# Token Optimization Plan (TOP)

通过分层管理实现 AI 编程助手 Token 节省 50-60% 的完整方法论。适用于 Claude Code 和 Codex。

本 Skill 自身即采用多文件渐进式披露结构 —— 吃自己的狗粮。

## 核心原则

1. **固定成本最小化** — 每轮全文加载的内容（Rules/CLAUDE.md/AGENTS.md）必须精简
2. **渐进式披露** — 信息分层：触发索引 → Skill 目录 → references 详情 → 源码
3. **元信息优于内容** — 存"哪里有什么"的索引，不存会变的实现细节

## 体系架构（四层）

| 层级 | Claude Code 载体 | Codex 载体 | 加载时机 |
|------|-----------------|--------------|---------|
| L0 | Rule（≤10行） | TOOLS.md / AGENTS.md | 每轮 |
| L1 | Skill SKILL.md（≤50行） | Skill SKILL.md（≤50行） | 触发时 |
| L2 | references/*.md | references/*.md | AI 按需 Read |
| L3 | 源码 | 源码 | AI 按需 Read |

## 参考文档目录

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `references/cost-model.md` | 上下文成本模型、延迟加载、精简技巧 | 理解原理时 |
| `references/patterns.md` | 五大设计模式详解 | 创建 Rule/Skill 时 |
| `references/setup-claude-code.md` | Claude Code 从零搭建 | Claude Code 用户 |
| `references/setup-codex.md` | Codex 从零搭建 | Codex 用户 |

## 快速入口

- Claude Code 用户 → 读 `references/setup-claude-code.md`
- Codex 用户 → 读 `references/setup-codex.md`
- 理解成本模型 → 读 `references/cost-model.md`
- 创建新 Rule/Skill → 读 `references/patterns.md`
