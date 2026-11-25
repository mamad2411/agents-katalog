---
name: using-agent-skills
description: "使用智能体技能系统——元技能指南：了解技能体系的结构、如何加载技能、技能如何与 Agent 配合、何时加载哪些技能。用于指导用户和编排者正确使用本项目的技能系统。"
version: "4.3.9"
updated: "2026-05-30"
---

# 使用智能体技能系统

## 概述

本技能是你的技能系统的"使用说明书"。它告诉你：
- 有哪些技能可用
- 技能与 Agent 如何配合
- 在什么阶段应该加载什么技能
- 如何扩展技能系统

**核心原则：** 技能是可复用的方法论——它们是"怎么做好一件事"的剧本。Agent 是执行者，技能是执行手册。

## 技能与 Agent 的关系

```
技能（Skills）         →  教 Agent "怎么做"
Agent（智能体）        →  负责 "做什么"

编排者（Jarvis）       →  决定 "谁做 + 什么时候做 + 用什么技能"
子 Agent（Workers）    →  执行具体任务，加载相关技能
```

### 工作流

```
用户请求
  ↓
Jarvis 加载相关技能（如 spec-driven-development）
  ↓
Jarvis 按流程调度子 Agent
  ↓
子 Agent 加载分配给自己的技能（如 TDD、source-driven-development）
  ↓
子 Agent 按技能方法论执行任务
  ↓
结果交付 + 审查
```

---

## 技能目录（按流程阶段）

### 阶段 0：想法细化
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `idea-refine` | 将模糊想法细化为结构化问题清单 | Jarvis（编排者） |

### 阶段 1：需求澄清
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `spec-driven-development` | 结构化需求规格编写 | Jarvis |
| `behavioral-guidelines` | 四项核心行为准则 | 所有 Agent |
| `context-engineering` | 选择性上下文传递 | Jarvis（传递上下文时） |
| `session-memory` | 跨会话记忆与上下文注入 | 所有 Agent |
| `chinese-documentation` | 中文文档排版与术语规范 | Jarvis（写文档时） |

### 阶段 2：任务分解
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `planning-and-task-breakdown` | 垂直切片、风险标注、并行识别 | task-design Agent |
| `context-engineering` | 选择性上下文打包 | Jarvis（传递上下文时） |

### 阶段 3：执行规划
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `behavioral-guidelines` | 行为准则 | planner Agent |
| `concurrency-policy` | 并发调用与 Team/Subagent 分配规范 | Jarvis（编排者） |

### 阶段 4：探索（按需）
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `find-docs` | 外部库/框架文档查询（通过 WebSearch/WebFetch） | external-resource-expert Agent |

### 阶段 5：实现
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `source-driven-development` | 先读代码再写代码 | 所有实现 Agent |
| `incremental-implementation` | 小步增量交付、每步可验证 | 所有实现 Agent |
| `test-driven-development` | Red→Green→Refactor 方法论 | 实现 Agent（TDD 任务时） |
| `verification-before-completion` | 交付前自检清单 | 所有实现 Agent |
| `debugging-and-error-recovery` | 系统化调试与根因追踪 | 所有 Agent（遇到 Bug 时） |
| `code-simplification` | 降低复杂度、消除重复 | 所有实现 Agent（Refactor 阶段） |
| `code-standards` | 通用编程规范（注释/嵌套/不可变/设计原则/DDD/外键） | 所有实现 Agent |
| `frontend-design` | 前端 UI/UX 设计方法论与组件设计原则 | 前端实现 Agent |
| `refactoring` | 安全重构流程（准备/执行/验证三阶段） | 所有实现 Agent |
| `behavioral-guidelines` | 行为准则 | 所有 Agent |

### 阶段 6：审查
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `code-review-and-quality` | 五轴审查框架、严重度分级 | qa-review-expert Agent |
| `code-simplification` | 审查时评估简化机会 | qa-review-expert Agent |

### 阶段 7：发布上线
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `shipping-and-launch` | 上线检查清单与灰度策略 | Jarvis |
| `git-workflow-and-versioning` | 分支管理、提交规范、版本管理 | Jarvis |

### 收尾
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `finishing-a-development-branch` | 合并、清理、部署验证 | Jarvis |

### 特殊场景
| 技能 | 用途 | 加载者 |
|------|------|--------|
| `security-and-hardening` | 安全漏洞修复 | 任何 Agent（安全任务时） |
| `debugging-and-error-recovery` | 系统化调试 | 任何 Agent（遇到 Bug 时） |
| `documentation-and-adrs` | 架构决策记录 | Jarvis/planner |
| `context-engineering` | 上下文不足时重置 | 任何 Agent |
| `browser-testing` | 浏览器测试方法论（用例格式/执行流程/报告模板） | browser-test-expert |
| `code-quality-gate` | Gate C1 四项检查（Lint/Type-check/Build/Deps Audit） | Jarvis（Gate C1 时） |
| `mcp-builder` | MCP 服务器构建方法论 | 需要构建自定义 MCP 工具的 Agent |
| `writing-skills` | 技能文件编写与验证 | 创建/编辑技能文件的 Agent |
| `debugging-and-error-recovery` | 调试与错误恢复方法论（含 Chrome DevTools MCP 调试） | frontend-debug-expert |
| `debugging-deep` | 深度调试：内存泄漏/并发竞态/死锁/性能瓶颈 | 复杂 Bug 排查 Agent |
| `perf-testing` | 性能测试方法论（基准测试/负载测试/剖析） | perf-test-expert |
| `security-testing` | 安全测试方法论（OWASP Top 10/渗透测试/安全审计） | security-review-expert |
| `test-data-factory` | 测试数据工厂（fixture/builder/mock/faker） | 测试 Agent |
| `jarvis-reference` | Jarvis 统一能力索引——Agent/命令/Skill/流水线/工具参考 | 所有 Agent（启动时自动加载） |

