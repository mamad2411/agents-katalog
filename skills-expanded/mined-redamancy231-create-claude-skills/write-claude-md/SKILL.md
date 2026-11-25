---
name: write-claude-md
description: '[流程:项目] Create or optimize project-level CLAUDE.md. Triggers when user asks to write/create/optimize/review a CLAUDE.md file, or when a new project lacks one. Uses five-step protocol: evidence collection, vulnerability testing, five-gap/five-abuse checks, empirical rules, and optional multi-backend validation. Not for: general documentation writing, README creation, project scaffolding, or conceptual discussions about CLAUDE.md without modification intent.'
allowed-tools: Read, Write, Edit, Bash(git:*), Glob, Grep
source: self
source_type: self
license: "CC-BY-4.0"
verified_by: "GPT-5.5, DeepSeek-V4-Pro, Kimi-K2.7, Qwen3.7-Max, GLM-5.2"
---

# Write CLAUDE.md — 项目级 CLAUDE.md 编写/优化执行器

> **定位**：流程型 Skill——每步有明确的输入/输出/完成标准。不替代用户对项目架构的判断，只提供裁剪框架。

## 快速参考（路由表）

| 场景 | 执行 |
|------|------|
| 新项目，无 CLAUDE.md | 创建模式：Step 0→5 全走 |
| 已有 CLAUDE.md，需审查/优化 | 审计模式：Step 0→1→2→3→4→5（增量修改，禁止全量重写） |
| CLOSED/冻结项目 | → 额外过「CLOSED/冻结项目额外要求」→ [lifecycle-differentiation.md](reference/lifecycle-differentiation.md) |
| 非软件项目（方法论/研究/内容） | → 额外过「非软件项目额外检查」→ [non-software-checks.md](reference/non-software-checks.md) |
| 重要项目需多后端验证 | → Step 5 多后端验证 |
| 仅讨论概念，非操作性请求 | 不触发 |

## 共享文件所有权

| 文件 | 本 Skill 角色 | 其他写入者 | 约束 |
|------|-------------|-----------|------|
| `CLAUDE.md` | **主写入者**（生成/修改） | 无（其他 Skill 只读） | 只在操作指令变更时修改，不由其他文件变化触发 |
| `project_status.md` | **只读**（Step 0 采集生命周期） | `session-end`（主写入者） | 读取前检查文件存在性；若不存在 → 假定为活跃项目 |
| `reference_files.md` | **只读**（Step 4a 指针目标） | `session-end`（主维护者） | 白名单指针化引用此文件 |

## 触发分级

**应触发**：用户要求"写/创建/优化/审查 CLAUDE.md"；新建项目且根目录无 `CLAUDE.md`（可主动提议，等用户确认）；用户调用 `/write-claude-md`。

**不应触发**：讨论 CLAUDE.md 概念或方法论（非操作性请求）；只是抱怨 CLAUDE.md 状态（未明确要求修改）；项目已有 CLAUDE.md 且用户正在进行无关操作。

**判定问句**：用户是否期望我生成或修改 CLAUDE.md 文件？不确定则先问。

## 路由分支

```
不存在 CLAUDE.md → 创建模式：Step 0→5 全走
已存在 CLAUDE.md → 审计模式：Step 0→1→2→3→4→5（增量修改，禁止全量重写）
```

## 五步协议

| Step | 内容 | 详细文件 |
|------|------|---------|
| 0 | 上下文采集 | [reference/step0-context-collection.md](reference/step0-context-collection.md) |
| 1 | 脆弱性测试（逐条审计） | [reference/step1-vulnerability-testing.md](reference/step1-vulnerability-testing.md) |
| 2 | 五缺检查 | [reference/step2-five-gaps.md](reference/step2-five-gaps.md) |
| 3 | 五滥检查 | [reference/step3-five-abuses.md](reference/step3-five-abuses.md) |
| 4 | 三项实证规则 | [reference/step4-empirical-rules.md](reference/step4-empirical-rules.md) |
| 5 | 多后端验证（重要项目） | [reference/step5-multi-backend-validation.md](reference/step5-multi-backend-validation.md) |

## 参考文件

| 文件 | 内容 |
|------|------|
| [reference/lifecycle-differentiation.md](reference/lifecycle-differentiation.md) | 项目生命周期差异 + 权重矩阵 |
| [reference/non-software-checks.md](reference/non-software-checks.md) | 非软件项目额外检查 |
| [reference/glossary.md](reference/glossary.md) | 术语定义 |
| [reference/anti-patterns.md](reference/anti-patterns.md) | 反例/教训 |
| [reference/death-criteria.md](reference/death-criteria.md) | 本 Skill 的死亡判据 |
| [reference/skill-relationships.md](reference/skill-relationships.md) | 与其他 Skill 的关系 |
| [templates/claude-md-template.md](templates/claude-md-template.md) | CLAUDE.md 输出模板 |
