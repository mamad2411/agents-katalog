---
name: system-design
description: "系统架构决策与设计文档：Design Doc（含 Alternatives Considered 强制段）、ADR、结构影响分析。用于多模块、存量系统改造、共享边界、高风险集成、重大技术选型。不管前端技术栈和视觉表达（那是 frontend-design-research 的事）。"
---

# 系统架构决策

## 技能定位

本技能处理"系统怎么切"的问题：模块边界、数据流向、存储选型、API 契约、依赖拓扑、扩展点。

**核心方法论**：Alternatives Considered 强制 + trade-off 诚实。没有 alternatives 段的 Design Doc 是推销文档，不是设计文档。

## 何时进入

- 多模块项目或跨模块改造
- 存量系统新增模块（需评估是否破坏现有边界）
- 高风险集成（第三方服务、跨团队 API）
- 重大技术选型（数据库、消息队列、部署架构）
- `req-suite:project-spec` 路由过来

## 何时不进入

- 前端技术栈选型（Next.js/Vite/状态管理）→ `frontend-design-research`
- 视觉/动效/组件库 → `frontend-design-research`
- 纯 UI 项目无后端 → 不需要本 skill
- 单模块小项目、local-light 模式 → 不需要本 skill

## 前置输入

从 `req-suite:project-spec` 获取：
- `knowledge/product-specs/PRODUCT-BRIEF.md`（目标结果 + 非目标）
- `knowledge/references/research-*.md`（调研结果，如有）
- 选择题清单中和架构相关的 🟡/🔴 项

## 核心流程

```
1. 结构影响分析 → 2. Design Doc / ADR → 3. 更新 ARCHITECTURE.md
```

### 步骤 1：结构影响分析

回答这些问题：

- 这次变化涉及哪些模块？
- 有没有模块不该碰（boundary violation）？
- 数据流方向是什么？有没有循环依赖？
- 失败模式是什么？一个模块挂了会影响什么？
- 有没有共享状态需要加锁/同步？

### 步骤 2：写 Design Doc 或 ADR

根据决策规模选用：

#### 大 Design Doc（重要方案决策）

核心段（按社区最佳实践）：

| 段 | 写什么 | 质量标准 |
|---|---|---|
| **Context** | 背景事实 + 相关链接，不写观点 | 3-5 行，读完知道为什么在讨论这件事 |
| **Goals / Non-goals** | 要达成什么、明确不追求什么 | 可验证的 bullet 列表 |
| **Proposed Design** | 方案概述 + 关键架构图 | Agent 读完能开始实现 |
| **Alternatives Considered** | 考虑过的其他方案 + 每个的 trade-off | **这是核心。没有这段的 doc 是推销文档** |
| **Risks & Mitigations** | 已知风险和应对 | 每条 risk 有对应 mitigation |
| **Success Criteria** | 怎么判断方案成功 | 可测量、可验证 |

规模：1-3 页小方案，5-10 页大方案。超过 10 页说明该拆。

产出写入 `knowledge/design-docs/DESIGN-DOC-[标题].md`。

#### 小 ADR（单个决策记录）

适用于具体技术选择、配置决策、依赖选型。

```markdown
# ADR-NNN: [决策标题]

## Status
Proposed | Accepted | Superseded by ADR-NNN | Deprecated

## Context
[驱动这个决策的背景力量、约束、需求]

## Decision
[选了什么、怎么做]

## Consequences
[好的后果 + 坏的后果 + trade-off]
```

一个文件一个决策，不合并。不修改已 Accepted 的 ADR，用新 ADR 替代。

产出写入 `knowledge/design-docs/ADR-NNN-[标题].md`。

### 步骤 3：更新 ARCHITECTURE.md

将稳定的结构事实写入项目根的 `ARCHITECTURE.md`（不是 knowledge/ 下的）：模块拓扑、关键依赖、数据流向。只写事实，不写决策理由（理由住在 Design Doc / ADR 里）。

## 与 frontend-design-research 的边界

两个 skill 是正交子域，不是上下层：

| 本 skill 管 | frontend-design-research 管 |
|---|---|
| 模块边界、数据流、存储、API 契约 | 主语言、参考案例、动效采访、视觉 token |
| 依赖拓扑、扩展点 | 前端技术栈（框架/路由/状态/构建） |
| 跨层集成协议 | 组件库路由、动效资产库 |

**边界冲突裁决**：
- 前端技术栈（Next.js/Vite 等）→ **归 frontend-design-research**（和视觉/动效紧密耦合）
- API 契约 → **归本 skill**（跨层协议）
- 全栈项目先跑本 skill 定系统骨架，再跑 frontend-design-research 定前端表达

## 知识库路由

| 触发 | 知识库条目 | 路径 |
|---|---|---|
| 结构影响分析 | 架构分层思考框架 | ~/note/01-AI工程/项目方案方法/架构分层思考框架.md |
| 多方案对比 | 方案对比指南 | ~/note/01-AI工程/项目方案方法/方案对比指南.md |
| 上游方法论 | req-project-spec 方法论 | ~/note/01-AI工程/Agent系统/方法/02-需求与项目方案/从需求到项目方案：req-project-spec 方法论.md |