---

## 编排者视角（Jarvis）

作为编排者，你不需要在每个阶段手动加载所有技能。关键规则：

1. **每个阶段只加载该阶段的核心技能**（1-3 个）
2. **通过 Execution Packet 传递技能清单**——planner 在 `required_skills` 字段指定该任务需要的技能；编排者 spawn 子 Agent 时原样传递；子 Agent 启动后逐一 `Skill()` 加载
3. **behavioral-guidelines 是所有 Agent 的基座**——每个 Agent 都会自动遵守
4. **context-engineering 在三个关键时刻使用**：启动新会话、任务切换、子 Agent 结果偏离预期时

---

## 如何加载技能

在 Claude Code 中，技能通过 `Skill` 工具加载：

```
Skill(skill="<技能名>")
```

加载技能后，技能的方法论和约束会融入当前会话上下文。

---

## 如何扩展技能系统

### 新增技能

1. 在 `.claude/skills/` 下创建目录：`.claude/skills/<skill-name>/`
2. 创建 `SKILL.md` 文件，包含：
   - YAML frontmatter（name、description）
   - 技能正文（何时使用、方法论、反模式、示例）
3. 技能命名遵循 kebab-case

### 技能设计原则

- 每个技能只解决一个问题
- 技能是方法论，不是 Agent——它教人"怎么做好"，但不执行
- 技能之间可以互相引用，但不应循环依赖
- 技能正文应包含：何时用、何时不用、具体步骤、常见错误/反模式

---

## 当前技能列表总览

| # | 技能名 | 类别 | 简要说明 |
|---|--------|------|----------|
| 1 | `behavioral-guidelines` | 基础 | 四项核心行为准则 |
| 2 | `chinese-documentation` | 文档 | 中文文档排版与术语规范 |
| 3 | `code-review-and-quality` | 审查 | 五轴审查框架、严重度分级 |
| 4 | `code-simplification` | 质量 | 降低复杂度、消除重复 |
| 5 | `context-engineering` | 基础 | 选择性上下文、混淆管理 |
| 6 | `documentation-and-adrs` | 架构 | 架构决策记录 |
| 7 | `find-docs` | 探索 | 文档查询（WebSearch/WebFetch） |
| 8 | `finishing-a-development-branch` | 流程 | 分支合并、清理、部署验证 |
| 9 | `git-workflow-and-versioning` | 流程 | Git 工作流与版本管理 |
| 10 | `idea-refine` | 梳理 | 模糊想法 → 结构化问题 |
| 11 | `incremental-implementation` | 实现 | 小步增量交付 |
| 12 | `planning-and-task-breakdown` | 规划 | 垂直切片、风险标注、并行识别 |
| 13 | `security-and-hardening` | 安全 | 安全漏洞修复与加固 |
| 14 | `shipping-and-launch` | 流程 | 上线检查清单与灰度策略 |
| 15 | `source-driven-development` | 实现 | 先读代码再写代码 |
| 16 | `spec-driven-development` | 需求 | 结构化需求规格编写 |
| 17 | `test-driven-development` | 测试 | Red→Green→Refactor 方法论 |
| 18 | `using-agent-skills` | 元技能 | 技能系统使用指南 |
| 19 | `verification-before-completion` | 质量 | 交付前 5 层验证清单 |
| 20 | `browser-testing` | 浏览器 | 浏览器测试方法论（用例/执行/报告/修复闭环） |
| 21 | `code-quality-gate` | 质量 | Gate C1 四项检查（Lint/Type-check/Build/Deps） |
| 22 | `mcp-builder` | 基础设施 | MCP 服务器构建方法论 |
| 23 | `writing-skills` | 元技能 | 技能文件编写与验证 |
| 24 | `debugging-and-error-recovery` | 调试 | 调试与错误恢复方法论（含 Chrome DevTools MCP 调试，性能追踪/渲染分析/网络诊断/控制台调试） |
| 25 | `code-standards` | 实现 | 通用编程规范（注释/嵌套/不可变/设计原则/DDD/外键） |
| 26 | `concurrency-policy` | 基础 | 并发调用与 Team/Subagent 分配规范 |
| 27 | `debugging-deep` | 调试 | 深度调试：内存泄漏/并发竞态/死锁/性能瓶颈 |
| 28 | `frontend-design` | 实现 | 前端 UI/UX 设计方法论与组件设计原则 |
| 29 | `perf-testing` | 测试 | 性能测试方法论（基准测试/负载测试/剖析） |
| 30 | `refactoring` | 实现 | 安全重构流程与模式（准备/执行/验证三阶段） |
| 31 | `security-testing` | 安全 | 安全测试方法论（OWASP Top 10/渗透测试/安全审计） |
| 32 | `session-memory` | 基础 | 跨会话记忆与上下文注入 |
| 33 | `test-data-factory` | 测试 | 测试数据工厂（fixture/builder/mock/faker 策略） |
| 34 | `jarvis-reference` | 参考 | Jarvis 统一能力索引（Agent/命令/Skill/流水线/工具） |
